# Havora connection review

Reviewed source: `194e346bb12bc601968b726bd29eaa5a23e8c71d` (Havora city Update).

## Corrected

- Western city ↔ North District: reciprocal offsets +6 / -6 account for the
  western city's reduction to 42 columns. Other map origins stay fixed.
- Daycare ↔ coastal cliffs: reciprocal horizontal offsets +1 / -1 account for
  the North Quay becoming 41 columns wide. All placement loops now agree.
- New coastal-cliffs map: matching city type, weather, music, region section,
  running and cycling settings replace the new-map defaults.
- Three out-of-bounds NPCs have safe land positions. Three additional NPCs
  painted over by water/stalls have adjacent land positions; one stale elevation
  was aligned with its ground.
- Shipwright and Trader house warps follow the actual door one column east;
  their repainted doors now have passable collision. The Daycare warp follows
  its moved door at (22,14). Warp array indices and all interior return IDs stay
  stable.
- Two walkway joins had incompatible elevations: four western-city edge cells
  and four North Quay stair-landing cells now use transition elevation zero.
- Daycare's continuous grass retained old mixed elevation 5/6 after its former
  divider was painted away. 429 non-cliff land cells now match the elevation-5
  approach; NPC and door elevations match. Every cliff cell is preserved.
- Map/border byte lengths, border references, map-buffer capacity, events,
  incoming/outgoing warp indices, and shared tilesets pass validation.

All eight maps retain every original metatile graphic reference. All 1,421
native cliff/corner cells retain their full collision and elevation words too.
No tileset art, dimensions, border files, Harbor map data or ferry scripts changed.

## Still needs authoring

Three western interiors have no visible matching building entrance after the
latest edits: WestHouse1, CliffHouse5, and HarborInn. They remain in the project,
with safe return landings and stable warp IDs. No invisible entrance was added.
The old inn return landing was moved off blocked water onto the western quay.

The coastal-cliffs extension is scenic terrain with no foot route. Its map
connections align visually; this review does not invent stairs or a coastal path.

## Validation

`python tools/havora/audit_connections.py` checks the current files and emits
`connection-audit.json`. Eight outdoor maps, eleven reciprocal connection pairs,
and all twenty-two visible entrances pass. Static four-direction foot-route
checks reach the Gym, Center, Mart, Daycare and visible houses/shops from the
ferry sailor. These checks ignore NPC occupancy and scripted movement.

The ROM compiles successfully. Porymap UI testing and in-game walking/ferry
verification were not performed in this review. The updated connected image is
rendered from current map data and actual offsets with NPC sprites.
