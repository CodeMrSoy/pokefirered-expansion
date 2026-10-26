"""Protect latest authored layout, sectional fills and submerged access."""
from pathlib import Path
import sys,struct,subprocess,itertools
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools/havora'))
import overhead_lock_geometry as g
latest=subprocess.check_output(['git','show','6ab7bd9e2:data/layouts/Havora_Gym/map.bin'],cwd=R)
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
old=subprocess.check_output(['git','show','6ab7bd9e2:src/havora_gym.c'],cwd=R).decode()
new=(R/'src/havora_gym.c').read_text()
assert old[old.index('void HavoraGym_Control(void)'):]==new[new.index('void HavoraGym_Control(void)'):],'puzzle control logic changed'
print('PASS puzzle control logic unchanged')
