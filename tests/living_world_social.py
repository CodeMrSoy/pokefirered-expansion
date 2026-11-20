"""Validate a real relay, provenance, cooldown, checkpoint branching and load."""

from pathlib import Path
from statistics import median, quantiles
import subprocess
import sys
from tempfile import TemporaryDirectory
from time import perf_counter, process_time

APP = Path(__file__).resolve().parents[1] / "experiments/living_world"
sys.path.insert(0, str(APP))

from bridge import Conversation, validate
from knowledge import retrieve
from reasoning import guide_reply, reaction_page
from social import COOLDOWN, DELAY, GUIDE, WATTS
from world import WorldMemory

PIKACHU = Conversation(WATTS, 25)
SQUIRTLE = Conversation(WATTS, 7)
GUIDE_ALONE = Conversation(GUIDE, None)


def keys(catalog, memory, who):
    return {fact.key for fact in retrieve(catalog, memory.context(who), limit=8)}


def verify(catalog, db):
    memory = WorldMemory(db, "demo", b"first")
    assert memory.social.deadline is None
    assert not memory.social.queue_sighting(memory.context(PIKACHU))
    assert "pallet-sighting:25" not in keys(catalog, memory, GUIDE_ALONE)
    memory.apply(memory.context(PIKACHU), "REMEMBER_EVENT")
    due = memory.social.deadline
    memory.apply(memory.context(SQUIRTLE), "REMEMBER_EVENT")
    assert memory.social.tick(due - 0.1) is None
    assert memory.social.scene() is None
    memory.checkpoint(b"second")
    memory.close()

    memory = WorldMemory(db, "demo", b"second")
    assert memory.social.deadline == due
    memory.social.tick(due)
    observed = memory.knowledge(GUIDE, None)
    assert len(observed) == 1
    assert observed[0]["source"] == WATTS
    assert observed[0]["origin"] == "conversation" and observed[0]["verified"] == 0
    assert observed[0]["acquired_at"]
    assert not memory.context(Conversation(GUIDE, 25)).remembered
    assert "pallet-sighting:25" in keys(catalog, memory, GUIDE_ALONE)
    assert "pallet-sighting:25" not in keys(catalog, memory, Conversation("oak", None))
    assert "pallet-sighting:25" not in keys(catalog, memory, Conversation(WATTS, None))
    turn = memory.social.guide_turn("pallet-sighting:25")
    assert turn.can_request and not turn.requested
    assert not memory.social.apply_guide_turn(turn, "CONSERVE")
    assert not reaction_page("I observed Pikachu at noon.")
    assert reaction_page("I would rather be careful.")
    assert memory.social.apply_guide_turn(turn, "ASK_WATTS", now=due)
    try:
        memory.social.apply_guide_turn(turn, "ASK_WATTS")
    except ValueError:
        pass
    else:
        raise AssertionError("Duplicate follow-up was accepted")
    assert not memory.social.guide_turn("pallet-sighting:7").can_request
    assert memory.social.tick(due + DELAY)["status"] == "answered_unknown_time"
    assert "wasn't sure when" in validate(guide_reply(memory.social.guide_turn(turn.fact)).dialogue).decode()
    assert memory.social.deadline == due + COOLDOWN
    assert memory.social.tick(due + COOLDOWN - 0.1) is None
    memory.social.tick(due + COOLDOWN)
    assert memory.social.deadline is None
    assert len(memory.knowledge(GUIDE, None)) == 2
    encounter = memory.context(PIKACHU)
    memory.apply(encounter, "COMMENT_ON_POKEMON")
    assert memory.social.deadline is None, "Known report was requeued"
    relations = memory.db.execute(
        "SELECT familiarity, trust, affinity, experiences, goal FROM social_relationship WHERE save=?",
        (memory.save,),
    ).fetchall()
    assert len(relations) == 2 and all(row[:4] == (2, 3, 2, 2) for row in relations)
    assert {row[4] for row in relations} == {"share_local_notes", "note_uncertain_sighting"}

    scene = memory.social.scene()
    assert verify_scene(scene, "Pikachu")
    memory.social.displayed(scene[0])
    memory.close()
    memory = WorldMemory(db, "demo", b"second")
    assert memory.social.guide_turn("pallet-sighting:25").requested
    assert verify_scene(memory.social.scene(), "Squirtle")
    memory.social.displayed(memory.social.scene()[0])
    assert "Watts: I couldn't tell you." in validate(memory.social.scene()[1]).decode()
    assert "pallet-sighting:25" in keys(catalog, memory, GUIDE_ALONE)
    assert memory.context(PIKACHU).remembered
    memory.checkpoint(b"first")
    assert memory.knowledge(GUIDE, None) == []
    assert not memory.social.guide_turn("pallet-sighting:25").can_request
    memory.close()

    memory = WorldMemory(db, "normal", b"second")
    assert memory.social.scene() is None and memory.knowledge(GUIDE, None) == []
    memory.apply(memory.context(PIKACHU), "REMEMBER_EVENT")
    memory.db.execute("UPDATE social_event SET listener='oak' WHERE save=?", (memory.save,))
    memory.db.commit()
    assert memory.social.tick(memory.social.deadline)["status"] == "rejected"
    assert memory.knowledge("oak", None) == []
    memory.close()
    print("PASS pending reload, report attribution, cooldown, coalescing, relationships, scene replay,"
          " checkpoint/slot isolation and rejection of unauthorized recipient.")


def verify_scene(scene, species):
    return scene and f"Watts: I saw a {species}." in validate(scene[1]).decode("ascii")


def benchmark(db, *, noise, repetitions=100):
    memory = WorldMemory(db, "benchmark", b"seed")
    with memory.db:
        memory.db.executemany("INSERT INTO social_event VALUES (?,?,?,?,?,?,?,?,?,?)", (
            (f"other-save:{i % 75}", f"other-event:{i}", f"npc-{i}", f"peer-{i}", "other", 150,
             0, 0, None, 0) for i in range(noise)
        ))
        memory.db.executemany("INSERT INTO social_relationship VALUES (?,?,?,?,?,?,?,?)", (
            (memory.save, f"npc-{i}", f"peer-{i}", 1, 1, 1, 1, "other") for i in range(noise)
        ))
    idle_start = process_time()
    for index in range(250000):
        memory.social.tick(index)
    idle_us = (process_time() - idle_start) * 1e6 / 250000
    scheduling, transfer = [], []
    for index in range(repetitions):
        memory.checkpoint(index.to_bytes(4, "little"))
        encounter = memory.context(PIKACHU)
        start = perf_counter()
        memory.apply(encounter, "REMEMBER_EVENT")
        scheduling.append((perf_counter() - start) * 1000)
        start = perf_counter()
        memory.social.tick(memory.social.deadline)
        transfer.append((perf_counter() - start) * 1000)
        # Use a fresh logical slot to measure scheduling a first sighting.
        memory = reset_benchmark(memory, db, index)
    memory.close()
    p95 = lambda values: quantiles(values, n=100)[94]
    print(f"{noise} synthetic NPC bonds and queued events, idle {idle_us:.3f} us CPU/tick, "
          f"witness+schedule p50/p95 {median(scheduling):.3f}/{p95(scheduling):.3f} ms, "
          f"transfer+memory p50/p95 {median(transfer):.3f}/{p95(transfer):.3f} ms")


def reset_benchmark(memory, db, index):
    memory.close()
    return WorldMemory(db, f"benchmark:{index}", b"seed")


if __name__ == "__main__":
    with TemporaryDirectory() as directory:
        root = Path(directory)
        catalog = root / "catalog.sqlite3"
        subprocess.run([sys.executable, "-B", APP / "build-knowledge.py", catalog], check=True)
        verify(catalog, root / "verify.sqlite3")
        benchmark(root / "baseline.sqlite3", noise=0)
        benchmark(root / "scale.sqlite3", noise=5000)
