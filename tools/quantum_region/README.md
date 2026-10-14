# Quantum island map

Regenerate the map assets from the repository root:

```sh
python3 -m pip install -r tools/quantum_region/requirements.txt
python3 tools/quantum_region/generate.py
```

The indexed `terrain.png` supplies the simplified island geography. The
generator overlays the existing 22 by 15 region-map cursor grid at 8 pixels
per cell, producing a 176 by 120 map image, palette, native 4bpp atlas,
tilemaps, buttons, region picker, and section metadata.

Five red circles identify the existing towns at their current Fly positions.
Hot Springs uses a small square. Seven additional cave/POI squares are
artwork placeholders recorded in `planned_pois.json`; they do not register
playable maps, names, warps, or Fly destinations.

The original 320 atlas tiles are preserved. Similar terrain tiles are merged
to fit BG0's 512-tile allocation; route and marker tiles are protected.
Exact tile patterns, including hardware flip variants, are reused. The
generator checks the remaining 192-tile budget before writing the atlas.
