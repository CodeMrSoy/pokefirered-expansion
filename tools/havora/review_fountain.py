#!/usr/bin/env python3
"""Render the exact shared-tileset fountain on grass/paving for all five frames."""
import json,struct
from PIL import Image,ImageDraw
from render import ROOT,atlas
j=json.loads((ROOT/'tools/havora/fountain.json').read_text());ids=j['animation_graphic_ids'];bank=j['palette_bank'];pals=[];tiles=[];meta=[]
for g in ['primary','secondary']:
 p=ROOT/f'data/tilesets/{g}/havora_city';im=Image.open(p/'tiles.png');tiles.extend(im.crop((i%16*8,i//16*8,i%16*8+8,i//16*8+8)) for i in range(640 if g=='primary' else 384));b=(p/'metatiles.bin').read_bytes();w=struct.unpack('<'+'H'*(len(b)//2),b);meta.extend(w[i:i+8] for i in range(0,len(w),8))
for b in range(13):
 p=ROOT/f'data/tilesets/{"primary" if b<7 else "secondary"}/havora_city/palettes/{b:02}.pal';pals.append([tuple(map(int,l.split())) for l in p.read_text().splitlines()[3:19]])
frames=[]
for f in range(5):
 anim=Image.open(ROOT/f'data/tilesets/secondary/havora_city/anim/fountain/{f}.png');active=tiles[:]
 for i,t in enumerate(ids):
  k=i+2;active[t]=anim.crop((k%2*8,k//2*8,k%2*8+8,k//2*8+8))
 canvas=Image.new('RGB',(480,350),'#24313b');d=ImageDraw.Draw(canvas)
 d.text((20,15),'HAVORA / ANIMATED CELADON FOUNTAIN',fill='white')
 for n,(label,grid) in enumerate(j['kits'].items()):
  small=Image.new('RGB',(48,64))
  for y,row in enumerate(grid):
   for x,mid in enumerate(row):
    for k,w in enumerate(meta[mid]):
     tile=active[w&1023]
     for yy in range(8):
      for xx in range(8):
       index=tile.getpixel((7-xx if w&1024 else xx,7-yy if w&2048 else yy))
       if index or k<4:small.putpixel((x*16+k%2*8+xx,y*16+(k%4//2)*8+yy),pals[w>>12][index])
  canvas.paste(small.resize((144,192),Image.Resampling.NEAREST),(30+n*240,55));d.text((30+n*240,260),label.title(),fill='white')
  for r,row in enumerate(grid):d.text((30+n*240,280+r*15),' '.join(f'{mid:03X}' for mid in row),fill='white')
 frames.append(canvas)
frames[0].save(ROOT/'docs/havora/fountain.png');frames[0].save(ROOT/'docs/havora/fountain.gif',save_all=True,append_images=frames[1:],duration=200,loop=0,disposal=2)
