#!/usr/bin/env python3
"""Check asset preservation, cliff cells, reviewed footprints and return warps."""
import io,json,struct,subprocess
from pathlib import Path
from PIL import Image
R=Path(__file__).resolve().parents[2];BASE='5ece37d98db1a8bc9fd9bbd2e3ed5ca69d56e1a1'
def source(p):return subprocess.check_output(['git','show',BASE+':'+p],cwd=R)
def js(p):return json.loads((R/p).read_text())
def words(b):return list(struct.unpack('<'+'H'*(len(b)//2),b))
report=js('tools/havora/green-house-placements.json');kits=js('tools/havora/green-houses.json')['kits'];kits['long_home']=report['long_home_grid'];allowed={}
for e in report['placements']:
 cells=allowed.setdefault(e['map'],set());x,y,w,h=e['old_rectangle'];cells.update((x+i,y+j) for j in range(h) for i in range(w));x,y=e['new_origin'];cells.update((x+i,y+j) for j,row in enumerate(kits[e['kit']]) for i in range(len(row)));x,y=e['door'];cells.add((x,y+1))
oldT=[];newT=[];oldM=[];newM=[];oldA=[];newA=[]
for group,count in [('primary',640),('secondary',384)]:
 p=f'data/tilesets/{group}/havora_city/'
 for dest,data in [(oldT,source(p+'tiles.png')),(newT,(R/p/'tiles.png').read_bytes())]:
  im=Image.open(io.BytesIO(data));dest.extend(im.crop((i%16*8,i//16*8,i%16*8+8,i//16*8+8)).tobytes() for i in range(count))
 for dest,data in [(oldM,source(p+'metatiles.bin')),(newM,(R/p/'metatiles.bin').read_bytes())]:
  w=words(data);dest.extend(tuple(w[i:i+8]) for i in range(0,len(w),8))
 for dest,data in [(oldA,source(p+'metatile_attributes.bin')),(newA,(R/p/'metatile_attributes.bin').read_bytes())]:dest.extend(struct.unpack('<'+'I'*(len(data)//4),data))
 for path in (R/p/'palettes').glob('*.pal'):assert path.read_text().splitlines()==source(str(path.relative_to(R))).decode().splitlines()
placed=set();layouts={};changed=0;cliff_cells=0
terrain=js('tools/havora/city-tileset.json')['native_general_ids'];cliffs={v for k,v in terrain.items() if int(k)>=104}|set(range(168,172))
for l in js('data/layouts/layouts.json')['layouts']:
 if l['primary_tileset']!='gTileset_HavoraCityPrimary':continue
 name=l['name'].replace('_Layout','');layouts[name]=l
 for f in ['blockdata_filepath','border_filepath']:
  old=words(source(l[f]));new=words((R/l[f]).read_bytes());assert len(old)==len(new);placed.update(v&1023 for v in old)
  for i,(a,b) in enumerate(zip(old,new)):
   if a&1023 in cliffs:assert a==b;cliff_cells+=1
   if a!=b:
    assert f=='blockdata_filepath' and (i%l['width'],i//l['width']) in allowed.get(name,set()),(name,i)
    changed+=1
 mp=f'data/maps/{name}/map.json';old=json.loads(source(mp));new=js(mp)
 assert old['connections']==new['connections']
 changed_warps={e['warp_index'] for e in report['placements'] if e['map']==name}
 assert len(old['warp_events'])==len(new['warp_events'])
 for i,(a,b) in enumerate(zip(old['warp_events'],new['warp_events'])):
  if i not in changed_warps:assert a==b
  else:assert a['dest_map']==b['dest_map'] and a['dest_warp_id']==b['dest_warp_id']
 for field in old:
  if field!='warp_events':assert old[field]==new[field],(name,field)
for mid in placed:
 assert oldM[mid]==newM[mid] and oldA[mid]==newA[mid],mid
 for w in oldM[mid]:assert oldT[w&1023]==newT[w&1023],(mid,w)
fixed=set(range(416,482))|set(range(508,512))|set(range(896,1024))|{0,20}
assert all(oldT[t]==newT[t] for t in fixed)
allmaps={m['id']:m for m in (json.loads(p.read_text()) for p in (R/'data/maps').glob('*/map.json'))}
for e in report['placements']:
 name=e['map'];l=layouts[name];m=js(f'data/maps/{name}/map.json');v=words((R/l['blockdata_filepath']).read_bytes());x,y=e['door'];block=v[y*l['width']+x];landing=v[(y+1)*l['width']+x]
 assert block&0xc00==0 and landing&0xc00==0,(name,'blocked door')
 assert block>>12==landing>>12,(name,'door elevation mismatch')
 assert newA[block&1023]&511==0x69,(name,'door behavior changed')
 warp=m['warp_events'][e['warp_index']];assert (warp['x'],warp['y'],warp['elevation'])==(x,y,block>>12)
 interior=allmaps[warp['dest_map']];assert any(w['dest_map']==m['id'] and int(w['dest_warp_id'])==e['warp_index'] for w in interior['warp_events'])
 for row in kits[e['kit']]:assert all(0<=i<1024 for i in row)
assert not subprocess.check_output(['git','diff','--name-only',BASE,'--','data/layouts/HavoraHarbor','data/maps/HavoraHarbor','data/layouts/layouts.json','data/maps/map_groups.json','src/fieldmap.c'],cwd=R).strip()
# The fountain adds a separate shared-city callback; legacy ocean functions
# must remain byte-for-byte equivalent as C source.
import re
animpath='src/tileset_anims.c';oldsrc=source(animpath).decode();newsrc=(R/animpath).read_text()
for function in ['TilesetAnim_HavoraHarbor','InitTilesetAnim_HavoraHarbor']:
 pattern=r'(?:static )?void '+function+r'\([^)]*\)\s*\{.*?\n\}'
 assert re.search(pattern,oldsrc,re.S).group()==re.search(pattern,newsrc,re.S).group()
result={'residences_replaced':len(report['placements']),'changed_cells_within_reviewed_plots':changed,'existing_placed_metatiles_preserved':len(placed),'cliff_and_stair_cells_preserved':cliff_cells,'all_borders_connections_and_harbor_unchanged':True,'door_collision_elevation_behavior_and_return_warps_checked':True,'fixed_animation_graphics_and_palettes_unchanged':True,'emulator_or_porymap_ui_test':False}
print(json.dumps(result,indent=2))
