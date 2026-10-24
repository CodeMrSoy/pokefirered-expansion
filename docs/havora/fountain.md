# Havora animated fountain

The original Celadon fountain is available in the shared
HavoraCityPrimary / HavoraCity pair, on both grass and paving. No maps have been
painted and no events, doors, borders, connections or cliff cells changed.

Assemble one complete 3-column by 4-row grid from
`tools/havora/fountain.json`. IDs in the preview are hexadecimal. Set the local
floor elevation and use the source collision mask in that manifest. The two
background versions share all fountain graphics and animation frames.

The animation retains five native frames at 12 ticks per frame. Two of Celadon's
eight source frame graphics are identical in every frame; these remain static.
Six changing graphics use reserved slots 553, 570, 571, 575, 576 and 578. Future
atlas edits must keep those slots reserved. Palette files are unchanged.

HavoraCity has its own secondary callback, combining the existing ocean update
with the fountain. A 1,920-tick common cycle preserves both animation phases.
The legacy HavoraHarbor callback stays unchanged. Peak transfer scheduling is
seven secondary DMA entries, or eight including General's primary animation,
within the engine's 20-entry queue.

24 new metatile definitions cover the two backgrounds. Only unplaced,
unprotected catalog remnants were reclaimed; their definitions and graphics are
archived in `tools/havora/fountain-archive.json`. All 266 currently placed
metatile definitions and all 563 protected authoring definitions retain their
original graphics and packed attributes.

Validation:

- ROM compilation passed with ARM GCC 13.2.1.
- `test_fountain_animation.py`: compiles the actual callback C functions and
  verifies 3,840 ticks, all five fountain frames, ocean phase, transfer sizes,
  destinations and the legacy callback.
- Existing topology, corner-buffer and housing preservation checks pass.
- `fountain.gif` is a five-frame native data preview, not an emulator capture.
- No in-game or Porymap UI test was performed.
