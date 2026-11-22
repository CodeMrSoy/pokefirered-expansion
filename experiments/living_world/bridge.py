"""Reference host for the Living Quantum World dialogue mailbox."""

import json
import re
import struct
import time
from dataclasses import dataclass

from profiles import NPC_IDS
from kanto import HOOKS
from autonomy import DESK, OFFER, REPORT
from world_rules import HOOKS as EVOLUTION_HOOKS

REQUEST = struct.Struct("<4sIHH")
REPLY_OFFSET = REQUEST.size
TEXT_CAPACITY = 115
MAILBOX_SIZE = 132
LINE = re.compile(r"[A-Za-z0-9 !?.,':-]{1,28}")
REQUEST_IDS = {**NPC_IDS, 10: "pallet_exchange", 11: "guide_followup",
               14: "brock_attendant", 15: "brock_contact", 16: "brock_return",
               17: "society_assistant", 18: "society_trainer", 19: "society_researcher", **HOOKS, 26: OFFER, 27: REPORT, 28: DESK, **EVOLUTION_HOOKS}
WAIT = object()
SKIP = object()


@dataclass(frozen=True)
class Conversation:
    npc: str
    visible_species: int | None


def unique_fields(pairs):
    fields = dict(pairs)
    if len(fields) != len(pairs):
        raise ValueError("Duplicate JSON field")
    return fields


def validate(raw):
    if not isinstance(raw, str) or len(raw) > 512:
        raise ValueError("Proposal exceeds the input limit")
    proposal = json.loads(raw, object_pairs_hook=unique_fields)
    if not isinstance(proposal, dict) or set(proposal) != {"action", "text"}:
        raise ValueError("Expected action and text fields")
    if proposal["action"] != "SAY_DIALOGUE" or not isinstance(proposal["text"], str):
        raise ValueError("Only SAY_DIALOGUE with plain text is available")
    pages = proposal["text"].split("\f")
    if len(pages) > 2:
        raise ValueError("Expected at most two short pages")
    for page in pages:
        lines = page.split("\n")
        if len(lines) > 2 or any(not LINE.fullmatch(line) or not line.strip() for line in lines):
            raise ValueError("Expected one or two short lines of plain text per page")
    return proposal["text"].encode("ascii")


class DialogueBridge:
    """Poll and publish on the emulator thread, exclusively between frames."""

    def __init__(self, read, write, mailbox_address, *, deferred=False):
        if mailbox_address % 4 or not 0x02000000 <= mailbox_address <= 0x02040000 - MAILBOX_SIZE:
            raise ValueError("Mailbox must be aligned and contained within EWRAM")
        self.read = read
        self.write = write
        self.address = mailbox_address
        self.handled = None
        self.pending = None
        self.deferred = deferred
        self.started = 0
        self.sequence = 0

    def _signal(self, sequence, length):
        self.write(self.address + REPLY_OFFSET + 4, bytes([length]))
        self.write(self.address + REPLY_OFFSET, struct.pack("<I", sequence))

    def poll(self, propose):
        header = self.read(self.address, REQUEST.size)
        magic, sequence, npc, species = REQUEST.unpack(header)
        if magic != b"LQW1":
            self.handled = None
            self.pending = None
            return None
        if not sequence or npc not in REQUEST_IDS or self.handled == header:
            return None

        context = Conversation(REQUEST_IDS[npc], species or None)
        self.sequence = sequence
        trace = {"context": vars(context), "sequence": sequence, "changes": []}
        if self.pending != header:
            self.started = time.perf_counter()
        try:
            raw = propose(context)
            if self.read(self.address, REQUEST.size) != header:
                raise ValueError("Request changed before publication")
            if self.deferred and raw is WAIT:
                if self.pending != header:
                    self._signal(sequence, 255)
                    self.pending = header
                return None
            if self.deferred and raw is SKIP:
                self._signal(sequence, 0)
                trace.update(validation="skipped")
                self.handled, self.pending = header, None
                return trace
            trace["proposal"] = raw[:512] if isinstance(raw, str) else None
            validate_start = time.perf_counter()
            payload = validate(raw)
            validated = time.perf_counter()
            self.write(self.address + REPLY_OFFSET + 4, bytes([len(payload)]) + payload)
            self.write(self.address + REPLY_OFFSET, struct.pack("<I", sequence))
            trace["validation_ms"] = (validated - validate_start) * 1000
            trace["handoff_ms"] = (time.perf_counter() - validated) * 1000
            trace["validation"] = "accepted"
            trace["changes"] = ["reply published to mailbox"]
        except ValueError as error:
            trace.update(validation="rejected", error=str(error))
        except Exception as error:
            trace.update(validation="error", error=f"{type(error).__name__}: {error}"[:320])
        if self.deferred and trace["validation"] != "accepted" and self.read(self.address, REQUEST.size) == header:
            self._signal(sequence, 0)
        self.handled, self.pending = header, None
        trace["elapsed_ms"] = round((time.perf_counter() - self.started) * 1000, 3)
        return trace
