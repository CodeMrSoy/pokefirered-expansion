"""Bounded, save-scoped Kanto routines and attributed cross-map reports."""

from dataclasses import dataclass

from reasoning import SIGHTINGS

DAY = 86400
TTL = 2 * DAY
BUDGET = 4
# Timings refer to clock seconds exported by the game, including across maps.
FIRST_LEG = 12
SECOND_LEG = 18
REVIEW = 60

SCHEMA = """
CREATE TABLE IF NOT EXISTS routine_event (
    save TEXT NOT NULL, event TEXT NOT NULL, route TEXT NOT NULL,
    fact TEXT NOT NULL, species INTEGER NOT NULL, source TEXT NOT NULL,
    started INTEGER NOT NULL, due INTEGER NOT NULL, expires INTEGER NOT NULL,
    stage TEXT NOT NULL, PRIMARY KEY (save, event)
);
CREATE INDEX IF NOT EXISTS routine_due ON routine_event(save, stage, due, event);
CREATE TABLE IF NOT EXISTS routine_clock (save TEXT PRIMARY KEY, observed INTEGER NOT NULL);
"""


@dataclass(frozen=True)
class Actor:
    npc: str
    area: str
    starts: int
    ends: int
    day_activity: str
    night_activity: str
    goal: str
    curiosity: int
    caution: int

    def activity(self, now):
        hour = now % DAY // 3600
        return self.day_activity if self.starts <= hour < self.ends else self.night_activity

    def next_shift(self, now):
        beginning = now - now % DAY + self.starts * 3600
        return beginning if now < beginning else beginning + DAY


@dataclass(frozen=True)
class Relay:
    guide: Actor
    scout: Actor
    researcher: Actor


KANTO = Relay(
    Actor("sign_guide", "pallet", 6, 20, "help_travelers", "sort_notes", "share_local_tips", 2, 1),
    Actor("route_scout", "route_1", 7, 19, "watch_the_route", "write_field_notes", "log_sightings", 3, 1),
    Actor("viridian_student", "viridian", 9, 18, "study_trail_habitats", "rest", "compare_habitat_notes", 2, 3),
)


class RoutineWorld:
    def __init__(self, memory, routes=None, *, standalone=()):
        self.memory = memory
        self.db = memory.db
        self.routes = {"kanto": KANTO} if routes is None else routes
        self.actors = {actor.npc: actor for relay in self.routes.values()
                       for actor in (relay.guide, relay.scout, relay.researcher)}
        self.actors.update((actor.npc, actor) for actor in standalone)
        self.by_npc = {actor.npc: key for key, relay in self.routes.items()
                       for actor in (relay.guide, relay.scout, relay.researcher)}
        self.db.executescript(SCHEMA)
        self.load()

    @property
    def save(self):
        return self.memory.save

    def load(self):
        row = self.db.execute("SELECT observed FROM routine_clock WHERE save=?", (self.save,)).fetchone()
        self.now = row[0] if row else None
        self.visible_at = self.now
        self.discovery_pending = True
        self.last_record = self.now
        self.next_due = self._deadline()

    def checkpoint(self, target):
        self.persist_clock()
        self.db.execute("""
            INSERT INTO routine_event
            SELECT ?,event,route,fact,species,source,started,due,expires,stage
            FROM routine_event WHERE save=?
        """, (target, self.save))
        self.db.execute("INSERT INTO routine_clock SELECT ?,observed FROM routine_clock WHERE save=?",
                        (target, self.save))

    def discard(self):
        self.db.execute("DELETE FROM routine_event WHERE save=?", (self.save,))
        self.db.execute("DELETE FROM routine_clock WHERE save=?", (self.save,))

    def persist_clock(self):
        if self.now is not None:
            self.db.execute("""
                INSERT INTO routine_clock VALUES (?,?)
                ON CONFLICT(save) DO UPDATE SET observed=excluded.observed
            """, (self.save, self.now))
            self.last_record = self.now

    def _deadline(self):
        row = self.db.execute("""
            SELECT MIN(due) FROM routine_event
            WHERE save=? AND stage IN ('to_route','to_city','await_review','reviewing')
        """, (self.save,)).fetchone()
        return row[0] if row else None

    def _heard(self, npc, fact, source):
        return self.db.execute("""
            SELECT 1 FROM npc_knowledge WHERE save=? AND npc=? AND fact=?
             AND origin='conversation' AND source=? AND verified=0
        """, (self.save, npc, fact, source)).fetchone() is not None

    def enqueue(self, route, fact, species, source, now):
        """Accept only a trusted social event with matching attribution."""
        relay = self.routes.get(route)
        if (not relay or species not in SIGHTINGS or not fact.startswith("pallet-sighting:")
                or self.now is not None and now < self.now):
            return False
        trusted = self.db.execute("""
            SELECT 1 FROM social_event WHERE save=? AND event=? AND species=? AND speaker=?
              AND listener=? AND area=? AND shared IS NOT NULL
        """, (self.save, fact, species, source, relay.guide.npc, relay.guide.area)).fetchone()
        if not trusted or not self._heard(relay.guide.npc, fact, source):
            return False
        event = f"{route}:{fact}"
        with self.db:
            row = self.db.execute("""
                INSERT OR IGNORE INTO routine_event VALUES (?,?,?,?,?,?,?,?,?, 'to_route')
            """, (self.save, event, route, fact, species, source, now, now + FIRST_LEG, now + TTL))
        if row.rowcount:
            self.next_due = self._deadline()
        return bool(row.rowcount)

    def _discover(self, now):
        for key, relay in self.routes.items():
            for fact, species, source in self.db.execute("""
                SELECT event,species,speaker FROM social_event
                WHERE save=? AND listener=? AND shared IS NOT NULL
            """, (self.save, relay.guide.npc)).fetchall():
                self.enqueue(key, fact, species, source, now)
        self.discovery_pending = False

    def tick(self, now):
        if now is None or now < 0:
            return []
        self.visible_at = now
        self.now = now if self.now is None else max(now, self.now)
        if self.discovery_pending:
            self._discover(self.now)
        if self.next_due is None or self.now < self.next_due:
            # Sudden time skips persist without writing at video-frame cadence.
            if self.last_record is None or self.now - self.last_record >= 60:
                with self.db:
                    self.persist_clock()
            return []
        with self.db:
            rows = self.db.execute("""
                SELECT event,route,fact,species,source,due,expires,stage FROM routine_event
                WHERE save=? AND stage IN ('to_route','to_city','await_review','reviewing') AND due<=?
                ORDER BY due,event LIMIT ?
            """, (self.save, self.now, BUDGET)).fetchall()
            changes = [self._advance(row) for row in rows]
            self.persist_clock()
        self.next_due = self._deadline()
        return changes

    def _advance(self, row):
        event, route, fact, species, source, due, expires, stage = row
        relay = self.routes.get(route)
        area, sender, receiver = ("", "", "")
        next_stage, next_due = "expired", self.now
        if relay and self.now < expires:
            if stage == "to_route":
                sender, receiver = relay.guide.npc, relay.scout.npc
                area = relay.scout.area
                if relay.scout.curiosity >= 2 and self._heard(sender, fact, source):
                    self._transfer(sender, receiver, species, "forward_sighting")
                    next_stage, next_due = "to_city", due + SECOND_LEG
            elif stage == "to_city":
                sender, receiver = relay.scout.npc, relay.researcher.npc
                area = relay.researcher.area
                if self._heard(sender, f"relay:{sender}:{species}", relay.guide.npc):
                    self._transfer(sender, receiver, species, "compare_habitat_notes")
                    # The cautious resident records a review, never a firsthand sighting.
                    actor = relay.researcher
                    if actor.caution < 2:
                        next_stage, next_due = "resolved", due
                    elif actor.activity(due) == actor.day_activity:
                        next_stage, next_due = "reviewing", due + REVIEW
                    else:
                        next_stage, next_due = "await_review", actor.next_shift(due)
            elif stage == "await_review":
                area = relay.researcher.area
                next_stage, next_due = "reviewing", due + REVIEW
            else:
                area = relay.researcher.area
                next_stage = "resolved"
                next_due = due
        self.db.execute("UPDATE routine_event SET stage=?,due=? WHERE save=? AND event=?",
                        (next_stage, next_due, self.save, event))
        return dict(event=event, source=source, sender=sender, receiver=receiver,
                    area=area, status=next_stage, at=self.now)

    def _transfer(self, sender, receiver, species, goal):
        learned = self.db.execute("""
            INSERT OR IGNORE INTO npc_knowledge(save,npc,fact,origin,source,verified)
            VALUES (?,?,?,'conversation',?,0)
        """, (self.save, receiver, f"relay:{receiver}:{species}", sender))
        if learned.rowcount:
            self.memory.social._relationship(sender, receiver, "share_local_notes", baseline=1)
            self.memory.social._relationship(receiver, sender, goal, baseline=1)

    def state(self, npc):
        actor = self.actors.get(npc)
        if actor is None or self.visible_at is None:
            return ()
        routine = actor.activity(self.visible_at)
        route = self.by_npc.get(npc)
        if route is None:
            return routine, actor.goal
        relay = self.routes[route]
        active = self.db.execute("""
            SELECT stage FROM routine_event WHERE save=? AND route=?
                AND stage IN ('to_route','to_city','await_review','reviewing')
            ORDER BY due,event
        """, (self.save, route)).fetchall()
        stages = {row[0] for row in active}
        if npc == relay.guide.npc and "to_route" in stages:
            return routine, "relay_sighting"
        if npc == relay.scout.npc and "to_city" in stages:
            return "record_report", "forward_sighting"
        if npc == relay.researcher.npc and "reviewing" in stages:
            return "compare_report", "review_secondhand_evidence"
        return routine, actor.goal
