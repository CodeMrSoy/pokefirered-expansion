#!/usr/bin/env python3
"""Landscape the approved gym plateau, preserving the user's a8b19167 cliffs."""
import copy,json,struct,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[2]
BASE='a8b19167'
def js(p):return json.loads((R/p).read_text())
def old(p):return subprocess.check_output(['git','show',BASE+':'+p],cwd=R)
def words(b):return list(struct.unpack('<'+'H'*(len(b)//2),b))
def write(p,data):(R/p).write_bytes(struct.pack('<'+'H'*len(data),*data))
l=next(l for l in js('data/layouts/layouts.json')['layouts'] if l['name']=='Havora_WestQuadrant_Layout');w=l['width'];path=l['blockdata_filepath'];before=words(old(path));blocks=before.copy()
meta=json.loads(old('data/maps/Havora_WestQuadrant/map.json'))
M=[];A=[]
for group in ['primary','secondary']:
 p=f'data/tilesets/{group}/havora_city/';v=words(old(p+'metatiles.bin'));M += [tuple(v[i:i+8]) for i in range(0,len(v),8)];b=old(p+'metatile_attributes.bin');A += list(struct.unpack('<'+'I'*(len(b)//4),b))
# No graphic or palette changes: new prop definitions reuse existing dock timber,
# native fence posts, and the existing sand-colour graphic at palette 10.
manifest=R/'tools/havora/gym-garden.json'
assert not manifest.exists(),'Already installed; edit the map in Porymap.'
free=[i for i,m in enumerate(M) if not any(m) and not A[i]]
def add(m,a=0):
 i=free.pop(0);M[i]=tuple(m);A[i]=a;return i
sand=add([0xa365]*4+[0]*4)
wood=M[641][0];post=M[0x5f][4]
bench=[add(list(M[0][:4])+[wood,wood,post,0]),add(list(M[0][:4])+[wood,wood,0,post^1024])]
# All alterations stay on this elevation-6 terrace, never the cliffs or seam.
allowed={0,4,5,12,13,449}|set(range(0x84,0x8e))|{0x91,0x92,0x93}
reserved=set();paths=set();features=[]
def put(x,y,mid,solid=False):
 assert 4<=x<=30 and 1<=y<=22,(x,y)
 i=y*w+x;assert before[i]>>12==6,(x,y,hex(before[i]))
 assert (before[i]&1023) in allowed or (x,y) in reserved,(x,y,hex(before[i]))
 blocks[i]=(before[i]&0xf000)|(1024 if solid else 0)|mid
 reserved.add((x,y))
def rect(x,y,ww,hh,mid,solid=False):
 for yy in range(y,y+hh):
  for xx in range(x,x+ww):put(xx,yy,mid,solid)
def paving(x,y,ww,hh):
 for yy in range(y,y+hh):
  for xx in range(x,x+ww):paths.add((xx,yy))
def tree(x,y):
 for j,row in enumerate([[10,11],[23,24],[29,30]]):
  for i,mid in enumerate(row):put(x+i,y+j,mid,True)
def flowers(x,y,count=1):rect(x,y,count,1,2,True)
def bush(x,y):put(x,y,3,True)
def seat(x,y):
 for i,mid in enumerate(bench):put(x+i,y,mid,True)
 features.append({'kind':'bench','x':x,'y':y})
# Entrance spine, gym forecourt, side passage, and eastern staircase connector.
paving(10,1,3,9);paving(9,9,11,2);paving(17,10,3,8)
paving(10,17,15,1);paving(20,15,5,3);paving(24,15,2,2)
# Lookout branch and sheltered sitting pad.
paving(6,5,4,2);paving(6,4,2,1)
# Court approach, linked around the planting at its west side.
paving(24,12,2,3)
# Lower coastal garden path, without disturbing the existing two evergreens.
paving(20,18,2,4);paving(19,21,3,2)
# Paint path edges around the connected mask, including existing staircase tiles.
existing={(x,y) for y in range(0,24) for x in range(w) if before[y*w+x]&1023 in {449,*range(0x84,0x8e),0x91,0x92,0x93}}
for x,y in paths:
 n=(x,y-1) in paths|existing;s=(x,y+1) in paths|existing;e=(x+1,y) in paths|existing;west=(x-1,y) in paths|existing
 if not n and not west:mid=0x84
 elif not n and not e:mid=0x86
 elif not s and not west:mid=0x91
 elif not s and not e:mid=0x93
 elif not n:mid=0x85
 elif not s:mid=0x92
 elif not west:mid=0x89
 elif not e:mid=0x8b
 else:mid=449
 put(x,y,mid)
# Compact doubles court: ten by eight tiles including its fence.
rect(21,6,8,6,sand)
for x in range(20,30):put(x,5,0x5a,True)
for y in range(6,12):put(20,y,0x5f,True);put(29,y,0x60,True)
for x in range(20,30):
 if x not in (24,25):put(x,12,0x5a,True)
# A legible two-tile entry with no forced battle trigger.
for x in (24,25):put(x,12,sand)
features.append({'kind':'doubles_practice_court','origin':[20,5],'size':[10,8],'entry':[[24,12],[25,12]]})
# Two wooden seating areas made from existing shared graphics.
seat(6,4);seat(19,21)
# Native trees: irregular sheltered groups, clear routes and sight lines.
for x,y in [(4,1),(7,1),(4,7),(8,7),(14,1),(16,3),(17,6),(27,1),(29,2),(29,9),(20,1)]:tree(x,y)
# Only on naturally available grass: do not paint trees over a path.
for x,y in [(6,3),(8,3),(14,4),(15,7),(18,2),(19,4),(26,3),(28,4),(30,13),(16,18),(19,19),(23,19)]:
 if (x,y) not in paths and (x,y) not in reserved:bush(x,y)
for x,y in [(9,2),(6,8),(14,3),(16,5),(18,5),(28,3),(30,8),(28,13),(21,14),(23,18),(17,19),(22,22)]:
 if (x,y) not in paths and (x,y) not in reserved and (before[y*w+x]&1023) in allowed:flowers(x,y)
# Rugged lookout stones use the native General rock rather than new artwork.
for x,y in [(4,4),(5,9),(19,20)]:
 if (x,y) not in reserved:put(x,y,18,True)
put(8,17,1,True)
meta['bg_events'].append({'type':'sign','x':8,'y':17,'elevation':6,'player_facing_dir':'BG_EVENT_PLAYER_FACING_ANY','script':'Havora_WestQuadrant_GymSign'})
# Place the Gym Guide beside the front door, never on its doorway or wall.
for index,x,y,direction in [(0,18,16,'DOWN'),(3,8,6,'LEFT'),(4,19,14,'RIGHT')]:
 e=meta['object_events'][index];e.update(x=x,y=y,elevation=6,movement_type='MOVEMENT_TYPE_FACE_'+direction,movement_range_x=0,movement_range_y=0)
 # Ensure a dialogue actor is on passable pavement/grass.
 if (blocks[y*w+x]>>10)&3:put(x,y,449 if (x,y) in paths else 0)
# Pair members face each other across the doubles court, dialogue only.
for i,(x,y,direction,gfx) in enumerate([(23,7,'DOWN','SAILOR'),(26,7,'DOWN','SAILOR'),(23,10,'UP','MAN'),(26,10,'UP','WOMAN_1')]):
 e=copy.deepcopy(meta['object_events'][0]);e.update(graphics_id='OBJ_EVENT_GFX_'+gfx,x=x,y=y,elevation=6,movement_type='MOVEMENT_TYPE_FACE_'+direction,script='Havora_WestQuadrant_Practice'+str(i+1));meta['object_events'].append(e)
assert len(meta['object_events'])<=16
# The existing door uses terrace elevation 6; keep its coordinates and destination.
meta['warp_events'][0]['elevation']=6
write(path,blocks);(R/'data/maps/Havora_WestQuadrant/map.json').write_text(json.dumps(meta,indent=2)+'\n')
for group,offset,count in [('primary',0,640),('secondary',640,384)]:
 p=f'data/tilesets/{group}/havora_city/';write(p+'metatiles.bin',[v for m in M[offset:offset+count] for v in m]);(R/p/'metatile_attributes.bin').write_bytes(struct.pack('<'+'I'*count,*A[offset:offset+count]))
manifest.write_text(json.dumps({'base_commit':BASE,'added_metatiles':{'sand':sand,'bench':bench},'features':features,'path_cells':[list(p) for p in sorted(paths)],'changed_cells':sum(a!=b for a,b in zip(before,blocks)),'scope':'West gym plateau only; no terrain reshaping or new exits; practice trainers use dialogue, not battles.'},indent=2)+'\n')
print('Gym garden installed:',sum(a!=b for a,b in zip(before,blocks)),'map cells; no graphics or palette modifications.')
