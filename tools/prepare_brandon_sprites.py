#!/usr/bin/env python3
"""Convert Brandon's reference-derived art and pose atlas to native, indexed GBA sheets.

No dithering: every exported PNG uses transparent index zero and at most
15 opaque colors. Run from any directory after replacing source/poses.png.
"""
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'graphics/avatars/brandon'
SOURCE = DEST / 'source'


def indexed(image, colors):
    rgba = np.asarray(image.convert('RGBA'))
    rgb = rgba[:, :, :3].astype(np.int32)
    palette = np.asarray(colors, dtype=np.int32)
    distances = ((rgb[:, :, None, :] - palette[None, None, :, :]) ** 2).sum(3)
    pixels = distances.argmin(2).astype(np.uint8) + 1
    neutral = (rgb.max(2) - rgb.min(2) < 18) & (rgb.max(2) < 120)
    neutral_ids = np.array([0,1,2,11])
    pixels[neutral] = neutral_ids[distances[:,:,neutral_ids].argmin(2)[neutral]] + 1
    pixels[rgba[:, :, 3] < 128] = 0
    output = Image.fromarray(pixels).convert('P')
    flat = [0, 0, 0] + [component for color in colors for component in color]
    output.putpalette(flat + [0] * (768 - len(flat)))
    output.info['transparency'] = 0
    return output


def colors_in(image):
    return sorted({pixel[:3] for pixel in image.convert('RGBA').getdata() if pixel[3]})


def write_pal(name, colors):
    colors = [(0, 0, 0)] + colors
    colors += [(0, 0, 0)] * (16 - len(colors))
    (DEST / (name + '.pal')).write_text('JASC-PAL\n0100\n16\n'
        + ''.join(f'{r} {g} {b}\n' for r, g, b in colors))


def main():
    atlas = Image.open(SOURCE / 'poses.png').convert('RGBA')
    assert atlas.width * 3 == atlas.height * 4, 'Atlas must retain its 4:3 layout'
    atlas = atlas.resize((384, 288), Image.Resampling.NEAREST)
    original = Image.open(SOURCE / 'overworld_down_16x32.png').convert('RGBA')
    colors = [(24,24,32),(48,48,48),(80,80,80),(248,192,144),(208,144,104),(136,88,64),(48,48,32),(80,80,48),(112,112,72),(240,240,232),(160,160,168),(72,72,80),(232,80,56)]
    # The shared activity palette also needs the existing bicycle's red trim.
    colors += [(208, 64, 64)]
    assert len(colors) <= 15

    def row(y, count, width):
        result = Image.new('RGBA', (count * width, 32))
        for frame in range(count):
            x = frame * 32 + (32 - width) // 2
            result.paste(atlas.crop((x, y, x + width, y + 32)), (frame * width, 0))
        return result

    sheets = {
        'normal': row(0, 9, 16),
        'bike': row(64, 9, 32),
        'item': row(128, 9, 16),
        'fish': row(160, 12, 32),
        'vs_seeker_bike': row(192, 6, 32),
    }
    # Preserve the front idle extracted from the supplied reference sheet.
    sheets['normal'].paste(original, (0, 0))
    surf_run = Image.new('RGBA', (224, 32))
    surf_run.paste(row(96, 3, 16), (0, 0))
    surf_run.paste(row(32, 11, 16), (48, 0))
    sheets['surf_run'] = surf_run
    # Protect the original vehicle geometry below the rider. The upper parts
    # contain the generated Brandon riding poses; Surf's mount remains an engine
    # field effect and is never copied into the rider sheet.
    for name, base in (('bike', 'red_bike'), ('vs_seeker_bike', 'red_vs_seeker_bike')):
        vehicle = Image.open(ROOT / f'graphics/object_events/pics/people/{base}.png').convert('RGBA')
        sheets[name].paste(vehicle.crop((0, 24, vehicle.width, 32)), (0, 24))
    for name, image in sheets.items():
        indexed(image, colors).save(DEST / (name + '.png'), bits=4)
    write_pal('overworld', colors)

    front = Image.open(SOURCE / 'battle_front_64x64.png').convert('RGBA')
    front_colors = colors
    assert len(front_colors) <= 15
    indexed(front, front_colors).save(DEST / 'front.png', bits=4)
    write_pal('trainer', front_colors)

    back = Image.new('RGBA', (64, 320))
    for frame in range(5):
        back.paste(atlas.crop((frame * 64, 224, (frame + 1) * 64, 288)), (0, frame * 64))
    indexed(back, front_colors).save(DEST / 'back.png', bits=4)
    write_pal('back', front_colors)

    # A head icon from the reference-derived overworld sprite, rather than another trainer.
    icon = original.crop((0, 7, 16, 23))
    indexed(icon, colors).save(DEST / 'map.png', bits=4)
    write_pal('map', colors)


if __name__ == '__main__':
    main()
