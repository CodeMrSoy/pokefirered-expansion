# Corvala tide authoring

`low.bin` is the current 80 × 64 LOW layout, identical to the installed map.
The generator intentionally builds LOW only pending composition review.

`legacy_56x60/` preserves the old low/mid/high experiments unchanged. Those
files have different dimensions and must never be loaded into the resized map.
No runtime tide switching is implemented. Derive new MID/HIGH from the approved
LOW geography before implementing a controller and safe player transitions.
