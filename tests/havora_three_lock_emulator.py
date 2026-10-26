"""Walk and sail the full solver route in mGBA, checking each native saved state."""
import os,pathlib,struct,subprocess,json,importlib.util
from collections import deque
import havora_emulator_support as m
source=(m.root/'tests/avatar_wardrobe_emulator.py').read_text();exec(source[source.index('native_dir ='):source.index('avatar_var = native')])
if hasattr(m,'record_step'):
 original_native=native
 def native(name,*args):
  old=getattr(m,'pause_capture',False);m.pause_capture=name!='HavoraGym_Control'
  try:return original_native(name,*args)
  finally:m.pause_capture=old
 m.record_stateaddr=native('GetVarPointer',0x40d7)
 m.record_stateoffset=m.record_stateaddr-struct.unpack('<I',m.read(m.symbols['gSaveBlock1Ptr'],4))[0]
spec=importlib.util.spec_from_file_location('geo',m.root/'tools/havora/build_fixed_transfer_gym.py');geo=importlib.util.module_from_spec(spec);spec.loader.exec_module(geo)
plan=json.loads((m.root/'docs/havora/fixed-transfer-design.json').read_text())
groups=json.loads((m.root/'data/maps/map_groups.json').read_text());ids={n:(g,i) for g,k in enumerate(groups['group_order']) for i,n in enumerate(groups[k])}
anchors=geo.ANCHORS
actors=geo.ACTORS
state=((2,2,0),0,0,4,0,False)
def encode(s):
 w,p,a,b,mo,r=s;return 0x8000|w[0]+3*w[1]+9*w[2]|a<<5|b<<8|mo<<11|int(r)<<13
def value(v):return native('VarGet',v)&65535
def pos():
 i=m.read(m.symbols['gPlayerAvatar']+5,1)[0];x,y=struct.unpack('<hh',m.read(m.symbols['gObjectEvents']+i*36+16,4));return x-7,y-7
def warp(x,y):
 g,n=ids['QuantumHavoraGym'];m.inject(b'\x39'+struct.pack('<BBBHH',g,n,255,x,y)+b'\x6b\x02');m.run(100)
def command(cmd,a=0,b=0):
 for v,n in [(0x8004,cmd),(0x8005,a),(0x8006,b)]:native('VarSet',v,n)
 native('HavoraGym_Control')
 for _ in range(5000):
  if not m.read(m.symbols['gPlayerAvatar']+6,1)[0]:break
  m.run(1)
 else:raise AssertionError('machinery task timed out')
 m.run(20)
 return value(0x800d)
def route(target):
 tiles=geo.draw(state);start=pos();q=deque([start]);pr={start:None}
 while q:
  x,y=q.popleft()
  if (x,y)==target:break
  z=tiles[y*geo.W+x]>>12
  for xx,yy in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
   if not(0<=xx<geo.W and 0<=yy<geo.H) or (xx,yy) in pr or (xx,yy) in actors:continue
   t=tiles[yy*geo.W+xx];zz=t>>12
   if t&0xc00 or (z not in (0,15) and zz not in (0,15) and z!=zz):continue
   pr[(xx,yy)]=(x,y);q.append((xx,yy))
 assert target in pr,('no walking route',state,start,target)
 path=[];v=target
 while pr[v] is not None:path.append(v);v=pr[v]
 for x,y in reversed(path):
  for attempt in range(3):
   px,py=pos();key=7 if x>px else 6 if x<px else 5 if y>py else 4
   m.press(key,20)
   if pos()==(x,y):break
  assert pos()==(x,y),('walk blocked',state,(px,py),(x,y),pos())
def beside(x,y):
 tiles=geo.draw(state)
 for xx,yy in [(x,y+1),(x,y-1),(x-1,y),(x+1,y)]:
  if not(tiles[yy*geo.W+xx]&0xc00) and (xx,yy) not in actors:
   try:route((xx,yy));return
   except AssertionError as e:
    if str(e).startswith("('no walking route'"):continue
    raise
 raise AssertionError(('console inaccessible',x,y))
native('VarSet',0x40d7,encode(state));native('VarSet',0x40d8,63);native('VarSet',0x40d9,0)
warp(*geo.ENTRY);assert pos()==geo.ENTRY,pos();m.snap('three-lock-entry')
for i,step in enumerate(plan['shortest_solution'],1):
 action=step['action'];nextstate=step['state'];w,p,a,b,mo,r=state
 if hasattr(m,'record_step'):m.record_step(i,action,state)
 print('STEP',i,action,'from',pos(),flush=True)
 if action.startswith('Ride'):
  boat=int(action.startswith('Ride cargo'));dest=nextstate[1]
  route((geo.SHORE[p],geo.BERTH_ROW+3*boat))
  command(11,boat,dest)
  expected=(geo.SHORE[dest],geo.BERTH_ROW+3*boat)
  assert pos()==expected,('ride endpoint',i,pos(),expected)
 elif action.startswith('Transfer'):
  src='ABC'.index(action.split()[1]);dst='ABC'.index(action.split()[3]);kind=('AB' if {src,dst}=={0,1} else 'BC')+('Forward' if src<dst else 'Reverse')
  console=next(c for c in geo.consoles if c[0]==p and c[3]==kind);beside(console[1],console[2]);command(10,src,dst)
 elif action.startswith('Walk'):route(anchors[nextstate[1]])
 elif action.startswith('Secure') or action.startswith('Release cargo'):
  beside(52,5);command(12)
 elif action.startswith('Release captain'):
  beside(39,14);command(13)
 elif action.startswith('Tension'):
  beside(78,6);command(14)
 else:raise AssertionError(action)
 state=(tuple(nextstate[0]),*nextstate[1:])
 assert value(0x40d7)==encode(state),('state mismatch',i,action,hex(value(0x40d7)),hex(encode(state)))
 if i in [5,9,10,17,22,23,25]:m.snap('three-lock-step-'+str(i))
print('PASS full 25-action solution with actual walking, ladders and both boat rides',flush=True)
if hasattr(m,'recording'):m.recording=False
assert state[1]==7
# Re-entry uses the saved configuration, then a machinery reset preserves victories.
warp(*anchors[7]);assert value(0x40d7)==encode(state)
native('VarSet',0x40d8,63);command(6);assert value(0x40d9)&1
command(15);assert value(0x40d7)==encode(((2,2,0),0,0,4,0,False)) and value(0x40d8)==63
warp(3,27);m.keys.add(5);m.run(15);m.keys.clear();m.run(180)
save=struct.unpack('<I',m.read(m.symbols['gSaveBlock1Ptr'],4))[0]
assert tuple(m.read(save+4,2))==ids['HavoraWestQuadrant'],'exit warp'
print('PASS saved configuration, crest award, reset preserving victories and exterior exit',flush=True)
# Old gym saves are relocated to the safe entry while retaining their victories.
native('VarSet',0x40d7,0);warp(20,33)
assert pos()==geo.ENTRY,('legacy migration position',pos())
assert value(0x40d8)==63 and value(0x40d7)==encode(((2,2,0),0,0,4,0,False))
def active(name):
 addr=m.symbols[name]|1
 return any(t[4] and struct.unpack_from('<I',t)[0]==addr for t in [m.read(m.symbols['gTasks']+i*40,40) for i in range(16)])
# Real A-button boarding and native destination menu, selecting B west quay.
warp(4,10);m.press(7,20);m.press(8,180)
assert active('Task_HandleMultichoiceInput'),'boarding menu did not open'
m.press(5,20);m.press(5,20);m.press(8,30)
for _ in range(5000):
 if not m.read(m.symbols['gPlayerAvatar']+6,1)[0]:break
 m.run(1)
m.run(80)
assert pos()==(31,10),('destination menu ride',pos())
assert value(0x40d7)==encode(((2,2,0),2,2,4,0,False))
# Real valve Yes/No prompt and transfer; invalid receiver/donor leaves save intact.
warp(28,6);m.press(4,20);m.press(8,600)
assert active('Task_YesNoMenu_HandleInput'),'valve prompt did not open'
m.press(8,30)
for _ in range(5000):
 if not m.read(m.symbols['gPlayerAvatar']+6,1)[0]:break
 m.run(1)
else:raise AssertionError('valve transfer timed out')
m.run(80)
assert value(0x40d7)==encode(((2,1,1),2,2,4,0,False)),'valve A interaction failed'
before=value(0x40d7);assert command(10,0,1)==3,'B station operated A/B valve'
assert value(0x40d7)==before
print('PASS legacy save migration, actual boat menu, valve Yes/No prompt and invalid-operation rejection',flush=True)

# Reset through the real lever prompt, including its scripted relocation.
warp(29,6);m.press(4,20);m.press(8,600)
assert active('Task_YesNoMenu_HandleInput'),'reset confirmation missing'
m.press(8,600);m.run(240)
assert pos()==geo.ENTRY,('reset warped outside the shorter map',pos())
assert value(0x40d8)==63
print('PASS actual reset prompt returns to the authored entrance and retains crew victories',flush=True)
