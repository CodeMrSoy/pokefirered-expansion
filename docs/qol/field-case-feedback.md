# Field case testing feedback

Unowned tools now retain their real names and native 64px previews. Names and
previews are grey, the footer still says "Tool not collected", and A cannot
launch them. The all-empty case starts on Pruning Shears. This also removes a
pointer to a block-scoped compound literal that caused corrupt missing-tool text.

The D-pad registration prompt now uses the Bag's native selection-text window
and frame, like the original "is selected" prompt. Cancel and actual directional
registration retain their existing behavior.

Verified with a development ROM build and the native mGBA fixtures:
`tests/field_case_empty_emulator.py` and `tests/field_item_case_emulator.py`.
Screenshots in `docs/qol/review` are actual ROM captures.

The Stellar Ticket script exists on Havora/V2, not QOL; its sailor-facing fix is
kept with that campaign rather than adding campaign maps/items to QOL.
