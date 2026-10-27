"""Protect latest authored layout, sectional fills and submerged access."""
from pathlib import Path
import sys,struct,subprocess,itertools
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools/havora'))
import overhead_lock_geometry as g
latest=subprocess.check_output(['git','show','4d5a43d97:data/layouts/HavoraCaptainsTrial/map.bin'],cwd=R)
latest=bytearray(latest);struct.pack_into('<H',latest,2*(21*80+27),0x37b1)
manifest=__import__('json').loads((R/'tools/havora/tidal_trial.json').read_text())
tile={'RED':0x300,'BLUE':0x301,'YELLOW':0x302,'GREEN':0x303}
for p in manifest['platforms']:
 for (x,y),color in zip(p['switches'],p['switch_colors']):
  i=2*(y*80+x);old=struct.unpack_from('<H',latest,i)[0]
  struct.pack_into('<H',latest,i,(old&~1023)|tile[color])
base=g.draw(((0,0,0),0,0,4,0,False))
assert struct.pack('<2160H',*base)==latest,'LOW layout differs from latest Porymap commit'
assert (g.W,g.H)==(80,27)
for levels in itertools.product(range(3),repeat=3):
 b=g.draw((levels,0,0,4,0,False));assert len(b)==g.W*g.H
 if levels[1]==2:
  assert all(b[y*80+x]==0x1682 for y in range(9,14) for x in range(37,44)),'floating island/controls at HIGH'
 elif levels[1]==1:
  floor=[b[y*80+x] for y in [10,11] for x in [39,40,41]]
  assert all(not t&0xc00 for t in floor) and len({t>>12 for t in floor})==1,'MID island floor/pads inaccessible'
 if levels[2]==0:
  assert b[20*80+65]&1023==0x281 and not b[20*80+65]&0xc00,'LOW captain floor inaccessible'
 elif levels[2]==1:
  roof=[b[y*80+x] for y in range(19,24) for x in range(63,70)]
  assert all(t&0x400 for t in roof) and any(t&1023!=0x282 for t in roof),'MID roof is missing or walkable'
 else:
  assert all(b[y*80+x]==0x1682 for y in range(16,24) for x in range(63,71)),'HIGH bunker/spur not submerged'
 for ch,(left,right) in enumerate(g.SECTION_COLUMNS):
  for y in range(3,g.H):
   for x in range(left,right):
    if g.authored[y*80+x]&1023 in (0x376,0x377,0x387):continue
    assert b[y*80+x]==g.refs[levels[ch]][y*80+x],('section affected by another section',levels,ch,x,y)
print('PASS 27 independent combinations; latest LOW layout; MID island access; MID bunker roof; HIGH submersion')
# Both authored mid-height landings remain connected to their existing stairs.
from collections import deque
for levels in itertools.product(range(3),repeat=3):
 b=g.draw((levels,0,0,4,0,False))
 for ch,left,top,target in [(0,23,(25,12),(24,16)),(1,28,(29,12),(30,16))]:
  if levels[ch]==2:
   assert all(b[y*80+x]==0x1682 for y in range(13,18) for x in range(left,left+4)),('submerged landing remains',levels,ch)
   continue
  todo=deque([top]);seen={top}
  while todo:
   x,y=todo.popleft();z=b[y*80+x]>>12
   for xx,yy in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
    if not(0<=xx<80 and 0<=yy<27) or (xx,yy) in seen:continue
    t=b[yy*80+xx];zz=t>>12
    if t&0xc00 or z not in (0,15) and zz not in (0,15) and z!=zz:continue
    seen.add((xx,yy));todo.append((xx,yy))
  assert target in seen,('landing disconnected from authored stair',levels,ch)
  assert b[target[1]*80+target[0]]>>12==4
print('PASS both mid-height platforms: LOW/MID stair-to-pad access, HIGH submersion, independent section levels')
