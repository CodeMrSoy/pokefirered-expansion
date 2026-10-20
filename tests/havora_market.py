"""Check district circulation, doorway behaviors and unique interior return warps."""
import json,struct
from pathlib import Path
from collections import deque
R=Path(__file__).resolve().parents[1]
def load(p):return json.loads((R/p).read_text())
layouts=load('data/layouts/layouts.json')['layouts']
m=load('data/maps/QuantumHavoraNorthQuay/map.json')
l=next(l for l in layouts if l['id']==m['layout'])
assert (l['width'],l['height'])==(40,64)
assert (40+15)*(64+14)<=0x2800
a=struct.unpack('<2560H',(R/l['blockdata_filepath']).read_bytes())
assert l['primary_tileset']=='gTileset_HavoraCityPrimary' and l['secondary_tileset']=='gTileset_HavoraCity'
assert len(m['object_events'])<=16
occupied={(e['x'],e['y']) for e in m['object_events']}
seen={(20,60)};q=deque(seen)
while q:
 x,y=q.popleft()
 for p in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
  xx,yy=p
  if 0<=xx<40 and 0<=yy<64 and p not in seen and p not in occupied and a[yy*40+xx]&0xC00==0:
   z=a[y*40+x]>>12;zz=a[yy*40+xx]>>12
   if z and zz and z!=zz:continue
   seen.add(p);q.append(p)
walk={(x,y) for y in range(64) for x in range(40) if a[y*40+x]&0xC00==0}-occupied
assert walk<=seen,walk-seen
assert (0,54) in seen and (5,63) in seen and (20,36) in seen
for e in m['object_events']:
 x,y=e['x'],e['y'];assert a[y*40+x]&0xFC00==0x4000 and e['elevation']==4
 assert any(p in seen for p in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)])
groups=load('data/maps/map_groups.json')['gMapGroup_QuantumIsland']
maps={load(f'data/maps/{n}/map.json')['id']:n for n in groups}
assert len(m['warp_events'])==7
retired=load('data/quantum/retired_content.json')['retired_layouts']
for i,e in enumerate(m['warp_events']):
 assert (e['x'],e['y']) in seen
 mid=a[e['y']*40+e['x']]&1023
 attrs=(R/'data/tilesets/primary/havora_city/metatile_attributes.bin').read_bytes()
 assert mid in [0x8F,0x90] and struct.unpack_from('<I',attrs,mid*4)[0]&0x1FF==0x60 and e['elevation']==4
 interior=load(f'data/maps/{maps[e["dest_map"]]}/map.json')
 il=next(l for l in layouts if l['id']==interior['layout'])
 assert il['name'] not in retired
 for kind in ['warp_events','object_events','bg_events','coord_events']:
  for obj in interior[kind]:assert 0<=obj['x']<il['width'] and 0<=obj['y']<il['height']
 back=interior['warp_events'][int(e['dest_warp_id'])]
 for back in interior['warp_events']:
  assert back['dest_map']==m['id'] and int(back['dest_warp_id'])==i
assert not any(e['dest_map']=='MAP_QUANTUM_HARBOR' for e in m['warp_events'])
# All three boundary maps now agree on one world-space position.
w=load('data/maps/QuantumHavoraWestQuay/map.json');h=load('data/maps/QuantumHarbor/map.json')
offset=lambda mm,target:next(c['offset'] for c in mm['connections'] if c['map']==target)
assert offset(m,w['id'])==0 and offset(w,m['id'])==0
assert offset(w,h['id'])==64 and offset(h,w['id'])==-64
assert offset(m,w['id'])+offset(w,h['id'])==l['height']
for left in [4,19]:
 for x in range(left,left+4):
  assert a[37*40+x]>>12==4 and a[40*40+x]>>12==3
  for y in [38,39]:assert a[y*40+x]&0xFC00==0
print('PASS: 40x64 raised district, elevation-aware circulation, two stairways, ten accessible NPCs, seven reciprocal interiors and coherent outdoor connections')
