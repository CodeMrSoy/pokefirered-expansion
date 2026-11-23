"""Manifest validation, transaction recovery and backwards compatibility."""
from contextlib import closing
from copy import deepcopy
from pathlib import Path
import sqlite3
import sys
from tempfile import TemporaryDirectory
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "experiments/living_world"))
from simulation.engine import Simulation
from world_initialization import PairedCheckpoints
from world_manifest import digest, import_world, validate_manifest


def reseal(manifest):
    manifest["manifest_sha256"] = digest({k:v for k,v in manifest.items() if k != "manifest_sha256"})
    return manifest


def sample():
    return reseal(dict(
        version=1, world_uuid="5b043b9b-21c8-4a9a-a12f-36390078daf0",
        build={"rom_sha256": "1"*64}, catalog_sha256="2"*64,
        context=dict(version=1, origin=1, mode=1, seed=123, generation=1, features=0, modes=8, trainer_id=13),
        maps=[dict(id=[3, 19], name="Route1", objects=[], access={"status":"conditional"})],
        encounters=[dict(table=dict(map=[3, 19], method=0, header=0, variant=0),
                         slots=[dict(authored=dict(slot=0, species=16, weight=100, rod=None),
                                     status="resolved", species=16, level=[3,3])])],
        species=[dict(id=16)], trainers=[], static_encounters=[], gyms=[], services=[], rules={},
    ))


class ManifestTests(unittest.TestCase):
    def test_rejects_corrupted_and_malformed_graph(self):
        world = sample()
        world["encounters"][0]["slots"][0]["species"] = 999
        with self.assertRaisesRegex(ValueError, "sha256 mismatch"):
            validate_manifest(world)
        with self.assertRaisesRegex(ValueError, "Invalid resolved Pokémon"):
            validate_manifest(reseal(world))
        world["encounters"][0]["slots"][0]["species"] = 16
        world["encounters"][0]["slots"][0]["authored"]["weight"] = 10
        with self.assertRaisesRegex(ValueError, "Invalid slot weights"):
            validate_manifest(reseal(world))

    def test_import_never_resets_or_assigns_owned_pokemon(self):
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "world.sqlite3"
            world = sample()
            with closing(import_world(path, world)) as sim:
                self.assertEqual({}, sim.state()["pokemon"])
                sim.advance(5)
            with closing(import_world(path, world)) as sim:
                self.assertEqual(5, sim.state()["tick"])
                self.assertEqual(5, sim.verify_replay())
            other = deepcopy(world)
            other["world_uuid"] = "5b043b9b-21c8-4a9a-a12f-36390078daf1"
            with self.assertRaisesRegex(ValueError, "starting_manifest_mismatch"):
                import_world(path, reseal(other))
            with closing(Simulation(path)) as sim:
                self.assertEqual(world["world_uuid"], sim.state()["world_uuid"])

    def test_pair_rollback_and_fork(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "world.sqlite3"
            world = sample()
            with closing(import_world(path, world)) as sim:
                sim.advance(2)
                with closing(PairedCheckpoints(root / "pairs.sqlite3")) as pairs:
                    pairs.store(b"battery one", path)
                    sim.advance(2)
                    def interrupted():
                        raise RuntimeError("interrupted")
                    with self.assertRaisesRegex(RuntimeError, "interrupted"):
                        pairs.store(b"battery two", path, before_commit=interrupted)
                    with self.assertRaisesRegex(ValueError, "No valid paired"):
                        pairs.restore(b"battery two", world["context"], world, root)
                    resumed = pairs.restore(b"battery one", world["context"], world, root)
                    with closing(Simulation(resumed)) as restored:
                        self.assertEqual(2, restored.state()["tick"])
                    self.assertEqual(4, sim.state()["tick"])
                    with self.assertRaisesRegex(ValueError, "Incompatible"):
                        pairs.restore(b"battery one", {**world["context"], "seed":456}, world, root)
                    pairs.db.execute("UPDATE paired SET world=? WHERE flash=?", (b"invalid",b"battery one"))
                    pairs.db.commit()
                    with self.assertRaisesRegex(ValueError, "No valid paired"):
                        pairs.restore(b"battery one", world["context"], world, root)


if __name__ == "__main__":
    unittest.main()
