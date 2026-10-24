#!/usr/bin/env python3
"""Render the imported native house kits and their hexadecimal Porymap grids."""
import json
from PIL import Image,ImageDraw
from render import ROOT,atlas
kits=json.loads((ROOT/'tools/havora/native-houses.json').read_text())['kits']
tiles=atlas('havora_city','havora_city')
im=Image.new('RGB',(800,460),'#24313b');d=ImageDraw.Draw(im)
for n,(name,grid) in enumerate(kits.items()):
 ox=24+n*380;oy=48;d.text((ox,16),name.replace('_',' ').title(),fill='white')
 for y,row in enumerate(grid):
  for x,mid in enumerate(row):im.paste(tiles[mid].resize((48,48),Image.Resampling.NEAREST),(ox+x*48,oy+y*48))
 for y,row in enumerate(grid):d.text((ox,310+y*20),'  '.join(f'{mid:03X}' for mid in row),fill='white')
d.text((24,430),'Original FireRed designs / Havora shared palette. Maps unchanged.',fill='white')
im.save(ROOT/'docs/havora/native-houses.png')
