"""ROM geometry, regional itinerary and three exclusive slot families."""
import quantum_qol_emulator as gba

support = (gba.root / "tests/living_world_travel_emulator.py").read_text().split("pewter = ")[0]
exec(compile(support, "regional fixture", "exec"))
from collections import deque
from planning import Proposal
from region import RESEARCHER_PRESENCE, route
from society import Step

assert route("researcher", "museum", "route_2") == (("pewter", "route_2"), 28)
assert route("trainer", "pewter", "museum") is None
assert route("researcher", "pewter", "mt_moon") is None
layouts = {x["id"]: x for x in json.loads((gba.root / "data/layouts/layouts.json").read_text())["layouts"]}

def reachable(name, start, end):
    map_data = json.loads((gba.root / f"data/maps/{name}/map.json").read_text())
    layout = layouts[map_data["layout"]]
    width, height = layout["width"], layout["height"]
    tiles = (gba.root / layout["blockdata_filepath"]).read_bytes()
    queue, seen = deque([start]), {start}
    while queue:
        x, y = queue.popleft()
        if (x, y) == end:
            return True
        for nx, ny in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
            if not (0 <= nx < width and 0 <= ny < height) or (nx, ny) in seen:
                continue
            if struct.unpack_from("<H", tiles, 2*(width*ny+nx))[0] >> 10 != 12:
                continue
            seen.add((nx, ny))
            queue.append((nx, ny))
    return False

assert reachable("PewterCity_Museum_1F", (2,4), (14,9))
assert reachable("PewterCity", (17,6), (21,39))
assert reachable("Route2", (9,0), (9,6))

museum = warp("PewterCity_Museum_1F", 2, 5)
assert spawned(museum, 2)
memory = WorldMemory(":memory:", "region", b"walk")
society = memory.society
now = 11*3600
society.tick(now, "pewter")
society.tick(now, "viridian")
ticket = society.decision("researcher")
steps = (Step("TRAVEL_TO", "route_2"), Step("INVESTIGATE", "tracks"),
         Step("RETURN_TO_DUTY", "museum"))
society.submit(ticket, Proposal("verify_observation", steps, society.primitives(ticket)))
researcher = society.state["agents"]["researcher"]

def publish():
    hint = FieldHint.decode(gba.read(hint_address, FIELD_SIZE))
    code = RESEARCHER_PRESENCE[researcher["location"]]
    gba.write(gba.symbols["gLivingWorldResearcherPresence"],
              BROCK_PRESENCE.pack(b"LWR1", hint.frame, code, code ^ 255))

publish()
gba.run(16)
assert not spawned(museum, 2)
assert researcher["active"]["journey"]["legs"] == ("pewter", "route_2")
society.tick(now+28, "viridian")
road = warp("Route2", 9,7)
publish()
gba.run(16)
assert spawned(road,9)
assert not spawned(museum,2)
# Give the sprite a field movement update before starting its real dialogue.
gba.press(4, 24)
publish()
gba.run(16)
invoke_event("Route2_EventScript_Volunteer")
for _ in range(30):
    gba.run(1)
    if gba.read(mailbox, 4) == b"LQW1":
        break
else:
    raise AssertionError("Route 2 volunteer did not start the exchange")
assert bridge.poll(lambda _: SKIP)["validation"] == "skipped"
gba.run(30)
assert not field_ready()
society.tick(now+60, "viridian")
assert researcher["facts"]["tracks"]["kind"] == "firsthand"
assert researcher["location"] == "in_transit"
publish()
gba.run(110)
assert not field_ready()
obj = gba.read(gba.symbols["gObjectEvents"], 16 * 36)
assert any(obj[i] & 1 and obj[i + 8] == 9 for i in range(0, len(obj), 36))
gba.snap("phase11-route2-volunteer-during-departure")
finish_dialogue()
publish()
gba.run(16)
assert spawned(road, 9), "Route 2 volunteer vanished in the player's view"
# Re-enter the map beyond the old sprite's camera bounds, then return
# to the survey spot while the volunteer is still travelling.
warp("PewterCity", 21, 37)
assert not spawned(road, 9), "Route 2 object survived the map transition"
warp("Route2", 9, 7)
publish()
gba.run(24)
assert not spawned(road, 9), "Departed volunteer respawned on Route 2"
society.tick(now+88,"viridian")
assert researcher["location"] == "museum"
museum = warp("PewterCity_Museum_1F",2,5)
publish()
gba.run(16)
assert spawned(museum,2)
assert not spawned(road,9)
memory.close()
print(f"PASS mode {mode}: verified connected geometry and multi-leg volunteer travel")
