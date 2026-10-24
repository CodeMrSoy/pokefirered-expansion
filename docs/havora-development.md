# Havora Harbor — approved Emerald hybrid

Havora Harbor now implements the approved dark Pacifidlog / Slateport / Lilycove
study as native FireRed map blocks. The 40×32 harbor keeps its original outdoor
map headers, ferry objects, sailor scripts and seamless city connections.

- Pacifidlog floating platform tiles supply timber boards, rounded sides and feet.
  Five timber colors are recolored to weathered brown; geometry stays native.
- Slateport supplies masonry quays, paving, green-roof warehouse, sailboats,
  planters, sea rocks and its original 32×64 white lighthouse.
- Lilycove supplies 64×64 blue-roof houses.
- The native Havora crane is retained. Lanterns, barrels and cargo boxes are removed.

## Editing in Porymap

See [havora-porymap-guide.md](havora-porymap-guide.md) for every metatile ID,
collision recommendations and protected ferry coordinates. Imported building
parts are reusable metatiles, not a single flattened scene. Source cutouts and
attribution are committed under `tools/havora/source_art/emerald_harbor`.

The map uses `gTileset_HavoraPrimary` + `gTileset_HavoraHarbor`. Both connected
approaches use the same pair. General graphics needed when scrolling into the
older city, plus every General animation destination, remain reserved. Palette
banks 0, 1 and 6 remain byte-compatible with General.

The expanded catalog contains 501 source metatile entries, including every selected
Pacifidlog platform/wood edge and both rope bridge directions; Lilycove exterior
walls, roofs, windows, larger facades, stairs, plazas and paths; and Slateport market
stalls, umbrellas, display goods, boats, docks and lighthouse pieces. The author's Porymap layout from be19b764 is retained, with additional coastal details
applied to 44 blocks. Three market stalls occupy the west quay.

Duplicate metatiles and mirrored 8×8 graphics are shared. The final set has 526
custom metatiles: all 384 secondary slots plus 142 unused primary slots. Original
primary blocks 5, 0x1C1 and 0x1D9 remain intact for city compatibility. There are
925 custom graphics plus 83 reserved General graphics. The 128-slot animation
range contains 120 active graphics and 8 padding slots. In total 1,016 of the
1,024 graphics slots are allocated, leaving 8 free; all 13 palette banks are used.
Additional metatiles can still combine existing graphics without adding artwork.

Extra imported pieces share the harbor's material palettes, with close-color
substitutions when all original town palettes cannot fit. Their pixel geometry
is preserved. Added catalog pieces generally use one palette per 8×8 patch to
avoid wasting a second graphics layer. Original placed art retains its material
colors, except the sea now uses genuine Emerald animation frames.

## Animated water

`InitTilesetAnim_HavoraHarbor` updates a dedicated 128-tile range at tile 896 every
16 frames through the engine DMA queue. Eight source phases animate exposed sea
pixels in ocean blocks, dock feet, rocks and boat surroundings. The rest of each
prop remains fixed. Catalog building colors are excluded from water animation
unless the original metatile has a General-water palette layer. The primary
General animation destinations remain reserved and run independently.

The callback is installed on the shared Havora secondary tileset, including both
approaches. The engine clears it when entering the older city or ferry destination.
Generated frame PNGs and `src/data/havora_water_anim.h` are committed for normal
ROM builds; source animation and the catalog live with the other native cutouts.

`python tools/havora/build_assets.py` rebuilds the tileset from committed source.
`python tools/havora/build_map.py` rebuilds the approved 40×32 layout. **Do not run
the latter after manual Porymap edits unless you intend to reset the layout.**
These scripts are not invoked by ordinary ROM builds. Python, Pillow and NumPy
are sufficient; the committed palette plan makes builds deterministic.

## Verification

The native map render includes the approved buildings/quays, a new market stall,
and the first animated sea frame at GBA color depth. `tests/havora_layouts.py` verifies dimensions, graphic references,
buffer limits, all event bounds, reciprocal connections/elevations, the ferry
route and connectivity of every unoccupied walking tile. Removed props no longer
leave invisible collision. The promenade and lighthouse shore fronts remain solid.

`tests/havora_rom_assets.py` checks map/border bytes, metatile definitions,
attributes and decompressed graphics actually embedded in the ROM against the
current source. The Makefile tracks layout binaries to prevent stale map builds.

The ARM GNU 13.2.1 build passed. ROM region usage is 21,502,952 bytes / 32 MiB
(64.08%). mGBA checks passed eight directional outdoor crossings, the lighthouse
walking loop and plaque, pier boundaries, the open boarding route, original sailor
return to Vermilion, Stellar Ticket return to (20,18), and free movement afterward.
Test setup uses injected warps; crossings and ferry travel use game controls.

`tests/havora_rom_assets.py` also compares every animation frame embedded in the
ROM against the current generated graphics. mGBA verifies the animation callback
on each city/harbor crossing, and saves a gameplay GIF.

No Porymap UI testing or full campaign playthrough is claimed. Outdoor water is
blocked as before; Surf and old saves stranded at changed coordinates are outside
these checks. Water animation was verified in both VRAM and the visible screen across eight phases; a sampled house graphic stayed byte-identical.

Only Havora-Development is updated. QOL, V1 and V2 refs are not modified.

## Appended animated water boulder

The new General/Emerald boulder at primary metatile **0x08E** is a native 16×16
rock cutout with its flat light-blue backing removed. It now sits on the harbor
sea animation. The stone pixels remain fixed while surrounding water cycles
through all eight phases. It consumes four existing animation-padding slots,
so total allocated graphics remain 1,016/1,024 and no old metatile IDs change.

`tests/havora_water_boulder.py` decodes the compiled metatile from actual mGBA VRAM
through eight phases, checks every opaque stone pixel stays fixed, and checks
that the visible water changes. The author pushed the screenshot layout in be19b764 during this task. It was
merged before applying 14 water rocks, 6 bollards, 6 planters and 2 extra stalls
(44 blocks total). Two proposed decorations were omitted to preserve one-tile
walking links at (29,24) and (37,27). All of the author's event and connection
positions remain intact. The moved pier required updating the ferry arrival
from (20,16), now water, to the walkable deck at (20,18), beside the sailor at
(21,18). `docs/havora-coastal-study.json` records the applied placements.

`tools/havora/layout.json` now stores the latest verified authored layout for
explicit regeneration. Future manual Porymap changes belong in map.bin as usual;
do not run build_map.py after editing unless you also update this snapshot.
