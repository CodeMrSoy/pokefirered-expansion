# PokéGlass overhaul verification — 2026-10-31

Target: QOL, based on 82967008. V2 is not changed by this work.

The native ARM release build completes with warnings limited to the existing
linker's RWX load segments. Linked use: EWRAM 238,828/262,144 bytes (91.11%),
IWRAM 27,573/32,768 bytes (84.15%), ROM 21,823,308/33,554,432 bytes (65.04%).
The Windows make dependency scan stalls in this environment, so changed C
translation units were preprocessed, compiled and assembled using the existing
release flags, then linked in the existing map's object order. This verifies
the linked incremental release ROM, rather than a clean-from-scratch build.

## Executed checks

Emulator: mGBA 0.11 libretro. Fixtures create populated parties, boxes, items
and known flags; these are behavior checks, not a full campaign playthrough.

- Launcher: both pages, app launches/returns, Save cancel and actual flash save.
- PC: 36-slot D-pad navigation, six-box wrap, move/swap/cancel, item actions,
  full Bag and last-able-mon guards, release confirmation, inspection and
  flash reset/Continue. Legacy 0/1/180-mon conversion and 181-mon refusal.
- Stats: all three pages, nature colors, Eggs, party wrapping, read-only data
  and repeated portrait/session cleanup.
- Field Kit: missing-tool rejection, badge gating and actual Lantern use with
  ownership retained and field controls restored.
- Summary: Info/Moves navigation skips Skills and returns through Party.
- Move learning: real Rare Candy into a fifth move, old/new descriptions,
  long names, cancellation and Summary return.
- Bag: real Potion healing/consumption, pocket switching, TM/Berry case entry
  and cancel, correct Berry names, retained Field Item Case and launcher return.
- Party: long names, level digit growth, 3-digit HP, thresholds/healing,
  actual candy stat popups; loading checks for stale sprites and blank frames.
  All 12 returns across bedroom/one, bedroom/six, Viridian and Cerulean retain
  a stable physical bezel and cover, then restore field controls.
- Pokédex: empty/seen/caught lists, alphabetical sort, cries, multiple habitat
  pages, cross-generation entries, cleanup and flash reset/Continue.
- Resources: repeated app sessions return transient allocations and palettes;
  benchmark verifies visible shell and responsive app transitions.

Party card width and shell pixel masks were updated in the tests to match the
new 104-pixel cards and ten-pixel bezel. Transparent rounded outside corners
are excluded from bezel equality checks because they reveal the field. Summary tests use the actual compiler
layout; the move-learning fixture now sets the PokéGlass unlock flag before END.
Earlier failing harness runs are retained in local logs, not counted as passes.

## Visual scope

Populated emulator captures cover both launcher pages, Pokédex, Party, PC,
Bag, Town Map, Stats/profile/training and Field Kit. Native map artwork remains
opaque for readability and scrolls inside the tablet viewport. The native Bag
keeps its existing pockets, item actions and nested cases. Wardrobe is absent.
Live multiplayer and a physical GBA were not tested.

Local evidence groups (under `v2-integration-test/results/` in the workspace):
`emulator-qol-overhaul-validation`, `emulator-qol-overhaul-bag`,
`emulator-qol-overhaul-final`, `emulator-qol-overhaul-complete`, and
`emulator-qol-overhaul-release`. Use the latest successful rerun for a given
suite; the earlier Bag item-ID and rounded-corner mask failures are preserved.
The complete group includes eight sessions with Field Kit allocation checks.
