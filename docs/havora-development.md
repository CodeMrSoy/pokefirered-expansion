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

The asset packer preserves every imported pixel at GBA 5-bit color depth using
12 of 13 palette banks. Some 8×8 patches use both hardware layers to combine two
material palettes without color loss. It uses 86 secondary metatiles and 193
custom graphics; the highest tile ID is 623. Layer attributes and collision are
native FireRed data. Empty primary slots outside the reserved set are available
for this dedicated harbor pair; do not swap to General + HavoraHarbor alone.

`python tools/havora/build_assets.py` rebuilds the tileset from committed source.
`python tools/havora/build_map.py` rebuilds the approved 40×32 layout. **Do not run
the latter after manual Porymap edits unless you intend to reset the layout.**
These scripts are not invoked by ordinary ROM builds. Python, Pillow and NumPy
are sufficient; the committed palette plan makes builds deterministic.

## Verification

The native map render matches the approved unoccupied artwork exactly at GBA
color depth. `tests/havora_layouts.py` verifies dimensions, graphic references,
buffer limits, all event bounds, reciprocal connections/elevations, the ferry
route and connectivity of every unoccupied walking tile. Removed props no longer
leave invisible collision. The promenade and lighthouse shore fronts remain solid.

`tests/havora_rom_assets.py` checks map/border bytes, metatile definitions,
attributes and decompressed graphics actually embedded in the ROM against the
current source. The Makefile tracks layout binaries to prevent stale map builds.

The ARM GNU 13.2.1 build passed. ROM region usage is 21,451,272 bytes / 32 MiB
(63.93%). mGBA checks passed eight directional outdoor crossings, the lighthouse
walking loop and plaque, pier boundaries, the open boarding route, original sailor
return to Vermilion, Stellar Ticket return to (20,16), and free movement afterward.
Test setup uses injected warps; crossings and ferry travel use game controls.

No Porymap UI testing or full campaign playthrough is claimed. Outdoor water is
blocked as before; Surf and old saves stranded at changed coordinates are outside
these checks. The imported sea art currently uses its static native preview frame.

Only Havora-Development is updated. QOL, V1 and V2 refs are not modified.
