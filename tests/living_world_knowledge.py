"""Exercise the packaged Phase 3 catalog, save isolation and optional live model."""

from dataclasses import replace
import json
import os
from pathlib import Path
import shutil
import sqlite3
from statistics import median, quantiles
import subprocess
import sys
import tempfile
from time import perf_counter_ns
from unittest.mock import patch
import tracemalloc

APP = Path(__file__).resolve().parents[1] / "experiments/living_world"
sys.path.insert(0, str(APP))

from bridge import Conversation, validate
from inference import LocalModel
from knowledge import prompt_facts, retrieve
from profiles import KNOWLEDGE_PROFILES
from world import Encounter, WorldMemory

NPCS = {
    "pc_resident": "watts:pikachu",
    "oak": "evolution:PIKACHU",
    "blue": "battle:electric",
    "daisy": "care:pikachu",
}


def keys(path, encounter, limit=8):
    return {fact.key for fact in retrieve(path, encounter, limit=limit)}


def verify_access(path):
    for npc, own in NPCS.items():
        allowed = keys(path, Encounter(npc, 25))
        assert allowed.intersection(NPCS.values()) == {own}, (npc, allowed)
        assert "witnessed:25" not in allowed and "vidra:koga" not in allowed
    assert keys(path, Encounter("blue", None)) >= {"pallet:league"}
    assert "pallet:league" not in keys(path, Encounter("oak", None))
    assert "pallet:daisy-care" not in keys(path, Encounter("daisy", None))
    assert "survey:pond" not in keys(path, Encounter("pc_resident", None, trust=3))
    assert "survey:pond" not in keys(path, Encounter("pc_resident", None, evidence=("witnessed:pond-survey",)))
    assert "survey:pond" in keys(path, Encounter("pc_resident", None, trust=2, evidence=("witnessed:pond-survey",)))
    assert "kanto:lance-rumor" not in keys(path, Encounter("blue", None, evidence=("witnessed:lance-journal",)))
    hearsay = Encounter("blue", None, evidence=("conversation:lance-journal",))
    rumor = next(fact for fact in retrieve(path, hearsay, limit=8) if fact.key == "kanto:lance-rumor")
    assert rumor.kind == "rumor" and "rumor:" in prompt_facts((rumor,))
    assert "kanto:lance-rumor" not in keys(path, replace(hearsay, npc="oak"))
    assert len(retrieve(path, Encounter("oak", 25), limit=1)) == 1
    assert not retrieve(path, Encounter("oak", 25), budget=1)


def verify_memory(path, directory):
    save = directory / "memory.sqlite3"
    show = Conversation("pc_resident", 25)
    daisy = Conversation("daisy", 25)
    memory = WorldMemory(save, "demo", b"before")
    memory.checkpoint(b"later")
    before = memory.context(show)
    assert "witnessed:25" not in keys(path, before)
    try:
        memory.apply(before, "SET_FLAG")
    except ValueError:
        pass
    else:
        raise AssertionError("Illegal action passed")
    assert memory.knowledge(show.npc, 25) == []
    memory.apply(before, "REMEMBER_EVENT")
    after = memory.context(show)
    memory.apply(after, "COMMENT_ON_POKEMON")
    records = memory.knowledge(show.npc, 25)
    assert len(records) == 1
    assert records[0]["source"] == "visible_follower" and records[0]["verified"] == 1
    assert records[0]["acquired_at"]
    assert "witnessed:25" in keys(path, after)
    assert "witnessed:25" not in keys(path, memory.context(daisy))
    memory.close()

    memory = WorldMemory(save, "demo", b"later")
    reopened = memory.context(show)
    assert memory.knowledge(show.npc, 25) == records
    assert "witnessed:25" in keys(path, reopened)
    memory.apply(reopened, "PROPOSE_OPTIONAL_QUEST")
    squirtle = Conversation("pc_resident", 7)
    assert "pond_survey:completed" in memory.apply(memory.context(squirtle), "SAY_DIALOGUE")
    assert "survey:pond" in keys(path, memory.context(Conversation("pc_resident", None)))
    memory.checkpoint(b"before")
    assert memory.knowledge(show.npc, 25) == [] and not memory.context(show).remembered
    memory.close()
    unrelated = WorldMemory(save, "normal", b"later")
    assert "witnessed:25" not in keys(path, unrelated.context(show))
    unrelated.close()
    print("Verified acquisition, deduplication, reopen, rollback, slot/NPC isolation and survey persistence.")
    return before, reopened


def benchmark(path, npcs):
    requests = [Encounter(npc, species) for npc in npcs for species in (25, 7, None)]
    durations = []
    for i in range(1200):
        start = perf_counter_ns()
        retrieve(path, requests[i % len(requests)])
        durations.append((perf_counter_ns() - start) / 1e6)
    tracemalloc.start()
    for encounter in requests[:12]:
        retrieve(path, encounter)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    print(f"Catalog {path.stat().st_size} bytes, {len(npcs)} NPCs, host Python allocation peak {peak} bytes"
          f", p50 {median(durations):.3f} ms, p95 {quantiles(durations, n=100)[94]:.3f} ms")


def live_model(runtime, path, before, remembered):
    model = LocalModel(runtime, {"25": "Pikachu", "7": "Squirtle"}, catalog=path)
    try:
        with patch.object(model.worker, "generate", return_value=("Unapproved words.\nValid ASCII.", {})):
            try:
                model.plan(Encounter("oak", 25))
            except ValueError as error:
                assert "outside approved choices" in str(error)
            else:
                raise AssertionError("Valid wire text outside allowed lines passed")
        expected = {
            "pc_resident": "Easy around my cables.",
            "oak": "A Thunder Stone does it.",
            "blue": "Water teams hate sparks.",
            "daisy": "Even sparks need a rest.",
        }
        pid = None
        for encounter in [before, *(Encounter(npc, 25) for npc in tuple(NPCS)[1:]),
                          Encounter("pc_resident", 7), remembered]:
            proposal = model.plan(encounter)
            reply = validate(proposal.dialogue).decode()
            if encounter.visible_species == 25 and not encounter.remembered:
                assert expected[encounter.npc] in reply, reply
            if encounter.remembered:
                assert "witnessed:25" in proposal.knowledge and "remember" in proposal.context_sent
            if pid is None:
                pid = model.worker.process.pid
            assert model.worker.process.pid == pid
            print(json.dumps({"npc": encounter.npc, "dialogue": reply, "action": proposal.action,
                              "facts": proposal.knowledge, **proposal.metrics}))
    finally:
        model.close()


def main():
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        path = root / "world-knowledge.sqlite3"
        subprocess.run([sys.executable, "-B", APP / "build-knowledge.py", path], check=True)
        verify_access(path)
        before, remembered = verify_memory(path, root)
        benchmark(path, tuple(KNOWLEDGE_PROFILES))
        scale = root / "scale.sqlite3"
        shutil.copyfile(path, scale)
        with sqlite3.connect(scale) as db:
            db.executemany("INSERT INTO fact VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (
                (f"benchmark:{index}", "canonical", "species", 100 + index % 1000, f"area{index % 150}",
                 "vidra", "local", "", 0, "", 20, "Synthetic load test.", "", "benchmark")
                for index in range(25000)
            ))
        db.close()
        verify_access(scale)
        copies = {f"benchmark_resident_{number}": KNOWLEDGE_PROFILES["pc_resident"]
                  for number in range(300)}
        with patch.dict(KNOWLEDGE_PROFILES, copies):
            benchmark(scale, tuple(KNOWLEDGE_PROFILES))
        runtime = os.environ.get("LIVING_WORLD_INFERENCE_RUNTIME")
        if runtime:
            live_model(Path(runtime), path, before, remembered)


if __name__ == "__main__":
    main()
