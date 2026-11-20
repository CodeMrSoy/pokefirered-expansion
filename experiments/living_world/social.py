"""Deterministic, save-scoped Pallet social simulation on the desktop host."""

import json
from time import time

from profiles import KNOWLEDGE_PROFILES, SOCIAL_CONTACTS

WATTS = "pc_resident"
GUIDE = "sign_guide"
SIGHTINGS = {25: "Pikachu", 7: "Squirtle"}
DELAY = 4
COOLDOWN = 12

SCHEMA = """
CREATE TABLE IF NOT EXISTS social_event (
    save TEXT NOT NULL, event TEXT NOT NULL, speaker TEXT NOT NULL,
    listener TEXT NOT NULL, area TEXT NOT NULL, species INTEGER NOT NULL,
    observed REAL NOT NULL, due REAL NOT NULL, shared REAL, displayed INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (save, event)
);
CREATE INDEX IF NOT EXISTS social_due ON social_event(save, shared, due, event);
CREATE TABLE IF NOT EXISTS social_relationship (
    save TEXT NOT NULL, npc TEXT NOT NULL, peer TEXT NOT NULL,
    familiarity INTEGER NOT NULL, trust INTEGER NOT NULL, affinity INTEGER NOT NULL,
    experiences INTEGER NOT NULL, goal TEXT NOT NULL,
    PRIMARY KEY (save, npc, peer)
);
"""


class SocialWorld:
    def __init__(self, memory):
        self.memory = memory
        self.db = memory.db
        self.db.executescript(SCHEMA)
        self.deadline = self.next_deadline()

    @property
    def save(self):
        return self.memory.save

    def next_deadline(self):
        row = self.db.execute("""
            SELECT due FROM social_event WHERE save=? AND shared IS NULL
            ORDER BY due, event LIMIT 1
        """, (self.save,)).fetchone()
        return row[0] if row else None

    def checkpoint(self, target):
        self.db.execute("""
            INSERT INTO social_event
            SELECT ?, event, speaker, listener, area, species, observed, due, shared, displayed
            FROM social_event WHERE save=?
        """, (target, self.save))
        self.db.execute("""
            INSERT INTO social_relationship
            SELECT ?, npc, peer, familiarity, trust, affinity, experiences, goal
            FROM social_relationship WHERE save=?
        """, (target, self.save))

    def discard(self):
        self.db.execute("DELETE FROM social_event WHERE save=?", (self.save,))
        self.db.execute("DELETE FROM social_relationship WHERE save=?", (self.save,))

    def queue_sighting(self, encounter, now=None):
        """Called in the same transaction as the witnessed follower record."""
        if encounter.npc != WATTS or encounter.visible_species not in SIGHTINGS:
            return False
        now = time() if now is None else now
        species = encounter.visible_species
        observed = self.db.execute("""
            SELECT unixepoch(acquired_at)
            FROM npc_knowledge WHERE save=? AND npc=? AND fact=?
              AND origin='witnessed' AND source='visible_follower' AND verified=1
        """, (self.save, WATTS, str(species))).fetchone()
        if not observed:
            return False
        event = f"pallet-sighting:{species}"
        last = self.db.execute("SELECT MAX(due) FROM social_event WHERE save=?", (self.save,)).fetchone()[0]
        due = max(now + DELAY, last + COOLDOWN if last is not None else now)
        result = self.db.execute("""
            INSERT OR IGNORE INTO social_event(save,event,speaker,listener,area,species,observed,due)
            VALUES (?,?,?,?,?,?,?,?)
        """, (self.save, event, WATTS, GUIDE, "pallet", species, observed[0], due))
        return bool(result.rowcount)

    def tick(self, now):
        """Idle calls cost one deadline check. Each due tick handles at most one event."""
        if self.deadline is None or now < self.deadline:
            return None
        with self.db:
            self.db.execute("BEGIN IMMEDIATE")
            row = self.db.execute("""
                SELECT event, speaker, listener, area, species, observed FROM social_event
                WHERE save=? AND shared IS NULL AND due<=? ORDER BY due, event LIMIT 1
            """, (self.save, now)).fetchone()
            result = self._share(row, now) if row else None
        self.deadline = self.next_deadline()
        return result

    def _share(self, row, now):
        event, speaker, listener, area, species, observed = row
        # Only this vetted social action is exposed. Reports never qualify as
        # first-hand evidence for a subsequent transmission.
        witness = self.db.execute("""
            SELECT 1 FROM npc_knowledge WHERE save=? AND npc=? AND fact=?
              AND origin='witnessed' AND source='visible_follower' AND verified=1
        """, (self.save, speaker, str(species))).fetchone()
        relationship = self.db.execute("""
            SELECT trust FROM social_relationship WHERE save=? AND npc=? AND peer=?
        """, (self.save, speaker, listener)).fetchone()
        trust = relationship[0] if relationship else SOCIAL_CONTACTS.get(speaker, {}).get(listener, 0)
        allowed = (speaker == WATTS and listener == GUIDE and area == "pallet"
                   and species in SIGHTINGS and event == f"pallet-sighting:{species}"
                   and KNOWLEDGE_PROFILES[speaker][0] == KNOWLEDGE_PROFILES[listener][0] == area
                   and listener in SOCIAL_CONTACTS[speaker] and speaker in SOCIAL_CONTACTS[listener]
                   and trust >= 1 and witness)
        if not allowed:
            self.db.execute("DELETE FROM social_event WHERE save=? AND event=?", (self.save, event))
            return {"event": event, "status": "rejected"}
        result = self.db.execute("""
            INSERT OR IGNORE INTO npc_knowledge(save,npc,fact,origin,source,verified)
            VALUES(?,?,?,'conversation',?,0)
        """, (self.save, listener, event, speaker))
        if result.rowcount:
            self._relationship(speaker, listener, "share_local_notes")
            self._relationship(listener, speaker, "pass_along_sightings")
        self.db.execute("UPDATE social_event SET shared=? WHERE save=? AND event=?",
                        (now, self.save, event))
        return dict(event=event, speaker=speaker, listener=listener, species=species,
                    area=area, observed=observed, shared=now, status="shared")

    def _relationship(self, npc, peer, goal):
        self.db.execute("""
            INSERT INTO social_relationship VALUES (?,?,?,1,?,1,1,?)
            ON CONFLICT(save,npc,peer) DO UPDATE SET
                familiarity=MIN(familiarity+1,5), trust=MIN(trust+1,5),
                affinity=MIN(affinity+1,5), experiences=experiences+1, goal=excluded.goal
        """, (self.save, npc, peer, SOCIAL_CONTACTS[npc][peer] + 1, goal))

    def scene(self):
        row = self.db.execute("""
            SELECT event, species FROM social_event WHERE save=? AND shared IS NOT NULL
            AND displayed=0 AND speaker=? AND listener=? AND area='pallet'
            ORDER BY shared,event LIMIT 1
        """, (self.save, WATTS, GUIDE)).fetchone()
        if not row or row[1] not in SIGHTINGS:
            return None
        event, species = row
        text = f"Watts: I saw a {SIGHTINGS[species]}.\nGuide: I'll tell visitors."
        return event, json.dumps({"action": "SAY_DIALOGUE", "text": text})

    def displayed(self, event):
        with self.db:
            self.db.execute("UPDATE social_event SET displayed=1 WHERE save=? AND event=? AND shared IS NOT NULL",
                            (self.save, event))
