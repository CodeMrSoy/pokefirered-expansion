#!/usr/bin/env python3
"""Uncommitted city design preview. Rebuild from reviewed ac291bc1 map data."""
import json,struct,subprocess,copy
from pathlib import Path
from collections import deque
R=Path(__file__).resolve().parents[2];BASE='ac291bc1'
def js(p):return json.loads((R/p).read_text())
def old(p):return subprocess.check_output(['git','show',BASE+':'+p],cwd=R)
def ww(b):return list(struct.unpack('<'+'H'*(len(b)//2),b))
L={l['name'].replace('_Layout',''):l for l in js('data/layouts/layouts.json')['layouts']};names=['Havora_Market','Havora_WestQuadrant','Havora_NorthQuadrant','Havora_DaycareExterior']
V={n:ww(old(L[n]['blockdata_filepath'])) for n in names};original=copy.deepcopy(V);M={n:json.loads(old(f'data/maps/{n}/map.json')) for n in names}
green=js('tools/havora/green-houses.json')['kits'];long=js('tools/havora/native-houses.json')['kits']['cerulean_home'];fountains=js('tools/havora/fountain.json');civil=js('tools/havora/civic-tiles.json')['assets'];stall=js('tools/havora/authoring-assets.json')['market_stall']
cliffs=set(range(33,77))|{166,167,168,169,170,171,642}
flat=set(range(33))|{449,640,834,1};structures=set();doors=[];newbuildings=[];reserved={n:set() for n in names};trees={n:[] for n in names}
for n in names:
 w=L[n]['width']
 for y in range(L[n]['height']-2):
  for x in range(w-1):
   if [V[n][(y+j)*w+x+i]&1023 for j in range(3) for i in range(2)]==[10,11,23,24,29,30]:trees[n].append({(x+i,y+j) for j in range(3) for i in range(2)})
def clear_tree(n,x,y):
 for cells in trees[n]:
  if (x,y) in cells and not cells&reserved[n]:
   for a,b in cells:V[n][b*L[n]['width']+a]=(V[n][b*L[n]['width']+a]&0xf000)
def tile(n,x,y,mid,solid=False,force=False):
 w=L[n]['width']
 if not (0<=x<w and 0<=y<L[n]['height']):return False
 if solid and any(n==name and x==dx and dy<=y<=dy+2 for name,dx,dy,index in doors):return False
 if not force and ((x,y) in reserved[n] or V[n][y*w+x]&1023 not in flat):return False
 if not force:clear_tree(n,x,y)
 v=V[n][y*w+x];V[n][y*w+x]=(v&0xf000)|(1024 if solid else 0)|mid;return True
def rect(n,x,y,w,h,mid=449,solid=False,force=False):
 for j in range(h):
  for i in range(w):tile(n,x+i,y+j,mid,solid,force)
def clear(n,x,y,w,h):
 # Explicit former building footprints may be cleared; terrain outside them is guarded.
 for j in range(h):
  for i in range(w):
   if original[n][(y+j)*L[n]['width']+x+i]&1023 not in cliffs:tile(n,x+i,y+j,0,force=True)
def path(n,points,width=2):
 for (x,y),(xx,yy) in zip(points,points[1:]):
  assert x==xx or y==yy
  rect(n,min(x,xx),min(y,yy),abs(xx-x)+width,abs(yy-y)+width)
def stamp(n,x,y,grid,collision=None,label='decoration'):
 for j,row in enumerate(grid):
  for i,mid in enumerate(row):
   pos=(y+j)*L[n]['width']+x+i
   assert 0<=x+i<L[n]['width'] and 0<=y+j<L[n]['height']
   assert V[n][pos]&1023 in flat,(n,label,x+i,y+j,hex(V[n][pos]&1023))
 for j,row in enumerate(grid):
  for i,mid in enumerate(row):
   clear_tree(n,x+i,y+j);tile(n,x+i,y+j,mid, bool(collision[j][i]) if collision else True,True);reserved[n].add((x+i,y+j))
 return (x,y,len(grid[0]),len(grid))
def warp(n,index,x,y):
 e=M[n]['warp_events'][index];e.update(x=x,y=y,elevation=V[n][y*L[n]['width']+x]>>12);V[n][y*L[n]['width']+x]&=~0xc00;doors.append((n,x,y,index));return e
def house(n,x,y,kind,index):
 grid=long if kind=='long' else green[kind];h=len(grid);w=len(grid[0]);rect(n,x-1,y-1,w+2,h+3,640)
 stamp(n,x,y,grid,label=kind);dx=x+(2 if kind=='long' else 1);dy=y+3;warp(n,index,dx,dy)
 # Native garden kits have a final planter row around their walkable doorstep.
 if kind=='viridian_garden':V[n][(dy+1)*L[n]['width']+dx]&=~0xc00
 reserved[n].discard((dx,dy+1));tile(n,dx,dy+1,449,force=True);tile(n,dx,dy+2,449)
 newbuildings.append({'map':n,'kind':kind,'origin':[x,y],'door':[dx,dy],'warp':index})
def fountain(n,x,y):
 rect(n,x-2,y-1,7,6,449);stamp(n,x,y,fountains['kits']['paving'],fountains['collision_mask'],'fountain');newbuildings.append({'map':n,'kind':'fountain','origin':[x,y]})
def tree(n,x,y):
 cells={(x+i,y+j) for j in range(3) for i in range(2)}
 if any(a<0 or b<0 or a>=L[n]['width'] or b>=L[n]['height'] or (a,b) in reserved[n] or V[n][b*L[n]['width']+a]&1023 not in {0,4,5,12,13} for a,b in cells):return
 stamp(n,x,y,[[10,11],[23,24],[29,30]],label='tree')
def flowers(n,x,y,count=3):
 for i in range(count):tile(n,x+i,y,2,True)
def bush(n,x,y):tile(n,x,y,3,True)
# MARKET: preserve the terraces and shift retail to the lower shopping promenade.
n='Havora_Market'
clear(n,31,5,4,5);clear(n,4,13,4,5);clear(n,28,21,8,5)
house(n,31,5,'viridian_home',1);house(n,4,13,'viridian_garden',2)
# Formal plaza: remove the scattered old planters from the central square.
# Existing planter IDs are recovered from the current asset mapping, not guessed.
a=js('tools/havora/assets.json')['assets']['planter']['metatiles'];mp=js('tools/havora/shared-tileset.json')['metatile_mapping']['harbor'];plant={mp[str(v)] for row in a for v in row}
for y in range(16,26):
 for x in range(15,25):
  if V[n][y*41+x]&1023 in plant:tile(n,x,y,449,force=True)
fountain(n,19,18)
# Eight stalls, generous browsing aisles, uninterrupted north/south circulation.
clear(n,1,27,38,12);rect(n,2,27,36,11,449)
stalls=[]
for y in [28,33]:
 for x in [4,10,27,33]:stamp(n,x,y,stall,label='stall');stalls.append((x,y))
for x,y in [(2,27),(37,27),(2,35),(37,35)]:bush(n,x,y)
for x in [4,10,27,33]:flowers(n,x,37,3)
# Clear only the lower east parcel; all original perimeter cliffs stay intact.
clear(n,26,47, 0,13);rect(n,26,42,12,15,640)
store=green['celadon_department_store'];stamp(n,27,43,store,label='department store')
warp(n,6,29,52);extra=copy.deepcopy(M[n]['warp_events'][6]);M[n]['warp_events'].append(extra);warp(n,len(M[n]['warp_events'])-1,33,52)
path(n,[(28,53),(24,53)],3);path(n,[(32,53),(32,57),(27,57)],2)
newbuildings.append({'map':n,'kind':'department_store','origin':[27,43],'doors':[[29,52],[33,52]],'interior':'existing Havora provisions shop'})
# Former provisions plot is now a pocket garden beside the trading square.
rect(n,28,21,8,5,0);path(n,[(28,24),(36,24)],2)
for x,y in [(28,21),(33,21),(5,44),(7,50),(3,53),(17,45),(21,50)]:tree(n,x,y)
for x,y,c in [(28,23,6),(28,26,6),(3,47,5),(3,56,7),(17,55,6)]:flowers(n,x,y,c)
for x,y in [(14,17),(24,17),(14,24),(24,24),(3,42),(8,42),(17,43),(22,43),(27,55),(36,55)]:bush(n,x,y)
path(n,[(3,45),(3,53),(9,53),(9,45),(3,45)],1)
# The port emblem becomes a meeting point, with room on either side to pass.
stamp(n,20,30,[[173],[488]],label='statue')
# Reposition vendors in front of each counter; use the existing shop script.
vendors=[e for e in M[n]['object_events'] if e['script']=='Havora_Market_Supplies']
while len(vendors)<8:
 e=copy.deepcopy(vendors[0]);M[n]['object_events'].append(e);vendors.append(e)
for e,(x,y) in zip(vendors,stalls):e.update(x=x+1,y=y+3,movement_type='MOVEMENT_TYPE_FACE_UP')
# WEST: link the gym terrace and cliffside residential lanes.
n='Havora_WestQuadrant';path(n,[(9,0),(9,14),(26,14)],3)
for args in [(5,5,'viridian_garden',1),(25,4,'viridian_home',2),(15,32,'long',3),(23,37,'viridian_home',4),(8,35,'viridian_garden',5),(15,42,'viridian_home',6),(23,31,'viridian_garden',7)]:house(n,*args)
warp(n,0,21,13)
path(n,[(6,9),(6,14),(18,14)],2);path(n,[(26,8),(26,14)],2)
path(n,[(28,28),(28,49),(16,49),(16,53)],2);path(n,[(9,39),(13,39),(13,36),(27,36)],2);path(n,[(16,46),(21,46),(21,39),(27,39)],2)
fountain(n,13,10)
for x,y in [(4,2),(13,3),(28,1),(4,12),(12,6),(17,7),(15,18),(11,29),(20,29),(7,42),(19,40),(23,44),(31,34)]:tree(n,x,y)
for x,y,c in [(5,11,5),(25,10,4),(14,16,4),(9,41,4),(15,47,4),(23,41,3)]:flowers(n,x,y,c)
# NORTH: match the west boundary walkway and give the services their full roofs.
n='Havora_NorthQuadrant';path(n,[(14,11),(14,27)],3)
for args in [(6,5,'viridian_garden',3),(5,15,'viridian_home',2),(73,16,'long',4),(49,15,'viridian_garden',7)]:house(n,*args)
path(n,[(7,9),(7,12),(15,12)],2);path(n,[(6,19),(6,22),(18,22)],2);path(n,[(50,19),(50,21),(63,21)],2);path(n,[(75,20),(63,20)],2)
# Existing roof fragments are within these plots; keep surrounding cliff tiles.
for x,kind,index in [(73,'center',0),(80,'mart',1)]:
 clear(n,x,3,4,4)
 # Close the old roof openings in the ridge and give both full buildings room.
 rect(n,x,3,4,2,51,True,True)
 clear(n,x,5,len(civil[kind][0]),4)
 stamp(n,x,5,civil[kind],label=kind);warp(n,index,x+2,8);path(n,[(x+2,9),(x+2,10)],2)
fountain(n,68,16)
for x,y in [(3,5),(11,5),(5,23),(10,23),(22,6),(32,5),(49,6),(54,16),(66,4),(85,4),(81,17),(85,21),(56,23)]:tree(n,x,y)
for x,y,c in [(6,11,5),(6,21,4),(49,21,6),(67,22,7),(73,22,7),(73,8,2),(80,8,2)]:flowers(n,x,y,c)
for x,y in [(67,14),(72,14),(67,21),(72,21),(60,13),(65,13),(87,14)]:bush(n,x,y)
# Small groves soften the civic approach without closing the route north.
for x,y in [(1,19),(24,6),(26,14),(49,7),(54,7),(56,13),(83,23)]:tree(n,x,y)
flowers(n,49,11,5)
for x,y in [(48,12),(55,12),(57,8),(85,16)]:bush(n,x,y)
# DAYCARE: a sheltered garden walk along the coastal paddock, no extra houses.
n='Havora_DaycareExterior';path(n,[(0,16),(7,16),(7,24),(13,24)],2);path(n,[(7,15),(7,16)],2)
for x,y in [(1,8),(1,20),(4,22),(10,19),(12,23)]:tree(n,x,y)
for x,y,c in [(3,18,3),(9,17,3),(4,25,4),(10,25,3),(5,8,2),(9,6,3)]:flowers(n,x,y,c)
# Fix old resize artifacts in NPC positions, then keep every actor off buildings
# and off the doorway/landing squares. No added labels or non-native sprites.
manual={'Havora_NorthQuadrant':{0:(70,12),1:(63,11),2:(62,3),3:(75,9),4:(82,9),8:(59,5),9:(9,23)},'Havora_DaycareExterior':{0:(10,15),1:(8,8),2:(12,10),3:(5,18),4:(12,22)}}
for n,changes in manual.items():
 for i,(x,y) in changes.items():M[n]['object_events'][i].update(x=x,y=y)
landing={(n,x,y+d) for n,x,y,i in doors for d in [0,1]}
for n in names:
 occupied=set()
 for e in M[n]['object_events']:
  x,y=e['x'],e['y'];w=L[n]['width'];h=L[n]['height'];candidates=[]
  for radius in range(0,20):
   for yy in range(max(0,y-radius),min(h,y+radius+1)):
    for xx in range(max(0,x-radius),min(w,x+radius+1)):
     if abs(xx-x)+abs(yy-y)>radius:continue
     v=V[n][yy*w+xx]
     if v&0xc00==0 and v&1023!=642 and (xx,yy) not in occupied and (n,xx,yy) not in landing:candidates.append((xx,yy))
   if candidates:break
  assert candidates,(n,e['script']);xx,yy=min(candidates,key=lambda a:abs(a[0]-x)+abs(a[1]-y));e.update(x=xx,y=yy,elevation=V[n][yy*w+xx]>>12,movement_range_x=0,movement_range_y=0);occupied.add((xx,yy))
# Every old cliff/water/stair cell is immutable, including collision/elevation.
cliffs=set(range(33,77))|{166,167,168,169,170,171,642}
for n in names:
 for i,a in enumerate(original[n]):
  if a&1023 in cliffs:assert V[n][i]==a,(n,'terrain changed',i%L[n]['width'],i//L[n]['width'])
 for name,x,y,index in doors:
  if name==n:
   assert V[n][y*L[n]['width']+x]&0xc00==0
 for p in [L[n]['border_filepath']]:assert (R/p).read_bytes()==old(p)
 (R/L[n]['blockdata_filepath']).write_bytes(struct.pack('<'+'H'*len(V[n]),*V[n]));(R/f'data/maps/{n}/map.json').write_text(json.dumps(M[n],indent=2)+'\n')
(R/'tools/havora/city-review.json').write_text(json.dumps({'base':BASE,'buildings':newbuildings,'doors':doors,'uncommitted_review':True,'harbor_and_tilesets_untouched':True},indent=2)+'\n')
print('City review written; no commit or push performed.')
