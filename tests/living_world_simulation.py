"""Headless simulation invariants. Model behavior is measured independently."""

from contextlib import closing
from copy import deepcopy
import json
from pathlib import Path
import sqlite3
import sys
from tempfile import TemporaryDirectory
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "experiments/living_world"))

from simulation.actions import Rejected, validate
from simulation.adapter import native_progression_policy, project
from simulation.engine import Simulation, digest, observation, replay
from simulation.inspector import inspect
from simulation.region import CASES, TOWNS, region
from world_rules import MARTS, team_ceiling

PEWTER = MARTS["PewterCity"]
OPTIONAL = "ViridianCity|CeruleanCity"


class SimulationTests(unittest.TestCase):
    def setUp(self):
        self.initial = region(case="cooperation")
        self.sim = Simulation(":memory:", self.initial)
        self.addCleanup(self.sim.close)
        self.actor, self.peer = self.initial["focus"]

    def action(self, actor, verb, source="npc", **fields):
        return self.sim.command(dict(kind="action", source=source, actor=actor,
                                     action=dict(verb=verb, **fields)))

    def incident(self, event, target):
        return self.sim.command(dict(kind="incident", source="director", event=event, target=target))

    def decision(self, actor, goal, steps, obs=None):
        obs = observation(self.sim.state(), actor) if obs is None else obs
        return self.sim.command(dict(kind="decision", source="model", actor=actor,
                                     observation=obs, observed_revision=obs["revision"],
                                     proposal=dict(ambition="An invariant test", goal=goal, steps=steps)))

    def test_all_region_fixtures(self):
        for case in CASES:
            with self.subTest(case=case), closing(Simulation(":memory:", region(case=case))) as sim:
                self.assertEqual(len(sim.state()["people"]), 25)
                self.assertEqual(tuple(sorted(sim.state()["requirements"])), tuple(sorted(TOWNS)))
                sim.advance(25)
                self.assertEqual(sim.verify_replay(), 25)

    def test_failed_purchase_keeps_assets_even_after_debit_attempt(self):
        self.assertTrue(self.incident("shortage", PEWTER)["accepted"])
        before = self.sim.state()
        result = self.action("player", "trade", source="player", firm=PEWTER,
                             item="POTION", count=1, side="buy")
        self.assertEqual(result, dict(accepted=False, reason="insufficient_tradeable_stock"))
        after = self.sim.state()
        self.assertEqual(before["people"], after["people"])
        self.assertEqual(before["firms"], after["firms"])
        self.assertEqual(self.sim.verify_replay(), 2)

    def test_actor_owned_resources_and_currency(self):
        p = self.sim.state()["people"]["player"]
        self.assertTrue(self.action("player", "trade", source="player", firm=PEWTER,
                                    item="POTION", count=1, side="buy")["accepted"])
        self.assertTrue(self.action("player", "give", source="player", peer=self.actor,
                                    item="POTION", count=1)["accepted"])
        after = self.sim.state()
        self.assertEqual(after["people"]["player"]["money"], p["money"] - 5)
        self.assertEqual(after["people"][self.actor]["goods"]["POTION"], 1)
        self.assertEqual(self.action("player", "work")["reason"], "unauthorized")
        self.assertEqual(self.action(self.actor, "train", pokemon="PewterCity:partner")["reason"],
                         "pokemon_not_owned")
        self.assertEqual(self.action(self.actor, "trade", firm=PEWTER, item="POTION",
                                     count=True, side="buy")["reason"], "invalid_action_argument")

    def test_stale_batch_and_rollback(self):
        goal = dict(kind="skill", skill="retail")
        steps = [dict(verb="request", peer=self.peer, skill="retail")]
        obs = observation(self.sim.state(), self.actor)
        self.sim.advance(1)
        self.assertEqual(self.decision(self.actor, goal, steps, obs)["reason"], "stale_observation")
        result = self.decision(self.actor, goal, steps * 2)
        self.assertEqual(result["reason"], "already_requested")
        self.assertEqual(self.sim.state()["requests"], {})

    def test_concurrent_proposals_are_revalidated_during_execution(self):
        # Seed equivalent skills to verify the last slot cannot be double-filled.
        start = region()
        a, b = start["focus"]
        start["people"][b]["skills"] = {"retail": 1}
        start["firms"][PEWTER]["jobs"] = 1 + sum(p["employer"] == PEWTER for p in start["people"].values())
        with closing(Simulation(":memory:", start)) as sim:
            for actor in (a, b):
                obs = observation(sim.state(), actor)
                result = sim.command(dict(kind="decision", source="model", actor=actor,
                                          observation=obs, observed_revision=obs["revision"],
                                          proposal=dict(ambition="A spare job", goal=dict(kind="employment", firm=PEWTER),
                                                        steps=[dict(verb="employment", firm=PEWTER)])))
                self.assertTrue(result["accepted"])
            sim.advance(1)
            effects = sim.history()[-1]["result"]["effect"]
            self.assertEqual(sum("effect" in e for e in effects), 1)
            self.assertEqual(next(e["rejected"] for e in effects if "rejected" in e), "no_vacancy")
            self.assertEqual(sim.verify_replay(), 3)

    def test_relationship_knowledge_and_privacy(self):
        self.assertTrue(self.incident("route_closure", OPTIONAL)["accepted"])
        self.assertTrue(self.incident("shortage", PEWTER)["accepted"])
        obs = observation(self.sim.state(), self.actor)
        self.assertTrue(all(e["location"] == PEWTER for e in obs["events"].values()))
        self.assertNotIn("money", obs["people"][self.peer])
        self.assertNotIn("skills", obs["people"][self.peer])
        self.assertEqual(list(obs["firms"]), [PEWTER])
        self.assertEqual(self.action(self.actor, "communicate", peer=self.peer, fact="invented")["reason"],
                         "unknown_fact")
        event = next(iter(obs["events"]))
        self.assertTrue(self.action(self.actor, "communicate", peer=self.peer, fact=f"event:{event}")["accepted"])
        learned = observation(self.sim.state(), self.peer)["self"]["known"][f"event:{event}"]
        self.assertEqual(learned["source"], self.actor)

    def test_essential_services_and_progression_boundary(self):
        result = self.incident("route_closure", "ViridianCity|PewterCity")
        self.assertFalse(result["accepted"])
        bad = self.sim.state()
        bad["locations"][bad["requirements"]["PewterCity"]["healing"]]["accessible"] = False
        with self.assertRaisesRegex(Rejected, "essential_service_unreachable"):
            validate(bad)
        self.assertEqual(self.action(self.actor, "set_badge", badge="brock")["reason"], "unknown_action")
        self.assertEqual(self.action(self.actor, "start_battle", levels=[5])["reason"], "unknown_action")
        policy = native_progression_policy()
        self.assertEqual(policy["authority"], "rom")
        self.assertFalse(team_ceiling("classic", "koga", 43, [44]))
        self.assertFalse(team_ceiling("quantum", "koga", 35, [36]))
        self.assertNotIn("badges", project(self.sim.state(), PEWTER))
        self.assertEqual(project(self.sim.state(), PEWTER)["authority"], "host_preview")

    def test_work_delay_replay_and_read_only_inspector(self):
        with TemporaryDirectory() as directory:
            db = Path(directory) / "world.sqlite3"
            employee = next(key for key, p in self.initial["people"].items()
                            if p["employer"] == PEWTER and p["location"] == PEWTER)
            money = self.initial["people"][employee]["money"]
            with closing(Simulation(db, self.initial)) as sim:
                result = sim.command(dict(kind="action", source="npc", actor=employee, action=dict(verb="work")))
                self.assertTrue(result["accepted"])
                sim.advance(3)
                self.assertEqual(sim.state()["people"][employee]["money"], money)
            with closing(Simulation(db)) as sim:
                sim.advance(1)
                self.assertEqual(sim.state()["people"][employee]["money"], money + 5)
                sim.advance(30 * 24 - 4)
                state, entries = sim.snapshot()
                self.assertEqual(digest(replay(entries)), digest(state))
                self.assertGreaterEqual(len(state["events"]), 6)
                self.assertEqual(sim.verify_replay(), 721)
            with closing(Simulation(db, read_only=True)) as sim:
                report = inspect(sim, employee)
                self.assertEqual(report["tick"], 720)
                self.assertTrue(any(e.get("routine") == "wage_paid" for e in report["timeline"]))
                with self.assertRaises(sqlite3.OperationalError):
                    sim.command(dict(kind="tick"))

    def test_production_profile_is_not_opened_as_a_simulation(self):
        with TemporaryDirectory() as directory:
            db = Path(directory) / "living-world.sqlite3"
            with closing(sqlite3.connect(db)) as prior:
                prior.execute("CREATE TABLE npc_checkpoint (save TEXT PRIMARY KEY)")
            original = db.read_bytes()
            with self.assertRaisesRegex(Rejected, "database_is_not_a_simulation"):
                Simulation(db, self.initial)
            self.assertEqual(original, db.read_bytes())

    def test_seeded_thirty_day_run_survives_midstream_reload(self):
        with TemporaryDirectory() as directory:
            db = Path(directory) / "world.sqlite3"
            with closing(Simulation(db, self.initial)) as sim:
                sim.advance(360)
            with closing(Simulation(db)) as sim:
                sim.advance(360)
                expected = sim.state()
            with closing(Simulation(":memory:", self.initial)) as whole:
                whole.advance(720)
                self.assertEqual(whole.state(), expected)
                entries = deepcopy(whole.history())
                entries[20]["result"]["effect"].append("changed")
                with self.assertRaisesRegex(Rejected, "replay_diverged_at_20"):
                    replay(entries)
            with self.assertRaisesRegex(Rejected, "catch_up_limit"):
                self.sim.advance(745)

    def test_model_fixture_is_data_only(self):
        initial = json.loads(json.dumps(region(case="employment")))
        self.assertIsNone(initial["people"][initial["focus"][0]]["goal"])
        self.assertEqual(initial["people"][initial["focus"][0]]["plan"], [])


if __name__ == "__main__":
    unittest.main()
