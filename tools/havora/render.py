#!/usr/bin/env python3
"""Render native General/Vermilion map blocks for review (not Porymap)."""
from pathlib import Path
import struct,json
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2]
def words(p):
 b=p.read_bytes();return struct.unpack('<'+'H'*(len(b)//2),b)
def atlas(secondary="vermilion_city"):
 paths=[ROOT/'data/tilesets'/p for p in ['primary/general','secondary/'+secondary]]
 tiles=[Image.open(p/'tiles.png') for p in paths]
 pals=[]
 for i in range(13):
  p=paths[0 if i<7 else 1]/'palettes'/f'{i:02}.pal'
  pals.append([tuple(map(int,s.split())) for s in p.read_text().splitlines()[3:19]])
 out=[]
 for group,p in enumerate(paths):
  ws=words(p/'metatiles.bin')
  for j in range(0,len(ws),8):
   im=Image.new('RGB',(16,16),pals[0][0])
   for k,w in enumerate(ws[j:j+8]):
    tid=w&1023;src=tiles[0 if tid<640 else 1];tid=tid if tid<640 else tid-640
    tx=(tid%(src.width//8))*8;ty=(tid//(src.width//8))*8
    for y in range(8):
     for x in range(8):
      idx=src.getpixel((tx+(7-x if w&1024 else x),ty+(7-y if w&2048 else y)))
      if idx or k<4:im.putpixel(((k%2)*8+x,((k%4)//2)*8+y),pals[w>>12][idx])
   out.append(im)
 return out
def render(name,out):
 l=next(x for x in json.loads((ROOT/'data/layouts/layouts.json').read_text())['layouts'] if x['id']==name)
 ims=atlas('havora_harbor' if l['secondary_tileset']=='gTileset_HavoraHarbor' else 'vermilion_city');ws=words(ROOT/l['blockdata_filepath']);im=Image.new('RGB',(l['width']*16,l['height']*16))
 for i,w in enumerate(ws):im.paste(ims[w&1023],((i%l['width'])*16,(i//l['width'])*16))
 im.save(out)
if __name__=='__main__':
 import sys
 if len(sys.argv)>2:render(sys.argv[1],sys.argv[2])
 else:
  ims=atlas();im=Image.new('RGB',(16*64,((len(ims)+15)//16)*48),'#ddd');d=ImageDraw.Draw(im)
  for i,t in enumerate(ims):
   x=i%16*64;y=i//16*48;im.paste(t.resize((32,32)),(x,y));d.text((x,y+32),f'{i:03X}',fill='black')
  im.save(ROOT/'build/havora-metatiles.png')
