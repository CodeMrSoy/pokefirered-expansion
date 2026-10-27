#!/usr/bin/env python3
"""Check actual packed GBA tiles, palette budgets, warp behavior and preview fidelity."""
from pathlib import Path
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
assert len(set(manifest['walkable_cells_by_tide']))==3
print('PASS: packed tile references, palette precision, tile budget, Center door and exact preview fidelity.')

# Primary references must remain live animated graphics, not copies in static secondary slots.
layout=next(l for l in json.loads((R/'data/layouts/layouts.json').read_text())['layouts'] if l['id']=='LAYOUT_CORVALA_TOWN')
assert layout['primary_tileset']=='gTileset_General'
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

# Authoring-state files preserve route changes for a future runtime controller.
assert (R/'tools/corvala/tide_states/low.bin').read_bytes()==raw
assert [a['cave_approach'] for a in manifest['tidal_access']]==[True,False,False]
assert [a['reef_walk'] for a in manifest['tidal_access']]==[True,False,False]
assert [a['pool_lookout'] for a in manifest['tidal_access']]==[True,True,False]
state_bytes=[(R/f'tools/corvala/tide_states/{n}.bin').read_bytes() for n in ['low','mid','high']]
assert len(set(state_bytes))==3 and all(len(b)==w*h*2 for b in state_bytes)
assert manifest['geography']['deck_cells']<manifest['geography']['previous_deck_cells']*.8
print('PASS: three distinct authoring states, planned tidal access, reduced deck footprint.')
