# Storage app redesign

The tablet storage screen now uses a solid PC-style display instead of blending the box with the overworld. The 30-slot box stays fixed on the right. The left side shows the selected Pokémon's front sprite, nickname, level and gender; opening Party replaces that preview with six party slots without shifting the box. Box name, occupancy and L/R controls remain visible.

A picks up and places Pokémon. Moving a carried Pokémon onto Party opens the party panel. The carry cursor turns red, and an occupied destination's icon is hidden beneath the carried sprite so the two sprites do not overlap. B cancels carrying before closing the party panel or app. L/R change boxes, including while carrying; SELECT retains release and box rename actions.

Grid sprites survive cursor movement and party-panel toggles. Only changed/hidden icons are recreated. The selected/held icon animates. The front-sprite buffer is reused for different selections. Closing storage frees its preview, icons and palettes, then restores the launcher's palette and transparency after the screen wipe. The tablet shell remains unchanged during entry.

The storage data path and save format are unchanged. Picking up still retains the source data until a validated placement commits. The existing party, release, field-move, Egg, held-item and recovery guards remain in place.

## Verification

`tests/pokeglass_storage_visual_emulator.py` adds release-ROM checks for an opaque screen, fixed grid coordinates and sprite IDs when opening Party, preview reuse, all 36 icons, carrying from the last box slot, ten repeated opens/closes without leaked sprites, unchanged party data, every exit frame retaining the tablet shell, carry icons staying inside the bezel even over the Party button, and a pixel-identical launcher return. It is included in `tests/run_qol_regressions.py`.

The existing storage regressions exercise deposits, swaps, cancellation across boxes, last-usable-member protection, actual Flash save/reset/Continue, default-No release, party/box release, rename/cancel, Eggs, sole Surf users, boxed replacements and held-item conservation. The tablet transition test checks every entry frame for shell changes and black flashes.

Release and development builds pass. Release linked ROM usage is 21,410,564 bytes (2,100 bytes above the pre-redesign build), with 258,352 bytes EWRAM and 27,573 bytes IWRAM. Save structures and species IDs are unchanged.

Test ROM SHA-256: `96ffe0d715a2c409d6455d5e5467adfe951d7fd69ca03f5cfb5842ebd27f3f33`.

The complete 25-check release regression run passed. After the final sprite-boundary adjustment, all six storage/launcher/transition checks were rerun against the downloadable ROM.
