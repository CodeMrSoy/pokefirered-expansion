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
