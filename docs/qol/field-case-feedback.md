# Field case testing feedback

Both the Field Item Case and PokéGlass Field Kit retain the real tool names
and native 64px preview shapes. Uncollected tools appear as black silhouettes;
collecting a tool restores its original colors. Names stay grey until the
corresponding gym badge is earned, independently of ownership. Use still needs
both the tool and badge. Owned tools without a badge show a badge reminder.
The all-empty case starts on Pruning Shears. The earlier missing-tool text fix
also removed a pointer to a block-scoped compound literal.

The D-pad registration prompt now uses the Bag's native selection-text window
and frame, like the original "is selected" prompt. Cancel and actual directional
registration retain their existing behavior.

Verified with a development ROM build and the native mGBA fixtures:
`tests/field_case_empty_emulator.py` and `tests/field_item_case_emulator.py`.
Screenshots in `docs/qol/review` are actual ROM captures.

The discovery/badge presentation is covered by
`tests/field_kit_discovery_emulator.py`: all seven tools in both interfaces,
all four ownership/badge combinations, original sprite tile/transparency
preservation, preview palettes, name colors and blocked use. The release ROM
build and this emulator check pass with EWRAM unchanged at 238,828 bytes.

The Stellar Ticket script exists on Havora/V2, not QOL; its sailor-facing fix is
kept with that campaign rather than adding campaign maps/items to QOL.
