"""Opt-in stall placement on the November Havora map; never run by ROM builds.

Uses the complete Slateport narrow kit already packed in the shared tileset.
The baseline guard prevents this migration from overwriting later Porymap work.
"""
from pathlib import Path
import argparse, hashlib, json, struct

R = Path(__file__).resolve().parents[2]
BASE = '2cc484e7bb2fa00be853fc7d83c865407782cca4e5919512de9d54accafe37da'
PLACEMENTS = [
    ('HealingBerries', 0, 40), ('Medicine', 5, 40),
    ('Meteorite', 0, 44), ('SoldOut', 0, 50),
    ('Refreshments', 0, 54), ('FriendshipBerries', 34, 42),
    ('ResistanceBerries', 34, 47), ('BattleBerries', 34, 52),
]

def load(path): return json.loads((R / path).read_text())

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    layout = next(l for l in load('data/layouts/layouts.json')['layouts']
                  if l['id'] == 'LAYOUT_HAVORA_MARKET')
    assert (layout['width'], layout['height']) == (41, 62)
    path = R / layout['blockdata_filepath']
    original = path.read_bytes()
    blocks = list(struct.unpack('<2542H', original))
    kit = load('tools/havora/editor-kits.json')['stalls']['narrow']
    market = load('data/maps/Havora_Market/map.json')
    def put(x, y, mid, solid=False):
        blocks[y * 41 + x] = 0x4000 | (0x400 if solid else 0) | mid
    if args.apply:
        assert hashlib.sha256(original).hexdigest() == BASE, 'Not the authored baseline; refusing to overwrite newer map edits'
        # Replace the small old blue kiosk with the matching Slateport row.
        for y in range(53, 56):
            for x in range(1, 5): put(x, y, 0)
        for name, x, y in PLACEMENTS:
            for dy, row in enumerate(kit):
                for dx, mid in enumerate(row):
                    put(x + dx, y + dy, mid, not (dy in (1, 2) and dx in (1, 2)))
            # A paved standing tile in front of each stall, connected to
            # the existing side streets rather than a new paved rectangle.
            put(x + 1, y + 3, 0x1C1)
            obj = next(o for o in market['object_events']
                       if o['script'] == 'Havora_Market_' + name)
            obj.update(x=x + 1, y=y + 2, elevation=4,
                       movement_type='MOVEMENT_TYPE_FACE_DOWN',
                       movement_range_x=0, movement_range_y=0)
        path.write_bytes(struct.pack('<2542H', *blocks))
        (R / 'data/maps/Havora_Market/map.json').write_text(json.dumps(market, indent=2) + '\n')
    for name, x, y in PLACEMENTS:
        for dy, row in enumerate(kit):
            for dx, mid in enumerate(row):
                value = blocks[(y + dy) * 41 + x + dx]
                assert value & 1023 == mid, (name, dx, dy)
                assert value >> 12 == 4
                assert bool(value & 0xC00) == (not (dy in (1, 2) and dx in (1, 2)))
        obj = next(o for o in market['object_events'] if o['script'] == 'Havora_Market_' + name)
        assert (obj['x'], obj['y'], obj['elevation']) == (x + 1, y + 2, 4)
        assert obj['movement_type'] == 'MOVEMENT_TYPE_FACE_DOWN'
        assert blocks[(y + 3) * 41 + x + 1] & 0xFC00 == 0x4000
    print('PASS: eight complete Slateport stalls and visible, approachable vendors')

if __name__ == '__main__': main()
