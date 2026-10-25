#!/usr/bin/env python3
"""Build Vidra with FireRed's native map palette, town tile and UI controls.

Campaign section IDs are optional: QOL can carry the shared UI/art without
adding island story maps, rewards or travel flags. Existing names are preserved.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json, struct
import numpy as np
from scipy.ndimage import distance_transform_edt
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'graphics/region_map'
base = Image.open(OUT / 'region_map.png')
COLORS = [tuple(map(int, row.split())) for row in (OUT/'region_map.pal').read_text().splitlines()[3:]]
# FireRed uses flat contour bands and horizontal ocean stripes, rather than a
# separately styled miniature painting. Keep the accepted island geography.
mask = Image.new('1', (176,120)); md = ImageDraw.Draw(mask)
md.polygon([(14,80),(18,47),(26,23),(42,15),(58,12),(73,5),(109,5),
 (135,15),(150,28),(159,48),(156,65),(166,80),(165,106),(148,114),
 (122,111),(108,102),(89,103),(78,97),(61,103),(42,96),(27,94)], fill=1)
land = np.array(mask,dtype=bool)
depth = distance_transform_edt(land)
y,x = np.mgrid[:120,:176]
# Shore and mountain contours reuse Kanto's exact greens/yellows.
height = (np.exp(-(((x-88)/45)**2+((y-28)/24)**2))*5.2
 + np.exp(-(((x-51)/27)**2+((y-60)/36)**2))*2.6
 + np.exp(-(((x-139)/20)**2+((y-91)/25)**2))*2.7)
levels = np.clip((height + np.minimum(depth,12)/9).astype(int),0,6)
arr = np.where((y%2)==0,14,15).astype(np.uint8)
land_colors = np.array([1,2,3,4,5,9,10],dtype=np.uint8)
arr[land] = land_colors[levels[land]]
# Eastern lake, with a small land bridge at its town on the southern shore.
lake = ((x-120)/19)**2+((y-49)/13)**2 < 1
arr[lake] = np.where((y[lake]%2)==0,14,15)
im=Image.fromarray(arr); im.putpalette(sum((list(c) for c in COLORS),[])+[0]*(768-len(COLORS)*3))
d=ImageDraw.Draw(im)
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
 pix=[(x*8+4,y*8+4) for x,y in points];d.line(pix,fill=7,width=5);d.line(pix,fill=8,width=3)
 for x,y in points:sections[y][x]='MAPSEC_QUANTUM_'+ident
 xs=[x for x,y in points];ys=[y for x,y in points]
 metadata.append(dict(id='MAPSEC_QUANTUM_'+ident,name=name,x=min(xs),y=min(ys),width=max(xs)-min(xs)+1,height=max(ys)-min(ys)+1))
towns=[(15,12,'PORT_CITY','HAVORA CITY'),(4,10,'COASTAL_CITY','COASTAL CITY'),
       (6,7,'FOREST_TOWN','FOREST TOWN'),(14,7,'LAKE_TOWN','LAKE TOWN'),(10,2,'SNOW_TOWN','SNOW TOWN')]
for x,y,ident,name in towns:
 pass # Native city tile is assigned below.
 sections[y][x]='MAPSEC_QUANTUM_'+ident
 metadata.append(dict(id='MAPSEC_QUANTUM_'+ident,name=name,x=x,y=y,width=1,height=1))
# Hot springs: warm pools next to the snow settlement, separate named map area.
x,y=13,2;cx,cy=x*8+4,y*8+4;d.rectangle((cx-2,cy-2,cx+2,cy+2),fill=10);d.rectangle((cx-1,cy-1,cx+1,cy+1),fill=7);d.point((cx,cy),fill=9)
sections[y][x]='MAPSEC_QUANTUM_HOT_SPRINGS';metadata.append(dict(id='MAPSEC_QUANTUM_HOT_SPRINGS',name='HOT SPRINGS',x=x,y=y,width=1,height=1))
# Every town uses the same native eight-pixel red/gold marker as Kanto. Its
# palette bank is assigned per tile, keeping original map colors byte-exact.
for tx,ty,_,_ in towns:
 im.paste(base.crop((8,0,16,8)),(tx*8,ty*8))
im.save(OUT/'quantum_map.png',bits=4)

def tile_bytes(image,x,y):
 pix=list(image.crop((x,y,x+8,y+8)).get_flattened_data())
 return bytes((pix[i]&15)|((pix[i+1]&15)<<4) for i in range(0,64,2))
old=bytearray()
for y in range(0,base.height,8):
 for x in range(0,base.width,8):old.extend(tile_bytes(base,x,y))
lookup={};tiles=[]
def register(b,index):
 a=np.array([[((b[y*4+x//2]>>(4*(x%2)))&15) for x in range(8)] for y in range(8)],dtype=np.uint8)
 for h,v,f in ((False,False,0),(True,False,0x400),(False,True,0x800),(True,True,0xc00)):
  t=a[::-1] if v else a
  if h:t=t[:,::-1]
  raw=bytes(t[:,::2].reshape(-1)|(t[:,1::2].reshape(-1)<<4))
  lookup.setdefault(raw,index|f)
for i in range(len(old)//32):register(bytes(old[i*32:i*32+32]),i)
def intern(b):
 if b not in lookup:
  register(b,320+len(tiles));tiles.append(b)
 return lookup[b]
original=list(struct.unpack('<600H',(OUT/'kanto.bin').read_bytes()))
# Preserve Kanto's transparent margins and top two rows so the shared native
# frame and blue header remain visible beneath BG0 on both Town and Fly maps.
mapbuf=original.copy()
# Replace all of the map viewport, including the non-selectable sea fringe.
for y in range(2,20):
 for x in range(3,27):mapbuf[y*30+x]=3
for y in range(15):
 for x in range(22):
  mapbuf[(y+4)*30+x+4]=intern(tile_bytes(im,x*8,y*8))
for tx,ty,_,_ in towns:mapbuf[(ty+4)*30+tx+4]=0x1001
for y in range(20):
 for x in range(30):
  if 24<=x<=26 and 14<=y<=18:mapbuf[y*30+x]=original[y*30+x]
assert len(tiles)<=192,('BG0 tile overflow',len(tiles))
(OUT/'quantum_atlas.bin').write_bytes(old+b''.join(tiles))
(OUT/'quantum_map.bin').write_bytes(struct.pack('<600H',*mapbuf))
# Exactly two region choices. UI row indices are independent of old page IDs.
menu=Image.new('P',(240,160));menu.putpalette(im.getpalette());md=ImageDraw.Draw(menu)
font=ImageFont.load_default(size=9)
for i,label in enumerate(('KANTO','VIDRA')):
 yy=48+i*32;md.rectangle((72,yy,167,yy+31),fill=7);md.rectangle((74,yy+2,165,yy+29),fill=10)
 box=md.textbbox((0,0),label,font=font)
 md.text((72+(96-box[2]+box[0])//2,yy+10),label,font=font,fill=1)
mt=[bytes(32)];ml={mt[0]:0};mb=[]
for y in range(20):
 for x in range(30):
  b=tile_bytes(menu,x*8,y*8)
  if b not in ml:ml[b]=len(mt);mt.append(b)
  mb.append(ml[b])
assert len(mt)<=128
(OUT/'quantum_switch_tiles.bin').write_bytes(b''.join(mt).ljust(4096,b'\0'))
(OUT/'quantum_switch.bin').write_bytes(struct.pack('<600H',*mb))
header='static const u8 sRegionMapSections_Quantum[2][MAP_HEIGHT][MAP_WIDTH] = {\n [LAYER_MAP] = {\n'
header+=''.join('  {'+', '.join(row)+'},\n' for row in sections)+' },\n [LAYER_DUNGEON] = {\n'
header+=''.join('  {'+', '.join(['MAPSEC_NONE']*22)+'},\n' for _ in range(15))+' }\n};\n'
(ROOT/'src/data/region_map/region_map_layout_quantum.h').write_text(header)
# Preserve authored names if the campaign already has them. QOL has no island
# section IDs yet; the generator must not append them or change existing IDs.
metadata_path=ROOT/'src/data/region_map/region_map_sections.json'
data=json.loads(metadata_path.read_text());by_id={e['id']:e for e in data['map_sections']}
for entry in metadata:
 if entry['id'] in by_id:
  entry['name']=by_id[entry['id']]['name']
  by_id[entry['id']].update(entry)
updated=json.dumps(data,indent=2)+'\n'
if any(e['id'] in by_id for e in metadata) and updated!=metadata_path.read_text():metadata_path.write_text(updated)
(ROOT/'tools/quantum_region/locations.json').write_text(json.dumps(metadata,indent=2)+'\n')
print('Vidra native map:',len(tiles),'new tiles;',len(old)+len(tiles)*32,'atlas bytes')
