"""Prove legal boat trips fit a 3x3 hull in the real overhead map footprint."""
from pathlib import Path
from collections import deque
import importlib.util
R=Path(__file__).resolve().parents[1]
def module(name):
 s=importlib.util.spec_from_file_location(name,R/'tools/havora'/f'{name}.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
geo=module('overhead_lock_geometry');model=module('solve_fixed_transfer_design')
cache={};checked=0
for state in model.search()[0]:
 w,p,a,c,moor,released=state
 for action,nxt in model.edges(state):
  if not action.startswith('Ride'):continue
  boat=int(action.startswith('Ride cargo'));src=(a,c)[boat];dst=nxt[1]
  key=(w,a,c,moor,boat)
  if key not in cache:
   tiles=geo.draw(state);sx=geo.SHORE[src]+2*geo.DIR[src];sy=geo.BERTH_ROW+3*boat
   def clear(x,y):
    if not(1<=x<geo.W-1 and 1<=y<geo.H-1):return False
    return all(abs(xx-sx)<=1 and abs(yy-sy)<=1 or tiles[yy*geo.W+xx]&1023==0x282 for yy in range(y-1,y+2) for xx in range(x-1,x+2))
   start=(sx,sy);seen={start};todo=deque([start])
   while todo:
    x,y=todo.popleft()
    for at in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
     if at not in seen and clear(*at):seen.add(at);todo.append(at)
   cache[key]=seen
  goal=(geo.SHORE[dst]+2*geo.DIR[dst],geo.BERTH_ROW+3*boat)
  assert goal in cache[key],('hull route blocked',state,action,goal)
  checked+=1
print('PASS',checked,'legal boat trips: whole hull clears islands, banks, other boat and gates')
# A berth is independent of the tide; no eight-row vertical teleport remains.
for n in range(6):
 for boat in range(2):assert geo.berth(n,boat)==(geo.SHORE[n],geo.BERTH_ROW+3*boat)
print('PASS fixed berths at all water levels')
