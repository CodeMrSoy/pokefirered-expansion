# PokéGlass text and border audit — 2026-10-31

Follow-up to e9cb1321 on QOL. No V2 integration or sprite/map-art changes.

## Corrections

- Pokédex: separate list headings from the top outline, retain room below the
  final row, and move the habitat separator below its label. Bound species and
  category names to their columns. Footer text remains inside the glass.
- Stats: shorten the profile panel and move types upward so its bottom outline
  clears the ability row. Fit headings, held items and abilities to the glass;
  ability descriptions have a bounded two-line area below the panel.
- PC: fit box names, inspection headings and item choices; inset the moving
  marker inside its slot outline. All six boxes and management dialogs reviewed.
- TM/Berry cases: fit move/berry names before font control codes and quantities.
  The ordinary Bag already fits names with its existing narrow-font helper.
- Party: move message, popup and field-description character-tile allocations
  away from the cards/header/hint; reserve separate ranges for simultaneously
  live windows. Hide the underlying Cancel button while popups occupy its area
  and restore it on close. Use compact popup rows/cursor spacing, a short fitted action
  prompt, and a separate description row for field moves. Returning from a
  field move restores the normal action prompt.

## Verification

Native incremental ARM release build: EWRAM 238,828/262,144 bytes, IWRAM
27,573/32,768 bytes, ROM 21,822,316/33,554,432 bytes. Existing linker RWX
warnings remain. As for the preceding overhaul, the environment's stalled
Windows make dependency scan was bypassed with the existing native build helper.

`tests/pokeglass_text_layout_emulator.py` captures 51 states across the two launcher pages,
Pokédex filters/sort/detail/habitat, all three Stats pages, all six PC boxes,
inspection/giving/moving/release, Party/actions/item/switch/field-move prompts,
Summary identity/moves/move details, all seven Field Kit selections and its
locked state, Trainer Card front/crests/records, all Options rows, and Save.

The test checks actual rendered border pixels on Pokédex and Stats, exercises
oversized strings through the real font renderer, and compares every live Party
window's character-tile range to detect shared graphics allocations. It also
compares the rendered Cancel region to verify it is hidden under popups and
restored on close. Visual captures are reviewed alongside Bag, TM/Berry case, retained Field Item Case
and Town Map captures from the native interaction suites.

Executed evidence groups under the workspace's `v2-integration-test/results/`:
`emulator-qol-text-layout`, `emulator-qol-text-audit`,
`emulator-qol-text-review`, `emulator-qol-text-dialogs`,
`emulator-qol-text-complete`, `emulator-qol-text-release`,
`emulator-qol-text-verified`, `emulator-qol-text-acceptance`, and
`emulator-qol-text-pixels`.
Use the latest successful rerun of a suite. Earlier audit fixtures attempted to
call an inlined paragraph helper and chained PC modal inputs; these harness
failures were corrected without relaxing border assertions. PC modal captures
now start independently and assert their actual task states.

Additional emulator checks cover Party digit/HP redraw, real Rare Candy move
learning and stat popups, Summary return, Field Kit use, PC transactions/flash,
Bag use/cases, launcher navigation/save, transitions and repeated allocation
cleanup. DexNav is disabled in this build. This is a menu/UI audit, not a full
campaign, multiplayer or physical-hardware test.
