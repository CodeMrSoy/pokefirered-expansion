"""Exercise the pilot through compiled Route 3 and Museum scripts in mGBA."""

import json
import struct
from pathlib import Path
from tempfile import TemporaryDirectory

import quantum_qol_emulator as gba

support = (gba.root / "tests/living_world_bridge_emulator.py").read_text().split(
    "native, mode, group, map_number = setup()")[0]
exec(compile(support, "native fixture", "exec"))

from autonomy import DESK, MUSEUM, OFFER, REPORT, SCOUTS


def warp(name, x, y):
    for group, key in enumerate(maps["group_order"]):
        if name in maps[key]:
            number = maps[key].index(name)
            gba.inject(b"\x39" + struct.pack("<BBBhh", group, number, 255, x, y) + b"\x27\x6b\x02")
            assert field_ready()
            return
    raise AssertionError(name)


def converse(label):
    seen = {}
    token = None

    def propose(context):
        nonlocal token
        text, token = pilot.reply(context.npc)
        if text is None:
            return SKIP
        seen[context.npc] = text
        return json.dumps({"action": "SAY_DIALOGUE", "text": text})

    invoke_event(label)
    try:
        for frame in range(1100):
            trace = bridge.poll(propose)
            if trace and trace["validation"] == "accepted":
                pilot.accept(token)
            if frame > 1 and field_ready():
                return seen
            if frame % 10 == 0:
                gba.keys.add(8)
            else:
                gba.keys.discard(8)
            gba.run(1)
    finally:
        gba.keys.discard(8)
    raise AssertionError(f"Script did not release controls: {label}")


native, mode, _, _ = setup()
native("FlagSet", 0x829)
maps = json.loads((gba.root / "data/maps/map_groups.json").read_bytes())
mailbox = gba.symbols["gLivingWorldMailbox"]
hint_address = gba.symbols["gLivingWorldFieldHint"]
bridge = DialogueBridge(gba.read, gba.write, mailbox, deferred=True)

with TemporaryDirectory() as folder:
    db = Path(folder) / "scenario.sqlite3"
    memory = WorldMemory(db, "phase13-test", b"before")
    pilot = memory.autonomy
    warp("PewterCity", 18, 16)
    assert not FieldHint.decode(gba.read(hint_address, FIELD_SIZE)).early_kanto_open
    assert pilot.reply(DESK) == (None, None)
    native("FlagSet", 0x820)  # Fixture represents Brock's badge, read from the actual ROM hint.
    warp("Route3", 4, 9)
    hint = FieldHint.decode(gba.read(hint_address, FIELD_SIZE))
    assert hint.early_kanto_open and hint.area == "route_3"
    pilot.advance(1000, hint.early_kanto_open)
    pilot.advance(1025, hint.early_kanto_open)
    ticket = pilot.decision()
    plan = next(option for option in ticket.options if option.startswith("route_3:") and option.endswith(":local"))
    assert pilot.submit(ticket, plan, "fallback")
    pilot.advance(1035, True)
    assert pilot.submit(pilot.decision(), "inspect", "fallback")
    assert pilot.reply(SCOUTS["mt_moon"]) == (None, None)
    scene = converse("Route3_EventScript_Youngster")
    assert "Report to Pewter Museum." in scene[SCOUTS["route_3"]]
    assert pilot.state["event"]["player"] == "witnessed"
    warp("PewterCity_Museum_1F", 5, 6)
    report = converse("PewterCity_Museum_1F_EventScript_LivingAssistant")
    assert OFFER in report and REPORT in report, report
    assert pilot.state["event"]["player"] == "reported"
    assert pilot.state["event"]["knowledge"][MUSEUM]["source"] == SCOUTS["route_3"]
    pilot.advance(1500, True)
    assert pilot.state["history"][0]["result"] == "verified"
    memory.checkpoint(b"after")
    memory.close()
    memory = WorldMemory(db, "phase13-test", b"after")
    pilot = memory.autonomy
    assert "The accounts matched." in converse("PewterCity_Museum_1F_EventScript_LivingAssistant")[DESK]
    assert OFFER not in converse("PewterCity_Museum_1F_EventScript_LivingAssistant")
    memory.close()
print(f"PASS mode {mode}: badge-gated inquiry, attributed field dialogue, Museum Yes report, verified history after reload")
