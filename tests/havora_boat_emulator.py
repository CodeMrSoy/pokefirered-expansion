"""Real no-warp sailings for the solved dam puzzle, with continuous movement checks."""
from pathlib import Path
src=Path(__file__).with_name('havora_tidal_trial_emulator.py').read_text()
exec(compile(src[:src.index('# Migrate legacy')],'boat-setup','exec'))
plan=json.loads((m.root/'build/havora-tests/directional-solution.json').read_text())
for tid in range(743,751):native('SetTrainerFlag',tid)
native('VarSet',0x40d7,encode((0,0,0)));native('VarSet',0x40d8,0);native('VarSet',0x40da,0);warp()
# Watch every emulator frame while the native boat task is active.
original_run=m.run;positions=[];boat_frames=0;last=None;record=False
from PIL import ImageDraw
frames=[];label=''
def run(count):
 global boat_frames,last
 for _ in range(count):
  original_run(1)
  if not record:continue
  active=False
  for i in range(16):
   t=m.read(m.symbols['gTasks']+i*40,40)
   if t[4] and struct.unpack_from('<I',t)[0]==m.symbols['MoveBoat']|1:
    active=True;phase=struct.unpack_from('<h',t,8)[0];break
  if not active:last=None;continue
  point=pos()
  if last is not None:assert abs(last[0]-point[0])+abs(last[1]-point[1])<=1,('boat teleported',last,point)
  last=point;positions.append(point);boat_frames+=phase==1
  if label and len(positions)%8==0:
   frame=m.screen.resize((720,480),m.Image.Resampling.NEAREST).copy();d=ImageDraw.Draw(frame);d.rectangle((0,0,720,28),fill='black');d.text((8,8),label,fill='white');frames.append(frame)
m.run=run;w=(0,0,0)
for action,state in plan:
 kind=action[0]
 if kind=='battle':assert command(22,P[action[1]]['victory'])==1
 elif kind=='switch':
  n,k=action[1:3];x,y=P[n]['switches'][k]
  stage(x+1,y) if n!=6 else stage(x,10)
  assert command(30,n,k)==1,(action,w,pos())
 elif kind=='travel':
  link=L[action[1]];stage(*link['pad_from']);record=True
  label=(link['source_label']+' -> '+link['destination_label']+' | boat sailing, no warp') if action[1] in (1,4) else ''
  block_before=struct.unpack('<I',m.read(m.symbols['gSaveBlock1Ptr'],4))[0]
  start_frames=boat_frames;assert command(31)==1,(action,w)
  assert pos()==tuple(link['pad_to']),('boat missed berth',action,pos())
  assert boat_frames>start_frames,('no visible sailing phase',action)
  assert struct.unpack('<I',m.read(m.symbols['gSaveBlock1Ptr'],4))[0]==block_before,'boat performed a map warp'
  record=False;label=''
  print('PASS continuous native sailing:',link['source_label'],'->',link['destination_label'],w,flush=True)
 elif kind=='walk':walk_to(P[action[1]]['npc'],w)
 w=tuple(state[0]);assert value(0x40d7)==encode(w);assert_map(w)
assert w[2]==0 and value(0x40d8)==251 and value(0x40da)==127
print('PASS complete boat-only solution, dam crossings, all crews/switches and LOW bunker',flush=True)
# Closed dams reject cross-section trips, including mixed MID/HIGH A/B.
native('VarSet',0x40d8,251);native('VarSet',0x40da,127)
for levels,index in [((0,0,0),1),((1,2,2),1),((2,1,1),1),((1,1,2),4),((2,2,1),4)]:
 setwater(levels);stage(*L[index]['pad_from']);record=True
 assert command(31)==7,(levels,index)
 record=False
print('PASS exposed dams block sailing; mixed A/B heights do not open its dam',flush=True)
if frames:
 out=m.root/'docs/havora/review/water-dam-boats.gif'
 frames[0].save(out,save_all=True,append_images=frames[1:],duration=134,loop=0,optimize=True)
 print('RECORDED',out,flush=True)
