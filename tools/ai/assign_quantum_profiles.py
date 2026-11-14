#!/usr/bin/env python3
"""Assign Quantum AI profiles in the trainer source, never the generated header.

Gym membership comes from gym scripts, not trainer names/classes (a Sailor can
be either a route trainer or gym trainer). Eirik uses the Sailor class too.
Run with --check in validation; regenerate trainers.h through make afterwards.
"""
import argparse
import collections
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "src/data/trainers.party"

# Story bosses and the former Fighting Gym do not use Leader trainer classes.
LEADER_EQUIVALENTS = {
    "TRAINER_HAVORA_CAPTAIN",
    "TRAINER_BOSS_GIOVANNI",
    "TRAINER_BOSS_GIOVANNI_2",
    "TRAINER_BLACK_BELT_KOICHI",
}


def gym_trainers():
    members = set()
    for path in (ROOT / "data/maps").glob("*Gym*/scripts.inc"):
        members.update(re.findall(r"\bTRAINER_[A-Z0-9_]+", path.read_text()))
    members.update(re.findall(r"\bTRAINER_[A-Z0-9_]+",
                             (ROOT / "data/maps/SaffronCity_Dojo/scripts.inc").read_text()))
    return members


def tier_for(trainer, trainer_class, gyms):
    if trainer.startswith("TRAINER_CHAMPION_") or trainer_class in {"Champion", "RS Champion"}:
        return "Champion"
    if trainer.startswith("TRAINER_ELITE_FOUR_") or trainer_class in {"Elite Four", "RS Elite Four"}:
        return "Elite Four"
    if trainer.startswith("TRAINER_RIVAL_") or trainer_class in {"Rival Early", "Rival Late"}:
        return "Rival"
    if trainer.startswith("TRAINER_LEADER_") or trainer in LEADER_EQUIVALENTS or trainer_class in {"Leader", "RS Leader"}:
        return "Gym Leader"
    if trainer in gyms:
        return "Gym Trainer"
    return "Regular"


def assign(source):
    gyms = gym_trainers()
    counts = collections.Counter()
    def update(match):
        block = match.group(0)
        trainer = match.group(1)
        trainer_class = re.search(r"^Class: (.+)$", block, re.M).group(1)
        if trainer == "TRAINER_NONE":
            return block
        tier = tier_for(trainer, trainer_class, gyms)
        counts[tier] += 1
        line = "AI: Quantum " + tier
        if re.search(r"^AI:.*$", block, re.M):
            return re.sub(r"^AI:.*$", line, block, flags=re.M)
        return re.sub(r"^(Double Battle:.*)$", r"\1\n" + line, block, count=1, flags=re.M)
    result = re.sub(r"^=== (TRAINER_\w+) ===\n.*?(?=^=== |\Z)", update, source, flags=re.M | re.S)
    return result, counts


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    original = SOURCE.read_text()
    updated, counts = assign(original)
    for tier, count in counts.items():
        print(f"{tier}: {count}")
    if args.check:
        if updated != original:
            raise SystemExit("Trainer AI profiles are stale; run this script without --check")
    else:
        SOURCE.write_text(updated)
