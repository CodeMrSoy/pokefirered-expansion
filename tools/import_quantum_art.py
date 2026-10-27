#!/usr/bin/env python3
"""Convert supplied Vidra and PokéGlass art to native GBA indexed assets."""
import argparse
from pathlib import Path
import struct
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]

def palette_file(path, colors):
    path.write_text('JASC-PAL\n0100\n' + str(len(colors)) + '\n' + ''.join(f'{r} {g} {b}\n' for r, g, b in colors))

def tablet(source, size, destination, palette):
    source = source.convert('RGBA')
    mask = source.getchannel('A').point(lambda a: 255 if a >= 128 else 0)
    source = source.crop(mask.getbbox())
    source.thumbnail((size - 2, size - 2), Image.Resampling.LANCZOS)
    canvas = Image.new('RGBA', (size, size))
    canvas.alpha_composite(source, ((size - source.width) // 2, (size - source.height) // 2))
    rgb = canvas.convert('RGB')
    mask = canvas.getchannel('A').point(lambda a: 255 if a >= 128 else 0)
    samples = [p for p, a in zip(rgb.getdata(), mask.getdata()) if a]
    swatch = Image.new('RGB', (len(samples), 1)); swatch.putdata(samples)
    quantized = swatch.quantize(colors=15, method=Image.Quantize.MEDIANCUT)
    colors = [(255, 0, 255)] + [tuple(quantized.getpalette()[i:i + 3]) for i in range(0, 45, 3)]
    indices = rgb.quantize(palette=quantized, dither=Image.Dither.NONE)
    out = Image.new('P', (size, size)); out.putpalette([v for c in colors for v in c] + [0] * (768 - 48))
    out.putdata([v + 1 if a else 0 for v, a in zip(indices.getdata(), mask.getdata())])
    out.save(destination)
    palette_file(palette, colors)
    return colors

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('vidra', type=Path)
parser.add_argument('tablet', type=Path)
args = parser.parse_args()
folder = ROOT / 'graphics/vidra_arrival'; folder.mkdir(exist_ok=True)
scene = Image.open(args.vidra).convert('RGB')
assert scene.width * 2 == scene.height * 3, 'Arrival artwork must match the 3:2 GBA screen'
scene = scene.resize((240, 160), Image.Resampling.LANCZOS).quantize(colors=256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
scene.save(folder / 'vidra.png')
palette_file(folder / 'vidra.pal', [tuple(scene.getpalette()[i:i + 3]) for i in range(0, 768, 3)])
(folder / 'vidra.bin').write_bytes(b''.join(struct.pack('<H', y * 30 + x if x < 30 and y < 20 else 0) for y in range(32) for x in range(32)))
source = Image.open(args.tablet)
colors = tablet(source, 64, ROOT / 'graphics/poke_glass_tablet.png', ROOT / 'graphics/poke_glass_tablet.pal')
palette_file(ROOT / 'graphics/poke_glass_tablet_off.pal', [(r // 3, g // 3, b // 3) if b - r > 15 else (r, g, b) for r, g, b in colors])
tablet(source, 24, ROOT / 'graphics/items/icons/poke_glass.png', ROOT / 'graphics/items/icon_palettes/poke_glass.pal')
print('Imported 240x160 arrival art, 64x64 startup tablet and 24x24 Bag icon')
