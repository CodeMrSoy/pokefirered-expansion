# Havora and current QOL integration into V2

Source tips at integration:

| Role | Commit |
| --- | --- |
| V2 before merge | 5ecfc051c22c4f82f9b6c6b6e3c1d0c0dec12bac |
| Havora development | 3a4217c7b1ad72a04c246efdd61f34911a94f395 |
| Latest QOL | 1df9e1212555b1ec3616d53a7bc572875ec94f29 |

QOL was already an ancestor of V2 (the Field Item Case and Lantern changes were
merged through V1). The V2/Havora merge preserves that ancestry, rather than
copying or reimplementing QOL. Only V2 is published by this integration.

The two textual conflicts were header additions in `src/scrcmd.c` and
`src/field_control_avatar.c`; both `field_tools.h` and `havora_puzzle.h` are
retained. The clean merge of `src/overworld.c` retains Lantern updates and
Havora's map-transition handling. No maps, events, offsets, cliffs or tilesets
were repainted for integration.

The asset audit checks 1,100 Havora/shared map, layout, event and art files
against the Havora tip, plus the common nurse fix, lab lighting, developer
Start entry, puzzle controller and QOL traversal/case/glow implementations.
The puzzle preservation check now allows Kanto dialogue/reward script changes
while continuing to protect all map geometry/events and Havora scripts; the
old blanket check incorrectly rejected legitimate QOL reward updates.

## Verification

- `make -j4 DEVELOPMENT=1 KEEP_TEMPS=1`: complete development ROM build.
- `python tests/havora_v2_merge_assets.py`: both branches' feature preservation.
- `python tools/havora/check_counterweight.py`: exact maze/art preservation and
  independent 37-action solution replay.
- `python tools/havora/check_puzzle_tiles.py --rom`: current assets linked in ROM.
- `python tests/window_lighting_assets.py --baseline-ref origin/Pokemon-Quantum-V2`:
  daytime-equivalent lab palette fixes across all seasonal variants.
- `python tools/havora/test_fountain_animation.py` and
  `python tools/havora/test_corner_buffer.py`: animation and border regressions.
- `python tests/havora_counterweight_emulator.py`: native full puzzle route,
  pits, gate frames/collision, state reload and reset. As previously documented,
  that route fixture enables Strength and invokes native removal for Cut results.
- `ARM_NM=arm-none-eabi-nm python tests/havora_qol_integration_emulator.py`:
  real Shears and Gloves prompts inside Havora, Cut-state persistence, reusable
  case tools, and a boulder filling a pit without party traversal moves.
- `ARM_NM=arm-none-eabi-nm python tests/field_tools_emulator.py`: all seven tools,
  reward/badge gates, native actions, registration, migration and flash Continue.
  Waterfall uses its documented transient RAM fixture; no retained map has one.
- `ARM_NM=arm-none-eabi-nm python tests/field_item_case_emulator.py`: actual Bag,
  Select/wheel navigation, seven 64px previews, Lantern cave entry, darkness,
  glow/flicker, cleanup and case ownership across flash save/Continue.
- `python tests/center_dialogue_emulator.py`,
  `python tests/lab_windows_emulator.py`, and
  `python tests/start_debug_menu_emulator.py`: the latest service/lighting/Start
  fixes in the combined ROM.

These are ROM and native asset checks, not a Porymap UI walkthrough. The build
uses the existing development gate; a normal release build keeps DEBUG hidden.

## Latest testing-feedback integration

Source tips: QOL `f35f5a79aea89e820342844ac46486fe0b9b3d5f` and
Havora-Development `c5ee4418b489b9f637043308b1d5a4d5b7e8b5c4`.
V2 base: `c980f9e01d6ddd9dadb066bdbd4f97b084fccee2`.

The old custom-tablet map conflicted with QOL's native-app restoration. The
native Pokeglass launcher/PC implementation is taken from QOL. V2 retains its
native Kanto/Vidra map pages and location/Fly destinations; retired Sevii pages
remain excluded. The map's startup selects Kanto or Vidra from the current
location, rather than using QOL's Kanto-only default. Havora's latest marked
controls, breeding nursery, sailor-facing fix and terrace sprite ordering are
preserved. The independent puzzle preservation validator is retained from
Havora. Development emulator fixtures launch Pokeglass through its real script,
so the Start menu DEBUG entry does not change which app they select.

Verified development ROM build and preservation of 1,102 layout/map/event/art
files. Native emulator checks passed for the empty case, all launcher apps,
PC deposit/withdraw/Move Items/last-mon protection, Kanto/Vidra page navigation
and location names/Fly safety, nursery breeding/doors/egg collection, canopy
and roof occlusion, the complete 37-action puzzle with animation/reset/reload,
Shears/Gloves in the grove, and both Stellar Ticket walking triggers.

## Menu, Stats, and colored-control integration

QOL `6f08125e892ab60451107771958ba05c53400646` and Havora-Development
`6776592f07de3f6c25038670df0a2825d5770603` merge into V2 after `ae9094c5`.
The merge is clean and preserves the latest Havora harbor/west-quadrant Surf
elevation edits, solid colored buttons, ground-layer resting gates and shared
cliff tiles. QOL contributes the title-menu spacing/unsigned seed fixes, Stats
ability descriptions/nature colors, menu-only overlay palette and corrected
main Gloves picture. Native Kanto/Vidra map pages and PC remain as in V2.

The Stats emulator fixture launches the real Pokeglass script directly, because
development builds expose DEBUG as the first Start-menu item. Preservation
checks now pin both source tips and require both as V2 ancestors.

Validation: development ROM compilation passed. All 1,102 checked Havora
map/layout/event/art files match the source tip, both source ancestries are
retained, and QOL implementation/assets match its tip. The terrain preservation
validator now pins the user's latest Harbor/West Surf edits instead of rejecting
them against the older pre-edit baseline. No game map was changed to satisfy a
test. Emulator passes: Stats nature-label pixels and palette preservation;
six-app grid; native PC deposit/withdrawal, Move Items and last-mon protection;
Kanto/Vidra pages and Fly safety; full 37-action maze, ground control layering,
gate animation/collision/reset/reload; native Shears/Gloves in Havora.
