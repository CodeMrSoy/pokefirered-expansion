"""Validate cove topology, assets, cave-only access and all town warps."""
import hashlib
from PIL import Image,ImageChops
from build_cove import R,D,read,words,flood,atlas
from refine_tides import reachable
m=read(R/'tools/corvala/map.json');assert m['design']=='cave-cove-v1'
assert {b['name'] for b in m['buildings'] if b['name'].startswith('house')}=={f'house{i}' for i in range(1,6)}
w,h=m['dimensions'];assert (w,h)==(64,64)
raw=(R/'data/layouts/Corvala_Town/map.bin').read_bytes();blocks=words(R/'data/layouts/Corvala_Town/map.bin')
assert len(blocks)==w*h and hashlib.sha256(raw).hexdigest()==m['result_sha256']
assert (w+15)*(h+14)<=0x2800
assert (R/'tools/corvala/tide_states/low.bin').read_bytes()==raw
sheet=Image.open(D/'tiles.png');assert sheet.mode=='P' and sheet.width==128 and sheet.width*sheet.height//64<=384
metas=words(D/'metatiles.bin');assert len(metas)==m['metatiles']*8 and len(words(D/'metatile_attributes.bin',4))==m['metatiles']<=384
assert all((v&1023)<640+m['tiles'] and v>>12<=12 for v in metas)
for p in (D/'palettes').glob('*.pal'):
 cs=p.read_text().splitlines();assert cs[:3]==['JASC-PAL','0100','16']
 assert all(0<=int(v)<=248 and int(v)%8==0 for row in cs[3:] for v in row.split())
images=atlas('corvala');out=Image.new('RGB',(w*16,h*16))
for i,b in enumerate(blocks):out.paste(images[b&1023],(i%w*16,i//w*16))
assert ImageChops.difference(out,Image.open(R/'docs/corvala/low-tide-playable.png')).getbbox() is None
print('PASS: GBA budgets, indexed tiles/palettes, LOW snapshot and exact packed preview')
center=next(b for b in m['buildings'] if b['name']=='center')
assert (center['w'],center['h'])==(5,5)
native_center=[[0x17b,0x17c,0x17d,0x17e,0x17f],[0x48,0x49,0x4a,0x4b,0x187],[0x50,0x51,0x52,0x53,0x18f],[0x58,0x59,0x5a,0x5b,0x197],[0x60,0x61,0x62,0x186,0x19f]]
primary=words(R/'data/tilesets/primary/general/metatiles.bin')
for yy,row in enumerate(native_center):
 for xx,expected in enumerate(row):
  actual=blocks[(center['y']+yy)*w+center['x']+xx]&1023
  if yy==0 or xx==4:
   assert metas[(actual-640)*8+4:(actual-640)*8+8]==primary[expected*8+4:expected*8+8]
  else:assert actual==expected
print('PASS: complete native Center roof cap, wall columns and animated doorway')
town=read(R/'data/maps/Corvala_Town/map.json');assert not town['connections'];assert len(town['warp_events'])==9
dest={v['dest_map'] for v in town['warp_events']};assert dest=={'MAP_CORVALA_TOWN_POKEMON_CENTER_1_F','MAP_CORVALA_MART','MAP_CORVALA_HOUSE_1','MAP_CORVALA_HOUSE_2','MAP_CORVALA_HOUSE_3','MAP_CORVALA_HOUSE_4','MAP_CORVALA_HOUSE_5','MAP_CORVALA_TIDAL_GYM','MAP_CORVALA_ENTRANCE_CAVE'}
maps={}
for path in (R/'data/maps').glob('*/map.json'):
 data=read(path);maps[data['id']]=data
incoming=[]
for data in maps.values():
 for c in data.get('connections') or []:assert c['map']!='MAP_CORVALA_TOWN','old road connection remains'
 for event in data.get('warp_events',[]):
  if event['dest_map']=='MAP_CORVALA_TOWN':incoming.append(data['id'])
assert set(incoming)==dest,'unexpected town entrance'
layouts={v['id']:v for v in read(R/'data/layouts/layouts.json')['layouts']}
for i,event in enumerate(town['warp_events']):
 interior=maps[event['dest_map']];back=interior['warp_events'][int(event['dest_warp_id'])]
 assert back['dest_map']=='MAP_CORVALA_TOWN' and back['dest_warp_id']==str(i)
 layout=layouts[interior['layout']];ib=words(R/layout['blockdata_filepath']);assert not ib[back['y']*layout['width']+back['x']]&0xc00
doors={(v['x'],v['y']) for v in town['warp_events']}
seen=reachable(blocks,m['landmarks']['entrance_approach'],doors)
assert len(seen)==m['walkable_cells']
assert not any(x in (0,63) or y in (0,63) for x,y in seen), 'accessible map boundary'
assert m['gym_terraces']['source']=='user-0c02a4ba'
high=words(R/'tools/corvala/tide_states/high.bin')
images=atlas('corvala');out=Image.new('RGB',(w*16,h*16))
for i,b in enumerate(high):out.paste(images[b&1023],(i%w*16,i//w*16))
assert ImageChops.difference(out,Image.open(R/'docs/corvala/high-tide-playable.png')).getbbox() is None
npcs={(v['x'],v['y']) for v in town['object_events']}
for phase,bs in [('LOW',blocks),('HIGH',high)]:
 seen=reachable(bs,m['landmarks']['entrance_approach'],doors|npcs)
 for name,xy in m['landmarks'].items():
  if phase=='HIGH' and name in m['tide_states']['low_only_landmarks']:continue
  assert tuple(xy) in seen,(phase,name,'blocked by terrain/NPC')
 for x,y in npcs:
  assert any(p in seen for p in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)])
 for ev in town['warp_events']:assert bs[ev['y']*w+ev['x']]>>12==ev['elevation']
print('PASS: both tides retain services, matching warp elevations and reachable dock NPCs')
assert tuple(m['landmarks']['gym_approach']) not in reachable(high,m['landmarks']['entrance_approach'],doors)
attrs=words(D/'metatile_attributes.bin',4);primary_attrs=words(R/'data/tilesets/primary/general/metatile_attributes.bin',4)
for v in high:
 mid=v&1023;a=primary_attrs[mid] if mid<640 else attrs[mid-640]
 assert a&511!=0x21,'sand remains exposed at high tide'
 assert mid not in (667,668,669,670,m['labels']['Stairs']),'dock support or wooden stairs remain exposed'
for x,y in m['tide_states']['submerged_cliff_cells']:assert high[y*w+x]&1023==0x12b
rim={(x,y) for x,y,mask in m['tide_states']['flooded_cliff_rim']}
assert {(39,10),(43,11),(46,12),(47,16),(51,16),(56,15),(58,16),(59,18),(60,20),(61,23),(62,27),(63,31)}<=rim,'circled lower cliff corners remain exposed'
assert {(30,10),(46,14),(61,25)}<=rim,'lower northern/eastern cliff sections were missed'
for x,y,original in [(30,9,0x447c),(62,25,0x3c73)]:
 assert (x,y) not in rim and high[y*w+x]==blocks[y*w+x]==original,'upper cliff layer changed'
for x,y in rim:
 assert high[y*w+x]&1023==0x12b and high[y*w+x]>>12==1
 assert bool(high[y*w+x]&0xc00)==(x==63)
for x,y in m['tide_states']['surf_landings']:
 assert high[y*w+x]>>12==3 and high[(y+1)*w+x]==0x112b
for x,y,size in m['tide_states']['rock_sites']:
 for dy in range(size):
  for dx in range(size):assert blocks[(y+dy)*w+x+dx]&0xc00 and high[(y+dy)*w+x+dx]&0xc00
print('PASS: full sand/terrace/support/stair flooding, low-only gym, Surf landings and solid rocks in both tides')
print('PASS: cave-only physical entrance, no road seams, nine reciprocal town warps and all approaches')
cave=maps['MAP_CORVALA_ENTRANCE_CAVE'];layout=layouts[cave['layout']];ib=words(R/layout['blockdata_filepath'])
a,b=cave['warp_events'];seen=flood(ib,layout['width'],layout['height'],(a['x'],a['y']+1),{(a['x'],a['y']),(b['x'],b['y'])})
assert (b['x'],b['y']+1) in seen
road=maps['MAP_VIDRA_COASTAL_ROAD'];assert road['warp_events'][0]['dest_map']=='MAP_CORVALA_ENTRANCE_CAVE'
layout=layouts[road['layout']];rb=words(R/layout['blockdata_filepath']);assert (20,10) in flood(rb,24,24,(11,0))
heal=next(v for v in read(R/'src/data/heal_locations.json')['heal_locations'] if v['id']=='HEAL_LOCATION_QUANTUM_COASTAL_CITY')
assert [heal['x'],heal['y']]==m['landmarks']['center_approach']
assert m['tide_states']['runtime_switching']
print('PASS: Coastal Road-to-cave access, cave traversal and relocated heal/Fly landing')
