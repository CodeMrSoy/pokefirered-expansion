#!/usr/bin/env python3
"""Verify the gym-garden patch against the user's latest cliff layout."""
import json,struct,subprocess
from pathlib import Path
from collections import deque
R=Path(__file__).resolve().parents[2];BASE='553b2f28'
def old(p):return subprocess.check_output(['git','show',BASE+':'+p],cwd=R)
def js(p):return json.loads((R/p).read_text())
def words(b):return list(struct.unpack('<'+'H'*(len(b)//2),b))
l=next(l for l in js('data/layouts/layouts.json')['layouts'] if l['name']=='HavoraWestQuadrant_Layout');w=l['width'];b=words((R/l['blockdata_filepath']).read_bytes());a=words(old(l['blockdata_filepath']));m=js('data/maps/HavoraWestQuadrant/map.json');om=json.loads(old('data/maps/HavoraWestQuadrant/map.json'))
assert len(b)==w*l['height']
assert m['connections']==om['connections']
assert len(m['warp_events'])==len(om['warp_events'])
for i,(u,v) in enumerate(zip(m['warp_events'],om['warp_events'])):
 assert {k:x for k,x in u.items() if k!='elevation'}=={k:x for k,x in v.items() if k!='elevation'}
 assert u['elevation']==(6 if i==0 else v['elevation'])
# Other map data, borders, dimensions and original tile definitions stay intact.
for layout in js('data/layouts/layouts.json')['layouts']:
 if layout['primary_tileset']!='gTileset_HavoraCityPrimary':continue
 for key in ('border_filepath','blockdata_filepath'):
  p=layout[key]
  if p!=l['blockdata_filepath']:assert (R/p).read_bytes()==old(p),p
assert (R/'data/layouts/layouts.json').read_bytes()==old('data/layouts/layouts.json')
extension=js('tools/havora/editor-kits.json') if (R/'tools/havora/editor-kits.json').exists() else {}
added=set(v for ids in js('tools/havora/gym-garden.json')['added_metatiles'].values() for v in (ids if isinstance(ids,list) else [ids]));added |= set(extension.get('new_metatiles',[])) | set(extension.get('retired_unplaced',[]));defs=[];original_defs=[];attrs=[];gfx_before=[];gfx_after=[]
for group in ('primary','secondary'):
 p='data/tilesets/'+group+'/havora_city/';raw=(R/p/'metatiles.bin').read_bytes();prior=old(p+'metatiles.bin');offset=0 if group=='primary' else 640
 for j in range(len(raw)//16):
  if j+offset not in added:assert raw[j*16:j*16+16]==prior[j*16:j*16+16]
 ar=(R/p/'metatile_attributes.bin').read_bytes();oa=old(p+'metatile_attributes.bin')
 for j in range(len(ar)//4):
  if j+offset not in added:assert ar[j*4:j*4+4]==oa[j*4:j*4+4]
 from PIL import Image
 import io
 for dest,data in [(gfx_before,old(p+'tiles.png')),(gfx_after,(R/p/'tiles.png').read_bytes())]:
  im=Image.open(io.BytesIO(data));dest.extend(im.crop((x,y,x+8,y+8)).tobytes() for y in range(0,im.height,8) for x in range(0,128,8))
 for pp in (R/p/'palettes').glob('*.pal'):assert pp.read_text().splitlines()==old(str(pp.relative_to(R))).decode().splitlines()
 v=words(raw);defs += [v[j:j+8] for j in range(0,len(v),8)];ov=words(prior);original_defs += [ov[j:j+8] for j in range(0,len(ov),8)];raw=(R/p/'metatile_attributes.bin').read_bytes();attrs+=list(struct.unpack('<'+'I'*(len(raw)//4),raw))
used=set()
for layout in js('data/layouts/layouts.json')['layouts']:
 if layout['primary_tileset']=='gTileset_HavoraCityPrimary':
  for key in ('blockdata_filepath','border_filepath'):used |= {v&1023 for v in words(old(layout[key]))}
for mid in used:
 assert defs[mid]==original_defs[mid],mid
 for v in defs[mid]:assert gfx_before[v&1023]==gfx_after[v&1023]
fixed=set(range(416,482))|set(range(508,512))|set(range(896,1024))|set(js('tools/havora/fountain.json')['animation_graphic_ids'])
assert all(gfx_before[i]==gfx_after[i] for i in fixed)
changed=[]
for i,(u,v) in enumerate(zip(a,b)):
 if u==v:continue
 x,y=i%w,i//w;assert 4<=x<=30 and 1<=y<=22
 assert u>>12==v>>12==6
 assert u&1023 in {0,4,5,12,13,449,*range(0x84,0x8e),0x91,0x92,0x93}
 changed.append((x,y))
assert len(m['object_events'])<=16
occupied={(e['x'],e['y']) for e in m['object_events']}
def foot(x,y):
 if not(0<=x<w and 0<=y<25):return False
 if 7<=x<=16 and 11<=y<=16 and (x,y)!=(11,16):return False
 v=b[y*w+x]
 return (v>>10)&3==0 and attrs[v&1023]&511 not in range(0x10,0x20)
start=(10,0);q=deque([start]);seen={start}
while q:
 x,y=q.popleft();u=b[y*w+x]
 for xx,yy in [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]:
  if not foot(xx,yy) or (xx,yy) in occupied|seen:continue
  v=b[yy*w+xx]
  if u>>12!=v>>12 and not({u>>12,v>>12}&{0,15}):continue
  seen.add((xx,yy));q.append((xx,yy))
goals={'gym_front_door':(11,16),'court_entry':(24,12),'lookout_bench':(6,5),'garden_bench':(20,22),'gym_sign':(9,17),'east_stairs':(29,17),'south_stairs':(25,23)}
for name,p in goals.items():assert p in seen,(name,p,'unreachable with actors as obstacles')
for e in m['object_events'][:1]+m['object_events'][3:5]+m['object_events'][10:]:
 x,y=e['x'],e['y'];assert foot(x,y),(e['script'],'not walkable');assert e['elevation']==b[y*w+x]>>12
 assert any((x+dx,y+dy) in seen for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]),(e['script'],'cannot talk to actor')
assert len(occupied)==len(m['object_events'])
report={'result':'PASS','base_commit':BASE,'changed_cells':len(changed),'objects':len(m['object_events']),'added_metatiles':sorted(added),'reachable_goals':{name:list(p) for name,p in goals.items()},'preserved':['cliff and water tiles','all map seams and offsets','harbor/ferry data','original tile art and animation graphics','all palettes','warp coordinates and destinations'],'limitations':['Static movement checks only; no emulator or Porymap walkthrough.','Existing North Lodge return warp index 7 targets a North Quadrant that currently has only five entries; unchanged by this patch.']}
print(json.dumps(report,indent=2))
