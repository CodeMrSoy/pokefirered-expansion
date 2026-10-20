"""Civic district geometry, walkable routes, service exits and respawn data."""
import json,struct
from pathlib import Path
from collections import deque
R=Path(__file__).resolve().parents[1]
def read(p):return json.loads((R/p).read_text())
layouts=read('data/layouts/layouts.json')['layouts'];groups=read('data/maps/map_groups.json')['gMapGroup_QuantumIsland']
allmaps={read(f'data/maps/{n}/map.json')['id']:n for n in groups}
names=['QuantumPortCity','QuantumHavoraNorthDistrict','QuantumHavoraCoastalDaycare','QuantumHavoraNorthWalk','QuantumHavoraNorthQuay','QuantumHavoraWestQuay','QuantumHarbor','QuantumHarborRoad']
cache={}
def load(name):
 if name in cache:return cache[name]
 m=read(f'data/maps/{name}/map.json');l=next(l for l in layouts if l['id']==m['layout']);b=(R/l['blockdata_filepath']).read_bytes()
 assert len(b)==l['width']*l['height']*2
 assert (l['width']+15)*(l['height']+14)<=0x2800
 a=struct.unpack('<'+'H'*(len(b)//2),b)
 for kind in ['object_events','warp_events','coord_events','bg_events']:
  for e in m[kind]:assert 0<=e['x']<l['width'] and 0<=e['y']<l['height'],(name,e)
 cache[name]=m,l,a;return m,l,a
starts={'QuantumHavoraWestQuay':(3,67),'QuantumPortCity':(42,66),'QuantumHavoraNorthDistrict':(69,38),'QuantumHavoraCoastalDaycare':(2,24),'QuantumHavoraNorthWalk':(7,30)}
for name in names:load(name)
for name,start in starts.items():
 m,l,a=load(name);w,h=l['width'],l['height'];occupied={(o['x'],o['y']) for o in m['object_events']}
 q=deque([start]);seen={start}
 while q:
  x,y=q.popleft();z=a[y*w+x]>>12
  for xx,yy in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
   if not(0<=xx<w and 0<=yy<h) or (xx,yy) in seen or (xx,yy) in occupied:continue
   b=a[yy*w+xx];zz=b>>12
   if b&0xC00 or (z and zz and z!=zz):continue
   seen.add((xx,yy));q.append((xx,yy))
 walk={(x,y) for y in range(h) for x in range(w) if not a[y*w+x]&0xC00}-occupied
 assert walk<=seen,(name,'isolated walk cells',sorted(walk-seen)[:30])
 assert len(occupied)<=15
 for o in m['object_events']:
  x,y=o['x'],o['y'];assert a[y*w+x]&0xFC00==o['elevation']<<12,(name,'object collision/elevation',o)
  assert any(p in seen for p in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]),(name,'inaccessible NPC',o)
 for i,e in enumerate(m['warp_events']):
  assert (e['x'],e['y']) in seen,(name,'unreachable door',i)
  dest=read(f'data/maps/{allmaps[e["dest_map"]]}/map.json')
  back=dest['warp_events'][int(e['dest_warp_id'])]
  assert back['dest_map']==m['id'] and int(back['dest_warp_id'])==i,(name,'bad return',i,back)
 for co in m['connections']:
  if co['map'] not in allmaps:continue
  other,ol,oa=load(allmaps[co['map']]);opp={'left':'right','right':'left','up':'down','down':'up'}[co['direction']]
  assert any(c['map']==m['id'] and c['direction']==opp and c['offset']==-co['offset'] for c in other['connections']),(name,'nonreciprocal',co)
  seams=[]
  for n in range(h if co['direction'] in ['left','right'] else w):
   v=n-co['offset']
   if co['direction'] in ['left','right']:
    if not 0<=v<ol['height']:continue
    aa=a[n*w+(0 if co['direction']=='left' else w-1)];bb=oa[v*ol['width']+(ol['width']-1 if co['direction']=='left' else 0)]
   else:
    if not 0<=v<ol['width']:continue
    aa=a[(0 if co['direction']=='up' else h-1)*w+n];bb=oa[(ol['height']-1 if co['direction']=='up' else 0)*ol['width']+v]
   if not aa&0xC00 and not bb&0xC00:
    assert aa>>12==bb>>12,(name,'boundary elevation mismatch',co,n,hex(aa),hex(bb));seams.append(n)
  assert seams,(name,'no walking seam',co)
heal=next(e for e in read('src/data/heal_locations.json')['heal_locations'] if e['id']=='HEAL_LOCATION_QUANTUM_PORT_CITY')
assert (heal['map'],heal['x'],heal['y'])==('MAP_QUANTUM_HAVORA_NORTH_DISTRICT',64,18)
assert '{MAP(MAP_QUANTUM_HAVORA_NORTH_DISTRICT), HEAL_LOCATION_QUANTUM_PORT_CITY}' in (R/'src/region_map.c').read_text()
assert read('tools/havora/civic-tiles.json')['graphics_budget']<=1024
print('PASS: civic map sizes/buffers, elevation-aware circulation, accessible service doors/NPCs, reciprocal connections, and relocated healing/Fly coordinates')

# Regression: the coastal quay must occupy the former gap and allow its
# stair route all the way from the north square to the harbor.
qm,ql,qa=load('QuantumHavoraWestQuay')
assert (ql['width'],ql['height'])==(8,96)
assert ql['primary_tileset']=='gTileset_HavoraCityPrimary'
assert next(c['offset'] for c in qm['connections'] if c['map']=='MAP_QUANTUM_HARBOR')==64
for name in ['QuantumPortCity','QuantumHavoraWestQuay']:
 _,_,aa=load(name)
 assert not any((v&1023)==0x1c1 and v&0xc00 for v in aa), (name,'invisible pavement wall')
print('PASS: terraced quay circulation, expanded-map origin, and no invisible pavement barriers in the western seam')
# A reachable warp must still be painted as a door, not overwritten by paving.
attributes=(R/'data/tilesets/primary/havora_city/metatile_attributes.bin').read_bytes()+(R/'data/tilesets/secondary/havora_city/metatile_attributes.bin').read_bytes()
for name in starts:
 m,l,a=load(name)
 for e in m['warp_events']:
  mid=a[e['y']*l['width']+e['x']]&1023
  assert struct.unpack_from('<I',attributes,mid*4)[0]&0x1ff==0x60,(name,'door behavior overwritten',e)
 for o in m['object_events']:
  if o['movement_type']=='MOVEMENT_TYPE_WANDER_LEFT_AND_RIGHT':
   for x in range(o['x']-o['movement_range_x'],o['x']+o['movement_range_x']+1):
    assert a[o['y']*l['width']+x]&0xfc00==o['elevation']<<12,(name,'unsafe wandering range',o)
print('PASS: functional door metatile behaviors and unobstructed resident walking ranges')
