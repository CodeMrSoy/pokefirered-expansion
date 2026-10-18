# Havora harbor — custom artwork and seamless waterfront

The approved single-map composition is now native FireRed map data: 40 x 32
metatiles, with the original Seagallop at the central pier, two western cargo
buildings, dock office, lighthouse, crane, lamps, crates, barrels, nets, bollards,
rope and masonry edges. The roofless entrance is a walkable passage.

## Branch and scope

Havora-Development incorporates V2 `7a5b1cacbb1b473400cba126af451ec52ceddea9`,
including the existing QOL and rival fixes. Only Havora-Development is published.
The harbor's temporary scripted city exit and the legacy city/harbor door warps
are removed. Other city warp indices (Pokemon Center warp 0) remain stable.
Warehouse, office and lighthouse art are exterior scenery; there are no new
interiors or shop interfaces. The lighthouse plaque is readable.

## Seamless geography

The north and west city boundaries require two nonoverlapping approach maps;
a single rectangular city cannot occupy both adjacent rectangles at once.
Coordinates in a shared world frame:

| Map | Origin | Size | Secondary tileset |
| --- | --- | --- | --- |
| QuantumPortCity | 0,0 | 80x80 | existing VermilionCity |
| QuantumHavoraWestQuay | 80,0 | 8x40 | HavoraHarbor |
| QuantumHavoraNorthQuay | 88,0 | 40x8 | HavoraHarbor |
| QuantumHarbor | 88,8 | 40x32 | HavoraHarbor |

All crossings use reciprocal map connections at elevation 3. There are no
harbor warp or coordinate events. The old city and new tileset meet through
seven columns of primary-only pavement on each side, preventing a mismatched
secondary tile pattern during scrolling. Existing 80x80 city construction stays
in place apart from this eastern transition strip and closing its old harbor
door facade. The approach maps are functional city edges, not finished streets.

## Assets and regeneration

`tools/havora/source_art/harbor-assets.png` is the AI-generated isolated atlas
derived from the approved blue-roof Nordic harbor direction. Asset request:
two warehouse facades, dock office, red-cap lighthouse, crane, cargo, crate,
barrel, lamp, bollard, rope, net, seawall, dock wood, stone sample, gatepost.
The atlas is source art, not a claim of GBA compatibility on its own.

`python tools/havora/build_assets.py` crops named assets, converts them to native
sizes and six RGB555 palette banks (7..12), and deduplicates only identical
8x8 tiles including flips. It emits a dedicated secondary tileset, metadata,
and an exact indexed-pixel review sheet. Final budget: 269/384 secondary tiles,
73/384 secondary metatiles. Transparent tile index zero is reserved. Primary
General graphics and water animation stay intact. Native General pavement is
reused to avoid opaque seams in the generated stone sample.

`python tools/havora/build_map.py` regenerates map blocks, placements and
connections. Both generators require Python, Pillow and NumPy. It does not
change the ferry script logic. The Seagallop sprite moves to (25,20), the sailor
to (20,20), and the destination coordinate table now lands at (20,19), directly
above that sailor. The existing ticket gate, ferry scene, return destination,
and sailor interaction are retained.

`python tools/havora/render.py LAYOUT_QUANTUM_HAVORA_HARBOR_LAYOUT output.png`
renders the actual native tiles and palettes (NPCs omitted). It is not Porymap.

## Verification

`python tests/havora_layouts.py` checks native graphics limits and references,
map buffer sizes, 40x32 dimensions, event bounds, no harbor warps, reciprocal
connections and their offsets/elevations, and routes from the boarding point
to all piers, the city edges and lighthouse frontage.

`tests/havora_emulator.py` exercises real directional controls for the two
harbor edges, city approach, and approach corner in both directions. Test-only
injected warps set up those scenarios. It also speaks to the original harbor
sailor, completes the Seagallop return to Vermilion, adds a Stellar Ticket as a
fixture, and speaks to the original Vermilion sailor to return to (20,19).
It saves native gameplay screenshots under build/havora-tests. Supply MGBA_CORE
and ARM_NM as necessary; the support module boots a fresh game.

See the delivered build/gameplay logs for actual pass/fail evidence. No Porymap
UI test or full campaign playthrough is claimed. Surf, every decorative edge,
and older saves stranded at a former harbor coordinate are outside these
checks. Existing interior doors shown on the new artwork are scenery.

### Results for this revision

ARM GNU 13.2.1 build completed; ROM region usage 20,936 KiB / 32 MiB (63.89%).
The static validator passed. mGBA confirmed all eight directional connection
crossings, harbor/warehouse/lighthouse rendering, the boarding promenade walk,
return to Vermilion (3,5)/(23,32), and the ticket-gated return to Havora
(43,19)/(20,19). The source-art atlas was generated with the built-in
image tool; delivered previews use converted native pixels and mGBA frames.

Player control after disembarking was also verified: walking north from the
new landing moved the player from (20,19) to (20,17) on Havora Harbor.
