"""Native indexed-pixel art kit for Corvala. Every piece remains a reusable metatile."""
from PIL import Image,ImageDraw
import random
# Banks 7–12; all values are GBA representable, index zero is transparent.
PALETTES=[
['000000','204868','286880','308898','48a8b0','68c0b8','90d8c0','c0e8d0','f0e0b0','d8c088','b8a070','98b088','e8f0d0','70a8a0','387888','b8d8b8'],
['000000','383838','504840','685848','887050','a08860','c0a878','d8c088','283c38','385840','487048','608850','80a060','a8b870','706858','908068'],
['000000','383838','584030','785038','986840','b88858','d0a870','e8c890','284858','386880','4888a0','68a8b8','b0c8b8','d8d8b8','182c38','f0e0b0'],
['000000','383838','584030','785038','986840','b88858','d0a870','e8c890','304838','486848','608858','80a870','b0c8b8','d8d8b8','182c38','f0e0b0'],
['000000','383838','584030','785038','986840','b88858','d0a870','e8c890','785030','a07038','c09848','e0b868','b0c8b8','d8d8b8','182c38','f0e0b0'],
['000000','286880','408898','68b0b0','90d0c0','584878','886898','b088c0','d8b0d8','985078','c87098','e8a0b8','887050','b09868','d8c088','d8e8c8']]
PALETTES=[[tuple((int(c[i:i+2],16)>>3)<<3 for i in (0,2,4)) for c in bank] for bank in PALETTES]
def im(w=16,h=16,c=0):return Image.new('P',(w,h),c)
def water(shallow=False,variant=0):
 a=im(c=5 if shallow else 3);d=ImageDraw.Draw(a)
 for x,y in [(1,3),(10,11)]:
  x=(x+variant*3)%12;d.line((x,y,x+3,y),fill=6 if shallow else 4);d.point((x-1,y+1),fill=4 if shallow else 2)
 return a

def sand():
 a=im(c=8);d=ImageDraw.Draw(a)
 for x,y in [(2,4),(12,10),(6,14)]:d.point((x,y),fill=9)
 return a

def grass():
 a=im(c=10);d=ImageDraw.Draw(a)
 for x,y in [(1,3),(7,11),(13,5)]:d.line((x,y+2,x+1,y),fill=11);d.point((x+2,y+2),fill=12)
 return a

def shore(mask,shallow=True):
 a=sand();d=ImageDraw.Draw(a)
 # N,E,S,W: small scallops soften the tile-grid outline.
 for bit in range(4):
  if not mask&(1<<bit):continue
  for u in range(16):
   depth=2+(u%8 in [0,1,6,7])
   for v in range(depth):
    x,y=[(u,v),(15-v,u),(u,15-v),(v,u)][bit];a.putpixel((x,y),5 if shallow else 3)
   x,y=[(u,depth),(15-depth,u),(u,15-depth),(depth,u)][bit];a.putpixel((x,y),7)
 return a

def cliff(mask=0,variant=0):
 a=im(c=4);d=ImageDraw.Draw(a);rng=random.Random(200+variant)
 for row in range(3):
  for col in range(3):
   x=col*6-(row%2)*3;y=row*6-1
   d.polygon([(x+1,y),(x+5,y),(x+6,y+3),(x+4,y+5),(x,y+4)],fill=5 if (col+row+variant)%3 else 3,outline=2)
   d.line((x+1,y+1,x+4,y+1),fill=6)
 for x,y in [(3,3),(12,12)]:d.point((x,y),fill=7)
 if mask&1:d.line((0,0,15,0),fill=12,width=2)
 if mask&4:d.line((0,14,15,14),fill=2,width=2)
 return a

def cave():
 a=im(48,48,c=4);d=ImageDraw.Draw(a)
 for y in range(0,48,16):
  for x in range(0,48,16):a.paste(cliff(variant=(x+y)//16%2),(x,y))
 d.polygon([(7,47),(7,26),(12,12),(19,6),(30,6),(38,17),(42,30),(42,47)],fill=2)
 d.polygon([(12,47),(12,27),(18,15),(28,13),(35,24),(37,47)],fill=1)
 for x,y in [(10,21),(17,10),(29,9),(36,19)]:d.line((x,y,x+3,y-2),fill=6)
 return a

def board():
 a=im(c=5);d=ImageDraw.Draw(a)
 for y in [0,8]:
  d.line((0,y,15,y),fill=3);d.line((0,y+1,15,y+1),fill=6)
  x=4 if y else 12;d.line((x,y+1,x,y+7),fill=4);d.point((x-2,y+2),fill=4)
 return a

def deckedge(mask):
 a=board();d=ImageDraw.Draw(a)
 for bit,box in enumerate([(0,0,15,3),(12,0,15,15),(0,12,15,15),(0,0,3,15)]):
  if mask&(1<<bit):
   d.rectangle(box,fill=2)
   for pos in [1,13]:
    if bit in [0,2]:x,y=pos,(1 if bit==0 else 12)
    else:x,y=(1 if bit==3 else 12),pos
    d.rectangle((x,y,x+1,y+2),fill=7)
   line=[(0,1,15,1),(13,0,13,15),(0,13,15,13),(1,0,1,15)][bit];d.line(line,fill=6)
 return a

def support():
 a=im(c=14);d=ImageDraw.Draw(a)
 d.rectangle((0,0,15,2),fill=2)
 for x in [2,12]:d.rectangle((x,2,x+2,10),fill=3);d.line((x,2,x,9),fill=6)
 d.line((0,12,5,12),fill=10);d.line((10,12,15,12),fill=10)
 return a

def stairs():
 a=im(c=4);d=ImageDraw.Draw(a)
 for y in range(0,16,4):d.rectangle((2,y,13,y+2),fill=6);d.line((2,y+3,13,y+3),fill=2)
 d.line((1,0,1,15),fill=3);d.line((14,0,14,15),fill=3)
 return a

def house(width=5,tall=False):
 # Pitched roof, two-pixel timber framing, deep window recesses and a porch.
 w=width*16;h=96 if tall else 80;a=im(w,h);d=ImageDraw.Draw(a)
 d.rectangle((8,34,w-9,h-12),fill=6,outline=2)
 for x in range(11,w-9,6):d.line((x,39,x,h-13),fill=5)
 d.polygon([(w//2,12),(5,36),(w-6,36)],fill=10)
 d.rectangle((5,35,w-6,38),fill=2)
 d.polygon([(w//2,2),(3,23),(3,36),(w//2,15),(w-4,36),(w-4,23)],fill=8,outline=1)
 # Overhead roof planes meet at a visible ridge.
 d.polygon([(w//2,3),(w-5,24),(w-5,35),(w//2,15)],fill=9)
 d.polygon([(w//2,3),(5,24),(5,34),(w//2,14)],fill=10)
 for y in [9,15,21]:
  d.line((7,23+y//3,w//2,3+y//3),fill=11)
  d.line((w//2+2,5+y//3,w-7,26+y//3),fill=8)
 d.line((w//2,2,w//2,15),fill=11)
 for x in [8,w-11,w//2-2]:d.rectangle((x,37,x+2,h-12),fill=3);d.line((x,38,x,h-13),fill=7)
 def window(x,y):
  d.rectangle((x,y,x+11,y+13),fill=2);d.rectangle((x+2,y+2,x+9,y+10),fill=14)
  d.line((x+3,y+3,x+8,y+3),fill=10);d.line((x+6,y+2,x+6,y+11),fill=7);d.line((x+2,y+7,x+9,y+7),fill=7)
  d.rectangle((x-1,y+13,x+12,y+15),fill=3);d.line((x,y+13,x+11,y+13),fill=7)
 for x in [15,w-27]:window(x,43)
 if tall:
  d.line((8,65,w-9,65),fill=3,width=3)
  for x in [15,w-27]:window(x,68)
 doorx=w//2-5;d.rectangle((doorx,h-30,doorx+11,h-12),fill=2);d.rectangle((doorx+2,h-28,doorx+9,h-12),fill=4);d.point((doorx+8,h-21),fill=15)
 d.rectangle((6,h-11,w-7,h-7),fill=3);d.line((6,h-11,w-7,h-11),fill=7)
 for x in [10,w-13]:d.rectangle((x,h-7,x+2,h-1),fill=2);d.line((x,h-7,x,h-2),fill=6)
 return a

def lighthouse():
 a=im(48,112);d=ImageDraw.Draw(a)
 d.ellipse((5,93,43,108),fill=2);d.ellipse((8,89,40,103),fill=12,outline=1)
 d.polygon([(16,35),(31,35),(35,94),(12,94)],fill=13,outline=1)
 d.polygon([(16,35),(21,35),(19,92),(13,94)],fill=12)
 for y in [47,64,80]:d.line((16,y,31,y),fill=12)
 for y in [45,65]:d.rectangle((22,y,26,y+7),fill=14)
 d.rectangle((12,25,35,36),fill=2);d.rectangle((15,15,32,28),fill=12,outline=1)
 for x in [18,25]:d.rectangle((x,17,x+3,25),fill=10)
 d.polygon([(9,15),(24,5),(38,15)],fill=8,outline=1);d.line((24,2,24,6),fill=1)
 d.rectangle((20,86,28,99),fill=2);d.rectangle((22,88,26,99),fill=4)
 return a

def coral(kind=0):
 a=im(c=3);d=ImageDraw.Draw(a);rng=random.Random(29+kind)
 # Layered boulder, fan, and branching growth; three compatible color ramps.
 ramp=[(9,10,11),(5,6,7),(12,13,14)][kind%3]
 if kind<3:
  d.ellipse((1,6,14,15),fill=1);d.ellipse((2,4,13,13),fill=ramp[0])
  for x,y in [(4,6),(9,5),(11,9),(5,11)]:d.ellipse((x-2,y-2,x+2,y+2),fill=ramp[1]);d.point((x-1,y-1),fill=ramp[2])
 else:
  for x,y in [(4,14),(11,13)]:
   d.line((x,y,x,y-10),fill=ramp[0],width=2)
   for off in [4,7]:d.line((x,y-off,x-3,y-off-3),fill=ramp[1],width=2);d.line((x,y-off+1,x+3,y-off-2),fill=ramp[1],width=2)
   d.point((x,y-10),fill=ramp[2])
 return a

def reefedge(mask):
 a=im(c=12);d=ImageDraw.Draw(a)
 for x,y in [(1,2),(9,1),(5,9),(12,10)]:
  d.rounded_rectangle((x-2,y-1,x+4,y+4),radius=2,fill=13,outline=1);d.point((x,y),fill=14)
 for bit in range(4):
  if mask&(1<<bit):
   for u in range(16):
    depth=2+(u%8 in [0,1,7])
    for v in range(depth):
     x,y=[(u,v),(15-v,u),(u,15-v),(v,u)][bit];a.putpixel((x,y),3)
    x,y=[(u,depth),(15-depth,u),(u,15-depth),(depth,u)][bit];a.putpixel((x,y),4)
 return a

def rock():
 a=im(c=3);d=ImageDraw.Draw(a);d.ellipse((2,5,14,15),fill=1);d.polygon([(2,10),(5,3),(10,1),(14,6),(13,12),(6,14)],fill=12,outline=1);d.line((5,4,9,3,12,6),fill=14);d.line((6,6,5,10),fill=13)
 return a

def reefpatch(variant=0):
 a=im(32,32,c=15);d=ImageDraw.Draw(a);rng=random.Random(918+variant)
 for _ in range(11):
  x=rng.randrange(1,31);y=rng.randrange(2,31);r=rng.choice([3,4,5,6]);ramp=rng.choice([(5,6,7),(9,10,11),(12,13,14)])
  d.ellipse((x-r,y-r,x+r,y+r),fill=ramp[0],outline=1)
  d.ellipse((x-r+1,y-r+1,x+r-1,y+r-1),fill=ramp[1]);d.point((x-1,y-r+1),fill=ramp[2])
 for x,y in [(5,14),(21,24),(28,10)]:
  d.line((x,y,x,y-8),fill=10,width=2)
  for off in [3,6]:d.line((x,y-off,x-3,y-off-2),fill=11);d.line((x,y-off,x+3,y-off-2),fill=11)
 return a

def coastal_tree():
 a=im(32,48);d=ImageDraw.Draw(a)
 d.ellipse((5,39,28,45),fill=8)
 d.polygon([(13,41),(15,15),(19,15),(19,40),(23,44),(16,43),(11,45)],fill=3)
 d.line((15,21,15,40),fill=6)
 for y in [22,28,34]:d.line((15,y,18,y+1),fill=2)
 for x,y,r in [(9,15,8),(21,15,9),(15,7,9),(7,25,6),(24,25,6),(15,22,10)]:
  d.ellipse((x-r,y-r,x+r,y+r),fill=8,outline=1)
  d.ellipse((x-r+2,y-r+1,x+r-1,y+r-3),fill=10)
  d.arc((x-r+3,y-r+2,x+r-2,y+r-4),190,290,fill=12,width=2)
  d.point((x-2,y-r+2),fill=13)
 return a

def lamp():
 a=im(16,32);d=ImageDraw.Draw(a)
 d.rectangle((7,9,9,29),fill=2);d.line((7,11,7,28),fill=6);d.rectangle((5,29,11,31),fill=3)
 d.rectangle((4,3,12,11),fill=2);d.rectangle((6,5,10,9),fill=15);d.line((8,4,8,10),fill=5)
 d.polygon([(3,3),(8,0),(13,3)],fill=8);d.point((7,6),fill=13)
 return a
