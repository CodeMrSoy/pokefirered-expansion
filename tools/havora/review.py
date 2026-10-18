#!/usr/bin/env python3
"""Render native tiles and original object sprites alongside emulator evidence."""
from pathlib import Path
import json
from PIL import Image,ImageDraw,ImageFont
from render import render
R=Path(__file__).resolve().parents[2];B=R/'build';render('LAYOUT_QUANTUM_HAVORA_HARBOR_LAYOUT',B/'havora-map-native.png');im=Image.open(B/'havora-map-native.png').convert('RGBA')
objs=json.loads((R/'data/maps/QuantumHarbor/map.json').read_text())['object_events']
spec={'OBJ_EVENT_GFX_SEAGALLOP':('misc/seagallop.png','seagallop',64,64),'OBJ_EVENT_GFX_SAILOR':('people/sailor.png','npc_pink',16,32),'OBJ_EVENT_GFX_MAN':('people/man.png','npc_white',16,32),'OBJ_EVENT_GFX_WOMAN_1':('people/woman_1.png','npc_green',16,32)}
for o in sorted(objs,key=lambda v:v['y']):
 file,pal,w,h=spec[o['graphics_id']];p=R/'graphics/object_events';s=Image.open(p/'pics'/file);s=s.crop((16 if w==16 and o['movement_type']=='MOVEMENT_TYPE_FACE_UP' else 0,0,(32 if w==16 and o['movement_type']=='MOVEMENT_TYPE_FACE_UP' else w),h))
 colors=[tuple(map(int,l.split())) for l in (p/'palettes'/(pal+'.pal')).read_text().splitlines()[3:19]];s.putpalette(sum((list(c) for c in colors),[])+[0]*720);s.info['transparency']=0;s=s.convert('RGBA');im.alpha_composite(s,(o['x']*16+8-w//2,o['y']*16+16-h))
im.convert('RGB').save(B/'havora-full-native.png')
sheet=Image.new('RGB',(1280,1560),'#132532');d=ImageDraw.Draw(sheet);f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',22);sm=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',17)
d.text((20,14),'HAVORA HARBOR — NATIVE GAME ASSETS',font=f,fill='white')
d.text((20,47),'40 x 32 map | Custom tileset: 269 / 384 graphics tiles | North + west outdoor city connections',font=sm,fill='#b3d8e4')
sheet.paste(im.convert('RGB').resize((1280,1024),Image.Resampling.NEAREST),(0,80))
d.text((20,1120),'VERIFIED mGBA GAMEPLAY — NIGHT LIGHTING',font=f,fill='white')
for i,name in enumerate(['havora-ferry-free-control','havora-lighthouse']):
 a=Image.open(B/'havora-tests'/(name+'.png')).resize((600,400),Image.Resampling.NEAREST);sheet.paste(a,(20+i*640,1160))
sheet.save(B/'Havora_Custom_Harbor_Preview.png')
