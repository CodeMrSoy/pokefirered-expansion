"""Run new early-Kanto authored asides through the real ROM script interpreter."""

import ctypes as c
import json
from pathlib import Path
import struct
import subprocess
from tempfile import TemporaryDirectory

import quantum_qol_emulator as gba

support = (gba.root / "tests/living_world_bridge_emulator.py").read_text().split(
    "native, mode, group, map_number = setup()")[0]
exec(compile(support, "Kanto fixture", "exec"))

from kanto import HOOKS, KantoCatalog, dialogue, residents as kanto_residents
from population import residents


def enter(name, x, y):
    for group, key in enumerate(maps["group_order"]):
        if name in maps[key]:
            number = maps[key].index(name)
            gba.inject(b"\x39" + struct.pack("<BBBhh", group, number, 255, x, y) + b"\x27\x6b\x02")
            assert field_ready()
            return
    raise AssertionError(name)


def wait_request():
    for frame in range(720):
        if (head := gba.read(mailbox, REPLY_OFFSET)).startswith(b"LQW1"):
            gba.keys.discard(8)
            return struct.unpack_from("<H", head, 8)[0]
        if frame % 8 == 0:
            gba.keys.add(8)
        else:
            gba.keys.discard(8)
        gba.run(1)
    gba.keys.discard(8)
    raise AssertionError("Expected a supplemental Kanto mailbox request")


native, mode, _group, _map_number = setup()
native("FlagSet", 0x829)
maps = json.loads((gba.root / "data/maps/map_groups.json").read_bytes())
mailbox = gba.symbols["gLivingWorldMailbox"]
hint_address = gba.symbols["gLivingWorldFieldHint"]
bridge = DialogueBridge(gba.read, gba.write, mailbox, deferred=True)

with TemporaryDirectory() as tmp:
    directory = Path(tmp)
    catalog_path = directory / "catalog.sqlite3"
    subprocess.run([sys.executable, "-B", gba.root / "experiments/living_world/build-knowledge.py", catalog_path],
                   check=True)
    catalog = KantoCatalog(catalog_path)
    memory = WorldMemory(directory / "world.db", "test", b"kanto",
                         roster=(*residents(), *kanto_residents(catalog)))
    for id_, name, label, area, x, y in (
        (20, "ViridianForest", "Boy", "viridian_forest", 27, 46),
        (21, "Route3", "Youngster", "route_3", 4, 9),
        (22, "MtMoon_1F", "BaldingMan", "mt_moon", 14, 33),
        (23, "Route4", "Boy", "route_4", 42, 8),
        (24, "CeruleanCity", "BaldingMan", "cerulean", 20, 20),
        (25, "Route25", "Man", "route_25", 29, 6),
    ):
        enter(name, x, y)
        assert FieldHint.decode(gba.read(hint_address, FIELD_SIZE)).area == area
        invoke_event(f"{name}_EventScript_{label}")
        assert wait_request() == id_
        npc = HOOKS[id_]
        expected = dialogue(catalog, memory, memory.population, Conversation(npc, None))
        trace = bridge.poll(lambda ctx: json.dumps({"action": "SAY_DIALOGUE", "text": expected}))
        assert trace["validation"] == "accepted", trace
        assert trace["context"]["npc"] == npc
        assert render_expected(expected) == printed_message()
        gba.snap(f"phase12-{area}-{mode}")
        finish_dialogue()
        bridge.poll(lambda _: SKIP)
    memory.close()

give_mon = b"\x23" + struct.pack("<I", (gba.symbols["ScrCmd_givegiftmon"] | 1) + 0x2000000)
gba.inject(give_mon + struct.pack("<BBHHI", 0, 6, 7, 16, 0) + b"\x02")
enter("ViridianForest", 27, 46)


def challenge(label, opponent):
    before = c.create_string_buffer(gba.lib.retro_serialize_size())
    assert gba.lib.retro_serialize(before, len(before))
    invoke_event(label)
    for _ in range(20):
        gba.press(8, 30)
        if struct.unpack("<I", gba.read(gba.symbols["gBattleTypeFlags"], 4))[0] & 8:
            break
    else:
        raise AssertionError(f"Expected battle at {label}")
    # opponentA follows the two one-byte mode and local-ID fields.
    assert struct.unpack("<H", gba.read(gba.symbols["gTrainerBattleParameter"] + 2, 2))[0] == opponent
    assert not gba.read(mailbox, 4).startswith(b"LQW1")
    assert gba.lib.retro_unserialize(before, len(before))
    gba.run(5)


challenge("ViridianForest_EventScript_Rick", 102)
enter("CeruleanCity_Gym", 4, 3)
assert native("AddBagItem", 715, 1)  # ITEM_TM_CASE
challenge("CeruleanCity_Gym_EventScript_Misty", 415)
native("SetTrainerFlag", 415)
invoke_event("CeruleanCity_Gym_EventScript_MistyDefeated")
for _ in range(30):
    if field_ready():
        break
    gba.press(8, 30)
    gba.press(0, 10)
else:
    gba.snap("misty-award-stalled")
    raise AssertionError("Misty's reward script did not release field controls")
assert native("FlagGet", 0x821) and native("FlagGet", 0x4B1)
print(f"PASS mode {mode}: six Kanto dialogue hooks, Forest trainer and Misty battle entry, badge continuation")
