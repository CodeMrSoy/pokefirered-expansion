"""Compare actual tiles/elevations to the abstract graph for every reachable state."""
from collections import deque
from pathlib import Path
import importlib.util
R=Path(__file__).resolve().parents[2]
def module(name):
 spec=importlib.util.spec_from_file_location(name,R/'tools/havora'/f'{name}.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
geo=module('build_fixed_transfer_gym');model=module('solve_fixed_transfer_design')
if getattr(geo,'ARTWORK_REVIEW',False):
 print('SKIP retired puzzle geometry; use havora_artwork_assets.py and havora_artwork_review_emulator.py')
 raise SystemExit(0)
anchors=geo.ANCHORS
actors=geo.ACTORS
def flood(b,start):
 todo=deque([start]);seen={start}
 while todo:
  x,y=todo.popleft();z=b[y*geo.W+x]>>12
  for xx,yy in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
   if not(0<=xx<geo.W and 0<=yy<geo.H) or (xx,yy) in seen or (xx,yy) in actors:continue
   t=b[yy*geo.W+xx];zz=t>>12
   if t&0xc00 or (z not in (0,15) and zz not in (0,15) and z!=zz):continue
   seen.add((xx,yy));todo.append((xx,yy))
 return seen
states,_,_,_=model.search();cache={};checked=0
for state in states:
 w,p,a,b,m,r=state
 key=(w,a,b,m)
 if key not in cache:
  tiles=geo.draw(state);components=[flood(tiles,start) for start in anchors]
  cache[key]=components
 else:components=cache[key]
 # Abstract walk reachability is a connected component, not just one edge.
 reachable={p};todo=deque([p])
 while todo:
  n=todo.popleft();ss=(w,n,a,b,m,r)
  for act,nextstate in model.edges(ss):
   if act.startswith('Walk') and nextstate[1] not in reachable:reachable.add(nextstate[1]);todo.append(nextstate[1])
 assert geo.ENTRY in components[0],('entry/exit disconnected',state)
 actual={n for n,anchor in enumerate(anchors) if anchor in components[p]}
 assert actual==reachable,('walk graph mismatch',state,'expected',reachable,'actual',actual)
 for boat,node in [(0,a),(1,b)]:
  if node==p and not(boat and m) and w[node//2] in model.DOCK[node]:
   port=geo.berth(node,boat)
   assert port in components[p],('legal boat port unreachable',state,boat,port)
 checked+=1
print('PASS',checked,'states: mapped walking connections, elevations and legal boat landings match solver')
