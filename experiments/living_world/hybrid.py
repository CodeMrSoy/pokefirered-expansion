"""Save-scoped dialogue planning, bounded prediction and response routing."""

from collections import OrderedDict
from concurrent.futures import Future
from dataclasses import dataclass, replace
import json
import struct
from time import perf_counter

from bridge import Conversation, validate
from inference import Proposal, SURVEY_OFFER, dialogue_options
from kanto import AREAS as KANTO_AREAS
from knowledge import retrieve, retrieve_examples
from profiles import KNOWLEDGE_PROFILES, NPC_IDS, PROFILES
from reasoning import GuideTurn
from world import Encounter

AREAS = {0: "", 1: "pallet", 2: "rival_house", 3: "oak_lab", 4: "route_1", 5: "viridian", 6: "pewter", 7: "pewter_gym", 8: "route_2", **KANTO_AREAS}
PREDICTION_DELAY = 0.2
MAX_REPLIES = 32
FIELD_HINT = struct.Struct("<4sHHBBBB")
FIELD_CLOCK = struct.Struct("<I")
FIELD_SIZE = FIELD_HINT.size + FIELD_CLOCK.size


@dataclass(frozen=True)
class FieldHint:
    frame: int
    species: int | None
    area: str
    story: int
    npc: str | None
    busy: bool
    local_second: int | None = None
    early_kanto_open: bool = False

    @classmethod
    def decode(cls, raw):
        magic, frame, species, area, story, npc, distance = FIELD_HINT.unpack_from(raw)
        if magic != b"LQP1" or area not in AREAS:
            return None
        area = AREAS[area]
        candidate = NPC_IDS.get(npc) if distance <= 7 else None
        if candidate and KNOWLEDGE_PROFILES[candidate][0] != area:
            candidate = None
        second = FIELD_CLOCK.unpack_from(raw, FIELD_HINT.size)[0] if len(raw) == FIELD_SIZE else 0xFFFFFFFF
        return cls(frame, (species & 0x7FFF) or None, area, story, candidate, distance == 255,
                   second if second != 0xFFFFFFFF else None, bool(species & 0x8000))


@dataclass(frozen=True)
class NpcState:
    encounter: Encounter
    area: str
    story: int
    activity: str
    goal: str
    secondary_goal: str
    concern: str
    topic: str
    intentions: tuple[str, ...]
    reports: tuple[GuideTurn, ...]


@dataclass(frozen=True)
class ReplyKey:
    save: str
    catalog: tuple
    state: NpcState


@dataclass(frozen=True)
class Lookup:
    key: ReplyKey
    future: Future
    cache: str
    state_ms: float
    lookup_ms: float


def npc_state(memory, conversation, hint=None):
    encounter = memory.context(conversation)
    area = KNOWLEDGE_PROFILES[encounter.npc][0]
    story = hint.story if hint and hint.area == area else 0
    profile = PROFILES[encounter.npc]
    intentions = encounter.allowed()
    topic = "companion" if encounter.visible_species else "greeting"
    concern = ""
    reports = ()
    if encounter.npc == "pc_resident" and (encounter.quest != "none" or "PROPOSE_OPTIONAL_QUEST" in intentions):
        topic, concern = "pond_survey", encounter.quest
    elif encounter.npc == "sign_guide" and any(x.startswith("conversation:pallet-sighting:") for x in encounter.evidence):
        topic, concern = "local_sightings", "attribute_secondhand_information"
        reports = tuple(memory.social.guide_turn(x.removeprefix("conversation:")) for x in encounter.evidence
                        if x.startswith("conversation:pallet-sighting:"))
        if any(report.requested for report in reports):
            concern = "check_the_sighting_details"
    routine = memory.routines.state(encounter.npc)
    if routine:
        activity, goal = routine
        if not concern:
            concern = goal
    else:
        activity = profile["role"]
    return NpcState(encounter, area, story, activity,
                    profile["primary_goal"], profile["secondary_motivation"], concern, topic, intentions, reports)


def needs_model(state):
    return "PROPOSE_OPTIONAL_QUEST" in state.intentions


def prepare(model, state, *, fallback=False):
    encounter = state.encounter
    modeled = needs_model(state) and not fallback and model.style != "unavailable"
    if modeled:
        selected, model_metrics, context = model.survey(encounter)
    start = perf_counter()
    # This is the same permissions query used by the model path.
    facts = retrieve(model.catalog, encounter) if model.catalog else ()
    examples = retrieve_examples(model.catalog, encounter) if model.catalog else ()
    retrieved = perf_counter()
    species = model.species_names.get(str(encounter.visible_species))
    first, second = dialogue_options(species, encounter, facts)
    # A learned fact owns the factual line. Authored examples add a voice only.
    opening = examples[0] if examples and state.topic != "pond_survey" else first[0]
    ending = second[0]
    report = next((report for report in state.reports if report.fact and
                   any(fact.key == report.fact and fact.line == ending for fact in facts)), None)
    if report and report.requested:
        opening = "Watts wasn't sure when." if report.answered else "I asked him for details."
    if encounter.npc == "route_scout":
        opening = {"record_report": "I'll pass this note along.",
                   "write_field_notes": "I'm sorting my field notes.",
                   "watch_the_route": "I keep an eye on the ledges."}.get(state.activity, opening)
    if encounter.npc == "viridian_student":
        opening = {"compare_report": "I'm checking that report.",
                   "rest": "My field notes can wait.",
                   "study_trail_habitats": "I'm studying trail habitats."}.get(state.activity, opening)
    action = next((option for option in state.intentions if option in (
        "ADJUST_RELATIONSHIP", "REMEMBER_EVENT", "COMMENT_ON_POKEMON", "SAY_DIALOGUE",
    )), "SAY_DIALOGUE")
    if modeled:
        if selected not in state.intentions:
            raise ValueError("Invalid survey intention")
        action = selected
    text = SURVEY_OFFER if action == "PROPOSE_OPTIONAL_QUEST" else opening + "\n" + ending
    raw = json.dumps({"action": "SAY_DIALOGUE", "text": text})
    before_validation = perf_counter()
    validate(raw)
    return Proposal(raw, action, {
        "inference_ms": 0.0,
        **(model_metrics if modeled else {}),
        "retrieval_ms": (retrieved - start) * 1000,
        "context_ms": (before_validation - retrieved) * 1000 + (model_metrics["context_ms"] if modeled else 0),
        "proposal_validation_ms": (perf_counter() - before_validation) * 1000,
    }, context if modeled else "", tuple(fact.key for fact in facts)), (
        "model_decision" if modeled else "fallback" if fallback or needs_model(state) else
        "retrieved_dialogue" if facts else "authored_dialogue"
    )


class HybridDialogue:
    """One speculative model job, a small LRU, and fresh authorization per use."""

    def __init__(self, memory, model, executor, *, ecology_sighting=None):
        self.memory = memory
        self.model = model
        self.executor = executor
        self.ecology_sighting = ecology_sighting
        self.replies = OrderedDict()
        self.speculative = None
        self.obsolete = None
        self.candidate = None
        self.since = 0.0
        self.prepared = False

    def key(self, conversation, hint=None):
        stat = self.model.catalog.stat() if self.model.catalog else None
        version = (stat.st_dev, stat.st_ino, stat.st_mtime_ns, stat.st_size) if stat else ()
        state = npc_state(self.memory, conversation, hint)
        if self.ecology_sighting and hint and hint.npc == conversation.npc and hint.area == state.area:
            fact = self.ecology_sighting(conversation.npc)
            if fact is not None:
                state = replace(state, encounter=replace(state.encounter, ecology=fact))
        return ReplyKey(self.memory.save, version, state)

    def _remember(self, key, future):
        self.replies[key] = future
        self.replies.move_to_end(key)
        if len(self.replies) > MAX_REPLIES:
            self.replies.popitem(last=False)
        return future

    def _get(self, key):
        future = self.replies.get(key)
        if future is not None and (future.cancelled() or (future.done() and future.exception() is not None)):
            del self.replies[key]
            return None
        if future is not None:
            self.replies.move_to_end(key)
        return future

    def _discard_speculative(self):
        if self.speculative is None:
            return
        key, future = self.speculative
        if not future.done():
            self.replies.pop(key, None)
            if not future.cancel():
                self.obsolete = future
        self.speculative = None

    def predict(self, hint, now):
        if not hint or not hint.npc:
            # An active script temporarily suppresses prediction. Foreground
            # request() owns promotion/cancellation while talking.
            if hint is None or not hint.busy:
                self._discard_speculative()
                self.candidate = None
            return None
        key = self.key(Conversation(hint.npc, hint.species), hint)
        if self.speculative and self.speculative[0] != key:
            self._discard_speculative()
        if self.candidate != key:
            self.candidate, self.since = key, now
            self.prepared = False
            return None
        if self.prepared or now - self.since < PREDICTION_DELAY or self._get(key):
            return None
        if needs_model(key.state) and self.model.style != "unavailable":
            if self.obsolete is not None and not self.obsolete.done():
                return None
            future = self.executor.submit(prepare, self.model, key.state)
            self.speculative = (key, future)
        else:
            future = Future()
            future.set_result(prepare(self.model, key.state))
        self._remember(key, future)
        self.prepared = True
        return key

    def request(self, conversation, hint=None):
        start = perf_counter()
        key = self.key(conversation, hint)
        retrieved = perf_counter()
        future = self._get(key)
        cache = "hit" if future is not None and future.done() else "pending" if future is not None else "miss"
        if self.speculative:
            if self.speculative[0] == key:
                self.speculative = None
            else:
                self._discard_speculative()
        lookup_ms = (perf_counter() - retrieved) * 1000
        if future is None:
            if needs_model(key.state) and self.model.style != "unavailable":
                future = self.executor.submit(prepare, self.model, key.state)
            else:
                future = Future()
                future.set_result(prepare(self.model, key.state))
            self._remember(key, future)
        return Lookup(key, future, cache, (retrieved - start) * 1000, lookup_ms)

    def worker_idle(self):
        return not ((self.obsolete is not None and not self.obsolete.done())
                    or any(not reply.done() for reply in self.replies.values()))

    def prioritize_followup(self):
        self._discard_speculative()
