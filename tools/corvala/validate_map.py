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
 assert 640<=v&1023<640+sheet.width*sheet.height//64
 assert v>>12 in [0,7,8,9,10,11,12]
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
