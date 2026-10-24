#!/usr/bin/env python3
"""Import the approved field-tool illustrations as native GBA item icons.

Requires Pillow, numpy and scipy. The original uploads are preserved in
tools/field_tool_sources. Their checkerboard is baked into RGB, so recover the
outline and remove the explicitly identified hollow regions before resampling.
These coordinates describe background holes, never alterations to the artwork.
"""
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'tools/field_tool_sources'
OUT = ROOT / 'graphics/items/field_tools'
HOLES = {
    'shears': [(780, 1130), (1100, 930)],
    'gloves': [],
    'lantern': [(770, 270)],
    'whistle': [(1300, 390), (1030, 735)],
    'hammer': [],
    'bait': [(1300, 400)],
    'wailmer_wailer': [(1360, 620)],
}


def import_icon(name, holes):
    rgb = np.array(Image.open(SOURCE / (name + '.png')).convert('RGB'))
    high, low = rgb.max(axis=2), rgb.min(axis=2)
    # Seal tiny export seams so the blade's pale interior stays in the mask.
    seed = (high < 145) | ((high.astype(int) - low) > 28)
    closed = ndimage.binary_closing(seed, iterations=2)
    labels, _ = ndimage.label(closed)
    counts = np.bincount(labels.ravel())
    counts[0] = 0
    mask = ndimage.binary_fill_holes(labels == counts.argmax())
    neutral = ((high.astype(int) - low) < 18) & (low > 175)
    labels, _ = ndimage.label(neutral)
    for x, y in holes:
        region = labels[y, x]
        assert region, (name, 'background seed is not neutral', x, y)
        mask[labels == region] = False
    rgba = Image.fromarray(np.dstack([rgb, mask.astype('uint8') * 255]))
    rgba = rgba.crop(rgba.getbbox())
    rgba.thumbnail((22, 22), Image.Resampling.BOX)
    reduced = np.array(rgba)
    opaque = reduced[:, :, 3] > 110
    # Foreground-only quantization reserves index zero for true transparency.
    strip = Image.fromarray(reduced[:, :, :3][opaque].reshape(1, -1, 3))
    quantized = strip.quantize(colors=15, method=Image.Quantize.MEDIANCUT,
                              dither=Image.Dither.NONE)
    colors = [(c >> 3) << 3 for c in quantized.getpalette()[:45]]
    palette = [180, 180, 180] + colors
    palette += [0] * (768 - len(palette))
    indices = np.zeros(opaque.shape, dtype=np.uint8)
    indices[opaque] = np.array(quantized).ravel() + 1
    icon = Image.fromarray(indices)
    icon.putpalette(palette)
    canvas = Image.new('P', (24, 24))
    canvas.putpalette(palette)
    canvas.paste(icon, ((24 - icon.width) // 2, (24 - icon.height) // 2))
    assert max(canvas.get_flattened_data()) < 16
    bounds = canvas.getbbox()
    assert min(bounds[:2]) >= 1 and max(bounds[2:]) <= 23
    canvas.save(OUT / (name + '.png'), transparency=0, optimize=False)
    (OUT / (name + '.pal')).write_text('JASC-PAL\n0100\n16\n' + '\n'.join(
        ' '.join(map(str, palette[i:i + 3])) for i in range(0, 48, 3)) + '\n')


if __name__ == '__main__':
    OUT.mkdir(parents=True, exist_ok=True)
    for name, holes in HOLES.items():
        import_icon(name, holes)
