"""Guard the three annotated Section A artwork corrections across all states."""
from pathlib import Path
import sys,itertools
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools/havora'))
import overhead_lock_geometry as g
for levels in itertools.product(range(3),repeat=3):
 b=g.draw((levels,0,0,4,0,False));level=levels[0]
 if not level:continue
 assert all(b[26*80+x]==0x1682 for x in range(2,5)),'entrance threshold not flooded'
 for y in range(7,10):
  for x in range(5,10):
   expected=g.refs[0][y*80+x+level] if 7-level<=x<=9-level else 0x37cf if level==1 and x==5 else 0x1682
   assert b[y*80+x]==expected,('incomplete hull or leftover outline',levels,x,y)
 for x in range(22,26):
  assert b[13*80+x]==(g.refs[0][13*80+x] if level==1 else 0x1682),'MID cliff face or HIGH submersion incorrect'
print('PASS annotated entrance, boat outlines and MID cliff face across all 27 water states')

for a,b,c in itertools.product(range(3),repeat=3):
 tiles=g.draw(((a,b,c),0,0,4,0,False))
 assert tiles[21*80+27]==0x37b1,'gate must start at row 22'
 for y in range(22,26):
  assert tiles[y*80+27]==(0x1682 if a==2 or a==b==1 else 0x1785)
print('PASS A gate is four tall at LOW/MID and hidden at HIGH independent of B')
