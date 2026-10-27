"""Apply the user's annotated Section A flood/artwork corrections."""
from pathlib import Path
import struct
R=Path(__file__).resolve().parents[2];folder=R/'data/layouts/Havora_Gym/reference_states'
def read(name):return list(struct.unpack('<2160H',(folder/f'all-{name}.bin').read_bytes()))
low=read('low')
for level,name in [(1,'mid'),(2,'high')]:
 b=read(name)
 # The threshold belongs to the flooded entrance at both raised levels.
 for x in range(2,5):b[26*80+x]=0x1682
 # Move the complete original hull, clearing the whole old/new union first.
 for y in range(7,10):
  for x in range(5,10):b[y*80+x]=0x1682
 for dy in range(3):
  for dx in range(3):b[(7+dy)*80+7-level+dx]=low[(7+dy)*80+7+dx]
 if level==1:
  for y in range(7,10):b[y*80+5]=0x37cf
  # The upper terrace's front fascia stays exposed above the MID landing.
  for x in range(22,26):b[13*80+x]=low[13*80+x]
 (folder/f'all-{name}.bin').write_bytes(struct.pack('<2160H',*b))
print('Fixed raised entrance, complete boat hulls, and MID terrace fascia; LOW unchanged')
