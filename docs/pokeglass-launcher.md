# PokéGlass launcher

Start opens PokéGlass directly. The old Start list is no longer displayed,
including when returning from a field item or another native menu.

Each page has a three-column, two-row grid. Left/right moves between apps;
moving past either row's left or right edge opens the other page. Up/down
moves within the current column. Page dots show which page is open. B closes
the launcher and releases field controls. Returning from an app keeps its tile
selected.

| Page | Top row | Bottom row |
| --- | --- | --- |
| 1 | Pokédex, Party, Storage | Map, Stats, Bag |
| 2 | Field Kit, TM Case, utility slot | Trainer Card, Save, Options |

Field Kit is always available and shows owned and missing field tools. TM Case
is available even with no TMs, and uses the normal teaching and item rules.
The top-right utility slot shows Retire during Safari; outside Safari it shows
DexNav if that optional feature is enabled and unlocked. Save is unavailable
during Safari and link sessions. Hidden
slots are skipped, including when a whole row is empty. Link and Union Room
sessions retain only Party, Bag, Trainer Card and Options.

Bag, Trainer Card and Options use their existing game screens. Bag, its TM and
Berry cases, Party and Town Map use the shared tablet border. Save
uses the existing confirmation/overwrite flow and flash-save implementation.
The Pokédex and storage unlock restrictions remain in their script handlers.
Storage now opens the [embedded six-box management app](pokeglass-storage.md),
sharing the tablet window instead of opening the native PC interface.
Party and Stats require at least one Pokémon.

The wardrobe app, preview screen and outfit-changing task have been removed.
The new-game character selection still chooses the appearance saved with the
player. Existing saves retain their current appearance. The legacy wardrobe
special is a no-op so old script references cannot change outfits. Field Kit uses the existing field-tool ownership, badge checks and callbacks;
the Bag's Field Item Case remains available.

## Validation

`tests/pokeglass_grid_emulator.py` exercises direct Start access, page changes
in both directions, all available app launches and returns, Save cancellation
and an actual flash write, unchanged outfit data, field unlocking, and reopening.
It works with standard and development ROMs. The avatar regression now checks
that the retired wardrobe function cannot change the saved appearance. Existing
PokéGlass emulator fixtures use the direct Start entry point.

Verified with standard and `DEVELOPMENT=1` ROM builds, the two-page launcher
emulator regression, the Storage/Town Map regression (real deposits and
withdrawals), the repeated Party-return regression (12 returns across four
locations), and the avatar regression (all seven appearances, battle backs,
Fly landing, and real save/reset/Continue). The standard-build launcher check
also exercises the native field-item return callback. Live multiplayer sessions
were not exercised in the emulator.

## Full-screen glass

The shared frame fills the 240×160 display, with a ten-pixel red-and-white edge bezel and
a 220×140 translucent work area. The launcher and Storage use the expanded
space. Embedded apps share the larger window; native app returns use the same
frame geometry. Storage uses a slightly darker glass tint for dense text.
The frame and its native-app tiles are generated together by
`tools/compile_pokeglass_frame.py`.

## App presentation

The launcher shows a description for the selected app. Pokédex uses a wider
six-entry list with Seen/Caught filters, alphabetical sorting, portraits, cries
and habitat paging. Party has six wider cards with Pokémon icons and readable
HP, level, status and nickname fields.

Stats has three SELECT-switched pages: values/EVs/IVs, profile (types, nature,
ability and item), and training (experience, next level, friendship and totals).
L/R changes party member. Eggs conceal their stat data. Summary retains its
identity and moves pages; left/right skips its redundant Skills page.

Field Kit lists the seven permanent field tools. Owned tools show their icon
and can be used through the established field callbacks when badge and field
conditions allow. Missing tools remain visible without being usable.

For the current overhaul's executed checks and limitations, see
[pokeglass-overhaul-qa.md](pokeglass-overhaul-qa.md).

## TM Case app

The TM Case tile opens the regular case inside the PokéGlass tablet border,
using the original gold case picture, type-colored discs, native list/stat
panels, and the original insertion/ejection animation. The launcher icon is a
disc again. B returns to the selected TM Case tile on page two. Trainer Card,
Save and Options remain the final three apps.

The Bag and registered-item routes remain available with their existing return
callbacks. Teaching and cancelling the Pokémon choice return to the case;
closing it returns to PokéGlass. Native TM consumption and flash saves are
unchanged. No SD-card artwork is loaded by the active TM screen. The experimental
art and its generator remain saved as unused assets for future reference.

The native case implementation is restored from the direct-app baseline
`b611c0a0`; later launcher ordering, Bag styling and other apps are retained. The regular
list starts at its original top row so a full list and CLOSE fit above the lower
panel border inside the tablet.
`tests/pokeglass_tm_case_emulator.py` compares the loaded disc graphics with the
original compressed ROM asset and checks the gold case, native 0/10/20-pixel
swap offsets, CLOSE/reopen, rapid scrolling and field return.
`tests/pokeglass_tm_layout_emulator.py` covers the regular list, scrolling,
context and no-party message, and window tile bounds.
`tests/pokeglass_tm_app_emulator.py` checks empty access, compatible teaching,
cancellation, real TM consumption, repeated entry and flash save/reset/Continue.
The previous `pokeglass_tm_cards_emulator.py` path now delegates to the regular
case regression for compatibility with older suite commands.

Build and emulator evidence for this restoration is saved under
`v2-integration-test/results/emulator-qol-restore-native-tm` in the workspace. Final native layout/animation reruns are under
`emulator-qol-restore-native-tm-final` (original assets/animation) and
`emulator-qol-restore-native-tm-verified` (native layout/actions). Earlier
harness failures sampled the green frame rather than the cream panel or tried
to run a field-script helper inside the case; these are not counted as passes.
