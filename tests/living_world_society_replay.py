"""Exercise seeded Pewter outcomes with a bounded replay policy and real Qwen cases."""
from collections import Counter
import json
import os
from pathlib import Path
import random
import statistics
import sys
from tempfile import TemporaryDirectory
from time import perf_counter, process_time
import tracemalloc

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "experiments/living_world"))
from director import DUTY, TRIP, choose_brock
from dynamic_quests import project_brock
from inference import LocalModel
from society import choose_agent
from world import WorldMemory


def sequence(ticket, action, target=None):
    return next(plan for plan in ticket.choices
                if any(step.action == action and (target is None or step.target == target) for step in plan))


def model_cases(model):
    runs = []
    for closing in (False, True):
        memory = WorldMemory(":memory:", "requests", b"run")
        world = memory.society
        start = 17 * 3600 - 32 if closing else 11 * 3600
        world.tick(start, "pewter")
        ticket = world.decision("researcher")
        world.submit(ticket, sequence(ticket, "REQUEST_ASSISTANCE", "assistant"))
        world.tick(start + 32, "viridian")
        world.tick(start + 36, "viridian")
        ticket = world.decision("assistant")
        assert ticket and ticket.cause.startswith("pewter:")
        plan, metrics = choose_agent(model, ticket)
        world.submit(ticket, plan)
        while active := world.state["agents"]["assistant"]["active"]:
            world.tick(active["due"], "viridian")
        request = world.state["requests"][ticket.cause]
        assert request["status"] in ("resolved", "declined")
        row = dict(closing=closing, first=plan[0].action, status=request["status"], **metrics)
        runs.append(row)
        print(json.dumps(row))
        memory.close()
    return runs


def replay(path):
    counters = Counter()
    ticks = []
    memory = None
    tracemalloc.start()
    cpu = process_time()
    for seed in range(120):
        rng = random.Random(seed)
        # Exhibition timing, earlier collaborations, commitments and actual player actions.
        hour = rng.choice((10, 11, 16))
        start = (hour + 1) * 3600 - 32 if hour == 16 else hour * 3600
        memory = WorldMemory(path, f"seed-{seed}", b"old")
        world = memory.society
        director = memory.director
        director.offscreen = director.notice_required = True
        director.society_demo = True
        world.tick(start, "pewter")
        if seed % 6 == 0:
            # Seed a prior validated working relationship from a previous shift.
            world.state["agents"]["assistant"]["bonds"]["researcher"] = 2
        if seed % 9 == 0:
            director.observe(start, "pewter_gym", False)
            director.challenger()
        for offset in range(0, 250, 4):
            second = start + offset
            frame_start = perf_counter()
            world.tick(second, "route_2")
            director.notice = world.notice_for_brock()
            director.observe(second, "route_2", False)
            world.reconcile_brock(director.state.get("last_notice_result"))
            # A copied data packet can only execute against the current battery checkpoint.
            if offset == 72:
                memory.checkpoint(b"current")
                memory.close()
                memory = WorldMemory(path, f"seed-{seed}", b"current")
                world, director = memory.society, memory.director
                director.offscreen = director.notice_required = director.society_demo = True
            request = director.decision()
            if request and request.notice:
                selected = next((p for p in request.plans if p == TRIP), DUTY)
                director.submit(request, selected)
                world.respond_brock(request.notice, selected == TRIP)
                counters["brock_outings" if selected == TRIP else "gym_commitments"] += 1
            elif ticket := world.decision():
                if ticket.cause.startswith("pewter:"):
                    closing = "close the desk" in ticket.context
                    plan = sequence(ticket, "DECLINE_REQUEST" if closing else "ACCEPT_REQUEST")
                elif ticket.actor == "researcher" and ticket.cause == "open_shift":
                    plan = sequence(ticket, "REQUEST_ASSISTANCE", "assistant")
                elif ticket.actor == "researcher":
                    plan = next((p for p in ticket.choices if p[0].target == "brock"), ticket.choices[0])
                elif ticket.actor == "trainer" and ticket.cause == "open_shift":
                    plan = sequence(ticket, "TRAVEL_TO")
                else:
                    plan = ticket.choices[0]
                world.submit(ticket, plan, fallback=None)
            if seed % 3 == 0 and director.location == "in_transit":
                director.message("brock_attendant", accepted=True)
            if seed % 3 == 0 and director.location == "museum_forecourt" and seed % 2:
                director.message("brock_contact", accepted=True)
            ticks.append((perf_counter() - frame_start) * 1000)
        assert director.location == "gym", director.state
        quests = director.state["quest"]
        if quests and quests["status"] == "returned":
            director.message("brock_return", accepted=True)
        if quests:
            counters[quests["status"]] += 1
            assert project_brock(director)[8] == 3
        for item in world.state["requests"].values():
            counters[item["status"]] += 1
        for actor in world.state["agents"].values():
            assert len(actor["memory"]) <= 8 and actor["location"] != "in_transit"
        assert len(world.state["requests"]) <= 12 and len(world.state["log"]) <= 48
        memory.close()
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    assert counters["resolved"] and counters["declined"] and counters["brock_outings"] and counters["gym_commitments"]
    print(json.dumps(dict(runs=120, outcomes=counters, authorized_gym_recovery=120,
                          p95_ms=statistics.quantiles(ticks, n=20)[18], peak_python_bytes=peak,
                          cpu_seconds=process_time()-cpu, db_bytes=path.stat().st_size, model_calls=0)))


def long_run(path):
    memory = WorldMemory(path, "long", b"long")
    world = memory.society
    start = perf_counter()
    for day in range(100):
        begin = day * 86400 + 11 * 3600
        for offset in range(0, 300, 4):
            world.tick(begin + offset, "pewter" if not day else "viridian")
            if ticket := world.decision():
                if ticket.cause.startswith("pewter:"):
                    selected = sequence(ticket, "ACCEPT_REQUEST")
                elif ticket.actor == "researcher" and ticket.cause == "open_shift":
                    selected = sequence(ticket, "REQUEST_ASSISTANCE", "assistant")
                else:
                    selected = ticket.choices[0]
                world.submit(ticket, selected)
        assert len(world.state["log"]) <= 48 and len(world.state["requests"]) <= 12
    count = world.state["agents"]["researcher"]["facts"]["cast"]["checks"]
    assert count == 100
    memory.close()
    checkpoint = WorldMemory(path, "long", b"long")
    assert checkpoint.society.state["agents"]["researcher"]["facts"]["cast"]["checks"] == count
    checkpoint.close()
    print(json.dumps(dict(days=100, checks=count, seconds=perf_counter()-start,
                          db_bytes=path.stat().st_size, model_calls=0)))


if __name__ == "__main__":
    runtime = os.environ.get("LIVING_WORLD_PHASE5_RUNTIME")
    if runtime:
        model = LocalModel(Path(runtime), {}, style="qwen3", natural=True)
        try:
            model_cases(model)
        finally:
            model.close()
    with TemporaryDirectory() as temp:
        replay(Path(temp) / "replay.sqlite")
        long_run(Path(temp) / "long.sqlite")
