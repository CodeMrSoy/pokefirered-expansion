# PokéGlass rendering fixes — 2026-11-04

Fixes the shared-background text capture and Summary Info/Moves overlap reported
in player feedback.

The backdrop compositor now excludes BG palettes 13–15, which belong to menu
windows and text. Field tilesets own palettes 0–12. This keeps UI glyphs out of
the cached glass scenery while retaining the field, sprites and transparency.

Summary's removed Skills page left a gap in the page enum. The slide code had
inferred a source/target from adjacent enum values and revealed the Skills
background beneath Moves text. It now loads the actual destination artwork into
the incoming background layer. Direct Moves entry initializes the same layer,
scroll and flip parity as Info → Moves. Native slide animations are retained.

## Validation

Tested in an isolated native release build based on current V2 `09152042`, with
these two shared source files overlaid. Their pre-fix versions are identical
between QoL and V2. Recompiled both units and relinked; this was an incremental
build, not a clean build. EWRAM and IWRAM usage remain unchanged.

Both new emulator regressions fail on unmodified V2 and pass with the fixes:

- `tests/pokeglass_backdrop_text_emulator.py`: text-palette glyphs on a shared
  foreground BG must not alter the cached scenery or its palette. Identical
  core snapshots isolate the overlay from animated scenery and sprite frames.
- `tests/pokeglass_summary_graphics_emulator.py`: compares actual visible BG
  body tiles against destination artwork, rather than checking only page
  numbers. Covers repeated Info/Moves/detail transitions, Pokémon switching,
  direct Moves entry, unchanged party data and unlocked return to the field.

Also passed the existing overhaul-action, glass-Bag and Bag-action emulator
suites: original pocket graphics/bounce, scrolling, sorting, item-action
windows, Potion use, nested cases, retained inventory and launcher returns.
Visually checked the rendered Moves list, move details and direct Moves entry.

The original phone save/state from the report was unavailable; the backdrop
regression recreates the text-capture failure with a controlled foreground
window overlay. Phone/browser-specific rendering was not tested.

Workspace logs are under `v2-integration-test/results/` with names ending in
`20261104`. Early backdrop-test attempts placed the overlay off-screen because
of camera scrolling; the final test accounts for that scroll and correctly
fails before the fix.

## Follow-up: stale heap allocation behind the Bag

The capture-palette filter alone did not resolve the player's remaining text
fragments. Repeated real Party/Stats/Pokédex/Bag visits reproduced entire UI
fragments in the Bag scenery. The captured bytes in VRAM matched the cached
bytes, ruling out a later Bag upload overwriting them in this reproduction.

Returning to the overworld relocates save blocks using `gHeap`, then resets the
allocator. `ReleasePokeGlassBackdrop` intentionally retained the snapshot during
a launcher session, leaving its pointer aimed at an allocation that no longer
existed. New window allocations could reuse that memory.

The overworld heap-reset boundary now explicitly invalidates the snapshot.
Party return captures the rebuilt field before installing the tablet window;
other native returns capture it when reopening the hub. An existing valid
snapshot is reused between apps rather than recapturing UI graphics. This adds
no persistent buffers or EWRAM/IWRAM usage.

`tests/pokeglass_backdrop_session_emulator.py` exercises three complete cycles
of Party, Stats, Pokédex, Map and Bag. It checks the snapshot allocation's live
heap header and separation from every active window buffer, checks Bag VRAM
against the snapshot, and verifies release on close and fresh capture on a
different map. The current published ROM fails this regression after the first
Party return. The fixed ROM passes all fifteen visits, and its Bag screenshots
were visually checked after repeated cycles.
