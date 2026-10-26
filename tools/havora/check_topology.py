#!/usr/bin/env python3
"""Check Havora naming, stable map numbers, geometry and preserved authored art."""
import json,re,struct,subprocess
from pathlib import Path
from collections import deque
R=Path(__file__).resolve().parents[2]
BASE='a85c6562'
RENAMES={'Havora_Harbor':'Havora_Harbor','Havora_Market':'Havora_Market','Havora_NorthQuadrant':'Havora_NorthQuadrant','Havora_WestQuadrant':'Havora_WestQuadrant','Havora_DaycareExterior':'Havora_DaycareExterior','Havora_River':'Havora_River','Havora_Lookout':'Havora_Lookout','Havora_CoastalCliffs':'Havora_CoastalCliffs'}
def load(p):return json.loads((R/p).read_text())
def source(p):return subprocess.check_output(['git','show',BASE+':'+p],cwd=R)
def words(b):return [v[0] for v in struct.iter_unpack('<H',b)]
L={l['id']:l for l in load('data/layouts/layouts.json')['layouts']}
oldL={l['id']:l for l in json.loads(source('data/layouts/layouts.json'))['layouts']}
allowed={}
placement_manifest=R/'tools/havora/green-house-placements.json'
if placement_manifest.exists():
 p=load('tools/havora/green-house-placements.json');kits=load('tools/havora/green-houses.json')['kits'];kits['long_home']=p['long_home_grid']
 for e in p['placements']:
  cells=allowed.setdefault(e['map'],set());x,y,w,h=e['old_rectangle'];cells.update((x+i,y+j) for j in range(h) for i in range(w));x,y=e['new_origin'];grid=kits[e['kit']];cells.update((x+i,y+j) for j,row in enumerate(grid) for i in range(len(row)));x,y=e['door'];cells.add((x,y+1))
M={n:load(f'data/maps/{n}/map.json') for n in RENAMES.values()};ids={m['id']:n for n,m in M.items()};events=[];art=0
for old,new in RENAMES.items():
 m=M[new];l=L[m['layout']];om=json.loads(source(f'data/maps/{old}/map.json'));ol=oldL[om['layout']]
 assert m['name']==new
 assert (l['width']+15)*(l['height']+14)<=0x2800
 b=words((R/l['blockdata_filepath']).read_bytes());a=words(source(ol['blockdata_filepath']))
 assert len(b)==l['width']*l['height']
 for y in range(ol['height']):
  for x in range(ol['width']):
   if (x,y) not in allowed.get(new,set()):assert b[y*l['width']+x]==a[y*ol['width']+x],(new,x,y)
 art+=len(a)-sum(1 for x,y in allowed.get(new,set()) if x<ol['width'] and y<ol['height'])
 border=(R/l['border_filepath']).read_bytes();assert len(border)==l['border_width']*l['border_height']*2
 assert border==source(ol['border_filepath'])
 for kind in ['object_events','warp_events','coord_events','bg_events']:
  for i,e in enumerate(m[kind]):
   if not (0<=e['x']<l['width'] and 0<=e['y']<l['height']):events.append({'map':new,'kind':kind,'index':i,'x':e['x'],'y':e['y']})
# The map group table's order, not the symbolic spelling, owns save-game IDs.
a=json.loads(source('data/maps/map_groups.json'));b=load('data/maps/map_groups.json')
for key,value in a.items():
 expected=[RENAMES.get(v,v) for v in value] if isinstance(value,list) else value
 assert b[key]==expected,key
pos={'Havora_Market':(0,0)};q=deque(pos);opposite={'left':'right','right':'left','up':'down','down':'up'};pairs=set()
while q:
 n=q.popleft();l=L[M[n]['layout']];x,y=pos[n]
 for c in M[n]['connections'] or []:
  m=ids.get(c['map'])
  if not m:continue
  ll=L[M[m]['layout']];off=int(c['offset']);d=c['direction'];reverse=[r for r in M[m]['connections'] if r['map']==M[n]['id'] and r['direction']==opposite[d]]
  assert len(reverse)==1 and int(reverse[0]['offset'])==-off,(n,m)
  p={'left':(x-ll['width'],y+off),'right':(x+l['width'],y+off),'up':(x+off,y-ll['height']),'down':(x+off,y+l['height'])}[d]
  if m in pos:assert pos[m]==p,(n,m,pos[m],p)
  else:pos[m]=p;q.append(m)
  pairs.add(tuple(sorted([n,m])))
assert len(pos)==8 and len(pairs)==11
assert pos['Havora_DaycareExterior'][0]==pos['Havora_CoastalCliffs'][0]==pos['Havora_Market'][0]+L[M['Havora_Market']['layout']]['width']
assert pos['Havora_DaycareExterior'][1]+L[M['Havora_DaycareExterior']['layout']]['height']==0
print(json.dumps({'maps':8,'consistent_connection_pairs':len(pairs),'map_group_numbers_preserved':True,'authored_cells_preserved_outside_reviewed_house_plots':art,'original_border_files_preserved':True,'north_quadrant_added_edge_columns':1,'origins':pos,'existing_out_of_bounds_events_needing_later_review':events},indent=2))
