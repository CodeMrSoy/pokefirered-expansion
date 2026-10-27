#!/usr/bin/env python3
"""Read-only review checks; never commit or rewrite player-authored terrain."""
import json,struct,subprocess,re
from pathlib import Path
from collections import deque
R=Path(__file__).resolve().parents[2];BASE='ac291bc1'
def js(p):return json.loads((R/p).read_text())
def source(p):return subprocess.check_output(['git','show',BASE+':'+p],cwd=R)
def ww(b):return list(struct.unpack('<'+'H'*(len(b)//2),b))
names=['Havora_Market','Havora_Harbor','Havora_River','Havora_WestQuadrant','Havora_NorthQuadrant','Havora_DaycareExterior','Havora_Lookout','Havora_CoastalCliffs'];layouts={l['id']:l for l in js('data/layouts/layouts.json')['layouts']};maps={n:js(f'data/maps/{n}/map.json') for n in names};ids={m['id']:n for n,m in maps.items()};V={n:ww((R/layouts[m['layout']]['blockdata_filepath']).read_bytes()) for n,m in maps.items()}
pos={'Havora_Market':(0,0)};q=deque(pos)
while q:
 n=q.popleft();l=layouts[maps[n]['layout']];x,y=pos[n]
 for c in maps[n]['connections'] or []:
  m=ids.get(c['map'])
  if not m:continue
  ll=layouts[maps[m]['layout']];off=int(c['offset']);p={'left':(x-ll['width'],y+off),'right':(x+l['width'],y+off),'up':(x+off,y-ll['height']),'down':(x+off,y+l['height'])}[c['direction']]
  if m in pos:assert pos[m]==p
  else:pos[m]=p;q.append(m)
coast={tuple(p) for p in js('tools/havora/market-naturalization.json')['coast_edit_cells']} if (R/'tools/havora/market-naturalization.json').exists() else set()
terrain=0;walk={};cliffs=set(range(33,77))|{166,167,168,169,170,171,642}
for n,m in maps.items():
 l=layouts[m['layout']];a=ww(source(l['blockdata_filepath']));b=V[n];assert len(a)==len(b)==l['width']*l['height']
 for i,v in enumerate(a):
  if v&1023 in cliffs:
   if not (n=='Havora_Market' and (i%l['width'],i//l['width']) in coast):assert v==b[i],(n,i);terrain+=1
 if n=='Havora_Market' and coast:assert all(v&1023==642 for v in ww((R/l['border_filepath']).read_bytes()))
 else:assert (R/l['border_filepath']).read_bytes()==source(l['border_filepath'])
 assert m['connections']==json.loads(source(f'data/maps/{n}/map.json'))['connections']
 for e in m['object_events']+m['warp_events']:assert 0<=e['x']<l['width'] and 0<=e['y']<l['height'],(n,e)
 for e in m['object_events']:assert V[n][e['y']*l['width']+e['x']]&0xc00==0,(n,'NPC on solid tile',e)
 assert len(m['object_events'])<=16,(n,'too many NPCs')
 for i,v in enumerate(b):
  if v&0xc00==0 and v&1023!=642:walk[(pos[n][0]+i%l['width'],pos[n][1]+i//l['width'])]=(n,i%l['width'],i//l['width'])
# Collision-level route check (engine elevation transitions still need emulator testing).
seen={(20,12)};q=deque(seen)
while q:
 x,y=q.popleft()
 for p in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
  if p in walk and p not in seen:seen.add(p);q.append(p)
allmaps={m['id']:m for m in (json.loads(p.read_text()) for p in (R/'data/maps').glob('*/map.json'))};unreachable=[];checked=0
for n in ['Havora_Market','Havora_WestQuadrant','Havora_NorthQuadrant','Havora_DaycareExterior']:
 m=maps[n];l=layouts[m['layout']]
 for i,e in enumerate(m['warp_events']):
  x,y=e['x'],e['y'];v=V[n][y*l['width']+x];assert v&0xc00==0,(n,'blocked door',i)
  assert any(w['dest_map']==m['id'] and int(w['dest_warp_id'])==i for w in allmaps[e['dest_map']]['warp_events']) or (n=='Havora_Market' and i==7)
  if (pos[n][0]+x,pos[n][1]+y+1) not in seen:unreachable.append([n,i,x,y])
  checked+=1
assert not subprocess.check_output(['git','diff','--name-only',BASE,'--','data/layouts/Havora_Harbor','data/maps/Havora_Harbor','data/layouts/layouts.json','src','include'],cwd=R).strip()
result={'terrain_water_cells_preserved_outside_approved_inlet':terrain,'approved_inlet_edit_cells':len(coast),'offsets_dimensions_and_harbor_map_unchanged':True,'market_border_matches_sea':bool(coast),'door_warp_references_checked':checked,'collision_route_reachable_cells':len(seen),'reachable_cells_by_district':{n:sum(1 for p in seen if walk.get(p,(None,))[0]==n) for n in names},'door_approaches_without_a_collision_route_from_market':unreachable,'all_npc_and_warp_coordinates_in_bounds':True,'emulator_tested':False,'uncommitted_review':True};print(json.dumps(result,indent=2))
