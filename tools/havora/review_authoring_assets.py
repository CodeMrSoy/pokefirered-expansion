#!/usr/bin/env python3
"""Render the current Porymap authoring pieces and their hexadecimal IDs."""
import json
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from render import atlas
R=Path(__file__).resolve().parents[2]
report=json.loads((R/'tools/havora/authoring-assets.json').read_text())
shared=json.loads((R/'tools/havora/shared-tileset.json').read_text())
old=json.loads((R/'tools/havora/assets.json').read_text())
mp={int(k):v for k,v in shared['metatile_mapping']['harbor'].items()}
tiles=atlas('havora_city','havora_city')
market=[e for e in old['catalog'] if 'market' in e['group'].lower() and e['havora_id'] in mp]
W=1040;H=1400
im=Image.new('RGB',(W,H),'#152b38');d=ImageDraw.Draw(im)
font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
f=lambda s:ImageFont.truetype(font,s)
d.text((30,18),'HAVORA  /  BUILDING + MARKET PIECES',font=f(27),fill='#f4e7cf')
d.text((30,58),'Shared pair: HavoraCityPrimary / HavoraCity  •  IDs are hexadecimal',font=f(17),fill='#b6cdd8')
for i,(label,parts) in enumerate(report['statue_metatiles'].items()):
 x=30+i*155
 for row,mid in enumerate(parts):im.paste(tiles[mid].resize((64,64),Image.Resampling.NEAREST),(x,95+row*64))
 d.text((x,229),label+' '+ '/'.join(f'{v:03X}' for v in parts),font=f(13),fill='#e8e5d7')
grid=report['market_stall'];scale=3
for y,row in enumerate(grid):
 for x,mid in enumerate(row):im.paste(tiles[mid].resize((48,48),Image.Resampling.NEAREST),(375+x*48,92+y*48))
d.text((545,105),'Stall assembly (3 × 3)',font=f(18),fill='#f4e7cf')
for y,row in enumerate(grid):d.text((545,140+y*24),'  '.join(f'{mid:03X}' for mid in row),font=f(17),fill='#b6cdd8')
d.text((30,257),'LILYCOVE BUILDING MODULES  /  walls, windows, roofs and connectors',font=f(19),fill='#f4e7cf')
d.text((30,286),'Teal frame = added piece. Small E number = original Emerald metatile ID.',font=f(15),fill='#b6cdd8')
new=set(report['new_metatiles'])
for i,e in enumerate(report['building_tiles']):
 x=30+i%14*72;y=322+i//14*76;mid=e['metatile']
 im.paste(tiles[mid].resize((48,48),Image.Resampling.NEAREST),(x,y))
 if mid in new:d.rectangle((x-2,y-2,x+49,y+49),outline='#57d6c3',width=2)
 d.text((x,y+50),f'{mid:03X}',font=f(13),fill='#f4e7cf');d.text((x+28,y+51),f'E{e["source_id"]:03X}',font=f(9),fill='#8fa8b5')
y0=802
d.text((30,y0),'SLATEPORT MARKET DETAILS  /  stall, umbrella and waterfront catalog',font=f(19),fill='#f4e7cf')
for i,e in enumerate(market):
 x=30+i%14*72;y=y0+40+i//14*76;mid=mp[e['havora_id']]
 im.paste(tiles[mid].resize((48,48),Image.Resampling.NEAREST),(x,y));d.text((x,y+50),f'{mid:03X}',font=f(13),fill='#f4e7cf')
d.text((30,1200),'Statues: stack the two IDs vertically. Use solid collision and the local elevation.',font=f(17),fill='#b6cdd8')
d.text((30,1231),'Building bases, statue bases and doorways can use the existing paving or grass.',font=f(17),fill='#b6cdd8')
d.text((30,1262),'Native tile preview • Existing map layouts and placed artwork preserved.',font=f(17),fill='#b6cdd8')
im.save(R/'docs/havora/authoring-assets.png')
print(R/'docs/havora/authoring-assets.png')
