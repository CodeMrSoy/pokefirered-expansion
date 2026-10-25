# Main menu layout cleanup

Each card now owns its entire frame instead of sharing a border row with its
neighbor. The new-game-only list is centered vertically. Continue retains its
original size and font; all four normal saved-game cards fit the 160px screen.
The optional Mystery Gift card scrolls into view when selected, and message
windows reset that scroll before drawing.

The disabled seed stays on the same baseline as the randomizer status. Active
seeds use an unsigned decimal formatter so values above INT32_MAX no longer
start with a question mark. Seed generation and saved seed values are unchanged.

Verified a development ROM build, native randomizer on/off navigation, the
maximum seed 4294967295, Options entry/return, the real Continue screen after
flash-save/reset, preview fixtures for the optional fifth-card layout and its
message handling, and the existing Quantum title/Start emulator check. The
review image contains actual ROM captures. This change is scoped to QOL.
