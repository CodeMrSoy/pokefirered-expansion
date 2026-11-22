"""ROM-grounded policy for permanent changes to the supported Pewter roles."""

from copy import deepcopy
from dataclasses import dataclass
from hashlib import sha256
import json

import agency
from autonomy import Decision

# Registry entries describe implemented native services. Optional projects may
# use an existing script but cannot mutate the registry or the service stock.
CENTERS = (
    "ViridianCity", "PewterCity", "Route4", "CeruleanCity", "VermilionCity",
    "Route10", "LavenderTown", "CeladonCity", "FuchsiaCity", "SaffronCity",
    "CinnabarIsland", "IndigoPlateau", "Havora", "Corvala_Town",
    "Eldervale_Village", "Myrdal_City", "Iskora_Village",
)
MARTS = {town: f"{town}_Mart" for town in (
    "ViridianCity", "PewterCity", "CeruleanCity", "VermilionCity",
    "LavenderTown", "FuchsiaCity", "SaffronCity", "CinnabarIsland",
)}
MARTS.update(CeladonCity="CeladonCity_DepartmentStore_2F", IndigoPlateau="IndigoPlateau_PokemonCenter_1F",
             Havora="Havora_Market")
KANTO_GYMS = dict(zip(
    ("brock", "misty", "surge", "erika", "koga", "sabrina", "blaine", "giovanni"),
    ("PewterCity", "CeruleanCity", "VermilionCity", "CeladonCity", "FuchsiaCity",
     "SaffronCity", "CinnabarIsland", "ViridianCity"),
))
QUANTUM_CAPS = dict(zip(
    ("brock", "misty", "surge", "erika", "koga", "eirik", "sabrina", "corvala",
     "blaine", "brandon", "ben", "cody", "giovanni", "league"),
    (14, 21, 24, 29, 35, 46, 50, 57, 63, 68, 73, 79, 82, 90),
))
CLASSIC_CAPS = dict(zip((*KANTO_GYMS, "league"), (14, 21, 24, 29, 43, 43, 47, 50, 63)))
RESERVED_CRESTS = ("corvala", "brandon", "ben", "cody")
MART, PITCH, SUPPORT, GYM = "evolution_mart", "evolution_pitch", "evolution_support", "evolution_gym"
CHECKOUT = "evolution_checkout"
PRACTICE_ROCK, PRACTICE_TRAIL = "practice_rock", "practice_trail"
HOOKS = {29: MART, 30: PITCH, 31: SUPPORT, 32: GYM, 33: CHECKOUT,
         34: PRACTICE_ROCK, 35: PRACTICE_TRAIL, 36: "mart_neighbor", 37: "neighbor_checkout"}
PROJECTS = {
    "mart": ("stock_helper", "counter_apprentice"),
    "gym": ("type_coaching", "expedition_coaching"),
}
ACTORS = {"mart": "Pewter Mart resident", "gym": "Brock"}
BASE = {"mart": "resident", "gym": "standard"}
DIALOGUE = {
    "stock_helper": "I help check the stock now.\nThe clerk handles sales.",
    "counter_apprentice": "I joined the Mart crew.\nI can take your order.",
    "type_coaching": "Brock started type lessons.\nTry Water against Rock.",
    "expedition_coaching": "Brock started trail lessons.\nPack an Escape Rope.",
}


def team_ceiling(mode, milestone, current_limit, levels):
    """Diagnostic ceiling for proposed levels. Whole-team replacement is closed."""
    caps = {"classic": CLASSIC_CAPS, "quantum": QUANTUM_CAPS}.get(mode, {})
    if (milestone not in caps or type(current_limit) is not int or not 1 <= current_limit <= 100
            or not isinstance(levels, (tuple, list)) or not 1 <= len(levels) <= 6):
        return False
    return all(type(level) is int and 1 <= level <= min(caps[milestone], current_limit) for level in levels)


@dataclass(frozen=True)
class Change:
    save: str
    revision: int
    project: str
    choice: str


class WorldRules:
    def __init__(self, world):
        self.world = world
        self.db = world.db
        self.db.execute("CREATE TABLE IF NOT EXISTS world_changes (save TEXT PRIMARY KEY, data TEXT NOT NULL)")
        self.load()

    def load(self):
        row = self.db.execute("SELECT data FROM world_changes WHERE save=?", (self.world.save,)).fetchone()
        self.original = row[0] if row else None
        self.now = None
        self.badge = False
        self.quarantined = False
        base = dict(revision=0, projects=dict(BASE), endorsed=False, open_at=None, audit=[])
        try:
            self.state = json.loads(self.original) if row else base
            self.check_state(self.state)
        except (ValueError, TypeError, KeyError):
            self.state = base
            self.quarantined = True

    @staticmethod
    def check_state(state):
        if not isinstance(state, dict) or set(state) - {"agency"} != {"revision", "projects", "endorsed", "open_at", "audit"}:
            raise ValueError("Unknown world-state fields")
        if (type(state["revision"]) is not int or state["revision"] < 0
                or type(state["endorsed"]) is not bool
                or (state["open_at"] is not None and
                    (type(state["open_at"]) is not int or state["open_at"] < 0))
                or not isinstance(state["audit"], list) or len(state["audit"]) > 16):
            raise ValueError("Malformed world state")
        if "agency" in state:
            agency.validate_state(state["agency"])
        if not isinstance(state["projects"], dict) or set(state["projects"]) != set(PROJECTS):
            raise ValueError("Project outside the rules registry")
        for project, value in state["projects"].items():
            if value != BASE[project] and value not in PROJECTS[project]:
                raise ValueError("Unimplemented transformation on load")

    def checkpoint(self, save):
        if not self.quarantined:
            self.db.execute("INSERT INTO world_changes SELECT ?, data FROM world_changes WHERE save=?",
                            (save, self.world.save))

    def discard(self):
        self.db.execute("DELETE FROM world_changes WHERE save=?", (self.world.save,))

    def store(self, candidate):
        if self.quarantined:
            raise ValueError("World changes are quarantined")
        self.check_state(candidate)
        encoded = json.dumps(candidate, separators=(",", ":"))
        with self.db:
            if self.original is None:
                cursor = self.db.execute("INSERT OR IGNORE INTO world_changes VALUES (?,?)",
                                         (self.world.save, encoded))
            else:
                cursor = self.db.execute("UPDATE world_changes SET data=? WHERE save=? AND data=?",
                                         (encoded, self.world.save, self.original))
            if cursor.rowcount != 1:
                raise ValueError("World changed before commit")
        self.original = encoded
        self.state = candidate

    def observe(self, second, badge):
        self.badge = bool(badge)
        if type(second) is not int or second < 0 or self.quarantined:
            return
        self.now = second
        if self.badge and self.state["open_at"] is None:
            opened = deepcopy(self.state)
            opened["open_at"] = second + 45
            self.store(opened)

    def decision(self, inquiry=None, project_scope=None):
        if self.quarantined or not self.badge or self.now is None or self.state["open_at"] is None:
            return None
        pending = [project for project in PROJECTS if self.state["projects"][project] == BASE[project]]
        if project_scope is not None:
            pending = [p for p in pending if p == project_scope]
        if not pending or self.now < self.state["open_at"]:
            return None
        seed = sha256(f"{self.world.save}:{self.state['revision']}".encode()).digest()
        topic = pending[seed[0] % len(pending)]
        options = PROJECTS[topic]
        # Player endorsement has an observable effect on the shortlist. The
        # original clerk remains available whichever role is commissioned.
        if topic == "mart" and self.state["endorsed"]:
            options = ("counter_apprentice",)
        result = inquiry.get("result", "none") if inquiry else "none"
        context = (f"{ACTORS[topic]} proposes a Pewter project. Recent inquiry: {result}. "
                   f"Counter endorsement: {self.state['endorsed']}. Keep all native services. "
                   "Stock checks supplies. Counter serves shoppers. Coaching is optional.")
        return Decision(self.world.save, self.state["revision"], topic, "evolve", options,
                        context, options[seed[1] % len(options)])

    def submit(self, change, source, timing=None, project_scope=None):
        if self.quarantined or change.save != self.world.save:
            return False
        ticket = self.decision(project_scope=project_scope)
        approved = (ticket is not None and change.save == ticket.save
                    and change.revision == ticket.number and change.project == ticket.actor
                    and change.choice in ticket.options and source in ("qwen", "fallback"))
        candidate = deepcopy(self.state)
        candidate["audit"] = [*candidate["audit"][-15:], {
            "approved": approved, "source": source, "project": str(change.project)[:40],
            "choice": str(change.choice)[:40], "timing": timing,
            "reason": "native services and progression preserved" if approved else "stale or unsupported change",
        }]
        if approved:
            candidate["projects"][change.project] = change.choice
            candidate["revision"] += 1
            candidate["open_at"] = self.now + 90
        self.store(candidate)
        return approved

    def endorse(self):
        if (self.quarantined or not self.badge or self.state["endorsed"]
                or self.state["projects"]["mart"] != "resident"):
            return False
        candidate = deepcopy(self.state)
        candidate["endorsed"] = True
        candidate["revision"] += 1
        self.store(candidate)
        return True

    def reply(self, actor):
        if self.quarantined or not self.badge:
            return None
        if actor == PITCH and self.state["projects"]["mart"] == "resident" and not self.state["endorsed"]:
            return "Back my counter training?"
        if actor == SUPPORT and self.state["projects"]["mart"] == "resident" and not self.state["endorsed"]:
            return "I'll tell the shop clerk."
        if a := self.state.get("agency"):
            owner = "neighbor" if actor in ("mart_neighbor", "neighbor_checkout") else "resident"
            person = a["people"][owner]
            peer = agency.PEER[owner]
            if actor in (MART, "mart_neighbor"):
                if target := agency.unfinished(person):
                    kind, skill = target.split()
                    if kind == "staff":
                        return "I hope to work the counter." if skill == "sales" else "Still aiming for stock work."
                    if kind == "learn":
                        return f"I still need to learn {skill}."
                    return f"I hope to teach {skill}."
                if person["feedback"].startswith(peer + " answered teach"):
                    return "My neighbor taught me."
                if owner in a["asked"]:
                    return "I asked about " + a["asked"][owner] + " work."
                if peer in a["asked"]:
                    return "My neighbor asked for help."
                if person["job"] == "stock":
                    return "I am checking supplies."
                if person["job"] == "sales":
                    return "I can serve customers now."
                if len(person["skills"]) == 2:
                    return "I learned another skill."
            if actor in (CHECKOUT, "neighbor_checkout") and person["job"]:
                return "Can I take your order?" if person["job"] == "sales" else None
        if actor == CHECKOUT and self.state["projects"]["mart"] == "counter_apprentice":
            return "Need anything from the Mart?"
        if actor == MART:
            return DIALOGUE.get(self.state["projects"]["mart"])
        course = self.state["projects"]["gym"]
        if actor == PRACTICE_ROCK and course == "type_coaching":
            return "Try the Rock type drill?"
        if actor == PRACTICE_TRAIL and course == "expedition_coaching":
            return "Try the trail drill?"
        if actor == GYM:
            return DIALOGUE.get(course)
        return None

    def monitor(self):
        return {
            "state": self.state, "quarantine": self.quarantined, "gate": self.badge,
            "protected_native_services": {"centers": CENTERS, "marts": MARTS},
            "native_gym_maps": {name: f"{town}_Gym" for name, town in KANTO_GYMS.items()},
            "vidra": {"eirik": "Havora_Gym", "reserved_crests": RESERVED_CRESTS},
            "progression_caps": {"classic": CLASSIC_CAPS, "quantum": QUANTUM_CAPS},
            "native_practice_caps": {"type_coaching": 10, "expedition_coaching": 11},
            "battle_overrides": False, "map_overrides": False,
        }


def apply_decision(rules, ticket, answer, source, timing=None, project_scope=None):
    return rules.submit(Change(ticket.save, ticket.number, ticket.actor, answer), source, timing, project_scope)
