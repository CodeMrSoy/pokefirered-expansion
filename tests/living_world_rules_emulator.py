"""Exercise the Phase 14 Mart counter and Gym advice in the compiled ROM."""

import json
import struct
from pathlib import Path
from tempfile import TemporaryDirectory

import quantum_qol_emulator as gba

fixture = (gba.root / "tests/living_world_bridge_emulator.py").read_text().split(
    "native, mode, group, map_number = setup()")[0]
exec(compile(fixture, "native fixture", "exec"))

from world_rules import CHECKOUT, GYM, MART, PITCH, SUPPORT, PRACTICE_ROCK, PRACTICE_TRAIL, apply_decision


def warp(name, x, y):
    for group, key in enumerate(maps["group_order"]):
        if name in maps[key]:
            number = maps[key].index(name)
            gba.inject(b"\x39" + struct.pack("<BBBhh", group, number, 255, x, y) + b"\x27\x6b\x02")
            assert field_ready()
            return
    raise AssertionError(name)


def task_active(name):
    address = gba.symbols[name] | 1
    for i in range(16):
        task = gba.read(gba.symbols["gTasks"] + 40*i, 5)
        if task[4] and struct.unpack_from("<I", task)[0] == address:
            return True
    return False


def converse(label, refusal=False, practice=False):
    seen = {}
    shop = False
    def propose(context):
        text = rules.reply(context.npc)
        if text is None:
            return SKIP
        seen[context.npc] = text
        return json.dumps({"action": "SAY_DIALOGUE", "text": text})
    invoke_event(label)
    try:
        for frame in range(1400):
            trace = bridge.poll(propose)
            if trace and trace["validation"] == "accepted" and trace["context"]["npc"] == SUPPORT:
                assert rules.endorse()
            in_shop = task_active("Task_ShopMenu")
            if in_shop:
                stock = struct.unpack("<I", gba.read(gba.symbols["sShopData"] + 4, 4))[0]
                assert stock == gba.symbols["PewterCity_Mart_Items"]
            shop = shop or in_shop
            if practice and gba.read(gba.symbols["gEnemyParty"] + 84, 1)[0] != 0:
                return seen, shop
            if frame > 1 and field_ready():
                return seen, shop
            gba.keys.clear()
            if frame % 10 == 0:
                decline = (refusal and PITCH in seen) or (not practice and
                           (PRACTICE_ROCK in seen or PRACTICE_TRAIL in seen))
                gba.keys.add(0 if in_shop or decline else 8)
            gba.run(1)
    finally:
        gba.keys.clear()
    raise AssertionError(f"Dialogue did not release controls: {label}")


native, mode, _, _ = setup()
native("FlagSet", 0x829)
maps = json.loads((gba.root / "data/maps/map_groups.json").read_bytes())
mailbox = gba.symbols["gLivingWorldMailbox"]
bridge = DialogueBridge(gba.read, gba.write, mailbox, deferred=True)

with TemporaryDirectory() as folder:
    path = Path(folder) / "world.db"
    memory = WorldMemory(path, "pilot", b"before")
    rules = memory.rules
    warp("PewterCity_Mart", 5, 6)
    resident = "PewterCity_Mart_EventScript_Boy"
    clerk = "PewterCity_Mart_EventScript_Clerk"
    assert converse(clerk)[1]
    assert converse(resident) == ({}, False)
    assert native("GetCurrentLevelCap") == 14
    native("FlagSet", 0x820)
    assert native("GetCurrentLevelCap") == 21
    native("FlagSet", 0x4B0)
    rules.observe(1000, True)
    offered, shop = converse(resident, refusal=True)
    assert PITCH in offered and SUPPORT not in offered and not shop
    assert not rules.state["endorsed"]
    accepted, _ = converse(resident)
    assert SUPPORT in accepted and rules.state["endorsed"]
    for second in (1050, 1150):
        rules.observe(second, True)
        choice = rules.decision()
        selection = ("type_coaching" if mode == 0 else "expedition_coaching") if choice.actor == "gym" else choice.fallback
        assert apply_decision(rules, choice, selection, "fallback")
    hired, shop = converse(resident)
    assert MART in hired and CHECKOUT in hired and shop
    assert converse(clerk)[1]
    warp("PewterCity_Gym", 6, 6)
    assert GYM in converse("PewterCity_Gym_EventScript_GymGuy")[0]
    gba.inject(b"\x23" + struct.pack("<I", (gba.symbols["ScrCmd_givegiftmon"] | 1) + 0x2000000)
               + struct.pack("<BBHHI", 0, 7, 14, 16, 0) + b"\x02")
    before = c.create_string_buffer(gba.lib.retro_serialize_size())
    assert gba.lib.retro_serialize(before, len(before))
    scene, _ = converse("PewterCity_Gym_EventScript_GymGuy", practice=True)
    assert (PRACTICE_ROCK if mode == 0 else PRACTICE_TRAIL) in scene
    assert struct.unpack("<H", gba.read(gba.symbols["gTrainerBattleParameter"] + 2, 2))[0] == 751 + mode
    assert gba.read(gba.symbols["gEnemyParty"] + 84, 1)[0] == 10 + mode
    assert gba.lib.retro_unserialize(before, len(before))
    gba.run(60)
    memory.checkpoint(b"after")
    memory.close()
    memory = WorldMemory(path, "pilot", b"after")
    rules = memory.rules
    rules.observe(1170, True)
    warp("PewterCity_Mart", 5, 6)
    assert converse(resident)[1]
    assert converse(clerk)[1]
    memory.close()
print(f"PASS mode {mode}: original and apprentice counters, endorsement consent, saved occupation and capped Gym practice")

# Exercise both actual object scripts with an accepted compositional plan.
import agency
memory = WorldMemory(":memory:", "agency", b"post-brock")
rules = memory.rules
rules.observe(0, True)
rules.observe(50, True)
assert agency.submit(rules, agency.ticket(rules), "Help my neighbor|ask stock;work sales")
warp("PewterCity_Mart", 5, 6)
assert converse(resident)[1]
rules.observe(150, True)
assert agency.submit(rules, agency.ticket(rules), "Share knowledge|teach stock;practice sales;work sales")
assert converse("PewterCity_Mart_EventScript_Youngster")[1]
assert converse(clerk)[1]
memory.close()
print(f"PASS mode {mode}: composed resident and neighbor plans reached both native shop menus")
