"""Check annotated Section A fixes against compiled map data and MID walking."""
from pathlib import Path
src=Path(__file__).with_name('havora_tidal_trial_emulator.py').read_text()
exec(compile(src[:src.index('# Migrate legacy')],'section-a-setup','exec'))
for tid in range(743,751):native('SetTrainerFlag',tid)
native('VarSet',0x40d8,0)
for level in [0,1,2,1,0]:
 setwater((level,0,0));stage(3,10);assert_map((level,0,0))
print('PASS native LOW/MID/HIGH/MID/LOW Section A artwork matches corrected profiles',flush=True)
setwater((1,0,0));stage(25,12)
for x,y in [(26,12),(26,13),(26,14),(25,14),(24,14),(24,15),(24,16)]:
 for _ in range(3):
  px,py=pos();m.press(7 if x>px else 6 if x<px else 5 if y>py else 4,22)
  if pos()==(x,y):break
 assert pos()==(x,y),('MID staircase blocked by restored cliff',pos(),(x,y))
print('PASS actual MID stair-to-boat-pad walking remains accessible',flush=True)
