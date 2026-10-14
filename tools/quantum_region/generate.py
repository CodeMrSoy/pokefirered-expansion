#!/usr/bin/env python3
"""Build the island's native 4bpp atlas, tilemaps and selectable map sections."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json, struct
import numpy as np
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'graphics/region_map'
COLORS = [(0,0,0),(115,189,247),(140,206,255),(24,90,41),
          (41,140,33),(82,181,41),(140,214,57),(115,123,115),
          (173,181,198),(247,247,239),(255,247,173),(255,222,82),
          (222,181,57),(231,41,24),(255,115,82),(66,57,33)]
im = Image.open(ROOT / 'tools/quantum_region/terrain.png').copy()
assert im.mode == 'P' and im.size == (176,120)
im.putpalette(sum((list(c) for c in COLORS),[])+[0]*720)
d = ImageDraw.Draw(im)
# Route centers share the exact selectable grid coordinates below.
segments = [([(4,10),(4,9),(5,9),(5,8),(6,8),(6,7)],'COASTAL_ROAD','COASTAL ROAD'),
 ([(6,7),(6,6),(7,6),(8,6),(8,5),(9,5),(9,4),(10,4)],'FOREST_PATH','FOREST PATH'),
 ([(10,4),(10,3),(10,2)],'MOUNTAIN_PASS','MOUNTAIN PASS'),
 ([(10,2),(11,2),(12,2),(13,2)],'SNOW_TRAIL','SNOW TRAIL'),
 ([(10,4),(11,4),(12,4),(13,4),(13,5),(14,5),(14,6),(14,7)],'LAKE_ROAD','LAKE ROAD'),
 ([(14,7),(14,8),(15,8),(15,9),(15,10),(15,11),(15,12)],'HARBOR_ROAD','HARBOR ROAD'),
 ([(4,10),(5,10),(6,10),(7,10),(8,10),(9,10),(10,11),(11,11),(12,11),(13,12),(14,12),(15,12)],'RIVER_ROAD','RIVER ROAD'),
 ([(6,7),(7,7),(8,7),(9,7),(10,7),(11,7),(12,7),(13,7),(14,7)],'WOODLAND_LINK','WOODLAND LINK')]
sections = [['MAPSEC_NONE']*22 for _ in range(15)];metadata=[]
for points,ident,name in segments:
 pix=[(x*8+4,y*8+4) for x,y in points];d.line(pix,fill=12,width=3);d.line(pix,fill=11,width=1)
 for x,y in points:sections[y][x]='MAPSEC_QUANTUM_'+ident
 xs=[x for x,y in points];ys=[y for x,y in points]
 metadata.append(dict(id='MAPSEC_QUANTUM_'+ident,name=name,x=min(xs),y=min(ys),width=max(xs)-min(xs)+1,height=max(ys)-min(ys)+1))
towns=[(15,12,'PORT_CITY','PORT CITY'),(4,10,'COASTAL_CITY','COASTAL CITY'),
       (6,7,'FOREST_TOWN','FOREST TOWN'),(14,7,'LAKE_TOWN','LAKE TOWN'),(10,2,'SNOW_TOWN','SNOW TOWN')]
for x,y,ident,name in towns:
 cx,cy=x*8+4,y*8+4;d.ellipse((cx-4,cy-4,cx+4,cy+4),fill=15);d.ellipse((cx-3,cy-3,cx+3,cy+3),fill=10);d.ellipse((cx-2,cy-2,cx+2,cy+2),fill=13);d.point((cx-1,cy-1),fill=14)
 sections[y][x]='MAPSEC_QUANTUM_'+ident
 metadata.append(dict(id='MAPSEC_QUANTUM_'+ident,name=name,x=x,y=y,width=1,height=1))
# Hot springs: warm pools next to the snow settlement, separate named map area.
x,y=13,2;cx,cy=x*8+4,y*8+4;d.rectangle((cx-2,cy-2,cx+2,cy+2),fill=10);d.rectangle((cx-1,cy-1,cx+1,cy+1),fill=7);d.point((cx,cy),fill=9)
sections[y][x]='MAPSEC_QUANTUM_HOT_SPRINGS';metadata.append(dict(id='MAPSEC_QUANTUM_HOT_SPRINGS',name='HOT SPRINGS',x=x,y=y,width=1,height=1))
# Planned caves and POIs are artwork markers only until their maps are registered.
# Existing town/Fly and hot-spring sections stay at their current V2 coordinates.
planned_pois = [(3,4,'Northwest Cave'),(9,5,'Mountain Cave'),(11,7,'Lake Cave'),
                (1,8,'West Coast Cave'),(2,11,'Lighthouse'),(16,10,'Daycare'),
                (17,12,'Southeast Cave')]
for x,y,label in planned_pois:
 cx,cy=x*8+4,y*8+4
 d.rectangle((cx-2,cy-2,cx+2,cy+2),fill=10)
 d.rectangle((cx-1,cy-1,cx+1,cy+1),fill=7)
 d.point((cx,cy),fill=9)
(ROOT/'tools/quantum_region/planned_pois.json').write_text(json.dumps([
 dict(name=label,x=x,y=y,registered_map_section=False) for x,y,label in planned_pois
],indent=2)+'\n')
# Merge the most similar terrain tiles to fit the existing VRAM allocation.
# Keep every route, town dot and POI tile exact, and never duplicate markers.
arr=np.array(im,dtype=np.uint8)
blocks=np.array([arr[y:y+8,x:x+8].reshape(64) for y in range(0,120,8) for x in range(0,176,8)])
patterns,inverse,counts=np.unique(blocks,axis=0,return_inverse=True,return_counts=True)
protected=np.isin(patterns,[11,12,13,14,15]).any(axis=1)
for px,py in [(13,2)]+[(x,y) for x,y,_ in planned_pois]:
 for yy in range(py*8+2,py*8+7):
  for xx in range(px*8+2,px*8+7):protected[inverse[(yy//8)*22+xx//8]]=True
colors=np.array(COLORS,dtype=np.float32)
rgb=colors[patterns]
# Strongly discourage moving shorelines and the snow biome.
classes=np.where(np.isin(patterns,[1,2]),1,np.where(np.isin(patterns,[8,9]),2,0))
dist=((rgb[:,None,:,:]-rgb[None,:,:,:])**2).sum(axis=(2,3))
dist+=(classes[:,None,:]!=classes[None,:,:]).sum(axis=2)*200000
np.fill_diagonal(dist,np.inf)
dist[:,protected]=np.inf
active=np.ones(len(patterns),dtype=bool);parent=np.arange(len(patterns))
while active.sum()>176:
 scores=dist.copy();scores[:,~active]=np.inf;scores[~active|protected,:]=np.inf
 scores*=counts[:,None]
 i,j=np.unravel_index(np.argmin(scores),scores.shape)
 if not np.isfinite(scores[i,j]):raise ValueError('Too many protected tiles')
 active[i]=False;parent[parent==i]=j;counts[j]+=counts[i]
for n,idx in enumerate(inverse):
 y=(n//22)*8;x=(n%22)*8
 arr[y:y+8,x:x+8]=patterns[parent[idx]].reshape(8,8)
assert all(np.array_equal(arr[(n//22)*8:(n//22)*8+8,(n%22)*8:(n%22)*8+8].reshape(64),blocks[n]) for n,idx in enumerate(inverse) if protected[idx])
im=Image.fromarray(arr);im.putpalette(sum((list(c) for c in COLORS),[])+[0]*720)
im.save(OUT/'quantum_map.png',bits=4)
# Native tile packing, deduplication and a hard BG0 16-KiB boundary.
def tile_bytes(image,x,y):
 pix=[v & 15 for v in image.crop((x,y,x+8,y+8)).get_flattened_data()];return bytes(pix[i] | pix[i+1]<<4 for i in range(0,64,2))
base=Image.open(OUT/'region_map.png');old=bytearray()
for y in range(0,base.height,8):
 for x in range(0,base.width,8):old.extend(tile_bytes(base,x,y))
# Reuse patterns, including GBA horizontal/vertical flip variants, across
# the original atlas and the new map. Original tiles and indices stay intact.
tiles=[];lookup={}
def register_tile(b, index):
 pixels=[[((b[y*4+x//2] >> (4*(x%2))) & 15) for x in range(8)] for y in range(8)]
 for h,v,flags in ((False,False,0),(True,False,0x400),(False,True,0x800),(True,True,0xc00)):
  rows=pixels[::-1] if v else pixels
  rows=[row[::-1] if h else row for row in rows]
  packed=bytes(row[x] | row[x+1]<<4 for row in rows for x in range(0,8,2))
  lookup.setdefault(packed,index|flags)
for i in range(len(old)//32):register_tile(bytes(old[i*32:i*32+32]),i)
def intern_tile(b):
 if b not in lookup:
  index=320+len(tiles);tiles.append(b);register_tile(b,index)
 return lookup[b]
original=list(struct.unpack('<600H',(OUT/'kanto.bin').read_bytes()));mapbuf=original.copy()
for y in range(15):
 for x in range(22):
  b=tile_bytes(im,x*8,y*8)
  intern_tile(b)
  if not (x >= 20 and y in (12,13,14)):
   mapbuf[(y+4)*30+(x+4)] = lookup[b] | 5<<12
# Fill outside the new island with its own ocean; preserve only the UI buttons.
ocean = bytes([0x11]*32)
if ocean not in lookup:
 intern_tile(ocean)
for y in range(20):
 for x in range(30):
  if not (4<=x<26 and 4<=y<19):mapbuf[y*30+x]=lookup[ocean]|5<<12
  if 24<=x<=26 and 16<=y<=18:mapbuf[y*30+x]=original[y*30+x]
# Native controls match this map's solid ocean rather than retaining old waves.
buttons=[]
for kind in range(2):
 button=Image.new('P',(24,24),1);bd=ImageDraw.Draw(button)
 bd.rectangle((2,2,21,21),fill=8)
 bd.rectangle((3,3,20,20),fill=14,outline=4)
 bd.rectangle((5,5,18,18),fill=10,outline=9)
 if kind==0:
  bd.rectangle((8,8,12,12),outline=9);bd.rectangle((10,10,14,14),outline=8)
 else:
  bd.polygon([(9,10),(9,14),(13,14),(13,12),(11,12),(11,10),(14,10),(14,8),(11,8),(11,8)],fill=8)
 rows=[]
 for yy in range(3):
  row=[]
  for xx in range(3):
   t=tile_bytes(button,xx*8,yy*8)
   intern_tile(t)
   row.append(lookup[t]|5<<12)
  rows.append(row)
 buttons.append(rows)
assert len(tiles)<=192,('BG0 tile overflow',len(tiles))
(OUT/'quantum_atlas.bin').write_bytes(old+b''.join(tiles))
(OUT/'quantum_map.bin').write_bytes(struct.pack('<600H',*mapbuf))
(OUT/'quantum_map.pal').write_text('JASC-PAL\n0100\n16\n'+''.join(f'{r} {g} {b}\n' for r,g,b in COLORS))
# Three-card region picker, using the same dedicated BG palette.
menu=Image.new('P',(240,160),0);menu.putpalette(im.getpalette());md=ImageDraw.Draw(menu);font=ImageFont.load_default(size=9)
for i,label in enumerate(('KANTO','SEVII ISLANDS','QUANTUM ISLAND')):
 yy=32+i*32;md.rectangle((72,yy,167,yy+31),fill=8);md.rectangle((74,yy+2,165,yy+29),fill=10)
 mask=Image.new('1',(96,32));draw=ImageDraw.Draw(mask);box=draw.textbbox((0,0),label,font=font);draw.text(((96-(box[2]-box[0]))//2,10),label,font=font,fill=1)
 menu.paste(8,(72,yy),mask)
mt=[bytes(32)];ml={mt[0]:0};mb=[]
for y in range(20):
 for x in range(30):
  b=tile_bytes(menu,x*8,y*8)
  if b not in ml:ml[b]=len(mt);mt.append(b)
  mb.append(ml[b]|5<<12)
assert len(mt)<=128
(OUT/'quantum_switch_tiles.bin').write_bytes(b''.join(mt).ljust(4096,b'\0'))
(OUT/'quantum_switch.bin').write_bytes(struct.pack('<600H',*mb))
# Cursor hit map and metadata feed the same names/positions as the artwork.
header='static const u8 sRegionMapSections_Quantum[2][MAP_HEIGHT][MAP_WIDTH] = {\n [LAYER_MAP] = {\n'
header+=''.join('  {'+', '.join(row)+'},\n' for row in sections)+' },\n [LAYER_DUNGEON] = {\n'
header+=''.join('  {'+', '.join(['MAPSEC_NONE']*22)+'},\n' for _ in range(15))+' }\n};\n'
header+='\nstatic const u16 sQuantumMapButtons[2][3][3] = {\n'+''.join(' {'+','.join('{'+','.join(hex(v) for v in row)+'}' for row in button)+'},\n' for button in buttons)+'};\n'
(ROOT/'src/data/region_map/region_map_layout_quantum.h').write_text(header)
(ROOT/'tools/quantum_region/locations.json').write_text(json.dumps(metadata,indent=2)+'\n')
# Keep location metadata and cursor geometry in sync without changing existing IDs.
metadata_path=ROOT/'src/data/region_map/region_map_sections.json'
if metadata_path.exists():
 data=json.loads(metadata_path.read_text())
 by_id={entry['id']:entry for entry in data['map_sections']}
 for entry in metadata:
  if entry['id'] not in by_id:raise ValueError('Register map-section ID before generating: '+entry['id'])
  by_id[entry['id']].update(entry)
 updated=json.dumps(data,indent=2)+'\n'
 if updated!=metadata_path.read_text():metadata_path.write_text(updated)
print('Quantum map:',len(tiles),'new tiles,',320+len(tiles),'total BG0 tiles;',len(metadata),'named locations')

