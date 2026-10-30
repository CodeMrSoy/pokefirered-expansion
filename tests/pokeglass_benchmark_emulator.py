#!/usr/bin/env python3
"""Frame-count PokéGlass response times and capture every app handoff in mGBA."""
import os
import ctypes as c
import json
import pathlib
import struct
import numpy as np
import quantum_qol_emulator as m
out=m.d/'pokeglass-benchmark';out.mkdir(exist_ok=True)
fixture=b''
for species in (1,4,7,25,133,143):
 fixture+=b'\x23'+struct.pack('<I',(m.symbols['ScrCmd_createmon']|1)+0x2000000)+struct.pack('<BBHHI',0,6,species,75,0)
fixture+=b'\x29'+struct.pack('<H',0x829)+b'\x44'+struct.pack('<HH',717,1)+b'\x02'
m.inject(fixture)
size=m.lib.retro_serialize_size()
def save():
 p=c.create_string_buffer(size);assert m.lib.retro_serialize(p,size);return p
def restore(p):assert m.lib.retro_unserialize(p,size)
def byte(name):return m.read(m.symbols[name],1)[0]
def task(name):
 if name not in m.symbols:return None
 tasks=m.read(m.symbols['gTasks'],640);fn=m.symbols[name]|1
 for i in range(16):
  if tasks[i*40+4] and struct.unpack_from('<I',tasks,i*40)[0]==fn:return i
 return None
def data(name,index):
 i=task(name)
 return struct.unpack('<h',m.read(m.symbols['gTasks']+i*40+8+2*index,2))[0] if i is not None else -1
def fade():return bool(m.read(m.symbols['gPaletteFade']+17,1)[0]&128)
def hub():return task('Task_PokeGlassHub') is not None and data('Task_PokeGlassHub',1)>=2 and not byte('sReturnCoverActive') and not fade()
def ready(name):
 if task(name) is None or fade():return False
 if name=='Task_HandleChooseMonInput' and byte('sReturnCoverActive'):return False
 if name in ('Task_PokeGlassStats','Task_PokeGlassPokedex'):return data(name,0)>=2
 if name=='Task_TrainerCard':
  p=struct.unpack('<I',m.read(m.symbols['sTrainerCardDataPtr'],4))[0]
  return m.read(p,1)[0]==10
 if name=='Task_OptionMenu':
  p=struct.unpack('<I',m.read(m.symbols['sOptionMenuPtr'],4))[0]
  return m.read(p+0x10,1)[0]>=2
 return True
shell=np.zeros((160,240),bool);shell[10:150,12:228]=True;shell[23:136,20:220]=False
results=[]
def trace(label,key,predicate,embedded=False,reference=None,maximum=900):
 frames=[];black=[];changed=[];stages=[];last=None;streak=0
 m.keys.add(key)
 for n in range(1,maximum+1):
  m.run(1)
  if n==2:m.keys.clear()
  frame=m.screen.copy();arr=np.asarray(frame)
  frames.append(frame)
  if arr.max()<8:black.append(n)
  if reference is not None and not np.array_equal(arr[shell],reference[shell]):
   changed.append(n)
   frame.save(out/(label+'-fault-'+str(n)+'.png'))
  callback=struct.unpack('<I',m.read(m.symbols['gMain']+4,4))[0]
  state=(callback,byte('sReturnCoverActive'),byte('sTabletNative'),task('Task_CloseTablet') is not None,m.read(m.symbols['gMain']+0x438,1)[0])
  if state!=last:stages.append([n,*state]);last=state
  if predicate():
   streak+=1
   if streak>=3:break
  else:streak=0
 else:
  frame.resize((720,480),m.Image.Resampling.NEAREST).save(out/(label+'-timeout.png'))
  raise AssertionError(('Timed out',label,stages))
 m.keys.clear()
 frames[-1].resize((720,480),m.Image.Resampling.NEAREST).save(out/(label+'-ready.png'))
 frames[0].save(out/(label+'.gif'),save_all=True,append_images=frames[1:],duration=17,loop=0)
 # Contact sheet samples the actual frames without depending on wall-clock speed.
 picks=sorted(set([0,1,len(frames)//4,len(frames)//2,len(frames)*3//4,len(frames)-1]))
 from PIL import Image,ImageDraw
 sheet=Image.new('RGB',(240*3,180*((len(picks)+2)//3)),(30,30,30));draw=ImageDraw.Draw(sheet)
 for i,p in enumerate(picks):
  x=i%3*240;y=i//3*180;sheet.paste(frames[p],(x,y+20));draw.text((x+4,y+3),f'{label}: frame {p+1}',fill='white')
 sheet.save(out/(label+'-frames.png'))
 row=dict(transition=label,frames=n,seconds=round(n/59.7275,3),black_frames=black,shell_changed_frames=changed,stages=stages)
 results.append(row);print(json.dumps(row),flush=True)
 if embedded and not os.environ.get('PGQA_RECORD_ONLY'):
  assert not black,(label,'black frame',black)
  assert not changed,(label,'shell changed',changed)
 return n
field=save()
trace('tablet-open',3,hub)
base=np.asarray(m.screen).copy();launcher=save()
apps=[('pokedex',0,'Task_PokeGlassPokedex',True),('party',1,'Task_HandleChooseMonInput',True),
 ('storage',2,'Task_PokeGlassStorage',True),('stats',3,'Task_PokeGlassStats',True),('map',4,'Task_RegionMap',False),
 ('bag',5,'Task_BagMenu_HandleInput',False),('trainer-card',6,'Task_TrainerCard',False),('options',7,'Task_OptionMenu',False),
 ('save',8,'task50_save_game',False)]
if 'DebugTask_HandleMenuInput_Main' in m.symbols:
 apps.append(('debug',9,'DebugTask_HandleMenuInput_Main',False))
for label,app,taskname,embedded in apps:
 restore(launcher)
 paths={0:[],1:[7],2:[7,7],3:[5,7],4:[5],5:[5,7,7],6:[7,7,7],7:[7,7,7,7],8:[7,7,7,7,7],9:[7,7,7,5]}
 for key in paths[app]:m.press(key,30)
 assert byte('sHubCursor')==app,(label,byte('sHubCursor'))
 if label=='save':
  def app_ready():
   return ready(taskname) and struct.unpack('<I',m.read(m.symbols['sSaveDialogCB'],4))[0]==(m.symbols['SaveDialogCB_AskSaveHandleInput']|1)
 else:
  def app_ready(t=taskname):return ready(t)
 trace(label+'-open',8,app_ready,embedded,base if embedded else None)
 m.run(15)
 trace(label+'-close',0,hub,embedded,base if embedded else None)
 m.run(15)
trace('tablet-close',0,lambda:byte('sGlobalScriptContextStatus')==2 and not byte('sLockFieldControls'))
(out/'timings.json').write_text(json.dumps(results,indent=2)+'\n')
print('PASS all visible apps opened/closed; timing and actual handoff frames saved',flush=True)
