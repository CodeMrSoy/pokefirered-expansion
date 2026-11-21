"""Checkpoint-scoped regional residents and their offscreen routines."""
from dataclasses import dataclass
import heapq
import json

DAY = 86400
TRANSITIONS = 32
GOAL_WINDOW = 10 * DAY
LOCATIONS = frozenset(("pewter", "museum", "route_2", "gym"))


@dataclass(frozen=True)
class Resident:
    id: str
    name: str
    role: str
    home: str
    shift: int
    days_off: tuple[int, ...]
    motive: str
    preference: str
    patience: int


# These are host-side inhabitants. Their homes are logical workplaces and
# this roster does not allocate or move any additional ROM sprites.
ROLES = {
    "researcher": ("museum", "verify the regional survey", "careful"),
    "curator": ("museum", "document the exhibit inventory", "precise"),
    "trainer": ("pewter", "prepare for a practice challenge", "competitive"),
    "guide": ("pewter", "keep local route advice accurate", "helpful"),
    "volunteer": ("route_2", "finish the recurring field survey", "observant"),
    "attendant": ("gym", "keep practice appointments available", "punctual"),
}
ROSTER = (
    ("ada", "Ada", "researcher"), ("bevan", "Bevan", "curator"),
    ("clara", "Clara", "trainer"), ("dev", "Dev", "guide"),
    ("eli", "Eli", "volunteer"), ("faye", "Faye", "attendant"),
    ("gail", "Gail", "researcher"), ("hugo", "Hugo", "curator"),
    ("inez", "Inez", "trainer"), ("jun", "Jun", "guide"),
    ("kit", "Kit", "volunteer"), ("lena", "Lena", "attendant"),
    ("mina", "Mina", "researcher"), ("noel", "Noel", "curator"),
    ("opal", "Opal", "trainer"), ("pia", "Pia", "guide"),
    ("quin", "Quin", "volunteer"), ("rui", "Rui", "attendant"),
    ("sana", "Sana", "researcher"), ("theo", "Theo", "curator"),
    ("uma", "Uma", "trainer"), ("vale", "Vale", "guide"),
    ("wren", "Wren", "volunteer"), ("yan", "Yan", "attendant"),
)


def residents():
    return tuple(Resident(id_, name, role, ROLES[role][0], (9 + i % 4) * 3600,
                          (i % 7,), *ROLES[role][1:], i % 3)
                 for i, (id_, name, role) in enumerate(ROSTER))


class Population:
    def __init__(self, world, roster=None):
        self.world = world
        self.db = world.db
        profiles = tuple(residents() if roster is None else roster)
        self.people = {person.id: person for person in profiles}
        if len(self.people) != len(profiles) or not self.people or any(
                p.home not in LOCATIONS or not 0 <= p.shift < DAY for p in profiles):
            raise ValueError("Invalid regional roster")
        self.db.execute("CREATE TABLE IF NOT EXISTS regional_population (save TEXT PRIMARY KEY, state TEXT NOT NULL)")
        self.load()

    def load(self):
        row = self.db.execute("SELECT state FROM regional_population WHERE save=?", (self.world.save,)).fetchone()
        self.state = json.loads(row[0]) if row else {"clock": -1, "actors": {}}
        self.rebuild()

    def rebuild(self):
        self.queue = [(actor["due"], key) for key, actor in self.state["actors"].items() if key in self.people]
        heapq.heapify(self.queue)

    def persist(self):
        with self.db:
            self.db.execute("INSERT OR REPLACE INTO regional_population VALUES (?,?)",
                            (self.world.save, json.dumps(self.state, separators=(",", ":"))))

    def checkpoint(self, key):
        # Capture pending deadlines and the clock along with the battery image.
        if self.state["actors"]:
            self.db.execute("INSERT INTO regional_population VALUES (?,?)",
                            (key, json.dumps(self.state, separators=(",", ":"))))

    def discard(self):
        self.db.execute("DELETE FROM regional_population WHERE save=?", (self.world.save,))

    @staticmethod
    def morning(person, day):
        while day % 7 in person.days_off:
            day += 1
        return day * DAY + person.shift

    def initialize(self, second):
        for id_, person in self.people.items():
            morning = self.morning(person, second // DAY)
            self.state["actors"].setdefault(id_, {
                "location": person.home, "activity": "off_shift", "day": -1,
                "due": max(second, morning) if morning // DAY == second // DAY
                       and second % DAY < 18 * 3600 else self.morning(person, second // DAY + 1),
                "memory": [], "facts": {}, "bonds": {},
            })
        self.rebuild()

    def remember(self, actor, when, kind, **details):
        actor["memory"] = [*actor["memory"][-7:], {"second": when, "kind": kind, **details}]

    def start_goal(self, person, actor, when):
        old = actor.get("goal")
        generation = old["generation"] + 1 if old else 1
        return {"id": f"{person.id}:{generation}", "generation": generation, "priority": person.patience + 1,
                "progress": 0, "target": 3 + person.patience,
                "deadline": when + GOAL_WINDOW, "status": "active"}

    def step(self, person, actor, when):
        goal = actor.get("goal")
        day = when // DAY
        if actor["activity"] == person.role:
            if actor["day"] == day and goal and when < goal["deadline"]:
                self.advance_goal(person, actor, when)
            else:
                self.remember(actor, when, "missed_shift")
            actor.update(activity="off_shift", due=self.morning(person, day + 1))
            return
        if day % 7 in person.days_off:
            actor["due"] = self.morning(person, day + 1)
            return
        if goal and goal["status"] == "active" and when >= goal["deadline"]:
            goal["status"] = "expired"
            self.remember(actor, when, "goal_expired", goal=goal["id"])
        if not goal or goal["status"] != "active":
            actor["goal"] = self.start_goal(person, actor, when)
        actor.update(day=day, activity=person.role, due=when + 24)
        self.remember(actor, when, "shift", location=person.home)

    def advance_goal(self, person, actor, when):
        goal = actor["goal"]
        goal["progress"] += 1
        if goal["progress"] >= goal["target"]:
            goal["status"] = "completed"
            self.remember(actor, when, "goal_completed", goal=goal["id"])

    def tick(self, second):
        if type(second) is not int or second < self.state["clock"]:
            return 0
        initialized = not self.queue
        if initialized:
            self.initialize(second)
        self.state["clock"] = second
        processed = 0
        while self.queue and self.queue[0][0] <= second and processed < TRANSITIONS:
            due, id_ = heapq.heappop(self.queue)
            actor = self.state["actors"][id_]
            # After long absences, resume from at most two days ago.
            when = max(due, (second // DAY - 2) * DAY)
            self.step(self.people[id_], actor, when)
            heapq.heappush(self.queue, (actor["due"], id_))
            processed += 1
        if initialized or processed:
            self.persist()
        return processed
