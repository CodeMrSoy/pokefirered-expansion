#!/usr/bin/env python3
"""Native tile reference sheet for the expanded Porymap kits."""
import json,sys,struct
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from render import atlas
from review_market import scene
R=Path(__file__).resolve().parents[2];d=json.loads((R/'tools/havora/editor-kits.json').read_text());ims=atlas('havora_city','havora_city')
font=lambda n:ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',n)
out=Image.new('RGB',(1040,940),'#172c36');dr=ImageDraw.Draw(out)
dr.text((24,16),'HAVORA / COMPLETE EDITOR KITS',font=font(27),fill='#f2dfbc')
def kit(grid,x,y,s=3):
 for j,row in enumerate(grid):
  for i,mid in enumerate(row):out.paste(ims[mid].resize((16*s,16*s),Image.Resampling.NEAREST),(x+i*16*s,y+j*16*s))
dr.text((24,65),'Wide stall — all side posts and counter ends',font=font(18),fill='white');kit(d['stalls']['wide'],24,99,4)
dr.text((480,65),'Narrow stall',font=font(18),fill='white');kit(d['stalls']['narrow'],480,99,4)
dr.text((24,310),'Goods, baskets and counters',font=font(18),fill='white')
ids=[d['slateport_source_mapping'][str(i)] for i in [0x20b,0x20c,0x213,0x214,0x21b,0x21c,0x220,0x221,0x222,0x223,0x224,0x228,0x229,0x22a,0x22b,0x230,0x231,0x238,0x239,0x23b]]
for n,mid in enumerate(ids):
 x=24+n%10*64;y=346+n//10*72;out.paste(ims[mid].resize((48,48)),(x,y));dr.text((x,y+50),f'{mid:03X}',font=font(13),fill='#cbdad9')
dr.text((24,520),'Bond Bridge forest mouth / reference entrance',font=font(18),fill='white')
# Exact native tree framing around the imported opening, using existing General IDs.
lookup=json.loads((R/'tools/havora/city-tileset.json').read_text())['native_general_ids'];tree=[[lookup[str(v)] for v in row] for row in [[20,21],[28,29],[36,37]]]
layouts=json.loads((R/'data/layouts/layouts.json').read_text())['layouts'];l=next(l for l in layouts if l['id']=='LAYOUT_THREE_ISLAND_BOND_BRIDGE');raw=(R/l['blockdata_filepath']).read_bytes();ws=struct.unpack('<'+'H'*(len(raw)//2),raw)
source=[[0x330,0x331,0x332,0x333],[0x338,0x339,0x33a,0x33b],[0x340,0x341,0x342,0x343]];mp={v:d['forest_entrance'][j][i] for j,row in enumerate(source) for i,v in enumerate(row)}
forest=[]
for y in range(2,7):
 forest.append([mp[v] if v in mp else lookup[str(v)] for x in range(9,17) for v in [ws[y*l['width']+x]&1023]])
forest += [[0]*8,[0]*8]
kit(forest,24,558,3)
dr.text((480,520),'Court chalk / native map tiles',font=font(18),fill='white')
kit(d['court'],480,558,3)
dr.text((24,910),'Native tile render. Kits are available to place in Porymap; no new forest destination or warp added.',font=font(16),fill='#b9ccd0');out.save(R/'docs/havora/editor-kits-preview.png')
scene('HavoraWestQuadrant','LAYOUT_HAVORA_WEST_QUADRANT').crop((48,0,576,384)).resize((1056,768),Image.Resampling.NEAREST).save(R/'docs/havora/gym-garden-preview.png')
