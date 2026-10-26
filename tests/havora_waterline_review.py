"""Record a native emulator water-transfer inspection at the lower dock."""
from pathlib import Path
from PIL import Image
source=Path(__file__).with_name('havora_three_lock_emulator.py').read_text()
exec(compile(source[:source.index('for i,step in enumerate')], 'gym-setup', 'exec'))
warp(30,20)
frames=[];old_run=m.run;tick=0
# Observe a direct machinery command from the dock to keep its flooding visible.
def capture(n):
 global tick
 for _ in range(n):
  old_run(1);tick+=1
  if tick%4==0:frames.append(m.screen.resize((720,480),Image.Resampling.NEAREST).copy())
for v,n in [(0x8004,10),(0x8005,1),(0x8006,2)]:native('VarSet',v,n)
m.run=capture
native('HavoraGym_Control')
m.run=old_run
assert value(0x40d7)==encode(((2,1,1),0,0,4,0,False))
for v,n in [(0x8004,10),(0x8005,2),(0x8006,1)]:native('VarSet',v,n)
m.run=capture
native('HavoraGym_Control')
m.run=old_run
assert value(0x40d7)==encode(((2,2,0),0,0,4,0,False))
frames[0].save(m.root/'docs/havora/review/waterline-structure.gif',save_all=True,append_images=frames[1:],duration=67,loop=0)
print('PASS recorded native fixed transfer with progressive dock exposure')
