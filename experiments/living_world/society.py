"""Pewter agents advance at decisions and deadlines on the battery checkpoint."""
from copy import copy, deepcopy
from dataclasses import dataclass
import json
from time import perf_counter

from planning import GOALS, Proposal, choose_plan

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
    "assistant": Persona("Pewter Museum assistant", "keep verified notes for the exhibit",
                         "helpful but careful", "museum", (9, 18), "WORK"),
    "trainer": Persona("Pewter Bug Catcher", "learn what wild Pokemon do around rocks",
                       "observant and competitive", "pewter", (8, 19), "TRAIN_POKEMON"),
    "attendant": Persona("Pewter Gym attendant", "keep the training floor useful for challengers",
                         "reliable and cautious", "gym", (8, 18), "WORK"),
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


DURATIONS = {"WORK": 24, "REST": 16, "INVESTIGATE": 32, "TRAIN_POKEMON": 28,
             "REQUEST_ASSISTANCE": 4, "ACCEPT_REQUEST": 4, "DECLINE_REQUEST": 4,
             "ARRANGE_MEETING": 6, "VISIT_NPC": 6, "SHARE_INFORMATION": 4,
             "TRAVEL_TO": 16, "RETURN_TO_DUTY": 16}
TRAVEL_STEPS = ("TRAVEL_TO", "RETURN_TO_DUTY")
TRAINER_PRESENCE = {"pewter": 0, "in_transit": 1, "route_2": 2}
LINKS = {
    "researcher": {"assistant", "brock"},
    "assistant": {"researcher", "trainer"},
    "trainer": {"assistant", "attendant"},
    "attendant": {"trainer"},
}
REQUEST_SECONDS = 150
MAX_PLAN_SECONDS = 110


def choose_agent(model, ticket):
    persona = PERSONAS[ticket.actor]
    labels = tuple("ABCDEF"[:len(ticket.choices)])
    instructions = (f"You are the {persona.role}, {persona.temperament}. Your long-term goal is to "
                    f"{persona.motive}. Select an available plan. Output only the choice letter.")
    descriptions = {
        "DECLINE_REQUEST": "Decline and continue your duties",
        "ACCEPT_REQUEST": "Help the colleague: book a short meeting, check the cast and send your result",
        "INVESTIGATE": "Check the Museum cast firsthand",
        "TRAIN_POKEMON": "Train your Pokemon",
        "TRAVEL_TO": "Travel to the public north end of Route 2, train, then return to Pewter",
        "WORK": "Stay on routine duty",
        "REST": "Rest briefly and resume duty",
    }
    def describe(plan):
        first = plan[0]
        if first.action == "REQUEST_ASSISTANCE":
            return f"Ask {first.target} to check your result"
        phrase = descriptions[first.action]
        if plan[-1].action == "REQUEST_ASSISTANCE":
            return f"{phrase}, then ask {plan[-1].target} to check it"
        return phrase
    plans = "\n".join(f"{letter}: {describe(plan)}" for letter, plan in zip(labels, ticket.choices))
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
        self.demo = False
        self.db = memory.db
        self.db.execute("CREATE TABLE IF NOT EXISTS society_state (save TEXT PRIMARY KEY, state TEXT NOT NULL)")
        self.load()

    def load(self):
        row = self.db.execute("SELECT state FROM society_state WHERE save=?", (self.memory.save,)).fetchone()
        self.state = json.loads(row[0]) if row else dict(visited=False, clock=-1, agents={}, log=[])
        for key, persona in PERSONAS.items():
            self.state["agents"].setdefault(key, dict(location=persona.duty, shift=-1, active=None,
                                                      activity="WORK", facts={}, bonds={}, memory=[]))
            self.state["agents"][key].setdefault("followup_count", 0)
        self.state.setdefault("requests", {})
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
            for actor, agent in self.state["agents"].items():
                if agent["active"]:
                    self.abort(actor, "clock unavailable or reversed")
            return
        self.now = second
        if not self.state["visited"] and area in ("pewter", "pewter_gym"):
            self.state["visited"] = True
            self.persist()
        if not self.state["visited"]:
            return
        dirty = False
        for request in self.state["requests"].values():
            if request["status"] in ("pending", "accepted") and second >= request["expires"]:
                request["status"] = "expired"
                dirty = True
        for actor, agent in self.state["agents"].items():
            active = agent["active"]
            if active and active["due"] <= second:
                if second >= active.get("deadline", second + 1):
                    self.abort(actor, "expired commitment")
                else:
                    self.advance(actor)
        if dirty:
            self.persist()

    def message(self, actor):
        if not self.state["visited"]:
            return None
        agent = self.state["agents"][actor]
        if actor == "assistant":
            if agent["facts"].get("cast", {}).get("kind") == "firsthand":
                return "I checked the cast myself.\nThe Museum has my notes."
            if self.pending(actor)[1]:
                return "The researcher asked me\nfor a second look."
        if actor == "trainer" and agent["location"] == "route_2":
            if agent["facts"].get("cast", {}).get("kind") == "firsthand":
                return "I checked the Museum cast.\nNow I'm training here."
            return "A short field practice.\nI head back to Pewter soon."
        return None

    def pending(self, actor):
        return next(((key, request) for key, request in self.state["requests"].items()
                     if request["recipient"] == actor and request["status"] == "pending"
                     and self.now < request["expires"]), (None, None))

    def notice_for_brock(self):
        key, request = self.pending("brock")
        return key if request and request["origin"] == "researcher" else None

    def respond_brock(self, key, accepted):
        if key and key == self.notice_for_brock():
            request = self.state["requests"][key]
            request["status"] = "accepted" if accepted else "declined"
            self.record(request["sender"], request["status"], peer="brock", event=key)
            self.persist()

    def reconcile_brock(self, result):
        if not result:
            return
        key, completed = result
        notice = self.state["requests"].get(key)
        if notice and notice["recipient"] == "brock" and notice["status"] == "accepted":
            notice["status"] = "resolved" if completed else "interrupted"
            researcher = self.state["agents"][notice["sender"]]
            if completed:
                researcher["facts"]["colleague_cast"] = dict(
                    source="brock", origin="brock", kind="reported", second=self.now)
                researcher["bonds"]["brock"] = min(20, researcher["bonds"].get("brock", 0) + 1)
            self.record(notice["sender"], notice["status"], event=key, peer="brock")
            self.persist()

    def request_key(self, actor, recipient):
        return f"pewter:cast:{self.now // DAY}:{actor}:{recipient}"

    def can_send(self, actor, recipient):
        return (recipient in LINKS[actor]
                and self.request_key(actor, recipient) not in self.state["requests"]
                and not self.pending(recipient)[0])

    def can_request(self, actor, recipient):
        return self.can_send(actor, recipient) and self.state["agents"][actor]["facts"].get("cast")

    def options(self, actor, incoming=None):
        persona = PERSONAS[actor]
        routine = (Step("WORK", persona.duty),)
        if incoming:
            peer = self.state["requests"][incoming]["sender"]
            return ((Step("DECLINE_REQUEST", incoming),),
                    (Step("ACCEPT_REQUEST", incoming), Step("ARRANGE_MEETING", incoming),
                     Step("VISIT_NPC", peer), Step("INVESTIGATE", "cast"),
                     Step("SHARE_INFORMATION", incoming)))
        if actor == "researcher":
            inspect = (Step("INVESTIGATE", "cast"),)
            if self.can_request(actor, "assistant"):
                return (routine, inspect + (Step("REQUEST_ASSISTANCE", "assistant"),))
            if self.can_request(actor, "brock"):
                return (routine, inspect + (Step("REQUEST_ASSISTANCE", "brock"),))
            variations = (routine, inspect + routine)
            if self.can_send(actor, "assistant"):
                return (*variations, inspect + (Step("REQUEST_ASSISTANCE", "assistant"),))
            return variations
        if actor == "trainer":
            return (routine, (Step("TRAIN_POKEMON", persona.duty), Step("REST", persona.duty)),
                    (Step("TRAVEL_TO", "route_2"), Step("TRAIN_POKEMON", "route_2"),
                     Step("RETURN_TO_DUTY", persona.duty)))
        return (routine, (Step("REST", persona.duty), Step("WORK", persona.duty)))

    def followups(self, actor):
        agent = self.state["agents"][actor]
        fact = agent["facts"].get("cast")
        if not fact or self.now - fact["second"] >= REQUEST_SECONDS:
            return ()
        recipients = {"researcher": ("brock", "assistant"), "assistant": ("trainer",),
                      "trainer": ("attendant",)}.get(actor, ())
        return tuple(peer for peer in recipients if self.can_request(actor, peer))

    def decision(self, actor=None):
        if self.busy or not self.state["visited"]:
            return None
        hour = 11 if self.demo else self.now % DAY // 3600
        day = self.now // DAY
        for key in (actor,) if actor else sorted(PERSONAS, key=lambda key: self.pending(key)[0] is None):
            persona = PERSONAS[key]
            agent = self.state["agents"][key]
            if agent["active"] or not persona.hours[0] <= hour < persona.hours[1]:
                continue
            event, notice = self.pending(key)
            if notice:
                trust = agent["bonds"].get(notice["sender"], 0)
                workload = hour >= persona.hours[1] - 1
                closing = workload and trust < 2
                context = (f"{notice['sender']} asks you to compare a fossil cast. "
                           f"The notice names {notice['origin']} as the source. "
                           f"You have worked successfully with this sender {trust} times. "
                           + ("Your shift is nearly over. You must close the desk. Decline rather than break your promise."
                              if closing else "You have spare time and your job is to verify exhibits. "
                              "A short meeting and independent check would help the Museum."))

                return Ticket(self.memory.save, key, event, day, context, self.options(key, event))
            peers = self.followups(key)
            if peers and agent["shift"] == day and agent["followup_count"] < 2:
                context = ("You completed a cast comparison. A colleague may be able to check it. "
                           + ("Brock can compare Rock-type exhibits and the Museum assistant can do a second count. "
                              if key == "researcher" else "")
                           + "Choose cooperation if it helps verify the work. "
                           + ", ".join(f"{peer} has helped {agent['bonds'].get(peer, 0)} times" for peer in peers))
                plans = ((Step("WORK", persona.duty),),)
                plans += tuple((Step("REQUEST_ASSISTANCE", peer),) for peer in peers)
                return Ticket(self.memory.save, key, "share_findings", day, context, plans)
            if agent["shift"] >= day:
                continue
            context = f"You are at {persona.duty}. Your shift is open. "
            if key == "researcher":
                context += ("You noticed a cast comparison worth checking at the Museum. "
                            "Ask the assistant if an independent second check would help.")
            elif key == "trainer":
                context += ("You can practice on the public north end of Route 2 or stay here. "
                            "The north path is clear. A short field practice is useful today. ")
            else:
                context += "You have heard no request. Continue your own routine. "
            context += f"You normally prefer {persona.preferred}. Past firsthand checks: " + str(
                agent["facts"].get("cast", {}).get("checks", 0))
            return Ticket(self.memory.save, key, "open_shift", day, context, self.options(key))
        return None

    def primitives(self, ticket):
        """Authorize atomic targets from the actor's situation, never from generated text."""
        actor = ticket.actor
        duty = PERSONAS[actor].duty
        options = [Step("WORK", duty), Step("REST", duty)]
        if ticket.cause in self.state["requests"]:
            notice = self.state["requests"][ticket.cause]
            options += [Step(action, ticket.cause) for action in (
                "DECLINE_REQUEST", "ACCEPT_REQUEST", "ARRANGE_MEETING", "SHARE_INFORMATION")]
            options += [Step("VISIT_NPC", notice["sender"]), Step("INVESTIGATE", "cast")]
        elif actor == "researcher":
            options.append(Step("INVESTIGATE", "cast"))
            options += [Step("REQUEST_ASSISTANCE", peer) for peer in sorted(LINKS[actor])
                        if self.can_send(actor, peer)]
        else:
            options += [Step("REQUEST_ASSISTANCE", peer) for peer in self.followups(actor)]
        if actor == "trainer":
            options += [Step("TRAIN_POKEMON", duty), Step("TRAVEL_TO", "route_2"),
                        Step("TRAIN_POKEMON", "route_2"), Step("RETURN_TO_DUTY", duty)]
        return tuple(options)

    def validate_proposal(self, ticket, proposal):
        steps = proposal.steps
        if proposal.available != self.primitives(ticket) or not 1 <= len(steps) <= 6 or len(set(steps)) != len(steps):
            raise ValueError("Plan contains changed capabilities or duplicate steps")
        if any(step not in proposal.available for step in steps) or not any(
                GOALS.get(step.action) == proposal.goal for step in steps):
            raise ValueError("Unauthorized action or unmet goal")
        if sum(DURATIONS[step.action] for step in steps) >= MAX_PLAN_SECONDS:
            raise ValueError("Plan exceeds time budget")

        # Use a shadow copy and the same transition code as execution.
        # Nothing runs against SQLite or the actual world while validating.
        shadow = copy(self)
        shadow.state = deepcopy(self.state)
        shadow.persist = lambda: None
        agent = shadow.state["agents"][ticket.actor]
        agent["active"] = dict(steps=[(s.action, s.target) for s in steps], index=0, due=self.now,
                               deadline=self.now + MAX_PLAN_SECONDS, event=ticket.cause)
        for step in steps:
            shadow.start(ticket.actor)
            active = agent["active"]
            if active is None:
                raise ValueError(f"{step.action} precondition is not met")
            shadow.now = active["due"]
            shadow.advance(ticket.actor, start_next=False)
            last = agent["memory"][-1]
            if last["outcome"] != "completed":
                raise ValueError(f"{step.action} cannot finish within the current commitments")
        if agent["location"] != PERSONAS[ticket.actor].duty:
            raise ValueError("Plan must end at the actor's duty location")
        if shadow.qualifies(ticket.actor, ticket.cause, "accepted"):
            raise ValueError("Cooperation needs a feasible completion before expiry")

    def submit(self, ticket, plan, fallback=None):
        if self.decision(ticket.actor) != ticket:
            raise ValueError("Rejected stale Pewter decision")
        goal = None
        if isinstance(plan, Proposal):
            self.validate_proposal(ticket, plan)
            goal, plan = plan.goal, plan.steps
        elif plan not in ticket.choices:
            raise ValueError("Rejected unauthorized recovery plan")
        if not 1 <= len(plan) <= 6 or sum(DURATIONS[step.action] for step in plan) >= MAX_PLAN_SECONDS:
            raise ValueError("Plan exceeds Pewter action or time bounds")
        agent = self.state["agents"][ticket.actor]
        if ticket.cause == "open_shift":
            agent["shift"] = ticket.window
            agent["followup_count"] = 0
        elif ticket.cause == "share_findings":
            agent["followup_count"] = agent["followup_count"] + 1 if plan[0].action == "REQUEST_ASSISTANCE" else 2
        agent["active"] = dict(steps=[(s.action, s.target) for s in plan], index=0, due=self.now,
                               deadline=self.now + MAX_PLAN_SECONDS, event=ticket.cause, goal=goal)
        self.record(ticket.actor, "accepted", steps=agent["active"]["steps"], fallback=fallback)
        self.start(ticket.actor)
        self.persist()

    def valid(self, actor, action, target, active, *, finishing=False):
        agent = self.state["agents"][actor]
        if action in TRAVEL_STEPS:
            destination, origin = ("route_2", "pewter") if action == "TRAVEL_TO" else ("pewter", "route_2")
            return actor == "trainer" and target == destination and agent["location"] == (
                "in_transit" if finishing else origin)
        if action == "TRAIN_POKEMON" and actor == "trainer":
            return target == agent["location"] and target in ("pewter", "route_2")
        if action in ("WORK", "REST"):
            return target == agent["location"] == PERSONAS[actor].duty
        if action == "INVESTIGATE":
            return target == "cast" and (actor == "researcher" or
                   self.qualifies(actor, active.get("event"), "accepted"))
        if action == "REQUEST_ASSISTANCE":
            return self.can_request(actor, target)
        if action in ("ACCEPT_REQUEST", "DECLINE_REQUEST"):
            return self.qualifies(actor, target, "pending")
        if action == "ARRANGE_MEETING":
            request = self.state["requests"].get(target)
            sender = self.state["agents"].get(request["sender"]) if request else None
            return (self.qualifies(actor, target, "accepted") and sender is not None
                    and sender["location"] == PERSONAS[request["sender"]].duty
                    and agent["location"] == PERSONAS[actor].duty)
        if action == "SHARE_INFORMATION":
            return self.qualifies(actor, target, "accepted")
        if action == "VISIT_NPC":
            request = self.state["requests"].get(active.get("event"))
            return (request and request["sender"] == target and "meeting" in request
                    and self.qualifies(actor, active["event"], "accepted")
                    and self.state["agents"][target]["location"] == PERSONAS[target].duty
                    and agent["location"] == PERSONAS[actor].duty)
        return False

    def qualifies(self, actor, event, status):
        request = self.state["requests"].get(event)
        return (request and request["recipient"] == actor and request["status"] == status
                and self.now < request["expires"])

    def abort(self, actor, reason):
        agent = self.state["agents"][actor]
        event = agent["active"].get("event")
        if self.qualifies(actor, event, "accepted"):
            self.state["requests"][event]["status"] = "interrupted"
        self.record(actor, "interrupted", reason=reason)
        agent.update(active=None, activity="WORK", location=PERSONAS[actor].duty)
        self.persist()

    def start(self, actor):
        agent = self.state["agents"][actor]
        active = agent["active"]
        action, target = active["steps"][active["index"]]
        if not self.valid(actor, action, target, active):
            self.abort(actor, f"{action} precondition changed")
            return
        if action in TRAVEL_STEPS:
            active["journey"] = dict(origin=agent["location"], destination=target, departed=self.now,
                                     arrival=self.now + DURATIONS[action])
            agent["location"] = "in_transit"
        agent["activity"] = action
        active["due"] = self.now + DURATIONS[action]

    def advance(self, actor, *, start_next=True):
        agent = self.state["agents"][actor]
        active = agent["active"]
        action, target = active["steps"][active["index"]]
        if not self.valid(actor, action, target, active, finishing=True):
            self.abort(actor, f"{action} precondition changed")
            return
        requests = self.state["requests"]
        if action in TRAVEL_STEPS:
            agent["location"] = target
            active.pop("journey")
        elif action == "INVESTIGATE":
            checks = agent["facts"].get(target, {}).get("checks", 0) + 1
            agent["facts"][target] = dict(source=actor, origin=actor, kind="firsthand",
                                          checks=checks, second=self.now)
        elif action == "REQUEST_ASSISTANCE":
            if len(requests) >= 12:
                disposable = next((key for key, report in requests.items()
                                   if report["status"] not in ("pending", "accepted")), None)
                if not disposable:
                    self.abort(actor, "request capacity reached")
                    return
                del requests[disposable]
            fact = agent["facts"]["cast"]
            requests[self.request_key(actor, target)] = dict(
                sender=actor, recipient=target, origin=fact.get("origin", actor), status="pending",
                issued=self.now, expires=self.now + REQUEST_SECONDS)
        elif action in ("ACCEPT_REQUEST", "DECLINE_REQUEST"):
            requests[target]["status"] = "accepted" if action == "ACCEPT_REQUEST" else "declined"
        elif action == "ARRANGE_MEETING":
            requests[target]["meeting"] = self.now
        elif action == "SHARE_INFORMATION":
            request = requests[target]
            if not agent["facts"].get("cast"):
                self.abort(actor, "missing firsthand result")
                return
            peer = self.state["agents"][request["sender"]]
            peer["facts"]["colleague_cast"] = dict(source=actor, origin=actor,
                                                  kind="reported", second=self.now)
            for person, name in ((peer, actor), (agent, request["sender"])):
                person["bonds"][name] = min(20, person["bonds"].get(name, 0) + 1)
            request["status"] = "resolved"
        self.record(actor, "completed", action=action, target=target)
        active["index"] += 1
        if active["index"] == len(active["steps"]):
            agent["active"] = None
            agent["activity"] = "WORK"
        elif start_next:
            self.start(actor)
        self.persist()
