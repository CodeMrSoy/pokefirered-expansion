#!/usr/bin/env python3
"""Install grass-backed FireRed puzzle authoring tiles without painting maps.

One-time migration. Reuses native sprites/cave props and the existing palettes.
All placed art, complete kits and animation graphics are protected. Losslessly
aliases hidden lower-layer pixels before reclaiming unused catalog fragments.
"""
import hashlib
import json
import struct
import subprocess
from collections import defaultdict
from pathlib import Path

import numpy as np
from PIL import Image

R = Path(__file__).resolve().parents[2]
MANIFEST = R / 'tools/havora/puzzle-tiles.json'


def js(name):
    return json.loads((R / f'tools/havora/{name}.json').read_text())


def words(path):
    raw = path.read_bytes()
    return list(struct.unpack('<' + 'H' * (len(raw) // 2), raw))


def graphics(path):
    im = Image.open(path)
    return [im.crop((x, y, x + 8, y + 8)).tobytes()
            for y in range(0, im.height, 8) for x in range(0, 128, 8)]


def flip(raw, flags):
    im = Image.frombytes('P', (8, 8), raw)
    if flags & 1024:
        im = im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    if flags & 2048:
        im = im.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
    return im.tobytes()


def canon(raw):
    return min((flip(raw, f), f) for f in (0, 1024, 2048, 3072))


def main():
    if MANIFEST.exists():
        print('Puzzle kit already installed; edit it in Porymap.')
        return
    base = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=R).decode().strip()
    T, M, A, P = [], [], [], []
    for group in ('primary', 'secondary'):
        p = R / f'data/tilesets/{group}/havora_city'
        T.extend(graphics(p / 'tiles.png'))
        v = words(p / 'metatiles.bin')
        M.extend(tuple(v[i:i + 8]) for i in range(0, len(v), 8))
        raw = (p / 'metatile_attributes.bin').read_bytes()
        A.extend(struct.unpack('<' + 'I' * (len(raw) // 4), raw))
    for i in range(13):
        group = 'primary' if i < 7 else 'secondary'
        lines = (R / f'data/tilesets/{group}/havora_city/palettes/{i:02}.pal').read_text().splitlines()
        P.append([tuple(map(int, line.split())) for line in lines[3:19]])
    oldT, oldM, oldA = T[:], M[:], A[:]
    layouts = json.loads((R / 'data/layouts/layouts.json').read_text())['layouts']
    placed = set()
    for layout in layouts:
        if layout['primary_tileset'] == 'gTileset_HavoraCityPrimary':
            for key in ('blockdata_filepath', 'border_filepath'):
                placed.update(w & 1023 for w in words(R / layout[key]))
    city = js('city-tileset')
    protected = placed | set(city['native_general_ids'].values()) | set(city['compatible_metatiles']) | set(range(168, 172))
    for file, key in [('civic-tiles', 'assets'), ('civic-repair', 'assets'),
                      ('green-houses', 'kits'), ('native-houses', 'kits'), ('fountain', 'kits')]:
        for grid in js(file)[key].values():
            for row in grid:
                protected.update(row)
    protected.update(js('editor-kits')['new_metatiles'])
    for value in js('gym-garden')['added_metatiles'].values():
        protected.update(value if isinstance(value, list) else [value])
    authoring = js('authoring-assets')
    for value in authoring['statue_metatiles'].values():
        protected.update(value)
    shared = js('shared-tileset')
    harbor_map = {int(k): v for k, v in shared['metatile_mapping']['harbor'].items()}
    harbor = js('assets')
    for asset in harbor['assets'].values():
        for row in asset['metatiles']:
            protected.update(harbor_map[i] for i in row if i in harbor_map)
    for entry in harbor['catalog']:
        if entry['town'] == 'pacifidlog' or entry['town'] == 'slateport' and entry['source_id'] < 0x260:
            if entry['havora_id'] in harbor_map:
                protected.add(harbor_map[entry['havora_id']])
    fixed = set(range(416, 482)) | set(range(508, 512)) | set(range(896, 1024)) | {0, 20}
    fixed.update(js('fountain')['animation_graphic_ids'])

    # A lower tile may alias another graphic when every visible pixel matches.
    # Keep every top-layer descriptor and all animated descriptors untouched.
    arr = np.array([list(raw) for raw in T], dtype=np.uint8).reshape(1024, 8, 8)
    variants = np.concatenate([arr, arr[:, :, ::-1], arr[:, ::-1, :], arr[:, ::-1, ::-1]]).reshape(-1, 64)
    ids = np.tile(np.arange(1024), 4)
    flags = np.repeat([0, 1024, 2048, 3072], 1024)

    def pixels(w):
        return variants[(w & 1023) + ((w & 3072) // 1024) * 1024]

    essential = fixed.copy()
    for m in M:
        for k, w in enumerate(m):
            if k >= 4 or m[k + 4] & 1023 in fixed or np.all(pixels(m[k + 4]) == 0):
                essential.add(w & 1023)
    candidates = np.array([i for i, tid in enumerate(ids) if tid in essential and tid not in fixed or tid == 0])
    proposed = [list(m) for m in M]
    for mid, m in enumerate(M):
        for k in range(4):
            w, top = m[k], m[k + 4]
            if top & 1023 in fixed:
                continue
            visible = pixels(top) == 0
            if visible.all():
                continue
            if not visible.any():
                replacement = 0
            else:
                pal = np.array(P[w >> 12])
                target = pal[pixels(w)[visible]]
                possible = pal[variants[candidates][:, visible]]
                match = np.flatnonzero(np.all(possible == target, axis=(1, 2)))
                if not len(match):
                    continue
                v = candidates[match[0]]
                replacement = int(ids[v]) | int(flags[v]) | (w & 0xf000)
            proposed[mid][k] = replacement
    freed = {w & 1023 for m in M for w in m} - {w & 1023 for m in proposed for w in m}
    aliases = []
    for mid, m in enumerate(M):
        new = list(m)
        for k in range(4):
            if m[k] & 1023 in freed and proposed[mid][k] != m[k]:
                new[k] = proposed[mid][k]
                aliases.append({'metatile': mid, 'quadrant': k, 'before': m[k], 'after': new[k]})
        M[mid] = tuple(new)

    refs = defaultdict(set)
    for mid, m in enumerate(M):
        if any(m) or A[mid]:
            for w in m:
                refs[w & 1023].add(mid)
    pinned = fixed | {w & 1023 for mid in protected for w in M[mid]}
    cache = {}
    for i, raw in enumerate(T):
        if i not in fixed or i in (0, 20):
            key, f = canon(raw)
            cache.setdefault(key, (i, f))
    archive = {'metatiles': {}, 'graphics': {}}
    retired, added = set(), []

    def allocate(raw):
        key, f = canon(raw)
        if key in cache:
            i, cf = cache[key]
            pinned.add(i)
            return i | (f ^ cf)
        free = [i for i in range(1024) if i not in pinned and not (refs[i] & protected)]
        assert free, 'No safe static graphic slot; nothing written.'
        i = min(free, key=lambda j: (len(refs[j]), j))
        for mid in list(refs[i]):
            assert mid not in protected
            archive['metatiles'][str(mid)] = {'words': oldM[mid], 'attribute': oldA[mid]}
            retired.add(mid)
            for w in M[mid]:
                refs[w & 1023].discard(mid)
            M[mid], A[mid] = (0,) * 8, 0
        archive['graphics'][str(i)] = list(T[i])
        oldkey, _ = canon(T[i])
        if cache.get(oldkey, (None, None))[0] == i:
            del cache[oldkey]
        T[i] = key
        cache[key] = (i, 0)
        pinned.add(i)
        return i | f

    palette = np.array(P, dtype=np.int32)

    def descriptors(im):
        rgba = np.array(im.convert('RGBA'))
        result = []
        for y, x in ((0, 0), (0, 8), (8, 0), (8, 8)):
            rgb = rgba[y:y + 8, x:x + 8, :3].astype('int32')
            mask = rgba[y:y + 8, x:x + 8, 3] > 0
            dist = ((rgb[:, :, None, None, :] - palette[None, None, :, 1:, :]) ** 2).sum(4)
            bank = int(dist.min(3)[mask].sum(0).argmin())
            indices = (dist[:, :, bank].argmin(2) + 1).astype('uint8')
            indices[~mask] = 0
            result.append((indices.tobytes(), bank))
        return result

    def object_art(name, pal):
        im = Image.open(R / f'graphics/object_events/pics/misc/{name}.png').crop((0, 0, 16, 16))
        lines = (R / f'graphics/object_events/palettes/{pal}.pal').read_text().splitlines()[3:19]
        colors = [tuple(map(int, line.split())) for line in lines]
        im.putpalette(sum(map(list, colors), []) + [0] * 720)
        im.info['transparency'] = 0
        return im.convert('RGBA')

    def cave_overlay(mid):
        paths = [R / 'data/tilesets/primary/general', R / 'data/tilesets/secondary/digletts_cave']
        tiles = graphics(paths[0] / 'tiles.png') + graphics(paths[1] / 'tiles.png')
        m = words(paths[1] / 'metatiles.bin')[(mid - 640) * 8:(mid - 640 + 1) * 8]
        out = Image.new('RGBA', (16, 16))
        for k, w in enumerate(m[4:]):
            lines = (paths[0 if w >> 12 < 7 else 1] / 'palettes' / f'{w >> 12:02}.pal').read_text().splitlines()[3:19]
            colors = [tuple(map(int, line.split())) for line in lines]
            im = Image.frombytes('P', (8, 8), flip(tiles[w & 1023], w & 3072))
            im.putpalette(sum(map(list, colors), []) + [0] * 720)
            im.info['transparency'] = 0
            out.paste(im.convert('RGBA'), (k % 2 * 8, k // 2 * 8))
        return out

    switch = cave_overlay(0x2c0)
    # The pressed disk uses the same native circular shape, lowered one pixel
    # and shaded with existing shared material colors; no palette is changed.
    pressed = Image.new('RGBA', (16, 16))
    dim = np.array(switch)
    dim[:, :, :3] = (dim[:, :, :3].astype('uint16') * 3 // 4).astype('uint8')
    pressed.paste(Image.fromarray(dim).crop((0, 0, 16, 15)), (0, 1))
    specs = {
        'boulder_grass': (object_art('strength_boulder', 'npc_white'), 0),
        'cut_tree_grass': (object_art('cut_tree', 'npc_green'), 0),
        'hole_open_grass': (cave_overlay(0x31c), 0),
        'switch_released_grass': (switch, 0x20),
        'switch_pressed_grass': (pressed, 0x20),
    }
    first = next(start for start in range(1024 - len(specs) + 1)
                 if all(not any(M[i]) and not A[i] and i not in protected
                        for i in range(start, start + len(specs))))
    asset_slots = list(range(first, first + len(specs)))
    protected.update(asset_slots)
    source = {name: descriptors(im) for name, (im, _) in specs.items()}
    # Pin every existing source match before making any allocation.
    for ds in source.values():
        for raw, _ in ds:
            key, _ = canon(raw)
            if key in cache:
                pinned.add(cache[key][0])
    assets = {}
    for (name, ds), mid in zip(source.items(), asset_slots):
        overlay = tuple(allocate(raw) | (bank << 12) for raw, bank in ds)
        M[mid] = tuple(oldM[0][:4]) + overlay
        A[mid] = specs[name][1]
        assets[name] = mid
        protected.add(mid)
        added.append(mid)
        for w in M[mid]:
            refs[w & 1023].add(mid)

    def render(tiles, m):
        out = np.zeros((16, 16, 3), dtype=np.uint8)
        for k, w in enumerate(m):
            indices = np.array(list(flip(tiles[w & 1023], w & 3072))).reshape(8, 8)
            colors = np.array(P[w >> 12], dtype=np.uint8)[indices]
            target = out[(k % 4 // 2) * 8:(k % 4 // 2 + 1) * 8, (k % 2) * 8:(k % 2 + 1) * 8]
            target[indices != 0 if k >= 4 else np.ones((8, 8), dtype=bool)] = colors[indices != 0 if k >= 4 else np.ones((8, 8), dtype=bool)]
        return out.tobytes()

    assert not placed & retired
    for mid in range(1024):
        if mid not in retired and mid not in added:
            assert A[mid] == oldA[mid]
            assert render(T, M[mid]) == render(oldT, oldM[mid]), ('Changed old art', mid)
    assert all(T[i] == oldT[i] for i in fixed)
    assert len(T) == len(M) == len(A) == 1024
    assert all(w >> 12 < 13 for m in M for w in m)
    # No edits are written until allocation and full retained-art checks pass.
    for group, offset, count in [('primary', 0, 640), ('secondary', 640, 384)]:
        p = R / f'data/tilesets/{group}/havora_city'
        im = Image.new('P', (128, count // 16 * 8))
        im.putpalette(Image.open(p / 'tiles.png').getpalette())
        for i, raw in enumerate(T[offset:offset + count]):
            im.paste(Image.frombytes('P', (8, 8), raw), (i % 16 * 8, i // 16 * 8))
        im.save(p / 'tiles.png')
        (p / 'metatiles.bin').write_bytes(struct.pack('<' + 'H' * (count * 8), *[w for m in M[offset:offset + count] for w in m]))
        (p / 'metatile_attributes.bin').write_bytes(struct.pack('<' + 'I' * count, *A[offset:offset + count]))
    for kind, mapping in shared['metatile_mapping'].items():
        shared['metatile_mapping'][kind] = {k: v for k, v in mapping.items() if v not in retired}
    (R / 'tools/havora/shared-tileset.json').write_text(json.dumps(shared, indent=2) + '\n')
    authoring['building_tiles'] = [e for e in authoring['building_tiles'] if e['metatile'] not in retired]
    authoring['puzzle_tiles'] = assets
    (R / 'tools/havora/authoring-assets.json').write_text(json.dumps(authoring, indent=2) + '\n')
    report = {
        'base_commit': base, 'assets': assets, 'grass_metatile': 0,
        'cleared_or_filled_ground': 0, 'background': 'Existing Havora grass metatile 0x000, unchanged',
        'lossless_lower_aliases': aliases, 'graphics_freed_by_aliasing': sorted(freed),
        'new_graphics': len(archive['graphics']), 'retired_unplaced': sorted(retired),
        'placed_metatiles_preserved': len(placed), 'animation_graphic_ids_preserved': sorted(fixed),
        'archive': archive,
        'sources': {'boulder': 'FireRed StrengthBoulder first frame / npc_white',
                    'cut_tree': 'FireRed CutTree first frame / npc_green',
                    'hole': 'FireRed Digletts Cave 0x31C overlay',
                    'switch': 'FireRed Digletts Cave 0x2C0 overlay / native Strength button'},
        'behavior': {'boulder_grass': 'MB_NORMAL: visual authoring tile only',
                     'cut_tree_grass': 'MB_NORMAL: visual authoring tile only',
                     'hole_open_grass': 'MB_NORMAL: no automatic fall warp',
                     'switch_released_grass': 'MB_STRENGTH_BUTTON: requires a coordinate-event script',
                     'switch_pressed_grass': 'MB_STRENGTH_BUTTON: requires a coordinate-event script'},
        'note': 'No maps, borders, events, warps, palettes or animations changed. For working boulders and Cut trees, use object events on plain grass, not static tiles. Shaft filling and reversible switches require puzzle scripts.'
    }
    MANIFEST.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: report[k] for k in ('assets', 'new_graphics', 'retired_unplaced', 'placed_metatiles_preserved')}))


if __name__ == '__main__':
    main()
