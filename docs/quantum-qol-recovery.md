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

- Expanded the legacy half-symbol tabs into complete 16-pixel badges.
- Positioned badges against health boxes in single and double battles.
- Kept both palettes and tile banks correct when displayed types change.
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
