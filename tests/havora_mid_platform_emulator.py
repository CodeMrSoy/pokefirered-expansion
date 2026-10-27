"""Walk the authored MID landings, verify independent tides and record review."""
from pathlib import Path
source=Path(__file__).with_name('havora_artwork_review_emulator.py').read_text()
exec(compile(source[:source.index("native('VarSet',0x40d8")],'mid-platform-setup','exec'))
from PIL import ImageDraw
import itertools
out=m.root/'docs/havora/review';out.mkdir(parents=True,exist_ok=True)
def pos():
 i=m.read(m.symbols['gPlayerAvatar']+5,1)[0]
 x,y=struct.unpack('<hh',m.read(m.symbols['gObjectEvents']+i*36+16,4));return x-7,y-7
native('VarSet',0x40d7,encode((1,1,0)))
for path in [[(25,12),(26,12),(26,13),(26,14),(25,14),(24,14),(24,15),(24,16)],[(29,12),(28,12),(28,13),(28,14),(29,14),(30,14),(30,15),(30,16)]]:
 warp(*path[0]);assert_map((1,1,0))
 for x,y in path[1:]:
  for attempt in range(3):
   px,py=pos();m.press(7 if x>px else 6 if x<px else 5 if y>py else 4,22)
   if pos()==(x,y):break
  assert pos()==(x,y),('MID landing walk blocked',pos(),(x,y))
print('PASS actual MID walking: both authored ladders to their boarding pads',flush=True)
# Review camera only: the hidden player is stationary over the divider.
native('VarSet',0x40d7,encode((0,0,0)));warp(27,15);native('SetObjectInvisibility',255,0,0,1)
original=m.run;frames=[];clock=0;capture=False;caption='LOW / LOW'
def take():
 frame=m.screen.resize((720,480),m.Image.Resampling.NEAREST).copy();d=ImageDraw.Draw(frame)
 d.rectangle((0,0,720,24),fill='black');d.text((8,6),'MID LANDINGS - '+caption,fill='white');frames.append(frame)
def run(count):
 global clock
 for _ in range(count):
  original(1);clock+=1
  if not capture or clock%12:continue
  for i in range(16):
   t=m.read(m.symbols['gTasks']+i*40,40)
   if t[4] and struct.unpack_from('<I',t)[0]==m.symbols['AnimateTide']|1:take();break
m.run=run;take();current=[0,0,0];capture=True
for target in [1,2,1,0]:
 for ch in [0,1]:
  caption='SECTION '+str(ch+1)+' TO '+['LOW','MID','HIGH'][target]
  assert command(26,ch,target)==1;current[ch]=target;assert_map(current);take()
capture=False
frames[0].save(out/'water-mid-platforms-cycle.gif',save_all=True,append_images=frames[1:],duration=110,loop=0,optimize=True)
print('PASS native LOW/MID/HIGH/MID/LOW fill/drain cycle for both new landings',flush=True)
for levels in itertools.product(range(3),repeat=3):
 native('VarSet',0x40d7,encode(levels));native('HavoraGym_OnResume');m.run(30);assert_map(levels)
native('VarSet',0x40d7,encode((0,0,0)));native('HavoraGym_OnResume')
print('PASS all 27 runtime maps, including switch-island and bunker profiles',flush=True)
