"""Verify lever frames and collision in mGBA during the complete gym route."""
import struct
from PIL import Image
import havora_emulator_support as m
original_run=m.run
seen={}; frames=[]; previous=None; restorations=0; pending=None

def entry(x,y):
 width,height,address=struct.unpack('<iiI',m.read(m.symbols['VMap'],12))
 return struct.unpack('<H',m.read(address+2*((y+7)*width+x+7),2))[0]

def run(count):
 global previous,restorations,pending
 for _ in range(count):
  original_run(1)
  active=None
  for i in range(16):
   t=m.read(m.symbols['gTasks']+i*40,40)
   if not t[4] or struct.unpack_from('<I',t)[0]!=(m.symbols['MoveBoat']|1):continue
   d=struct.unpack_from('<16h',t,8)
   if d[0] not in (2,3) or not d[10]:continue
   x,y,base=d[8:11];tile=entry(x,y);mid=tile&1023
   active=(x,y,base)
   # The 4,320-cell redraw can span a video frame; its base copy is not
   # displayed until DrawWholeMapView commits the finished overlay.
   if not 0x3a0+(base-0x300)*3<=mid<=0x3a2+(base-0x300)*3:continue
   assert tile&0x400,('lever lost collision',hex(tile))
   seen.setdefault(d[0],set()).add((mid-0x3a0)%3)
   active=(x,y,base)
   if d[0]==2 and len(frames)<28 and d[5]%4==0:
    frames.append(m.screen.resize((720,480),Image.Resampling.NEAREST).copy())
  if previous and not active:pending=(*previous,0)
  if pending:
   x,y,base,age=pending
   if entry(x,y)&1023==base:restorations+=1;pending=None
   else:
    assert age<30,('lever did not return to neutral',pending,hex(entry(x,y)))
    pending=(x,y,base,age+1)
  previous=active
m.run=run
exec(compile((m.root/'tests/havora_three_lock_emulator.py').read_text(),'three-lock-route','exec'))
assert seen=={2:{0,1,2},3:{0,1,2}},seen
assert restorations>=14,restorations
out=m.root/'docs/havora/review/lever-animation.gif'
frames[0].save(out,save_all=True,append_images=frames[1:],duration=80,loop=0)
print('PASS native lever animation: all three poses, blocking collision and neutral restoration; water and mooring controls',flush=True)
