#!/usr/bin/env python3
"""Render selected Havora housing and the optional department-store kit."""
import json
from PIL import Image,ImageDraw
from render import ROOT,atlas
kits=json.loads((ROOT/'tools/havora/green-houses.json').read_text())['kits']
kits={'cerulean_home':json.loads((ROOT/'tools/havora/native-houses.json').read_text())['kits']['cerulean_home'],**kits}
tiles=atlas('havora_city','havora_city')
im=Image.new('RGB',(960,800),'#24313b');d=ImageDraw.Draw(im)
positions={'viridian_garden':(24,58),'viridian_home':(304,58),'cerulean_home':(584,58),'celadon_department_store':(24,360)}
for name,grid in kits.items():
 x0,y0=positions[name];scale=3 if name!='celadon_department_store' else 2
 d.text((x0,y0-25),name.replace('_',' ').title(),fill='white')
 for y,row in enumerate(grid):
  for x,mid in enumerate(row):im.paste(tiles[mid].resize((16*scale,16*scale),Image.Resampling.NEAREST),(x0+x*16*scale,y0+y*16*scale))
d.text((355,375),'Shared Havora tileset',fill='white')
d.text((355,400),'Original blue harbor houses retained.',fill='white')
d.text((355,425),'FireRed building designs fitted to the shared palette.',fill='white')
d.text((355,450),'Department store: tileset kit; not placed in the city.',fill='white')
d.text((24,760),'Native map-data render. Not an emulator or Porymap screenshot.',fill='white')
im.save(ROOT/'docs/havora/green-houses.png')
