#!/usr/bin/env python3
"""Plain colored pressure buttons and matching log tips, using existing palettes.
Keeps all terrain, puzzle coordinates and solution rules intact. No water slots.
"""
import json, struct
from pathlib import Path
from PIL import Image, ImageDraw
R=Path(__file__).resolve().parents[2]
p=R/'data/tilesets/primary/havora_city/metatiles.bin'
M=list(struct.unpack('<'+'H'*(p.stat().st_size//2),p.read_bytes()))
ap=p.with_name('metatile_attributes.bin');A=list(struct.unpack('<'+'I'*(ap.stat().st_size//4),ap.read_bytes()))
pals=[];ims=[]
for group in ['primary','secondary']:ims.append(Image.open(R/f'data/tilesets/{group}/havora_city/tiles.png'))
for i in range(13):
 group='primary' if i<7 else 'secondary'
 pals.append([tuple(map(int,l.split())) for l in (R/f'data/tilesets/{group}/havora_city/palettes/{i:02}.pal').read_text().splitlines()[3:19]])
palette=pals[12]
def source(w):
 i=w&1023;im=ims[int(i>=640)];i=i if i<640 else i-640
 t=im.crop((i%16*8,i//16*8,i%16*8+8,i//16*8+8))
 if w&1024:t=t.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
 if w&2048:t=t.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
 return t
# Only one additional blank graphic is needed; never touch ocean DMA 896..1015.
slot=1023
used={w&1023 for g in ['primary','secondary'] for w in struct.unpack('<'+'H'*((R/f'data/tilesets/{g}/havora_city/metatiles.bin').stat().st_size//2),(R/f'data/tilesets/{g}/havora_city/metatiles.bin').read_bytes())}
assert slot not in used or M[0x23b*8+4]&1023==slot
if slot not in used:assert not any(source(slot).tobytes())
def put(slot,t):ims[1].paste(t,((slot-640)%16*8,(slot-640)//16*8))
colors=[7,6,13,4] # A red, B blue, C yellow, D green
plates=[[0x233,0x234],[0x235,0x236],[0x237,0x238],[0x23c,0x23d]]
for i,(color,mids) in enumerate(zip(colors,plates)):
 # Mirrored quarter-circle: colored face with a dark rim, no added symbols.
 t=Image.new('P',(8,8));d=ImageDraw.Draw(t)
 d.ellipse((1,1,14,14),fill=15);d.ellipse((2,2,13,13),fill=color)
 d.arc((3,3,12,12),190,265,fill=14,width=1)
 put(1017+i,t)
 for mid in mids:
  M[mid*8:(mid+1)*8]=M[:4]+[(1017+i)|0xc000,(1017+i)|0xc400,(1017+i)|0xc800,(1017+i)|0xcc00]
  # Both halves below actors: a boulder covers the button, never vice versa.
  A[mid]=(A[0x22f]&~0x60000000)|0x20000000
# Restore unmarked native wood and tint the upper posts. Final lock requires B/C/D.
base=source(M[0x231*8+4]);nearest=lambda c:min(range(1,16),key=lambda j:sum((c[k]-palette[j][k])**2 for k in range(3)))
combined=Image.new('P',(16,240))
raw=Image.open(R/'graphics/havora/gate.png')
for i in range(3):
 t=Image.new('P',(8,8))
 for y in range(8):
  for x in range(8):
   v=base.getpixel((x,y))
   if v:
    c=colors[i] if i<2 else [6,13,4][min(2,y//3)]
    t.putpixel((x,y),15 if x in (1,6) else (14 if x==2 else c))
 put(1021+i,t)
 mid=0x239+i;M[mid*8:(mid+1)*8]=M[0x231*8:(0x232)*8];M[mid*8+4:mid*8+6]=[0xc000|1021+i,0xc400|1021+i]
 A[mid]=A[0x231]
 out=Image.new('P',(16,80))
 for y in range(80):
  for x in range(16):
   v=raw.getpixel((x,y));out.putpixel((x,y),nearest(pals[1][v]) if v else 0)
 top=Image.new('P',(16,8));top.paste(t,(0,0));top.paste(t.transpose(Image.Transpose.FLIP_LEFT_RIGHT),(8,0))
 for frame,shift in enumerate([0,4,8,10,None]):
  if shift is not None:out.paste(top.crop((0,0,16,min(8,16-shift))),(0,frame*16+shift))
 combined.paste(out,(0,i*80))
# Resting caps are ground decoration, below the player and all boulders.
A[0x232]=(A[0x232]&~0x60000000)|0x20000000
combined.putpalette(sum((list(c) for c in palette),[])+[0]*720)
combined.save(R/'graphics/havora/gate_marked.png',bits=4)
p.write_bytes(struct.pack('<'+'H'*len(M),*M));ap.write_bytes(struct.pack('<'+'I'*len(A),*A))
ims[1].save(R/'data/tilesets/secondary/havora_city/tiles.png',bits=4)
l=next(x for x in json.loads((R/'data/layouts/layouts.json').read_text())['layouts'] if x['id']=='LAYOUT_HAVORA_NORTH_QUADRANT')
p=R/l['blockdata_filepath'];b=list(struct.unpack('<'+'H'*(p.stat().st_size//2),p.read_bytes()));k=14*l['width']+18;b[k]=(b[k]&~1023)|0x23c;p.write_bytes(struct.pack('<'+'H'*len(b),*b))
(R/'tools/havora/puzzle-markers.json').write_text(json.dumps({'plates':plates,'gates':[0x239,0x23a,0x23b],'graphic_ids':list(range(1017,1024)),'palette':12,'colors':['red','blue','yellow','green'],'ground_caps':0x232},indent=2)+'\n')
