# Havora western hills and northern services

This stage adds connected cliff districts around the established market and
harbor. All outdoor movement uses normal reciprocal map connections. Only
building interiors use warps. The harbor layout, tilesets, sailor and ferry
scripts remain unchanged.

## Porymap maps

| Map | Size | Purpose |
| --- | --- | --- |
| QuantumPortCity | 48×96 | Western gym plateau, residential terrace and lower waterfront |
| QuantumHavoraNorthDistrict | 96×40 | Northern square, Center, Mart, homes and upper promenade |
| QuantumHavoraCoastalDaycare | 48×40 | Eastern coastal cliffs, raising facility and fenced grounds |
| QuantumHavoraNorthWalk | 16×32 | Northern cliff walk and elevated lookout |

All four use **HavoraCityPrimary / HavoraCity**. The northern walk currently
ends at the lookout; its further connection to a regional route is future
work. The western old road has a narrow shared-paving boundary strip for a
clean connection. Existing road events and the rest of its layout are kept.

## Elevations and entrances

The gym plateau is elevation 5, the western residential terrace 4, and the
waterfront 3. The northern services are 5; the upper northern promenade is 6.
The coastal daycare and paddock are 6, above the arrival promenade at 5.
The northern lookout reaches 7. All stair tiles use transition elevation 0.

| Stair map | Left x | Top row | Upper / lower |
| --- | --- | --- | --- |
| QuantumPortCity | 16 | 28 | 5 / 4 |
| QuantumPortCity | 28 | 62 | 4 / 3 |
| QuantumHavoraNorthDistrict | 24 | 10 | 6 / 5 |
| QuantumHavoraNorthDistrict | 68 | 10 | 6 / 5 |
| QuantumHavoraNorthDistrict | 68 | 28 | 5 / 4 |
| QuantumHavoraCoastalDaycare | 22 | 26 | 6 / 5 |
| QuantumHavoraNorthWalk | 6 | 10 | 7 / 6 |

Each stairway is four tiles wide and two tiles deep. Keep both landings open.
The northern market entrance is the four-tile path at x12–15 on rows 0–11 of
QuantumHavoraNorthQuay. It replaces part of the former northern boundary.

| Service | Outdoor map | Door x,y | Interior |
| --- | --- | --- | --- |
| Gym | QuantumPortCity | 23,13 | QuantumHavoraGym |
| Center | QuantumHavoraNorthDistrict | 64,17 | QuantumPortCityPokemonCenter1F |
| Mart | QuantumHavoraNorthDistrict | 82,17 | QuantumHavoraMart |
| Daycare | QuantumHavoraCoastalDaycare | 30,13 | QuantumHavoraDaycare |

Five additional homes have private interiors and matching return destinations.
Stock multi-tile entrances use their center entry mat; warp IDs are zero-based.

## Services and scope

The Center keeps the existing nurse script and the project's single-floor
Center artwork. Outdoor exit warps, healing-location data and the region-map
Fly target now lead to the northern square. Its legacy upper-floor map and
scripts are preserved, but there is no active upstairs escalator in the
shared first-floor artwork; no upstairs route is claimed or restored here.

The Mart opens the native Buy interface with the existing Havora supplies.
The daycare reuses FireRed's live Route 5 single-Pokémon raising service and
save slot. Pokémon deposited through either attendant share that service;
this does not create a separate breeding system. The coastal field Pokémon
and caretaker use ordinary events inside the fenced grounds.

The gym has an enterable stock training hall and a guide. No leader, team,
badge, rewards or battle progression are assigned, and no Brock flags or
Kanto gym battles are reused. Those choices remain a later design stage.

## Artwork and editing

The Center, Mart and gym exterior shapes come from FireRed's General assets
as used in Vermilion. Their colors are fitted to the existing city material
palettes per 8×8 tile, without dithering. Existing city graphics, metatile IDs,
palette entries and the animated-water range are preserved. The new service
art brings the reserved/active city graphics budget to 687 of 1,024 slots.

New art IDs and reusable grids are in `tools/havora/civic-tiles.json`.
District entrances and stairs are listed in `tools/havora/civic-districts.json`.
Normal `make` does not run authoring tools. Save Porymap edits normally;
rerunning `build_civic_districts.py` deliberately restores this authored pass.
Do not run the older first-pass or terrace generators over later manual work.

## Verification

`tests/havora_civic_layouts.py` checks buffers, event coordinates, elevation-
aware circulation, reciprocal walking seams, service returns, and healing/Fly
configuration. `tests/havora_city_tileset.py` checks preserved native terrain
and compatible neighbor art. `tests/havora_rom_assets.py` checks actual ROM
blocks, attributes, graphics, and water frames against source.

`tests/havora_civic_emulator.py` tests ten outdoor crossings, all seven new
stairs in both directions with actual player elevations, nine new service/home
doorway round trips, nurse healing, respawn storage, the native Mart menu,
and daycare deposit, walking-based level growth, and return of the same
Pokémon. Setup warps and test party creation are emulator instrumentation.
The existing market/ferry emulator test covers the retained ferry round trip.
Native review renders and mGBA screenshots are provided; no Porymap UI testing
is claimed.

## Coastal neighborhood refinement

The refinement keeps all pre-existing service/house entrance coordinates and
ferry interactions. It adds nine private, enterable homes/lodgings: five cliff
homes, the harbor guesthouse, two northern homes and a northern lodge. The inn
and lodge currently provide resident dialogue, not a paid/rest service. Existing
Center healing, Mart sales and daycare raising remain the functional services.
Outdoor resident counts are now west 10, north 10, daycare 5 and market 12.
Three residents have short horizontal walking ranges; they stand off stairs,
service thresholds and the ferry route. No new graphics or palettes are added.

The west coast has water, native rock faces and stepped headlands below the
residential plateaus. The old coastal road now meets the lower waterfront:
QuantumPortCity's left connection offset is 60, with the road's reciprocal
right offset -60. The road's existing events/layout are retained.

QuantumHavoraWestQuay expands from 8x40 to 8x96. Its old cells begin at row 51;
its world origin now matches the market's northern edge. It uses the city
pair, whose lower quay and harbor-facing art remains compatible with the
harbor. New stairs at x2..5 / y16..17 and y36..37 descend 5→4→3. The northern
square connects at x50..53; its down offset is 48 and the quay's up offset -48.
Market/quay offsets are both zero. Harbor/quay offsets are -64/+64. Existing
west city/quay offsets are now zero. Former invisible pavement barriers on
these two western maps have visible railings; the established eight-tile
crossing at west-city rows 64..71 stays open.

A single weathered impact hollow and sign near the northern lookout introduce
Minior folklore. The larger crater landscape remains reserved for future
mountain settlements. The lookout still has no onward regional connection.

`tools/havora/refine_city.py` is a one-shot authoring recipe for the preceding
8x40-quay civic baseline. It refuses to run again over the expanded layout.
Do not run old district generators over this pass or subsequent Porymap edits.
`tools/havora/review_connected.py OUTPUT.png` renders all current outdoor maps
using their actual reciprocal connection offsets; it asserts world-placement
consistency and includes native object sprites.

### Different-primary camera transitions

The visual runtime review exposed an engine assumption: camera connections
only reloaded the secondary tileset. Walking from General to HavoraCity, or
HavoraHarbor to HavoraCity, could therefore reach the correct map while drawing
it with stale primary VRAM. `LoadMapFromCameraTransition` now compares the
resolved old/new primary tilesets and reloads both banks, palettes, weather
colors and animation callbacks when they differ. Same-primary transitions
retain their prior behavior. This also respects resolved seasonal General
variants rather than comparing only layout pointers.

Metatile 0x1D8 in the city primary now uses the exact General water definition
and existing reserved graphics. The west map's first eight columns use only
this shared water and the already shared paving, so the approach remains
readable while the camera is still on the General/Cinnabar coastal road.
No graphics slots or palettes were added for this repair.

`tests/havora_refinement_emulator.py` checks destination primary tile bytes in
actual VRAM after road↔city and harbor↔market crossings, accounting for the
active seasonal General variant and excluding reserved animated tiles. It
also interacts with the Minior sign and checks the visible western railing.
The civic tests now include fourteen crossings, nine stairways and all eighteen
civic service/home doorways. The market/ferry suite retains its seven doorways,
two stairways, shop tests and original ferry round trip.
