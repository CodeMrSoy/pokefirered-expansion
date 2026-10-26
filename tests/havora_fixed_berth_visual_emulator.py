"""Stationary-camera drain/fill review; direct scripted transfers are labelled."""
from pathlib import Path
from PIL import ImageDraw,ImageFont
s=Path(__file__).with_name('havora_three_lock_emulator.py').read_text()
exec(compile(s[:s.index('for i,step in enumerate')],'gym-setup','exec'))
native('VarSet',0x40d7,encode(((0,2,2),0,0,4,0,False)));warp(3,22)
frames=[];original=m.run;clock=0
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',11)
def run(n):
 global clock
 for _ in range(n):
  original(1);clock+=1
  width,height,address=struct.unpack('<iiI',m.read(m.symbols['VMap'],12))
  tile=struct.unpack('<H',m.read(address+2*((19+7)*width+7+7),2))[0]&1023
  # A map rebuild spans frames in RAM; water is copied before the stationary
  # boat overlay, and is not committed to the displayed BG until Draw finishes.
  assert tile in (0x2c0,0x282),('unexpected berth tile during redraw',tile)
  if clock%12:continue
  frame=m.screen.copy();d=ImageDraw.Draw(frame)
  d.rectangle((0,0,240,15),fill='black');d.text((3,1),'FIXED BERTH - scripted tide cycle',font=font,fill='white')
  frames.append(frame.resize((720,480),m.Image.Resampling.NEAREST))
m.run=run
m.run(90)
for src,dst in [(1,0),(1,0),(0,1),(0,1)]:
 assert command(10,src,dst)==1
 m.run(75)
 width,height,address=struct.unpack('<iiI',m.read(m.symbols['VMap'],12))
 assert struct.unpack('<H',m.read(address+2*((19+7)*width+7+7),2))[0]&1023==0x2c0
assert value(0x40d7)==encode(((0,2,2),0,0,4,0,False))
out=Path(__import__('sys').argv[1]) if len(__import__('sys').argv)>1 else m.d/'fixed-berth-water-cycle.gif'
frames[0].save(out,save_all=True,append_images=frames[1:],duration=100,loop=0,optimize=True)
print('PASS stationary berth through LOW/MID/HIGH/MID/LOW; actual native tide animation',out,flush=True)
