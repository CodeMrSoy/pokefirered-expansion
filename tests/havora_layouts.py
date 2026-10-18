"""Validate the authored harbor asset budget and every outdoor approach seam."""
import json,struct
from pathlib import Path
from collections import deque
R=Path(__file__).resolve().parents[1];ls=json.loads((R/'data/layouts/layouts.json').read_text())['layouts'];maps={}
def read(name):
 m=json.loads((R/f'data/maps/{name}/map.json').read_text());l=next(l for l in ls if l['id']==m['layout']);b=(R/l['blockdata_filepath']).read_bytes();w,h=l['width'],l['height']
 assert len(b)==2*w*h;assert (w+15)*(h+14)<=0x2800
 a=struct.unpack('<'+'H'*(len(b)//2),b);limit=713 if l['secondary_tileset']=='gTileset_HavoraHarbor' else 808
 assert all((v&1023)<limit for v in a)
 for k in ['object_events','warp_events','coord_events','bg_events']:
  for e in m[k]:assert 0<=e['x']<w and 0<=e['y']<h
 assert m['map_type'] in ['MAP_TYPE_CITY','MAP_TYPE_TOWN'];maps[m['id']]=(m,l,a);return m,l,a
h,hl,ha=read('QuantumHarbor');c,cl,ca=read('QuantumPortCity');read('QuantumHavoraWestQuay');read('QuantumHavoraNorthQuay')
assert (hl['width'],hl['height'])==(40,32);assert not h['warp_events'] and not h['coord_events'];assert not any(w['dest_map']=='MAP_QUANTUM_HARBOR' for w in c['warp_events'])
assert h['object_events'][0]['graphics_id']=='OBJ_EVENT_GFX_SEAGALLOP';assert h['object_events'][1]['script']=='QuantumHarbor_Sailor'
assert (h['object_events'][1]['x'],h['object_events'][1]['y'])==(20,20)
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
def reachable(start,target):
 q=deque([start]);seen={start}
 while q:
  x,y=q.popleft()
  if (x,y)==target:return True
  for xx,yy in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
   if 0<=xx<40 and 0<=yy<32 and (xx,yy) not in seen and ha[yy*40+xx]&0xc00==0:
    seen.add((xx,yy));q.append((xx,yy))
 return False
for p in [(0,2),(5,0),(20,21),(5,23),(16,25),(35,27),(14,5),(24,5),(10,11),(9,17)]:assert reachable((20,19),p),p
asset=json.loads((R/'tools/havora/assets.json').read_text());assert asset['tiles']<=384;assert asset['metatiles']<=384
path=R/'data/tilesets/secondary/havora_harbor';data=(path/'metatiles.bin').read_bytes()
for v in struct.unpack('<'+'H'*(len(data)//2),data):assert (v&1023)<640+asset['tiles'];assert (v>>12)<13
print('PASS: graphics budget, native tile references, 40x32 blocks, event bounds, no harbor warps, all reciprocal seams and walking routes')
