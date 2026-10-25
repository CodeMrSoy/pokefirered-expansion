#!/usr/bin/env python3
"""Add color/symbol identities using six unused, non-animated graphic slots.
Never remaps existing art, palettes, cliffs or object coordinates.
"""
from pathlib import Path
import struct,json
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[2]
if (R/'tools/havora/puzzle-markers.json').exists():
 print('Puzzle marker kit already installed; edit in Porymap.');raise SystemExit(0)
p=R/'data/tilesets/primary/havora_city/metatiles.bin'
M=list(struct.unpack('<'+'H'*(len(p.read_bytes())//2),p.read_bytes()))
ap=R/'data/tilesets/primary/havora_city/metatile_attributes.bin';A=list(struct.unpack('<'+'I'*(len(ap.read_bytes())//4),ap.read_bytes()))
ims=[Image.open(R/f'data/tilesets/{g}/havora_city/tiles.png') for g in ('primary','secondary')]
pals=[]
for i in range(13):
 g='primary' if i<7 else 'secondary'
 pals.append([tuple(map(int,l.split())) for l in (R/f'data/tilesets/{g}/havora_city/palettes/{i:02}.pal').read_text().splitlines()[3:19]])
def tile(w):
 i=w&1023;im=ims[i>=640];i=i if i<640 else i-640
 t=im.crop((i%16*8,i//16*8,i%16*8+8,i//16*8+8))
 if w&1024:t=t.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
 if w&2048:t=t.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
 return t
palette=pals[12]
def nearest(c):return min(range(1,16),key=lambda j:sum((c[k]-palette[j][k])**2 for k in range(3)))
def paint(source,kind,color):
 t=tile(source);out=Image.new('P',(8,8))
 for y in range(8):
  for x in range(8):
   v=t.getpixel((x,y));out.putpixel((x,y),nearest(pals[source>>12][v]) if v else 0)
 d=ImageDraw.Draw(out)
 if kind=='circle':d.ellipse((2,2,5,5),fill=color,outline=15)
 elif kind=='diamond':d.polygon([(3,1),(6,4),(3,6),(1,4)],fill=color,outline=15)
 elif kind=='triangle':d.polygon([(3,1),(6,6),(1,6)],fill=color,outline=15)
 else:
  d.rectangle((1,2,3,5),fill=6);d.rectangle((4,2,6,5),fill=13)
 return out
slots=list(range(1017,1023));assert all(not any(w&1023==i for w in M) for i in slots),'Graphic already referenced'
new=0x233;result={'plates':[],'gates':[],'graphic_ids':slots,'palette':12}
def add(base,graphic):
 global new
 mid=new;new+=1
 assert M[mid*8:(mid+1)*8]==[0]*8 and A[mid]==0
 m=M[base*8:(base+1)*8].copy();m[4]=graphic|0xc000;m[5]=graphic|0xc400
 M[mid*8:(mid+1)*8]=m;A[mid]=A[base];return mid
for i,(kind,c) in enumerate([('circle',7),('diamond',6),('triangle',13)]):
 slot=slots[i];im=paint(M[0x22f*8+4],kind,c);ims[1].paste(im,((slot-640)%16*8,(slot-640)//16*8))
 result['plates'].append([add(0x22f,slot),add(0x230,slot)])
combined=Image.new('P',(16,240))
for i,(kind,c) in enumerate([('circle',7),('diamond',6),('combination',13)]):
 slot=slots[3+i];im=paint(M[0x231*8+4],kind,c);ims[1].paste(im,((slot-640)%16*8,(slot-640)//16*8))
 result['gates'].append(add(0x231,slot))
 # Full animation is recolored into existing palette 12; the colored identity
 # sinks with its logs. The last frame still shows their caps flush in grass.
 sheet=Image.open(R/'graphics/havora/gate.png');out=Image.new('P',sheet.size)
 for y in range(sheet.height):
  for x in range(sheet.width):
   v=sheet.getpixel((x,y));out.putpixel((x,y),nearest(pals[1][v]) if v else 0)
 for f,shift in enumerate([0,4,8,10,None]):
  if shift is not None:
   top=Image.new('P',(16,8));top.paste(im,(0,0));top.paste(im.transpose(Image.Transpose.FLIP_LEFT_RIGHT),(8,0))
   h=min(8,16-shift);out.paste(top.crop((0,0,16,h)),(0,f*16+shift))
 out.putpalette(sum((list(c) for c in palette),[])+[0]*720)
 combined.paste(out,(0,i*80))
combined.putpalette(sum((list(c) for c in palette),[])+[0]*720)
combined.save(R/'graphics/havora/gate_marked.png',bits=4)
p.write_bytes(struct.pack('<'+'H'*len(M),*M));ap.write_bytes(struct.pack('<'+'I'*len(A),*A));ims[1].save(R/'data/tilesets/secondary/havora_city/tiles.png',bits=4)
# Paint identities at only the existing 7 interactive coordinates.
l=json.loads((R/'data/layouts/layouts.json').read_text())['layouts'];l=next(v for v in l if v['id']=='LAYOUT_HAVORA_NORTH_QUADRANT');p=R/l['blockdata_filepath'];b=list(struct.unpack('<'+'H'*(len(p.read_bytes())//2),p.read_bytes()))
for i,(x,y) in enumerate([(16,22),(21,21),(13,27),(18,14)]):
 k=y*l['width']+x;b[k]=(b[k]&~1023)|result['plates'][min(i,2)][0]
for i,(x,y) in enumerate([(19,22),(16,21),(10,13)]):
 k=y*l['width']+x;b[k]=(b[k]&~1023)|result['gates'][i]
p.write_bytes(struct.pack('<'+'H'*len(b),*b))
(R/'tools/havora/puzzle-markers.json').write_text(json.dumps(result,indent=2)+'\n')
