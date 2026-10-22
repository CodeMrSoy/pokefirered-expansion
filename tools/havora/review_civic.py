"""Map-data review panels and genuine mGBA service screenshots."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from review_market import scene
R=Path(__file__).resolve().parents[2];B=R/'build'
def main(out):
 maps={name:scene(name,lid) for name,lid in [
  ('HavoraWestQuadrant','LAYOUT_HAVORA_WEST_QUADRANT'),
  ('HavoraNorthQuadrant','LAYOUT_HAVORA_NORTH_QUADRANT'),
  ('HavoraDaycare','LAYOUT_HAVORA_DAYCARE'),
  ('HavoraLookout','LAYOUT_HAVORA_LOOKOUT')]}
 font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',30)
 small=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',23)
 sheet=Image.new('RGB',(2400,2528),'#132532');d=ImageDraw.Draw(sheet)
 d.text((32,18),'HAVORA — WESTERN HILLS, NORTHERN SQUARE & COASTAL DAYCARE',font=font,fill='white')
 d.text((32,60),'Actual map tiles and original sprites; panels show separate maps, not one continuous image.',font=small,fill='#badce7')
 d.text((32,104),'NORTHERN SQUARE — Center, Mart, homes and northern walk connection',font=small,fill='white')
 d.text((1600,104),'FAR EAST — Cliffside daycare & fenced yard',font=small,fill='white')
 sheet.paste(maps['HavoraNorthQuadrant'],(32,144));sheet.paste(maps['HavoraDaycare'],(1600,144))
 d.text((32,810),'WESTERN TERRACES — Gym above the waterfront',font=small,fill='white')
 d.text((832,810),'NORTHERN WALK / LOOKOUT',font=small,fill='white')
 d.text((1440,810),'VERIFIED mGBA GAMEPLAY',font=small,fill='white')
 sheet.paste(maps['HavoraWestQuadrant'],(32,856))
 sheet.paste(maps['HavoraLookout'].resize((512,1024),Image.Resampling.NEAREST),(832,856))
 for i,(file,label) in enumerate([('civic-center-healing','Nurse healing & relocated respawn'),('civic-mart-buy','Northern Mart — native Buy menu'),('civic-daycare-return','Daycare — deposit, level growth & collection')]):
  y=856+i*520;im=Image.open(B/'havora-tests'/(file+'.png'));sheet.paste(im,(1440,y));d.text((1440,y+480),label,font=small,fill='#badce7')
 d.text((832,1930),'Gym interior is enterable.',font=small,fill='white')
 d.text((832,1970),'Leader, team and badge',font=small,fill='white')
 d.text((832,2010),'progression are still unassigned.',font=small,fill='white')
 d.text((32,2420),'Seven new stairways | Seamless outdoor connections | Existing harbor layout and ferry interactions preserved',font=small,fill='white')
 d.text((32,2460),'Daycare uses the existing FireRed raising service. The northern lookout is ready for a future route connection.',font=small,fill='#badce7')
 sheet.save(out)
 maps['HavoraWestQuadrant'].resize((1536,3072),Image.Resampling.NEAREST).save(Path(out).with_name('Havora_Western_Gym_District.png'))
 north=Image.new('RGB',(2304,640));north.paste(maps['HavoraNorthQuadrant'],(0,0));north.paste(maps['HavoraDaycare'],(1536,0))
 north.resize((4608,1280),Image.Resampling.NEAREST).save(Path(out).with_name('Havora_North_And_Coastal_Districts.png'))
if __name__=='__main__':
 import sys
 main(sys.argv[1])
