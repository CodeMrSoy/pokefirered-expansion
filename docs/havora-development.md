# Havora harbor — Nordic buildings and completed waterfront

The initial native harbor compressed the buildings, reduced the seawalls to
thin rails, and placed the main pier too far south. This revision measures the
approved reference against the 40x32 footprint and restores those proportions.

## Nordic silhouettes with native FireRed materials

The warehouse and fish store retain the earlier tall gables and 80x96 footprints;
the office keeps a 64x64 footprint and a smaller front gable. The fish sign,
framed attic window, chimneys, timber beams and cargo details distinguish them
from the flat vanilla replacements. These shapes are authored directly on the
native pixel grid in `firered_buildings.py`, without resized concept pixels.

Material colors come from General blue roofs/windows and Vermilion wall and
timber palettes (secondary banks 02 and 10). Window clusters come from General
metatile 0x006; the closed door is based on Vermilion 0x29e. Detail colors are
mapped into the same small building palette. Broad roof courses, restrained
shingle joints and one-pixel contours replace the earlier fine texture. The
building materials use a small palette shared with native FireRed graphics.

Ferry scripts, events and map connections remain unchanged. Buildings remain
exterior scenery, with no new door warps or interiors.

## Native FireRed harbor props

`firered_props.py` replaces the concept-derived crane, crates, stacked cargo,
barrels and lighthouse at native resolution. It uses the same blue-grey outline,
Vermilion timber and General window colors as the Nordic buildings. The crane
has a pulley, brace, hand winch and suspended net; cargo uses clear cross braces
and metal barrel hoops. The lighthouse has a tapered white tower, red gallery,
stepped roof and blue windows. Lanterns retain their hook with a wider framed
light and highlighted iron base.

All six footprints and palette banks remain unchanged. Map block data, collision,
events, ferry scripts and connections are byte-identical to the waterfront revision.
The ROM was rebuilt and its embedded graphics checked against source. mGBA tests
passed all eight crossings, lighthouse walkway, pier barriers and ferry round trip.

## Docks, lanterns and continuous seawall

`firered_waterfront.py` supplies native-pixel timber boards, continuous side
rails, banded posts, pier end caps, rope coils, netting and mooring bollards.
The eight lanterns use a compact hooked iron silhouette and warm glass. Their
feet block movement; the upper tile retains the underlying walking behavior.
A short visual gangplank aligns the main pier with Seagallop. It does not
replace the original sailor boarding script or add a warp.

The approved south-facing masonry and rock artwork retain palette bank 09.
New coping variants are quantized against that original palette rather than
changing it. Front corners take priority over side edges, so vertical coping
cannot erase the wall face. Thin north/west/east coping leaves paving walkable;
adjacent water remains impassable. Front wall faces and dock rails block walking.

The office, crane and lighthouse now have complete stone footings and room for
perimeter coping. The isolated crane-plinth ledge is blocked. The planter that
covered the promenade wall moves one tile inward; foundation rocks sit below
the lighthouse wall, not over its face. The main promenade and lighthouse front
have continuous two-row masonry. Buildings and the original ferry/NPC events
retain their positions and graphics.

Static checks require every unoccupied walkable tile to connect to the ferry
arrival. They also protect the long promenade/lighthouse wall fronts from
being replaced by prop backgrounds. Emulator checks walk the lighthouse coping
loop, test the main pier's end and side rails, traverse all eight map seams,
and complete the original ferry round trip.

## Visible changes

- Western warehouse and fish store: 80x96 native pixels, at (1,3) and (1,11).
- Dock office: 64x64 at (11,16), beside the open-air boarding entrance.
- Main pier: starts at (18,13); Seagallop, sailor and arrival move together.
- Lighthouse: 48x96 at (35,20), with a rocky foundation and walkable frontage.
- Two-row masonry faces and side coping replace the flat boundary rails.
- Timber piles, deck support legs, narrower lamps, planters, cargo, nets and
  rope provide the details missing from the first native conversion.
- A fisher and lighthouse keeper join the original harbor NPCs.

Warehouse, office and lighthouse art remain exterior scenery; no new interiors
or shop interfaces are introduced. The lighthouse plaque is readable. The
harbor retains its 40x32 dimensions and seamless north/west connections.

## Graphics allocation

`gTileset_HavoraPrimary` and `gTileset_HavoraHarbor` are a dedicated standard
primary/secondary pair. This uses the engine's existing 1024-tile graphics
address space; no graphics limit is raised. The prior design unnecessarily
confined all new art to the 384 secondary slots and therefore shrank it.

There are 381 unique custom graphics tiles and 155 secondary metatiles.
The primary PNG occupies its normal 640 slots; the secondary PNG contains a
minimal blank row. All referenced graphics IDs are below 624. The remaining
slots are available for future harbor art.

83 original General graphics slots remain byte-identical, including every
General animation destination (416..481 and 508..511) and the pavement,
water and shrub graphics. Original metatiles 5, 0x1c1 and 0x1d9, their attributes,
and palette banks 0, 1 and 6 stay compatible. Other primary slots are repacked
with harbor artwork. General itself and all unrelated maps are unchanged.
The normal General animation callback is safe because custom artwork never
reuses an animated graphics slot, even when its initial pixels happen to match.

The old city and new tileset meet through seven columns of compatible paving
on both sides of the boundary. This prevents mismatched graphics while the
camera scrolls between tileset pairs. Harbor and both approach maps use the
same dedicated pair; only that transition strip remains in the old city.

## Geography and ferry

| Map | World origin | Dimensions |
| --- | --- | --- |
| QuantumPortCity | 0,0 | 80x80 |
| QuantumHavoraWestQuay | 80,0 | 8x40 |
| QuantumHavoraNorthQuay | 88,0 | 40x8 |
| QuantumHarbor | 88,8 | 40x32 |

Approach maps keep the north/west city rectangles from overlapping. All outdoor
crossings are reciprocal map connections at elevation 3. Harbor warp and
coordinate-event arrays remain empty. Original city Pokemon Center warp 0 is
unchanged; the former harbor doorway remains closed.

The original Seagallop object is now at (25,17), sailor at (20,17), and arrival
at (20,16). Original ticket checks, sailor interaction, ferry scene and return
to Vermilion are retained. Only the destination coordinates change together.

## Editing and regeneration

The source atlas and supplementary terrain art are in
`tools/havora/source_art`. The built-in image tool produced the terrain request:
full-height grey masonry face, vertical quay side, rock outcrop, wooden pile,
dock-front support legs and a planted stone box, matched to the approved art.
Generated source images are not assumed to be engine-ready.

`python tools/havora/build_assets.py` extracts assets, scales them to the native
sizes above, quantizes each material to a 15-color RGB555 bank, and packs exact
8x8 tile patterns with flip reuse. Banks with fewer than 15 colors are explicitly padded to the fixed 16-entry
GBA palette format. It emits both native tilesets, metadata and
an indexed-pixel asset review sheet. No approximate tile replacement is used.

`python tools/havora/build_map.py` places the artwork, collision and events.
Tall freestanding props block at their feet, allowing the player to walk behind
their upper portions where the underlying ground was already passable.

`python tools/havora/review.py` renders the actual blocks, palettes and original
object sprites. `python tools/havora/compare.py --reference IMAGE_PATH` creates
a comparison of the approved illustration with the native map and emulator
captures. These are native renders, not Porymap screenshots. Python, Pillow
and NumPy are required for the asset/build helpers.

## Verification and limits

Porymap binary edits previously could leave `maps.o` stale: the make rule did
not depend directly on layout `map.bin` / `border.bin` inputs. The rule now
tracks those files. `tests/havora_rom_assets.py` compares embedded map/border
bytes, metatile tables, attributes and decompressed graphics against source,
so a successful compile cannot silently ship the previous layout.

`python tests/havora_layouts.py` verifies dimensions, buffer size, graphics
references, metatile limits, event bounds, reciprocal offsets/elevations,
walking routes to every pier and lighthouse, absence of harbor warps, and
byte-identical reserved graphics/palette compatibility.

`tests/havora_emulator.py` boots the compiled ROM in mGBA and checks eight
outdoor crossings, asset loading, the boarding route, original sailor return
to Vermilion, Stellar Ticket return to (20,16), and movement after disembarking.
Injected warps are test setup; the connection checks use directional controls.
The lighthouse plaque and native building/terrain views are also captured.

ARM GNU 13.2.1 ROM build passed, with ROM region usage 21,453,672 bytes / 32 MiB
(63.94%). There is no new dynamic RAM allocation for the artwork. Emulator
captures use normal game lighting; the overview renders native palettes
without time-of-day tint. No Porymap UI testing or full campaign playthrough
is claimed. Older saves stranded at a changed harbor coordinate, Surf and
all possible decorative collision approaches are outside these checks.

Only Havora-Development is updated. QOL, V1 and V2 refs are not modified.
