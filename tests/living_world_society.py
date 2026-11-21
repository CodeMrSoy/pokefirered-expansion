"""Pewter agent scheduling and save checkpoints, with optional real model."""
import json
import os
from pathlib import Path
import sys
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "experiments/living_world"))
from director import choose_brock
from inference import LocalModel
from society import Step, choose_agent
from world import WorldMemory

def test(path, model=None):
    memory = WorldMemory(path, "pewter", b"first")
    second = 11 * 3600
    memory.director.observe(second, "pewter", False)
    brock = memory.director.decision()
    assert brock and brock.report
    if model:
        plan, metrics = choose_brock(model, brock)
        memory.director.submit(brock, plan)
        print(json.dumps({"actor": "brock", "goal": plan.goal, **metrics}))
    society = memory.society
    society.tick(second, "pewter")
    society.tick(second + 3, "viridian")
    ticket = society.decision()
    assert ticket.actor == "researcher"
    try:
        society.submit(ticket, (Step("TRAVEL_TO", "mt_moon"),))
    except ValueError:
        pass
    else:
        raise AssertionError("Invalid action accepted")
    plan, metrics = choose_agent(model, ticket) if model else (ticket.choices[1], {})
    society.submit(ticket, plan)
    print(json.dumps({"actor": ticket.actor, "actions": [step.action for step in plan], **metrics}))
    memory.checkpoint(b"second")
    try:
        memory.society.submit(ticket, plan)
    except ValueError:
        pass
    else:
        raise AssertionError("Stale checkpoint accepted")
    memory.close()
    memory = WorldMemory(path, "pewter", b"second")
    society = memory.society
    assert society.state["agents"]["researcher"]["active"]
    society.tick(second + 50, "route_1")
    assert society.state["agents"]["researcher"]["memory"][-1]["outcome"] == "completed"
    if plan[0].action == "INVESTIGATE":
        assert society.state["agents"]["researcher"]["facts"]["cast"]["kind"] == "firsthand"
    memory.close()

def negotiate(path, model=None):
    memory = WorldMemory(path, "negotiation", b"test")
    society = memory.society
    stamp = 11 * 3600
    society.tick(stamp, "pewter")
    society.tick(stamp + 1, "route_1")

    def act(actor, intent=None):
        ticket = society.decision(actor)
        assert ticket, actor
        if model:
            plan, metrics = choose_agent(model, ticket)
            print(json.dumps(dict(actor=actor, trigger=ticket.cause, plan=[s.action for s in plan], **metrics)))
        else:
            plan = next((p for p in ticket.choices if intent is None or
                         any(s.action == intent for s in p)), None)
        assert plan
        society.submit(ticket, plan)
        while active := society.state["agents"][actor]["active"]:
            society.tick(active["due"], "route_1")
        return plan

    researched = act("researcher", "REQUEST_ASSISTANCE")
    event, request = society.pending("assistant")
    did_work = any(s.action == "INVESTIGATE" for s in researched)
    if did_work and not event:
        act("researcher", "REQUEST_ASSISTANCE")
    if event:
        assert request["origin"] == "researcher"
        assert society.state["agents"]["trainer"]["facts"] == {}
        shared = act("assistant", "ACCEPT_REQUEST")
        if shared[0].action == "ACCEPT_REQUEST":
            result = society.state["agents"]["researcher"]["facts"]["colleague_cast"]
            assert result["kind"] == "reported" and result["source"] == "assistant"
            assert society.state["agents"]["assistant"]["bonds"]["researcher"] == 1
        else:
            assert request["status"] == "declined"
    if did_work:
        # A distinct decision for Brock depends on a legitimate notice.
        ticket = society.decision("researcher")
        if ticket:
            act("researcher", "REQUEST_ASSISTANCE")
        notice = society.notice_for_brock()
        if notice:
            assert society.state["requests"][notice]["origin"] == "researcher"
            society.respond_brock(notice, False)
            assert society.notice_for_brock() is None
    if society.decision("assistant"):
        act("assistant")
    act("trainer")
    act("attendant")
    assert len(society.state["log"]) <= 48
    memory.close()


if __name__ == "__main__":
    runtime = os.environ.get("LIVING_WORLD_PHASE5_RUNTIME")
    model = LocalModel(Path(runtime), {}, style="qwen3", natural=True) if runtime else None
    try:
        with TemporaryDirectory() as directory:
            test(Path(directory) / "pewter.sqlite", model)
            negotiate(Path(directory) / "negotiation.sqlite", model)
    finally:
        if model:
            model.close()
    print("PASS independent offscreen decision, action rejection and checkpoint reload")
