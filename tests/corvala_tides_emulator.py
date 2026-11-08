"""Fresh-game mGBA checks of the restarted Corvala cove and every doorway."""
import json,struct,os,subprocess
from collections import deque
import havora_emulator_support as m
m.d=m.root/'build/corvala/tides-emulator';m.d.mkdir(parents=True,exist_ok=True)
groups=json.loads((m.root/'data/maps/map_groups.json').read_text())
ids={n:(g,i) for g,k in enumerate(groups['group_order']) for i,n in enumerate(groups[k])};names={v:k for k,v in ids.items()}
layouts={v['id']:v for v in json.loads((m.root/'data/layouts/layouts.json').read_text())['layouts']}
manifest=json.loads((m.root/'tools/corvala/map.json').read_text())
keys={(0,-1):4,(0,1):5,(-1,0):6,(1,0):7}
def map_id():
 p=struct.unpack('<I',m.read(m.symbols['gSaveBlock1Ptr'],4))[0];return tuple(m.read(p+4,2))
def pos():
 obj=m.symbols['gObjectEvents']+m.read(m.symbols['gPlayerAvatar']+5,1)[0]*36
 x,y=struct.unpack('<hh',m.read(obj+16,4));return x-7,y-7
def warp(name,x,y):
 group,num=ids[name];m.inject(b'\x39'+struct.pack('<BBBHH',group,num,255,x,y)+b'\x6b\x02');m.run(120)
 assert map_id()==ids[name] and pos()==(x,y),(name,'fixture',map_id(),pos())
def step(key,expected=None):
 old=(map_id(),pos());m.keys.add(key)
 for _ in range(50):
  m.run(1)
  if (map_id(),pos())!=old:break
 m.keys.clear();m.run(32)
 assert (map_id(),pos())!=old,('blocked step',key,old)
 if expected is not None:assert pos()==expected,('unexpected step',pos(),expected)
def follow(goal,surf=False):
 current=map_id();name=names[current];data=json.loads((m.root/f'data/maps/{name}/map.json').read_text());l=layouts[data['layout']];w,h=l['width'],l['height']
 vw,vh,ptr=struct.unpack('<iiI',m.read(m.symbols['VMap'],12));bs=tuple(v for yy in range(h) for v in struct.unpack('<'+'H'*w,m.read(ptr+2*((yy+7)*vw+7),w*2)))
 avoid={(v['x'],v['y']) for v in data['warp_events']+data['object_events']}
 start=pos();parents={start:None};q=deque([start])
 while q and goal not in parents:
  x,y=q.popleft()
  for dx,dy in keys:
   p=x+dx,y+dy
   if not (0<=p[0]<w and 0<=p[1]<h) or p in parents or p in avoid:continue
   b=bs[p[1]*w+p[0]]
   e=bs[y*w+x]>>12;ee=b>>12
   if b&0xc00:continue
   if surf:
    if ee!=1:continue
   elif ee==1 or (e and ee and e!=ee):continue
   parents[p]=(x,y);q.append(p)
 assert goal in parents,('no path',name,start,goal)
 route=[];p=goal
 while p!=start:route.append(p);p=parents[p]
 for p in reversed(route):
  a=pos();step(keys[(p[0]-a[0],p[1]-a[1])],p);assert map_id()==current
 return len(route)
def enter(expected,key=4,frames=22):
 m.keys.add(key);m.run(frames);m.keys.clear();m.run(200)
 assert map_id()==ids[expected],('door transition',expected,names[map_id()],pos())

native_dir=m.d/'native';native_dir.mkdir(exist_ok=True)
native_addr=m.symbols['gDecompressionBuffer']+0x3000;result_addr=m.symbols['gDecompressionBuffer']+0x3f00
prefix=os.environ.get('ARM_NM','arm-none-eabi-nm').removesuffix('.exe').removesuffix('nm')
def native(name,*args):
 assembly=['.syntax unified','.thumb','.thumb_func','_start:','push {r4, lr}']
 assembly += [f'ldr r{i}, arg{i}' for i in range(len(args))]
 assembly += ['ldr r4, function','bl invoke','ldr r3, result','str r0, [r3]','movs r0, #1','pop {r4, pc}','invoke:','bx r4','.align 2',f'function: .word {m.symbols[name]|1}',f'result: .word {result_addr}']
 assembly += [f'arg{i}: .word {a}' for i,a in enumerate(args)]
 (native_dir/'call.s').write_text('\n'.join(assembly)+'\n')
 subprocess.run([prefix+'as','-mthumb','-mcpu=arm7tdmi','-o',str(native_dir/'call.o'),str(native_dir/'call.s')],check=True)
 subprocess.run([prefix+'objcopy','-O','binary','-j','.text',str(native_dir/'call.o'),str(native_dir/'call.bin')],check=True)
 m.write(native_addr,(native_dir/'call.bin').read_bytes());m.inject(b'\x23'+struct.pack('<I',native_addr|1)+b'\x6b\x02')
 return struct.unpack('<I',m.read(result_addr,4))[0]

def hour(value):
 native('RtcInitLocalTimeOffset',value,0);m.run(120)
 assert native('GetCurrentHour')==value

def check_phase(phase):
 raw=(m.root/f'tools/corvala/tide_states/{phase}.bin').read_bytes()
 vw,vh,ptr=struct.unpack('<iiI',m.read(m.symbols['VMap'],12))
 for y in range(64):assert m.read(ptr+2*((y+7)*vw+7),128)==raw[y*128:(y+1)*128],(phase,'row',y)

def finish_tide_rescue(phase):
 assert m.read(m.symbols['sGlobalScriptContext']+1,1)!=b'\0'
 for _ in range(10):
  m.press(8,60);m.run(100)
  if pos()==(31,26) and m.read(m.symbols['sGlobalScriptContext']+1,1)==b'\0':break
 assert pos()==(31,26)
 assert not m.read(m.symbols['gPlayerAvatar'],1)[0]&8
 check_phase(phase)

hour(10);native('DisableWildEncounters',1)
warp('Vidra_CoastalRoad',11,12);follow((20,10));enter('Corvala_EntranceCave');follow((24,3));enter('Corvala_Town')
assert pos()==(49,16);check_phase('low')
print('PASS: actual cave entrance reaches the moved Corvala doorway at low tide',flush=True)
for phase,clock in [('low',10),('high',11)]:
 follow((31,26));hour(clock);check_phase(phase);m.snap(phase+'-center')
 for label,target in [('center','Corvala_Town_PokemonCenter_1F'),('mart','Corvala_Mart'),('house1','Corvala_House1'),('house2','Corvala_House2'),('house3','Corvala_House3'),('house4','Corvala_House4'),('house5','Corvala_House5'),('gym','Corvala_TidalGym')]:
  if phase=='high' and label=='gym':continue
  approach=tuple(manifest['landmarks'][label+'_approach']);follow(approach);m.snap(phase+'-'+label);enter(target)
  enter('Corvala_Town',5,40 if label=='gym' else 22);assert pos()==approach,(label,pos(),approach)
  check_phase(phase)
 if phase=='low':
  hour(11);check_phase('low');finish_tide_rescue('high');hour(10)
  print('PASS: gym approach returns safely to the Center at tide change',flush=True)
 else:
  try:follow(tuple(manifest['landmarks']['gym_approach']))
  except AssertionError as e:assert e.args[0][0]=='no path'
  else:raise AssertionError('Gym footpath should flood at HIGH')
 print('PASS:',phase,'building access; gym walking route is LOW-only',flush=True)
for value,phase in [(12,'low'),(23,'high'),(0,'low')]:
 follow((31,26));hour(value);check_phase(phase)
print('PASS: even/odd hours and midnight rollover update the live map',flush=True)

# Sand evacuation at the hourly boundary.
follow((24,46));m.snap('low-reef');hour(11);check_phase('low')
finish_tide_rescue('high')
print('PASS: sand warning and Center rescue',flush=True)

# Every resident can be approached and their full message dismissed normally.
town=json.loads((m.root/'data/maps/Corvala_Town/map.json').read_text())
for npc in town['object_events']:
 for dx,dy,key in [(0,1,4),(-1,0,7),(1,0,6),(0,-1,5)]:
  try:follow((npc['x']+dx,npc['y']+dy));break
  except AssertionError as e:
   if e.args[0][0]!='no path':raise
 else:raise AssertionError(('no NPC approach',npc))
 m.press(key,30);m.press(8,100)
 assert m.read(m.symbols['sMessageBoxType'],1)!=b'\x00',npc['script']
 m.snap(npc['script'])
 for _ in range(8):
  m.press(8,60)
  if m.read(m.symbols['sGlobalScriptContext']+1,1)==b'\x00':break
 assert m.read(m.symbols['sGlobalScriptContext']+1,1)==b'\x00'
for i in range(1,6):
 follow(tuple(manifest['landmarks'][f'house{i}_approach']));enter(f'Corvala_House{i}')
 follow((2,4));m.press(4,30);m.press(8,100)
 assert m.read(m.symbols['sMessageBoxType'],1)!=b'\x00'
 m.snap(f'house{i}-dialogue')
 for _ in range(8):
  m.press(8,60)
  if m.read(m.symbols['sGlobalScriptContext']+1,1)==b'\x00':break
 assert m.read(m.symbols['sGlobalScriptContext']+1,1)==b'\x00'
 follow((4,6));enter('Corvala_Town',5,40)
print('PASS: all dock residents, friendly Pokemon and five house dialogues open and close',flush=True)

# Return through the cave at HIGH; re-entering chooses the RTC's phase.
follow((49,16));enter('Corvala_EntranceCave');follow((5,3));enter('Vidra_CoastalRoad')
assert pos()==(20,10)
enter('Corvala_EntranceCave');follow((24,3));enter('Corvala_Town');check_phase('high')
print('PASS: high-tide cave route works both ways',flush=True)

fixture=b'\x23'+struct.pack('<I',(m.symbols['ScrCmd_createmon']|1)+0x2000000)+struct.pack('<BBHHI',0,6,131,30,0)+b'\x02';m.inject(fixture)
for i,(x,y) in enumerate(manifest['tide_states']['surf_landings']):
 follow((x,y));m.press(5,30);assert pos()==(x,y)
 assert native('IsPlayerFacingSurfableFishableWater')==1
 m.write(m.symbols['gFieldEffectArguments'],b'\0'*4);native('FieldEffectStart',10);m.run(500)
 assert pos()==(x,y+1) and m.read(m.symbols['gPlayerAvatar'],1)[0]&8
 if i==0:
  follow((14,23),surf=True);m.press(4,30);assert pos()==(14,23),'rock should block Surf'
  follow((x,y+1),surf=True)
  hour(12);check_phase('high');finish_tide_rescue('low');hour(11)
  continue
 m.keys.add(4);m.run(12);m.keys.clear();m.run(90)
 assert pos()==(x,y) and not m.read(m.symbols['gPlayerAvatar'],1)[0]&8,('dock Surf return',x,y,pos())
 follow((31,26));m.run(120)

print('PASS: all six dock Surf landings, solid sea rocks and saved high-water safety',flush=True)

# Real movement on encounter sand must launch a wild battle; docks must not.
hour(10);follow((31,26))
follow((14,23));m.press(4,30);assert pos()==(14,23),'dry boulder should block walking';m.snap('low-rocks');follow((31,26))
native('DisableWildEncounters',0)
for _ in range(12):step(7,(32,26));step(6,(31,26))
assert struct.unpack('<I',m.read(m.symbols['gMain']+4,4))[0]==m.symbols['CB2_Overworld']|1
native('DisableWildEncounters',1);follow((24,46));native('DisableWildEncounters',0)
encounter=False
for i in range(160):
 m.keys.add(7 if i%2==0 else 6);m.run(9);m.keys.clear();m.run(32)
 callback=struct.unpack('<I',m.read(m.symbols['gMain']+4,4))[0]
 if callback!=m.symbols['CB2_Overworld']|1:
  m.run(600);m.snap('sand-wild-battle');encounter=True;break
assert encounter,'No sand encounter after 160 steps'
for _ in range(3):m.press(8,180)
assert struct.unpack('<I',m.read(m.symbols['gMain']+4,4))[0]==m.symbols['BattleMainCB2']|1
m.snap('sand-battle-ready')
assert struct.unpack('<I',m.read(m.symbols['gBattleTypeFlags'],4))[0]&8==0
print('PASS: docks stay encounter-free and real sand walking launches a wild battle',flush=True)
print('PASS: Corvala tides and residents',flush=True)
