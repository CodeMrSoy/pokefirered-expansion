#!/usr/bin/env python3
"""Measure offline planners against the same starting worlds and concrete outcomes."""

import argparse
from contextlib import closing
from hashlib import file_digest
import json
from pathlib import Path
import platform
from tempfile import TemporaryDirectory

from simulation.engine import Simulation, encoded
from simulation.planner import OfflinePlanner
from simulation.region import CASES, region
from world_rules import MARTS


def summarize(initial, final, history):
    lead, peer = initial["focus"]
    before, after = initial["people"][lead], final["people"][lead]
    commands = [e for e in history[1:] if e["command"]["kind"] == "decision"]
    routine = [e for entry in history[1:] if entry["command"]["kind"] == "tick"
               and entry["result"]["accepted"] for e in entry["result"]["effect"]]
    actions = [e for e in routine if "action" in e]
    goals = [e for e in routine if e.get("routine") == "goal_met"]
    cases = {
        "ordinary": bool(goals),
        "shortage": (final["firms"][MARTS["PewterCity"]]["goods"]["POTION"] > 1
                     or after["goods"].get("POTION", 0) > before["goods"].get("POTION", 0)),
        "employment": after["employer"] is not None and after["employer"] != before["employer"],
        "cooperation": any(r["from"] == lead and r["status"] == "teach"
                           for r in final["requests"].values()) and "retail" in after["skills"],
        "relocation": after["home"] is not None and after["home"] != before["home"],
        "event": any(e.get("action", {}).get("verb") == "travel" and e.get("actor") == lead
                     and e["action"]["to"] == "CeruleanCity" and "effect" in e for e in actions),
    }
    flags = {e["command"]["actor"] for e in commands
             if e["command"]["proposal"] is not None and e["result"]["accepted"]}
    return dict(
        case=initial["case"], goal_condition_met=cases[initial["case"]],
        acting_npcs=sorted({e["actor"] for e in actions if "effect" in e}),
        observed_goals_completed=len(goals), active_model_actors=sorted(flags),
        accepted_plans=sum(e["result"]["accepted"] and
                           bool(e["command"].get("proposal", {}) and e["command"]["proposal"]["steps"])
                           for e in commands),
        invalid_plans=sum(not e["result"]["accepted"] for e in commands),
        worker_errors=sum(e["command"]["source"] == "unavailable" for e in commands),
        action_ticks=[e["tick"] for e in history[1:] if e["command"]["kind"] == "tick"
                      and e["result"]["accepted"] and any("action" in r and "effect" in r
                                                         for r in e["result"]["effect"])],
        lead=dict(id=lead, home=after["home"], employer=after["employer"], money=after["money"],
                  skills=after["skills"], location=after["location"]),
        peer=dict(id=peer, goal=final["people"][peer]["goal"]),
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("runtime", type=Path)
    parser.add_argument("weights", type=Path)
    parser.add_argument("style", choices=("qwen3", "gemma"))
    parser.add_argument("--case", action="append", choices=CASES)
    parser.add_argument("--decisions", type=int, default=8)
    parser.add_argument("--trace", type=Path, help="save per-case replayable traces in this directory")
    args = parser.parse_args()
    if args.trace:
        args.trace.mkdir(parents=True, exist_ok=True)
    with args.weights.open("rb") as weights:
        print(encoded(dict(platform=platform.platform(), weights=args.weights.name,
                           sha256=file_digest(weights, "sha256").hexdigest())), flush=True)
    with TemporaryDirectory() as workspace:
        for case in args.case or CASES:
            initial = region(case=case)
            planner = OfflinePlanner(args.runtime, args.weights, style=args.style, measure_memory=True)
            path = Path(workspace) / (case + ".sqlite3")
            try:
                with closing(Simulation(path, initial)) as sim:
                    if case == "event":
                        # Planners receive the world after reopening/occupancy
                        # changes only when they can perceive them.
                        sim.command(dict(kind="incident", source="director", event="route_closure",
                                         target="ViridianCity|CeruleanCity"))
                    sim.advance(36, planner, actors=tuple(initial["focus"]), limit=args.decisions)
                with closing(Simulation(path)) as sim:
                    sim.advance(36, planner, actors=tuple(initial["focus"]), limit=args.decisions // 2)
                    final, history = sim.snapshot()
                    assert sim.verify_replay() == final["revision"]
            finally:
                planner.close()
            if args.trace:
                (args.trace / (case + ".jsonl")).write_text(
                    "".join(encoded(entry) + "\n" for entry in history), encoding="utf-8")
            for entry in history[1:]:
                command = entry["command"]
                if command["kind"] == "decision":
                    print(encoded(dict(case=case, tick=entry["tick"], actor=command["actor"],
                                       evidence=command["evidence"], proposal=command["proposal"],
                                       result=entry["result"])), flush=True)
            print(encoded(summarize(initial, final, history)), flush=True)


if __name__ == "__main__":
    main()
