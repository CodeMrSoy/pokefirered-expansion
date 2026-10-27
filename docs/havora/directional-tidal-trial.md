# Directional boat-and-dam trial

Current player travel is continuous boat sailing. There is no warp in the travel
script: board, sail the actual water footprint, and disembark at the fixed partner.
The camera follows the passenger; the sail-less launch turns with the route.
Only the optional emergency reset retains its explicit return-to-entrance warp.

## Existing circled dams

The user's annotated `gatees.png` identifies the existing submerged crossings.
No new opening is cut into the authored map. Only the dam stems at columns 27
and 54 are covered with water when their condition is met. A's gate is four tiles
tall (rows 22–25); B/C retains rows 21–25. A's face is also visually covered
whenever A is HIGH, but unequal A/B water still prevents sailing.

| Dam | Covered / boat-passable | Closed |
| --- | --- | --- |
| Green A/B | A MID + B MID, or A HIGH + B HIGH | LOW or unequal A/B levels |
| Blue B/C | B HIGH + C HIGH | Every other combination |

The three-by-three hull footprint is checked on actual runtime tiles. A closed
dam cannot be bypassed by a scripted straight line. Filling and draining restore
the corresponding water or original dam art in all 27 combinations.

All four switch effects change A/B/C simultaneously, modulo three:

| Color | A | B | C |
| --- | --- | --- | --- |
| Green | +1 | -1 | -1 |
| Red | -1 | 0 | +1 |
| Yellow | 0 | +1 | 0 |
| Blue | +1 | +1 | -1 |

A+C is invariant modulo three. From all LOW, all HIGH is unreachable, so a single
trip crossing BOTH dams would be impossible. The earlier AL1→CR2 example is
therefore replaced with adjacent-section partners and intermediate stops.

## Fixed one-way boat partners

| Outbound | Inbound partner | Required condition |
| --- | --- | --- |
| AL1 | AR2 | Same A pool; exposed berths |
| AR3 | BL3 | A MID and B MID; green dam submerged |
| BL3 | Island LEFT | B MID |
| BL1 | BR2 | B HIGH; B-only crossing |
| Island RIGHT | AR3 | A MID and B MID; green dam submerged |
| BR1 | CR2 | B HIGH and C HIGH; blue dam submerged |
| CR1 | CL2 | Same C pool; exposed berths |
| CL1 | BL2 | B HIGH and C HIGH; blue dam submerged |
| AR1 | AL2 | Same A pool; all crews defeated (optional return) |

Inbound berths never reverse a route. Source/destination coordinates and route
rules are in `tools/havora/tidal_trial.json`. The actual water path is searched
at departure; a blocked route returns an error before boarding begins.

The switch colors vary by station, so the player must read each panel instead
of repeating the same choice at every quay. Quay switches are listed top to
bottom; island switches are listed left to right.

| Station | Switch colors |
| --- | --- |
| A Left | Yellow / Yellow / Red |
| A Right | Blue / Red / Blue |
| B Left | Green / Blue / Blue |
| B Right | Yellow / Green / Yellow |
| C Left | Green / Red / Green |
| C Right | Yellow / Yellow / Red |
| Switch island | Blue / Green / Green |

Operations that would submerge the player on the island at B HIGH are refused.
The safe island sequence is GREEN to lower B, then BLUE to raise it to MID.
Cached object elevations update with the tide so the player can walk between
levers.

## Mandatory crews and solution

Trainers face left/right, spot the player, walk toward them and initiate doubles.
Each station's switches and outbound boat require its crew victory, and the boat
also requires at least one successful local switch use. Eirik checks all seven
crew victories and seven switch stations, C LOW, and six conscious party members.
C's original foot crossing remains LOW-only and leads into the exposed bunker.

One shortest 30-action solution (walking steps and leader combat excluded):

1. A Left crew; top YELLOW, bottom RED; boat AL1 → AR2.
2. A Right crew; bottom RED; boat AR3 → BL3 at MID/MID.
3. B Left crew; top GREEN twice, middle BLUE twice; boat BL3 → island LEFT at B MID.
4. Island crew; middle GREEN, then left BLUE; sail island RIGHT → AR3 at A/B MID.
5. Return AR3 → BL3; top GREEN twice sets A LOW / B HIGH / C LOW. Sail BL1 → BR2, defeat B Right, use top YELLOW and middle GREEN.
6. Boat BR1 → CR2 at B/C HIGH; defeat C Right and use top YELLOW.
7. Boat CR1 → CL2; defeat C Left and use middle RED. C is LOW; walk to Eirik's bunker.

Gauge panels retain the optional emergency drain/return reset and preserve earned
progress. Normal boat travel never calls a warp or changes the map destination.

## Validation

- `havora_directional_trial.py`: solves the rules with physical water routing;
  every crew and switch station is required before Eirik.
- `havora_boat_routes.py`: all 27 dam profiles, correct exposed/covered behavior,
  actual three-by-three hull connectivity, and no warp in the travel script.
- `havora_boat_emulator.py`: full native solution, continuous player movement,
  visible sailing phases, unchanged save-block address across trips (no map warp),
  correct arrival berths, and rejection of exposed/mismatched dam crossings.
- `havora_section_water.py`, `havora_artwork_assets.py`: original tilesets,
  authored all-LOW map, MID landings, island and bunker behavior remain intact.

`review/water-dam-boats.gif` shows native sailing through both dam crossings.
The earlier recipe-based tests and earlier MP4 describe retired revisions.
