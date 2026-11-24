"""Ecology safety, attribution and checkpoint semantics."""
from contextlib import closing
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from living_world_manifest import reseal, sample
import ecology
from knowledge import ecological_fact
from live_world import advance_native_clock, append_events
from simulation.engine import Simulation
from world_initialization import PairedCheckpoints
from world_manifest import compatible_catalog, digest, import_world


def scenario():
    manifest = sample()
    names = ("Route24", "Route25", "Route1", "ViridianCity", "Indoor")
    ids = [[3, n] for n in range(30, 30 + len(names))]
    manifest["maps"] = [
        dict(id=key, name=name, objects=[], section=2, map_type=kind,
             access=dict(vidra_section=False), connections=[])
        for key, name, kind in zip(ids, names, (3, 3, 3, 1, 8), strict=True)]
    for origin, dest, direction in ((0, 1, 4), (1, 0, 3), (1, 4, 4), (4, 1, 3), (0, 2, 2)):
        manifest["maps"][origin]["connections"].append(
            dict(target=ids[dest], direction=direction, offset=0))
    manifest["species"] = [dict(id=s, authored={"enabled": True}) for s in (16, 17, 150)]
    manifest["encounters"] = [
        dict(table=dict(map=key, method=0, kind="land", header=i, variant=0),
             slots=[dict(authored=dict(slot=j, species=species, weight=weight, rod=None),
                         status="resolved", species=species, level=[3, 4])
                    for j, (species, weight) in enumerate(((16, 60), (17, 30), (150, 10)))])
        for i, key in enumerate(ids)]
    manifest["ecology_protected"] = [150]
    return reseal(manifest)


class EcologyTests(unittest.TestCase):
    def test_topology_pressure_and_travel_duration(self):
        manifest = scenario()
        before = deepcopy(manifest)
        state = ecology.initial_state(manifest, [150], 0)
        self.assertEqual(before, manifest)
        self.assertEqual({"3:31": 1}, state["habitats"]["3:30"]["simulated"]["edges"]["land"])
        self.assertEqual({"3:30": 1}, state["habitats"]["3:31"]["simulated"]["edges"]["land"])
        self.assertEqual({}, state["groups"]["3:34"])
        self.assertNotIn("150", state["groups"]["3:30"]["land"])
        self.assertFalse(any(ecology.initial_state(manifest, None, 0)["groups"].values()))
        state["groups"]["3:30"]["land"].update({"16": 72, "17": 0})
        state["groups"]["3:31"]["land"].update({"16": 1, "17": 0})
        ecology.evolve_day(state, 1)
        scheduled = state["transit"][0]
        self.assertEqual("3:31", scheduled["destination"])
        self.assertEqual(2, scheduled["arrival"])
        ecology.evolve_day(state, 2)
        self.assertTrue(any(row["kind"] == "migration_arrived" for row in state["history"]))
        for day in range(3, 96):
            ecology.evolve_day(state, day)
            for key, count in ecology.totals(state).items():
                self.assertLessEqual(count, 72)
                self.assertGreaterEqual(count, 0)

    def test_reviewed_compatible_migrant_is_simulation_only(self):
        manifest = scenario()
        for species in manifest["species"]:
            species["authored"]["types"] = [12, 12] if species["id"] == 150 else [2, 2]
        template = manifest["encounters"][1]["slots"]
        manifest["encounters"][1]["slots"] = [template[1]]
        template[1]["authored"].update(slot=0, weight=100)
        state = ecology.initial_state(manifest, [150], 0)
        self.assertNotIn("16", state["groups"]["3:31"]["land"])
        state["groups"]["3:30"]["land"] = {"16": 72, "17": 0}
        state["groups"]["3:31"]["land"] = {"17": 1}
        ecology.evolve_day(state, 1)
        self.assertEqual("16", state["transit"][0]["species"])
        ecology.evolve_day(state, 2)
        self.assertGreater(state["groups"]["3:31"]["land"]["16"], 0)
        self.assertEqual({"17": 100}, state["habitats"]["3:31"]["native"]["distributions"][0]["weights"])

    def test_sighting_scope_confidence_and_age(self):
        state = ecology.initial_state(scenario(), [150], 0)
        day = next(d for d in range(1, 20) if ecology.draw(state["seed"], "patrol", d, "route_scout") % 3 == 0)
        state["day"] = day
        ecology.note(state, "unusual_sighting", "3:32", species=16, confidence=70)
        ecology.fieldwork(state)
        report = state["sightings"]["route_scout"]
        self.assertEqual("route_scout", report["source"])
        self.assertNotIn("viridian_student", state["sightings"])
        state["day"] += 1
        ecology.fieldwork(state)
        secondhand = state["sightings"]["viridian_student"]
        self.assertEqual("route_scout", secondhand["source"])
        self.assertLess(secondhand["confidence"], report["confidence"])
        self.assertIn("heard", ecological_fact(secondhand, state["day"]).line)
        self.assertIsNone(ecological_fact(secondhand, state["day"] + 22))

    def test_report_reuses_validated_dialogue_for_the_verified_speaker(self):
        from concurrent.futures import ThreadPoolExecutor
        import sqlite3
        from types import SimpleNamespace

        from bridge import Conversation, LINE, validate
        from hybrid import FieldHint, HybridDialogue, prepare
        from knowledge import SCHEMA
        from world import WorldMemory

        base = dict(kind="migration_arrived", activity="local_patrol", source="route_scout",
                    location="3:32", observed_day=4, confidence=66)
        for kind in ("migration_arrived", "unusual_sighting", "unusual_population_change"):
            self.assertIsNotNone(LINE.fullmatch(ecological_fact(dict(base, kind=kind), 4).line))
        received = ecological_fact(dict(base, activity="received_from_contact", confidence=41), 5)
        with TemporaryDirectory() as tmp:
            path = Path(tmp)
            lore = path / "lore.db"
            with closing(sqlite3.connect(lore)) as db:
                db.executescript(SCHEMA)
            with (ThreadPoolExecutor() as pool,
                  closing(WorldMemory(path / "world.db", "demo", b"fixture")) as memory):
                model = SimpleNamespace(catalog=lore, style="unavailable", species_names={})
                router = HybridDialogue(memory, model, pool,
                                        ecology_sighting=lambda npc: received if npc == "viridian_student" else None)
                reader = Conversation("viridian_student", None)
                hint = FieldHint(4, None, "viridian", 0, reader.npc, False)
                state = router.key(reader, hint).state
                result, _ = prepare(model, state)
                self.assertIn(received.line.encode(), validate(result.dialogue))
                self.assertEqual((received.key,), result.knowledge)
                self.assertIsNone(router.key(reader).state.encounter.ecology)
                unrelated = FieldHint(4, None, "route_1", 0, reader.npc, False)
                self.assertIsNone(router.key(reader, unrelated).state.encounter.ecology)

    def test_capture_and_native_checkpoint_replay(self):
        with TemporaryDirectory() as tmp:
            path = Path(tmp).resolve()
            manifest = scenario()
            with closing(import_world(path / "world.db", manifest)) as sim:
                base = dict(map=[3, 30], battle_kind="wild", battle=1, seq=1, actor=None, flags=0,
                            mon=dict(species=16, ot=1, personality=2, ivs=3, slot=0), value=0,
                            kind="capture")
                original = ecology.initial_state(manifest, [150], 0)["groups"]["3:30"]["land"]["16"]
                real_apply = ecology.apply

                def interrupted(db, entries):
                    real_apply(db, entries)
                    raise RuntimeError("worker interrupted")

                with patch.object(ecology, "apply", interrupted):
                    with self.assertRaisesRegex(RuntimeError, "interrupted"):
                        append_events(sim, "run", None, [base])
                append_events(sim, "run", None, [base, dict(base, seq=2, flags=1 << 14),
                                                dict(base, seq=3, kind="battle_end", outcome="won", mon=None)])
                append_events(sim, "run", None, [base])
                state = ecology.replay(sim.db)
                self.assertEqual(original - 1, state["groups"]["3:30"]["land"]["16"])
                self.assertEqual([], list(state["individuals"]))
                for hour in range(1, 25):
                    advance_native_clock(sim, "run", hour)
                advance_native_clock(sim, "run", 24)
                self.assertEqual(1, ecology.replay(sim.db)["day"])
                with closing(PairedCheckpoints(path / "paired.db")) as checkpoints:
                    checkpoints.store(b"fixture flash", path / "world.db")
                    restored = checkpoints.restore(b"fixture flash", manifest["context"], manifest, path)
                with closing(Simulation(restored, read_only=True)) as copy:
                    self.assertEqual(ecology.replay(sim.db), ecology.replay(copy.db))

    def test_legacy_catalog_requires_same_rom_and_exact_previous_meaning(self):
        original = {"build": {"rom_sha256": "1"*64, "revision": "old"}, "maps": [3]}
        manifest = {"build": original["build"], "catalog_sha256": digest(original)}
        modern = {**original, "ecology_protected": [150],
                  "build": {"rom_sha256": "1"*64, "revision": "new"}}
        modern["catalog_sha256"] = digest(modern)
        self.assertTrue(compatible_catalog(manifest, modern))
        self.assertFalse(compatible_catalog(manifest, {**modern, "maps": [4]}))
        self.assertFalse(compatible_catalog(manifest,
                                           {**modern, "build": {"rom_sha256": "2"*64}}))


if __name__ == "__main__":
    unittest.main()
