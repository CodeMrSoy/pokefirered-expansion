"""Protect original tile assets and the latest Porymap-authored default."""
import subprocess,struct,itertools,sys
from pathlib import Path
from io import BytesIO
from PIL import Image
R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R/'tools/havora'));import overhead_lock_geometry as geo
BASE='e7737e147:'
def original(path):return subprocess.check_output(['git','show',BASE+path],cwd=R)
p='data/tilesets/secondary/havora_gym/metatiles.bin';old=original(p);new=(R/p).read_bytes()
assert new[:(0x3c5-640)*16]==old[:(0x3c5-640)*16],'an existing metatile changed'
p='data/tilesets/primary/havora_gym/metatiles.bin';primary=original(p)
assert (R/p).read_bytes()==primary,'primary metatiles changed'
p='data/tilesets/primary/havora_gym/tiles.png'
source=Image.open(BytesIO(original(p)));current=Image.open(R/p)
metas=primary+old;used={v&1023 for v in struct.unpack('<'+'H'*(len(metas)//2),metas)}
for n in used:
 if n<640:
  box=(n%16*8,n//16*8,n%16*8+8,n//16*8+8)
  assert source.crop(box).tobytes()==current.crop(box).tobytes(),('existing graphic changed',n)
print('PASS existing metatiles and used graphics restored byte-for-byte')
for levels in itertools.product(range(3),repeat=3):
 b=geo.draw((levels,0,0,4,0,False));assert len(b)==geo.W*geo.H and all(0<=v<65536 for v in b)
b=geo.draw(((0,0,0),0,0,4,0,False))
assert (R/'data/layouts/Havora_Gym/authored.bin').read_bytes()==subprocess.check_output(['git','show','6ab7bd9e2:data/layouts/Havora_Gym/map.bin'],cwd=R),'latest authored baseline changed'
assert all(v&1023!=0x318 for v in b),'generated bridge/gallery remains'
assert struct.pack('<'+'H'*len(b),*b)==(R/'data/layouts/Havora_Gym/map.bin').read_bytes()
print('PASS all 27 independent height combinations; all-LOW default retains latest authored layout without generated paths')
