"""Validate native blocks, ferry events and the reciprocal outdoor seam."""
import json,struct,subprocess
from pathlib import Path
from collections import deque
R=Path(__file__).resolve().parents[1]
layouts=json.loads((R/'data/layouts/layouts.json').read_text())['layouts']
def read(name):
 m=json.loads((R/f'data/maps/{name}/map.json').read_text());l=next(l for l in layouts if l['id']==m['layout']);b=(R/l['blockdata_filepath']).read_bytes()
 assert len(b)==2*l['width']*l['height'];assert (l['width']+15)*(l['height']+14)<=0x2800
 assert l['primary_tileset']=='gTileset_General' and l['secondary_tileset']=='gTileset_VermilionCity'
 a=struct.unpack('<'+'H'*(len(b)//2),b);assert all((v&1023)<808 for v in a)
 for k in ['object_events','warp_events','coord_events','bg_events']:
  for e in m[k]:assert 0<=e['x']<l['width'] and 0<=e['y']<l['height']
 assert m['map_type']=='MAP_TYPE_CITY'
 return m,l,a
h,hl,ha=read('QuantumHarbor');c,cl,ca=read('QuantumPortCity')
assert (hl['width'],hl['height'])==(40,32)
for name,m in [('QuantumHarbor',h),('QuantumPortCity',c)]:
 old=json.loads(subprocess.check_output(['git','show','563419b86:data/maps/'+name+'/map.json'],cwd=R))
 assert m['object_events'][:len(old['object_events'])]==old['object_events'];assert m['warp_events']==old['warp_events']
for y in [1,2,3]:
 assert ha[y*40]&0xfc00==0x3000;assert ca[y*80+79]&0xfc00==0x3000
assert {'map':'MAP_QUANTUM_PORT_CITY','offset':0,'direction':'left'} in h['connections']
assert {'map':'MAP_QUANTUM_HARBOR','offset':0,'direction':'right'} in c['connections']
def reachable(a,w,h,start,target):
 q=deque([start]);seen={start}
 while q:
  x,y=q.popleft()
  if (x,y)==target:return True
  for xx,yy in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
   if 0<=xx<w and 0<=yy<h and (xx,yy) not in seen and a[yy*w+xx]&0xc00==0:
    seen.add((xx,yy));q.append((xx,yy))
 return False
for point in [(0,2),(8,6),(24,24),(32,21),(38,27)]:assert reachable(ha,40,32,(8,5),point),point
assert reachable(ca,80,80,(79,2),(11,11))
print('PASS: map sizes, tile IDs, outdoor headers, preserved ferry/events/warps, seam and walkable routes')
