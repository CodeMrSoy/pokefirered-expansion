# Havora stage one

Based on V2 commit `563419b86` (Additional start for harbor), fast-forwarded from
Havora-Development `56a44ae16`. Changes belong only on Havora-Development.

## Scope

The 40x32 General/Vermilion harbor now has a dry original ferry landing,
seawalled stone promenade, warehouse facades, market booths, wooden piers and
an eastern breakwater. Its west edge connects outdoors to the east edge of
Havora City with offset zero; the open seam spans y=1..3 at elevation 3.
The city retains its 80x80 dimensions and original town buildings. An eastern
warehouse/market district connects the harbor to the existing town opening.
Previously empty expansion space is blocked and the developed district bounded
by hedges. It is not a completed 80x80 city. Warehouses and booths are exterior
scenery; their interiors and shop interfaces are future work.

All preexisting object events and warp events remain unchanged, including the
Seagallop at (8,9), sailor at (8,6), arrival at (8,5), harbor warp 0 and city
warp 1. The original door-based city/harbor warp remains available as a legacy
entrance; the new primary route is the outdoor east/west connection. Ferry
scripts and seagallop.c are unchanged. New NPCs provide local directions.
No tileset, metatile definition, map group, ferry destination, QOL or V1 changes.

## Native map validation

`python tests/havora_layouts.py` checks dimensions, map buffer capacity,
General/Vermilion compatibility, metatile IDs (<808), event bounds, preservation
of preexisting objects/warps, reciprocal connection offsets, elevation at the
seam, and connected walkable routes from the ferry to the piers and city center.
The renderer `tools/havora/render.py LAYOUT_ID output.png` decodes the actual
metatile and palette assets. Its output is a static tile render, not a Porymap
screenshot, and omits NPCs, time-of-day lighting and animations.

## Verified build and gameplay

Built with ARM GNU 13.2.1 and newlib, standard `make -j8`. In this environment,
DEVKITARM points at the available toolchain and C_INCLUDE_PATH at its
usr/include/newlib directory. Host gbagfx/rsfont required the installed libpng
headers/library and `LIBS='-lpng -lz -lm'`; no build-system changes committed.
ROM linked size: 23,838,728 bytes, 71.04% of the 32 MiB ROM region.

`tests/havora_emulator.py` uses an mGBA libretro core through ctypes. Set
MGBA_CORE and ARM_NM as needed (and LD_LIBRARY_PATH for core dependencies).
It boots a new game, uses a script-injected warp only to set up test locations,
then exercises real directional controls and the unchanged sailor scripts.
Verified:
- Harbor arrival and city district load and render.
- City -> harbor walk crosses into map (43,19).
- Harbor -> city walk crosses into map (43,0).
- Havora sailor yes prompt and ferry scene arrive in Vermilion at (23,32).
- Adding a Stellar Ticket as test fixture and speaking to the original
  Vermilion sailor returns to Havora (43,19), exactly (8,5).
Screenshots are generated in build/havora-tests.

No Porymap UI testing was performed. Tests do not cover every decorative edge,
Surf, bicycle behavior, every older Quantum map, or a full story playthrough.
