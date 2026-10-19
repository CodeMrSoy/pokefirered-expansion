# Havora market and residential district

The area directly north of the harbor is now a 40×64 outdoor district. Its
existing Porymap name is **QuantumHavoraNorthQuay**. The map ID is unchanged.
It uses a dedicated **HavoraCityPrimary / HavoraCity** pair. Lilycove
buildings and Slateport stalls sit on a raised FireRed cliff terrace, with
native grass, trees, flowers, gray stairs and flagstone streets. Original
harbor edge graphics and animated-water slots remain compatible.

## Streets and buildings

- Twelve stalls in two rows, with a central walking aisle and side aisles.
- Six stall vendors open the native FireRed shop interface.
- Four residential houses, a trade hall, an outfitter and a provisions shop
  have individual interiors and matching return destinations.
- The provisions shop uses the active FireRed Mart layout. Other interiors
  use the active House2 layout; House3 is retired in this repository.
- Blue and orange threshold definitions **0x08F / 0x090** reuse existing
  graphics with native nonanimated entrance behavior. No door animation is
  claimed. The existing harbor metatiles retain their definitions.
- Two roofs finish the buildings whose bottom halves are on harbor rows 0/1.

## Outdoor connections

The harbor remains exactly as authored in commit a08a9c5c. Its ferry object,
sailor, scripts, collision, return warps and arrival coordinates are preserved.
The north district uses a normal outdoor map connection to the harbor.
Only building interiors use warps.

The west quay begins at district row 51. The harbor begins at west quay row
13, matching district row 64. The reciprocal west/north offsets are therefore
-51/+51; the user's harbor/west offsets remain -13/+13. This makes the three
maps agree on one world-space geometry.

## Editing

Edit **QuantumHavoraNorthQuay** in Porymap and save normally. Do not rerun
`tools/havora/build_terrace_city.py` after manual changes unless you intend
to restore this authored version. Normal `make` does not run that tool.
The old `build_market_district.py` restores the earlier flat 40×40 design;
it should not be run during ordinary editing. The seven interiors remain
unchanged apart from their outdoor entrance elevations.
Their positions are listed in `tools/havora/market-district.json`.

Keep routes through residential flower beds open at x6 and x33. Keep the
market's central aisle (x20/21) and the south promenade open. There are ten
outdoor NPCs, below the engine's sixteen-object budget.

Interior decoration is a first pass using stock FireRed rooms; bespoke
residential and trade-hall furnishing can be developed later.

## Verification

Run `tests/havora_layouts.py`, `tests/havora_market.py`, and
`tests/havora_city_tileset.py` for layout, elevation and graphics checks.
After compilation, `tests/havora_rom_assets.py` checks embedded blocks,
metatiles and animated-water frames against source.
`tests/havora_market_emulator.py` exercises eight outdoor crossings, every
building entrance/return, a vendor Buy menu, and the original ferry round trip
in mGBA. Setup warps in this test are only test instrumentation, not gameplay
connections. Native render previews are not Porymap UI testing.

## Raised terrace and native terrain

The market and residential streets use engine elevation **4**; the harbor
and lower promenade use **3**. The two four-tile-wide stairs occupy x4–7 and
x19–22 on rows 38/39. Their elevation is **0**, the engine's ordinary
transition height. The upper landing is row 37 and the lower landing row 40.
The remaining cliff faces are solid; there are no elevation-change scripts
or outdoor warps. All ten upper-city NPCs and seven entrance warps use 4.

The dedicated city pair imports the compatible-palette native FireRed General
terrain catalog without changing its GBA colors. Its original General IDs
map to city IDs in `tools/havora/city-tileset.json`. Useful city metatiles:

| Piece | City metatile |
| --- | --- |
| Mowed grass | 0x000 |
| Native flowers | 0x002 |
| Cliff top | 0x039 |
| Cliff face | 0x030 |
| Stairs top | 0x0A6 |
| Stairs bottom | 0x0A7 |

The five native stair colors use previously unused entries in a city palette;
colors used by shared harbor edge tiles are preserved. The native terrain
comparison checks exact color values at GBA depth. All source art is already
in this repository; no external tileset checkout is required.

The lower promenade provides room for tree gardens and keeps new terrain
outside the harbor and west-quay neighbor buffers. Its southern eight rows
and western buffer strip use definitions that render identically with either
map's tileset. Primary and secondary city graphics together use 595 reserved
or active 8×8 slots, including the unchanged water-animation range.

The mGBA market test also walks both stairs up and down, reads actual player
object elevations, and checks that a cliff face stops northward movement.
`tests/havora_city_water.py` verifies eight real animation phases while the
city tileset is active at the harbor boundary. No Porymap UI test is claimed.
