"""Native FireRed house geometry/materials, fitted to Corvala's timber palettes.

Sources are the existing repository maps and their original tilesets. No image
scaling, smoothing or outside asset imports. The seven-tile-wide adaptation
repeats native center columns; doors/windows/eaves remain at 1x pixel scale.
"""
from pathlib import Path
from collections import deque
import json,struct
from PIL import Image,ImageDraw
import art
SOURCES={
 'pallet':('PalletTown','pallet_town',(5,3,5,5),1),
 'cerulean':('CeruleanCity','cerulean_city',(13,14,7,4),2),
 'sevii':('OneIsland','sevii_islands_123',(18,6,5,4),1),
}
def original(root,name,atlas):
 town,secondary,rect,door=SOURCES[name];x,y,w,h=rect
 lyt=json.loads((root/'data/layouts/layouts.json').read_text())['layouts'];m=json.loads((root/f'data/maps/{town}/map.json').read_text());l=next(l for l in lyt if l['id']==m['layout'])
 blocks=struct.unpack('<'+'H'*(l['width']*l['height']),(root/l['blockdata_filepath']).read_bytes());tiles=atlas(secondary)
 out=Image.new('RGB',(w*16,h*16));grid=[]
 for yy in range(h):
  row=[]
  for xx in range(w):
   mid=blocks[(y+yy)*l['width']+x+xx]&1023;out.paste(tiles[mid],(xx*16,yy*16));row.append(mid)
  grid.append(row)
 return out,grid

def transparent_ground(image):
 # Only connected exterior grass is removed. Green interior door frames stay.
 w,h=image.size;seen=set();q=deque()
 def ground(x,y):
  r,g,b=image.getpixel((x,y));return g>r*1.10 and g>b*1.06
 for x in range(w):
  for y in [0,h-1]:
   if ground(x,y):q.append((x,y));seen.add((x,y))
 for y in range(h):
  for x in [0,w-1]:
   if ground(x,y):q.append((x,y));seen.add((x,y))
 while q:
  x,y=q.popleft()
  for xx,yy in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
   if 0<=xx<w and 0<=yy<h and (xx,yy) not in seen and ground(xx,yy):seen.add((xx,yy));q.append((xx,yy))
 return seen

def native_house(root,name,atlas):
 original_image,grid=original(root,name,atlas);w,h=original_image.size;ground=transparent_ground(original_image)
 indexed=Image.new('P',(w,h));colors=art.PALETTES[0]
 silhouette=Image.new('1',(w,h));sd=ImageDraw.Draw(silhouette)
 if name=='pallet':sd.polygon([(12,0),(w-13,0),(w-1,7),(w-1,32),(w-4,35),(w-4,h-1),(3,h-1),(3,35),(0,32),(0,7)],fill=1)
 elif name=='cerulean':sd.polygon([(10,8),(w-11,8),(w-1,14),(w-1,h-1),(0,h-1),(0,14)],fill=1)
 else:sd.rectangle((0,8,w-1,h-1),fill=1)
 for y in range(h):
  for x in range(w):
   if (x,y) in ground or not silhouette.getpixel((x,y)):continue
   r,g,b=original_image.getpixel((x,y));brightness=(r*3+g*6+b)//10
   if y<32:
    # Preserve native ridge/shingle/eave pixel clusters, recoloring only roof materials.
    if (r,g,b)==(65,74,106):index=1
    elif name=='sevii':index=9 if brightness<105 else 10 if brightness<170 else 11
    else:index=8 if brightness<135 else 9 if brightness<165 else 10 if brightness<200 else 11
   elif b-r>60 and b-g>25:
    # Glass remains blue-grey independent of the roof-color bank.
    index=8 if brightness<100 else 9 if brightness<160 else 10 if brightness<210 else 11
   else:
    index=min([1,2,3,4,5,6,7,14],key=lambda i:sum((v-c)**2 for v,c in zip((r,g,b),colors[i])))
   indexed.putpixel((x,y),index)
 # Repeat central metatile columns, rather than stretching native details.
 columns=[0,1,2,2,2,3,4] if w==80 else list(range(7))
 wide=Image.new('P',(112,h))
 for x,col in enumerate(columns):wide.paste(indexed.crop((col*16,0,col*16+16,h)),(x*16,0))
 out=Image.new('P',(112,96));out.paste(wide,(0,96-h))
 # Small porch contact shadow; no drawing over imported doors or windows.
 d=ImageDraw.Draw(out);d.line((7,95,104,95),fill=2)
 return out,{'source_map':SOURCES[name][0],'secondary_tileset':SOURCES[name][1],'source_rectangle':SOURCES[name][2],'source_metatiles':grid,'door_column':SOURCES[name][3],'door_row':5,'wall_start_row':3 if name=='pallet' else 4}

def kit(root,atlas):
 art.PALETTES[0]=[(0,0,0),(56,56,56),(88,64,48),(120,80,56),(152,104,64),(184,136,88),(208,168,112),(232,200,144),(48,72,104),(80,136,176),(136,192,216),(208,232,240),(176,200,184),(216,216,184),(24,40,56),(240,224,176)]
 out={};provenance={}
 for name in SOURCES:out[name],provenance[name]=native_house(root,name,atlas)
 return out,provenance
