"""Exercise the installed Counterweight Grove using native overworld movement.

The test enables the existing Strength flag and uses the native removeobject
command for Cut results, isolating puzzle logic from party/badge prerequisites.
All boulder moves, pits, pressure plates and gate updates run in the real ROM.
"""
import json,re,struct,subprocess
from collections import deque
from pathlib import Path
import havora_emulator_support as m
R=m.root
plan=json.loads((R/'tools/havora/counterweight-puzzle.json').read_text())
# SaveBlock1 has grown in Quantum; compile offsets rather than trusting the
# original FireRed layout comments.
probe=R/'build/havora-tests/puzzle-layout.c'
probe.write_text('#include "global.h"\nconst u32 offsets[]={__builtin_offsetof(struct SaveBlock1,vars),__builtin_offsetof(struct SaveBlock1,flags),sizeof(struct ObjectEvent)};\n')
subprocess.run(['arm-none-eabi-gcc','-c','-iquote',str(R/'include'),'-iquote',str(R/'gflib'),'-DFIRERED',str(probe),'-o',str(probe.with_suffix('.o'))],check=True)
subprocess.run(['arm-none-eabi-objcopy','-O','binary','-j','.rodata',str(probe.with_suffix('.o')),str(probe.with_suffix('.bin'))],check=True)
VAR_OFFSET,FLAG_OFFSET,OBJECT_SIZE=struct.unpack('<III',probe.with_suffix('.bin').read_bytes())
assert OBJECT_SIZE==36

raw=(R/'include/constants/map_groups.h').read_text();num,group=map(int,re.search(r'#define MAP_HAVORA_NORTH_QUADRANT\s+\((\d+) \| \((\d+) << 8\)\)',raw).groups())
flags=(R/'include/constants/flags.h').read_text();sysbase=int(re.search(r'#define SYS_FLAGS[^\n]*//\s*(0x[0-9A-Fa-f]+)',flags)[1],16);strength=sysbase+int(re.search(r'#define FLAG_SYS_USE_STRENGTH\s+\(SYS_FLAGS \+ (0x[0-9A-Fa-f]+)\)',flags)[1],16)
def saveptr():return struct.unpack('<I',m.read(m.symbols['gSaveBlock1Ptr'],4))[0]
def flag(n,value=True):
 addr=saveptr()+FLAG_OFFSET+n//8;b=m.read(addr,1)[0];m.write(addr,bytes([(b|(1<<(n%8))) if value else (b&~(1<<(n%8)))]))
def var(n):return struct.unpack('<H',m.read(saveptr()+VAR_OFFSET+(n-0x4000)*2,2))[0]
def pack(p):return p[0]|p[1]<<8
def rockvars():return [var(0x40d0+i) for i in range(6)]
def player():
 i=m.read(m.symbols['gPlayerAvatar']+5,1)[0];x,y=struct.unpack('<hh',m.read(m.symbols['gObjectEvents']+i*36+16,4));return x-7,y-7
def tile(p):
 width,height,ptr=struct.unpack('<iiI',m.read(m.symbols['VMap'],12));return struct.unpack('<H',m.read(ptr+2*((p[1]+7)*width+p[0]+7),2))[0]
def warp(p):
 m.inject(b'\x39'+struct.pack('<BBBHH',group,num,255,*p)+b'\x6b\x02');m.run(120);assert player()==tuple(p),(player(),p);flag(strength)
def snapshot():
 size=m.lib.retro_serialize_size();buf=m.c.create_string_buffer(size);assert m.lib.retro_serialize(buf,size);return buf

def weighted():return [pack(p) in rockvars() for p in plan['plates']]
def check_world():
 vals=rockvars();state=var(0x40d6);holes=state>>3&7;weights=weighted();opened=[weights[0],weights[1],holes==7 and all(weights[1:])]
 for p,o in zip(plan['gates'],opened):
  v=tile(p);assert v&1023==(0x232 if o else 0x231),(p,'gate art',hex(v),o);assert bool(v&0xc00)==(not o),(p,'gate collision')
 for i,p in enumerate(plan['holes']):
  v=tile(p);done=holes>>i&1;assert v&1023==(0 if done else 0x22e),(p,'pit art');assert bool(v&0xc00)==(not done),(p,'pit collision')
 for p,o in zip(plan['plates'],weights):assert tile(p)&1023==(0x230 if o else 0x22f),(p,'plate art')
 return opened

def active_objects():
 out=[]
 for i in range(16):
  b=m.read(m.symbols['gObjectEvents']+i*36,36)
  if b[0]&1 and b[9]==num and b[10]==group:out.append((b[8],struct.unpack('<hh',b[16:20])))
 return out

def route(dest):
 start=player();blocked={tuple(p) for p in plan['trees'] if not (var(0x40d6)>>(plan['trees'].index(p))&1)}
 blocked|={(v&255,v>>8) for v in rockvars() if v!=65535}
 for lid,(x,y) in active_objects():
  if lid!=255 and not 11<=lid<=19:blocked.add((x-7,y-7))
 q=deque([start]);prev={start:None}
 while q:
  p=q.popleft()
  if p==dest:
   out=[]
   while prev[p] is not None:out.append(p);p=prev[p]
   return out[::-1]
  for dx,dy in [(0,-1),(1,0),(0,1),(-1,0)]:
   n=p[0]+dx,p[1]+dy
   if n in prev or n in blocked or not(0<=n[0]<92 and 0<=n[1]<28):continue
   v=tile(n)
   if not v&0xc00 and v>>12==6:prev[n]=p;q.append(n)
 raise AssertionError(('No route',start,dest))
keys={(0,-1):4,(0,1):5,(-1,0):6,(1,0):7}
def walk(dest):
 for n in route(tuple(dest)):
  p=player();key=keys[n[0]-p[0],n[1]-p[1]];m.keys.add(key)
  for _ in range(100):
   m.run(1)
   if player()==n:break
  else:raise AssertionError(('walk blocked',p,n))
  m.keys.clear();m.run(20)
 assert player()==tuple(dest)

warp(plan['start']);assert rockvars()==list(map(pack,plan['boulders']));assert var(0x40d6)==0x5a00;check_world();m.snap('grove-initial')
initial=snapshot();captures=[]
for index,action in enumerate(plan['solution']):
 if action['action']=='cut':
  p=tuple(action['from']);neigh=[(p[0]+dx,p[1]+dy) for dx,dy in keys]
  for stand in neigh:
   try:walk(stand);break
   except AssertionError:continue
  else:raise AssertionError(('cannot approach tree',p))
  tree_index=plan['trees'].index(list(p));lid=17+tree_index
  m.inject(b'\x53'+struct.pack('<H',lid)+b'\x02')
 else:
  a=tuple(action['from']);b=tuple(action['to']);dx,dy=b[0]-a[0],b[1]-a[1];walk((a[0]-dx,a[1]-dy));which=rockvars().index(pack(a));key=keys[dx,dy]
  if list(a)==plan['plates'][0]:
   # Place an ordinary NPC inside the gate using native script commands. A
   # plate release must be rejected until that actor has left the gate.
   checkpoint=snapshot();before=rockvars();table=(R/'data/script_cmd_table.inc').read_text()
   op=lambda name:int(re.search(r'script_cmd_table_entry SCR_OP_'+name+r'[^\n]*@ (0x[0-9a-fA-F]+)',table)[1],16)
   gx,gy=plan['gates'][0]
   m.inject(bytes([op('SETOBJECTXYPERM')])+struct.pack('<HHH',7,gx,gy)+bytes([op('ADDOBJECT')])+struct.pack('<H',7)+b'\x02')
   assert (7,(gx+7,gy+7)) in active_objects()
   m.keys.add(key);m.run(100);m.keys.clear();m.run(20)
   assert rockvars()==before and check_world()[0],'gate closed onto an actor'
   assert m.lib.retro_unserialize(checkpoint,len(checkpoint));m.run(5)
   print('PASS occupied-gate guard prevents closing on an NPC',flush=True)
  m.keys.add(key)
  for _ in range(150):
   m.run(1)
   if rockvars()[which]!=pack(a):break
  else:raise AssertionError(('native push failed',index,a,b,player(),rockvars()))
  m.keys.clear();m.run(45)
  expected=65535 if list(b) in plan['holes'] else pack(b)
  # Filled shafts later accept ordinary walking/pushing; solution consumes each once.
  assert rockvars()[which]==expected,(index,a,b,rockvars())
 assert var(0x40d6)&7==action['cut_mask'],(index,'cut mask')
 assert var(0x40d6)>>3&7==action['filled_mask'],(index,'pit mask')
 opened=check_world()
 if index==2:m.snap('grove-gate-a-open')
 if opened[1] and 'B' not in captures:m.snap('grove-gate-b-open');captures.append('B')
 print('action',index+1,action['action'],'PASS',flush=True)
 if index==12:
  # Re-enter the map with moved stones and Cut results. Native temp flags clear,
  # but the controller must restore progress rather than respawn original art.
  before=rockvars(),var(0x40d6);p=player();warp(p);assert (rockvars(),var(0x40d6))==before;check_world()
assert check_world()==[False,True,True]
walk(plan['goal']);m.snap('grove-forest-gate-open');print('PASS complete native boulder route, three filled pits, reversible gates, and map-reload persistence',flush=True)
# The documented shortcut opens a confirmation instead of resetting silently.
warp((20,27));before=rockvars(),var(0x40d6);m.keys.update({2,10,11});m.run(3);m.keys.clear();m.run(90);m.press(0);assert (rockvars(),var(0x40d6))==before;print('PASS cancelling reset preserves progress',flush=True)
m.keys.update({2,10,11});m.run(3);m.keys.clear();m.run(90);m.snap('grove-reset-confirmation');m.press(8);m.run(240)
assert player()==tuple(plan['start']);assert rockvars()==list(map(pack,plan['boulders']));assert var(0x40d6)==0x5a00;check_world();m.snap('grove-reset-complete')
print('PASS reset shortcut and confirmation restore all pieces, trees, pits, gates, plates and entrance position',flush=True)
