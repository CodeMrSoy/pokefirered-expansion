#!/usr/bin/env python3
"""Render actual engine animation PNGs over the packed map for visual QA/export."""
from pathlib import Path
import json,struct
from PIL import Image
R=Path(__file__).resolve().parents[2]
P=R/'data/tilesets/primary/general';S=R/'data/tilesets/secondary/corvala'
def words(p):
 b=p.read_bytes();return struct.unpack('<'+'H'*(len(b)//2),b)
def palettes():
 result=[]
 for bank in range(13):
  path=(P if bank<7 else S)/'palettes'/f'{bank:02}.pal'
  result.append([tuple(map(int,row.split())) for row in path.read_text().splitlines()[3:19]])
 return result

def render():
 m=json.loads((R/'tools/corvala/map.json').read_text());w,h=m['dimensions'];blocks=words(R/'data/layouts/Corvala_Town/map.bin')
 definitions=words(P/'metatiles.bin')+words(S/'metatiles.bin');pals=palettes();secondary=Image.open(S/'tiles.png')
 frames=[];shore_positions=[i for i,v in enumerate(blocks) if v&1023 in m['shoreline']['generated_metatiles']]
 assert shore_positions,'No animated shoreline on map'
 shore_hashes=set()
 for frame in range(16):
  primary=Image.open(P/'tiles.png').copy()
  for folder,start,count,index in [('sandwatersedge',464,18,frame%8),('water_current_landwatersedge',416,48,(frame//2)%8)]:
   incoming=Image.open(P/'anim'/folder/f'{index}.png')
   for i in range(count):
    patch=incoming.crop((i%2*8,i//2*8,i%2*8+8,i//2*8+8));tid=start+i
    primary.paste(patch,(tid%16*8,tid//16*8))
  cache={};out=Image.new('RGB',(w*16,h*16))
  for i,block in enumerate(blocks):
   mid=block&1023
   if mid not in cache:
    tile=Image.new('RGB',(16,16))
    for k,v in enumerate(definitions[mid*8:mid*8+8]):
     tid=v&1023;sheet=primary if tid<640 else secondary;tid=tid if tid<640 else tid-640
     patch=sheet.crop((tid%16*8,tid//16*8,tid%16*8+8,tid//16*8+8))
     if v&1024:patch=patch.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
     if v&2048:patch=patch.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
     for y in range(8):
      for x in range(8):
       index=patch.getpixel((x,y))
       if index or k<4:tile.putpixel((k%2*8+x,k%4//2*8+y),pals[v>>12][index])
    cache[mid]=tile
   out.paste(cache[mid],(i%w*16,i//w*16))
  shore_hashes.add(b''.join(cache[blocks[i]&1023].tobytes() for i in shore_positions))
  frames.append(out)
 assert len(shore_hashes)==8,('Native shoreline frames do not animate',len(shore_hashes))
 palette=Image.new('P',(1,1));colors=[c for bank in pals for rgb in bank for c in rgb];palette.putpalette(colors+[0]*(768-len(colors)))
 frames=[f.quantize(palette=palette,dither=Image.Dither.NONE) for f in frames]
 path=R/'build/corvala/Corvala_Animated_Shoreline.gif'
 frames[0].save(path,save_all=True,append_images=frames[1:],loop=0,duration=[130,140,130]*5+[130],optimize=True,disposal=1)
 print(f'PASS: {len(shore_positions)} shoreline cells; eight distinct native surf frames; {path.name}')
 return path
if __name__=='__main__':render()
