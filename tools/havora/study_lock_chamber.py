"""Isolated native-tile art study. Does not modify map layouts or game logic."""
from pathlib import Path
from PIL import Image,ImageDraw
import textwrap
R=Path(__file__).resolve().parents[2]
# Reuse the exact tile decoding/palette logic of the production renderer.
source=(R/'tools/havora/render_captains_trial.py').read_text()
ns={'__file__':str(R/'tools/havora/render_captains_trial.py')}
exec(source[:source.index('def render(out):')],ns)
exec(textwrap.dedent(source.split('def render(out):\n')[1].split(' layout=')[0]),ns)
T=ns['metas'];W,H=26,24
out=R/'docs/havora/review';out.mkdir(exist_ok=True)
def terrace_face(width):
 # Native-resolution stepped corners and two shaded stone courses, using the
 # gym's existing stone palette. Transparent corners preserve the water below.
 p=Image.new('RGBA',(width,20));d=ImageDraw.Draw(p)
 dark=(40,48,56);shade=(64,80,88);stone=(88,104,112);light=(152,168,168)
 outline=[(4,0),(width-5,0),(width-2,3),(width-1,6),(width-1,14),(width-4,18),(width-7,19),(6,19),(3,18),(0,14),(0,6),(1,3)]
 d.polygon(outline,fill=dark)
 d.polygon([(4,1),(width-5,1),(width-2,4),(width-4,7),(3,7),(1,4)],fill=light)
 d.rectangle((4,3,width-5,5),fill=stone)
 d.polygon([(2,8),(width-3,8),(width-3,13),(width-6,17),(5,17),(2,13)],fill=stone)
 for x in range(8,width-3,14):
  d.line((x,8,x,11),fill=shade);d.line((x+5,12,x+5,16),fill=dark)
 d.line((3,11,width-4,11),fill=shade)
 d.line((6,16,width-7,16),fill=shade)
 return p

def study(level):
 im=Image.new('RGB',(W*16,H*16))
 def tile(x,y,m):im.paste(T[m],(x*16,y*16))
 def rect(x,y,w,h,m):
  for yy in range(y,y+h):
   for xx in range(x,x+w):tile(xx,yy,m)
 rect(0,0,W,H,0x3b0)
 # Finite building footprint and permanent upper control terrace.
 rect(1,2,24,20,0x380);rect(1,2,24,1,0x349);rect(1,3,24,1,0x348)
 rect(2,4,22,3,0x281);rect(2,7,22,1,0x3b1)
 for x in [2,9,16,23]:tile(x,3,0x347)
 tile(4,5,0x301);tile(5,5,0x303);tile(21,5,[0x376,0x387,0x377][round(level)])
 # The lock is a fixed basin, not a giant wall replacing the water.
 rect(6,8,14,12,0x282)
 # Only a shallow rear retaining face changes its exposed height.
 wall=round((2-level)*8)
 strip=Image.new('RGB',(13*16,32))
 for x in range(13):strip.paste(T[0x380],(x*16,0));strip.paste(T[0x380],(x*16,16))
 if wall:im.paste(strip.crop((0,0,208,wall)),(7*16,8*16))
 for x in range(7,20):im.paste(T[0x381],(x*16,8*16+wall))
 # Separate landing tiers have a face, a deck edge and a short ladder flight.
 for side in [2,20]:
  rect(side,8,4,12,0x282)
  for tier,y in [(2,8),(1,12),(0,16)]:
   if level<tier+1:
    rect(side,y,4,3,0x281);rect(side,y+3,4,1,0x3b1)
    lip=side+3 if side==2 else side
    for yy in range(y,y+3):tile(lip,yy,0x3b2 if side==2 else 0x3b3)
    # Round the seaward masonry lip; the lower courses give a cliff-like face.
    edge=lip*16+(12 if side==2 else 0)
    draw=ImageDraw.Draw(im)
    draw.rectangle((edge,y*16+3,edge+3,(y+3)*16-2),fill=(40,48,56))
    draw.line((edge+1,y*16+4,edge+1,(y+3)*16-3),fill=(152,168,168))
    tile(lip,y+1,0x370 if side==2 else 0x372)
    face=terrace_face(64)
    im.paste(face,(side*16,(y+3)*16-4),face)
  # Stair towers stay solid and dry; two short flights link the landings.
  shaft=side if side==2 else side+3
  # Dry landings interrupt the ladder silhouette. Each short flight spans
  # only one terrace face, with rail ends anchored to its upper landing.
  rect(shaft,8,1,12,0x281)
  for yy in [7,11,15,19]:
   tile(shaft,yy,0x380)
   draw=ImageDraw.Draw(im);px=shaft*16;py=yy*16
   for x in [4,11]:
    draw.line((px+x,py-2,px+x,py+14),fill=(40,48,56),width=3)
    draw.line((px+x,py-2,px+x,py+14),fill=(152,168,168))
   for rung in [2,7,12]:
    draw.line((px+4,py+rung+1,px+11,py+rung+1),fill=(40,48,56))
    draw.line((px+4,py+rung,px+11,py+rung),fill=(232,224,192))
  # During rising water, cover each lower landing from its seaward edge.
  for tier,y in [(1,12),(0,16)]:
   fraction=max(0,min(1,level-tier))
   if fraction and fraction<1:
    width=round(3*16*fraction)
    water=Image.new('RGB',(48,64))
    for yy in range(4):
     for xx in range(3):water.paste(T[0x282],(xx*16,yy*16))
    px=(side+1)*16 if side==2 else side*16
    if side==2:px+=48-width
    im.paste(water.crop((0,0,width,64)),(px,y*16))
 # Finished foreground seawall and safe entrance.
 rect(2,20,22,1,0x3b1);rect(2,21,22,1,0x380)
 rect(10,4,4,1,0x280)
 # Boat floats vertically by a small amount; the basin never moves north.
 bx,by=12*16,15*16-round(level*8)
 for yy in range(3):
  for xx in range(3):im.paste(T[0x2bc+yy*3+xx],(bx+xx*16,by+yy*16))
 return im
panels=Image.new('RGB',(W*16*3+32,H*16+58),'#20282e');d=ImageDraw.Draw(panels)
for i,label in enumerate(['LOW: all landings exposed','MID: lower landing submerged','HIGH: upper landing only']):
 x=i*(W*16+8)+4;panels.paste(study(i),(x,30));d.text((x+8,10),label,fill='#eee2c1')
d.text((12,H*16+38),'TILE ART STUDY + PROPOSED STONE CAPS — not an implemented map',fill='white')
panels.save(out/'lock-chamber-study.png')
frames=[]
for v in [0]*8+[i/8 for i in range(17)]+[2]*8+[i/8 for i in range(16,-1,-1)]:
 frames.append(study(v).resize((W*32,H*32),Image.Resampling.NEAREST))
frames[0].save(out/'lock-chamber-study.gif',save_all=True,append_images=frames[1:],duration=140,loop=0)

study(0).crop((16,112,128,320)).resize((448,832),Image.Resampling.NEAREST).save(out/'lock-rounded-platform-detail.png')
