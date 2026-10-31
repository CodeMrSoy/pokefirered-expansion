# Glass Bag — 2026-10-31

The Bag app uses the PokéGlass palette, translucent captured field, tablet
bezel, cyan panel outlines and small text. The original male/female bag sprite,
three pocket frames, opening/bounce callbacks and selection shake are retained.
Five item rows occupy the right pane; the selected item icon and up to three
native description lines sit below. The header shows the pocket and stack count.

The existing Bag tasks still own use, give, toss, registration, sorting,
reordering, pocket switching and native TM/Berry/Field Item Case callbacks.
Only Bag screens in an active PokéGlass launcher session use this presentation;
tutorial, battle, shop and ordinary non-tablet entry points keep their native
layout. The nested cases retain their existing separate screens.

## Layout and memory

- BG0 contains text and native dialogs; BG1 contains the shared glass frame and
  two compact tile-built outlines; BG3 reuses the launcher's captured field.
- Bag sprite and item icons keep their original graphics and palettes.
- Pocket changes retain the bag animation and timing, while skipping the old
  cream-paper list wipe. The tablet background and bezel stay stable.
- Item/action and quantity dialogs use cyan borders and dark fills. Temporary
  window tiles are placed into free ranges after the permanent windows, with
  no overlapping live windows or writes into the tablet's reserved tile area.
- Initial window graphics shrink from 314 tiles to 280 (1,088 fewer heap bytes).
  No new persistent EWRAM data or duplicate screen bitmap is introduced.
- Build use: EWRAM 238,828/262,144 bytes; IWRAM 27,573/32,768 bytes;
  ROM 21,824,080/33,554,432 bytes.

## Executed verification

The native incremental ARM build uses the established release flags and object
order; the existing linker RWX warnings remain. Windows make dependency scanning
has the previously documented environment limitation.

`tests/pokeglass_glass_bag_emulator.py` exercises populated Items, Key Items and
Poké Balls; scrolls beyond the fifth row; records actual sprite animation frames,
y-offset bounce and an animated GIF; checks the physical bezel every animation
frame; opens sorting, context, quantity and toss confirmation; cancels toss and
reorder without losing items; and checks all live BG0 window tile ranges.

`tests/pokeglass_bag_actions_emulator.py` additionally heals with a real Potion,
checks quantity consumption, opens/cancels TM and Berry cases and the retained
Field Item Case, and returns through the launcher with field control unlocked.
The repeated-session resource suite now opens the Bag and switches pockets on
every cycle. Launcher/save and app-transition benchmarks also pass.

Local evidence lives in `v2-integration-test/results/` under
`emulator-qol-glass-bag`, `emulator-qol-glass-bag-actions`,
`emulator-qol-glass-bag-final`, `emulator-qol-glass-bag-release`, and
`emulator-qol-glass-bag-padding`.
Use the latest successful run for each suite. Screenshots and the native pocket
animation GIF are copied into `qol-pokeglass-preview/glass-bag/` in the workspace.
