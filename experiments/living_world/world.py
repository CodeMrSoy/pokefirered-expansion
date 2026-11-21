"""Save-scoped Pallet resident state. Only trusted observations update SQLite."""

from dataclasses import dataclass
import hashlib
import json
import sqlite3
from uuid import uuid4

from director import WorldDirector
from profiles import PROFILES, WATTS
from routines import RoutineWorld
from social import SocialWorld
from society import Society

QUEST = "pond_survey"


@dataclass(frozen=True)
class Encounter:
    npc: str
    visible_species: int | None
    remembered: bool = False
    trust: int = 0
    quest: str = "none"
    quest_species: int | None = None
    evidence: tuple[str, ...] = ()

    @property
    def completes_quest(self):
        return self.npc == "pc_resident" and self.quest == "offered" and self.visible_species not in (None, self.quest_species)

    def allowed(self):
        if self.npc != "pc_resident":
            action = "COMMENT_ON_POKEMON" if self.npc in PROFILES and self.visible_species else "SAY_DIALOGUE"
            return (action,)
        if self.completes_quest:
            return ("SAY_DIALOGUE",)
        if (self.quest == "none" and self.remembered
                and self.visible_species == WATTS["favorite_species"]):
            return ("PROPOSE_OPTIONAL_QUEST", "COMMENT_ON_POKEMON")
        if self.visible_species == WATTS["favorite_species"] and not self.remembered and self.trust == 0:
            return ("ADJUST_RELATIONSHIP", "REMEMBER_EVENT")
        if self.visible_species is not None:
            return ("COMMENT_ON_POKEMON", "SAY_DIALOGUE") if self.remembered else (
                "REMEMBER_EVENT", "COMMENT_ON_POKEMON"
            )
        return ("SAY_DIALOGUE",)


class WorldMemory:
    def __init__(self, path, slot, battery, *, unsaved=False):
        self.db = sqlite3.connect(path)
        self.slot = slot
        self.save = "unsaved:" + uuid4().hex if unsaved else self._key(battery)
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS npc_memory (
                save TEXT NOT NULL, npc TEXT NOT NULL, state TEXT NOT NULL,
                PRIMARY KEY (save, npc)
            )
        """)
        self.db.executescript("""
            CREATE TABLE IF NOT EXISTS npc_knowledge (
                save TEXT NOT NULL, npc TEXT NOT NULL, fact TEXT NOT NULL,
                origin TEXT NOT NULL CHECK (origin IN ('witnessed', 'conversation')),
                source TEXT NOT NULL, verified INTEGER NOT NULL CHECK (verified IN (0, 1)),
                acquired_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (save, npc, fact, origin)
            );
            CREATE TABLE IF NOT EXISTS npc_checkpoint (save TEXT PRIMARY KEY);
        """)
        with self.db:
            self.db.execute("INSERT OR IGNORE INTO npc_checkpoint SELECT DISTINCT save FROM npc_memory")
            self.db.execute("INSERT OR IGNORE INTO npc_checkpoint VALUES (?)", (self.save,))

        self.social = SocialWorld(self)
        self.routines = RoutineWorld(self)
        self.director = WorldDirector(self)
        self.society = Society(self)

    def _key(self, battery):
        return self.slot + ":" + hashlib.sha256(battery).hexdigest()

    def checkpoint(self, battery):
        next_save = self._key(battery)
        if next_save != self.save:
            with self.db:
                new = self.db.execute("INSERT OR IGNORE INTO npc_checkpoint VALUES (?)", (next_save,))
                if new.rowcount:
                    self.db.execute("""
                        INSERT INTO npc_memory (save, npc, state)
                        SELECT ?, npc, state FROM npc_memory WHERE save = ?
                    """, (next_save, self.save))
                    self.db.execute("""
                        INSERT INTO npc_knowledge (save, npc, fact, origin, source, verified, acquired_at)
                        SELECT ?, npc, fact, origin, source, verified, acquired_at
                        FROM npc_knowledge WHERE save = ?
                    """, (next_save, self.save))
                    self.social.checkpoint(next_save)
                    self.routines.checkpoint(next_save)
                    self.director.checkpoint(next_save)
                    self.society.checkpoint(next_save)
                self._discard_unsaved()
            self.save = next_save
            self.social.deadline = self.social.next_deadline()
            self.routines.load()
            self.director.load()
            self.society.load()

    def _discard_unsaved(self):
        if self.save.startswith("unsaved:"):
            self.db.execute("DELETE FROM npc_memory WHERE save=?", (self.save,))
            self.db.execute("DELETE FROM npc_knowledge WHERE save=?", (self.save,))
            self.social.discard()
            self.routines.discard()
            self.director.discard()
            self.society.discard()
            self.db.execute("DELETE FROM npc_checkpoint WHERE save=?", (self.save,))

    def knowledge(self, npc, species):
        rows = self.db.execute("""
            SELECT fact, origin, source, verified, acquired_at FROM npc_knowledge
            WHERE save=? AND npc=? AND fact IN (?, 'pond-survey', 'pallet-sighting:25', 'pallet-sighting:7', ?, ?)
            ORDER BY fact, origin
        """, (self.save, npc, str(species), f"relay:{npc}:25", f"relay:{npc}:7")).fetchall()
        return [dict(zip(("fact", "origin", "source", "verified", "acquired_at"), row)) for row in rows]

    def _witness(self, npc, fact, source):
        self.db.execute("""
            INSERT OR IGNORE INTO npc_knowledge (save, npc, fact, origin, source, verified)
            VALUES (?, ?, ?, 'witnessed', ?, 1)
        """, (self.save, npc, fact, source))

    def snapshot(self, npc):
        row = self.db.execute("SELECT state FROM npc_memory WHERE save=? AND npc=?",
                              (self.save, npc)).fetchone()
        return json.loads(row[0]) if row else {
            "seen": [], "trust": 0, "quest": "none", "quest_species": None,
        }

    def context(self, conversation):
        state = self.snapshot(conversation.npc)
        species = conversation.visible_species
        evidence = tuple(
            f"{record['origin']}:{record['fact']}"
            for record in self.knowledge(conversation.npc, species)
            if record["verified"] or record["origin"] == "conversation"
        )
        return Encounter(conversation.npc, species, species in state["seen"],
                         state["trust"], state["quest"], state["quest_species"], evidence)

    def apply(self, encounter, action):
        with self.db:
            self.db.execute("BEGIN IMMEDIATE")
            changes = self._apply(encounter, action)
            if self.social.queue_sighting(encounter):
                changes.append("social_sighting_scheduled")
        if "social_sighting_scheduled" in changes:
            self.social.deadline = self.social.next_deadline()
        return changes

    def _apply(self, encounter, action):
        current = self.context(encounter)
        if current != encounter or current.npc not in PROFILES or action not in current.allowed():
            raise ValueError("Stale encounter or action outside allowed game state")

        state = self.snapshot(current.npc)
        changes = []
        if current.visible_species is not None:
            self._witness(current.npc, str(current.visible_species), "visible_follower")
            if not current.remembered:
                state["seen"].append(current.visible_species)
                changes.append("REMEMBER_EVENT")
        if action == "ADJUST_RELATIONSHIP":
            state["trust"] += 1
            changes.append("ADJUST_RELATIONSHIP")
        if action == "PROPOSE_OPTIONAL_QUEST":
            state["quest"] = "offered"
            state["quest_species"] = current.visible_species
            changes.append(QUEST + ":offered")
        elif current.completes_quest:
            state["quest"] = "completed"
            state["trust"] += 2
            self._witness(current.npc, "pond-survey", "validated_quest_completion")
            changes.append(QUEST + ":completed")
        if changes:
            self.db.execute("""
                INSERT INTO npc_memory(save, npc, state) VALUES (?, ?, ?)
                ON CONFLICT(save, npc) DO UPDATE SET state=excluded.state
            """, (self.save, current.npc, json.dumps(state, separators=(",", ":"))))
        return changes

    def close(self):
        with self.db:
            if not self.save.startswith("unsaved:"):
                self.routines.persist_clock()
            self._discard_unsaved()
        self.db.close()
