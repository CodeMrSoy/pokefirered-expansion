# Havora market and residential district

The area directly north of the harbor is now a 40×40 outdoor district. Its
existing Porymap name is **QuantumHavoraNorthQuay**. The map ID is unchanged.
It uses Havora's existing Lilycove buildings, Slateport stalls, harbor brick,
flower beds and planters, plus the reserved FireRed flagstone paving.
No new pixel graphics or palette banks were added.

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

The west quay begins at district row 27. The harbor begins at west quay row
13, matching district row 40. The reciprocal west/north offsets are therefore
-27/+27; the user's harbor/west offsets remain -13/+13. This makes the three
maps agree on one world-space geometry.

## Editing

Edit **QuantumHavoraNorthQuay** in Porymap and save normally. Do not rerun
`tools/havora/build_market_district.py` after manual changes unless you intend
to restore this authored version. Normal `make` does not run that tool.
The tool also creates the seven interior maps and their script includes.
Their positions are listed in `tools/havora/market-district.json`.

Keep routes through residential flower beds open at x6 and x33. Keep the
market's central aisle (x20/21) and the south promenade open. There are ten
outdoor NPCs, below the engine's sixteen-object budget.

Interior decoration is a first pass using stock FireRed rooms; bespoke
residential and trade-hall furnishing can be developed later.

## Verification

Run `tests/havora_layouts.py` and `tests/havora_market.py` for layout checks.
After compilation, `tests/havora_rom_assets.py` checks embedded blocks,
metatiles and animated-water frames against source.
`tests/havora_market_emulator.py` exercises eight outdoor crossings, every
building entrance/return, a vendor Buy menu, and the original ferry round trip
in mGBA. Setup warps in this test are only test instrumentation, not gameplay
connections. Native render previews are not Porymap UI testing.
