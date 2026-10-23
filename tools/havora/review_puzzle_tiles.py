#!/usr/bin/env python3
"""Render the installed grass-backed puzzle kit from the actual metatiles."""
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from render import atlas

R = Path(__file__).resolve().parents[2]
data = json.loads((R / 'tools/havora/puzzle-tiles.json').read_text())
tiles = atlas('havora_city', 'havora_city')
out = Image.new('RGB', (1160, 560), '#172d34')
d = ImageDraw.Draw(out)
font = lambda size: ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', size)
d.text((28, 20), 'HAVORA / GRASS PUZZLE TILES', font=font(30), fill='#f3dfbc')
d.text((28, 64), 'Actual shared-tileset render • Native 16 × 16 pixels, enlarged without smoothing', font=font(19), fill='#c7d9cd')
labels = ['Boulder', 'Cut tree', 'Open shaft', 'Switch / released', 'Switch / pressed']
for i, ((name, mid), label) in enumerate(zip(data['assets'].items(), labels)):
    x = 28 + i * 226
    for y in range(3):
        for xx in range(3):
            source = tiles[mid] if (xx, y) == (1, 1) else tiles[0]
            out.paste(source.resize((64, 64), Image.Resampling.NEAREST), (x + xx * 64, 117 + y * 64))
    d.text((x, 325), label, font=font(19), fill='#f3dfbc')
    d.text((x, 355), f'Porymap: 0x{mid:03X}', font=font(18), fill='#c7d9cd')
d.text((28, 414), 'All five use the existing Havora grass underneath. Clear or fill a shaft with grass 0x000.', font=font(20), fill='#d6e1d7')
d.text((28, 452), 'Boulders and trees painted as tiles are scenery. Use object events for pushing and cutting.', font=font(19), fill='#d6e1d7')
d.text((28, 488), 'Switches expose the native Strength-button behavior; connect puzzle scripts when placing them.', font=font(19), fill='#b3c8c1')
dest = R / 'docs/havora/puzzle-tiles-preview.png'
dest.parent.mkdir(parents=True, exist_ok=True)
out.save(dest)
print(dest)
