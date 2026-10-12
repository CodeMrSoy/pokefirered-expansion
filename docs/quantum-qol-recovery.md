# Quantum V1 QOL recovery

Recovered on 2026-10-12 from published commit
`62bd66518fe31cdd9398d8910b5efe7218a0493d` and the implementation notes for
the uncommitted Emerald QOL test build. This reconstructs the source; it is not
claimed to be a byte-identical reproduction of that earlier test ROM.

Restored features:

- DS party cards in the PokéGlass bezel with the translucent field backdrop,
  row-based navigation, HP text, and safe window allocations during swaps.
- Item descriptions for ground pickups and NPC gifts, with loaded borders,
  correctly sized windows, and bounded description formatting.
- Physical, special, and status icons in move selection.
- Persistent battle type badges following the health boxes.
- Slower tablet rise, power-on lighting, and hold animation.

Battle icon fixes:

- Expanded the legacy half-symbol tabs into complete symbols. The follow-up
  compact design uses 12-by-10-pixel badges inside native 16-pixel sprites,
  with crisp pixel symbols and a one-pixel frame.
- Positioned badges against health boxes in single and double battles.
- Kept both palettes and tile banks correct when displayed types change.
- Draw badges above neighbouring health-box shadows so all symbols remain
  visible in double battles.
- Moved category icons inside the move panel and matched their background
  to the panel's palette, preserving its right border.

Validation:

- ARM GCC 13.2.1 ROM build passed.
- `tests/quantum_qol_emulator.py` passed against the rebuilt ROM and ELF,
  using mGBA 0.10.2. Checks include a new-game boot, six party members,
  tablet/party opening, navigation, a real party swap, single/double battles,
  and ground/gift description dismissal. PNGs are written under
  `build/quantum-qol-tests` for visual inspection.
- Visual inspection covered physical, special, status, all four double
  battle boxes, the preserved party bezel, and item description frames.
- `test/host/cap_candy.py`: 12 sanitizer boundary cases passed.
- `tests/randomizer_regressions.py`: passed.
- No full-game playthrough was performed.

For the emulator check, install Pillow, NumPy, an mGBA libretro core, and ARM
binutils. Set `MGBA_CORE` when the core is not at the default Linux path and
`ARM_NM` when `arm-none-eabi-nm` is not on PATH. Build the ROM first, then run:

```sh
python3 tests/quantum_qol_emulator.py
```


## PokéGlass reference design and Stats app

The tablet now uses red corner grips, ivory shell panels, a graphite bezel,
and cyan app symbols, with matching bag and startup art. Startup lights the
screen before revealing its app symbols. The field stays visible through the
glass. The hub preserves the Stats shortcut beside its four main apps.

Stats opens a dedicated field overlay rather than the party/summary workflow.
It shows a front portrait, nickname, level, current ability, and six rows of
actual stats, EVs and IVs. HP uses maximum HP. Left/right wraps through party
members; B resumes the hub script. Eggs show a portrait but hide stats and
ability. The portrait buffer and tiles are reused during navigation, with a
private OBJ palette released on exit.

Validation: ARM build and `tests/quantum_qol_emulator.py` passed. The additional
`tests/pokeglass_stats_emulator.py` uses distinct EV/IV values, checks egg
handling and wraparound, switches portraits 36 times, opens/closes the app
eight times, and verifies that party data is unchanged and the script resumes.
Native-resolution emulator captures were inspected for column placement,
portrait colors, and return to the hub.


## Minior title formation

The title uses the native meteor-form Minior sprite and palette. Three Minior
travel in a diagonal V from the top-left to the bottom-right, with their trails
following the same slope. A shared clock preserves the formation through the
offscreen pause and next pass. The space scene, planet, and Quantum Version
text remain in place. `tests/quantum_title_emulator.py` passed checks for three
Minior, 18 trail sprites, constant offsets, diagonal motion, a synchronized
pause/loop, and transition to the main menu with Start. Emulator frames were
visually inspected.

## Shared opaque tablet shell

The app hub, Stats screen, and party picker now draw the same inset tablet
shell. Hardware window masking limits alpha blending to the blue display;
the ivory panels, red grips, camera, and home button remain opaque. The six
party cards use cyan app borders inside that display, with matching hints and
Cancel control. Deduplicated shell tiles occupy reserved VRAM at 0x7000;
party cards, action menus, and field-move help use separate tile allocations.

Closing a field tablet clears its tilemap before restoring the original palette
and window registers, then captures the backdrop after VBlank. This removes
the brief pink/grey recoloring when opening Party. Footer text stays inside
the glass. The ARM build, existing QOL and Stats emulator checks, and new
`tests/pokeglass_shell_emulator.py` checks passed. Native-resolution captures
and the frame-by-frame Party transition were inspected.
