"""Native tile/sprite review sheet; no generated illustration or Porymap claim."""
import json
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from render import render
R=Path(__file__).resolve().parents[2]
B=R/'build'
def scene(name,layout):
    path=B/(name+'-native.png');render(layout,path)
    im=Image.open(path).convert('RGBA')
    objects=json.loads((R/f'data/maps/{name}/map.json').read_text())['object_events']
    specs={'MAN':('people/man.png','npc_white',16,32),
           'WOMAN_1':('people/woman_1.png','npc_green',16,32),
           'SAILOR':('people/sailor.png','npc_pink',16,32),
           'FISHER':('people/fisher.png','npc_white',16,32),
           'SEAGALLOP':('misc/seagallop.png','seagallop',64,64),
           'GENTLEMAN':('people/gentleman.png','npc_white',16,32),
           'GYM_GUY':('people/gym_guy.png','npc_pink',16,32),
           'PIDGEY':('pokemon/pidgey.png','npc_blue',16,16),
           'NIDORAN_F':('pokemon/nidoran_f.png','npc_pink',16,16)}
    for obj in sorted(objects,key=lambda o:o['y']):
        file,pal,w,h=specs[obj['graphics_id'].removeprefix('OBJ_EVENT_GFX_')]
        root=R/'graphics/object_events'
        image=Image.open(root/'pics'/file)
        x=16 if w==16 and obj['movement_type'].endswith('UP') else 0
        image=image.crop((x,0,x+w,h))
        palette=[tuple(map(int,s.split())) for s in (root/'palettes'/(pal+'.pal')).read_text().splitlines()[3:19]]
        image.putpalette(sum((list(c) for c in palette),[])+[0]*720)
        image.info['transparency']=0
        im.alpha_composite(image.convert('RGBA'),(obj['x']*16+8-w//2,obj['y']*16+16-h))
    return im.convert('RGB')
def main(out):
    city=scene('QuantumHavoraNorthQuay','LAYOUT_QUANTUM_HAVORA_NORTH_QUAY')
    harbor=scene('QuantumHarbor','LAYOUT_QUANTUM_HAVORA_HARBOR_LAYOUT')
    cityheight=city.height*2;footer=88+cityheight+1024
    sheet=Image.new('RGB',(1280,footer+136),'#132532');d=ImageDraw.Draw(sheet)
    font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',24)
    small=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',18)
    d.text((20,14),'HAVORA — RAISED CITY TERRACE',font=font,fill='white')
    d.text((20,50),'Dedicated city tileset | Native FireRed cliffs, trees and stairs | Elevation 4 city / elevation 3 harbor',font=small,fill='#badce7')
    sheet.paste(city.resize((1280,cityheight),Image.Resampling.NEAREST),(0,88))
    sheet.paste(harbor.resize((1280,1024),Image.Resampling.NEAREST),(0,88+cityheight))
    d.text((20,footer+20),'Two stairways join the raised market to a lower garden promenade and the existing harbor.',font=small,fill='white')
    d.text((20,footer+52),'Actual tile-and-sprite render. Dedicated city pair keeps compatible harbor edge graphics and animated water.',font=small,fill='#badce7')
    d.text((20,footer+84),'Porymap map: QuantumHavoraNorthQuay | Primary: HavoraCityPrimary | Secondary: HavoraCity',font=small,fill='#badce7')
    sheet.save(out)
if __name__=='__main__':
    import sys
    main(sys.argv[1])
