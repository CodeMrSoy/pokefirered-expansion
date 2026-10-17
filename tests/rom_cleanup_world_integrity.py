#!/usr/bin/env python3
"""Audit every retained map's static exits against the actual map/layout data."""
import json
from pathlib import Path
root = Path(__file__).resolve().parents[1]
retired = set(json.loads((root/'data/quantum/retired_content.json').read_text())['retired_maps'])
maps = {p.parent.name: json.loads(p.read_text()) for p in (root/'data/maps').glob('*/map.json')}
by_id = {v['id']: k for k,v in maps.items()}
layouts = {v['id']: v for v in json.loads((root/'data/layouts/layouts.json').read_text())['layouts']}
warps = connections = 0
for name, data in maps.items():
    if name in retired:
        continue
    layout = layouts[data['layout']]
    assert len((root/layout['blockdata_filepath']).read_bytes()) == layout['width'] * layout['height'] * 2, name
    for warp in data.get('warp_events', []):
        warps += 1
        if warp['x'] == 32760:  # Deliberately disabled former stairs keep their stable warp index.
            assert warp['dest_map'] == 'MAP_PALLET_TOWN' and int(warp['dest_warp_id']) == 255, (name, warp)
            continue
        assert 0 <= warp['x'] < layout['width'] and 0 <= warp['y'] < layout['height'], (name, warp)
        if warp['dest_map'] == 'MAP_DYNAMIC':
            continue
        dest = by_id[warp['dest_map']]
        assert dest not in retired, (name, 'exit into retired map', dest)
        index = int(warp['dest_warp_id'])
        if index != 255:  # WARP_ID_NONE: the destination is supplied dynamically.
            assert 0 <= index < len(maps[dest].get('warp_events', [])), (name, dest, index)
    for connection in data.get('connections') or []:
        connections += 1
        dest = by_id[connection['map']]
        assert dest not in retired, (name, 'connection into retired map', dest)
print(f'{len(maps)-len(retired)} retained maps: layout sizes, {warps} warps, {connections} connections valid')
