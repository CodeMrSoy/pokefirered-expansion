# Vidra region map

Run `python3 tools/quantum_region/generate.py` from the repository root.
Install `tools/quantum_region/requirements.txt` when needed.

The generator uses the original FireRed map palette, striped ocean, red/gold
city tile and native controls. The original 320 atlas tiles remain byte-for-byte
intact. The combined atlas is 510 tiles (16,320 bytes), within BG0's 512-tile
allocation. There is no extra runtime palette or map heap allocation.

The five city positions and eight route hit maps retain their campaign section
IDs and coordinates. Planned, unregistered cave markers are omitted. The picker
has exactly two entries: Kanto and Vidra. UI row 1 translates to retained native
page ID 2; page IDs 1 and 3 have no map data or icons.

QOL has no island campaign maps or section IDs. It carries the conditional
shared map code and assets, with only Kanto enabled. Merging with V2 or
Havora-Development enables Vidra automatically through QUANTUM_MAPSEC_START.
No campaign items, progression flags, maps or story are imported into QOL.
Existing campaign names are preserved during regeneration: Havora City is
confirmed; the other four settlements still have descriptive labels.

Use `tests/region_map_destinations_emulator.py` on QOL and the V2 integration
build to exercise real F.I. Case/Sky Whistle entry, all city markers, locked
travel, independent Center unlocks, completed flights, picker and cancel cleanup.
