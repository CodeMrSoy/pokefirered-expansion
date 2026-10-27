"""Physical boat routing across the user's two submerged dams."""
from collections import deque
import overhead_lock_geometry as g

def dam_open(levels,boundary):
 return levels[0]==levels[1] and levels[0] in (1,2) if boundary==0 else levels[1]==levels[2]==2

def water_map(levels):
 b=g.draw((levels,0,0,4,0,False))
 for boundary,x in enumerate((27,54)):
  if dam_open(levels,boundary):
   for y in range(22 if x==27 else 21,26):b[y*g.W+x]=0x1682
 return b

def route(levels,source,destination):
 b=water_map(levels)
 def launch(p):
  x,y=p;direction=1 if b[y*g.W+x]&1023==0x370 else -1
  return x+4*direction,y
 start=launch(source);goal=launch(destination)
 def clear(x,y):
  if any(xx==27 and not dam_open(levels,0) or xx==54 and not dam_open(levels,1) for xx in range(x-1,x+2)):return False
  return 1<=x<g.W-1 and 1<=y<g.H-1 and all((b[yy*g.W+xx]&1023==0x282 or 0x2bc<=b[yy*g.W+xx]&1023<=0x2c4 or 0x390<=b[yy*g.W+xx]&1023<=0x398) for yy in range(y-1,y+2) for xx in range(x-1,x+2))
 q=deque([start]);prev={start:None}
 while q:
  x,y=q.popleft()
  if (x,y)==goal:
   path=[];p=goal
   while p is not None:path.append(p);p=prev[p]
   return list(reversed(path))
  for p in [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]:
   if p not in prev and clear(*p):prev[p]=(x,y);q.append(p)
 return None
