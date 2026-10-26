"""Precise planning diagram for the abstract lock model; not game artwork."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[2]
im=Image.new('RGB',(1200,1050),'#122131');d=ImageDraw.Draw(im)
fp='/usr/share/fonts/truetype/dejavu/DejaVuSans'
f=ImageFont.truetype(fp+'.ttf',17);small=ImageFont.truetype(fp+'.ttf',14);b=ImageFont.truetype(fp+'-Bold.ttf',19);title=ImageFont.truetype(fp+'-Bold.ttf',28)
def txt(x,y,s,font=f,c='#e4edf4'):d.text((x,y),s,font=font,fill=c)
def rect(box,c,outline=None,w=2):d.rectangle(box,fill=c,outline=outline,width=w)
def label(x,y,text):
 box=d.textbbox((x,y),text,font=small);rect((box[0]-3,box[1]-2,box[2]+3,box[3]+2),'#122131');txt(x,y,text,small)
def dash(points,c='#f5d18f',width=3):
 for p,q in zip(points,points[1:]):
  import math
  distance=math.dist(p,q)
  for t in range(0,int(distance),12):
   aa=t/distance;bb=min(t+7,distance)/distance
   d.line([(p[0]+(q[0]-p[0])*aa,p[1]+(q[1]-p[1])*aa),(p[0]+(q[0]-p[0])*bb,p[1]+(q[1]-p[1])*bb)],fill=c,width=width)
def boat(x,y,text):
 d.polygon([(x-28,y-8),(x-20,y-16),(x+20,y-16),(x+28,y-8),(x+28,y+8),(x+20,y+16),(x-20,y+16),(x-28,y+8)],fill='#795c3a',outline='#f4d59e',width=3)
 d.line((x-15,y-10,x-15,y+10),fill='#d6b77e',width=4);d.line((x+15,y-10,x+15,y+10),fill='#d6b77e',width=4)
 label(x-30,y+24,text)
def valve(x,y,t):
 d.ellipse((x-11,y-11,x+11,y+11),fill='#2f536b',outline='#8cdae3',width=2);d.line((x-7,y,x+7,y),fill='#f8dda7',width=2);d.line((x,y-7,x,y+7),fill='#f8dda7',width=2);label(x-30,y+14,t)

txt(26,16,'HAVORA — FIXED-TRANSFER LOCK DESIGN',title)
txt(26,56,'Logic and height study • larger interior approved • not a finished game map',f,'#9fb7c9')
# Upper isolated platforms: cargo bridge is a physical access dependency.
rect((445,100,720,180),'#856745','#e2c18b');txt(460,112,'SERVICE PLATFORM',b);txt(460,140,'Low maintenance winch + dry pump',small)
rect((865,100,1160,180),'#856745','#e2c18b');txt(882,112,'CAPTAIN’S DECK',b);txt(882,140,'Reached from B on the final bridge',small)
dash([(650,180),(650,245)]);label(485,195,'Cargo bridge first: B HIGH')
dash([(745,255),(840,210),(975,180)],'#b9e69d');label(815,217,'Final bridge: B = C = HIGH')

for i,(x,name,level) in enumerate([(30,'A  RECEIVING LOCK',2),(420,'B  SERVICE LOCK',2),(810,'C  CAPTAIN LOCK',0)]):
 rect((x,260,x+360,665),'#657582','#a6b2bc');rect((x+10,270,x+350,650),'#344954')
 txt(x+14,275,name,b)
 # Retaining face with exposed masonry, and three distinct water marks.
 rect((x+22,325,x+298,635),'#627783')
 for yy in range(325,636,22):
  d.line((x+22,yy,x+298,yy),fill='#344954',width=2)
  for xx in range(x+22+(11 if yy//22%2 else 0),x+299,44):d.line((xx,yy,xx,yy+20),fill='#344954',width=1)
 surface={2:360,1:465,0:570}[level]
 rect((x+22,surface,x+298,635),'#337eac')
 for yy in range(surface+6,635,12):d.line((x+22,yy,x+298,yy),fill='#458fb9')
 d.line((x+22,surface,x+298,surface),fill='#c7edf2',width=3)
 for yy,t in [(360,'HIGH'),(465,'MID'),(570,'LOW')]:
  d.line((x+272,yy,x+304,yy),fill='#e5d69a',width=2);txt(x+236,yy-20,t,small)
 # Raised control deck remains above highest flood line; ladder descends to dock.
 rect((x+20,304,x+300,322),'#a08050','#d6b77e')
 rect((x+303,304,x+349,326),'#a08050','#d6b77e')
 for xx in [x+315,x+338]:d.line((xx,328,xx,563),fill='#d6b77e',width=4)
 for yy in range(336,562,13):d.line((x+315,yy,x+338,yy),fill='#c5a16b',width=3)
 # Ghosted low dock shows what will be submerged when filling.
 rect((x+210,543,x+301,558),'#46718a' if level==2 else '#a08050','#d6b77e')
 label(x+34,615,'Start: '+['LOW','MID','HIGH'][level])
 valve(x+76,312,'A ↔ B' if i==0 else 'B ↔ C' if i==1 else 'A ↔ B + B ↔ C')
 if i==0:boat(x+100,384,'Launch starts here')
 if i==2:boat(x+218,598,'Cargo starts here')
# Gate connection channels and service shore.
for x,text,color in [(390,'A/B OPEN','#a7e0a6'),(780,'B/C CLOSED','#f3a1a1')]:
 d.line((x-6,450,x+36,450),fill=color,width=7);label(x-54,422,text)
dash([(445,686),(1160,686),(1160,330)],'#a2d5c4');label(575,677,'Middle service boardwalk: B = C = MID')
dash([(850,550),(1090,550)],'#f2d08e');label(848,521,'C shore: walk here only at LOW')

rect((24,735,1176,1027),'#1e3448','#435d72')
txt(44,750,'THE THREE DEPENDENCIES',b,'#ffda96')
for y,a,c in [(789,'1. Service access','Move the cargo boat to B HIGH. Drain to uncover the winch; refill to get back.'),(847,'2. Leave a way back','Park the launch at C. Move cargo to the outer berth, then drain C to walk off.'),(905,'3. Final configuration','Redistribute to A LOW, B HIGH, C HIGH. Secure cargo; use the launch to return to B.')]:
 txt(44,y,a,b);txt(44,y+25,c,small)
txt(44,980,'One valve operation transfers exactly one level. Neither chamber can go below LOW or above HIGH.',small,'#aac3d8')
txt(44,1003,'Dry controls sit above HIGH; flooded docks have separate upper landings. Minor recovery ledges are omitted here.',small,'#aac3d8')
out=R/'docs/havora/review/fixed-transfer-design.png';im.save(out);print(out)
