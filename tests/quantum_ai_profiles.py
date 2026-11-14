#!/usr/bin/env python3
"""Host checks for the six-tier campaign assignment and source regeneration."""
import importlib.util
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("profiles", ROOT / "tools/ai/assign_quantum_profiles.py")
PROFILES = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PROFILES)


class QuantumProfiles(unittest.TestCase):
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
