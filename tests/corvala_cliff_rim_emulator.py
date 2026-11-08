"""Fresh-game mGBA checks of the restarted Corvala cove and every doorway."""
import json,struct,os,subprocess
from collections import deque
import havora_emulator_support as m
m.d=m.root/'build/corvala/cliff-rim-emulator';m.d.mkdir(parents=True,exist_ok=True)
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

hour(11);native('DisableWildEncounters',1)
warp('Corvala_Town',49,16);check_phase('high');m.snap('high-cave-rim')
enter('Corvala_EntranceCave');enter('Corvala_Town');check_phase('high')
fixture=b'\x23'+struct.pack('<I',(m.symbols['ScrCmd_createmon']|1)+0x2000000)+struct.pack('<BBHHI',0,6,131,30,0)+b'\x02';m.inject(fixture)
follow((21,23));m.press(5,30);assert native('IsPlayerFacingSurfableFishableWater')==1
m.write(m.symbols['gFieldEffectArguments'],b'\0'*4);native('FieldEffectStart',10);m.run(500)
assert pos()==(21,24)
for point,key,label in [((30,10),4,'high-north-rim'),((61,25),7,'high-east-rim'),
                        ((39,10),4,'high-north-corner'),((59,18),7,'high-east-corner')]:
 follow(point,surf=True);m.press(key,40);assert pos()==point,('cliff collision',point,pos());m.snap(label)
follow((21,24),surf=True);m.keys.add(4);m.run(12);m.keys.clear();m.run(90);assert pos()==(21,23)
follow((31,26));hour(10);check_phase('low');m.snap('low-unchanged')
hour(11);check_phase('high')
print('PASS: final ROM renders both phases, north/east cliff collision, Surf return and cave entry/exit',flush=True)
