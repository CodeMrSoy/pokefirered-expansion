#!/usr/bin/env python3
"""Build GBA radial-light dithering masks with subtle flame variation.

Each frame packs four 64px OBJ quadrants vertically. Black pixels attenuate
light, transparent pixels reveal the cave. The fixed Bayer pattern does not
crawl; only the gentle falloff strength changes, without touching game RNG.
"""
from pathlib import Path
from PIL import Image
import math
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'graphics/field_effects/lantern_glow'
BAYER=((0,32,8,40,2,34,10,42),(48,16,56,24,50,18,58,26),
       (12,44,4,36,14,46,6,38),(60,28,52,20,62,30,54,22),
       (3,35,11,43,1,33,9,41),(51,19,59,27,49,17,57,25),
       (15,47,7,39,13,45,5,37),(63,31,55,23,61,29,53,21))
PULSE=(0.0,0.35,-0.25,0.6,0.1,-0.4,0.25,-0.1)
OUT.mkdir(parents=True,exist_ok=True)
for frame,pulse in enumerate(PULSE):
    mask=Image.new('P',(128,128))
    mask.putpalette([0]*768)
    for y in range(128):
        for x in range(128):
            radius=math.hypot(x-63.5,y-63.5)
            t=max(0.0,min(1.0,(radius-22-pulse)/(34-pulse)))
            darkness=t*t*(3-2*t)
            if darkness>(BAYER[y&7][x&7]+0.5)/64:
                mask.putpixel((x,y),1)
    packed=Image.new('P',(64,256));packed.putpalette([0]*768)
    for i,(x,y) in enumerate(((0,0),(64,0),(0,64),(64,64))):
        packed.paste(mask.crop((x,y,x+64,y+64)),(0,i*64))
    packed.save(OUT/f'frame_{frame}.png',transparency=0)
