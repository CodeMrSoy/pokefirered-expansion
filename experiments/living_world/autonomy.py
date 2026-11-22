"""Checkpointed event decisions for the Pewter–Mt. Moon pilot."""

from dataclasses import dataclass
from hashlib import sha256
import json

MUSEUM = "society_assistant"
SCOUTS = {"route_3": "route3/youngster", "mt_moon": "mtmoon_1f/baldingman"}
OFFER = "autonomy_offer"
REPORT = "autonomy_report"
DESK = "autonomy_desk"
TOPICS = {"tracks": "unusual tracks", "notes": "conflicting notes", "delay": "a missed field check"}
SITES = {"route_3": "Route 3", "mt_moon": "Mt. Moon"}
REASONS = {
    "inspect": "verify the evidence personally",
    "consult": "request a colleague's account",
    "compare": "help compare two accounts",
    "decline": "keep existing responsibilities",
    "wait": "wait for a stronger account",
}
INTERVAL = 3 * 3600
DEADLINE = 360


@dataclass(frozen=True)
class Decision:
    save: str
    number: int
    actor: str
    purpose: str
    options: tuple
    context: str
    fallback: str


def choose(model, ticket):
    """Serialize one compact decision on the existing shared worker."""
    aliases = dict(zip("ABCDEFGHIJKLM", ticket.options, strict=False))
    labels = " | ".join(map(json.dumps, aliases))
    def describe(option):
        if ticket.purpose != "propose":
            return option
        site, topic, lead = option.split(":")
        return f"{SITES[site]} {topic} {lead}"

    options = "\n".join(f"{key} {describe(value)}" for key, value in aliases.items())
    prompt = model.render_prompt("Choose one option. Output its letter only.", f"{ticket.context}\n{options}")
    # The compatibility Windows core uses the conservative CPU backend.
    limit = 18 if ticket.purpose == "propose" else 12
    raw, timing = model.worker.generate(f"root ::= {labels}\n", prompt, timeout=limit)
    if raw.strip() not in aliases:
        raise ValueError("Unsupported autonomous decision")
    return aliases[raw.strip()], timing


class AutonomousWorld:
    def __init__(self, world):
        self.world = world
        self.db = world.db
        self.db.execute("CREATE TABLE IF NOT EXISTS autonomous_world (save TEXT PRIMARY KEY, state TEXT NOT NULL)")
        self.load()

    def load(self):
        row = self.db.execute("SELECT state FROM autonomous_world WHERE save=?", (self.world.save,)).fetchone()
        seed = sha256(self.world.save.encode()).hexdigest()[:16]
        self.state = json.loads(row[0]) if row else {
            "seed": seed, "number": 0, "unlocked": False, "next": None, "event": None,
            "history": [], "log": [], "bonds": {}, "memories": {}, "player_trust": 0,
        }
        self.now = self.state.get("last", -1)

    def checkpoint(self, save):
        self.db.execute("INSERT INTO autonomous_world SELECT ?, state FROM autonomous_world WHERE save=?",
                        (save, self.world.save))

    def discard(self):
        self.db.execute("DELETE FROM autonomous_world WHERE save=?", (self.world.save,))

    def persist(self):
        self.state["last"] = self.now
        with self.db:
            self.db.execute("INSERT OR REPLACE INTO autonomous_world VALUES (?,?)",
                            (self.world.save, json.dumps(self.state, separators=(",", ":"))))

    def roll(self, label, count):
        value = f"{self.state['seed']}:{self.state['number']}:{label}".encode()
        return int.from_bytes(sha256(value).digest()[:4], "big") % count

    def log(self, kind, **fields):
        self.state["log"] = [*self.state["log"][-23:], dict(kind=kind, number=self.state["number"], **fields)]

    def advance(self, second, unlocked):
        if type(second) is not int or second < self.now:
            return
        self.now = second
        if unlocked and not self.state["unlocked"]:
            self.state.update(unlocked=True, next=second + 12 + self.roll("first", 10))
            self.persist()
        event = self.state["event"]
        if event and self.now >= event["deadline"]:
            actions = set(event["actions"].values())
            if {"inspect", "compare"} <= actions:
                result = "verified"
            elif event["player"] == "reported":
                result = "filed_with_player"
            elif actions & {"inspect", "compare"}:
                result = "filed"
            else:
                result = "unresolved"
            self.finish(result)

    def decision(self, catalog=None):
        if not self.state["unlocked"]:
            return None
        event = self.state["event"]
        if event is None:
            if self.now < self.state["next"]:
                return None
            history = self.state["history"][-2:]
            counts = {site: sum(event["site"] == site for event in history) for site in SITES}
            # A seeded environmental signal limits topics before Qwen sees them.
            conditions = tuple(TOPICS)
            focus = self.roll("conditions", len(conditions))
            topics = (conditions[focus], conditions[(focus + 1) % len(conditions)])
            sites = sorted(SITES, key=lambda site: (counts[site], self.roll("priority:" + site, 2**32)))
            options = tuple(f"{site}:{topic}:{lead}" for site in sites
                            for topic in topics for lead in ("local", "museum"))
            last = history[-1]["result"] if history else "no previous inquiry"
            context = (f"Start a local inquiry. New lead near {SITES[sites[0]]}. "
                       f"Likely topics: {TOPICS[topics[0]]} or {TOPICS[topics[1]]}. "
                       f"Last outcome: {last}. Pick location, topic and originator.")
            return Decision(self.world.save, self.state["number"] + 1, "world_director", "propose",
                            options, context, options[self.roll("director", len(options))])

        lead = event["lead"]
        other = MUSEUM if lead != MUSEUM else SCOUTS[event["site"]]
        if lead not in event["actions"] and self.now >= event["started"] + 8:
            actor = lead
            options = ("inspect", "consult", "wait") if lead != MUSEUM else ("consult", "wait")
        elif other in event["knowledge"] and other not in event["actions"] and self.now >= event["started"] + 20:
            actor = other
            options = ("compare", "decline", "wait")
        else:
            return None
        source = event["knowledge"][actor]
        profile = catalog.profile(actor) if catalog else None
        role = profile["role"] if profile else "field observer" if actor != MUSEUM else "museum assistant"
        goal = profile["long_goal"] if profile else "record reliable accounts"
        traits = ", ".join(profile["traits"]) if profile else "careful"
        memories = self.state["memories"].get(actor, [])
        colleague = other if actor == lead else lead
        trust = self.state["bonds"].get(actor, {}).get(colleague, 0)
        resident = self.world.population.state["actors"].get(actor, {})
        routine = resident.get("activity", "regular duties" if actor == MUSEUM else "free to observe")
        local_hour = self.now % 86400 // 3600
        past = memories[-1]["result"] if memories else "none"
        context = (f"You are the {role}, {traits}. Goal: {goal}. "
                   f"Your {source['kind']} account concerns {TOPICS[event['topic']]} at {SITES[event['site']]}. "
                   f"Past result: {past}. Colleague trust: {trust}. Local hour: {local_hour}. Routine: {routine}. "
                   + " ".join(f"{option} means {REASONS[option]}." for option in options))
        if actor == MUSEUM:
            context += f" The player filed {self.state.get('player_trust', 0)} accounts you received."
        weighted = [*options]
        if trust and "compare" in options:
            weighted.extend(("compare", "compare"))
        elif past == "unresolved" and 7 <= local_hour < 19:
            weighted.extend(option for option in options if option in ("consult", "inspect"))
        fallback = weighted[self.roll(actor, len(weighted))]
        return Decision(self.world.save, event["number"], actor, "respond", options, context, fallback)

    def submit(self, ticket, choice, source, timing=None, error=None):
        if ticket.save != self.world.save:
            return False
        current = self.decision()
        if (not current or (ticket.save, ticket.number, ticket.actor, ticket.purpose, ticket.options)
                != (current.save, current.number, current.actor, current.purpose, current.options)
                or choice not in current.options or source not in ("qwen", "fallback")):
            self.log("rejected", actor=ticket.actor, choice=str(choice)[:80], reason="stale or infeasible")
            self.persist()
            return False
        self.log(ticket.purpose, actor=ticket.actor, choice=choice, source=source, options=ticket.options,
                 timing=timing, error=error, why=REASONS.get(choice, "grounded in a reachable site and current leads"))
        if ticket.purpose == "propose":
            site, topic, origin = choice.split(":")
            lead = MUSEUM if origin == "museum" else SCOUTS[site]
            self.state.update(number=ticket.number, event={
                "number": ticket.number, "site": site, "topic": topic, "lead": lead, "started": self.now,
                "deadline": self.now + DEADLINE, "origin": source, "actions": {},
                "knowledge": {lead: {"kind": "firsthand" if lead != MUSEUM else "unconfirmed",
                                     "source": lead}}, "player": None,
            })
        else:
            event = self.state["event"]
            event["actions"][ticket.actor] = choice
            if ticket.actor == event["lead"] and choice in ("inspect", "consult"):
                other = MUSEUM if ticket.actor != MUSEUM else SCOUTS[event["site"]]
                event["knowledge"][other] = {"source": ticket.actor,
                                             "kind": "reported" if choice == "inspect" else "unconfirmed"}
                self.log("shared", actor=ticket.actor, recipient=other, provenance=event["knowledge"][other])
        self.persist()
        return True

    def finish(self, result):
        event = self.state["event"]
        event["result"] = result
        event["relationship_changes"] = []
        for actor in event["knowledge"]:
            memory = self.state["memories"].get(actor, [])
            self.state["memories"][actor] = [*memory[-3:], {
                "event": event["number"], "result": result, "source": event["knowledge"][actor]["source"],
            }]
            if result == "verified" and event["actions"].get(actor) in ("inspect", "compare", "consult"):
                peers = self.state["bonds"].setdefault(actor, {})
                other = MUSEUM if actor != MUSEUM else SCOUTS[event["site"]]
                if other in event["knowledge"] and peers.get(other, 0) < 10:
                    peers[other] = peers.get(other, 0) + 1
                    event["relationship_changes"].append({"actor": actor, "peer": other, "delta": 1})
        self.state["history"] = [*self.state["history"][-7:], event]
        self.state.update(event=None, next=self.now + INTERVAL + self.roll("interval", 1800))
        self.log("resolved", result=result, player=event["player"])
        self.persist()

    def reply(self, actor):
        actor = MUSEUM if actor == DESK else actor
        event = self.state["event"]
        if actor == OFFER:
            if event and event["player"] == "heard":
                return "File your field account?", None
            return None, None
        if actor == REPORT:
            if event and event["player"] == "heard":
                return "I'll add your field account.\nThanks for checking in.", (event["number"], "reported")
            return None, None
        if event and actor in event["knowledge"]:
            update = {"tracks": "We found unusual tracks.", "notes": "Our notes do not agree.",
                      "delay": "A field check was missed."}[event["topic"]]
            if actor == SCOUTS[event["site"]]:
                if event["knowledge"][actor]["kind"] != "firsthand":
                    update = {"tracks": "Someone reported tracks.", "notes": "Someone reported a mix-up.",
                              "delay": "I heard a check was missed."}[event["topic"]]
                if event["player"] is None:
                    return update + "\nReport to Pewter Museum.", (event["number"], "heard")
                return update + "\nThanks for stopping by.", None
            site = SITES[event["site"]]
            attribution = "A local sent word." if event["lead"] != MUSEUM else "I have a field lead."
            return f"{attribution}\nWe're checking {site}.", None
        for past in reversed(self.state["history"]):
            if actor in past["knowledge"]:
                result = {"verified": "The accounts matched.", "filed": "We filed a single account.",
                          "filed_with_player": "We filed your account.",
                          "unresolved": "We could not verify it."}[past["result"]]
                return result + "\nI remember that inquiry.", None
        return None, None

    def accept(self, token):
        event = self.state["event"]
        if token is None or not event or token[0] != event["number"]:
            return False
        target = token[1]
        if ((target == "heard" and event["player"] is None)
                or (target == "reported" and event["player"] == "heard")):
            event["player"] = target
            if target == "reported":
                event["player_report"] = {"kind": "relayed", "source": "player",
                                          "origin": SCOUTS[event["site"]]}
                event["knowledge"].setdefault(MUSEUM, event["player_report"])
                self.state["player_trust"] = min(self.state.get("player_trust", 0) + 1, 10)
            self.log("player", action=target, source="player")
            self.persist()
            return True
        return False
