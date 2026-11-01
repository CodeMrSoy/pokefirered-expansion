# Vidra region map

Run `python3 tools/quantum_region/generate.py` from the repository root.
Install `tools/quantum_region/requirements.txt` when needed.

The generator uses the original FireRed map palette, striped ocean, red/gold
city tile. Routes use the same broad gold bands and terrain uses crisp stepped
contours. The original 320 atlas tiles remain byte-for-byte
intact. The combined atlas is 502 tiles (16,064 bytes), within BG0's 512-tile
allocation. There is no extra runtime palette or map heap allocation.

The five city positions and eight route hit maps retain their campaign section
IDs and coordinates. Planned, unregistered cave markers are omitted. The picker
has exactly two entries: Kanto and Vidra. UI row 1 translates to retained native
page ID 2; page IDs 1 and 3 have no map data or icons.

The shared code conditionally enables Vidra when the snapshot supplies
QUANTUM_MAPSEC_START. The region picker stays hidden until FLAG_QUANTUM_ARRIVED
is set, or the player is already physically in Vidra (including a legacy save).
Legacy Sevii flags cannot unlock it. Both Town Map and Fly use this gate.
PokéGlass's map omits navigation instructions while retaining its city names,
map cursor and region/cancel buttons. The generator does not add campaign maps,
story events or section IDs, and preserves authored metadata and UTF-8 names.
Existing campaign names are preserved during regeneration: Havora City,
Corvala Town, Eldervale Village, Myrdal City and Iskora Village.

Use `tests/region_map_destinations_emulator.py` on QOL and the V2 integration
build to exercise real F.I. Case/Sky Whistle entry, all city markers, locked
travel, independent Center unlocks, completed flights, picker and cancel cleanup.
