#!/usr/bin/env python3
"""Run, inspect, export or replay an isolated Living World database."""

import argparse
from contextlib import closing
import json
from pathlib import Path

from simulation.engine import HOURS_PER_DAY, Simulation, encoded, replay
from simulation.inspector import inspect
from simulation.planner import OfflinePlanner
from simulation.region import CASES, region


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_subparsers(dest="mode", required=True)
    run = modes.add_parser("run")
    run.add_argument("database", type=Path)
    run.add_argument("--days", type=int, default=30)
    run.add_argument("--seed", type=int, default=16)
    run.add_argument("--case", choices=CASES, default="ordinary")
    run.add_argument("--runtime", type=Path)
    run.add_argument("--model", type=Path)
    run.add_argument("--style", choices=("qwen3", "gemma"), default="qwen3")
    run.add_argument("--decisions", type=int, default=8)
    run.add_argument("--all-npcs", action="store_true")
    inspector = modes.add_parser("inspect")
    inspector.add_argument("database", type=Path)
    inspector.add_argument("--actor")
    inspector.add_argument("--limit", type=int, default=50, choices=range(0, 1001), metavar="0..1000")
    record = modes.add_parser("trace")
    record.add_argument("database", type=Path)
    check = modes.add_parser("replay")
    check.add_argument("input", type=Path)
    check.add_argument("--trace", action="store_true", help="read a JSONL journal instead of a database")
    args = parser.parse_args()

    if args.mode == "run":
        if args.model and not args.runtime:
            parser.error("--model requires --runtime")
        planner = OfflinePlanner(args.runtime, args.model, style=args.style) if args.runtime else None
        with closing(Simulation(args.database, region(args.seed, args.case))) as simulation:
            state = simulation.state()
            actors = tuple(key for key, p in state["people"].items() if p["controller"] == "npc")
            if not args.all_npcs:
                actors = tuple(state["focus"])
            try:
                turns = simulation.advance(args.days * HOURS_PER_DAY, planner, actors=actors, limit=args.decisions)
            finally:
                if planner:
                    planner.close()
            state = simulation.state()
            print(encoded(dict(days=state["tick"] / HOURS_PER_DAY, npcs=len(state["people"]) - 1,
                               revisions=state["revision"], decisions=turns, events=len(state["events"]))))
    elif args.mode == "replay" and args.trace:
        with args.input.open(encoding="utf-8") as records:
            state = replay([json.loads(line) for line in records])
        print(encoded(dict(verified_revision=state["revision"], tick=state["tick"])))
    else:
        with closing(Simulation(args.input if args.mode == "replay" else args.database, read_only=True)) as simulation:
            if args.mode == "replay":
                print(encoded(dict(verified_revision=simulation.verify_replay())))
            elif args.mode == "inspect":
                print(json.dumps(inspect(simulation, args.actor, history_limit=args.limit), indent=2))
            else:
                for entry in simulation.history():
                    print(encoded(entry))


if __name__ == "__main__":
    main()
