"""Exercise the solved water trial, transport, save migration, and all eight battles in mGBA."""
from pathlib import Path
source=Path(__file__).with_name('havora_artwork_review_emulator.py').read_text()
exec(compile(source[:source.index("native('VarSet',0x40d8")],'tidal-setup','exec'))
from collections import deque
spec=json.loads((m.root/'tools/havora/tidal_trial.json').read_text());P=spec['platforms'];L=spec['links']
plan=json.loads((m.root/'build/havora-tests/tidal-solution.json').read_text())
def encode(w):return 0x8000+w[0]+3*w[1]+9*w[2]
def pos():
 i=m.read(m.symbols['gPlayerAvatar']+5,1)[0]
 x,y=struct.unpack('<hh',m.read(m.symbols['gObjectEvents']+i*36+16,4));return x-7,y-7
def walk_to(target,w):
 b=geo.draw((w,0,0,4,0,False));solid={tuple(p['npc']) for p in P}
 if w[2]==0:solid.add((65,20))
 start=pos();q=deque([start]);prev={start:None};end=None
 while q:
  x,y=q.popleft()
  if abs(x-target[0])+abs(y-target[1])==1:end=(x,y);break
  z=b[y*80+x]>>12
  for xx,yy in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
   if not(0<=xx<80 and 0<=yy<27) or (xx,yy) in prev or (xx,yy) in solid:continue
   t=b[yy*80+xx];nz=t>>12
   if t&0xc00 or z not in (0,15) and nz not in (0,15) and z!=nz:continue
   prev[xx,yy]=(x,y);q.append((xx,yy))
 assert end is not None,('no walking route',start,target,w)
 path=[]
 while prev[end] is not None:path.append(end);end=prev[end]
 for x,y in reversed(path):
  for _ in range(3):
   px,py=pos();m.press(7 if x>px else 6 if x<px else 5 if y>py else 4,22)
   if pos()==(x,y):break
  assert pos()==(x,y),('real walking route blocked',pos(),(x,y),w)
 return len(path)
def setwater(w):native('VarSet',0x40d7,encode(w));native('HavoraGym_OnResume')
def stage(x,y):warp(x,y);assert pos()==(x,y)
def visible(local):
 return native('GetObjectEventIdByLocalIdAndMap',local,ids['Havora_Gym'][1],ids['Havora_Gym'][0])<16
# Migrate legacy unfinished saves to all LOW without losing trainer clearance.
native('VarSet',0x40d8,1);native('VarSet',0x40da,0);native('VarSet',0x40d7,0x4400);warp()
assert value(0x40d7)==encode((0,0,0)) and value(0x40d8)==1
assert_map((0,0,0));assert command(24)==2
native('VarSet',0x40d8,0)
print('PASS legacy save migration; all LOW artwork; captain locked before all stations',flush=True)
# Replay the independently solved rules against compiled C, staging at each real control/pad.
w=(0,0,0)
for action,state in plan:
 kind=action[0]
 if kind in ('switch','battle'):
  n=action[1];target=P[n]['switches'][action[2]] if kind=='switch' else P[n]['npc']
  b=geo.draw((w,0,0,4,0,False));solid={tuple(a['npc']) for a in P}
  adj=[(target[0]+dx,target[1]+dy) for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)] if 0<=target[0]+dx<80 and 0<=target[1]+dy<27]
  at=next((x,y) for x,y in adj if not b[y*80+x]&0xc00 and (x,y) not in solid)
  stage(*at)
  if kind=='switch':assert command(30,n,action[2])==1,('valid switch rejected',action,w,pos())
  else:
   assert command(32,n)==1,('trainer puzzle requirements rejected',action,w)
   assert command(22,P[n]['victory'])==1
 elif kind=='travel':
  link=L[action[1]];src=link['pad_from'] if action[2] else link['pad_to'];dest=link['pad_to'] if action[2] else link['pad_from']
  stage(*src);assert command(31)==1,('valid transport rejected',action,w,pos())
  assert [value(0x8008),value(0x8009)]==dest
  stage(*dest)
 elif kind=='reset':
  assert command(15)==1;stage(3,25)
 else:
  count=walk_to(P[action[1]]['npc'],w);print('PASS actual LOW C crossing:',count,'walking steps',flush=True)
 w=tuple(state[0]);assert value(0x40d7)==encode(w),(action,value(0x40d7),w)
 assert value(0x40d8)==state[2] and value(0x40da)==state[3]
 assert_map(w)
print('PASS complete 28-action native solution; seven compulsory switch stations and crew clearances',flush=True)
# Failed/no-op switches do not count; wrong recipes and underwater transports fail.
native('VarSet',0x40d8,0);native('VarSet',0x40da,0);setwater((0,0,0));stage(2,4)
assert command(30,0,1)==7 and value(0x40da)==0
stage(2,3);assert command(30,0,0)==1
setwater((2,0,0));assert command(30,0,0)==7
assert command(32,0)==7
stage(4,8);assert command(31)==2
native('VarSet',0x40d8,251);native('VarSet',0x40da,127)
setwater((2,2,2));stage(24,16);assert command(31)==7
setwater((1,2,1));stage(31,11);assert command(31)==7
setwater((1,1,0));stage(58,8);assert command(31)==7
print('PASS no-op/remote switch protection, trainer recipe enforcement, clearance and submerged-pad guards',flush=True)
# Captain gate independently rejects every missing crew or switch, regardless of physical shortcuts.
setwater((1,1,0))
for p in P:
 native('VarSet',0x40d8,251^p['victory']);assert command(24)==2
native('VarSet',0x40d8,251)
for n in range(7):
 native('VarSet',0x40da,127^(1<<n));assert command(24)==2
native('VarSet',0x40da,127)
# Water occludes NPCs and saves/re-entry retain puzzle state and clearances.
for levels in [(0,0,0),(1,1,1),(2,2,2),(1,1,0)]:
 setwater(levels);warp(3,6);assert_map(levels)
 warp(66,20);assert visible(7)==(levels[2]==0),('captain visibility',levels)
 warp(40,10);assert visible(9)==(levels[1]!=2),('island visibility',levels)
 warp(4,24);assert visible(1)==(levels[0]==0),('steward visibility',levels)
 assert value(0x40d8)==251 and value(0x40da)==127
assert command(15)==1;assert value(0x40d7)==encode((0,0,0));assert value(0x40d8)==251 and value(0x40da)==127
print('PASS every captain bypass rejected; captain/island/steward occlusion; reset and re-entry retain victories',flush=True)
# Real scripted transport (dialogue, yes/no and same-map warp) reaches the selected pad.
setwater((1,1,0));stage(24,16)
m.inject(b'\x05'+struct.pack('<I',m.symbols['HavoraTide_Travel']))
for _ in range(18):
 m.press(8,50)
 if pos()==(30,16):break
assert pos()==(30,16),('scripted MID lock lift failed',pos())
print('PASS actual dialogue-to-warp MID landing transport',flush=True)
# Preserve the real MID stair walk check after replacing all puzzle logic.
for path in [[(25,12),(26,12),(26,13),(26,14),(25,14),(24,14),(24,15),(24,16)],[(29,12),(28,12),(28,13),(28,14),(29,14),(30,14),(30,15),(30,16)]]:
 stage(*path[0])
 for x,y in path[1:]:
  for attempt in range(3):
   px,py=pos();m.press(7 if x>px else 6 if x<px else 5 if y>py else 4,22)
   if pos()==(x,y):break
  assert pos()==(x,y),('MID stair walk blocked',pos(),(x,y))
print('PASS real walking on both required MID stair-to-pad routes',flush=True)
# Launch every actual doubles script; victories above are fixture state, not battle flags.
setwater((1,1,0));stage(65,21)
fixture=b''
for species in [131,68,131,68,131,68]:fixture+=b'\x23'+struct.pack('<I',(m.symbols['ScrCmd_createmon']|1)+0x2000000)+struct.pack('<BBHHI',0,6,species,60,0)
m.inject(fixture+b'\x02')
assert command(24)==1
size=m.lib.retro_serialize_size();snap=m.c.create_string_buffer(size);assert m.lib.retro_serialize(snap,size)
for name,count in [('Harbormaster',2),('Crew',2),('Diver',4),('Lockkeeper',3),('Engineer',3),('FirstMate',4),('Navigator',3),('Captain',6)]:
 assert m.lib.retro_unserialize(snap,size)
 m.inject(b'\x05'+struct.pack('<I',m.symbols['HavoraTrial_'+name]))
 for _ in range(18):
  m.press(8,120)
  if m.read(m.symbols['gBattlersCount'],1)==b'\x04':break
 flags=struct.unpack('<I',m.read(m.symbols['gBattleTypeFlags'],4))[0]
 assert flags&1 and m.read(m.symbols['gBattlersCount'],1)==b'\x04',('double battle did not launch',name)
 assert m.read(m.symbols['gEnemyPartyCount'],1)==bytes([count]),('wrong party',name)
 print('PASS real double battle:',name,count,'opponents',flush=True)
assert m.lib.retro_unserialize(snap,size)
# Missing/full-party requirement and reward regressions.
native('VarSet',0x40d8,255);assert command(6)==0;assert value(0x40d9)&1
print('PASS crest reward remains tied to captain victory',flush=True)
