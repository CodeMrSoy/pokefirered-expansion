"""Passively observe the native player session and persist checkpointed history."""
from collections import deque
from concurrent.futures import ThreadPoolExecutor
from contextlib import closing
from dataclasses import dataclass
import ctypes as c
from hashlib import sha256
import sqlite3
from struct import Struct
from time import perf_counter_ns
from uuid import uuid4

import ecology
import trainers
from native_world import ewram_pointer
from simulation.engine import Simulation, encoded
from world_initialization import PairedCheckpoints, flash_identity

MAGIC = 0x3831574C
HEADER = Struct("<8I")
RECORD = Struct("<11I7H6B")
KINDS = ("map", "story", "battle_start", "battle_mon", "battle_end", "ball_failed",
         "capture", "party", "evolution", "save")
OUTCOMES = {1: "won", 2: "lost", 3: "draw", 4: "player_escaped", 5: "player_teleported",
            6: "wild_fled", 7: "caught", 8: "out_of_safari_balls", 9: "forfeited",
            10: "wild_teleported"}
BATCH = 24
PENDING_LIMIT = 384
FRAMES_PER_TICK = 3600


def unpack_event(raw):
    seq, frame, kind, map_id, battle, actor, value, flags, pid, ot, ivs, species, ability, item, *tail = RECORD.unpack(raw)
    if not 1 <= kind <= len(KINDS) or map_id > 0xFFFF:
        raise ValueError("Unsupported native observation")
    name = KINDS[kind - 1]
    moves = tail[:4]
    level, nature, ball, slot, ability_slot, egg = tail[4:]
    mon = None
    if species:
        mon = dict(species=species, personality=pid, ot=ot, ivs=ivs, egg=bool(egg), slot=slot,
                   ability=None if egg else ability, ability_slot=None if egg else ability_slot,
                   level=None if egg else level, nature=None if egg else nature,
                   ball=None if egg else ball, item=None if egg else item, moves=None if egg else moves)
    return dict(seq=seq, frame=frame, kind=name, source="native_rom", map=[map_id >> 8, map_id & 255],
                battle=battle or None, actor=actor or None, value=value, flags=flags,
                slot=slot if name == "party" else None, mon=mon,
                battle_kind=("trainer" if flags & 8 else "wild") if battle else None,
                outcome=OUTCOMES.get(value, "unknown") if name == "battle_end" else None)


class NativeObservations:
    """Cursor owned by the host. Nothing is written to emulator memory."""
    def __init__(self, address):
        self.address = address
        self.generation = None
        self.frame = None
        self.sequence = 0
        self.last = None

    def read(self, memory, expected_generation):
        base = ewram_pointer(memory, self.address, HEADER.size)
        magic, version, capacity, size, generation, latest, frame, _ = HEADER.unpack(c.string_at(base, HEADER.size))
        if magic != MAGIC:
            if self.generation is not None:
                raise ValueError("Native observation timeline reset")
            return None, []
        if (version, capacity, size, generation) != (1, 48, RECORD.size, expected_generation):
            raise ValueError("Incompatible observation ABI or generation")
        ewram_pointer(memory, self.address, HEADER.size + capacity * size)
        if self.generation is not None and (generation != self.generation or latest < self.sequence
                                           or not 0 <= frame - self.frame <= 8):
            raise ValueError(f"Native timeline rolled back or jumped ({self.frame}:{self.sequence} → {frame}:{latest})")

        def raw(seq):
            return c.string_at(base + HEADER.size + ((seq - 1) % capacity) * size, size)

        if latest - self.sequence >= capacity:
            raise ValueError("Native observation ring overrun")
        if self.last is not None and raw(self.sequence) != self.last:
            raise ValueError("Previously read native observation changed")
        rows = []
        for seq in range(self.sequence + 1, latest + 1):
            data = raw(seq)
            event = unpack_event(data)
            if event["seq"] != seq or event["frame"] > frame:
                raise ValueError("Inconsistent native observation record")
            rows.append(event)
        if rows:
            self.last = data
        self.generation, self.frame, self.sequence = generation, frame, latest
        return frame, rows


SCHEMA = (
    "CREATE TABLE IF NOT EXISTS native_streams (stream TEXT PRIMARY KEY, world TEXT NOT NULL, "
    "manifest TEXT NOT NULL, checkpoint TEXT, ack INTEGER NOT NULL DEFAULT 0)",
    "CREATE TABLE IF NOT EXISTS native_events (stream TEXT NOT NULL, seq INTEGER NOT NULL, tick INTEGER NOT NULL, "
    "event TEXT NOT NULL, PRIMARY KEY(stream,seq))",
    "CREATE TABLE IF NOT EXISTS observed_pokemon (id TEXT PRIMARY KEY, owner TEXT, location TEXT NOT NULL, "
    "attributes TEXT NOT NULL, last_event TEXT NOT NULL)",
    "CREATE TABLE IF NOT EXISTS observed_aliases (transient TEXT PRIMARY KEY, individual TEXT NOT NULL)",
    "CREATE TABLE IF NOT EXISTS observed_party (slot INTEGER PRIMARY KEY, individual TEXT)",
    "CREATE TABLE IF NOT EXISTS native_ticks (stream TEXT NOT NULL, frame INTEGER NOT NULL, PRIMARY KEY(stream,frame))",
    "CREATE TABLE IF NOT EXISTS native_clock (slot INTEGER PRIMARY KEY CHECK(slot=1), remaining INTEGER NOT NULL)",
    "CREATE VIEW IF NOT EXISTS native_event_journal AS SELECT e.stream || ':' || e.seq AS event_id, "
    "s.world, s.manifest, s.checkpoint, e.stream, e.seq, e.tick, e.event, s.ack "
    "FROM native_events e JOIN native_streams s ON e.stream=s.stream",
)


def project_mon(db, stream, event, event_id):
    mon = event["mon"]
    kind = event["kind"]
    if kind == "party" and not mon:
        db.execute("DELETE FROM observed_party WHERE slot=?", (event["slot"],))
        return
    if not mon or kind not in {"battle_mon", "party", "capture", "evolution"}:
        return
    transient = f"{stream}:{event['battle']}:{mon['slot']}"
    if kind == "battle_mon":
        individual = transient
        owner = f"trainer:{event['actor']}" if event["actor"] else None
    elif kind == "capture" and event["value"] not in (0, 1):
        return  # Native party and PC both rejected the handoff.
    else:
        individual = "player:{ot:08x}:{personality:08x}:{ivs:08x}".format_map(mon)
        owner = "player"
        if kind == "capture":
            db.execute("INSERT OR REPLACE INTO observed_aliases VALUES (?,?)", (transient, individual))
            db.execute("DELETE FROM observed_pokemon WHERE id=?", (transient,))
        if kind == "party":
            db.execute("INSERT OR REPLACE INTO observed_party VALUES (?,?)", (mon["slot"], individual))
    attributes = dict(mon)
    attributes.pop("slot")
    db.execute("INSERT INTO observed_pokemon VALUES (?,?,?,?,?) ON CONFLICT(id) DO UPDATE SET "
               "owner=excluded.owner, location=excluded.location, attributes=excluded.attributes, "
               "last_event=excluded.last_event",
               (individual, owner, encoded(event["map"]), encoded(attributes), event_id))


def append_events(sim, stream, base_checkpoint, events, protection=None):
    """Commit the ordered payload, Pokémon projection and acknowledgment together."""
    with sim._write():
        identity_fields = sim.db.execute(
            "SELECT json_extract(document,'$.world_uuid'), json_extract(document,'$.manifest_sha256') "
            "FROM starting_manifest WHERE slot=1").fetchone()
        if identity_fields is None or None in identity_fields:
            raise ValueError("Native journal needs a valid starting manifest")
        for statement in SCHEMA:
            sim.db.execute(statement)
        identity = (*identity_fields, base_checkpoint)
        sim.db.execute("INSERT OR IGNORE INTO native_streams(stream,world,manifest,checkpoint) VALUES (?,?,?,?)",
                       (stream, *identity))
        world, manifest_hash, checkpoint, ack = sim.db.execute(
            "SELECT world,manifest,checkpoint,ack FROM native_streams WHERE stream=?", (stream,)).fetchone()
        if (world, manifest_hash, checkpoint) != identity:
            raise ValueError("Native event stream belongs to another world or checkpoint")
        tick, = sim.db.execute("SELECT json_extract(state,'$.tick') FROM simulation WHERE slot=1").fetchone()
        ecology.initialize(sim.db, protection)
        ecological = []
        team = []
        for event in events:
            seq = event["seq"]
            payload = encoded(event)
            if seq <= ack:
                previous = sim.db.execute("SELECT event FROM native_events WHERE stream=? AND seq=?",
                                          (stream, seq)).fetchone()
                if previous != (payload,):
                    raise ValueError("Divergent replay of native event")
                continue
            if seq != ack + 1:
                raise ValueError("Noncontiguous native event stream")
            sim.db.execute("INSERT INTO native_events VALUES (?,?,?,?)", (stream, seq, tick, payload))
            event_id = f"{stream}:{seq}"
            project_mon(sim.db, stream, event, event_id)
            if ecology.relevant(event):
                ecological.append((event_id, {"event": event}))
            if event["kind"] == "battle_mon" and event["actor"] and event["mon"]:
                team.append(dict(location=":".join(map(str, event["map"])), trainer=event["actor"],
                                 species=event["mon"]["species"], slot=event["mon"]["slot"]))
            ack = seq
        if team:
            sim._apply_command(dict(kind="native_roster", source="native_rom", team=team))
        ecology.apply(sim.db, ecological)
        sim.db.execute("UPDATE native_streams SET ack=? WHERE stream=?", (ack, stream))
    return ack


def advance_native_clock(sim, stream, frame, protection=None, trainer_proposal=None):
    with sim._write():
        if sim.db.execute("INSERT OR IGNORE INTO native_ticks VALUES (?,?)", (stream, frame)).rowcount:
            ecology.initialize(sim.db, protection)
            if not sim._apply_command(dict(kind="tick"))["accepted"]:
                raise RuntimeError("Live simulation clock transaction failed")
            tick, = sim.db.execute("SELECT json_extract(state,'$.tick') FROM simulation").fetchone()
            if tick % 24 == 0:
                entry = dict(day=tick // 24, trainer_phase=1)
                if trainer_proposal is not None:
                    entry["proposal"] = trainer_proposal
                ecology.apply(sim.db, [(f"day:{tick // 24}", entry)])


@dataclass(frozen=True)
class Checkpoint:
    flash: bytes
    remaining: int
    layout: dict | None = None
    context: dict | None = None
    counter: int | None = None

    def verify(self):
        if self.layout is None:
            return
        identity = flash_identity(self.flash, self.layout, include_counter=True)
        if (not identity or identity.pop("counter") != self.counter
                or any(self.context[key] != value for key, value in identity.items())):
            raise ValueError("Native save marker did not match the Flash image")


def apply_batch(database, checkpoint_path, stream, base, entries, protection=None):
    timings = []
    with closing(Simulation(database)) as sim:
        events = []
        arrivals = []

        def commit_events():
            if events:
                start = perf_counter_ns()
                append_events(sim, stream, base, events, protection)
                completed = perf_counter_ns()
                timings.append(("ingestion", len(events), (completed - start) / 1e6))
                if arrivals:
                    timings.append(("event_latency", len(arrivals), (completed - min(arrivals)) / 1e6))
                events.clear()
                arrivals.clear()

        for kind, value in entries:
            if kind == "event":
                payload = dict(value)
                received = payload.pop("_received_ns", None)
                if received is not None:
                    arrivals.append(received)
                events.append(payload)
                continue
            commit_events()
            start = perf_counter_ns()
            if kind == "tick":
                if isinstance(value, tuple):
                    value, proposal = value
                else:
                    proposal = None
                advance_native_clock(sim, stream, value, protection, proposal)
            elif kind == "checkpoint":
                value.verify()
                with sim._write():
                    sim.db.execute("INSERT OR REPLACE INTO native_clock VALUES (1,?)", (value.remaining,))
                with closing(PairedCheckpoints(checkpoint_path)) as pair:
                    pair.store(value.flash, database)
            timings.append((kind, 1, (perf_counter_ns() - start) / 1e6))
        commit_events()
        summary = None
        if any(kind in ("event", "tick") for kind, _ in entries):
            summary = ecology.monitor(ecology.read_state(sim.db))
            summary["recent_native_individuals"] = ecology.native_individuals(sim.db)
            summary["trainers"] = trainers.load(sim.db)
    return timings, summary


class LiveWorld:
    def __init__(self, startup):
        self.startup = startup
        self.reader = NativeObservations(startup.catalog["ports"]["observation"])
        self.queue = deque()
        self.executor = ThreadPoolExecutor(max_workers=1, thread_name_prefix="native-world")
        self.future = None
        self.stream = str(uuid4())
        self.base = None
        self.next_tick = None
        self.database = None
        self.failure = None
        self.metrics = deque(maxlen=256)
        self.retry = 0
        self.ecology_snapshot = None
        self.trainer_proposal = None
        self.trainer_requested_day = None

    def quarantine(self, reason):
        self.failure = str(reason)
        self.queue.clear()

    def poll(self, game):
        context = self.startup.context
        if self.failure or not context:
            return
        if context["origin"] == 2 and self.startup.database is None and self.reader.generation is None:
            return
        try:
            frame, events = self.reader.read(lambda key: (game.memory(key), game.memory_size(key)),
                                             context["generation"])
            if frame is None:
                return
            if self.reader.generation == context["generation"] and self.next_tick is None:
                remaining = FRAMES_PER_TICK
                if context["origin"] == 2:
                    self.base = sha256(game.save_bytes()).hexdigest()
                    if self.startup.database is not None:
                        with closing(sqlite3.connect(self.startup.database.as_uri() + "?mode=ro", uri=True)) as db:
                            if db.execute("SELECT name FROM sqlite_master WHERE name='native_clock'").fetchone():
                                row = db.execute("SELECT remaining FROM native_clock WHERE slot=1").fetchone()
                                if row and 1 <= row[0] <= FRAMES_PER_TICK:
                                    remaining = row[0]
                self.next_tick = frame + remaining
            if self.startup.task is None and self.startup.database is not None:
                if self.database is not None and self.database != self.startup.database:
                    raise ValueError("Native world attachment changed")
                self.database = self.startup.database

            def advance_until(native_frame):
                while self.database is not None and self.next_tick <= native_frame:
                    value = (self.next_tick, self.trainer_proposal) if self.trainer_proposal is not None else self.next_tick
                    self.queue.append(("tick", value))
                    self.next_tick += FRAMES_PER_TICK

            for event in events:
                advance_until(event["frame"])
                self.queue.append(("event", {**event, "_received_ns": perf_counter_ns()}))
                if event["kind"] == "save":
                    remaining = max(1, min(FRAMES_PER_TICK, self.next_tick - event["frame"]))
                    cut = Checkpoint(game.save_bytes(), remaining, self.startup.catalog["save"],
                                     context, event["value"])
                    self.queue.append(("checkpoint", cut))
            advance_until(frame)
            if len(self.queue) > PENDING_LIMIT:
                raise ValueError("Live world queue overrun")
            self.pump()
        except (OSError, ValueError, RuntimeError, sqlite3.Error) as error:
            self.quarantine(error)

    def pump(self, *, drain=False):
        if self.future is not None and (drain or self.future.done()):
            try:
                timings, summary = self.future.result()
                self.metrics.extend(timings)
                if summary is not None:
                    self.ecology_snapshot = summary
                    if self.trainer_proposal and summary["day"] > self.trainer_proposal["day"]:
                        self.trainer_proposal = None
            except sqlite3.OperationalError:
                if self.retry or self.failure:
                    raise
                # Each operation has a durable idempotency key. Replay an
                # interrupted batch without advancing simulation time twice.
                self.retry += 1
            else:
                if not self.failure:
                    for _ in range(self.inflight):
                        self.queue.popleft()
                self.retry = 0
            self.future = None
        if self.future is None and self.database is not None and self.queue and not self.failure:
            entries = tuple(self.queue[index] for index in range(min(BATCH, len(self.queue))))
            self.inflight = len(entries)
            self.future = self.executor.submit(apply_batch, self.database, self.startup.directory / "checkpoints.sqlite3",
                                               self.stream, self.base, entries,
                                               self.startup.catalog.get("ecology_protected"))

    def trainer_request(self):
        state = (self.ecology_snapshot or {}).get("trainers")
        request = state["request"] if state and not self.failure else None
        if request and request["day"] != self.trainer_requested_day:
            self.trainer_requested_day = request["day"]
            return request
        return None

    def accept_trainer_proposal(self, proposal):
        state = (self.ecology_snapshot or {}).get("trainers")
        if state and not self.failure and proposal["day"] == state["day"]:
            self.trainer_proposal = proposal

    def ecology_sighting(self, npc):
        from knowledge import ecological_fact
        if self.ecology_snapshot is None or self.failure:
            return None
        state = self.ecology_snapshot.get("trainers")
        return ((trainers.fact(state, npc) if state else None) or
                ecological_fact(self.ecology_snapshot["npc_sightings"].get(npc), self.ecology_snapshot["day"]))

    def ecology_monitor(self):
        timings = {kind: round(ms, 3) for kind, _, ms in self.metrics}
        snapshot = dict(self.ecology_snapshot or {})
        if snapshot.get("trainers"):
            snapshot["trainers"] = {key: value for key, value in snapshot["trainers"].items() if key != "request"}
        return {**snapshot, "health": {
            "failure": self.failure, "pending_jobs": len(self.queue), "last_worker_ms": timings}}

    def close(self):
        try:
            while not self.failure and self.database is not None and (self.future is not None or self.queue):
                self.pump(drain=True)
        finally:
            self.executor.shutdown(wait=True)
