"""Durable observation acknowledgments, ownership, and paired rollback."""
from contextlib import closing
from copy import deepcopy
import json
from pathlib import Path
import sqlite3
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from living_world_manifest import sample
from live_world import Checkpoint, append_events, apply_batch
from simulation.engine import Simulation
from world_initialization import PairedCheckpoints
from world_manifest import import_world


class ObservationPersistence(unittest.TestCase):
    def test_exactly_once_capture_and_checkpoint_cut(self):
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            db = root / "world.sqlite3"
            pairs = root / "pairs.sqlite3"
            manifest = sample()
            with closing(import_world(db, manifest)):
                pass
            wild = dict(slot=0, species=16, personality=43, ivs=9, ot=0, moves=[1, 0, 0, 0])
            captured = {**wild, "ot": 13}
            encounter = dict(seq=1, kind="battle_mon", mon=wild, map=[3, 19], actor=None, battle=1)
            catch = dict(encounter, seq=2, kind="capture", mon=captured, value=0)
            party = dict(catch, seq=3, battle=None, kind="party")
            save = [("event", encounter), ("event", catch), ("tick", 3601), ("checkpoint", Checkpoint(b"flash", 12))]
            batch = [*save, ("event", party)]
            store = PairedCheckpoints.store

            def interrupt_after_commit(pair, *args):
                store(pair, *args)
                raise sqlite3.OperationalError("worker stopped after a durable checkpoint")

            with patch.object(PairedCheckpoints, "store", interrupt_after_commit):
                with self.assertRaisesRegex(sqlite3.OperationalError, "worker stopped"):
                    apply_batch(db, pairs, "run", None, batch)
            apply_batch(db, pairs, "run", None, batch)
            apply_batch(db, pairs, "run", None, batch)

            with closing(Simulation(db)) as sim:
                self.assertEqual(1, sim.verify_replay())
                self.assertEqual(3, sim.db.execute("SELECT ack FROM native_streams").fetchone()[0])
                self.assertEqual([(1,), (2,), (3,)], sim.db.execute("SELECT seq FROM native_events").fetchall())
                individual, owner = sim.db.execute("SELECT id,owner FROM observed_pokemon").fetchone()
                self.assertEqual("player", owner)
                self.assertEqual(("run:1:0", individual), sim.db.execute("SELECT * FROM observed_aliases").fetchone())
                self.assertEqual((0, individual), sim.db.execute("SELECT * FROM observed_party").fetchone())
                divergent = deepcopy(encounter)
                divergent["mon"]["species"] = 17
                with self.assertRaisesRegex(ValueError, "Divergent"):
                    append_events(sim, "run", None, [divergent])
                with self.assertRaisesRegex(ValueError, "another world"):
                    append_events(sim, "run", "another", [encounter])
                with self.assertRaisesRegex(ValueError, "Noncontiguous"):
                    append_events(sim, "run", None, [dict(party, seq=5)])
                self.assertEqual(manifest, json.loads(sim.db.execute("SELECT document FROM starting_manifest").fetchone()[0]))

            with closing(PairedCheckpoints(pairs)) as pair:
                resumed = pair.restore(b"flash", manifest["context"], manifest, root)
            with closing(Simulation(resumed)) as sim:
                self.assertEqual((2,), sim.db.execute("SELECT ack FROM native_streams").fetchone())
                self.assertEqual([], sim.db.execute("SELECT * FROM observed_party").fetchall())
                self.assertEqual(1, sim.state()["tick"])
                self.assertEqual((12,), sim.db.execute("SELECT remaining FROM native_clock").fetchone())
            with closing(import_world(db, manifest)) as sim:
                self.assertEqual(1, sim.state()["tick"])


if __name__ == "__main__":
    unittest.main()
