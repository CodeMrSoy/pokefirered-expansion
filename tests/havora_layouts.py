"""Validate the authored harbor asset budget and every outdoor approach seam."""
import json,struct
from pathlib import Path
from collections import deque
R=Path(__file__).resolve().parents[1];ls=json.loads((R/'data/layouts/layouts.json').read_text())['layouts'];maps={}
def read(name):
 m=json.loads((R/f'data/maps/{name}/map.json').read_text());l=next(l for l in ls if l['id']==m['layout']);b=(R/l['blockdata_filepath']).read_bytes();w,h=l['width'],l['height']
 assert len(b)==2*w*h;assert (w+15)*(h+14)<=0x2800
 a=struct.unpack('<'+'H'*(len(b)//2),b);limit=1024 if l['secondary_tileset'] in ['gTileset_HavoraHarbor','gTileset_HavoraCity'] else 808
 assert all((v&1023)<limit for v in a)
 for k in ['object_events','warp_events','coord_events','bg_events']:
  for e in m[k]:assert 0<=e['x']<w and 0<=e['y']<h
 assert m['map_type'] in ['MAP_TYPE_CITY','MAP_TYPE_TOWN'];maps[m['id']]=(m,l,a);return m,l,a
h,hl,ha=read('QuantumHarbor');c,cl,ca=read('QuantumPortCity');read('QuantumHavoraWestQuay');read('QuantumHavoraNorthQuay')
assert (hl['width'],hl['height'])==(40,32);assert not h['warp_events'] and not h['coord_events'];assert not any(w['dest_map']=='MAP_QUANTUM_HARBOR' for w in c['warp_events'])
assert h['object_events'][0]['graphics_id']=='OBJ_EVENT_GFX_SEAGALLOP';assert h['object_events'][1]['script']=='QuantumHarbor_Sailor'
assert (h['object_events'][1]['x'],h['object_events'][1]['y'])==(21,18)
for mid,(m,l,a) in maps.items():
 for co in m['connections']:
  if co['map'] not in maps:continue
  other,ol,oa=maps[co['map']];opposite={'left':'right','right':'left','up':'down','down':'up'}[co['direction']]
  assert any(r['map']==mid and r['direction']==opposite and r['offset']==-co['offset'] for r in other['connections']),(mid,co)
  # Require at least one elevation-3 walking seam; test all overlapping cells.
  seams=[]
  for n in range(l['height'] if co['direction'] in ['left','right'] else l['width']):
   v=n-co['offset']
   if co['direction'] in ['left','right']:
    if not 0<=v<ol['height']:continue
    aa=a[n*l['width']+(0 if co['direction']=='left' else l['width']-1)];bb=oa[v*ol['width']+(ol['width']-1 if co['direction']=='left' else 0)]
   else:
    if not 0<=v<ol['width']:continue
    aa=a[(0 if co['direction']=='up' else l['height']-1)*l['width']+n];bb=oa[(ol['height']-1 if co['direction']=='up' else 0)*ol['width']+v]
   if aa&0xc00==0 and bb&0xc00==0:assert aa&0xf000==bb&0xf000==0x3000;seams.append(n)
  assert seams,(mid,co)
npc_cells={(o['x'],o['y']) for o in h['object_events']}
def component(start):
 q=deque([start]);seen={start}
 while q:
  x,y=q.popleft()
  for xx,yy in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
   if 0<=xx<40 and 0<=yy<32 and (xx,yy) not in seen and (xx,yy) not in npc_cells and ha[yy*40+xx]&0xc00==0:
    seen.add((xx,yy));q.append((xx,yy))
 return seen
def reachable(start,target):return target in component(start)
for p in [(0,2),(5,0),(20,18),(5,19),(15,24),(36,28),(13,6),(24,6),(14,24)]:assert reachable((20,18),p),p
asset=json.loads((R/'tools/havora/assets.json').read_text());assert asset['tiles']<=1024;assert asset['secondary_tiles']<=384;assert asset['metatiles']<=384
# Coping and dock changes must not create isolated walkable pockets.
walkable={(x,y) for y in range(32) for x in range(40) if ha[y*40+x]&0xfc00==0x3000} - npc_cells
assert walkable<=component((20,18)),walkable-component((20,18))
# New coastal details are solid and preserve the authored walking connections.
solid_ids={asset['assets'][name]['metatiles'][0][0] for name in ['zz_water_boulder','bollard','planter']}
for block in ha:
 if block&1023 in solid_ids:assert block&0x400
for directory in ['primary','secondary']:
 path=R/'data/tilesets'/directory/'havora_harbor';data=(path/'metatiles.bin').read_bytes()
 for v in struct.unpack('<'+'H'*(len(data)//2),data):
  assert (v&1023)<max(640,asset['tiles']);assert (v>>12)<13
assert len(asset['catalog'])>=500
pacific={e['source_id'] for e in asset['catalog'] if e['town']=='pacifidlog'}
assert set(range(0x208,0x22f))<=pacific
assert set(range(0x250,0x254))|set(range(0x258,0x264))<=pacific
assert asset['animation']['frames']==8
assert asset['animation']['start']+asset['animation']['slots']==1024
print('PASS: graphics budget, native tile references, 40x32 blocks, event bounds, no harbor warps, all reciprocal seams and walking routes')

# Native compatibility: animation destinations, pavement, water and shrub tiles
# remain byte-identical to General, including their required palette banks.
from PIL import Image
import numpy as np
general=R/'data/tilesets/primary/general';primary=R/'data/tilesets/primary/havora_harbor'
g=Image.open(general/'tiles.png');p=Image.open(primary/'tiles.png')
for tid in asset['reserved_primary_tiles']:
 box=((tid%16)*8,(tid//16)*8,(tid%16)*8+8,(tid//16)*8+8)
 assert np.array_equal(np.array(g.crop(box)),np.array(p.crop(box))),tid
for bank in [0,1,6]:
 assert (general/'palettes'/f'{bank:02}.pal').read_text().splitlines()[3:19]==(primary/'palettes'/f'{bank:02}.pal').read_text().splitlines()[3:19]
print('PASS: reserved General animation tiles and compatible paving/water/shrub palettes')
