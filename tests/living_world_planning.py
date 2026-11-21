"""Composed choices, transactional validation and actual Qwen output."""
import json
import os
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "experiments/living_world"))
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
        for actor in ("trainer", "assistant", "attendant"):
            ticket = society.decision(actor)
            proposal, metrics = choose_plan(model, ticket, society.primitives(ticket), PERSONAS[actor])
            try:
                society.submit(ticket, proposal)
                valid = True
            except ValueError as error:
                society.submit(ticket, ticket.choices[0], fallback=str(error))
                valid = False
            print(json.dumps(dict(actor=actor, goal=proposal.goal,
                                  steps=[(s.action,s.target) for s in proposal.steps], valid=valid, **metrics)))
    world.close()


if __name__ == "__main__":
    runtime = os.environ.get("LIVING_WORLD_PHASE5_RUNTIME")
    model = LocalModel(Path(runtime), {}, style="qwen3", natural=True) if runtime else None
    try:
        run(model)
    finally:
        if model:
            model.close()
