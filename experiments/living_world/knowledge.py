"""Read-only lore retrieval. Permissions come from the game hook and NPC profile."""

from contextlib import closing
from dataclasses import dataclass
import sqlite3

from bridge import LINE
from profiles import KNOWLEDGE_PROFILES

SCHEMA = """
CREATE TABLE fact (
    key TEXT PRIMARY KEY,
    kind TEXT NOT NULL CHECK (kind IN ('canonical', 'belief', 'rumor', 'discovery')),
    topic TEXT NOT NULL,
    species INTEGER,
    area TEXT NOT NULL,
    region TEXT NOT NULL,
    access TEXT NOT NULL CHECK (access IN
        ('public', 'expertise', 'local', 'character', 'personal', 'witnessed', 'conversation')),
    required TEXT NOT NULL,
    min_trust INTEGER NOT NULL CHECK (min_trust >= 0),
    progress TEXT NOT NULL,
    priority INTEGER NOT NULL,
    text TEXT NOT NULL CHECK (length(text) BETWEEN 1 AND 160),
    line TEXT NOT NULL,
    source TEXT NOT NULL
);
CREATE INDEX fact_species ON fact(species, priority DESC);
CREATE INDEX fact_area ON fact(area, species, priority DESC);
CREATE INDEX fact_topic ON fact(topic, priority DESC);
CREATE TABLE dialogue_example (
    npc TEXT NOT NULL,
    species INTEGER NOT NULL,
    remembered INTEGER NOT NULL CHECK (remembered IN (0, 1)),
    line TEXT NOT NULL,
    source TEXT NOT NULL,
    PRIMARY KEY(npc, species, remembered)
);
PRAGMA user_version = 1;
"""


@dataclass(frozen=True)
class Fact:
    key: str
    kind: str
    text: str
    line: str
    source: str


def ecological_fact(report, day):
    if not report or day - report["observed_day"] > 21:
        return None
    kind = report["kind"]
    if kind == "named_local_report":
        line = "A rare Pokemon was seen."
    elif report["activity"] == "received_from_contact":
        line = "I heard the wildlife moved."
    elif kind == "migration_arrived":
        line = "I saw wild Pokemon arrive."
    elif kind == "unusual_sighting":
        line = "I thought I saw a rare one."
    else:
        line = "The local wildlife shifted."
    source = (f"ecology:{report['source']}:{report['location']}:"
              f"{report['observed_day']}:{report['confidence']}")
    return Fact(source, "rumor", line, line, source)


def retrieve(path, encounter, *, limit=2, budget=220):
    """Return only facts the NPC can use in this conversation."""
    profile = KNOWLEDGE_PROFILES.get(encounter.npc)
    if profile is None:
        return ()
    if not 1 <= limit <= 8 or not 1 <= budget <= 800:
        raise ValueError("Invalid knowledge budget")
    area, regions, expertise, characters, progress = profile
    # Only successful game-hook observations can supply personal evidence.
    evidence = encounter.evidence
    params = {
        "species": encounter.visible_species, "area": area, "trust": encounter.trust,
        "regions": ",".join(regions), "expertise": ",".join(expertise),
        "characters": ",".join(characters), "npc": encounter.npc,
        "progress": ",".join(progress), "evidence": ",".join(evidence), "limit": limit,
    }
    with closing(sqlite3.connect(path.resolve().as_uri() + "?mode=ro", uri=True)) as db:
        if db.execute("PRAGMA user_version").fetchone() != (1,):
            raise ValueError("Unsupported world knowledge catalog version")
        rows = db.execute("""
            SELECT key, kind, text, line, source
            FROM fact
            WHERE (species = :species OR (species IS NULL AND area = :area))
              AND (region = '' OR instr(',' || :regions || ',', ',' || region || ',') > 0)
              AND min_trust <= :trust
              AND (progress = '' OR instr(',' || :progress || ',', ',' || progress || ',') > 0)
              AND CASE access
                WHEN 'public' THEN 1
                WHEN 'expertise' THEN instr(',' || :expertise || ',', ',' || required || ',') > 0
                WHEN 'local' THEN area = :area
                WHEN 'character' THEN instr(',' || :characters || ',', ',' || required || ',') > 0
                WHEN 'personal' THEN required = :npc
                WHEN 'witnessed' THEN instr(',' || :evidence || ',', ',witnessed:' || required || ',') > 0
                WHEN 'conversation' THEN instr(',' || :evidence || ',', ',conversation:' || required || ',') > 0
                ELSE 0
              END
              AND (kind NOT IN ('rumor', 'belief') OR access IN ('personal', 'conversation'))
            ORDER BY (topic='local_news' AND :area IN ('route_1','viridian')) DESC,
                     species IS NOT NULL DESC, priority DESC, key
            LIMIT :limit
        """, params).fetchall()

    selected = []
    candidates = [Fact(*row) for row in rows]
    if encounter.ecology is not None:
        candidates.insert(0, encounter.ecology)
    for fact in candidates:
        if fact.line and not LINE.fullmatch(fact.line):
            raise ValueError("Invalid dialogue line in world knowledge catalog")
        cost = len(f"{fact.kind}: {fact.text}".encode("utf-8")) + 2
        if len(selected) < limit and cost <= budget:
            selected.append(fact)
            budget -= cost
    return tuple(selected)


def prompt_facts(facts):
    return " | ".join(f"{fact.kind}: {fact.text}" for fact in facts)


def retrieve_examples(path, encounter):
    """Fetch one reviewed voice line for this NPC and companion, if any."""
    with closing(sqlite3.connect(path.resolve().as_uri() + "?mode=ro", uri=True)) as db:
        if not db.execute("SELECT 1 FROM sqlite_master WHERE name='dialogue_example'").fetchone():
            return ()
        row = db.execute("""
            SELECT line FROM dialogue_example
            WHERE npc=? AND species=? AND remembered=?
        """, (encounter.npc, encounter.visible_species or 0, encounter.remembered)).fetchone()
        return row if row and LINE.fullmatch(row[0]) else ()
