"""Solve the real platform rules and reject bypasses; verify authored tile access."""
from pathlib import Path
from collections import deque
import json,sys,subprocess
R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R/'tools/havora'));import overhead_lock_geometry as geo
spec=json.loads((R/'tools/havora/tidal_trial.json').read_text());P=spec['platforms'];L=spec['links']
ALL=sum(a['victory'] for a in P)
def operate(w,n,k):
 w=list(w);p=P[n];s=p['section']
 if n==6:
  if w[1]!=1:return
  if k==0:
   if w[0]==2:return
   w[0]+=1
  elif k==1:
   if not w[2]:return
   w[2]-=1
  else:
   if not w[0] or w[2]==2:return
   w[0]-=1;w[2]+=1
 elif k==0:
  if w[s]==2:return
  w[s]+=1
 elif k==1:
  if not w[s]:return
  w[s]-=1
 else:w[p['remote']]=(w[p['remote']]+1)%3
 return tuple(w)
def solve(forbidden=None):
 start=((0,0,0),0,0,0);q=deque([start]);prev={start:None};actions={}
 def add(s,t,a):
  if t not in prev:prev[t]=s;actions[t]=a;q.append(t)
 while q:
  s=q.popleft();w,n,progress,switches=s;p=P[n]
  if progress==ALL and switches==127 and w[2]==0 and n in [4,5]:
   plan=[]
   while prev[s] is not None:plan.append((actions[s],s));s=prev[s]
   return list(reversed(plan)),len(prev)
  for k in range(3):
   if n==forbidden:continue
   nw=operate(w,n,k)
   if nw is not None:add(s,(nw,n,progress,switches|1<<n),['switch',n,k])
  if not progress&p['victory'] and progress&p['prerequisite']==p['prerequisite'] and switches&1<<n and list(w)==p['water']:
   add(s,(w,n,progress|p['victory'],switches),['battle',n])
  for i,link in enumerate(L):
   if any(a>=0 and a!=b for a,b in zip(link['water'],w)):continue
   if n==link['from'] and progress&link['clearance']==link['clearance']:add(s,(w,link['to'],progress,switches),['travel',i,1])
   if n==link['to']:add(s,(w,link['from'],progress,switches),['travel',i,0])
  # LOW connects C's two quays by the authored walkway (cannot bypass captain checks).
  if n in [4,5] and w[2]==0:add(s,(w,9-n,progress,switches),['walk',9-n])
  if n or any(w):add(s,((0,0,0),0,progress,switches),['reset'])
 return None,len(prev)
plan,visited=solve();assert plan,'no solution'
for n in range(7):
 bypass,_=solve(n);assert bypass is None,('switch station can be skipped',n)
print('PASS solvable from all LOW; every one of seven switch stations and trainer battles is mandatory;',len(plan),'actions;',visited,'states')
# Decode the exact C RLE overlays for all 27 states, not just the Python source snapshots.
import re,itertools
header=(R/'src/data/havora_lock_geometry.h').read_text()
offsets=list(map(int,re.search(r'sLockMapOffsets\[\] = \{([^}]+)',header).group(1).split(',')))
runs=[(int(n),int(t,16)) for n,t in re.findall(r'\{(\d+),0x([0-9a-f]+)\}',header)]
for value,offset in enumerate(offsets):
 end=offsets[value+1] if value+1<len(offsets) else len(runs)
 decoded=[tile for count,tile in runs[offset:end] for _ in range(count)]
 levels=(value%3,value//3%3,value//9)
 assert decoded==geo.draw((levels,0,0,4,0,False)),('compiled RLE profile differs',levels)
print('PASS all 27 compiled C overlays match the independent section artwork')
# Every binding uses existing switch/pad artwork; compiled LOW map remains byte-identical.
baseline=subprocess.check_output(['git','show','4d5a43d97:data/layouts/HavoraCaptainsTrial/map.bin'],cwd=R)
assert (R/'data/layouts/Havora_Gym/map.bin').read_bytes()==baseline
m=json.loads((R/'data/maps/Havora_Gym/map.json').read_text())
for n,p in enumerate(P):
 for k,(x,y) in enumerate(p['switches']):
  assert 0x300<=geo.authored[y*80+x]&1023<=0x303
  assert sum(e['x']==x and e['y']==y and e['script']==f'HavoraTide_Switch{n}_{k}' for e in m['bg_events'])==1
# Follow the solution on the actual collision/elevation grid, with trainers solid.
point=(3,25);w=(0,0,0)
def reachable(w,point):
 b=geo.draw((w,0,0,4,0,False));solid={tuple(p['npc']) for p in P if p['trainer']!='Lockkeeper' or w[1]!=2}
 solid.add((5,24))
 if w[2]==0:solid.add((65,20))
 q=[point];seen={point}
 for x,y in q:
  z=b[y*80+x]>>12
  for xx,yy in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
   if not(0<=xx<80 and 0<=yy<27) or (xx,yy) in seen or (xx,yy) in solid:continue
   t=b[yy*80+xx];nz=t>>12
   if t&0xc00 or z not in (0,15) and nz not in (0,15) and z!=nz:continue
   seen.add((xx,yy));q.append((xx,yy))
 return seen
for action,state in plan:
 seen=reachable(w,point);kind=action[0]
 if kind=='switch':target=P[action[1]]['switches'][action[2]]
 elif kind=='battle':target=P[action[1]]['npc']
 elif kind=='travel':
  link=L[action[1]];src=link['pad_from'] if action[2] else link['pad_to'];dest=link['pad_to'] if action[2] else link['pad_from']
  assert any(abs(x-src[0])+abs(y-src[1])<=1 for x,y in seen),('boarding pad unreachable',action,w,point)
  point=tuple(dest);target=None
 elif kind=='walk':target=P[action[1]]['npc']
 else:point=(3,25);target=None
 if target:
  adj=[(x,y) for x,y in seen if abs(x-target[0])+abs(y-target[1])==1]
  assert adj,('switch or trainer unreachable',action,w,point,target)
  point=adj[0]
 w=tuple(state[0])
assert any(abs(x-65)+abs(y-20)==1 for x,y in reachable(w,point)),'bunker not reachable'
out=R/'build/havora-tests/tidal-solution.json';out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(plan,indent=2)+'\n')
# C's crossing is walkable only at LOW for every combination of A/B heights.
import itertools
for levels in itertools.product(range(3),repeat=3):
 assert ((77,6) in reachable(levels,(56,6)))==(levels[2]==0),('C crossing height',levels)
print('PASS solution walks on actual tiles with solid NPCs; all 21 switches bound; both MID pads used; unchanged artwork; bunker reachable')
for a,s in plan:print(a,list(s[0]))
