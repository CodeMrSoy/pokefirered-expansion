# Havora harbor — reference fidelity rework

The initial native harbor compressed the buildings, reduced the seawalls to
thin rails, and placed the main pier too far south. This revision measures the
approved reference against the 40x32 footprint and restores those proportions.

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

There are 479 unique custom graphics tiles and 137 secondary metatiles.
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
8x8 tile patterns with flip reuse. It emits both native tilesets, metadata and
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

ARM GNU 13.2.1 ROM build passed, with ROM region usage 21,460,172 bytes / 32 MiB
(63.96%). There is no new dynamic RAM allocation for the artwork. Emulator
captures use normal game night lighting; the overview renders native palettes
without time-of-day tint. No Porymap UI testing or full campaign playthrough
is claimed. Older saves stranded at a changed harbor coordinate, Surf and
all possible decorative collision approaches are outside these checks.

Only Havora-Development is updated. QOL, V1 and V2 refs are not modified.
