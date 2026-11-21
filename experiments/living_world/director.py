"""Authoritative, save-scoped plans for the reachable Pewter demonstration."""

from dataclasses import asdict, dataclass
import json
from time import perf_counter

GYM = "gym"
COURT = "museum_forecourt"
TRAVEL = "in_transit"
PRESENCE = {GYM: 0, TRAVEL: 1, COURT: 2}
REPORT = "museum_cast_comparison"
SOURCE = "pewter_museum_researcher"
DAY = 86400
COOLDOWN = 180
MAX_ABSENCE = 90
# The Gym door opens onto Pewter. The forecourt is on that same map, outside
# Museum admission. This graph has no Route 3 or Mt. Moon edge.
ROUTES = {(GYM, COURT): 12, (COURT, GYM): 12}


@dataclass(frozen=True)
class Step:
    action: str
    target: str


@dataclass(frozen=True)
class Action:
    duration: int
    location: str
    target: str
    effect: str
    needs_report: bool = False


ACTIONS = {
    "WORK": Action(20, GYM, GYM, "finish planning the next Gym challenge"),
    "TRAIN_POKEMON": Action(28, GYM, GYM, "finish a training session"),
    "REST": Action(20, GYM, GYM, "finish a short rest"),
    "TRAVEL_TO": Action(0, GYM, COURT, "arrive at the forecourt", True),
    "VISIT_NPC": Action(8, COURT, SOURCE, "meet the researcher", True),
    "INVESTIGATE": Action(42, COURT, REPORT, "complete the exhibit comparison", True),
    "SHARE_INFORMATION": Action(4, COURT, SOURCE, "record the exhibit comparison", True),
    "RETURN_TO_DUTY": Action(0, COURT, GYM, "resume Gym duty"),
}


@dataclass(frozen=True)
class Plan:
    goal: str
    steps: tuple[Step, ...]


DUTY = Plan("prepare_challenges", (Step("WORK", GYM),))
TRAIN = Plan("practice_rock_type_training", (Step("TRAIN_POKEMON", GYM), Step("REST", GYM)))
TRIP = Plan("compare_museum_cast", (
    Step("TRAVEL_TO", COURT), Step("VISIT_NPC", SOURCE), Step("INVESTIGATE", REPORT),
    Step("SHARE_INFORMATION", SOURCE), Step("RETURN_TO_DUTY", GYM),
))


@dataclass(frozen=True)
class Decision:
    checkpoint: str
    number: int
    trigger: str
    report: bool
    hour: int
    plans: tuple[Plan, ...]
    comparisons: int
    expected_challenger: bool
    notice: str | None = None


def choose_brock(model, decision):
    """The worker supplies a constrained choice, never a command or location."""
    labels = ("DUTY", "TRAIN", "VISIT")
    labels = labels[:len(decision.plans)]
    instructions = (
        "You are Brock, the responsible Pewter Gym Leader and a Rock-type specialist. "
        "You like to train and study stones. Honor your duty to challengers. "
        "Select one plan by its label. Output only the label."
    )
    context = (
        f"Time {decision.hour}:00. You are at your Gym and free for one short activity. "
        + ("A museum researcher personally asks you to compare a rock cast at the free forecourt. "
           "The attendant can tell challengers your plans. VISIT: walk there, meet the researcher, "
           "inspect the cast, share notes, and return before your duty deadline. "
           if TRIP in decision.plans else
           "The museum researcher asked for help, but you have a Gym commitment. "
           if decision.report else "You have heard no current research request. ")
        + (f"You have finished {decision.comparisons} past exhibit comparisons. " if decision.comparisons else "")
        + ("A challenger is already expected. Prefer DUTY. " if decision.expected_challenger or decision.trigger == "gym_duty" else
           "Your scheduled team practice is due. Prefer TRAIN. " if decision.trigger == "practice" else
           "The researcher is ready now. The next Gym challenge is still some time away. ")
        + "DUTY: stay and prepare the Gym. TRAIN: train and recover at the Gym."
    )
    start = perf_counter()
    if model.style != "qwen3":
        raise ValueError("Brock planning needs the bundled Qwen3 worker")
    grammar = "root ::= " + " | ".join(json.dumps(label) for label in labels)
    raw, metrics = model.worker.generate(grammar, model.render_prompt(instructions, context))
    try:
        index = labels.index(raw.strip())
    except ValueError as error:
        raise ValueError("Brock returned a choice outside the proposed plans") from error
    return decision.plans[index], {**metrics, "decision_ms": (perf_counter() - start) * 1000}


def initial_state():
    return dict(number=0, busy_until=-1, last_ready=-1, clock=-1, location=GYM,
                activity="gym_duty", active=None, history=[], quest=None, attempted=[],
                research=None, familiarity=0, challenger_until=-1, appointment=None)


class WorldDirector:
    """One plan and one location per agent, using the battery checkpoint key."""

    def __init__(self, memory):
        self.memory = memory
        self.demo = False
        self.notice_required = False
        self.notice = None
        self.offscreen = False
        self.db = memory.db
        with self.db:
            self.db.execute("CREATE TABLE IF NOT EXISTS director_state (save TEXT PRIMARY KEY, state TEXT NOT NULL)")
        self.load()

    def load(self):
        row = self.db.execute("SELECT state FROM director_state WHERE save=?", (self.memory.save,)).fetchone()
        self.state = initial_state()
        if row:
            self.state.update(json.loads(row[0]))
        self.context = None

    def persist(self):
        with self.db:
            self.db.execute("INSERT OR REPLACE INTO director_state VALUES (?, ?)",
                            (self.memory.save, json.dumps(self.state, separators=(",", ":"))))

    def checkpoint(self, key):
        self.db.execute("INSERT INTO director_state SELECT ?, state FROM director_state WHERE save=?",
                        (key, self.memory.save))

    def discard(self):
        self.db.execute("DELETE FROM director_state WHERE save=?", (self.memory.save,))

    @property
    def location(self):
        return self.state["location"]

    def record(self, status, **details):
        self.state["history"] = [*self.state["history"][-31:], {
            "time": self.state["clock"], "status": status, **details,
        }]

    def observe(self, second, area, protected, busy=False):
        """Clock and story are ROM observations, never model output."""
        self.context = (second, area, protected, busy)
        if second is None:
            if self.state["active"]:
                self.finish("clock_unavailable")
            return
        if self.state["clock"] > second:
            if self.state["active"]:
                self.finish("clock_reversed")
            return
        self.state["clock"] = second
        active = self.state["active"]
        if active is None:
            return
        if protected:
            self.finish("protected_progression")
            return
        if second >= active["deadline"]:
            self.finish("return_deadline")
            return
        if second >= active["due"]:
            self.advance(second)

    def decision(self):
        if self.context is None or self.state["active"]:
            return None
        second, area, protected, busy = self.context
        if (second is None or (area != "pewter" and not (self.offscreen and area != "pewter_gym"))
                or protected or busy or
                second < self.state["clock"] or second < self.state["busy_until"]):
            return None
        hour = second % DAY // 3600
        day = second // DAY
        # A curator working the exhibit, an expected Gym challenge, and
        # scheduled training are distinct causal triggers.
        if 10 <= hour < 16 or (self.demo and self.state["number"] == 0):
            trigger = "research_request"
        else:
            trigger = "practice" if 16 <= hour < 20 else "gym_duty"
        bucket = day * 3 + {"gym_duty": 0, "research_request": 1, "practice": 2}[trigger]
        if bucket in self.state["attempted"] or self.state["last_ready"] == bucket:
            return None
        expected = second < self.state["challenger_until"]
        report = trigger == "research_request"
        if report and self.notice_required and not (self.notice or self.demo):
            return None
        choices = (DUTY, TRAIN, TRIP) if report and not expected else (DUTY, TRAIN)
        return Decision(self.memory.save, bucket, trigger, report, hour, choices,
                        self.state["familiarity"], expected, self.notice if report else None)

    def validate(self, decision, plan):
        if decision != self.decision():
            raise ValueError("Planning context changed or another commitment exists")
        if plan not in decision.plans:
            raise ValueError("Plan is outside Brock's available goals")
        location, elapsed = GYM, 0
        for step in plan.steps:
            spec = ACTIONS.get(step.action)
            if spec is None or spec.target != step.target or spec.location != location:
                raise ValueError("Unsupported action, destination, or step order")
            if spec.needs_report and not decision.report:
                raise ValueError("Brock has no sourced research appointment")
            elapsed += spec.duration
            if step.action in ("TRAVEL_TO", "RETURN_TO_DUTY"):
                elapsed += ROUTES[location, step.target]
                location = step.target
        if location != GYM or elapsed >= MAX_ABSENCE:
            raise ValueError("Plan does not keep the Gym return commitment")

    def submit(self, decision, plan, *, fallback=None):
        self.validate(decision, plan)
        now = self.state["clock"]
        self.state["busy_until"] = now + COOLDOWN
        self.state["last_ready"] = decision.number
        self.state["attempted"] = [*self.state["attempted"][-5:], decision.number]
        if decision.report:
            self.state["research"] = dict(id=f"{REPORT}:{decision.number}", source=SOURCE,
                                          learned=now, origin="request", status="reported")
        self.state["number"] += 1
        self.state["active"] = dict(id=self.state["number"], goal=plan.goal, steps=[asdict(s) for s in plan.steps],
                                    index=0, due=now, deadline=now + MAX_ABSENCE,
                                    trigger=decision.trigger, report_source=SOURCE if decision.report else None,
                                    departure_notice=plan == TRIP)
        self.record("approved", plan=plan.goal, cause=decision.trigger, fallback=fallback)
        self.start_step(now)

    def start_step(self, second):
        active = self.state["active"]
        step = Step(**active["steps"][active["index"]])
        spec = ACTIONS[step.action]
        report = self.state["research"]
        if (spec.location != self.location or
                (spec.needs_report and (not report or report["source"] != active["report_source"]
                                        or second - report["learned"] >= MAX_ABSENCE))):
            self.finish("precondition_changed")
            return
        if spec.duration:
            duration = spec.duration
        else:
            duration = ROUTES[self.location, step.target]
            self.state["location"] = TRAVEL
        active["due"] = second + duration
        self.state["activity"] = step.action
        self.persist()

    def advance(self, second):
        active = self.state["active"]
        step = Step(**active["steps"][active["index"]])
        expected = TRAVEL if step.action in ("TRAVEL_TO", "RETURN_TO_DUTY") else ACTIONS[step.action].location
        if self.location != expected:
            self.finish("location_changed")
            return
        if expected == TRAVEL:
            self.state["location"] = step.target
        if step.action == "SHARE_INFORMATION":
            self.state["research"].update(status="compared", compared_at=second, origin="firsthand")
            self.state["familiarity"] = min(100, self.state["familiarity"] + 1)
        self.record("step_complete", step=step.action, effect=ACTIONS[step.action].effect)
        active["index"] += 1
        if active["index"] == len(active["steps"]):
            self.finish("completed")
        else:
            self.start_step(second)

    def finish(self, reason):
        active = self.state["active"]
        self.record(reason, plan=active["goal"] if active else None)
        self.state.update(active=None, location=GYM, activity="gym_duty")
        if self.state["research"] and self.state["research"]["status"] == "reported":
            self.state["research"]["status"] = "expired"
        quest = self.state["quest"]
        if self.state["appointment"] and self.state["appointment"]["status"] == "scheduled":
            self.state["appointment"]["status"] = "ready_at_gym"
        if quest and quest["status"] == "seeking":
            quest.update(status="returned", clue=GYM, source="gym_attendant_return_commitment")
        self.persist()

    def challenger(self):
        if self.state["clock"] >= 0 and self.location == GYM:
            self.state["challenger_until"] = self.state["clock"] + COOLDOWN
            self.persist()

    def message(self, npc, *, accepted=False):
        """Player clues derive from a notice Brock left and confirmed contact."""
        active = self.state["active"]
        quest = self.state["quest"]
        if npc == "brock_attendant" and self.location != GYM and active and active["departure_notice"]:
            returning = self.state["activity"] == "RETURN_TO_DUTY"
            if accepted and (not quest or quest["plan"] != active["id"]):
                self.state["quest"] = dict(plan=active["id"], status="seeking",
                                           clue=GYM if returning else COURT,
                                           source="brock_departure_notice")
                self.persist()
            clue = ("Brock said he'd return.\nPlease check back here." if returning else
                    "Brock told me he was headed\nto the Museum forecourt.")
            return clue + "\fLocate Brock\nMeet him or return here."
        if npc == "brock_contact" and self.location == COURT:
            if accepted and quest and quest["status"] == "seeking":
                quest.update(status="contacted", clue=COURT, source="firsthand_brock")
                self.state["appointment"] = dict(plan=active["id"], due_by=active["deadline"],
                                                 location=GYM, status="scheduled")
                self.record("appointment", source="firsthand_brock", location=GYM,
                            due_by=active["deadline"])
                self.persist()
            return "I'll be back at the Gym\nsoon. Meet me there."
        if self.location == GYM and quest and quest["status"] in ("seeking", "returned"):
            if npc == "brock_attendant":
                return "Brock is back on duty.\nHis challenge is at the Gym."
            if npc == "brock_return":
                if accepted:
                    quest.update(status="completed_at_gym", clue=GYM, source="firsthand_brock")
                    self.persist()
                return "Good to see you.\nReady for our challenge?"
        return None
