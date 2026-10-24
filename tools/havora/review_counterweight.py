#!/usr/bin/env python3
"""Labeled native tile/sprite plan and real emulator captures for the grove."""
from pathlib import Path
import json
from PIL import Image,ImageDraw,ImageFont
from review_market import scene
R=Path(__file__).resolve().parents[2];d=json.loads((R/'tools/havora/counterweight-puzzle.json').read_text());dest=R/'docs/havora';dest.mkdir(parents=True,exist_ok=True)
font=lambda n:ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',n)
mapim=scene('HavoraNorthQuadrant','LAYOUT_HAVORA_NORTH_QUADRANT').crop((3*16,9*16,32*16,28*16)).resize((928,608),Image.Resampling.NEAREST)
out=Image.new('RGB',(1370,795),'#172d34');out.paste(mapim,(24,112));draw=ImageDraw.Draw(out)
draw.text((24,20),'HAVORA / WORKING COUNTERWEIGHT GROVE',font=font(28),fill='#f3dfbc');draw.text((24,66),'Your placed maze • Native gate art and interactive objects • Reference labels added',font=font(19),fill='#c7d9cd')
for kind,coords in [('plate',d['plates']),('gate',d['gates'])]:
 for i,(x,y) in enumerate(coords):
  xx,yy=24+(x-3)*32,112+(y-9)*32;co='#f0d47b' if kind=='plate' else '#83d3ec';label=('ABCD' if kind=='plate' else 'ABZ')[i]
  draw.rectangle((xx,yy,xx+31,yy+31),outline=co,width=2);draw.text((xx+2,yy+1),label,font=font(13),fill=co,stroke_width=1,stroke_fill='#172d34')
lines=[('BUTTON / GATE PAIRS',22),('A (16,22) → gate (19,22)',18),('B (21,21) → gate (16,21)',18),('',12),('FOREST GATE (10,13)',22),('Fill all three pits.',18),('Keep B + C + D weighted.',18),('',12),('REUSABLE WEIGHTS',22),('Only boulders press buttons.',18),('Taking one away closes its gate.',18),('Occupied gates cannot close.',18),('',12),('PERSISTENT PROGRESS',22),('Moves, cuts and filled pits',18),('survive leaving/reloading.',18),('',12),('RESET',22),('Use the notice by the entrance,',18),('inspect a gate, or press',18),('L + R + SELECT in the maze.',18),('Confirmation comes first.',18)]
y=116
for s,n in lines:draw.text((985,y),s,font=font(n),fill='#f3dfbc' if n>20 else '#d6e1d7');y+=28 if n<20 else 35
draw.text((24,748),'Native tile/sprite plan, not a Porymap screenshot. Separate emulator captures show the tested runtime.',font=font(18),fill='#c7d9cd');out.save(dest/'counterweight-preview.png')
names=[('grove-initial','Initial gates and reset notice'),('grove-gate-a-open','Gate A opens under boulder weight'),('grove-forest-gate-open','Completed forest approach'),('grove-reset-confirmation','Reset asks before changing progress')]
sheet=Image.new('RGB',(1480,1100),'#172d34');sd=ImageDraw.Draw(sheet);sd.text((24,12),'HAVORA / REAL ROM EMULATOR CHECKS',font=font(28),fill='#f3dfbc')
for i,(name,title) in enumerate(names):
 x=20+i%2*740;y=60+i//2*520;sd.text((x,y),title,font=font(19),fill='#d6e1d7');sheet.paste(Image.open(R/'build/havora-tests'/f'{name}.png'),(x,y+30))
sheet.save(dest/'counterweight-emulator.png')
