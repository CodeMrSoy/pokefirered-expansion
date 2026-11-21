"""Exercise the production routine scheduler with real and synthetic Kanto saves."""

from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace
import json
from pathlib import Path
import random
import subprocess
import sys
from tempfile import TemporaryDirectory
from time import perf_counter, process_time
import tracemalloc
from types import SimpleNamespace

APP = Path(__file__).resolve().parents[1] / "experiments/living_world"
sys.path.insert(0, str(APP))
from bridge import Conversation, validate
from hybrid import HybridDialogue
from routines import BUDGET, DAY, FIRST_LEG, KANTO, REVIEW, SECOND_LEG, TTL, Relay, RoutineWorld
from world import WorldMemory

WATTS = Conversation("pc_resident", 25)
GUIDE = Conversation("sign_guide", None)
ROUTE = Conversation("route_scout", None)
CITY = Conversation("viridian_student", None)


def advance_to_next(world):
    assert world.next_due is not None
    return world.tick(world.next_due)


def source_report(memory):
    memory.apply(memory.context(WATTS), "ADJUST_RELATIONSHIP")
    assert memory.social.tick(memory.social.deadline)["status"] == "shared"


def regression(path, catalog):
    clock = 5 * DAY + 10 * 3600
    memory = WorldMemory(path, "demo", b"start")
    routine = memory.routines
    routine.tick(clock)
    assert routine.state(ROUTE.npc)[0] == "watch_the_route"
    assert routine.state(CITY.npc)[0] == "study_trail_habitats"
    assert not routine.enqueue("kanto", "pallet-sighting:25", 25, "pc_resident", clock)
    source_report(memory)
    assert not routine.enqueue("kanto", "pallet-sighting:25", 25, "oak", clock)
    routine.discovery_pending = True
    routine.tick(clock)
    assert routine.state(GUIDE.npc)[1] == "relay_sighting"
    with ThreadPoolExecutor(max_workers=1) as pool:
        router = HybridDialogue(memory, SimpleNamespace(catalog=catalog, style="unavailable",
                                                        species_names={"25": "Pikachu"}), pool)
        old = router.request(CITY)
        other = router.request(Conversation("daisy", 25))
        assert "reported" not in validate(old.future.result()[0].dialogue).decode()
        assert routine.tick(clock + FIRST_LEG - 1) == []
        event = advance_to_next(routine)[0]
        assert (event["area"], event["sender"], event["receiver"], event["source"]) == (
            "route_1", GUIDE.npc, ROUTE.npc, WATTS.npc)
        assert routine.state(ROUTE.npc) == ("record_report", "forward_sighting")
        assert not memory.knowledge(CITY.npc, None)
        event = advance_to_next(routine)[0]
        assert (event["area"], event["sender"], event["receiver"]) == ("viridian", ROUTE.npc, CITY.npc)
        assert memory.knowledge(CITY.npc, None)[0]["source"] == ROUTE.npc
        assert memory.knowledge(CITY.npc, None)[0]["verified"] == 0
        assert not memory.knowledge("daisy", None)
        current = router.request(CITY)
        assert current.key != old.key and current.cache == "miss"
        assert "Watts reported a Pikachu." in validate(current.future.result()[0].dialogue).decode()
        assert router.request(Conversation("daisy", 25)).future is other.future
        changes = advance_to_next(routine)
        assert changes[0]["status"] == "resolved"
        assert router.request(CITY).key != current.key
        assert not routine.enqueue("kanto", "pallet-sighting:25", 25, "pc_resident", routine.now)
        assert not routine.tick(clock)
        rows = memory.db.execute("""
            SELECT familiarity,trust,affinity,experiences FROM social_relationship
            WHERE save=? AND npc='viridian_student'
        """, (memory.save,)).fetchall()
        assert rows == [(1, 2, 1, 1)]
        memory.checkpoint(b"end")
    memory.close()
    memory = WorldMemory(path, "demo", b"end")
    assert memory.routines.now == clock + FIRST_LEG + SECOND_LEG + REVIEW
    assert memory.knowledge(CITY.npc, None)[0]["fact"] == "relay:viridian_student:25"
    assert memory.routines.next_due is None
    shown = Conversation(CITY.npc, 25)
    memory.apply(memory.context(shown), "COMMENT_ON_POKEMON")
    with ThreadPoolExecutor(max_workers=1) as pool:
        router = HybridDialogue(memory, SimpleNamespace(catalog=catalog, style="unavailable",
                                                        species_names={"25": "Pikachu"}), pool)
        assert "Watts reported a Pikachu." in validate(router.request(shown).future.result()[0].dialogue).decode()
    memory.close()
    memory = WorldMemory(path, "new-slot", b"end")
    assert not memory.knowledge(CITY.npc, None)
    memory.close()

    for kind, offset in (("after-hours", 23 * 3600), ("expiry", 2 * 3600)):
        memory = WorldMemory(path, kind, b"start")
        source_report(memory)
        routine = memory.routines
        day = 8 * DAY
        routine.tick(day + offset)
        if kind == "expiry":
            assert routine.tick(day + offset + TTL)[0]["status"] == "expired"
            assert not memory.knowledge(ROUTE.npc, None)
        else:
            advance_to_next(routine)
            assert advance_to_next(routine)[0]["status"] == "await_review"
            assert routine.state(CITY.npc)[0] == "rest"
            memory.checkpoint(b"pending")
            memory.close()
            memory = WorldMemory(path, kind, b"pending")
            routine = memory.routines
            assert routine.next_due == day + DAY + 9 * 3600
            assert advance_to_next(routine)[0]["status"] == "reviewing"
            assert advance_to_next(routine)[0]["status"] == "resolved"
        memory.close()
    print("PASS shifts, interruption, two hops, provenance, bounded relationship, expiry, rollback clock, cache and reload.")


def synthetic(path, population):
    seed = random.Random(70125 + population)
    routes = {
        str(i): Relay(*(replace(actor, npc=f"{actor.npc}_{i}") for actor in
                        (KANTO.guide, KANTO.scout, KANTO.researcher)))
        for i in range(population // 3)
    }
    extras = [replace(KANTO.scout, npc=f"extra_{i}") for i in range(population % 3)]
    memory = WorldMemory(path, "synthetic", b"run")
    engine = RoutineWorld(memory, routes, standalone=extras)
    assert len(engine.actors) == population
    batches = sorted((day * DAY + seed.randrange(24) * 3600, key, species)
                      for key in routes for day, species in ((0, 25), (3, 7)))
    starts = {}
    for moment, key, species in batches:
        starts.setdefault(moment, []).append((key, species))
    tick_times = []
    transitions = 0
    duplicates = 0
    from director import DUTY
    director = memory.director
    completed_plans = 0
    previous_plan = None
    tracemalloc.start()
    cpu = process_time()
    for now in range(0, 7 * DAY, 300):
        for key, species in starts.get(now, ()):
            guide = routes[key].guide
            fact = f"pallet-sighting:{species}:{key}"
            with memory.db:
                memory.db.execute("INSERT INTO social_event VALUES (?,?,?,?,?,?,?,?,?,0)",
                                  (memory.save, fact, WATTS.npc, guide.npc, guide.area,
                                   species, now, now, now))
                memory.db.execute("""
                    INSERT INTO npc_knowledge(save,npc,fact,origin,source,verified)
                    VALUES (?,?,?,'conversation',?,0)
                """, (memory.save, guide.npc, fact, WATTS.npc))
            assert engine.enqueue(key, fact, species, WATTS.npc, now)
            duplicates += int(engine.enqueue(key, fact, species, WATTS.npc, now))
        start = perf_counter()
        if previous_plan is not None:
            director.observe(previous_plan["due"], "pewter", False)
        director.observe(now, "pewter", False)
        if previous_plan is not None and director.state["active"] is None:
            completed_plans += 1
        if now % DAY == 43200:
            ready = director.decision()
            assert ready
            director.submit(ready, DUTY)
        previous_plan = director.state["active"]
        changes = engine.tick(now)
        tick_times.append((perf_counter() - start) * 1000)
        while changes:
            assert len(changes) <= BUDGET
            transitions += len(changes)
            start = perf_counter()
            changes = engine.tick(now)
            tick_times.append((perf_counter() - start) * 1000)
        if now % DAY == 43200:
            assert all(engine.state(npc) for npc in engine.actors)
    run_cpu = process_time() - cpu
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    assertions = memory.db.execute("SELECT stage,COUNT(*) FROM routine_event GROUP BY stage").fetchall()
    assert assertions == [("resolved", len(batches))], assertions
    assert duplicates == 0 and completed_plans == 7
    assert memory.db.execute("""
        SELECT COUNT(*) FROM npc_knowledge WHERE fact LIKE 'relay:%' AND verified=0
    """).fetchone()[0] == len(batches) * 2
    assert memory.db.execute("SELECT MAX(experiences) FROM social_relationship").fetchone()[0] == 2
    memory.close()
    reopened = WorldMemory(path, "synthetic", b"run")
    reloaded = RoutineWorld(reopened, routes, standalone=extras)
    assert reloaded.next_due is None
    assert all(reloaded.state(npc) for npc in reloaded.actors)
    reopened.close()
    ticks = sorted(tick_times)
    return dict(population=population, in_game_days=7, events=len(batches), transitions=transitions,
                cpu_seconds=round(run_cpu, 3), tick_p95_ms=round(ticks[int(len(ticks) * 0.95)], 4),
                tick_max_ms=round(max(ticks), 4), tracemalloc_kib=round(peak / 1024, 1),
                database_kib=path.stat().st_size // 1024, duplicates=duplicates, inference_calls=0,
                completed_director_plans=completed_plans)


if __name__ == "__main__":
    with TemporaryDirectory() as folder:
        root = Path(folder)
        catalog = root / "catalog.sqlite"
        subprocess.run([sys.executable, "-B", APP / "build-knowledge.py", catalog], check=True)
        regression(root / "regression.sqlite", catalog)
        for population in (10, 50, 100, 250):
            print(json.dumps(synthetic(root / f"population-{population}.sqlite", population)))
