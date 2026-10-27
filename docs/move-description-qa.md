# Move description layout audit

The QoL ROM's 935 compiled move descriptions are checked using the actual
Latin glyph widths from the built ROM and the current UI window dimensions.
Summary allows 113 pixels per line and four normal-font lines. The Move
Relearner's box also holds four lines. Battle uses a compact, nine-tile-high
popup with space for its header and four small-font description lines.

The audit found six descriptions too wide for Summary: Disable, Poison Gas,
Tri Attack, Cotton Spore, Uproar and Tail Glow. Five more exceeded its four-line
height: Hyper Beam, Giga Impact, Rock Wrecker, Volt Tackle and Thunderous Kick.
These descriptions were rewrapped or shortened, including their nearby
conditional variants. Move mechanics are unchanged.

The battle popup previously had room for only its header plus two lines in its
16-pixel font. It now sits above the move panel, uses the standard small font,
and holds every description in full. Its category-icon graphics occupy a
separate tile range. Healthbox type badges hide while the popup is open and
return when it closes.

Validation:

- Standard ROM build and whitespace check passed.
- `tests/move_description_layout.py`: all 935 compiled descriptions fit Summary,
  Move Relearner, standard battle and Battle Arena; battle tile ranges do not
  overlap or exceed their character block.
- `tests/move_description_emulator.py`: all 11 formerly overflowing Summary
  descriptions and a four-line control rendered in mGBA. The four-line battle
  popup was inspected visually; closing it restores the entire move panel
  byte-for-byte at the pixel level.
