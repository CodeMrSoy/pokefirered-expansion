"""Trainer validation, accounting, replay, and paired saves."""
from contextlib import closing
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
import json
import unittest
from unittest.mock import patch

from living_world_manifest import reseal
from living_world_ecology import scenario as ecological_fixture
import ecology
import trainers
from live_world import advance_native_clock, append_events
from simulation.engine import Simulation
from world_initialization import PairedCheckpoints
from world_manifest import compatible_catalog, digest, import_world


def scenario():
    manifest = ecological_fixture()
    towns = manifest["maps"]
    towns[2]["objects"] = [dict(labels=["Route1_EventScript_Boy"], binding=None)]
    towns[3]["objects"] = [dict(labels=["ViridianCity_EventScript_Youngster"], binding=None)]
    towns[2]["connections"].append(dict(target=towns[3]["id"], direction=1, offset=2))
    towns[3]["connections"].append(dict(target=towns[2]["id"], direction=2, offset=-2))
    authored = dict(enabled=True, catch_rate=230, types=[7, 7], stats=[40] * 6, evolutions=[])
    manifest["species"] = [dict(id=species, authored=deepcopy(authored), status="resolved",
                                abilities=[ability, 0], learnset=[[move, 1], [move+1, 4]])
                           for species, ability, move in ((16, 31, 90), (17, 32, 92), (150, 33, 94))]
    manifest["species"][0]["authored"]["evolutions"] = [dict(method=1, conditions=[], target=17, parameter=4)]
    return reseal(manifest)


def assert_accounting(state, eco):
    all_owned = set()
    for key, a in state["actors"].items():
        money = a["resources"]
        assert a["cash"] == money["grant_cash"] + money["earned"] - money["spent"] >= 0
        assert a["balls"] == money["grant_balls"] + money["balls_bought"] - money["balls_used"] >= 0
        assert len(a["party"]) <= 6 and len(a["storage"]) <= trainers.STORAGE_SLOTS
        for uid in a["party"] + a["storage"]:
            assert uid not in all_owned and uid not in eco["individuals"]
            assert state["mons"][uid]["owner"] == key
            assert state["mons"][uid]["level"] <= trainers.MAX_LEVEL
            all_owned.add(uid)
    assert set(state["mons"]) == all_owned
    counters = state["counters"]
    assert counters.get("capture", 0) == len(all_owned)
    assert counters.get("capture", 0) + counters.get("capture_failed", 0) == sum(
        a["resources"]["balls_used"] for a in state["actors"].values())
    assert min((count for groups in eco["groups"].values() for layer in groups.values()
                for count in layer.values()), default=0) >= 0


class TrainerTests(unittest.TestCase):
    def test_distinct_journeys_and_conservation(self):
        manifest = scenario()
        index = trainers.build_index(manifest, [150])
        self.assertEqual({"route_scout", "viridian_student"}, set(index["actors"]))
        self.assertNotIn(150, index["species"])
        self.assertEqual({"3:33": 1}, index["edges"]["3:32"])
        self.assertFalse(trainers.build_index(manifest, None)["actors"])
        eco = ecology.initial_state(manifest, [150], 0)
        state = trainers.start(index, eco, 0)
        histories = {key: [] for key in state["actors"]}
        for day in range(1, 366):
            ecology.evolve_day(eco, day)
            before = sum(ecology.totals(eco).values())
            events = trainers.advance(state, eco, index)
            self.assertEqual(before - sum(row["kind"] == "capture" for row in events),
                             sum(ecology.totals(eco).values()))
            assert_accounting(state, eco)
            for key in histories:
                histories[key].append(state["actors"][key]["activity"])
        self.assertNotEqual(*histories.values())
        self.assertGreater(state["counters"]["capture"], 5)
        self.assertGreater(state["counters"]["training"], 20)
        self.assertGreater(state["counters"]["evolution"], 0)
        self.assertTrue(any(a["storage"] for a in state["actors"].values()))
        self.assertFalse(any(mon["species"] == 150 for mon in state["mons"].values()))
        self.assertEqual(scenario(), manifest)

    def test_notable_transfer_and_invalid_sightings(self):
        manifest = scenario()
        index = trainers.build_index(manifest, [150])
        eco = ecology.initial_state(manifest, [150], 0)
        state = trainers.start(index, eco, 0)
        a = state["actors"]["route_scout"]
        loc = a["location"]
        uid = "sim:rare"
        eco["individuals"][uid] = dict(location=loc, species=16, layer="land", id=uid)
        a["sighting"] = dict(day=0, location=loc, species=16, individual=uid, confidence=90, source="route_scout")
        before = ecology.totals(eco)[loc]
        with patch("ecology.draw", return_value=0):
            trainers.capture(state, eco, index, "route_scout", "16", [])
        self.assertIn(uid, a["party"])
        self.assertNotIn(uid, eco["individuals"])
        self.assertEqual(before-1, ecology.totals(eco)[loc])
        a["sighting"] = dict(day=0, location=loc, species=16, individual=uid, confidence=90, source="route_scout")
        trainers.capture(state, eco, index, "route_scout", "16", [])
        self.assertEqual(2, a["balls"])
        self.assertEqual([uid], a["party"])
        assert_accounting(state, eco)

    def test_model_action_validation_and_failure_atomicity(self):
        with TemporaryDirectory() as tmp:
            path = Path(tmp).resolve()
            db = path / "world.sqlite3"
            world = scenario()
            with closing(import_world(db, world)) as sim:
                append_events(sim, "clock", None, [], [150])
                sim.advance(23)
                advance_native_clock(sim, "clock", 100, [150])
                state = trainers.load(sim.db)
                request = state["request"]
                self.assertIsNotNone(request)
                model = SimpleNamespace(style="qwen3", render_prompt=lambda *p: p,
                                        worker=SimpleNamespace(generate=lambda *args, **kw: ("A:1", {})))
                proposed = trainers.request_plan(model, request)
                self.assertEqual("recover", proposed["goal"])
                self.assertTrue(trainers.confirmed_plan(request, proposed))
                self.assertFalse(trainers.confirmed_plan(request, dict(proposed,
                                                                       steps=[["ATTEMPT_CAPTURE", "150"]])))
                sim.advance(23)
                before = ecology.read_state(sim.db)
                with patch("trainers.write", side_effect=RuntimeError("interrupted")):
                    with self.assertRaisesRegex(RuntimeError, "interrupted"):
                        advance_native_clock(sim, "clock", 200, [150], proposed)
                self.assertEqual(47, sim.state()["tick"])
                self.assertEqual(before, ecology.read_state(sim.db))
                self.assertEqual(state, trainers.load(sim.db))
                advance_native_clock(sim, "clock", 200, [150], proposed)
                after = trainers.load(sim.db)
                self.assertEqual(1, after["counters"]["model_plan_admitted"])
                self.assertEqual("offline_qwen", after["actors"][request["actor"]]["decisions"][-1]["source"])
                advance_native_clock(sim, "clock", 200, [150], proposed)
                self.assertEqual(after, trainers.load(sim.db))
                self.assertEqual(ecology.read_state(sim.db), ecology.replay(sim.db))
                self.assertEqual(world, json.loads(sim.db.execute("SELECT document FROM starting_manifest").fetchone()[0]))
                with closing(PairedCheckpoints(path / "paired.sqlite3")) as paired:
                    paired.store(b"flash", db)
                    sim.advance(23)
                    advance_native_clock(sim, "clock", 300, [150])
                    restored = paired.restore(b"flash", world["context"], world, path)
                    with closing(Simulation(restored, read_only=True)) as resumed:
                        self.assertEqual(after, trainers.load(resumed.db))
                        self.assertEqual(48, resumed.state()["tick"])
                        ecology.replay(resumed.db)

    def test_dialogue_uses_current_speakers_documented_activity(self):
        from concurrent.futures import ThreadPoolExecutor
        import sqlite3

        from bridge import Conversation, validate
        from hybrid import FieldHint, HybridDialogue, prepare
        from knowledge import SCHEMA
        from world import WorldMemory

        manifest = scenario()
        index = trainers.build_index(manifest, [150])
        eco = ecology.initial_state(manifest, [150], 0)
        state = trainers.start(index, eco, 0)
        a = state["actors"]["route_scout"]
        a["sighting"] = dict(day=0, location=a["location"], species=16, individual=None,
                             confidence=80, source="route_scout")
        with patch("ecology.draw", return_value=0):
            trainers.capture(state, eco, index, "route_scout", "16", [])
        fact = trainers.fact(state, "route_scout")
        self.assertIsNotNone(fact)
        self.assertIsNone(trainers.fact(state, "viridian_student"))
        with TemporaryDirectory() as tmp:
            path = Path(tmp)
            lore = path / "lore.db"
            with closing(sqlite3.connect(lore)) as db:
                db.executescript(SCHEMA)
            with (ThreadPoolExecutor() as pool,
                  closing(WorldMemory(path / "world.db", "demo", b"fixture")) as memory):
                model = SimpleNamespace(catalog=lore, style="unavailable", species_names={})
                router = HybridDialogue(memory, model, pool, ecology_sighting=lambda npc: trainers.fact(state, npc))
                reader = Conversation("route_scout", None)
                hint = FieldHint(4, None, "route_1", 0, reader.npc, False)
                exchange = router.key(reader, hint).state
                result, _ = prepare(model, exchange)
                self.assertIn(fact.line.encode(), validate(result.dialogue))
                self.assertEqual((fact.key,), result.knowledge)
                other = FieldHint(4, None, "viridian", 0, reader.npc, False)
                self.assertIsNone(router.key(reader, other).state.encounter.ecology)

    def test_old_compiled_binding_digest_and_protected_roster(self):
        original = dict(build={"rom_sha256": "1"*64, "revision": "legacy"}, ecology_protected=[150],
                        maps=[dict(objects=[dict(binding=dict(opcode=0x5C, battle_script_mode=4,
                                                             trainer=26624))])])
        updated = deepcopy(original)
        updated["build"]["revision"] = "new"
        updated["maps"][0]["objects"][0]["binding"].update(trainer=104, trainer_local=0)
        updated["catalog_sha256"] = digest(updated)
        manifest = dict(build=original["build"], catalog_sha256=digest(original), ecology_protected=[150])
        self.assertTrue(compatible_catalog(manifest, updated))
        updated["maps"][0]["objects"][0]["binding"]["trainer"] = 105
        self.assertFalse(compatible_catalog(manifest, updated))

        fixture = scenario()
        fixture["maps"][4].update(name="ViridianForest", objects=[
            dict(labels=["ViridianForest_EventScript_Sammy"], binding=original["maps"][0]["objects"][0]["binding"])])
        fixture["trainers"].append(dict(id=104, protected=True))
        self.assertNotIn("sammy", trainers.build_index(fixture, [150])["actors"])
        fixture["trainers"][0]["protected"] = False
        self.assertEqual(104, trainers.build_index(fixture, [150])["actors"]["sammy"]["native_roster"]["id"])


if __name__ == "__main__":
    unittest.main()
