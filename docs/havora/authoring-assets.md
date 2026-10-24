# Havora authoring additions

Use Porymap pair **HavoraCityPrimary / HavoraCity** on all Havora outdoor maps.
These additions extend the editing catalog; no objects were painted onto maps.

## Pokémon statue

The stock FireRed gym Pokémon sculpture is two metatiles tall. Place the head
above the base. Its original pixel silhouette is retained and its material
colors use the current outdoor gray/stone palettes. No palette entries changed.

| Background | Head | Base |
| --- | --- | --- |
| Paving | `0x0AD` | `0x1E8` |
| Grass | `0x1E9` | `0x1EA` |

Use solid collision for both statue cells and the surrounding ground elevation.
The source sculpture is the one at the Pewter Gym sign events: secondary
PewterGym metatiles 0x2AF / 0x2B2, with their transparent Building overlays.

## Buildings

84 Lilycove facade/roof modules are available, including 34 newly restored
pieces for walls, windows, roof edges and connectors. Their current metatile
IDs and original Emerald IDs are listed in `tools/havora/authoring-assets.json`
and on the labeled preview. These pieces reuse the archived Harbor artwork.

## Market stalls

The complete existing stall is assembled as follows (hexadecimal metatile IDs):

| Left | Middle | Right |
| --- | --- | --- |
| `2AC` | `2AD` | `2AE` |
| `2AF` | `2B0` | `2B1` |
| `2B2` | `2B2` | `2B3` |

The preview also identifies 55 retained Slateport market/umbrella/waterfront
catalog entries. The stall pieces were already included in the shared pair;
they have been protected and documented rather than duplicated.

## Preservation and limits

All currently placed metatiles have identical graphics and packed attributes
at the initial frame and all eight water-animation frames. Native terrain,
cliffs, civic buildings, full Pacifidlog wood/docks, named Harbor assets and
retained market pieces are protected. No map, collision, elevation, event, warp,
connection or animation callback changed.

To make room, unused catalog definitions referencing reclaimed graphic slots
were retired. Their original metatile words, attributes and graphic pixels are
saved in `tools/havora/authoring-assets-archive.json`. The current shared mapping
excludes those retired definitions. The exact list is in authoring-assets.json.
The frozen merge migration remains historical; use current manifests/Porymap
for subsequent work.

`python tools/havora/add_authoring_assets.py --check` validates this migration
against source commit 0673644. It intentionally stops matching after later
manual tileset edits. `--apply` refuses to replace newer tileset edits.

ROM compilation and the current map-data audit pass. No Porymap UI or emulator
visual testing was performed for this catalog update.
