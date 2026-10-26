"""Check only the section water presentation/access and produce two tide cycles."""
from pathlib import Path
source=Path(__file__).with_name('havora_artwork_review_emulator.py').read_text()
source=source[:source.index("native('VarSet',0x40d8")].replace('def warp(x=3,y=27):','def warp(x=3,y=25):')
exec(compile(source,'water-review-setup','exec'))
from PIL import ImageDraw
out=m.root/'docs/havora/review';out.mkdir(parents=True,exist_ok=True)
g,n=ids['Havora_Gym']
def captain():return native('GetObjectEventIdByLocalIdAndMap',7,n,g)&255
def hidden_player():native('SetObjectInvisibility',255,0,0,1)
native('VarSet',0x40d7,encode((0,0,0)));warp(66,20);hidden_player();assert captain()!=16
original=m.run;frames=[];caption='';clock=0;capture=False
def take(w,label):
 frame=m.screen.resize((720,480),m.Image.Resampling.NEAREST).copy();d=ImageDraw.Draw(frame);d.rectangle((0,0,720,24),fill='black');d.text((8,6),label,fill='white');frames.append(frame)
def run(count):
 global clock
 for _ in range(count):
  original(1);clock+=1
  if not capture or clock%12:continue
  for i in range(16):
   t=m.read(m.symbols['gTasks']+i*40,40)
   if t[4] and struct.unpack_from('<I',t)[0]==m.symbols['MoveBoat']|1 and struct.unpack_from('<h',t,8)[0]==4:
    take(None,caption);break
m.run=run
for ch,xy,name in [(2,(66,20),'bunker'),(1,(40,10),'island')]:
 native('VarSet',0x40d7,encode((0,0,0)));warp(*xy);hidden_player();frames=[]
 current=[0,0,0];take(current,name.upper()+' - LOW');capture=True
 for level in [1,2,1,0]:
  caption=name.upper()+' - '+['LOW','MID','HIGH'][current[ch]]+' to '+['LOW','MID','HIGH'][level]
  assert command(26,ch,level)==1;current[ch]=level;assert_map(current)
  if ch==2:assert (captain()==16)==(level!=0),('captain visibility',level,captain())
  take(current,name.upper()+' - '+['LOW','MID','HIGH'][level])
 capture=False
 frames[0].save(out/('water-'+name+'-cycle.gif'),save_all=True,append_images=frames[1:],duration=110,loop=0,optimize=True)
 print('PASS native '+name+' LOW/MID/HIGH/MID/LOW: exact tiles and captain visibility',flush=True)
# Hiding must survive camera/map re-entry, not just hide an already-spawned NPC.
for level in [1,2,0]:
 native('VarSet',0x40d7,encode((0,0,level)));warp(66,20);hidden_player()
 assert (captain()==16)==(level!=0),('captain on re-entry',level,captain());assert_map((0,0,level))
print('PASS submerged captain remains absent on re-entry and returns at LOW',flush=True)
# Complete RLE decode coverage, without changing puzzle controls or progression.
import itertools
for levels in itertools.product(range(3),repeat=3):
 native('VarSet',0x40d7,encode(levels));native('HavoraGym_OnResume');m.run(30);assert_map(levels)
native('VarSet',0x40d7,encode((0,0,0)));native('HavoraGym_OnResume')
print('PASS all 27 runtime section combinations exactly match authored profiles',flush=True)
