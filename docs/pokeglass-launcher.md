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

TM Case keeps the original gold case picture, type-colored discs and native
insertion/ejection animation. Its surrounding UI matches the other PokéGlass
apps: translucent field backdrop, cyan panel rules, compact light text and
matching context/error menus. The selected move and type share the header;
Power (Pow), Accuracy (Acc) and PP sit beneath the case in three columns. The
right panel holds the move list and quantities; descriptions wrap into the
lower panel. The launcher still uses a disc icon. Trainer Card, Save and Options
remain the final three apps.

The original case pixels come from the native TM case tilemap and artwork.
`tools/compile_pokeglass_native_tm_case.py` removes only the surrounding old
screen background and encodes those pixels in
`src/data/poke_glass_native_tm_case.h`. The original male/female palette bank
is loaded directly from the native assets. The case and disc share an eight-pixel
horizontal shift to fit the bezel; native vertical positions and 0/10/20-pixel
swap offsets are retained. The native case layer stays in front of the sinking
disc. Empty/CLOSE hides it only after insertion finishes.

Bag and registered-item routes keep their callbacks. Teaching/cancelling the
Pokémon choice returns to the case; B returns to its selected launcher tile.
Outside a PokéGlass session, the original regular UI remains. No experimental
SD-card art is loaded. Saved experiments remain as unused reference assets.

The case uses BG2 art tiles at 0xCC20..0xD080 and a transparent tile at 0xCC00,
separate from text/panel/frame tiles, the captured field and the BG2 tilemap at
0xE800. No persistent EWRAM or new heap allocation is needed. Build usage is
238,828 bytes EWRAM; the local build log records the final ROM size.

`tests/pokeglass_tm_case_emulator.py` compares the disc data with the original
ROM asset, compares every opaque case pixel and both palettes with the native
assets, and checks native animation, CLOSE/reopen, rapid scrolling and return.
`tests/pokeglass_tm_layout_emulator.py` covers glass panels and action borders,
a dense list, scrolling, context/no-party handling and disjoint window graphics.
The teaching/Continue, Bag actions and repeated-session suites cover the normal
callbacks, item consumption and resource cleanup.

Evidence is saved under `emulator-qol-glass-original-case` (animation and real
teaching/save/reset/Continue), `emulator-qol-glass-original-case-final`
(exact original assets, glass layout/actions, Bag, eight-session cleanup), and
`emulator-qol-glass-original-case-palettes` (final original assets and both
palette banks) in the workspace's `v2-integration-test/results/` directory.


The stat labels and values use adjacent 16-pixel windows, so their tilemaps do
not cover each other. Text has room for its complete glyph height. Lower action
and error panels draw their cyan borders inside the panel rather than over the
stat row. Selecting Use restores the stat tilemaps before a no-Pokémon error.
The layout regression compares every expected stat foreground pixel with the
actual screen on the list, in action/error panels, and after returning. Evidence
for this clipping fix is under `emulator-qol-tm-stats-clipping-final`; the earlier
run caught the error-screen cleanup clearing part of the values.
