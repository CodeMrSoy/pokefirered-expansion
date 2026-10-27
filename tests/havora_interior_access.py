"""Exercise the native locked-door hook and audit Havora's selected interiors."""
from pathlib import Path
from collections import deque
import ctypes as c,json,re,struct,subprocess
R=Path(__file__).resolve().parents[1];D=R/'build/havora-interiors';D.mkdir(parents=True,exist_ok=True)
def read(p):return json.loads((R/p).read_text())
def words(p,fmt='H'):
 data=Path(p).read_bytes();return struct.unpack('<'+fmt*(len(data)//struct.calcsize(fmt)),data)
ls={l['id']:l for l in read('data/layouts/layouts.json')['layouts']};maps={p.parent.name:json.loads(p.read_text()) for p in (R/'data/maps').glob('*/map.json')};byid={j['id']:j for j in maps.values()};policy=read('tools/havora/interior-access.json')
attrs=[]
for kind in ['primary','secondary']:attrs+=list(words(R/f'data/tilesets/{kind}/havora_city/metatile_attributes.bin','I'))
closed={(p['map'],p['x'],p['y']) for p in policy['locked_doors']};assert len(closed)==8
assert len(policy["private_interiors"])==10
for name in ['Havora_Market','Havora_WestQuadrant','Havora_NorthQuadrant']:
 j=maps[name];l=ls[j['layout']];b=words(R/l['blockdata_filepath']);W=l['width']
 for i,t in enumerate(b):
  if attrs[t&1023]&0x1ff!=0x69:continue
  x,y=i%W,i//W;locked=(name,x,y) in closed
  events=[e for e in j['bg_events'] if (e['x'],e['y'])==(x,y) and e['script']=='EventScript_HavoraDoorLocked']
  warps=[w for w in j['warp_events'] if (w['x'],w['y'])==(x,y)]
  if locked:
   assert len(events)==1 and not warps and t&0xc00,(name,x,y)
   assert events[0]['player_facing_dir']=='BG_EVENT_PLAYER_FACING_NORTH'
  else:assert warps,(name,'unhandled door',x,y)
 for idx,w in enumerate(j['warp_events']):
  if (name,idx) in {(e['map'],e['index']) for e in policy['return_only_warps']}:continue
  t=b[w['y']*W+w['x']];assert attrs[t&1023]&0x1ff in (0x60,0x69),(name,'ghost warp',w)
  assert w['elevation']==t>>12,(name,'wrong elevation',w)
  dest=byid[w['dest_map']];entry=dest['warp_events'][int(w['dest_warp_id'])]
  assert 0<=entry['x']<ls[dest['layout']]['width'] and 0<=entry['y']<ls[dest['layout']]['height']
  if w['dest_map']!='MAP_CELADON_CITY_DEPARTMENT_STORE_1F':
   assert entry['dest_map']==j['id'] and int(entry['dest_warp_id'])==idx,(name,'return mismatch',w,entry)
for e in policy['return_only_warps']:
 j=maps[e['map']];l=ls[j['layout']];b=words(R/l['blockdata_filepath']);w=j['warp_events'][e['index']];tile=b[w['y']*l['width']+w['x']]
 assert attrs[tile&1023]&0x1ff not in range(0x60,0x72) and not tile&0xc00,('legacy exit not safe',e)
print('PASS all actual house doors handled; 8 locked doors; legacy return-only slots safe; two ghost entrances removed; active entrance elevations/return links valid')

# Check the production helper itself, not a rewritten version of its predicate.
s=(R/'src/field_control_avatar.c').read_text();start=s.index('static bool8 TryLockedBuildingDoor(struct MapPosition *position, u8 direction)\n{');end=s.index('\n}\n',start)+3;helper=s[start:end]
code='''#include <stdint.h>
#include <stddef.h>
typedef uint8_t u8;typedef int bool8;
#define TRUE 1
#define FALSE 0
#define DIR_NORTH 2
struct MapPosition {int x,y;};
const u8 EventScript_HavoraDoorLocked[]={1}, OtherScript[]={2};
const u8 *event;int calls;
const u8 *GetSignpostScriptAtMapPosition(struct MapPosition *p){(void)p;return event;}
void ScriptContext_SetupScript(const u8 *s){if(s==EventScript_HavoraDoorLocked)calls++;}
'''+helper+'''
int probe(int which,int direction){struct MapPosition p={0,0};calls=0;event=which==1?EventScript_HavoraDoorLocked:which==2?OtherScript:NULL;int result=TryLockedBuildingDoor(&p,direction);return result*10+calls;}
'''
p=D/'locked-door-host.c';p.write_text(code);so=D/'locked-door-host.so';subprocess.run(['gcc','-shared','-fPIC','-Wall','-Wextra','-Werror',str(p),'-o',str(so)],check=True)
h=c.CDLL(str(so))
for which in [0,1,2]:
 for direction in [1,2,3,4]:assert h.probe(which,direction)==(11 if which==1 and direction==2 else 0)
inputblock=s.split('if (input->heldDirection2 && input->dpadDirection == playerDirection)',1)[1].split('if (input->pressedStartButton)',1)[0]
assert inputblock.index('TryLockedBuildingDoor')<inputblock.index('TryDoorWarp')
script=(R/'data/maps/Havora_Market/scripts.inc').read_text().split('EventScript_HavoraDoorLocked::',1)[1]
assert 'lockall' in script and 'releaseall' in script and '"It\'s locked.$"' in script
assert not re.search(r'^\s*(warp|applymovement)\b',script,re.M)
print('PASS actual compiled C: UP into tagged door starts message; other directions, untagged doors and missing events unaffected; intercept runs before warp; no transition/movement in message script')

# Inspect each chosen room's public walking component and all interactive NPCs.
selected=list(policy['private_interiors'])+['Havora_TradeHall','Havora_Outfitters','Havora_HarborInn']
for name in selected:
 j=maps[name];l=ls[j['layout']];b=words(R/l['blockdata_filepath']);W,H=l['width'],l['height'];start=(j['warp_events'][0]['x'],j['warp_events'][0]['y']);solid={(o['x'],o['y']) for o in j['object_events']};q=deque([start]);seen={start}
 while q:
  x,y=q.popleft();z=b[y*W+x]>>12
  for xx,yy in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
   if not(0<=xx<W and 0<=yy<H) or (xx,yy) in seen or (xx,yy) in solid:continue
   t=b[yy*W+xx];nz=t>>12
   if t&0xc00 or z not in (0,15) and nz not in (0,15) and nz!=z:continue
   seen.add((xx,yy));q.append((xx,yy))
 script=(R/f'data/maps/{name}/scripts.inc').read_text()
 for o in j['object_events']:
  assert o['script']+'::' in script,(name,'missing resident script',o['script'])
  t=b[o['y']*W+o['x']];assert not t&0xc00,(name,'NPC on solid furniture',o)
  access=any(abs(x-o['x'])+abs(y-o['y'])==1 for x,y in seen)
  if name=='Havora_Outfitters' and o['graphics_id']=='OBJ_EVENT_GFX_CLERK':
   # Clerk stands behind the native Mart counter, reachable from its right.
   attr=list(words(R/'data/tilesets/primary/building/metatile_attributes.bin','I'))+list(words(R/'data/tilesets/secondary/mart/metatile_attributes.bin','I'))
   x,y=o['x'],o['y'];access=access or ((x+2,y) in seen and attr[b[y*W+x+1]&1023]&0x1ff==0x80)
  assert access,(name,'NPC inaccessible',o)
print('PASS entrance-to-resident paths in all ten homes and three public rooms, native furniture collision and Outfitters counter')
# Compile every modified map and all text with the project's own build tools.
subprocess.run(['make','-C',str(R/'tools/mapjson'),'-j2'],check=True,stdout=subprocess.DEVNULL);subprocess.run(['make','-C',str(R/'tools/preproc'),'-j2'],check=True,stdout=subprocess.DEVNULL)
changed=subprocess.check_output(['git','diff','--name-only'],cwd=R,text=True).splitlines()
for path in changed:
 if path.endswith('/map.json'):
  dest=D/Path(path).parent.name;dest.mkdir(exist_ok=True);subprocess.run([str(R/'tools/mapjson/mapjson'),'map','firered',path,'data/layouts/layouts.json',str(dest)+'/'],cwd=R,check=True,capture_output=True)
combined=D/'interiors.s';combined.write_text('\n'.join((R/p).read_text() for p in changed if p.endswith('/scripts.inc')))
with (D/'interiors-preprocessed.s').open('w') as out:subprocess.run([str(R/'tools/preproc/preproc'),str(combined),str(R/'charmap.txt')],cwd=R,check=True,stdout=out)
print('PASS native map compiler and text/charmap preprocessing')
