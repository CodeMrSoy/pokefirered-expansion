#!/usr/bin/env python3
"""Verify the one-time puzzle-kit migration against its recorded source commit."""
import io
import json
import sys
import struct
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image

R = Path(__file__).resolve().parents[2]
kit = json.loads((R / 'tools/havora/puzzle-tiles.json').read_text())
base = kit['base_commit']


def prior(path):
    return subprocess.check_output(['git', 'show', base + ':' + path], cwd=R)


def split(raw, fmt):
    return list(struct.unpack('<' + fmt * (len(raw) // struct.calcsize(fmt)), raw))


old_tiles, new_tiles, old_meta, new_meta, old_attrs, new_attrs, palettes = [], [], [], [], [], [], []
for group, count in [('primary', 640), ('secondary', 384)]:
    root = f'data/tilesets/{group}/havora_city/'
    for data, target in [(prior(root + 'tiles.png'), old_tiles), ((R / root / 'tiles.png').read_bytes(), new_tiles)]:
        im = Image.open(io.BytesIO(data))
        assert im.mode == 'P' and im.size == (128, count // 16 * 8)
        assert int(np.max(np.array(im))) <= 15
        target.extend(np.array(im.crop((x, y, x + 8, y + 8))) for y in range(0, im.height, 8) for x in range(0, 128, 8))
    for data, target in [(prior(root + 'metatiles.bin'), old_meta), ((R / root / 'metatiles.bin').read_bytes(), new_meta)]:
        assert len(data) == count * 16
        words = split(data, 'H')
        target.extend(words[i:i + 8] for i in range(0, len(words), 8))
    old_attrs.extend(split(prior(root + 'metatile_attributes.bin'), 'I'))
    raw = (R / root / 'metatile_attributes.bin').read_bytes()
    assert len(raw) == count * 4
    new_attrs.extend(split(raw, 'I'))
    for p in (R / root / 'palettes').glob('*.pal'):
        assert p.read_text().splitlines() == prior(str(p.relative_to(R))).decode().splitlines(), p
for bank in range(13):
    group = 'primary' if bank < 7 else 'secondary'
    lines = (R / f'data/tilesets/{group}/havora_city/palettes/{bank:02}.pal').read_text().splitlines()[3:19]
    palettes.append(np.array([tuple(map(int, line.split())) for line in lines], dtype=np.uint8))


def render(m, graphics):
    out = np.zeros((16, 16, 3), dtype=np.uint8)
    for k, w in enumerate(m):
        a = graphics[w & 1023]
        if w & 1024:
            a = a[:, ::-1]
        if w & 2048:
            a = a[::-1, :]
        mask = a != 0 if k >= 4 else np.ones((8, 8), dtype=bool)
        x, y = k % 2 * 8, k % 4 // 2 * 8
        out[y:y + 8, x:x + 8][mask] = palettes[w >> 12][a][mask]
    return out


new_ids = set(kit['assets'].values())
retired = set(kit['retired_unplaced'])
assert sorted(new_ids) == list(range(0x22c, 0x231))
for mid in range(1024):
    assert all(w & 1023 < 1024 and w >> 12 < 13 for w in new_meta[mid])
    if mid not in new_ids | retired:
        assert new_attrs[mid] == old_attrs[mid], ('changed old behavior', mid)
        assert np.array_equal(render(old_meta[mid], old_tiles), render(new_meta[mid], new_tiles)), ('changed retained pixels', mid)
fixed = set(kit['animation_graphic_ids_preserved'])
for i in fixed:
    assert np.array_equal(old_tiles[i], new_tiles[i]), ('changed animation graphic', i)
# Aliases are strictly hidden lower-layer changes under a static overlay, so
# their pixel equality also holds while water, flowers and fountains animate.
for alias in kit['lossless_lower_aliases']:
    mid, q = alias['metatile'], alias['quadrant']
    assert q < 4 and alias['before'] & 1023 not in fixed
    assert old_meta[mid][q + 4] & 1023 not in fixed
for key, mid in kit['assets'].items():
    assert new_meta[mid][:4] == old_meta[0][:4], (key, 'wrong grass')
    assert new_attrs[mid] & 511 == (0x20 if key.startswith('switch_') else 0)
assert not np.array_equal(render(new_meta[kit['assets']['switch_released_grass']], new_tiles), render(new_meta[kit['assets']['switch_pressed_grass']], new_tiles))
for key, archived in kit['archive']['metatiles'].items():
    assert archived['words'] == old_meta[int(key)]
    assert archived['attribute'] == old_attrs[int(key)]
changed = subprocess.check_output(['git', 'diff', '--name-only', base, '--', 'data/maps', 'data/layouts', 'src', 'include'], cwd=R).decode().strip()
assert not changed, ('Migration must not paint maps or change events/engine', changed)
assert not subprocess.check_output(['git', 'diff', '--name-only', base, '--', '**/anim/**', '**/palettes/**'], cwd=R).decode().strip()
print('PASS: five contiguous grass-backed entries, 4-bit graphics, palette/animation budgets, retained-metatile pixels, archived fragments, and unchanged maps/events/engine.')

if '--rom' in sys.argv:
    # Check the linked ROM, not just the converter's intermediate files.
    symbols = {}
    for line in subprocess.check_output(['arm-none-eabi-nm', str(R / 'pokefirered.elf')], text=True).splitlines():
        fields = line.split()
        if len(fields) == 3:
            symbols[fields[2]] = int(fields[0], 16)
    rom = (R / 'pokefirered.gba').read_bytes()

    def embedded(symbol, path):
        data = (R / path).read_bytes()
        offset = symbols[symbol] - 0x08000000
        assert 0 <= offset <= len(rom) - len(data)
        assert rom[offset:offset + len(data)] == data, ('stale linked asset', symbol)
        return offset

    def decompress(offset):
        assert rom[offset] == 0x10, 'Expected GBA LZ77 graphics'
        size = int.from_bytes(rom[offset + 1:offset + 4], 'little')
        pos, output = offset + 4, bytearray()
        while len(output) < size:
            flags = rom[pos]
            pos += 1
            for bit in range(7, -1, -1):
                if len(output) >= size:
                    break
                if flags & (1 << bit):
                    a, b = rom[pos:pos + 2]
                    pos += 2
                    distance, length = ((a & 15) << 8 | b) + 1, (a >> 4) + 3
                    assert distance <= len(output)
                    for _ in range(length):
                        output.append(output[-distance])
                else:
                    output.append(rom[pos])
                    pos += 1
        assert len(output) == size
        return output

    for group, suffix in [('primary', 'HavoraCityPrimary'), ('secondary', 'HavoraCity')]:
        root = f'data/tilesets/{group}/havora_city/'
        embedded('gMetatiles_' + suffix, root + 'metatiles.bin')
        embedded('gMetatileAttributes_' + suffix, root + 'metatile_attributes.bin')
        offset = embedded('gTilesetTiles_' + suffix, root + 'tiles.4bpp.lz')
        im = Image.open(R / root / 'tiles.png')
        expected = bytearray()
        for y in range(0, im.height, 8):
            for x in range(0, im.width, 8):
                for yy in range(8):
                    for xx in range(0, 8, 2):
                        expected.append(im.getpixel((x + xx, y + yy)) | im.getpixel((x + xx + 1, y + yy)) << 4)
        assert decompress(offset) == expected, ('linked PNG pixels differ', suffix)
        for bank in (range(7) if group == 'primary' else range(7, 13)):
            start = symbols['gTilesetPalettes_' + suffix] - 0x08000000 + bank * 32
            colors = palettes[bank].astype('uint16')
            expected_pal = ((colors[:, 0] >> 3) | ((colors[:, 1] >> 3) << 5) | ((colors[:, 2] >> 3) << 10))
            assert rom[start:start + 32] == struct.pack('<16H', *expected_pal), ('linked palette differs', suffix, bank)
    print('PASS: linked ROM contains the current Havora metatiles, behaviors, all 1,024 graphics, and all 13 active background palette banks.')
