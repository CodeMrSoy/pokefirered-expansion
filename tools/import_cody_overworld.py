#!/usr/bin/env python3
"""Import Cody's supplied 40x40 atlas into FireRed's native frame layouts.

Only overworld sheets/palettes and the map icon are written. The trainer
portrait and battle back sprite have separate palettes and remain untouched.
"""
import json
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'graphics/avatars/cody'
SOURCE = DEST / 'source/overworld'


def main():
    metadata = json.loads((SOURCE / 'atlas.json').read_text())
    atlas = Image.open(SOURCE / 'atlas.png').convert('RGBA')
    assert atlas.size == (metadata['size']['w'], metadata['size']['h'])
    frames = {}
    for f in metadata['frames']:
        assert f['w'] == f['h'] == 40
        frames[f['id']] = atlas.crop((f['x'], f['y'], f['x'] + 40, f['y'] + 40))

    def frame(direction, animation, index, width=16):
        image = frames[f'{direction}-{animation}-{index}']
        # Fixed crop origins preserve the supplied walking bob and foot positions.
        if animation in ('walk', 'idle', 'run'):
            return image.crop((12, 4, 28, 36))
        if animation == 'cycle':
            return image.crop((4, 4, 36, 36))
        if animation == 'fish':
            # Rods reach all four edges; fit the entire cell without clipping.
            return image.resize((32, 32), Image.Resampling.NEAREST)
        if animation == 'surf':
            # FireRed renders the mount as a field effect. Export only the rider.
            result = Image.new('RGBA', (16, 32))
            result.paste(image.crop((12, 7, 28, 24)), (0, 14))
            return result
        assert direction == 'down' and animation == 'use_pokeball'
        return image.crop((11, 4, 29, 36)).resize((16, 32), Image.Resampling.NEAREST)

    def sheet(images, width):
        result = Image.new('RGBA', (len(images) * width, 32))
        for i, image in enumerate(images):
            assert image.size == (width, 32)
            result.paste(image, (i * width, 0))
        return result

    directions = ('down', 'up', 'left')  # The engine mirrors left for right.
    normal = [frame(d, 'idle', 0) for d in directions]
    normal += [frame(d, 'walk', i) for d in directions for i in (0, 2)]
    bike = [frame(d, 'cycle', 1) for d in directions]
    bike += [frame(d, 'cycle', i) for d in directions for i in (0, 2)]
    running = [frame(d, 'run', i) for d in directions for i in (1, 0, 2)]
    # Last two slots are addressed by the base animation table's extra poses.
    running += [frame('down', 'idle', 0)] * 2
    surf = [frame(d, 'surf', 0) for d in directions]
    fishing = [frame(d, 'fish', i, 32) for d in ('left', 'up', 'down') for i in range(4)]
    item = Image.open(SOURCE / 'legacy_item.png').convert('RGBA')
    # This export only supplies the down-facing throw. Never import the N/A text.
    for i, source_index in enumerate((0, 1, 2, 3, 3)):
        item.paste(frame('down', 'use_pokeball', source_index), (i * 16, 0))
    sheets = {
        'normal': sheet(normal, 16),
        'surf_run': sheet(surf + running, 16),
        'bike': sheet(bike, 32),
        'fish': sheet(fishing, 32),
        'item': item,
        'vs_seeker_bike': Image.open(SOURCE / 'legacy_vs_seeker_bike.png').convert('RGBA'),
    }
    # Build one shared palette from actual runtime pixels, excluding N/A labels.
    pixels = [p[:3] for image in sheets.values() for p in image.get_flattened_data() if p[3]]
    strip = Image.new('RGB', (len(pixels), 1))
    strip.putdata(pixels)
    quantized = strip.quantize(colors=15, method=Image.Quantize.MEDIANCUT)
    colors = quantized.getpalette()[:45]
    palette = np.array(colors, dtype=np.int32).reshape(15, 3)

    def indexed(image):
        rgba = np.asarray(image.convert('RGBA'))
        rgb = rgba[:, :, :3].astype(np.int32)
        indices = (((rgb[:, :, None] - palette) ** 2).sum(3).argmin(2) + 1).astype('uint8')
        indices[rgba[:, :, 3] == 0] = 0
        result = Image.fromarray(indices).convert('P')
        result.putpalette([0, 0, 0] + colors + [0] * 720)
        result.info['transparency'] = 0
        return result

    for name, image in sheets.items():
        indexed(image).save(DEST / f'{name}.png', bits=4)
    indexed(normal[0]).save(DEST / 'source/overworld_down_16x32.png', bits=4)
    indexed(normal[0].crop((0, 10, 16, 26))).save(DEST / 'map.png', bits=4)
    text = 'JASC-PAL\n0100\n16\n0 0 0\n' + ''.join(
        f'{colors[i]} {colors[i+1]} {colors[i+2]}\n' for i in range(0, 45, 3))
    for name in ('overworld', 'map'):
        (DEST / f'{name}.pal').write_text(text)


if __name__ == '__main__':
    main()
