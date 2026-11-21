"""Replay Pewter causal scenarios and benchmark the optional bundled worker."""
from collections import Counter
from dataclasses import replace
import json
import os
from pathlib import Path
import random
import statistics
import struct
import sys
from tempfile import TemporaryDirectory
from time import perf_counter

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "experiments/living_world"))
from director import COURT, DUTY, GYM, MAX_ABSENCE, TRAIN, TRAVEL, TRIP, Plan, Step, choose_brock
from inference import LocalModel
from world import WorldMemory


def verify_maps():
    def map_data(name):
        return json.loads((ROOT / "data/maps" / name / "map.json").read_text())
    city, gym = map_data("PewterCity"), map_data("PewterCity_Gym")
    assert city["warp_events"][2]["dest_map"] == "MAP_PEWTER_CITY_GYM"
    assert gym["warp_events"][1]["dest_map"] == "MAP_PEWTER_CITY"
    assert gym["warp_events"][1]["dest_warp_id"] == "2"
    assert city["warp_events"][0]["dest_map"] == "MAP_PEWTER_CITY_MUSEUM_1F"
    slot = city["object_events"][6]
    assert (slot["graphics_id"], slot["x"], slot["y"], slot["elevation"]) == ("OBJ_EVENT_GFX_BROCK", 19, 9, 3)
    layout = (ROOT / "data/layouts/PewterCity/map.bin").read_bytes()
    assert struct.unpack_from("<H", layout, 2 * (48 * 9 + 19))[0] >> 10 == 12
    assert not any(e["x"] == 19 and e["y"] == 9 for e in city["warp_events"] + city["coord_events"])
    assert gym["object_events"][0]["script"] == "PewterCity_Gym_EventScript_Brock"


def rejected(director, ticket, plan):
    before = json.dumps(director.state)
    try:
        director.submit(ticket, plan)
    except ValueError:
        assert json.dumps(director.state) == before
    else:
        raise AssertionError(plan)


def until_done(director):
    steps = 0
    while director.state["active"]:
        director.observe(director.state["active"]["due"], "pewter_gym", False)
        steps += 1
        assert steps <= 5
    assert director.location == GYM


def exercise(path, seeds, decisions):
    outcomes, causes = Counter(), Counter()
    ticks = []
    for seed in range(seeds):
        rng = random.Random(seed)
        hour = rng.choice((8, 11, 17))
        start = seed * 86400 + hour * 3600
        memory = WorldMemory(path, f"scenario-{seed}", b"initial")
        director = memory.director
        assert director.decision() is None
        director.observe(start, "pewter", True)
        assert director.decision() is None
        director.observe(start, "pewter", False)
        if seed % 13 == 0:
            director.challenger()
        ticket = director.decision()
        assert ticket
        causes[ticket.trigger] += 1
        rejected(director, ticket, Plan("fossil", (Step("TRAVEL_TO", "Mt. Moon"),)))
        rejected(director, ticket, Plan("badges", (Step("SET_FLAG", "BADGE01_GET"),)))
        rejected(director, ticket, replace(TRIP, steps=TRIP.steps[:-1]))
        plan = decisions.get((ticket.trigger, ticket.expected_challenger),
                             (DUTY if ticket.expected_challenger else {"gym_duty": DUTY, "practice": TRAIN, "research_request": TRIP}[ticket.trigger]))
        failure = "offline model failure" if seed % 11 == 0 else None
        if failure:
            plan = DUTY
        director.submit(ticket, plan, fallback=failure)
        rejected(director, ticket, plan)
        if plan == TRIP:
            assert director.location == TRAVEL
            first_clue = director.message("brock_attendant")
            assert "Brock told me" in first_clue and director.state["quest"] is None
            if seed % 4:
                director.message("brock_attendant", accepted=True)
            assert director.message("brock_contact") is None
            memory.checkpoint(b"travel")
            memory.close()
            memory = WorldMemory(path, f"scenario-{seed}", b"travel")
            director = memory.director
            assert director.location == TRAVEL
            if seed % 5 == 0:
                director.observe(start - 1, "pewter", False)
                outcome = "clock_recovery"
            elif seed % 5 == 1:
                director.observe(start + MAX_ABSENCE, "pewter_gym", False)
                outcome = "deadline_recovery"
            elif seed % 5 == 2:
                director.observe(start + 5, "pewter_gym", True)
                outcome = "story_recovery"
            else:
                director.observe(start + 12, "pewter", False)
                assert director.location == COURT
                if seed % 2:
                    director.message("brock_contact", accepted=True)
                until_done(director)
                assert director.state["research"]["status"] == "compared"
                assert director.state["familiarity"] == 1
                if director.state["appointment"]:
                    assert director.state["appointment"]["status"] == "ready_at_gym"
                outcome = "contacted" if director.state["quest"] and director.state["quest"]["status"] == "contacted" else "returned"
            assert director.location == GYM
            quest = director.state["quest"]
            if quest and quest["status"] == "returned":
                director.message("brock_return", accepted=True)
                assert quest["status"] == "completed_at_gym"
                assert quest["source"] == "firsthand_brock"
            old = WorldMemory(path, f"scenario-{seed}", b"initial")
            assert old.director.location == TRAVEL
            old.close()
        else:
            assert director.location == GYM
            until_done(director)
            outcome = "safe_fallback" if failure else plan.goal
        assert director.location == GYM and director.state["active"] is None
        later = perf_counter()
        director.observe(start + 79, "pewter", False)
        assert director.decision() is None
        ticks.append(1000 * (perf_counter() - later))
        outcomes[outcome] += 1
        memory.close()
    print(json.dumps(dict(seeds=seeds, outcomes=outcomes, causes=causes, replay_model_calls=0,
                          replay_tick_p95_ms=statistics.quantiles(ticks, n=20)[18],
                          database_bytes=path.stat().st_size)))


def model_benchmark(runtime):
    model = LocalModel(runtime, {}, style="qwen3", natural=True)
    observed = {}
    scenarios = [(8, False, DUTY), (11, False, TRIP), (17, False, TRAIN), (11, True, DUTY)]
    valid, count = 0, 0
    metrics_log = []
    try:
        for sample in range(3):
            for hour, waiting, expected in scenarios:
                memory = WorldMemory(":memory:", "fixture", bytes([sample]))
                director = memory.director
                second = sample * 86400 + hour * 3600
                director.observe(second, "pewter", False)
                if waiting:
                    director.challenger()
                ticket = director.decision()
                chosen, metrics = choose_brock(model, ticket)
                director.submit(ticket, chosen)
                valid += 1
                count += chosen == expected
                observed[ticket.trigger, waiting] = chosen
                metrics_log.append(metrics["decision_ms"])
                print(json.dumps(dict(trigger=ticket.trigger, waiting=waiting, proposed=chosen.goal,
                                      expected=expected.goal, metrics=metrics)))
                memory.close()
    finally:
        model.close()
    print(json.dumps(dict(valid=valid, context_matches=count, total=len(metrics_log),
                          median_ms=statistics.median(metrics_log), max_ms=max(metrics_log))))
    return observed


if __name__ == "__main__":
    verify_maps()
    runtime = os.environ.get("LIVING_WORLD_PHASE5_RUNTIME")
    decisions = model_benchmark(Path(runtime)) if runtime else {}
    with TemporaryDirectory() as temporary:
        exercise(Path(temporary) / "seeded.sqlite3", 120, decisions)
    print("PASS map graph, allowlist, one location, stale commitments, progression, lifecycle and save checkpoints")
