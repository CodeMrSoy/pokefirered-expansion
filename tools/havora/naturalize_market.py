#!/usr/bin/env python3
"""Second, uncommitted market composition pass. Run after design_city_review.py."""
import json,struct,subprocess,copy
from pathlib import Path
R=Path(__file__).resolve().parents[2]
def js(p):return json.loads((R/p).read_text())
def ww(b):return list(struct.unpack('<'+'H'*(len(b)//2),b))
l=next(l for l in js('data/layouts/layouts.json')['layouts'] if l['name']=='Havora_Market_Layout');v=ww((R/l['blockdata_filepath']).read_bytes());before=v[:];w=l['width'];m=js('data/maps/Havora_Market/map.json');coast=set()
def tile(x,y,mid,solid=False,elev=None):
 i=y*w+x;v[i]=((v[i]&0xf000) if elev is None else elev<<12)|(1024 if solid else 0)|mid

def rect(x,y,ww,hh,mid,solid=False):
 for yy in range(y,y+hh):
  for xx in range(x,x+ww):tile(xx,yy,mid,solid)
def piece(x,y,grid,mask=None):
 for j,row in enumerate(grid):
  for i,mid in enumerate(row):tile(x+i,y+j,mid, bool(mask[j][i]) if mask is not None else True)
# Trading floor: stagger stalls and vary the edges instead of a paved rectangle.
rect(1,27,37,12,0)
rect(15,26,10,13,449);rect(3,31,32,2,449);rect(5,36,28,2,449)
positions=[(4,28),(10,29),(27,27),(33,29),(5,34),(11,35),(26,33),(31,34)]
stall=js('tools/havora/authoring-assets.json')['market_stall']
for x,y in positions:
 rect(x-1,y-1,5,5,640);piece(x,y,stall);tile(x+1,y+3,449)
# Thread two broad browsing paths through the clusters, leaving planted pockets.
rect(3,32,11,1,449);rect(26,31,10,1,449);rect(24,32,2,6,449)
for x,y in [(2,28),(8,27),(14,29),(3,35),(9,37),(25,28),(31,27),(36,33),(29,37)]:tile(x,y,3,True)
for x,y,count in [(2,37,3),(6,27,3),(12,38,2),(27,38,3),(35,36,2)]:
 for i in range(count):tile(x+i,y,2,True)
piece(18,31,[[173],[488]])
# Fountain stays accessible but sits slightly off the visual axis.
rect(19,18,3,4,449);f=js('tools/havora/fountain.json');piece(18,18,f['kits']['paving'],f['collision_mask'])
# Small green cuts soften the department store forecourt, never its doors.
for x,y in [(26,43),(26,44),(26,45),(37,43),(37,44),(36,55),(37,55),(26,55)]:tile(x,y,0)
for x,y in [(26,44),(37,43),(36,55)]:tile(x,y,3,True)
# Borrow a complete native cliff diagonal from the authored western coast.
# This preserves FireRed's existing corner pieces rather than inventing bevels.
wl=next(l for l in js('data/layouts/layouts.json')['layouts'] if l['name']=='Havora_WestQuadrant_Layout');src=ww(subprocess.check_output(['git','show','ac291bc1:'+wl['blockdata_filepath']],cwd=R))
for yy in range(5):
 for xx in range(7):
  x,y=34+xx,35+yy;source=src[(45+yy)*wl['width']+20+xx];i=y*w+x
  # Plain source ground is a green clifftop pocket; cliff/water graphics and
  # their collision/elevation stay exactly as the native source stencil.
  if source&1023 in {0,4,5,449,640}:tile(x,y,0)
  else:v[i]=source
  coast.add((x,y))
# A narrow tidal inlet rounds into the shopping terrace below, then returns
# to the original eastern wall before the harbor seam.
for y in range(40,45):
 for x in range(38,41):tile(x,y,46 if x==38 else 642,x==38,3 if x==38 else 1);coast.add((x,y))
for y,row in [(45,[107,169,642]),(46,[0,46,642]),(47,[0,107,169]),(48,[0,44,46])]:
 for x,mid in zip(range(38,41),row):tile(x,y,mid,mid not in {0,642},1 if mid==642 else 3);coast.add((x,y))
# Outside the only unconnected edge is sea. All cardinal connections and their
# shared edge strips remain intact; the harbor and river layouts are untouched.
border=ww((R/l['border_filepath']).read_bytes());(R/l['border_filepath']).write_bytes(struct.pack('<'+'H'*len(border),*([0x1282]*len(border))))
vendors=[e for e in m['object_events'] if e['script']=='Havora_Market_Supplies']
for e,(x,y) in zip(vendors,positions):
 tile(x+1,y+3,449)
 e.update(x=x+1,y=y+3,movement_type='MOVEMENT_TYPE_FACE_UP',elevation=v[(y+3)*w+x+1]>>12)
# Keep shoppers clear of counters, the statue, flowers and the new inlet.
occupied={(e['x'],e['y']) for e in vendors};landing={(e['x'],e['y']+1) for e in m['warp_events']}
for e in m['object_events']:
 if e in vendors:continue
 x,y=e['x'],e['y'];options=[]
 for radius in range(12):
  for yy in range(max(0,y-radius),min(l['height'],y+radius+1)):
   for xx in range(max(0,x-radius),min(w,x+radius+1)):
    if abs(xx-x)+abs(yy-y)<=radius and v[yy*w+xx]&0xc00==0 and v[yy*w+xx]&1023!=642 and (xx,yy) not in occupied|landing:options.append((xx,yy))
  if options:break
 assert options
 xx,yy=min(options,key=lambda a:abs(a[0]-x)+abs(a[1]-y));e.update(x=xx,y=yy,elevation=v[yy*w+xx]>>12);occupied.add((xx,yy))
(R/l['blockdata_filepath']).write_bytes(struct.pack('<'+'H'*len(v),*v));(R/'data/maps/Havora_Market/map.json').write_text(json.dumps(m,indent=2)+'\n');(R/'tools/havora/market-naturalization.json').write_text(json.dumps({'uncommitted':True,'coast_edit_cells':sorted(coast),'stalls':positions,'fountain':[18,18],'native_cliff_stencil':'Havora_WestQuadrant (20,45) 7x5','market_border':'ocean beyond eastern coastline','source':'ac291bc1','modified_terrain_cells':sum(before[y*w+x]!=v[y*w+x] for x,y in coast)},indent=2)+'\n')
print('Staggered market and native cliff inlet written without commit.')
