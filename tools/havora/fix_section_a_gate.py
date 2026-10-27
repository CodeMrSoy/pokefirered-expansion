"""Apply the second annotated A correction: four-tile gate and intact MID side face."""
from pathlib import Path
import struct
R=Path(__file__).resolve().parents[2];d=R/'data/layouts/Havora_Gym'
def read(p):return list(struct.unpack('<2160H',p.read_bytes()))
def write(p,b):p.write_bytes(struct.pack('<2160H',*b))
# Shorten the gate from five tiles to four by completing its wall above it.
a=read(d/'authored.bin');a[21*80+27]=a[21*80+26];write(d/'authored.bin',a)
for name in ['low','mid','high']:
 p=d/'reference_states'/f'all-{name}.bin';b=read(p);b[21*80+27]=a[21*80+27]
 if name=='mid':
  for y in range(7,10):b[y*80+5]=b[6*80+5]
 write(p,b)
print('A gate is four tiles (rows 22–25); MID left-quay cliff face restored')
