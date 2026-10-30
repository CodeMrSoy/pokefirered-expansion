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
| 2 | Trainer Card, Options, Save | Debug, DexNav, Retire |

Debug follows the existing development-build setting (`make DEVELOPMENT=1`).
DexNav appears only if it is enabled and unlocked. Retire appears during a
Safari session; Save is unavailable during Safari and link sessions. Hidden
slots are skipped, including when a whole row is empty. Link and Union Room
sessions retain only Party, Bag, Trainer Card and Options.

Bag, Trainer Card, Options and Debug use their existing game screens. Save
uses the existing confirmation/overwrite flow and flash-save implementation.
The Pokédex and storage unlock restrictions remain in their script handlers.
Storage now opens the [embedded six-box management app](pokeglass-storage.md),
sharing the tablet window instead of opening the native PC interface.
Party and Stats require at least one Pokémon.

The wardrobe app, preview screen and outfit-changing task have been removed.
The new-game character selection still chooses the appearance saved with the
player. Existing saves retain their current appearance. The legacy wardrobe
special is a no-op so old script references cannot change outfits. Debug tools
are development tools and are not part of the normal outfit selection flow.

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
