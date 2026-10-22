#!/usr/bin/env python3
"""Audit current Havora data and static foot routes; does not run the game.

Run from any directory. Emits JSON; nonzero exit on a technical invariant error.
The movement graph ignores NPC occupancy, scripts, doors' interior transitions,
and special movement. It is a conservative four-direction outdoor route check.
"""
import json
import struct
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def load(path):
    return json.loads((ROOT / path).read_text())

def words(path):
    b = (ROOT / path).read_bytes()
    assert len(b) % 2 == 0, path
    return list(struct.unpack('<' + 'H' * (len(b) // 2), b))

layouts = {l['id']: l for l in load('data/layouts/layouts.json')['layouts']}
maps = {}
for path in (ROOT / 'data/maps').glob('*/map.json'):
    m = json.loads(path.read_text())
    maps[m['id']] = m
selected = {k for k, m in maps.items()
            if layouts[m['layout']]['primary_tileset'] == 'gTileset_HavoraCityPrimary'}
assert len(selected) == 8
attrs = []
metas = []
for group in ('primary', 'secondary'):
    path = ROOT / f'data/tilesets/{group}/havora_city'
    raw = (path / 'metatile_attributes.bin').read_bytes()
    attrs += list(struct.unpack('<' + 'I' * (len(raw) // 4), raw))
    raw = words(path.relative_to(ROOT) / 'metatiles.bin')
    metas += [raw[i:i+8] for i in range(0, len(raw), 8)]
assert len(attrs) == len(metas) == 1024
D = {}
for k in sorted(selected):
    m = maps[k]
    l = layouts[m['layout']]
    assert l['secondary_tileset'] == 'gTileset_HavoraCity'
    assert m['map_type'] == 'MAP_TYPE_CITY'
    assert (l['width'] + 15) * (l['height'] + 14) <= 0x2800
    w = words(l['blockdata_filepath'])
    border = words(l['border_filepath'])
    assert len(w) == l['width'] * l['height'], m['name']
    assert len(border) == l['border_width'] * l['border_height'], m['name']
    for value in w + border:
        mid = value & 1023
        assert any(metas[mid]) or attrs[mid], (m['name'], 'undefined metatile', mid)
    D[k] = (l, w)
    for kind in ('object_events', 'warp_events', 'coord_events', 'bg_events'):
        for i, e in enumerate(m[kind]):
            assert 0 <= e['x'] < l['width'] and 0 <= e['y'] < l['height'], (m['name'], kind, i)
    for e in m['warp_events']:
        assert e['dest_map'] in maps
        assert 0 <= int(e['dest_warp_id']) < len(maps[e['dest_map']]['warp_events'])
# Incoming return-warp indices must remain valid too.
for m in maps.values():
    for e in m['warp_events']:
        if e['dest_map'] in selected:
            assert 0 <= int(e['dest_warp_id']) < len(maps[e['dest_map']]['warp_events']), m['name']
opposite = {'left': 'right', 'right': 'left', 'up': 'down', 'down': 'up'}
pos = {'MAP_HAVORA_MARKET': (0, 0)}
q = deque(pos)
connection_count = 0
while q:
    k = q.popleft()
    m = maps[k]
    l, _ = D[k]
    x, y = pos[k]
    for c in m['connections'] or []:
        target, off, dr = c['map'], int(c['offset']), c['direction']
        if target not in selected:
            continue
        connection_count += 1
        reverse = [r for r in maps[target]['connections'] or []
                   if r['map'] == k and r['direction'] == opposite[dr]]
        assert len(reverse) == 1 and int(reverse[0]['offset']) == -off, (k, target)
        ll, _ = D[target]
        assert max(0, off) < min(l['width'] if dr in ('up', 'down') else l['height'],
                                off + (ll['width'] if dr in ('up', 'down') else ll['height']))
        p = {'left': (x-ll['width'], y+off), 'right': (x+l['width'], y+off),
             'up': (x+off, y-ll['height']), 'down': (x+off, y+l['height'])}[dr]
        if target in pos:
            assert pos[target] == p, ('inconsistent map loop', k, target, pos[target], p)
        else:
            pos[target] = p
            q.append(target)
assert len(pos) == len(selected)

def cell(k, x, y):
    l, w = D[k]
    if 0 <= x < l['width'] and 0 <= y < l['height']:
        return w[y*l['width']+x]
    return None

def foot(value):
    return value is not None and (value >> 10) & 3 == 0 and (attrs[value & 1023] & 511) not in range(0x10, 0x20)

start = ('MAP_HAVORA_HARBOR', 21, 18)
assert foot(cell(*start))
q = deque([start])
seen = {start}
while q:
    k, x, y = q.popleft()
    l, _ = D[k]
    u = cell(k, x, y)
    for dx, dy, dr in ((1, 0, 'right'), (-1, 0, 'left'), (0, 1, 'down'), (0, -1, 'up')):
        target, xx, yy = k, x+dx, y+dy
        if not (0 <= xx < l['width'] and 0 <= yy < l['height']):
            found = False
            for c in maps[k]['connections'] or []:
                if c['direction'] != dr or c['map'] not in D:
                    continue
                ll, _ = D[c['map']]
                tx, ty = xx, yy
                if dr in ('left', 'right'):
                    ty -= int(c['offset'])
                    tx = ll['width']-1 if dr == 'left' else 0
                else:
                    tx -= int(c['offset'])
                    ty = ll['height']-1 if dr == 'up' else 0
                if cell(c['map'], tx, ty) is not None:
                    target, xx, yy = c['map'], tx, ty
                    found = True
                    break
            if not found:
                continue
        v = cell(target, xx, yy)
        if not foot(v) or not (u >> 12 == v >> 12 or u >> 12 in (0, 15) or v >> 12 in (0, 15)):
            continue
        point = target, xx, yy
        if point not in seen:
            seen.add(point)
            q.append(point)
visible_doors = []
inactive = []
for k in sorted(selected):
    for i, e in enumerate(maps[k]['warp_events']):
        point = k, e['x'], e['y']
        assert point in seen, ('unreachable entrance/return landing', k, i)
        behavior = attrs[cell(*point) & 1023] & 511
        if behavior in (0x60, 0x69):
            visible_doors.append({'map': maps[k]['name'], 'warp_index': i, 'interior': e['dest_map']})
        else:
            inactive.append({'map': maps[k]['name'], 'warp_index': i, 'interior': e['dest_map'],
                             'reason': 'No door graphic/behavior; retained safe return landing only'})
assert len(inactive) == 3, inactive
print(json.dumps({'outdoor_maps': len(selected), 'reciprocal_connections': connection_count//2,
                  'origins': {maps[k]['name']: p for k, p in pos.items()},
                  'reachable_foot_cells': len(seen), 'reachable_visible_doors': len(visible_doors),
                  'inactive_interiors': inactive,
                  'scenic_maps_without_foot_routes': [maps[k]['name'] for k in sorted(selected) if not any(p[0] == k for p in seen)],
                  'checks': ['map and border lengths', 'map-buffer capacity', 'shared tileset compatibility',
                             'event bounds', 'outgoing and incoming warp indices',
                             'reciprocal offsets and consistent placement loops',
                             'static land routes from ferry sailor to all entrance/return locations']}, indent=2))
