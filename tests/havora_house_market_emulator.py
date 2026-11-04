"""Real Havora house round trips and interaction with every market vendor."""
import collections, json, pathlib, struct
source = pathlib.Path(__file__).with_name('eirik_surf_progression_emulator.py')
exec(compile(source.read_text().split('wailer=constant')[0], str(source), 'exec'))
m.d = m.root / 'build/havora-house-market-tests'
m.d.mkdir(parents=True, exist_ok=True)
layouts = {l['id']:l for l in json.loads((m.root/'data/layouts/layouts.json').read_text())['layouts']}
retired = json.loads((m.root/'data/quantum/retired_content.json').read_text())['retired_layouts']
maps = {json.loads(p.read_text())['id']:json.loads(p.read_text()) for p in (m.root/'data/maps').glob('Havora*/map.json')}

def current(): return tuple(m.read(ptr('gSaveBlock1Ptr')+4, 2))

def cross(key, target):
    before = current()
    m.keys.add(key)
    try: until(lambda:current()!=before, 600)
    finally:m.keys.clear()
    m.run(180)
    assert current() == ids[target] and field(), (target, current(), pos())

repaired = ('Havora_WeaverHouse', 'Havora_FisherHouse', 'Havora_CliffHouse_3')
# Check every currently connected house. Unconnected legacy templates are not
# made reachable by this regression or this map fix.
houses = {e['dest_map'] for outside in maps.values()
          if outside['map_type'] != 'MAP_TYPE_INDOOR'
          for e in outside['warp_events'] if e['dest_map'] in maps
          and any(s in maps[e['dest_map']]['name'] for s in ('House', 'Inn', 'Lodge'))}
for mid in sorted(houses):
    inside = maps[mid]
    name = inside['name']
    assert layouts[inside['layout']]['name'] not in retired
    back = inside['warp_events'][0]
    outside = maps[back['dest_map']]
    door = outside['warp_events'][int(back['dest_warp_id'])]
    assert door['dest_map'] == inside['id']
    # Repeat actual entrance/exit, rather than injecting the return warp.
    visits = 2 if name in repaired else 1
    for visit in range(visits):
        warp(outside['name'], door['x'], door['y']+1)
        cross(4, name)
        assert pos() == (back['x'], back['y']), (name, pos())
        assert native('MapGridGetMetatileBehaviorAt', back['x']+7,back['y']+7) == 0x65
        m.snap(name+'-inside')
        cross(5, outside['name'])
        assert pos() == (door['x'],door['y']+1), (name, pos())
        m.snap(name+'-returned')
    print('PASS actual house round trips:', name, visits, flush=True)

market = maps['MAP_HAVORA_MARKET']
layout = layouts[market['layout']]
words = struct.unpack('<2542H', (m.root/layout['blockdata_filepath']).read_bytes())
vendors = ['HealingBerries','Medicine','Meteorite','SoldOut','Refreshments',
           'FriendshipBerries','ResistanceBerries','BattleBerries']
occupied = {(o['x'],o['y']) for o in market['object_events']}
# Check every customer tile has a land route from the established harbor stairs.
start=(11,61);seen={start};queue=collections.deque([start])
while queue:
    x,y=queue.popleft()
    for p in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)):
        xx,yy=p
        if not(0<=xx<41 and 0<=yy<62) or p in seen or p in occupied:continue
        old=words[y*41+x]; value=words[yy*41+xx]
        if value & 0xC00 or (old>>12 and value>>12 and old>>12!=value>>12):continue
        seen.add(p);queue.append(p)
for name in vendors:
    obj=next(o for o in market['object_events'] if o['script']=='Havora_Market_'+name)
    x,y=obj['x'],obj['y']
    assert (x,y+1) in seen, ('Stall disconnected',name)
    warp('Havora_Market', x,y+1)
    m.press(4,12); m.press(8,90)
    assert not field(), ('Stall interaction failed',name)
    m.snap('stall-'+name)
    # The six normal shops proceed into the real buy/sell/cancel menu.
    if name not in ('Meteorite','SoldOut'):
        for _ in range(12):
            if task('Task_ShopMenu'):break
            m.press(8,30)
        assert task('Task_ShopMenu'), ('Shop menu did not open',name)
        m.snap('shop-'+name)
    # Cancel the shop, purchase prompt or dialogue without altering inventory.
    for _ in range(50):
        m.press(0,30)
        if field():break
    assert field(), ('Could not close vendor',name)
    print('PASS accessible stall and actual interaction:',name,flush=True)
# Koga retains all four original approach tiles during the story visit.
assert all(p in seen for p in ((2,49),(1,48),(3,48),(2,47)))
warp('Havora_Market', 6,43);m.snap('west-market-stalls')
warp('Havora_Market', 35,50);m.snap('east-market-stalls')
print('PASS connected houses, eight vendors, harbor circulation and Koga approaches', flush=True)
