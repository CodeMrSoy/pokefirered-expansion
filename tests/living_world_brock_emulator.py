"""Exercise production Brock presence and the original Gym challenge in mGBA."""
import ctypes as c
import json
import os
from pathlib import Path
import struct
from tempfile import TemporaryDirectory

import quantum_qol_emulator as gba

# Use the same native fixture and script driver as the Pallet bridge tests.
support = (gba.root / "tests/living_world_bridge_emulator.py").read_text().split(
    "native, mode, group, map_number = setup()")[0]
exec(compile(support, "Pewter fixture", "exec"))
from director import COURT, GYM, MAX_ABSENCE, PRESENCE, TRAVEL, TRIP, choose_brock
from play import BROCK_PRESENCE

native, mode, _, _ = setup()
native("FlagSet", 0x829)
native("FlagSet", 0x828)
native("RtcInitLocalTimeOffset", 11, 0)
gba.inject(b"\x23" + struct.pack("<I", (gba.symbols["ScrCmd_givegiftmon"] | 1) + 0x2000000)
           + struct.pack("<BBHHI", 0, 6, 7, 16, 0) + b"\x02")
maps = json.loads((gba.root / "data/maps/map_groups.json").read_text())
mailbox = gba.symbols["gLivingWorldMailbox"]
hint_address = gba.symbols["gLivingWorldFieldHint"]
projection = gba.symbols["gLivingWorldBrockPresence"]
bridge = DialogueBridge(gba.read, gba.write, mailbox, deferred=True)
gba.lib.retro_get_memory_data.restype = c.c_void_p
gba.lib.retro_get_memory_size.restype = c.c_size_t


def warp(name, x, y):
    for group, key in enumerate(maps["group_order"]):
        if name in maps[key]:
            number = maps[key].index(name)
            break
    else:
        raise AssertionError(name)
    gba.inject(b"\x39" + struct.pack("<BBBhh", group, number, 255, x, y) + b"\x27\x6b\x02")
    return group, number


def presence(world):
    hint = FieldHint.decode(gba.read(hint_address, FIELD_SIZE))
    code = PRESENCE[world.location]
    gba.write(projection, BROCK_PRESENCE.pack(b"LWB1", hint.frame, code, code ^ 255))


def spawned(place, local):
    group, number = place
    return native("GetObjectEventIdByLocalIdAndMap", local, number, group) < 16


def talk(director, label, expected=None, *, finish=True):
    invoke_event(label)
    for _ in range(40):
        if gba.read(mailbox, 4) == b"LQW1":
            break
        gba.run(1)
    else:
        raise AssertionError(f"No request from {label}")
    def respond(context):
        message = director.message(context.npc)
        return json.dumps({"action": "SAY_DIALOGUE", "text": message}) if message else SKIP
    trace = bridge.poll(respond)
    assert trace["validation"] == ("accepted" if expected else "skipped"), trace
    if expected:
        assert expected in json.loads(trace["proposal"])["text"], trace
        director.message(trace["context"]["npc"], accepted=True)
        gba.run(30)
    if finish:
        finish_dialogue()
        bridge.poll(lambda _: SKIP)
    return trace


def battery():
    assert native("TrySavingData", 0) == 1
    return c.string_at(gba.lib.retro_get_memory_data(0), gba.lib.retro_get_memory_size(0))


with TemporaryDirectory() as directory:
    path = Path(directory) / "world.sqlite3"
    memory = WorldMemory(path, "pewter-demo", b"test")
    director = memory.director
    gym = warp("PewterCity_Gym", 6, 6)
    assert spawned(gym, 1)
    gba.snap("phase8-brock-home")

    city = warp("PewterCity", 16, 17)
    native("RtcInitLocalTimeOffset", 11, 0)
    if os.environ.get("LIVING_WORLD_PEWTER_FIXTURE"):
        (gba.d / "PewterTest.sav").write_bytes(battery())
        assert native("AddBagItem", 717, 1)
        (gba.d / "PewterSocietyTest.sav").write_bytes(battery())
        # Capture a separate post-Brock demo from the stable Pewter field.
        # Restore the entire pre-badge session before testing Brock's storyline.
        before_demo = c.create_string_buffer(gba.lib.retro_serialize_size())
        assert gba.lib.retro_serialize(before_demo, len(before_demo))
        native("FlagSet", 0x820)
        native("FlagSet", 0x4B0)
        native("SetTrainerFlag", 414)
        assert native("AddBagItem", 715, 1)
        (gba.d / "Phase13Pewter.sav").write_bytes(battery())
        assert gba.lib.retro_unserialize(before_demo, len(before_demo))
    gba.run(65)
    hint = FieldHint.decode(gba.read(hint_address, FIELD_SIZE))
    assert hint.area == "pewter" and hint.story == 0 and hint.local_second is not None, hint
    now = hint.local_second
    director.observe(now, hint.area, bool(hint.story), hint.busy)
    request = director.decision()
    assert request and request.report
    runtime = os.environ.get("LIVING_WORLD_PHASE5_RUNTIME")
    if runtime:
        from inference import LocalModel
        model = LocalModel(Path(runtime), {}, style="qwen3", natural=True)
        try:
            chosen, metrics = choose_brock(model, request)
            assert chosen == TRIP, (chosen, metrics)
            print("Bundled Qwen3 chose the museum plan", metrics)
        finally:
            model.close()
    else:
        chosen = TRIP
    director.submit(request, chosen)
    assert director.location == TRAVEL
    gym = warp("PewterCity_Gym", 7, 11)
    presence(director)
    gba.run(12)
    assert not spawned(gym, 1)
    talk(director, "PewterCity_Gym_EventScript_GymGuy", "Brock told me", finish=False)
    gba.run(40)
    gba.snap("phase8-attendant")
    gba.press(8, 55)
    gba.snap("phase8-objective")
    try:
        finish_dialogue()
    except AssertionError:
        gba.snap("phase8-stuck")
        raise
    bridge.poll(lambda _: SKIP)
    assert director.state["quest"]["status"] == "seeking"

    save = battery()
    memory.checkpoint(save)
    memory.close()
    memory = WorldMemory(path, "pewter-demo", save)
    director = memory.director
    assert director.location == TRAVEL and director.state["quest"]["status"] == "seeking"

    city = warp("PewterCity", 19, 9)
    director.observe(now + 12, "pewter", False)
    assert director.location == COURT
    presence(director)
    gba.run(12)
    assert not spawned(city, 7), "Brock appeared on the player"
    gba.keys.add(5)
    gba.run(30)
    gba.keys.clear()
    gba.run(18)
    presence(director)
    gba.run(24)
    assert spawned(city, 7), "Brock failed to arrive on a cleared tile"
    assert not spawned(gym, 1)
    presence(director)
    gba.snap("phase8-forecourt")
    talk(director, "PewterCity_EventScript_BrockForecourt", "I'll be back", finish=False)
    gba.snap("phase8-contact")
    finish_dialogue()
    bridge.poll(lambda _: SKIP)
    assert director.state["quest"]["status"] == "contacted"

    for _ in range(4):
        director.observe(director.state["active"]["due"], "pewter", False)
    assert director.location == GYM
    presence(director)
    gba.run(12)
    assert not spawned(city, 7)
    gym = warp("PewterCity_Gym", 6, 6)
    assert spawned(gym, 1)
    gba.snap("phase8-returned")
    field_save = c.create_string_buffer(gba.lib.retro_serialize_size())
    assert gba.lib.retro_serialize(field_save, len(field_save))
    talk(director, "PewterCity_Gym_EventScript_Brock", finish=False)
    for _ in range(20):
        gba.press(8, 30)
        flags = struct.unpack("<I", gba.read(gba.symbols["gBattleTypeFlags"], 4))[0]
        if flags & 8:
            break
    else:
        raise AssertionError("Brock's trainer battle did not start")

    # Exercise the exact retail victory continuation with a field fixture
    # rather than simulating a battle win or handing out a test-only badge.
    assert gba.lib.retro_unserialize(field_save, len(field_save))
    gba.run(5)
    invoke_event("PewterCity_Gym_EventScript_DefeatedBrock")
    finish_dialogue()
    assert native("FlagGet", 0x820) and native("FlagGet", 0x4B0)
    assert spawned(gym, 1)
    gba.snap("phase8-badge")
    memory.close()
    print(f"PASS mode {mode}: home, absence, clue, travel checkpoint, collision, contact, original challenge and award continuation")
