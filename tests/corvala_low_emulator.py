"""Corvala LOW: actual walking, reciprocal seams, Center and surf DMA (mGBA).

Use MGBA_CORE for a libretro core and ARM_NM for the matching toolchain.
Fixtures warp a fresh test game; they do not bypass collision during walking.
"""
import json, struct, os, subprocess
from collections import deque
import havora_emulator_support as m

m.d=m.root/'build/corvala/emulator';m.d.mkdir(parents=True,exist_ok=True)
groups=json.loads((m.root/'data/maps/map_groups.json').read_text())
ids={n:(g,i) for g,k in enumerate(groups['group_order']) for i,n in enumerate(groups[k])}
manifest=json.loads((m.root/'tools/corvala/map.json').read_text())
w,h=manifest['dimensions']
raw=(m.root/'data/layouts/Corvala_Town/map.bin').read_bytes()
blocks=struct.unpack('<'+'H'*(w*h),raw)

def map_id():
 p=struct.unpack('<I',m.read(m.symbols['gSaveBlock1Ptr'],4))[0]
 return tuple(m.read(p+4,2))

def pos():
 obj=m.symbols['gObjectEvents']+m.read(m.symbols['gPlayerAvatar']+5,1)[0]*36
 x,y=struct.unpack('<hh',m.read(obj+16,4))
 return x-7,y-7

def warp(name,x,y):
 group,num=ids[name]
 m.inject(b'\x39'+struct.pack('<BBBHH',group,num,255,x,y)+b'\x6b\x02')
 m.run(120)
 assert map_id()==ids[name] and pos()==(x,y),(name,'warp',map_id(),pos())

def step(key,expected=None):
 old=(map_id(),pos());m.keys.add(key)
 for _ in range(50):
  m.run(1)
  if (map_id(),pos())!=old:break
 m.keys.clear();m.run(32)
 assert (map_id(),pos())!=old,('blocked real step',key,old)
 if expected is not None:assert pos()==expected,('unexpected position',key,pos(),expected)

keys={(0,-1):4,(0,1):5,(-1,0):6,(1,0):7}
def follow(goal):
 start=pos();parents={start:None};q=deque([start])
 while q and goal not in parents:
  x,y=q.popleft()
  for dx,dy in keys:
   p=(x+dx,y+dy)
   if not(0<=p[0]<w and 0<=p[1]<h) or p in parents:continue
   if p==tuple(manifest['landmarks']['center_door']):continue
   block=blocks[p[1]*w+p[0]]
   if block&0xc00 or block>>12!=3:continue
   parents[p]=(x,y);q.append(p)
 assert goal in parents,('no route',start,goal)
 route=[];p=goal
 while p!=start:route.append(p);p=parents[p]
 for p in reversed(route):
  a=pos();step(keys[(p[0]-a[0],p[1]-a[1])],p)
 assert map_id()==ids['Corvala_Town']
 return len(route)

warp('Corvala_Town',1,26);m.snap('west-village')
# Confirm the engine loaded exactly the installed LOW, with its padded stride.
vm=m.read(m.symbols['VMap'],12);vw,vh,ptr=struct.unpack('<iiI',vm)
assert (vw,vh)==(w+15,h+14),(vw,vh)
for y in range(h):
 assert m.read(ptr+2*((y+7)*vw+7),w*2)==raw[y*w*2:(y+1)*w*2],('runtime map row',y)
print('PASS: ROM loads all 80x64 LOW blocks with correct padded stride',flush=True)

total=0
for name,x,y in manifest['buildings']:
 if name in manifest['house_doors']:
  total+=follow((x+manifest['house_doors'][name],y+6))
  m.snap('approach-'+name+'-'+str(x))
for name in ['cave_approach','reef_walk','arrival_pier','lighthouse_approach']:
 total+=follow(tuple(manifest['landmarks'][name]));m.snap(name)
print('PASS:',total,'real walking steps through village, bluff stairs, reef and lighthouse',flush=True)

for start,key,target,back in [((1,26),6,'Vidra_CoastalRoad',7),((78,27),7,'Vidra_HarborRoad',6)]:
 warp('Corvala_Town',*start)
 step(key);step(key);m.run(100)
 assert map_id()==ids[target],('outgoing seam',target,map_id(),pos())
 step(back);m.run(100)
 assert map_id()==ids['Corvala_Town'],('return seam',target,map_id(),pos())
print('PASS: west/east seamless crossings and both returns',flush=True)

warp('Corvala_Town',26,22)
m.keys.add(4);m.run(24);m.keys.clear();m.run(180)
assert map_id()==ids['Corvala_Town_PokemonCenter_1F'],('Center entry',map_id(),pos())
m.snap('center-interior')
m.keys.add(5);m.run(32);m.keys.clear();m.run(180)
assert map_id()==ids['Corvala_Town'] and pos()==(26,22),('Center return',map_id(),pos())
print('PASS: animated Center door and working return to relocated entrance',flush=True)

# Use the same native Surf effect as gameplay, with a test Lapras. Badge/party
# progression belongs to the field-tool tests; launch/landing physics matter here.
native_dir=m.d/'native';native_dir.mkdir(exist_ok=True)
native_addr=m.symbols['gDecompressionBuffer']+0x3000
result_addr=m.symbols['gDecompressionBuffer']+0x3f00
prefix=os.environ.get('ARM_NM','arm-none-eabi-nm').removesuffix('.exe').removesuffix('nm')
def native(name,*args):
 assembly=['.syntax unified','.thumb','.thumb_func','_start:','push {r4, lr}']
 assembly += [f'ldr r{i}, arg{i}' for i in range(len(args))]
 assembly += ['ldr r4, function','bl invoke','ldr r3, result','str r0, [r3]',
              'movs r0, #1','pop {r4, pc}','invoke:','bx r4','.align 2',
              f'function: .word {m.symbols[name]|1}',f'result: .word {result_addr}']
 assembly += [f'arg{i}: .word {a}' for i,a in enumerate(args)]
 (native_dir/'call.s').write_text('\n'.join(assembly)+'\n')
 subprocess.run([prefix+'as','-mthumb','-mcpu=arm7tdmi','-o',str(native_dir/'call.o'),str(native_dir/'call.s')],check=True)
 subprocess.run([prefix+'objcopy','-O','binary','-j','.text',str(native_dir/'call.o'),str(native_dir/'call.bin')],check=True)
 m.write(native_addr,(native_dir/'call.bin').read_bytes())
 m.inject(b'\x23'+struct.pack('<I',native_addr|1)+b'\x6b\x02')
 return struct.unpack('<I',m.read(result_addr,4))[0]

heals=json.loads((m.root/'src/data/heal_locations.json').read_text())['heal_locations']
heal_id=next(i+1 for i,v in enumerate(heals) if v['id']=='HEAL_LOCATION_QUANTUM_COASTAL_CITY')
landing=struct.unpack('<bbhh',m.read(native('GetHealLocation',heal_id),6))
assert landing==(*ids['Corvala_Town'],26,22),('compiled Fly landing',landing)
print('PASS: compiled Fly landing matches the relocated Center approach',flush=True)

fixture=b'\x23'+struct.pack('<I',(m.symbols['ScrCmd_createmon']|1)+0x2000000)
fixture+=struct.pack('<BBHHI',0,6,131,25,0)+b'\x02';m.inject(fixture)
def surfing():return bool(m.read(m.symbols['gPlayerAvatar'],1)[0]&8)
shore=set(manifest['shoreline']['generated_metatiles'])
candidates=[]
for y in range(1,h-1):
 for x in range(1,w-1):
  b=blocks[y*w+x]
  if b&0xc00 or b>>12!=3 or b&1023 not in shore:continue
  for (dx,dy),key in keys.items():
   if blocks[(y+dy)*w+x+dx]&1023==0x12b:candidates.append((x,y,dx,dy,key))
launches=[(68,56,0,1,5)]
for target in [(6,36),(56,32)]:
 launches.append(min(candidates,key=lambda p:abs(p[0]-target[0])+abs(p[1]-target[1])))
for i,(x,y,dx,dy,key) in enumerate(launches):
 warp('Corvala_Town',x,y)
 m.keys.add(key);m.run(2);m.keys.clear();m.run(30)
 assert pos()==(x,y),('walked into sea without Surf',pos())
 assert native('IsPlayerFacingSurfableFishableWater')==1,('Surf unavailable',x,y)
 m.write(m.symbols['gFieldEffectArguments'],b'\0'*4)
 native('FieldEffectStart',10);m.run(500)
 assert surfing() and pos()==(x+dx,y+dy),('Surf launch',x,y,pos(),surfing())
 m.snap('surf-launch-'+str(i))
 m.keys.add(keys[(-dx,-dy)]);m.run(12);m.keys.clear();m.run(90)
 assert not surfing() and pos()==(x,y),('Surf landing',x,y,pos(),surfing())
print('PASS: native Surf launch and landing at the pier and two beach edges',flush=True)

# Read the actual emulated primary tile VRAM, covering all native surf phases.
warp('Corvala_Town',21,45);frames=[];phases=set()
for _ in range(16):
 m.run(8);phases.add(m.read(0x06000000+464*32,18*32));frames.append(m.screen.copy())
assert len(phases)==8,('surf DMA phases',len(phases))
frames[0].save(m.d/'native-shoreline.gif',save_all=True,append_images=frames[1:],duration=134,loop=0)
print('PASS: eight actual native shoreline VRAM animation phases',flush=True)
print('PASS: Corvala LOW gameplay checks',flush=True)
