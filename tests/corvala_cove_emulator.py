"""Fresh-game mGBA checks of the restarted Corvala cove and every doorway."""
import json,struct,os,subprocess
from collections import deque
import havora_emulator_support as m
m.d=m.root/'build/corvala/cove-emulator';m.d.mkdir(parents=True,exist_ok=True)
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
def follow(goal):
 current=map_id();name=names[current];data=json.loads((m.root/f'data/maps/{name}/map.json').read_text());l=layouts[data['layout']];w,h=l['width'],l['height']
 bs=struct.unpack('<'+'H'*(w*h),(m.root/l['blockdata_filepath']).read_bytes())
 avoid={(v['x'],v['y']) for v in data['warp_events']+data['object_events']}
 start=pos();parents={start:None};q=deque([start])
 while q and goal not in parents:
  x,y=q.popleft()
  for dx,dy in keys:
   p=x+dx,y+dy
   if not (0<=p[0]<w and 0<=p[1]<h) or p in parents or p in avoid:continue
   b=bs[p[1]*w+p[0]]
   if b&0xc00 or b>>12!=3:continue
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

warp('Vidra_CoastalRoad',11,12);walks=follow((20,10));enter('Corvala_EntranceCave');m.snap('entrance-cave')
assert pos()==(5,3),('cave entry landing',pos())
walks+=follow((24,3));enter('Corvala_Town');assert pos()==(49,17);m.snap('town-arrival')
print('PASS: real Coastal Road entrance, cave traversal, and arrival in Corvala',flush=True)
w,h=manifest['dimensions'];raw=(m.root/'data/layouts/Corvala_Town/map.bin').read_bytes()
vw,vh,ptr=struct.unpack('<iiI',m.read(m.symbols['VMap'],12));assert (vw,vh)==(w+15,h+14)
for y in range(h):assert m.read(ptr+2*((y+7)*vw+7),w*2)==raw[y*w*2:(y+1)*w*2]
for name,point in manifest['landmarks'].items():walks+=follow(tuple(point));m.snap(name)
print('PASS:',walks,'real walking steps across the new cove and all approaches',flush=True)
for label,target in [('center','Corvala_Town_PokemonCenter_1F'),('mart','Corvala_Mart'),('house1','Corvala_House1'),('house2','Corvala_House2'),('house3','Corvala_House3'),('house4','Corvala_House4'),('house5','Corvala_House5'),('gym','Corvala_TidalGym')]:
 approach=tuple(manifest['landmarks'][label+'_approach']);follow(approach);enter(target);m.snap(label+'-interior')
 if label=='gym':
  entrance=pos();follow((13,5));m.snap('gym-tidal-pools');follow((entrance[0],entrance[1]-1))
 enter('Corvala_Town',5,40 if label=='gym' else 22);assert pos()==approach,(label,'return position',pos(),approach)
print('PASS: Center, Mart, all five houses and tidal gym enter and return correctly',flush=True)
follow((49,17));enter('Corvala_EntranceCave');assert pos()==(24,3)
follow((5,3));enter('Vidra_CoastalRoad');assert pos()==(20,10)
print('PASS: entire cave route works in reverse',flush=True)

# Reuse the game's native call bridge to check compiled Fly, Surf and shop data.
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
heals=json.loads((m.root/'src/data/heal_locations.json').read_text())['heal_locations'];hid=next(i+1 for i,v in enumerate(heals) if v['id']=='HEAL_LOCATION_QUANTUM_COASTAL_CITY')
assert struct.unpack('<bbhh',m.read(native('GetHealLocation',hid),6))==(*ids['Corvala_Town'],31,26)
print('PASS: compiled Fly/heal location matches the new Center',flush=True)
fixture=b'\x23'+struct.pack('<I',(m.symbols['ScrCmd_createmon']|1)+0x2000000)+struct.pack('<BBHHI',0,6,131,25,0)+b'\x02';m.inject(fixture)
bs=struct.unpack('<'+'H'*(w*h),raw);shore=set(manifest['shoreline']['generated_metatiles']);candidates=[]
for y in range(1,h-1):
 for x in range(1,w-1):
  b=bs[y*w+x]
  if b&0xc00 or b>>12!=3 or b&1023 not in shore:continue
  for (dx,dy),key in keys.items():
   v=bs[(y+dy)*w+x+dx]
   if v&1023==0x12b and not v&0xc00:candidates.append((x,y,dx,dy,key))
for i,target in enumerate([(7,35),(25,55),(56,45)]):
 x,y,dx,dy,key=min(candidates,key=lambda p:abs(p[0]-target[0])+abs(p[1]-target[1]))
 warp('Corvala_Town',x,y);m.press(key,30);assert pos()==(x,y)
 assert native('IsPlayerFacingSurfableFishableWater')==1
 m.write(m.symbols['gFieldEffectArguments'],b'\0'*4);native('FieldEffectStart',10);m.run(500)
 assert pos()==(x+dx,y+dy) and m.read(m.symbols['gPlayerAvatar'],1)[0]&8
 m.snap('surf-'+str(i));m.keys.add(keys[(-dx,-dy)]);m.run(12);m.keys.clear();m.run(90)
 assert pos()==(x,y) and not m.read(m.symbols['gPlayerAvatar'],1)[0]&8
print('PASS: native Surf launch/landing at three new shoreline points',flush=True)
warp('Corvala_Town',24,46);phases=set()
for _ in range(16):m.run(8);phases.add(m.read(0x06000000+464*32,18*32))
assert len(phases)==8
print('PASS: all eight native shoreline animation phases',flush=True)
warp('Corvala_Mart',4,6);follow((4,3));m.press(6,30);m.press(8,120);m.press(8,120);m.press(8,180);m.snap('mart-shopping')
callback=struct.unpack('<I',m.read(m.symbols['gMain']+4,4))[0]
assert callback==m.symbols['CB2_BuyMenu']|1,('Mart Buy menu not active',hex(callback))
print('PASS: clerk opens the working Buy menu',flush=True)
print('PASS: Corvala cave-cove gameplay checks',flush=True)
