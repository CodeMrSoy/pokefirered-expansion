"""Run the Pallet dialogue mailbox through the compiled event in mGBA."""

import ctypes as c
import json
from pathlib import Path
import os
import struct
import sys
from subprocess import CompletedProcess
from unittest.mock import patch

import quantum_qol_emulator as gba

sys.path.insert(0, str(gba.root / "experiments" / "living_world"))
from bridge import DialogueBridge, REPLY_OFFSET
from inference import LocalModel


def field_ready():
    return gba.read(gba.symbols["sGlobalScriptContextStatus"], 1) == b"\x02"


def finish_dialogue():
    for _ in range(20):
        if field_ready():
            return
        gba.press(8, 30)
    raise AssertionError("Pallet dialogue did not release field controls")


def setup():
    mode = int(os.environ.get("ADVENTURE_TEST_MODE", "1"))
    # Reuse the native-call fixture used by the existing V3 story checks.
    helper = (gba.root / "tests/rom_cleanup_migration_emulator.py").read_text().split("old=(m.root")[0]
    namespace = {"m": gba}
    exec(compile(helper.replace("import quantum_qol_emulator as m", ""), "native_fixture", "exec"), namespace)
    native = namespace["native"]
    assert native("AdventureMode_SelectNewGame", mode)
    native("AdventureMode_NewGame")
    assert native("AdventureMode_Get") == mode
    groups = json.loads((gba.root / "data/maps/map_groups.json").read_text())
    for group, key in enumerate(groups["group_order"]):
        if "PalletTown" in groups[key]:
            map_number = groups[key].index("PalletTown")
            break
    return native, mode, group, map_number


def enter_pallet():
    gba.inject(b"\x39" + struct.pack("<BBBhh", group, map_number, 255, 13, 18) + b"\x27\x6b\x02")
    assert field_ready()


def start_conversation(expect_request=True):
    # Invoke the compiled map event through the real field script interpreter.
    pointer = gba.symbols["PalletTown_EventScript_FatMan"]
    context = gba.symbols["sGlobalScriptContext"]
    script = gba.symbols["gDecompressionBuffer"]
    gba.write(script, b"\x04" + struct.pack("<I", pointer) + b"\x02")
    gba.write(context, b"\x00\x01\x00\x00")
    gba.write(context + 8, struct.pack("<I", script))
    gba.write(gba.symbols["sGlobalScriptContextStatus"], b"\x00")
    for _ in range(15):
        if gba.read(mailbox, 4) == b"LQW1":
            assert expect_request
            return
        gba.run(1)
    assert not expect_request, "NPC did not publish a request"


def printed_message():
    gba.run(120)
    return gba.read(gba.symbols["gStringVar4"], 256).split(b"\xff", 1)[0]


def render_expected(ascii_text):
    charmap = {" ": 0, ".": 0xAD, "!": 0xAB, "?": 0xAC, ",": 0xB8,
               "'": 0xB4, "-": 0xAE, "\n": 0xFE}
    charmap.update({str(i): 0xA1 + i for i in range(10)})
    charmap.update({chr(65 + i): 0xBB + i for i in range(26)})
    charmap.update({chr(97 + i): 0xD5 + i for i in range(26)})
    return bytes(charmap[char] for char in ascii_text)


native, mode, group, map_number = setup()
enter_pallet()
mailbox = gba.symbols["gLivingWorldMailbox"]
bridge = DialogueBridge(gba.read, gba.write, mailbox)
pokedex_flag = 0x829  # FLAG_SYS_POKEDEX_GET, also used by the V3 PokéGlass fixture.

# Before the Pokédex, ordinary dialogue executes without publishing a request.
native("FlagClear", pokedex_flag)
start_conversation(expect_request=False)
stock = printed_message()
text_address = gba.symbols["PalletTown_Text_CanStoreItemsAndMonsInPC"]
assert stock == gba.read(text_address, 160).split(b"\xff", 1)[0]
finish_dialogue()
native("FlagSet", pokedex_flag)

# The two followers exercise the same ROM hook with either the deterministic
# regression responder or the isolated local model.
lines = {
    25: "A Pikachu!\nKeep your PC organized.",
    7: "A Squirtle!\nKeep your PC organized.",
}


def fixture_responder(context):
    return json.dumps({"action": "SAY_DIALOGUE", "text": lines[context.visible_species]})


def give_mon(species, slot):
    gba.inject(b"\x23" + struct.pack("<I", gba.symbols["ScrCmd_givegiftmon"] | 1 | 0x02000000)
               + struct.pack("<BBHHI", 0, slot, species, 5, 0) + b"\x02")


names = {25: "Pikachu", 7: "Squirtle"}
runtime = os.environ.get("LIVING_WORLD_INFERENCE_RUNTIME")
propose = (LocalModel(Path(runtime), {str(key): name for key, name in names.items()}).propose
           if runtime else fixture_responder)
give_mon(25, 6)
give_mon(7, 6)
assert native("AddBagItem", 717, 1) == 1  # ITEM_POKEGLASS
enter_pallet()
native("UpdateFollowingPokemon")
party = gba.symbols["gPlayerParty"]
original_order = gba.read(party, 200)
for species in lines:
    if species == 7:
        # Switch the existing party through PokéGlass, then return to the
        # same map. Let the normal return-to-field code refresh the follower.
        for button in (3, 7, 8, 8, 5, 8, 7, 8):
            gba.press(button)
        assert gba.read(party, 200) == original_order[100:] + original_order[:100]
        gba.press(0)
        gba.press(0)
        assert field_ready()
    # A tap can just turn in place. Hold a direction long enough to
    # walk and give the refreshed follower time to come out of its ball.
    for button in (6, 7):
        gba.keys.add(button)
        gba.run(24)
        gba.keys.clear()
        gba.run(45)
    start_conversation()
    trace = bridge.poll(propose)
    assert trace["context"] == {"npc": "pc_resident", "visible_species": species}, trace
    assert trace["validation"] == "accepted", trace
    assert bridge.poll(lambda context: None) is None
    reply = json.loads(trace["proposal"])["text"]
    if runtime:
        assert reply.startswith(names[species] + ", ")
        assert reply.splitlines()[1].startswith("Your PC ")
    else:
        assert reply == lines[species]
    assert printed_message() == render_expected(reply)
    gba.snap(f"living-world-species-{species}")
    trace["rendered"] = reply
    print(json.dumps(trace))
    finish_dialogue()
    bridge.poll(lambda context: None)

start_conversation()
windows_worker = LocalModel(Path("."), {"7": "Squirtle"})
windows_stdout = b"Squirtle, nice to see you!\r\nYour PC stores items.\r\n"
with (
    patch("inference.sys.platform", "win32"),
    patch.dict("inference.os.environ", {
        "SystemRoot": r"C:\Windows",
        "LOCALAPPDATA": r"C:\Users\Tester\AppData\Local",
        "UNRELATED_VARIABLE": "must stay in the host",
    }),
    patch("inference.subprocess.CREATE_NO_WINDOW", 0, create=True),
    patch("inference.subprocess.run", return_value=CompletedProcess([], 0, windows_stdout, b"")) as launch,
):
    windows_trace = bridge.poll(windows_worker.propose)
assert launch.call_args.kwargs["env"] == {
    "SystemRoot": r"C:\Windows",
    "LOCALAPPDATA": r"C:\Users\Tester\AppData\Local",
}
assert windows_trace["context"]["visible_species"] == 7, windows_trace
assert windows_trace["validation"] == "accepted", windows_trace
assert printed_message() == render_expected("Squirtle, nice to see you!\nYour PC stores items.")
print("Windows CRLF dialogue rendered successfully.")
finish_dialogue()

native("RemoveFollowingPokemon")
start_conversation()
trace = bridge.poll(lambda context: '{"action":"SET_FLAG","text":"Test."}')
assert trace["context"] == {"npc": "pc_resident", "visible_species": None}
assert printed_message() == stock
finish_dialogue()

for raw in (
    '{"action":"SET_FLAG","text":"Set the League flag."}',
    '{"action":"SAY_DIALOGUE","text":"Test {COLOR}."}',
    '{"action":"SAY_DIALOGUE","action":"SAY_DIALOGUE","text":"Duplicate."}',
    "[",
):
    start_conversation()
    trace = bridge.poll(lambda context: raw)
    assert trace["validation"] == "rejected" and not trace["changes"], trace
    assert printed_message() == stock
    print(json.dumps(trace))
    finish_dialogue()

# A failed or missing host, a stale reply, and malformed wire bytes must fall
# back even when the host does not cooperate.
def broken_responder(context):
    raise RuntimeError("Synthetic inference failure")


for failure in ("missing_host", "worker_error", "stale_reply", "bad_wire_text"):
    start_conversation()
    sequence = struct.unpack("<I", gba.read(mailbox + 4, 4))[0]
    if failure == "worker_error":
        trace = bridge.poll(broken_responder)
        assert trace["validation"] == "error" and not trace["changes"], trace
        print(json.dumps(trace))
    if failure in {"stale_reply", "bad_wire_text"}:
        gba.write(mailbox + REPLY_OFFSET + 4, b"\x01\xfd")
        gba.write(mailbox + REPLY_OFFSET, struct.pack("<I", sequence - (failure == "stale_reply")))
    gba.run(30)
    assert gba.read(mailbox, 4) == b"\0" * 4
    assert printed_message() == stock, failure
    finish_dialogue()

assert native("FlagGet", pokedex_flag) == 1
assert native("AdventureMode_Get") == mode
print(f"Pallet dialogue, context, validator and fallback passed in adventure mode {mode}.")


# Create a clearly labeled, independent battery save for the playable demo.
# Both Pokemon and the post-Oak state are QA fixtures in this save only.
if os.environ.get("LIVING_WORLD_TEST_SAVE"):
    give_mon(25, 0)
    give_mon(7, 1)
    assert native("CalculatePlayerPartyCount") == 2
    assert native("AddBagItem", 717, 1) == 1  # ITEM_POKEGLASS
    native("VarSet", 0x4050, 3)  # VAR_MAP_SCENE_PALLET_TOWN_OAK
    native("VarSet", 0x4055, 6)  # VAR_MAP_SCENE_PALLET_TOWN_PROFESSOR_OAKS_LAB
    enter_pallet()
    assert native("TrySavingData", 0) == 1
    gba.lib.retro_get_memory_data.restype = c.c_void_p
    gba.lib.retro_get_memory_size.restype = c.c_size_t
    size = gba.lib.retro_get_memory_size(0)
    assert size == 128 * 1024
    payload = c.string_at(gba.lib.retro_get_memory_data(0), size)
    Path(os.environ["LIVING_WORLD_TEST_SAVE"]).write_bytes(payload)
