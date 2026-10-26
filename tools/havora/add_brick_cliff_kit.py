"""Extend the existing private brick tiles with native 16px cliff contours.
Uses the gym's existing palette and graphic allocator; no other tilesets change.
"""
from pathlib import Path
import struct
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[2]
P=R/'data/tilesets/primary/havora_gym';S=R/'data/tilesets/secondary/havora_gym'
def words(p,fmt='H'):
 b=p.read_bytes();return list(struct.unpack('<'+fmt*(len(b)//struct.calcsize(fmt)),b))
m=words(P/'metatiles.bin')+words(S/'metatiles.bin');attrs=words(S/'metatile_attributes.bin','I')
im=Image.open(P/'tiles.png');used={w&1023 for w in m};free=iter(i for i in range(128,640) if i not in used)
# Idempotent: graphics already assigned to the kit can be reused on the next run.
kit=set(range(0x3c5,0x3d3));other={w&1023 for n in range(len(m)//8) if n not in kit for w in m[n*8:n*8+8]}
free=iter(i for i in range(128,640) if i not in other);packed={}
def graphic(t):
 key=t.tobytes()
 if key not in packed:
  idx=next(free);packed[key]=idx;im.paste(t,(idx%16*8,idx//16*8))
 return packed[key]
def store(mid,t):
 overlay=[graphic(t.crop((x,y,x+8,y+8)))|0x2000 for y in [0,8] for x in [0,8]]
 m[mid*8:(mid+1)*8]=m[0x282*8:0x282*8+4]+overlay;attrs[mid-640]=0x20000000
# Straight sides, convex caps/feet and concave returns are directional variants
# of one brick fabric. The light upper lip and dark lower rim imply depth.
for mid,side,kind in [(0x3c5,'L','side'),(0x3c6,'R','side'),(0x3c7,'L','top'),(0x3c8,'R','top'),(0x3c9,'L','foot'),(0x3ca,'R','foot'),(0x3cb,'L','inner'),(0x3cc,'R','inner'),(0x3cd,'C','front'),(0x3ce,'L','front'),(0x3cf,'R','front'),(0x3d0,'C','cap'),(0x3d1,'L','return'),(0x3d2,'R','return')]:
 t=Image.new('P',(16,16),0);d=ImageDraw.Draw(t)
 if side=='C':mask=[(0,0),(15,0),(15,15),(0,15)]
 elif kind in ['foot','front']:
  mask=[(2,0),(15,0),(15,15),(6,15),(2,12),(1,9)]
 elif kind=='top':mask=[(6,0),(15,0),(15,15),(2,15),(2,4)]
 else:mask=[(2,0),(15,0),(15,15),(2,15)]
 d.polygon(mask,fill=5)
 if side=='C':
  d.rectangle((0,0,15,2),fill=6);d.line((0,3,15,3),fill=3)
  d.line((0,15,15,15),fill=3)
 else:
  d.line((2,0,2,11 if kind in ['foot','front'] else 15),fill=6)
  d.line((3,0,3,11 if kind in ['foot','front'] else 15),fill=5)
 # Subtle mortar keeps long courses coherent; dark courses model the side plane.
 for y in [6,14]:d.line((4,y,15,y),fill=3)
 for x,y in [(9,0),(5,7)]:d.line((x,y,x,y+5),fill=3)
 if kind in ['foot','front']:
  d.line((3,12,6,15),fill=3);d.line((6,15,15,15),fill=3)
 if kind in ['top','cap']:d.line((6 if side!='C' else 0,0,15,0),fill=6)
 if kind in ['inner','return']:
  d.rectangle((0,0,6,4),fill=6);d.line((0,5,5,5),fill=3)
 if side=='R':t=t.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
 store(mid,t)
im.save(P/'tiles.png',bits=4)
(S/'metatiles.bin').write_bytes(struct.pack('<'+'H'*(len(m)-640*8),*m[640*8:]))
(S/'metatile_attributes.bin').write_bytes(struct.pack('<'+'I'*len(attrs),*attrs))
print('Added 14 brick cliff pieces at 0x3C5–0x3D2 using',len(packed),'8px graphics')
