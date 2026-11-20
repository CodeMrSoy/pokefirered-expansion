"""Run the Pallet dialogue mailbox through the compiled event in mGBA."""

import json
import os
import struct
import sys

import quantum_qol_emulator as gba

sys.path.insert(0, str(gba.root / "experiments" / "living_world"))
from bridge import DialogueBridge, REPLY_OFFSET


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
    charmap = {" ": 0, ".": 0xAD, "!": 0xAB, "\n": 0xFE}
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

# The same NPC sees a different follower on a second visit. Synthetic output
# exercises the production validator while keeping the regression deterministic.
lines = {
    25: "A Pikachu!\nKeep your PC organized.",
    7: "A Squirtle!\nKeep your PC organized.",
}


def fixture_responder(context):
    return json.dumps({"action": "SAY_DIALOGUE", "text": lines[context.visible_species]})


for species, reply in lines.items():
    gba.inject(b"\x23" + struct.pack("<I", gba.symbols["ScrCmd_givegiftmon"] | 1 | 0x02000000)
               + struct.pack("<BBHHI", 0, 0, species, 5, 0) + b"\x02")
    enter_pallet()
    native("UpdateFollowingPokemon")
    gba.press(5, 45)
    gba.press(4, 45)
    start_conversation()
    trace = bridge.poll(fixture_responder)
    assert trace["context"] == {"npc": "pc_resident", "visible_species": species}, trace
    assert trace["validation"] == "accepted", trace
    assert bridge.poll(lambda context: None) is None
    assert printed_message() == render_expected(reply)
    gba.snap(f"living-world-species-{species}")
    trace["rendered"] = reply
    print(json.dumps(trace))
    finish_dialogue()
    bridge.poll(lambda context: None)

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
