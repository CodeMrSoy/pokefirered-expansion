"""Audit Havora's real grass/water tiles, generated tables and native slot odds."""
from pathlib import Path
from collections import Counter
import ctypes as c,json,re,struct,subprocess
R=Path(__file__).resolve().parents[1];D=R/'build/havora-encounters';D.mkdir(parents=True,exist_ok=True)
def read(p):return json.loads((R/p).read_text())
def old(p):return subprocess.check_output(['git','show','HEAD:'+p],cwd=R)
def words(p,fmt='H'):
 b=Path(p).read_bytes();return struct.unpack('<'+fmt*(len(b)//struct.calcsize(fmt)),b)
plan=read('tools/havora/wild-encounters.json');j=read('src/data/wild_encounters.json');before=json.loads(old('src/data/wild_encounters.json'));g=j['wild_encounter_groups'][0];og=before['wild_encounter_groups'][0]
mapnames=set(plan['water_habitats'])|set(plan['grass_habitats']);maps={n:read(f'data/maps/{n}/map.json') for n in mapnames};ids={v['id'] for v in maps.values()};entries={e['map']:e for e in g['encounters'] if e['map'] in ids};assert len(entries)==len(ids)
def without_levels(e):
 e=json.loads(json.dumps(e))
 for kind in ('land_mons','water_mons','rock_smash_mons','fishing_mons'):
  for mon in e.get(kind,{}).get('mons',[]):
   mon.pop('min_level');mon.pop('max_level')
 return e
# Area level shifts are audited separately by story_level_progression.py.
assert [without_levels(e) for e in g['encounters'] if e['map'] not in ids]==[without_levels(e) for e in og['encounters'] if e['map'] not in ids]
assert g['fields']==og['fields'] and j['wild_encounter_groups'][1:]==before['wild_encounter_groups'][1:]
known=set(re.findall(r'^#define (SPECIES_\w+)',(R/'include/constants/species.h').read_text(),re.M))
for e in entries.values():
 for kind,count in [('land_mons',12),('water_mons',5),('fishing_mons',10)]:
  if kind not in e:continue
  assert len(e[kind]['mons'])==count
  for m in e[kind]['mons']:assert m['species'] in known and m['species']!='SPECIES_NONE' and plan['level_range'][0]<=m['min_level']<=m['max_level']<=plan['level_range'][1]
for name in plan['grass_habitats']:assert 'land_mons' in entries[maps[name]['id']]
for name in plan['water_habitats']:assert {'water_mons','fishing_mons'}<=entries[maps[name]['id']].keys()
for sp,mid in plan['signature_species'].items():assert entries[mid]['water_mons']['mons'][4]['species']==sp
print('PASS two complete land pools and three Surf/fishing pools, all levels within the Havora progression range, valid species, no empty slots; unrelated encounters preserved')
attrs=[]
for kind in ['primary','secondary']:attrs+=list(words(R/f'data/tilesets/{kind}/havora_city/metatile_attributes.bin','I'))
ls={l['id']:l for l in read('data/layouts/layouts.json')['layouts']};grass_counts={}
for p in (R/'data/maps').glob('Havora_*/map.json'):
 m=json.loads(p.read_text())
 if m['map_type']=='MAP_TYPE_INDOOR':continue
 l=ls[m['layout']];b=words(R/l['blockdata_filepath']);grass=[i for i,t in enumerate(b) if attrs[t&1023]&0x1ff==2 or (attrs[t&1023]>>24)&7==1]
 if not grass:continue
 assert m['name'] in plan['grass_habitats'],('grass lacks encounter pool',m['name'])
 for i in grass:assert (attrs[b[i]&1023]>>24)&7==1,'grass lacks land encounter attribute'
 assert (R/l['blockdata_filepath']).read_bytes()==old(l['blockdata_filepath']),'grass map art/collision changed'
 grass_counts[m['name']]=len(grass)
assert grass_counts=={'Havora_Market':99,'Havora_WestQuadrant':22}
for name in plan['water_habitats']:
 m=maps[name];l=ls[m['layout']];b=words(R/l['blockdata_filepath']);W,H=l['width'],l['height'];launches=[]
 for y in range(1,H-1):
  for x in range(1,W-1):
   t=b[y*W+x]
   if t&0xc00 or t>>12!=3:continue
   for xx,yy in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
    water=b[yy*W+xx];a=attrs[water&1023]
    if a&0x1ff==0x15 and (a>>24)&7==2 and water>>12!=3:launches.append(((x,y),(xx,yy)))
 assert launches,('no Surf/fishing launch',name)
 if name=='Havora_River':
  assert (tuple(plan['river_launch']['shore']),tuple(plan['river_launch']['water'])) in launches
  oldb=struct.unpack('<'+'H'*len(b),old(l['blockdata_filepath']));fixes={(e['x'],e['y']) for e in plan['river_launch']['elevation_changes']}
  for i,(a,z) in enumerate(zip(oldb,b)):
   assert a&0xfff==z&0xfff
   if a!=z:assert (i%W,i//W) in fixes
  for route in [[(0,13),(1,13),(2,13),(3,13)],[(6,13),(5,13),(4,13),(3,13)],[(4,14),(3,14),(3,13)]]:
   for path in [route,route[::-1]]:
    for (x,y),(xx,yy) in zip(path,path[1:]):
     a,z=b[y*W+x],b[yy*W+xx];assert not(a|z)&0xc00 and ((a>>12)==0 or (z>>12) in (0,15,a>>12))
print('PASS all 121 existing tall-grass tiles covered without art changes; all three water pools have bank/dock access; river boarding/return elevation paths valid')
subprocess.run(['python3','tools/wild_encounters/wild_encounters_time_season.py'],cwd=R,check=True)
header=(R/'src/data/wild_encounters.h').read_text();suffixes={'land_mons':('LandMons','landMonsInfo'),'water_mons':('WaterMons','waterMonsInfo'),'fishing_mons':('FishingMons','fishingMonsInfo')}
for e in entries.values():
 for kind,(suffix,field) in suffixes.items():
  if kind not in e:continue
  name=e['base_label']+'_'+suffix;body=header.split('const struct WildPokemon '+name+'[] =',1)[1].split('};',1)[0];got=[(int(a),int(b),sp) for a,b,sp in re.findall(r'\{ (\d+), (\d+), (SPECIES_\w+) \}',body)]
  assert got==[(m['min_level'],m['max_level'],m['species']) for m in e[kind]['mons']]
  assert '.'+field+' = &'+name+'Info' in header
print('PASS native encounter generator: all land, Surf and rod tables contain the correct species and levels')
source=(R/'src/wild_encounter.c').read_text()
def function(name):
 m=re.search(r'^(?:static )?u8 '+name+r'\([^\n]*\)\n\{',source,re.M);assert m;i=m.end();depth=1
 while depth:depth+=(source[i]=='{')-(source[i]=='}');i+=1
 return source[m.start():i]+'\n'
macros='\n'.join(l for l in header.splitlines() if l.startswith('#define ENCOUNTER_CHANCE_'))
code='''#include <stdint.h>
typedef uint8_t u8;typedef int bool8;
#define TRUE 1
#define FALSE 0
#define LURE_STEP_COUNT 0
#define OLD_ROD 0
#define GOOD_ROD 1
#define SUPER_ROD 2
#define max(a,b) ((a)>(b)?(a):(b))
unsigned roll;
unsigned Random(void){return roll;}
'''+macros+'\n'+''.join(function(n) for n in ['ChooseWildMonIndex_Land','ChooseWildMonIndex_WaterRock','ChooseWildMonIndex_Fishing'])+'\nint pick(int n,int kind){roll=n;return kind==-2?ChooseWildMonIndex_Land():kind==-1?ChooseWildMonIndex_WaterRock():ChooseWildMonIndex_Fishing(kind);}\n'
p=D/'wild-slots-host.c';p.write_text(code);so=D/'wild-slots-host.so';subprocess.run(['gcc','-shared','-fPIC','-Wall','-Wextra','-Werror',str(p),'-o',str(so)],check=True);h=c.CDLL(str(so))
for kind,weights,offset in [(-2,[20,20,10,10,10,10,5,5,4,4,1,1],0),(-1,[60,30,5,4,1],0),(0,[70,30],0),(1,[60,20,20],2),(2,[40,40,15,4,1],5)]:assert Counter(h.pick(n,kind) for n in range(100))=={i+offset:w for i,w in enumerate(weights)}
print('PASS actual compiled C selection: exact land, Surf and all three rod distributions (without lure modifiers)')
