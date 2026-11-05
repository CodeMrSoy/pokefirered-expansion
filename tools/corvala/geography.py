"""80 x 64 LOW-tide plan; native 16px cells, maintained with build_map.py."""
import math
from PIL import Image, ImageDraw
W, H = 80, 64

def rect(x,y,w,h):
 return {(xx,yy) for yy in range(y,y+h) for xx in range(x,x+w)
         if 0<=xx<W and 0<=yy<H}

def polygon(points):
 im=Image.new('1',(W,H));ImageDraw.Draw(im).polygon(points,fill=1)
 return {(x,y) for y in range(H) for x in range(W) if im.getpixel((x,y))}

def blob(cx,cy,rx,ry,seed=0):
 out=set()
 for y in range(max(0,int(cy-ry-2)),min(H,int(cy+ry+3))):
  for x in range(max(0,int(cx-rx-2)),min(W,int(cx+rx+3))):
   angle=math.atan2((y-cy)/ry,(x-cx)/rx)
   radius=1+.07*math.sin(angle*3+seed)+.04*math.cos(angle*5-seed)
   if ((x-cx)/rx)**2+((y-cy)/ry)**2<radius**2:out.add((x,y))
 return out

def path(points,width=2):
 out=set()
 for (ax,ay),(bx,by) in zip(points,points[1:]):
  steps=max(abs(bx-ax),abs(by-ay))
  for i in range(steps+1):
   out|=rect(round(ax+(bx-ax)*i/max(1,steps)),round(ay+(by-ay)*i/max(1,steps)),width,width)
 return out

# Northern escarpment and eastern headland form a stepped horseshoe.
north=polygon([(0,0),(79,0),(79,14),(76,14),(75,16),(72,17),
 (66,17),(63,16),(60,15),(57,12),(54,10),(50,10),(47,11),(44,12),
 (42,14),(40,16),(37,16),(36,14),(31,14),(29,13),(25,13),
 (23,11),(22,9),(18,8),(14,8),(11,9),(9,12),(7,13),(5,12),
 (3,10),(0,9)])
east=polygon([(57,14),(62,15),(66,17),(72,17),(76,15),(79,14),
 (79,32),(77,34),(75,35),(72,36),(69,36),(67,35),(64,35),
 (63,33),(60,33),(59,30),(57,29),(57,26),(54,26),(53,24),
 (51,24),(50,22),(46,22),(44,20),(42,18),(42,16),(46,14),(51,13)])
bluff=polygon([(9,10),(13,9),(19,9),(21,10),(22,12),(23,14),
 (23,18),(21,20),(18,20),(16,21),(11,21),(9,20),(8,17),(8,13)])
cliffs=north|east|bluff
terrace=polygon([(0,0),(79,0),(79,5),(74,5),(72,6),(65,6),
 (61,5),(54,5),(51,4),(45,4),(42,5),(35,5),(31,4),(27,4),
 (25,5),(20,5),(17,6),(13,6),(10,7),(5,7),(3,6),(0,6)])

beach=(blob(20,29,19,13,1)|blob(22,37,13,10,2)
       |blob(43,30,17,9,3)|blob(60,26,11,8,4)
       |blob(39,38,9,6,4))-cliffs
pools=blob(6,35,2,2,1)|blob(36,38,2,2,2)|blob(29,46,3,1.5,3)
lagoon=polygon([(38,19),(41,18),(44,19),(46,21),(51,23),(55,24),
 (54,26),(51,27),(47,26),(44,25),(41,24),(39,23),(37,22)])
beach-=pools|lagoon
# Coastal Road joins the west; Harbor Road still joins the east.
west_route=path([(0,26),(6,26),(10,28)],3)
east_route=path([(55,28),(60,29),(70,29),(74,27),(79,27)],2)
beach|=west_route|east_route
cliffs-=east_route

buildings=[('lodge',12,9),('center',23,18),('house_blue',8,24),
 ('house_green',20,24),('house_gold',32,24),('house_green',40,35),
 ('house_green',10,36),('house_gold',24,36),('lighthouse',67,37)]
for name,x,y in buildings:
 if name in ['lighthouse','lodge']:continue
 beach|=rect(x,y,7 if name!='center' else 6,7)
 pools-=rect(x,y,7,7);cliffs-=rect(x,y,7,7)

grass=(polygon([(4,24),(8,21),(17,22),(20,20),(30,21),(39,24),
                (40,33),(46,34),(47,42),(33,44),(28,47),
                (10,45),(4,39)])
       |blob(13,15,7,5,3)|blob(39,5,6,2,4)
       |blob(66,11,6,3,5)|blob(74,29,4,3,6))
grass&=beach|cliffs
# Smaller coastal turf patches leave the exposed northern rock readable.
grass|=(blob(8,4,7,2,2)|blob(30,7,5,2,3)|blob(54,7,5,2,1))&cliffs
stairs=rect(20,17,2,6)
# Each house gets a short landing rather than an unattached wooden rectangle.
decks=set().union(*(rect(x+2,y+6,3,1) for name,x,y in buildings
                    if name.startswith('house_')))
lighthouse_island=blob(69,42,5,5,1)
decks|=rect(65,43,8,3)|rect(67,46,2,8)|rect(64,54,8,3)
beach|=lighthouse_island
reefs=(blob(11,47,7,3,1)|blob(20,51,7,3,2)|blob(32,53,9,3,3)
       |blob(43,55,6,3,4)|blob(51,50,6,3,5)|blob(59,51,5,3,6))
reef_route=path([(22,44),(22,47),(28,50),(36,52),(44,53),
                 (51,50),(58,50),(62,47),(67,45)],2)
beach|=reefs|reef_route
cave_origin=(65,23);cave_approach=(65,24)
cave_court=polygon([(64,24),(66,24),(68,26),(68,28),(65,30),
                    (61,30),(61,28),(63,26)])
beach|=cave_court;cliffs-=cave_court
palms=[(6,21),(10,16),(28,9),(39,11),(49,19),(58,13),
 (70,17),(75,22),(55,29),(4,29),(18,35),(17,38),
 (20,41),(31,36),(47,34),(70,40)]
rocks=[(3,5),(17,3),(34,4),(48,3),(61,6),(73,7),(53,18),
 (59,24),(6,35),(47,36),(28,44),(10,45),(40,48),
 (54,44),(73,44),(59,57),(25,58)]
# Short, worn village paths: sand still separates the houses and tide pools.
village_paths=(path([(0,26),(5,26),(5,32),(38,32)],3)
 |path([(26,22),(26,32)],2)
 |path([(23,33),(23,43),(43,43),(43,41)],2)
 |path([(13,43),(23,43)],2))
for name,x,y in buildings:
 if name.startswith('house_'):
  village_paths|=path([(x+3,y+6),(x+3,32 if y==24 else 43)],2)
lamps=[(17,29),(30,29),(8,34),(28,34),(37,43),(65,44)]
flowerbeds=[(8,22),(17,24),(29,24),(38,29),(10,34),(30,40),(45,42)]
sea_rocks=[(48,40),(58,44),(36,46),(59,57)]
reef_gardens=[(10,47,5,2),(20,51,5,2),(32,53,6,2),
              (44,55,4,2),(52,50,4,2),(59,51,3,2)]
landmarks={'center_door':[26,21],'west_exit':[0,26],
 'east_exit':[79,27],'lighthouse_approach':[68,44],
 'arrival_pier':[68,55],'cave_approach':list(cave_approach),
 'reef_walk':[44,53]}
