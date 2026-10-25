"""Record the verified mapped solution; automated controls/battles are labeled."""
import os,pathlib,struct,subprocess,runpy
from PIL import Image,ImageDraw,ImageFont
import havora_emulator_support as m
out=pathlib.Path('/workspace/scratch/53b0ac21dfa3/deliverables/havora-three-lock-puzzle.mp4')
ff=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s','960x640','-r','30','-i','-','-an','-c:v','libx264','-preset','fast','-crf','22','-pix_fmt','yuv420p','-movflags','+faststart',str(out)],stdin=subprocess.PIPE)
fp='/usr/share/fonts/truetype/dejavu/DejaVuSans';f=ImageFont.truetype(fp+'.ttf',16);small=ImageFont.truetype(fp+'.ttf',14);b=ImageFont.truetype(fp+'-Bold.ttf',18);title=ImageFont.truetype(fp+'-Bold.ttf',24)
ref=Image.open(m.root/'docs/havora/review/captains-trial-clean.png').convert('RGB').resize((216,146),Image.Resampling.NEAREST)
old_run=m.run;clock=0;frames=0;pose_frames=0;caption='';number=0;m.recording=False;m.pause_capture=False

def step(i,action,state):
 global caption,number
 caption=action;number=i;m.recording=True
m.record_step=step

def run(n):
 global clock,frames,pose_frames
 for _ in range(n):
  old_run(1);clock+=1
  if not m.recording or m.pause_capture or clock%4:continue
  im=Image.new('RGB',(960,640),'#122131');d=ImageDraw.Draw(im)
  d.text((18,10),'HAVORA — THREE-LOCK TRIAL',font=title,fill='white')
  d.text((18,48),f'{number:02}/25  '+caption,font=b,fill='#ffdc93')
  im.paste(m.screen.resize((720,480),Image.Resampling.NEAREST),(0,94));im.paste(ref,(732,100))
  d.text((734,257),'Layout reference',font=small,fill='#a9bfd0')
  save=struct.unpack('<I',m.read(m.symbols['gSaveBlock1Ptr'],4))[0]
  word=struct.unpack('<H',m.read(save+m.record_stateoffset,2))[0];v=word&31
  for i in range(16):
   task=m.read(m.symbols['gTasks']+i*40,40)
   if task[4] and struct.unpack_from('<I',task)[0]==m.symbols['MoveBoat']|1 and struct.unpack_from('<h',task,8)[0]==1 and struct.unpack_from('<h',task,22)[0]:
    sid=struct.unpack_from('<h',task,20)[0]-1;boat=m.read(m.symbols['gSprites']+sid*68,68)
    if boat[62]&4:continue
    oid=m.read(m.symbols['gPlayerAvatar']+5,1)[0];pid=m.read(m.symbols['gObjectEvents']+oid*36+35,1)[0];player=m.read(m.symbols['gSprites']+pid*68,68)
    px,py,px2,py2=struct.unpack_from('<hhhh',player,32)
    assert struct.unpack_from('<hhhh',boat,32)==(px,py+12,px2,py2)
    assert player[42]<4 and player[44]&64,'passenger walking during boat ride'
    pose_frames+=1
  for ch in range(3):
   w=v%3;v//=3;y=306+ch*57
   d.text((734,y),'ABC'[ch]+'  '+['LOW','MID','HIGH'][w],font=b,fill='#dceaf2')
   for j in range(3):d.rectangle((849+j*27,y+1,870+j*27,y+17),fill='#6bb4d6' if j<=w else '#314b5b')
  d.text((734,500),'Launch + cargo',font=f,fill='#ffdc93')
  d.text((734,527),'Four water units',font=f,fill='#dceaf2')
  d.text((18,589),'Actual emulator route: walking, ladders, boat travel and fixed water transfers.',font=f,fill='white')
  d.text((18,617),'2x speed  |  Automated controls  |  Battles preset as won  |  Idle pauses shortened',font=small,fill='#a9bfd0')
  ff.stdin.write(im.tobytes());frames+=1
m.run=run
try:
 runpy.run_path(str(m.root/'tests/havora_three_lock_emulator.py'),run_name='__main__')
finally:
 ff.stdin.close();code=ff.wait()
assert code==0
assert pose_frames>100
print('PASS standing passenger / smooth boat alignment on',pose_frames,'captured frames')
print('VIDEO',out,'seconds',frames/30,'bytes',out.stat().st_size)
