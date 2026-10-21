# Shared Havora outdoor tilesets

All seven Havora outdoor layouts now use `gTileset_HavoraCityPrimary` and
`gTileset_HavoraCity` (Porymap: HavoraCityPrimary / HavoraCity).

## Preservation

- All six City map/block and border files are byte-identical to the source tree.
  Existing City metatile IDs, packed attributes, cliffs and stairs are retained.
- Harbor block low ten-bit metatile references are remapped; all collision and
  elevation bits are identical. Its border did not need modification.
- No map dimensions, map headers, connections, events, scripts, ferry interactions
  or warps were changed. Only Harbor's layout tileset names changed.
- All retained metatiles match their previous rendered pixels at the initial
  frame and all eight Harbor water-animation frames: 6,102 comparisons.
- All 14,009 map and border cells retain collision/elevation. The full connected
  tile-and-NPC preview is pixel-identical before and after migration.
- Graphics 0 and 20 retain the engine's transparent/backdrop roles. General and
  Harbor animation destinations are reserved and their callbacks unchanged.

## Available catalog

581 defined metatiles share the pair. It retains 317 valid City source entries
and 361 Harbor source entries (some deduplicate), including every placed tile,
all primary custom Harbor assets, all Pacifidlog catalog entries, and the named
boats, lighthouse, warehouse, market stalls, and dock assets.

170 unplaced Harbor definitions do not fit. Their original files remain under
`data/tilesets/{primary,secondary}/havora_harbor`; no source art was deleted.
`tools/havora/shared-tileset.json` records retained ID mappings and omitted IDs.
The old Harbor pair is an archive, not the pair to select for current maps.

The graphics atlas is full, including 198 animation slots. Blank metatile cells
can compose existing graphics, but do not represent free 8x8 graphic storage.

Water-backed cliff corners are primary metatiles 0x0A8 (NW), 0x0A9 (NE),
0x0AA (SW), and 0x0AB (SE). They replace four unplaced, invalid prototypes.
They reuse native cliff colors over existing animated water; their attributes
remain solid native cliff attributes, not water encounter/Surf attributes.
When placing them, use solid collision and the neighboring cliff elevation.
No new corners were painted over the user's existing map.

## Verification and editing

`python tools/havora/merge_tilesets.py --check` validates this exact migration
against source Git tree `1e49f05b8e46803773587e4d03f212c403063fc6`.
It is a frozen migration check, not a command to run after additional Porymap
edits. `--apply` refuses to replace subsequent edits in its output files.

The older build/refinement scripts and assets.json describe historical layouts
and IDs. Do not regenerate today's maps from those historical recipes. Edit
current maps in Porymap using the shared pair and shared-tileset.json instead.

ROM compilation completed successfully with ARM GCC 13.2.1. A headless mGBA
harness was attempted, but its forced new-game initialization did not reach the
field. Therefore map loading, walking transitions and ferry travel are NOT
claimed as emulator-tested. Porymap UI testing was not performed.

The connected image is a native asset render, not an emulator or Porymap capture.
