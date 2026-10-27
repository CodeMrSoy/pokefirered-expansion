"""Validate market inventories, relocation exits, vendor access and purchase guards."""
from pathlib import Path
from collections import deque
import json,re,struct,subprocess
R=Path(__file__).resolve().parents[1]
def read(p):return json.loads((R/p).read_text())
def baseline(p):return json.loads(subprocess.check_output(['git','show','db333930:'+p],cwd=R,text=True))
manifest=read('tools/havora/department-store-stock.json');market=read('data/maps/Havora_Market/map.json');city=read('data/maps/CeladonCity/map.json');oldcity=baseline('data/maps/CeladonCity/map.json')
assert not any(w['dest_map']=='MAP_CELADON_CITY_DEPARTMENT_STORE_1F' for w in city['warp_events'])
for xy in [(11,14),(15,14)]:assert any((o['x'],o['y'])==xy and o['script']=='CeladonCity_DepartmentStoreRelocated' for o in city['object_events'] if o['type']=='object')
checked=0
for p in (R/'data/maps').glob('*/map.json'):
 j=json.loads(p.read_text())
 if not any(w['dest_map']=='MAP_CELADON_CITY' for w in j['warp_events']):continue
 old=baseline(str(p.relative_to(R)))
 for now,was in zip(j['warp_events'],old['warp_events'],strict=True):
  if now['dest_map']=='MAP_CELADON_CITY':
   assert oldcity['warp_events'][int(was['dest_warp_id'])]==city['warp_events'][int(now['dest_warp_id'])],p
   checked+=1
lobby=read('data/maps/CeladonCity_DepartmentStore_1F/map.json')
for i in [6,7]:
 w=market['warp_events'][i];assert w['dest_map']==lobby['id'];dest=lobby['warp_events'][int(w['dest_warp_id'])];assert dest['dest_map']==market['id'] and int(dest['dest_warp_id'])==i
print('PASS both Havora entrances/returns, two Celadon closure signs and',checked,'other Celadon return warps preserved')
allitems=set();known=set(re.findall(r'^#define (ITEM_\w+)',(R/'include/constants/items.h').read_text(),re.M));definitions=(R/'src/data/items.h').read_text()
for floor,shops in manifest['floors'].items():
 s=(R/f'data/maps/CeladonCity_DepartmentStore_{floor}/scripts.inc').read_text()
 for name,stock in shops:
  body=s.split('HavoraDepartment_'+name+'_Stock::',1)[1].split('\n\n',1)[0];assert re.findall(r'\.2byte ITEM_(\w+)',body)==stock+['NONE'];allitems.update(stock)
for stall in manifest['stalls']:
 if stall['items']:
  body=(R/'data/maps/Havora_Market/scripts.inc').read_text().split('Havora_Market_'+stall['name']+'_Stock::',1)[1].split('\n\n',1)[0];assert re.findall(r'\.2byte ITEM_(\w+)',body)==stall['items']+['NONE'];allitems.update(stall['items'])
for item in allitems:
 assert 'ITEM_'+item in known,item
 body=re.search(r'\[ITEM_'+item+r'\]\s*=\s*\{(.*?)(?=\n    \},)',definitions,re.S)[1];price=re.search(r'\.price\s*=\s*([^,]+)',body);assert price and price[1]!='0',item
assert not {'LEVEL_BALL','LURE_BALL','MOON_BALL','FRIEND_BALL','LOVE_BALL','FAST_BALL','HEAVY_BALL'}&allitems
assert len(manifest['stalls'])==8
print('PASS eight stall roles, four floor catalogs, valid priced stock and no Apricorn Balls')
def words(p,fmt='H'):
 b=Path(p).read_bytes();return struct.unpack('<'+fmt*(len(b)//struct.calcsize(fmt)),b)
layouts={l['id']:l for l in read('data/layouts/layouts.json')['layouts']}
for name in ['Havora_Market']+['CeladonCity_DepartmentStore_'+f for f in ['1F','2F','3F','4F','5F']]:
 j=read('data/maps/'+name+'/map.json');l=layouts[j['layout']];w,h=l['width'],l['height'];b=words(R/l['blockdata_filepath']);start=(6,2) if 'Department' in name else (18,58);solid={(o['x'],o['y']) for o in j['object_events'] if o['type']=='object'};q=deque([start]);seen={start}
 while q:
  x,y=q.popleft();z=b[y*w+x]>>12
  for xx,yy in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
   if not(0<=xx<w and 0<=yy<h) or (xx,yy) in seen or (xx,yy) in solid:continue
   t=b[yy*w+xx];nz=t>>12
   if t&0xc00 or z not in (0,15) and nz not in (0,15) and z!=nz:continue
   seen.add((xx,yy));q.append((xx,yy))
 primary,secondary=('building','department_store') if 'Department' in name else ('havora_city','havora_city')
 attr=list(words(R/f'data/tilesets/primary/{primary}/metatile_attributes.bin','I'))+list(words(R/f'data/tilesets/secondary/{secondary}/metatile_attributes.bin','I'))
 if 'Department' in name:assert j['region_map_section']=='MAPSEC_HAVORA_CITY'
 for o in j['object_events']:
  if not(o['script'].startswith('HavoraDepartment_') or any(o['script']=='Havora_Market_'+s['name'] for s in manifest['stalls'])):continue
  x,y=o['x'],o['y'];access=False
  for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
   adj=(x+dx,y+dy);far=(x+2*dx,y+2*dy)
   if adj in seen:access=True
   elif far in seen and 0<=adj[0]<w and 0<=adj[1]<h and attr[b[adj[1]*w+adj[0]]&1023]&0x1ff==0x80:access=True
  assert access,(name,o['script'])
print('PASS public collision/elevation paths to every vendor and retained Counter tutor')
s=(R/'data/maps/Havora_Market/scripts.inc').read_text();blocks={name:[line.strip() for line in body.strip().splitlines()] for name,body in re.findall(r'^(\w+)::\n(.*?)(?=^\w+::|\Z)',s,re.M|re.S)}
def buy(money=10000,owned=False,yes=True,space=True,add_ok=True):
 label='Havora_Market_Meteorite';result=0;received=0
 for _ in range(30):
  for line in blocks[label]:
   if line.startswith('checkitem '):result=int(owned)
   elif line.startswith('msgbox Havora_Market_MeteoriteOffer'):result=int(yes)
   elif line.startswith('checkmoney '):result=int(money>=int(line.split()[1]))
   elif line.startswith('checkitemspace '):result=int(space)
   elif line.startswith('additem '):result=int(add_ok);received+=result
   elif line.startswith('removemoney '):money-=int(line.split()[1])
   elif line.startswith('goto_if_eq '):
    _,value,target=line.split(', ')
    if result=={'TRUE':1,'FALSE':0,'NO':0}[value]:label=target;break
   elif line.startswith('goto '):label=line[5:];break
   elif line=='end':return money,received
  else:raise AssertionError(('sale fell through',label))
 raise AssertionError('sale loop')
assert buy()==(0,1)
for opts in [dict(owned=True),dict(yes=False),dict(space=False),dict(add_ok=False)]:assert buy(**opts)==(10000,0)
assert buy(money=9999)==(9999,0)
print('PASS Meteorite sale success, decline, already owned, insufficient money, full Bag and add failure')
out=R/'build/havora-market-review/compiled';out.mkdir(parents=True,exist_ok=True)
changed=subprocess.check_output(['git','diff','--name-only','db333930'],cwd=R,text=True).splitlines()
for p in changed:
 if p.endswith('/map.json'):
  dest=out/Path(p).parent.name;dest.mkdir(exist_ok=True);subprocess.run([str(R/'tools/mapjson/mapjson'),'map','firered',p,'data/layouts/layouts.json',str(dest)+'/'],cwd=R,capture_output=True,check=True)
paths=[R/p for p in changed if p.endswith(('/scripts.inc','/text.inc'))];combined=out/'shops.s';combined.write_text('\n'.join(p.read_text() for p in paths))
with (out/'shops-preprocessed.s').open('w') as f:subprocess.run([str(R/'tools/preproc/preproc'),str(combined),str(R/'charmap.txt')],cwd=R,stdout=f,check=True)
print('PASS native map JSON compilation and text/charmap preprocessing')
