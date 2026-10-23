# Havora stall, forest entrance and court kits

Uncommitted extension to the western gym garden, based on the latest Havora map edits at a8b19167.

## Complete stalls

The former three-by-three kit was the middle cutout. Complete five-by-three and four-by-three Slateport stalls now include the outer canopy posts, side panels and counter ends. Matching baskets, flowers, weighing/counter pieces are included. Current market placements are preserved.

Rows below list hexadecimal shared metatile IDs, left to right.

### Wide

| Row | Metatile IDs |
|---|---|
| 1 | `1F9` `13F` `140` `141` `214` |
| 2 | `216` `167` `220` `168` `165` |
| 3 | `21B` `143` `143` `21F` `21E` |

### Narrow

| Row | Metatile IDs |
|---|---|
| 1 | `14F` `13F` `141` `13C` |
| 2 | `164` `167` `168` `217` |
| 3 | `21D` `21F` `21F` `21C` |

## Forest entrance

This is the dark canopy opening from Three Island Bond Bridge in FireRed: source secondary metatiles 0x330–0x343, arranged as the original four-by-three kit. Surrounding standard tree pieces already exist in the shared tileset. This adds art for placement; it does not add a forest map, route connection or warp. Keep the two central bottom cells passable when placing the entrance.

| Row | Metatile IDs |
|---|---|
| 1 | `221` `169` `222` `223` |
| 2 | `16A` `16B` `224` `225` |
| 3 | `226` `090` `1C7` `227` |

## Training court

White chalk boundary, halfway line and centered Poké Ball are installed across the existing 8x6-tile court interior at (21,6). These are static metatiles; no objects, movement triggers or battle scripts are added. Court collision and elevation bits are preserved.

## Packing and validation

The combined tileset remains at the normal 1024-graphics limit. This migration archives and reclaims 52 unplaced legacy catalogue definitions to pack 106 required static graphics. All currently placed map art, named harbor assets, selected house/store kits, native terrain, palettes, animated water, flowers and fountain slots are protected. Archived definitions and graphic bytes are retained in editor-kits.json; obsolete shared catalogue aliases are removed.

Full ROM compilation passed (build/editor-kits/build.log). check_gym_garden.py verifies preservation against the user map baseline plus local route access with NPCs blocking their tiles. No emulator or Porymap UI testing was performed. The existing North Lodge return-warp issue remains outside this patch.

Source art: existing FireRed repo assets and pret/pokeemerald commit 731ad5bfd6e6f265508d0efcca0ba42f9dcf5881. Emerald files needed to recover missing stall end pieces are preserved under tools/havora/source_art/editor_kits.

Preview: editor-kits-preview.png. Updated placed court: gym-garden-preview.png.
