#!/usr/bin/env python3
"""Host checks for the six-tier campaign assignment and source regeneration."""
import importlib.util
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("profiles", ROOT / "tools/ai/assign_quantum_profiles.py")
PROFILES = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PROFILES)


class QuantumProfiles(unittest.TestCase):
    def test_trainer_ids_have_exactly_one_source_entry(self):
        entries = re.findall(r"^=== (TRAINER_\w+) ===$", PROFILES.SOURCE.read_text(), re.M)
        ids = set(re.findall(r"^#define (TRAINER_\w+)\s+\d+\s*$",
                             (ROOT / "include/constants/opponents.h").read_text(), re.M))
        self.assertEqual(len(entries), len(set(entries)))
        self.assertEqual(set(entries), ids)

    def test_generated_profiles_and_retirement_list_match_source(self):
        source = dict(re.findall(r"^=== (TRAINER_\w+) ===\n(.*?)(?=^=== |\Z)",
                                 PROFILES.SOURCE.read_text(), re.M | re.S))
        generated = dict(re.findall(
            r"^    \[DIFFICULTY_NORMAL\]\[(TRAINER_\w+)\] =\n(.*?)(?=^    \[DIFFICULTY_NORMAL\]|\Z)",
            (ROOT / "src/data/trainers.h").read_text(), re.M | re.S))
        retired = set(json.loads((ROOT / "docs/rom-retired-trainers.json").read_text()))
        self.assertEqual(set(source) - set(generated), retired)
        self.assertFalse(set(generated) - set(source))
        self.assertFalse(retired & set(generated))
        for trainer, block in generated.items():
            if trainer == "TRAINER_NONE":
                continue
            tier = re.search(r"^AI: Quantum (.*)$", source[trainer], re.M).group(1)
            expected = "AI_FLAG_QUANTUM_" + tier.upper().replace(" ", "_")
            with self.subTest(trainer=trainer):
                self.assertEqual(re.findall(r"\.aiFlags\s*=\s*([^,]+)", block), [expected])

    def test_vs_seeker_rematches_keep_their_base_tier(self):
        source = dict(re.findall(r"^=== (TRAINER_\w+) ===\n(.*?)(?=^=== |\Z)",
                                 PROFILES.SOURCE.read_text(), re.M | re.S))
        table = (ROOT / "src/vs_seeker.c").read_text().split(
            "static const struct RematchData sRematches[] = {")[1].split("\n};")[0]
        rows = re.findall(r"\{\s*\{([^}]+)\}", table)
        self.assertTrue(rows)
        for row in rows:
            trainers = re.findall(r"\bTRAINER_\w+", row)
            with self.subTest(trainers=trainers):
                self.assertTrue(trainers)
                tiers = {re.search(r"^AI: (.*)$", source[t], re.M).group(1) for t in trainers}
                self.assertEqual(len(tiers), 1)

    def test_source_is_current_and_idempotent(self):
        source = PROFILES.SOURCE.read_text()
        assigned, counts = PROFILES.assign(source)
        self.assertEqual(source, assigned)
        self.assertEqual(assigned, PROFILES.assign(assigned)[0])
        self.assertEqual(set(counts), {"Regular", "Gym Trainer", "Gym Leader", "Rival", "Elite Four", "Champion"})

    def test_gym_membership_uses_location_and_eirik_is_a_leader(self):
        gyms = PROFILES.gym_trainers()
        for trainer, trainer_class, expected in [
            ("TRAINER_CAMPER_LIAM", "Camper", "Gym Trainer"),
            ("TRAINER_HAVORA_DOCK_CREW", "Sailor", "Gym Trainer"),
            ("TRAINER_HAVORA_CAPTAIN", "Sailor", "Gym Leader"),
            ("TRAINER_BOSS_GIOVANNI", "Boss", "Gym Leader"),
            ("TRAINER_BOSS_GIOVANNI_2", "Boss", "Gym Leader"),
            ("TRAINER_BLACK_BELT_KOICHI", "Black Belt", "Gym Leader"),
            ("TRAINER_BLACK_BELT_AARON", "Black Belt", "Gym Trainer"),
            ("TRAINER_BLACK_BELT_HIDEKI", "Black Belt", "Gym Trainer"),
            ("TRAINER_BLACK_BELT_HITOSHI", "Black Belt", "Gym Trainer"),
            ("TRAINER_BLACK_BELT_MIKE", "Black Belt", "Gym Trainer"),
            ("TRAINER_LEADER_GIOVANNI", "Leader", "Gym Leader"),
            ("TRAINER_SAILOR_TEST_ROUTE", "Sailor", "Regular"),
            ("TRAINER_RIVAL_OAKS_LAB_SQUIRTLE", "Rival Early", "Rival"),
            ("TRAINER_RIVAL_ROUTE22_LATE_SQUIRTLE", "Rival Late", "Rival"),
            ("TRAINER_ELITE_FOUR_LORELEI_2", "Elite Four", "Elite Four"),
            ("TRAINER_CHAMPION_REMATCH_SQUIRTLE", "Champion", "Champion"),
        ]:
            with self.subTest(trainer=trainer):
                self.assertEqual(PROFILES.tier_for(trainer, trainer_class, gyms), expected)

    def test_every_party_entry_has_one_profile_except_empty_placeholder(self):
        for trainer, block in re.findall(r"^=== (TRAINER_\w+) ===\n(.*?)(?=^=== |\Z)", PROFILES.SOURCE.read_text(), re.M | re.S):
            profiles = re.findall(r"^AI: (.+)$", block, re.M)
            with self.subTest(trainer=trainer):
                if trainer == "TRAINER_NONE":
                    self.assertFalse(profiles)
                else:
                    self.assertEqual(len(profiles), 1)
                    self.assertRegex(profiles[0], r"^Quantum (Regular|Gym Trainer|Gym Leader|Rival|Elite Four|Champion)$")


if __name__ == "__main__":
    unittest.main()
