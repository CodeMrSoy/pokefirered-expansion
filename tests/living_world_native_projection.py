"""Wire format, map policy, and unregistered acceptance checks."""
import ctypes as c
from contextlib import closing
from pathlib import Path
import sqlite3
import sys
from types import SimpleNamespace
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "experiments/living_world"))

import native_projection as p
from ecology import native_wild


class ProjectionTests(unittest.TestCase):
    def test_sealed_write_and_complete_packet(self):
        address = 0x02001300
        ram = c.create_string_buffer(0x40000)
        game = SimpleNamespace(memory=lambda _: c.addressof(ram), memory_size=lambda _: len(ram))
        base = address - 0x02000000
        document = dict(generation=1, counter=7, seed=11, mode=0, modes=23, trainer_id=37,
                        key_a=45, key_b=99, kind=p.TRAINER, map=[1, 0], variant=104,
                        revision=84, party=[dict(tag=24, species=13, ability=19, ability_slot=0,
                                                moves=[33], level=8)])
        self.assertFalse(p.publish(game, address, document, 123))
        self.assertEqual(b"\0" * (p.SIZE + 4), ram.raw[base:base+p.SIZE+4])
        seal = (p.SEAL ^ address).to_bytes(4, "little")
        ram[base+p.SIZE:base+p.SIZE+4] = seal
        self.assertTrue(p.publish(game, address, document, 123))
        frame = ram.raw[base:base+p.SIZE]
        header = p.HEADER.unpack(frame[:p.HEADER.size])
        self.assertEqual((p.MAGIC, 1, 1, 7, 123), header[:5])
        self.assertEqual(p.checksum(frame[4:64] + frame[68:]), header[-1])
        self.assertEqual((24, 13, 19, 33, 0, 0, 0, 8, 0, 0, 0),
                         p.MON.unpack(frame[68:88]))
        self.assertTrue(p.publish(game, address, None, 0))
        self.assertEqual(ram.raw[base:base+4], b"\0"*4)
        self.assertEqual(ram.raw[base+p.SIZE:base+p.SIZE+4], seal)

    def test_unregistered_native_revision_is_quarantinable(self):
        event = dict(kind="projection", battle=9, value=1, actor=1, map=[1, 0], flags=1)
        with closing(sqlite3.connect(":memory:")) as db:
            with self.assertRaisesRegex(ValueError, "unregistered"):
                p.receive(db, "stream", event)
            for sql in p.SCHEMA:
                db.execute(sql)
            with self.assertRaisesRegex(ValueError, "stream or revision"):
                p.receive(db, "another-stream", event)

    def test_land_weight_and_native_variants_have_bounded_scope(self):
        habitat = dict(name="Route24", native=dict(protected_encounter=False, distributions=[
            dict(method="land", variant=0, weights={"13": 80, "16": 20}),
            dict(method="land", variant=1, weights={"13": 100}),
            dict(method="surf", variant=2, weights={"72": 100})]),
            simulated=dict(edges={"land": {"3:44": 1}}, layers={"land": dict(compatible_arrivals=["25", "150"])}))
        state = dict(habitats={"3:43": habitat}, groups={"3:43": {"land": {"13":72, "16":20, "25":5, "150":17}}})
        mask, rows = p.wild_offer(dict(ecology_protected=[150]), state, [3, 43])
        self.assertEqual(3, mask)
        self.assertEqual([(25, 6, True), (13, 20, False)],
                         [(row["species"], row["weight"], row["migrant"]) for row in rows])
        self.assertEqual((0, []), p.wild_offer({}, state, [3, 45]))


    def test_lease_cannot_be_reused_and_old_streams_release_it(self):
        uid = "sim:reviewed"
        state = dict(day=2, history=[], event_counts={}, sightings={},
                     individuals={uid: dict(location="3:43", layer="land", species=16)})
        lease = dict(stream="first", individual=uid, lease="a", location="3:43", level=7)
        native_wild(state, dict(lease, status="reserved"))
        with self.assertRaisesRegex(ValueError, "could not acquire"):
            native_wild(state, dict(lease, status="reserved"))
        native_wild(state, dict(lease, status="engaged", battle="first:8"))
        with self.assertRaisesRegex(ValueError, "did not own"):
            native_wild(state, dict(lease, stream="another", status="captured", battle="first:8"))
        native_wild(state, dict(status="map", stream="after-continue", location="3:43"))
        self.assertNotIn("reservation", state["individuals"][uid])
        lease.update(stream="after-continue", lease="b")
        native_wild(state, dict(lease, status="reserved"))
        native_wild(state, dict(lease, status="engaged", battle="after-continue:4"))
        native_wild(state, dict(lease, status="captured", battle="after-continue:4"))
        self.assertNotIn(uid, state["individuals"])
        with self.assertRaisesRegex(ValueError, "no wild individual"):
            native_wild(state, dict(lease, status="captured", battle="after-continue:4"))


    def test_verified_sammy_mailbox_keeps_facts_during_busy_script(self):
        from concurrent.futures import ThreadPoolExecutor
        from tempfile import TemporaryDirectory

        from bridge import Conversation, validate
        from hybrid import FieldHint, HybridDialogue, prepare
        from knowledge import Fact, SCHEMA
        from world import WorldMemory

        fact = Fact("sammy:training", "rumor", "I trained my Pokemon.", "I trained my Pokemon.", "trainer")
        with (TemporaryDirectory() as temporary, ThreadPoolExecutor() as executor,
              closing(WorldMemory(Path(temporary) / "notes.sqlite3", "demo", b"flash")) as memory):
            catalog = Path(temporary) / "knowledge.sqlite3"
            with closing(sqlite3.connect(catalog)) as db:
                db.executescript(SCHEMA)
            model = SimpleNamespace(catalog=catalog, style="unavailable", species_names={})
            dialogue = HybridDialogue(memory, model, executor, ecology_sighting=lambda npc: fact)
            request = Conversation("sammy", None)
            active = FieldHint(42, None, "viridian_forest", 0, None, True)
            prepared, _ = prepare(model, dialogue.key(request, active).state)
            self.assertIn(fact.line.encode(), validate(prepared.dialogue))
            wrong_map = FieldHint(42, None, "pallet", 0, None, True)
            self.assertIsNone(dialogue.key(request, wrong_map).state.encounter.ecology)


if __name__ == "__main__":
    unittest.main()
