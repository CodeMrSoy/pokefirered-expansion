"""Pewter agents advance at decisions and deadlines on the battery checkpoint."""
from dataclasses import dataclass
import json
from time import perf_counter

DAY = 86400


@dataclass(frozen=True)
class Persona:
    role: str
    motive: str
    temperament: str
    duty: str
    hours: tuple[int, int]
    preferred: str


PERSONAS = {
    "researcher": Persona("Pewter fossil researcher", "compare casts with care",
                          "curious and methodical", "museum", (9, 17), "INVESTIGATE"),
}


@dataclass(frozen=True)
class Step:
    action: str
    target: str


@dataclass(frozen=True)
class Ticket:
    save: str
    actor: str
    cause: str
    window: int
    context: str
    choices: tuple[tuple[Step, ...], ...]


DURATIONS = {"WORK": 24, "REST": 16, "INVESTIGATE": 32}


def choose_agent(model, ticket):
    persona = PERSONAS[ticket.actor]
    labels = tuple("ABCDEF"[:len(ticket.choices)])
    instructions = (f"You are the {persona.role}, {persona.temperament}. Your long-term goal is to "
                    f"{persona.motive}. Select an available plan. Output only the choice letter.")
    plans = "\n".join(f"{letter}: " + ", then ".join(f"{s.action} at or with {s.target}" for s in plan)
                      for letter, plan in zip(labels, ticket.choices))
    if model.style != "qwen3":
        raise ValueError("Pewter agent requires the bundled Qwen3 worker")
    prompt = model.render_prompt(instructions, ticket.context + "\n" + plans)
    start = perf_counter()
    raw, metrics = model.worker.generate("root ::= " + " | ".join(map(json.dumps, labels)), prompt)
    if raw.strip() not in labels:
        raise ValueError("Choice outside the actor's action set")
    return ticket.choices[labels.index(raw.strip())], {**metrics, "decision_ms": (perf_counter() - start) * 1000}


class Society:
    def __init__(self, memory):
        self.memory = memory
        self.db = memory.db
        self.db.execute("CREATE TABLE IF NOT EXISTS society_state (save TEXT PRIMARY KEY, state TEXT NOT NULL)")
        self.load()

    def load(self):
        row = self.db.execute("SELECT state FROM society_state WHERE save=?", (self.memory.save,)).fetchone()
        self.state = json.loads(row[0]) if row else dict(visited=False, clock=-1, agents={}, log=[])
        for key, persona in PERSONAS.items():
            self.state["agents"].setdefault(key, dict(location=persona.duty, shift=-1, active=None,
                                                      activity="WORK", facts={}, bonds={}, memory=[]))
        self.now = self.state["clock"]
        self.busy = True

    def persist(self):
        self.state["clock"] = self.now
        with self.db:
            self.db.execute("INSERT OR REPLACE INTO society_state VALUES (?,?)",
                            (self.memory.save, json.dumps(self.state, separators=(",", ":"))))

    def checkpoint(self, key):
        self.db.execute("INSERT INTO society_state SELECT ?,state FROM society_state WHERE save=?",
                        (key, self.memory.save))

    def discard(self):
        self.db.execute("DELETE FROM society_state WHERE save=?", (self.memory.save,))

    def record(self, actor, outcome, **details):
        row = dict(actor=actor, outcome=outcome, second=self.now, **details)
        agent = self.state["agents"][actor]
        agent["memory"] = [*agent["memory"][-7:], row]
        self.state["log"] = [*self.state["log"][-47:], row]

    def tick(self, second, area, busy=False):
        self.busy = busy
        if second is None or second < self.now:
            self.busy = True
            return
        self.now = second
        if not self.state["visited"] and area in ("pewter", "pewter_gym"):
            self.state["visited"] = True
            self.persist()
        if not self.state["visited"]:
            return
        for actor, agent in self.state["agents"].items():
            active = agent["active"]
            if active and active["due"] <= second:
                self.advance(actor)

    def options(self, actor):
        persona = PERSONAS[actor]
        routine = (Step("WORK", persona.duty),)
        if actor == "researcher":
            return (routine, (Step("INVESTIGATE", "cast"), Step("WORK", persona.duty)))
        return (routine,)

    def decision(self, actor=None):
        if self.busy or not self.state["visited"]:
            return None
        hour = self.now % DAY // 3600
        day = self.now // DAY
        for key in (actor,) if actor else PERSONAS:
            persona = PERSONAS[key]
            agent = self.state["agents"][key]
            if agent["active"] or agent["shift"] >= day or not persona.hours[0] <= hour < persona.hours[1]:
                continue
            context = (
                f"You are on duty at {persona.duty}. The Museum publicly exhibits fossil casts. "
                "You independently noticed a comparison worth checking this shift. "
                f"Your previous checks: {agent['facts'].get('cast', {}).get('checks', 0)}. "
                f"Prefer {persona.preferred} when there is useful work and time."
            )
            return Ticket(self.memory.save, key, "open_shift", day, context, self.options(key))
        return None

    def submit(self, ticket, plan, fallback=None):
        if self.decision(ticket.actor) != ticket or plan not in ticket.choices:
            raise ValueError("Rejected stale or unauthorized Pewter plan")
        agent = self.state["agents"][ticket.actor]
        agent["shift"] = ticket.window
        agent["active"] = dict(steps=[(s.action, s.target) for s in plan], index=0, due=self.now)
        self.record(ticket.actor, "accepted", steps=agent["active"]["steps"], fallback=fallback)
        self.start(ticket.actor)
        self.persist()

    def start(self, actor):
        agent = self.state["agents"][actor]
        active = agent["active"]
        action, _ = active["steps"][active["index"]]
        agent["activity"] = action
        active["due"] = self.now + DURATIONS[action]

    def advance(self, actor):
        agent = self.state["agents"][actor]
        active = agent["active"]
        action, target = active["steps"][active["index"]]
        if action == "INVESTIGATE":
            checks = agent["facts"].get(target, {}).get("checks", 0) + 1
            agent["facts"][target] = dict(source=actor, kind="firsthand", checks=checks, second=self.now)
        self.record(actor, "completed", action=action, target=target)
        active["index"] += 1
        if active["index"] == len(active["steps"]):
            agent["active"] = None
            agent["activity"] = "WORK"
        else:
            self.start(actor)
        self.persist()
