"""The circled dam stems are the only new passable water cells."""
from pathlib import Path
import sys,itertools
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools/havora'))
import overhead_lock_geometry as g
from boat_routes import route,dam_open
for w in itertools.product(range(3),repeat=3):
 b=g.draw((w,0,0,4,0,False))
 for boundary,x in enumerate((27,54)):
  expected=w[0]==w[1] and w[0] in (1,2) if boundary==0 else w[1]==w[2]==2
  assert dam_open(w,boundary)==expected
  for y in range(22 if boundary==0 else 21,26):assert (b[y*80+x]==0x1682)==(expected or boundary==0 and w[0]==2),('wrong dam submersion',w,x,y)
  for y in range(21):assert b[y*80+x]==g.authored[y*80+x],('divider artwork changed',w,x,y)
assert not dam_open((1,2,2),0) and not dam_open((2,1,2),0)
assert route((1,1,2),(24,16),(30,16)) is not None
assert route((1,2,2),(50,8),(75,11)) is not None
assert route((1,1,2),(50,8),(75,11)) is None
assert route((0,0,0),(4,8),(75,11)) is None
scripts=(R/'data/maps/Havora_Gym/scripts.inc').read_text()
travel=scripts.split('HavoraTide_Travel::',1)[1].split('HavoraTide_Status::',1)[0]
assert 'warp ' not in travel and 'waitstate' in travel
print('PASS all 27 dam profiles; mixed levels closed; 3x3 hull crosses only submerged dams; travel script contains no warp')
