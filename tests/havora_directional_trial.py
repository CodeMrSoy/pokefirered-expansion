"""Solve directional color trial; verify every outbound station needs battle and switch."""
from pathlib import Path
from collections import deque
import json,struct,sys
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools/havora'))
from tidal_color_rules import apply_switch
import overhead_lock_geometry as g
from boat_routes import route,water_map,dam_open
j=json.loads((R/'tools/havora/tidal_trial.json').read_text());P=j['platforms'];L=j['links'];colors={0x300:'red',0x301:'blue',0x302:'yellow',0x303:'green'}
start=((0,0,0),0,0,0);q=deque([start]);prev={start:None};actions={}
def add(s,t,a):
 if t not in prev:prev[t]=s;actions[t]=a;q.append(t)
while q:
 s=q.popleft();w,n,v,b=s;p=P[n]
 if v==251 and b==127 and w[2]==0 and n in (4,5):break
 if not v&p['victory']:add(s,(w,n,v|p['victory'],b),['battle',n])
 if v&p['victory']:
  for k,(x,y) in enumerate(p['switches']):
   color=colors[g.authored[y*80+x]&1023];nw=apply_switch(w,color)
   if n==6 and nw[1]==2:continue
   add(s,(nw,n,v,b|1<<n),['switch',n,k,color])
 for i,l in enumerate(L):
  if n!=l['from'] or v&l['clearance']!=l['clearance'] or not b&1<<n:continue
  if any(a>=0 and a!=z for a,z in zip(l['water'],w)):continue
  tiles=water_map(w)
  if route(w,l['pad_from'],l['pad_to']) is None:continue
  if any(tiles[y*80+x]&0xc00 for x,y in [l['pad_from'],l['pad_to']]):continue
  add(s,(w,l['to'],v,b),['travel',i])
 if n in (4,5) and w[2]==0:add(s,(w,9-n,v,b),['walk',9-n])
else:raise AssertionError('no complete solution')
plan=[]
while prev[s] is not None:plan.append([actions[s],s]);s=prev[s]
plan.reverse();out=R/'build/havora-tests/directional-solution.json';out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(plan,indent=2)+'\n')
for a,s in plan:print(a,s[0])
assert all(any(a[0]=='battle' and a[1]==n for a,s in plan) for n in range(7))
assert all(any(a[0]=='switch' and a[1]==n for a,s in plan) for n in range(7))
for l in L:
 assert l['clearance']&P[l['from']]['victory']
assert any(l['source_label']=='AL1' and l['destination_label']=='AR2' for l in L)
assert any(l['source_label']=='AR3' and l['destination_label']=='BL3' for l in L)
m=json.loads((R/'data/maps/Havora_Gym/map.json').read_text())
for p in P:
 o=next(o for o in m['object_events'] if o['script']=='HavoraTrial_'+p['trainer'])
 assert o['trainer_type']=='TRAINER_TYPE_NORMAL' and o['movement_type'] in ['MOVEMENT_TYPE_FACE_LEFT','MOVEMENT_TYPE_FACE_RIGHT']
scripts=(R/'data/maps/Havora_Gym/scripts.inc').read_text()
for p in P:assert scripts.split('HavoraTrial_'+p['trainer']+'::\n',1)[1].lstrip().startswith('trainerbattle_double')
print('PASS complete directional solution:',len(plan),'actions;',len(prev),'reachable states; all seven battles/switch stations required; sight scripts parse correctly')
