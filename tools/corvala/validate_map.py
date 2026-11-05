#!/usr/bin/env python3
"""Check actual packed GBA tiles, palette budgets, warp behavior and preview fidelity."""
from pathlib import Path
from collections import deque
import struct,json,sys
from PIL import Image,ImageChops
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'tools/havora'))
from render import atlas
manifest=json.loads((R/'tools/corvala/map.json').read_text());w,h=manifest['dimensions']
d=R/'data/tilesets/secondary/corvala';sheet=Image.open(d/'tiles.png')
assert sheet.mode=='P' and sheet.width==128
assert sheet.width*sheet.height//64<=384
metas=struct.unpack('<'+'H'*((d/'metatiles.bin').stat().st_size//2),(d/'metatiles.bin').read_bytes())
assert len(metas)%8==0 and len(metas)//8==manifest['metatiles']
for v in metas:
 assert (v&1023)<640+sheet.width*sheet.height//64
 assert 0<=v>>12<=12
for p in (d/'palettes').glob('*.pal'):
 rows=p.read_text().splitlines();assert rows[:3]==['JASC-PAL','0100','16'] and len(rows)==19
 colors=[list(map(int,row.split())) for row in rows[3:]]
 assert all(len(c)==3 and all(0<=v<=248 and v%8==0 for v in c) for c in colors)
ims=atlas('corvala');raw=(R/'data/layouts/Corvala_Town/map.bin').read_bytes();assert len(raw)==w*h*2
blocks=struct.unpack('<'+'H'*w*h,raw);out=Image.new('RGB',(w*16,h*16))
for i,v in enumerate(blocks):
 assert v&1023<len(ims)
 out.paste(ims[v&1023],(i%w*16,i//w*16))
ref=Image.open(R/'build/corvala/Corvala_Low_Tide_Map.png').convert('RGB')
assert ImageChops.difference(out,ref).getbbox() is None,'preview does not match packed tile flips/palettes'
# Confirm the moved Center uses the ordinary native animated door, with a return warp.
m=json.loads((R/'data/maps/Corvala_Town/map.json').read_text());door=m['warp_events'][0]
assert [door['x'],door['y']]==manifest['landmarks']['center_door']
assert blocks[door['y']*w+door['x']]&1023==0x62
assert door['elevation']==3 and door['dest_map']=='MAP_CORVALA_TOWN_POKEMON_CENTER_1_F'
interior=json.loads((R/'data/maps/Corvala_Town_PokemonCenter_1F/map.json').read_text())
assert interior['warp_events'][int(door['dest_warp_id'])]['dest_map']=='MAP_CORVALA_TOWN'
assert all(v['dest_warp_id']=='0' for v in interior['warp_events'] if v['dest_map']=='MAP_CORVALA_TOWN')
print('PASS: packed tile references, palette precision, tile budget, Center door and exact preview fidelity.')

# Primary references must remain live animated graphics, not copies in static secondary slots.
layout=next(l for l in json.loads((R/'data/layouts/layouts.json').read_text())['layouts'] if l['id']=='LAYOUT_CORVALA_TOWN')
assert layout['primary_tileset']=='gTileset_General'
assert [layout['width'],layout['height']]==[w,h]==[80,64]
assert layout['secondary_tileset']=='gTileset_Corvala'
assert (w+15)*(h+14)<=0x2800,'engine virtual map buffer exceeded'
assert (d/'metatile_attributes.bin').stat().st_size==manifest['metatiles']*4
headers=(R/'src/data/tilesets/headers.h').read_text().split('const struct Tileset gTileset_General =',1)[1].split('};',1)[0]
assert '.callback = InitTilesetAnim_General' in headers
shore_ids=set(manifest['shoreline']['generated_metatiles'])
assert shore_ids and any(v&1023 in shore_ids for v in blocks)
for mid in shore_ids:
 desc=metas[(mid-640)*8:(mid-640)*8+8]
 assert all(v&1023<640 for v in desc), 'shoreline flattened into secondary graphics'
 assert any(464<=v&1023<=481 for v in desc),'shoreline missing native surf animation reference'
assert manifest['kit']['sand']==0x115
print('PASS: native sand, live primary surf references, and General animation callback retained.')

# Every native crop must retain the source door's true column; sources have off-center doors.
for name,source in manifest['house_sources'].items():
 x,y,sw,sh=source['source_rectangle'];source_map=json.loads((R/('data/maps/'+source['source_map']+'/map.json')).read_text())
 assert any(v['x']==x+source.get('native_reference_column',source['door_column']) and v['y']==y+sh-1 for v in source_map['warp_events']),('native door anchor mismatch',name)
 assert source['wall_start_row'] in [3,4]
print('PASS: native material references and current house entrances validated.')

# Recompute reachability from the installed binary, not recorded generator counts.
def flood(data,width,height,start):
 assert not data[start[1]*width+start[0]]&0xc00
 seen={start};q=deque(seen)
 while q:
  x,y=q.popleft()
  for xx,yy in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
   if 0<=xx<width and 0<=yy<height and (xx,yy) not in seen and not data[yy*width+xx]&0xc00 and data[yy*width+xx]>>12==3:
    seen.add((xx,yy));q.append((xx,yy))
 return seen
seen=flood(blocks,w,h,tuple(manifest['landmarks']['west_exit']))
for name,p in manifest['landmarks'].items():assert tuple(p) in seen,('unreachable landmark',name,p)
for name,x,y in manifest['buildings']:
 if name in manifest['house_doors']:
  column=manifest['house_doors'][name]
  assert (x+column,y+6) in seen,('house approach',name,x,y)
  assert (x+column,y+5) in seen,('house door',name,x,y)
assert all(blocks[y*w+x]>>12==3 for x,y in seen),'unexpected walking elevation'
assert len(seen)==manifest['walkable_cells']
heal=json.loads((R/'src/data/heal_locations.json').read_text())
landing=next(v for v in heal['heal_locations'] if v['id']=='HEAL_LOCATION_QUANTUM_COASTAL_CITY')
assert landing['map']=='MAP_CORVALA_TOWN' and (landing['x'],landing['y'])==(door['x'],door['y']+1)
assert (landing['x'],landing['y']) in seen,'Fly landing is not reachable'
assert blocks[22*w+65]&1023==0xa1 and blocks[23*w+65]&1023==0xa9
assert blocks[23*w+65]&0xc00,'unfinished cave doorway must remain blocked'
assert manifest['geography']['deck_cells']<manifest['geography']['previous_deck_cells']*.25
print('PASS: actual LOW collision/elevation routes, seven house approaches, cave and lighthouse access.')

# Verify reciprocal directions, offsets and *walkable* seam cells on both maps.
layouts=json.loads((R/'data/layouts/layouts.json').read_text())['layouts']
opposite={'left':'right','right':'left'}
for c in m['connections']:
 other_name={'MAP_VIDRA_COASTAL_ROAD':'Vidra_CoastalRoad','MAP_VIDRA_HARBOR_ROAD':'Vidra_HarborRoad'}[c['map']]
 other=json.loads((R/f'data/maps/{other_name}/map.json').read_text())
 reciprocal=next(v for v in other['connections'] if v['map']=='MAP_CORVALA_TOWN')
 assert reciprocal['direction']==opposite[c['direction']] and reciprocal['offset']==-c['offset']
 ol=next(v for v in layouts if v['id']==other['layout']);ow,oh=ol['width'],ol['height']
 ob=struct.unpack('<'+'H'*ow*oh,(R/ol['blockdata_filepath']).read_bytes())
 ox=ow-1 if c['direction']=='left' else 0;tx=0 if c['direction']=='left' else w-1
 crossed=0
 for oy in [11,12]:
  ty=oy+c['offset'];a=blocks[ty*w+tx];b=ob[oy*ow+ox]
  assert (tx,ty) in seen and not (a|b)&0xc00,(other_name,'blocked seam',ty,oy)
  assert a>>12==b>>12==3
  other_seen=flood(ob,ow,oh,(ox,oy))
  goal=(11,0) if other_name=='Vidra_CoastalRoad' else (23,11)
  assert goal in other_seen,(other_name,'route onward severed')
  crossed+=1
 assert crossed==2
print('PASS: west Coastal Road/Eldervale route and east Harbor Road route remain reciprocal and walkable.')
primary_attrs=struct.unpack('<640I',(R/'data/tilesets/primary/general/metatile_attributes.bin').read_bytes())
assert (primary_attrs[0x12b]>>9)&2,'native sea lacks water terrain'
sea=[v for v in blocks if v&1023==0x12b]
assert sea and all(v>>12==1 and not v&0xc00 for v in sea),'Surf requires elevation 1, collision 0 water'
print('PASS: native Surf-compatible water elevations, collision and terrain flags.')

# Only LOW is current. Retain earlier experiments without claiming revised tides.
assert (R/'tools/corvala/tide_states/low.bin').read_bytes()==raw
for n in ['low','mid','high']:
 assert (R/f'tools/corvala/tide_states/legacy_56x60/{n}.bin').stat().st_size==56*60*2
assert not manifest['tide_states']['runtime_switching']
assert not (R/'tools/corvala/tide_states/mid.bin').exists()
assert not (R/'tools/corvala/tide_states/high.bin').exists()
print('PASS: installed LOW matches authoring output; old tide experiments preserved separately.')
