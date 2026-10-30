# PokéGlass Storage

Storage is an embedded tablet app. It uses the launcher's existing window and
tile buffer instead of loading the native PC menu and its storage-screen data.
Six boxes provide 180 slots. Party and box slots appear side by side; six box
entries are visible per page, across five pages.

## Controls

- D-pad: choose a row or switch between party and box.
- L/R: previous/next box, wrapping through six boxes.
- Start: next page in the current box, wrapping after page five.
- A: select a Pokémon, then place it in an empty slot or swap it with another.
- B: cancel a selected move; otherwise return to the launcher.
- Select: take a held item, or choose an eligible Bag item to give to an empty-handed Pokémon.
- Select while moving a Pokémon: open a separate Release confirmation. A confirms;
  B keeps the Pokémon. Held items return to the Bag before a release succeeds.

Moves retain their source record until the destination is confirmed. Mail,
full-Bag item transfers, Eggs on release, and the last able party Pokémon are
protected. Successful party changes compact the party immediately. Existing
PC healing/PP rules apply to deposits and withdrawals. Giving Mail and giving
items to Eggs use the existing restrictions rather than creating orphaned Mail.

## Memory and save compatibility

The active `PokemonStorage` is six boxes. Its ASLR allocation drops from 34,272
to 14,992 bytes: **19,280 bytes of permanent EWRAM reclaimed**. The general heap
size is unchanged. Opening Storage does not allocate another screen, box cache,
or moving-Pokémon buffer; the selection is a few task fields and moves use
temporary stack records.

Flash still uses the established fourteen-box layout and nine storage sectors.
Serialization writes six live boxes at their original offsets, zeroes the eight
retired box ranges, and preserves box metadata and legacy fusion/recovery records.
Sector lengths, checksums, rotation, SaveBlock3 tails and backup slots retain
their existing format. This saves RAM rather than reducing the flash file size.

On load, a temporary legacy-sized heap buffer is freed after conversion. Pokémon
already in boxes 1–6 keep their positions. Occupied slots in boxes 7–14 move into
available slots in boxes 1–6; current-box selection is clamped, and the first six
box names/wallpapers are retained. Loading alone never writes the save.

If a legacy save contains more than 180 boxed Pokémon, the game displays a
conversion message and blocks Continue/New Game at that screen. The flash is
left unchanged. Open a backup with the previous ROM, bring the boxed count to
180 or fewer, save, and retry this ROM. Do not delete the save. Temporary-buffer
allocation failure also blocks this path rather than permitting a partial load.

The change is developed on `QOL`; merging it into V2 is a separate integration.

## Regression coverage

- `tests/pokeglass_native_apps_emulator.py`: Town Map and real tablet storage
  navigation, transfers, swaps/cancellation, held items, release confirmation,
  last-mon protection and flash reset/Continue.
- `tests/pokeglass_storage_migration_emulator.py`: real checksummed legacy flash
  fixtures at 0, 1 and 180 boxed Pokémon, including box 14; retained recovery
  records; 181-mon refusal without flash writes.
- `tests/pokeglass_resources_emulator.py`: repeated sessions and equal heap
  allocation before/after opening Storage.
- Launcher and transition regressions expect the embedded Storage task.
