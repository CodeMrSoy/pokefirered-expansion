#!/usr/bin/env python3
"""Compare approved art with the actual native map, keeping labels explicit."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import argparse,subprocess,sys
R=Path(__file__).resolve().parents[2];B=R/'build'
p=argparse.ArgumentParser();p.add_argument('--reference',required=True);args=p.parse_args()
subprocess.run([sys.executable,str(R/'tools/havora/review.py')],check=True)
sheet=Image.new('RGB',(1280,1100),'#132532');d=ImageDraw.Draw(sheet);f=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',21);sm=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',16)
d.text((20,12),'APPROVED REFERENCE — ILLUSTRATION',font=f,fill='white');d.text((660,12),'REWORKED MAP — NATIVE GAME TILES',font=f,fill='white')
sheet.paste(Image.open(args.reference).convert('RGB').resize((640,512),Image.Resampling.NEAREST),(0,52));sheet.paste(Image.open(B/'havora-full-native.png'),(640,52))
d.text((20,580),'40 x 32 map. Restored building heights, raised pier, deep seawalls, dock supports and rocky lighthouse footing.',font=sm,fill='#c6dce7')
d.text((20,616),'mGBA: WAREHOUSE / CRANE',font=f,fill='white');d.text((660,616),'mGBA: LIGHTHOUSE / SEAWALL',font=f,fill='white')
for i,name in enumerate(['havora-warehouses','havora-lighthouse']):sheet.paste(Image.open(B/'havora-tests'/(name+'.png')).resize((600,400),Image.Resampling.NEAREST),(20+i*640,658))
d.text((20,1072),'Gameplay captures show normal night lighting. The native overview uses untinted game palettes.',font=sm,fill='#c6dce7')
sheet.save(B/'Havora_Harbor_Reworked_Preview.png')
