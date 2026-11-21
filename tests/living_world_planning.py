"""Composed choices, transactional validation and actual Qwen output."""
from collections import Counter
import json
import random
from statistics import quantiles
from time import perf_counter
import tracemalloc
import os
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "experiments/living_world"))
from director import choose_brock
from inference import LocalModel
from planning import Proposal, choose_plan
from society import PERSONAS, Step
from world import WorldMemory


def run(model):
    world = WorldMemory(":memory:", "planning", b"start")
    society = world.society
    society.tick(39600, "pewter")
    society.tick(39601, "viridian")
    ticket = society.decision("researcher")
    available = society.primitives(ticket)
    steps = (Step("INVESTIGATE", "cast"), Step("REST", "museum"),
             Step("REQUEST_ASSISTANCE", "brock"))
    assert steps not in ticket.choices
    for invalid in (steps[::-1], (*steps, steps[0]), (Step("TRAVEL_TO", "mt_moon"),)):
        before = json.dumps(society.state)
        try:
            society.submit(ticket, Proposal("verify_observation", invalid, available))
        except ValueError:
            assert json.dumps(society.state) == before
        else:
            raise AssertionError("Invalid proposal mutated the world")
    society.submit(ticket, Proposal("verify_observation", steps, available))
    assert society.state["agents"]["researcher"]["active"]["goal"] == "verify_observation"
    start = society.now
    for offset in (32, 48, 52):
        society.tick(start + offset, "viridian")
    assert society.notice_for_brock()
    print("PASS composed non-template plan, offscreen execution, and atomic rejection")
    if model:
        director = world.director
        director.notice = society.notice_for_brock()
        director.offscreen = director.notice_required = True
        director.observe(society.now, "viridian", False)
        protected = director.decision()
        selected, metrics = choose_brock(model, protected)
        director.submit(protected, selected)
        print(json.dumps(dict(actor="brock", goal=selected.goal, protected=True, **metrics)))
        for actor in ("researcher", "trainer", "assistant", "attendant"):
            if actor == "researcher":
                society.regional_demo = True
                society.tick(86400+39600, "viridian")
            ticket = society.decision(actor)
            proposal, metrics = choose_plan(model, ticket, society.primitives(ticket), PERSONAS[actor], society.planning_snapshot())
            try:
                society.submit(ticket, proposal)
                valid = True
            except ValueError as error:
                society.submit(ticket, ticket.choices[0], fallback=str(error))
                valid = False
            print(json.dumps(dict(actor=actor, goal=proposal.goal,
                                  steps=[(s.action,s.target) for s in proposal.steps], valid=valid, **metrics)))
    world.close()


def replay():
    timings, outcomes = [], Counter()
    tracemalloc.start()
    for seed in range(120):
        start = 39600 + random.Random(seed).randrange(120)
        memory = WorldMemory(":memory:", "replay", b"start")
        society = memory.society
        society.tick(start, "pewter")
        society.tick(start, "viridian")
        ticket = society.decision("researcher")
        journey = (Step("TRAVEL_TO", "route_2"), Step("INVESTIGATE", "tracks"),
                   Step("RETURN_TO_DUTY", "museum"))
        # A policy replay with a shorter local plan when the encounter
        # window is unsuitable for a regional observation.
        feasible = start < 39680
        steps = journey if feasible else (Step("INVESTIGATE", "cast"), Step("WORK", "museum"))
        first = perf_counter()
        society.submit(ticket, Proposal("verify_observation", steps, society.primitives(ticket)))
        timings.append((perf_counter()-first)*1000)
        memory.checkpoint(b"after-planning")
        society = memory.society
        if feasible and seed % 8 == 0:
            society.tick(start+120, "viridian")
            assert society.state["agents"]["researcher"]["location"] == "museum"
            society.tick(start+130, "viridian")
            assert society.decision("researcher").cause == "recover_plan"
            outcomes["replan_after_interruption"] += 1
        else:
            times = (28,60,88) if feasible else (32,56)
            for offset in times:
                first = perf_counter()
                society.tick(start+offset, "route_2")
                timings.append((perf_counter()-first)*1000)
            record = society.state["agents"]["researcher"]["facts"]
            assert "tracks" in record if feasible else "cast" in record
            assert society.state["agents"]["researcher"]["location"] == "museum"
            outcomes["regional" if feasible else "local"] += 1
        assert len(society.state["log"]) <= 48
        memory.close()
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    print(json.dumps(dict(scenarios=120, outcomes=outcomes, p95_ms=quantiles(timings,n=20)[18],
                          peak_python_bytes=peak, model_calls=0)))


if __name__ == "__main__":
    runtime = os.environ.get("LIVING_WORLD_PHASE5_RUNTIME")
    model = LocalModel(Path(runtime), {}, style="qwen3", natural=True) if runtime else None
    try:
        run(model)
        replay()
    finally:
        if model:
            model.close()
