"""Corvala: west village, east cliff/cave, south tidal reefs.

Height bands are artwork/navigation authoring data: 0=low-only, 1=mid-exposed,
2=always dry. The game still loads LOW until a runtime tide controller is added.
"""
import math
W,H=56,60
def rect(x,y,w,h):return {(xx,yy) for yy in range(y,y+h) for xx in range(x,x+w)}
def blob(cx,cy,rx,ry,seed=0):
 out=set()
 for y in range(max(0,int(cy-ry-2)),min(H,int(cy+ry+3))):
  for x in range(max(0,int(cx-rx-2)),min(W,int(cx+rx+3))):
   angle=math.atan2((y-cy)/ry,(x-cx)/rx);r=1+.12*math.sin(angle*3+seed)+.07*math.cos(angle*5-seed)
   if ((x-cx)/rx)**2+((y-cy)/ry)**2<r*r:out.add((x,y))
 return out
def path(points,width=2):
 out=set()
 for (ax,ay),(bx,by) in zip(points,points[1:]):
  count=max(abs(bx-ax),abs(by-ay))
  for i in range(count+1):
   x=round(ax+(bx-ax)*i/max(1,count));y=round(ay+(by-ay)*i/max(1,count));out|=rect(x,y,width,width)
 return out
buildings=[('lodge',6,4),('house_green',4,21),('house_blue',14,17),('center',25,14),('house_green',32,21),('house_gold',37,29),('house_green',17,33),('house_gold',27,33),('lighthouse',49,34)]
platform_rects=[(3,21,9,8),(13,17,9,8),(24,14,8,7),(31,21,9,8),(36,29,9,8),(16,33,9,8),(26,33,9,8),(42,40,10,4),(44,54,9,5)]
decks=set().union(*(rect(*r) for r in platform_rects))
bridge_rects=[(11,20,3,8),(9,26,10,3),(17,23,3,6),(19,23,11,3),(27,20,3,10),(28,26,8,3),(24,24,3,17),(22,39,8,3),(33,27,3,11),(33,35,8,3),(38,35,3,5),(39,37,10,3),(47,38,3,19)]
bridge_rects=[(x,y,2 if w==3 else w,2 if h==3 else h) for x,y,w,h in bridge_rects]
decks|=set().union(*(rect(*r) for r in bridge_rects))
# A permanent exposed path connects the two existing map seams and cliff-side landing.
permanent=path([(10,0),(10,2),(16,2),(16,12),(25,12)],3)
permanent|=path([(53,11),(53,42),(48,42)],3)|rect(51,10,5,3)
# Prominent eastern headland: irregular west face and tapering southern spur.
cliffs=set()
for y in range(36):
 left=39+([0,0,1,2,1,1,2,3,3,4,3,4][y%12] if y<18 else 4+(y-18)//5)
 cliffs|=rect(left,y,W-left,1)
# Northern bluff and western rock stacks frame, rather than close off, the bay.
cliffs|=set().union(*(blob(*r) for r in [(8,6,12,8,1),(28,3,13,6,2),(1,22,3,12,3)]))
# Isolated stone base supports the lighthouse above the waterline.
lighthouse=blob(52,39,5,5,4)
heights={p:2 for p in permanent|lighthouse}
# Narrow, irregular upper beaches; the lagoon itself remains water even at LOW.
upper=blob(8,22,7,12,2)|blob(22,17,10,5,3)|blob(35,27,6,6,4)
for p in upper:heights.setdefault(p,1)
low=blob(9,31,7,8,1)|blob(23,27,9,5,2)|blob(34,35,5,5,3)
for p in low:heights.setdefault(p,0)
# Uneven reef shelves merge into the coast; no rectangular coral allotments.
reefs=set().union(*(blob(*r) for r in [(7,41,6,5,0),(12,43,5,4,1),(6,47,4,3,2),(15,52,6,3,3),(21,50,6,4,1),(27,46,5,5,4),(35,52,4,3,2),(39,47,3,4,5)]))
for x,y in reefs:heights.setdefault((x,y),1 if (x*7+y*3)%13<3 else 0)
# Low-tide walking route threads the pools and a reef shelf.
reef_route=path([(9,33),(9,39),(13,44),(19,47),(23,47)],2)
for p in reef_route:heights[p]=0
# A higher pool lookout stays exposed at MID, but floods at HIGH.
mid_route=path([(8,28),(7,33),(7,35)],2)
for p in mid_route:heights[p]=1
# Cave threshold is cut into the eastern headland, approached only at LOW tide.
cave_origin=(46,17);cave_approach=(47,20)
cave_route=path([(39,27),(41,25),(44,23),(47,20)],2)
for p in cave_route:heights[p]=0
cave_court=rect(46,20,4,3)
for p in cave_court:heights[p]=0
cliffs-=cave_route|cave_court
# Pools interrupt the sand; use native shallow-water behavior when exposed.
pools=blob(8,33,2,2,0)|blob(19,27,3,2,1)|blob(13,40,2,2,2)|blob(31,35,2,2,3)
pools-=reef_route|mid_route|cave_route
for p in pools:heights.pop(p,None)
landmarks={'center_door':[28,18],'north_exit':[11,0],'east_exit':[55,11],'lighthouse_approach':[49,42],'arrival_pier':[48,56]}
tidal_goals={'cave_approach':list(cave_approach),'reef_walk':[23,47],'pool_lookout':[7,35]}
