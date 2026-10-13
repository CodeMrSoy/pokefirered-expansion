#!/usr/bin/env python3
"""Build the island's native 4bpp atlas, tilemaps and selectable map sections."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json, struct
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'graphics/region_map'
COLORS = [(0,0,0),(32,104,176),(64,152,208),(112,200,224),(224,208,144),
          (112,176,96),(64,136,72),(40,96,64),(80,88,112),(136,144,160),
          (232,240,248),(176,216,240),(216,88,72),(248,160,88),(248,224,144),(248,248,248)]
im = Image.new('P',(176,120),1);im.putpalette(sum((list(c) for c in COLORS),[])+[0]*720)
d = ImageDraw.Draw(im)
land = [(32,20),(48,12),(64,8),(80,3),(112,6),(132,14),(146,28),(152,44),
        (145,64),(157,78),(149,103),(128,112),(106,105),(91,100),(67,99),
        (49,105),(28,91),(20,74),(22,48)]
d.polygon(land,fill=3);d.polygon([(x,y-2) for x,y in land],fill=4)
d.polygon([(x+(1 if x<90 else -1),y-3) for x,y in land],fill=5)
# Mountain spine, snowy summit and lower forest. Sparse deterministic texture.
d.polygon([(49,30),(65,13),(81,9),(101,10),(120,20),(138,34),(127,47),(103,35),(84,43),(64,38)],fill=8)
d.polygon([(55,30),(68,17),(77,25),(86,11),(102,24),(115,17),(128,33),(115,30),(106,31),(92,24),(80,35)],fill=9)
d.polygon([(63,24),(70,14),(77,22),(85,7),(94,19),(105,16),(118,24),(115,31),(101,28),(84,30),(76,28)],fill=10)
for x,y in [(39,38),(47,37),(54,42),(31,55),(39,53),(49,52),(56,57),(67,48),(75,58),
            (29,65),(42,65),(52,66),(63,70),(69,81),(77,84),(120,45),(131,46),(137,52),(139,71),(131,83)]:
 d.rectangle((x-2,y-1,x+2,y+2),fill=7);d.polygon([(x,y-4),(x-3,y),(x+3,y)],fill=6)
# Lake, meltwater, river, waterfall and southeastern sheltered harbor.
d.ellipse((99,43,133,67),fill=3);d.ellipse((101,45,131,65),fill=2)
d.line([(113,29),(113,37),(120,41),(119,48)],fill=11,width=3)
d.line([(61,37),(54,47),(50,56),(56,68),(65,74),(76,91),(101,102)],fill=3,width=3)
d.line([(65,72),(66,76)],fill=15,width=3)
d.ellipse((131,89,159,111),fill=3);d.ellipse((133,90,159,110),fill=1)
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
 pix=[(x*8+4,y*8+4) for x,y in points];d.line(pix,fill=8,width=3);d.line(pix,fill=14,width=1)
 for x,y in points:sections[y][x]='MAPSEC_QUANTUM_'+ident
 xs=[x for x,y in points];ys=[y for x,y in points]
 metadata.append(dict(id='MAPSEC_QUANTUM_'+ident,name=name,x=min(xs),y=min(ys),width=max(xs)-min(xs)+1,height=max(ys)-min(ys)+1))
towns=[(15,12,'PORT_CITY','PORT CITY'),(4,10,'COASTAL_CITY','COASTAL CITY'),
       (6,7,'FOREST_TOWN','FOREST TOWN'),(14,7,'LAKE_TOWN','LAKE TOWN'),(10,2,'SNOW_TOWN','SNOW TOWN')]
# Port's built-up district, piers and market/daycare symbols, around one Fly cell.
d.rectangle((110,86,129,105),fill=9);d.rectangle((111,87,128,104),fill=10)
for x,y in [(112,88),(118,88),(124,88),(112,96)]:d.rectangle((x,y,x+3,y+3),fill=12)
for x in (130,137,145):d.line([(x,101),(x,111)],fill=9,width=2)
d.rectangle((123,82,129,86),fill=6) # daycare garden
for x,y,ident,name in towns:
 cx,cy=x*8+4,y*8+4;d.rectangle((cx-3,cy-3,cx+3,cy+3),fill=8);d.rectangle((cx-2,cy-2,cx+2,cy+2),fill=12);d.point((cx-1,cy-1),fill=15)
 sections[y][x]='MAPSEC_QUANTUM_'+ident
 metadata.append(dict(id='MAPSEC_QUANTUM_'+ident,name=name,x=x,y=y,width=1,height=1))
# Hot springs: warm pools next to the snow settlement, separate named map area.
x,y=13,2;cx,cy=x*8+4,y*8+4;d.ellipse((cx-3,cy-2,cx+3,cy+2),fill=8);d.ellipse((cx-2,cy-1,cx+2,cy+1),fill=3);d.point((cx,cy-3),fill=15)
sections[y][x]='MAPSEC_QUANTUM_HOT_SPRINGS';metadata.append(dict(id='MAPSEC_QUANTUM_HOT_SPRINGS',name='HOT SPRINGS',x=x,y=y,width=1,height=1))
# Ocean waves avoid land and add a small sense of scale.
for y in range(4,120,16):
 for x in range(4,176,24):
  if all(im.getpixel((x+k,y))==1 for k in range(4)):d.line((x,y,x+3,y),fill=2)
im.save(OUT/'quantum_map.png')
# Native tile packing, deduplication and a hard BG0 16-KiB boundary.
def tile_bytes(image,x,y):
 pix=[v & 15 for v in image.crop((x,y,x+8,y+8)).get_flattened_data()];return bytes(pix[i] | pix[i+1]<<4 for i in range(0,64,2))
base=Image.open(OUT/'region_map.png');old=bytearray()
for y in range(0,base.height,8):
 for x in range(0,base.width,8):old.extend(tile_bytes(base,x,y))
tiles=[];lookup={};original=list(struct.unpack('<600H',(OUT/'kanto.bin').read_bytes()));mapbuf=original.copy()
for y in range(15):
 for x in range(22):
  b=tile_bytes(im,x*8,y*8)
  if b not in lookup:lookup[b]=320+len(tiles);tiles.append(b)
  if not (x >= 20 and y in (12,13,14)):
   mapbuf[(y+4)*30+(x+4)] = lookup[b] | 5<<12
# Fill outside the new island with its own ocean; preserve only the UI buttons.
ocean = bytes([0x11]*32)
if ocean not in lookup:
 lookup[ocean]=320+len(tiles);tiles.append(ocean)
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
   if t not in lookup:lookup[t]=320+len(tiles);tiles.append(t)
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
