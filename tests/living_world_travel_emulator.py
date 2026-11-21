"""Validate the Route 2 projection, collision and offscreen planning with mGBA."""
import struct
import quantum_qol_emulator as gba

support = (gba.root / "tests/living_world_brock_emulator.py").read_text().split("with TemporaryDirectory()")[0]
exec(compile(support, "Pewter travel fixture", "exec"))
from society import TRAINER_PRESENCE

pewter = json.loads((gba.root / "data/maps/PewterCity/map.json").read_text())
route_data = json.loads((gba.root / "data/maps/Route2/map.json").read_text())
assert any(link["map"] == "MAP_ROUTE2" and link["direction"] == "down" for link in pewter["connections"])
assert any(link["map"] == "MAP_PEWTER_CITY" and link["direction"] == "up" for link in route_data["connections"])
terrain = (gba.root / "data/layouts/Route2/map.bin").read_bytes()
walkable = lambda x, y: struct.unpack_from("<H", terrain, 2 * (24 * y + x))[0] >> 10 == 12
# Open north path from the direct map connection, with no warp or Cut requirement.
assert all(walkable(8, y) for y in range(7)) and walkable(7, 6)
assert not any(event["x"] == 7 and event["y"] == 6 for event in route_data["warp_events"])

city = warp("PewterCity", 33, 28)
assert spawned(city, 4)
gba.snap("phase9-trainer-home")
memory = WorldMemory(":memory:", "travel", b"start")
society = memory.society
now = 11 * 3600
society.tick(now, "pewter")
society.tick(now, "viridian")
ticket = society.decision("trainer")
trip = next(plan for plan in ticket.choices if plan[0].action == "TRAVEL_TO")
society.submit(ticket, trip)
trainer = society.state["agents"]["trainer"]
assert trainer["location"] == "in_transit"
trainer_projection = gba.symbols["gLivingWorldTrainerPresence"]

def publish_trainer():
    hint = FieldHint.decode(gba.read(hint_address, FIELD_SIZE))
    code = TRAINER_PRESENCE[trainer["location"]]
    gba.write(trainer_projection, BROCK_PRESENCE.pack(b"LWS1", hint.frame, code, 255 ^ code))

publish_trainer()
gba.run(12)
assert not spawned(city, 4)
gba.snap("phase9-trainer-away")
society.tick(now + 16, "viridian")
assert trainer["location"] == "route_2"
route = warp("Route2", 7, 6)
publish_trainer()
gba.run(12)
assert not spawned(route, 8), "NPC appeared on the occupied arrival tile"
gba.keys.add(5)
gba.run(28)
gba.keys.clear()
gba.run(18)
publish_trainer()
gba.run(24)
assert spawned(route, 8), "Trainer failed to appear after the arrival tile cleared"
assert not spawned(city, 4)
gba.snap("phase9-trainer-route2")
society.tick(now + 44, "viridian")
assert trainer["location"] == "in_transit"
society.tick(now + 60, "viridian")
assert trainer["location"] == "pewter"
publish_trainer()
gba.run(12)
assert not spawned(route, 8)
city = warp("PewterCity", 33, 28)
assert spawned(city, 4)
memory.close()
print(f"PASS mode {mode}: trainer departed, arrived without collision, and returned")
