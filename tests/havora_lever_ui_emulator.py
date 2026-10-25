"""Actual A-button mooring feedback and animated reset, with no route shortcuts."""
from pathlib import Path
source=Path(__file__).with_name('havora_three_lock_emulator.py').read_text()
exec(compile(source[:source.index('for i,step in enumerate')], 'gym-setup', 'exec'))
route_source=Path(__file__).with_name('havora_three_lock_emulator.py').read_text()
exec(route_source[route_source.index('def active(name):'):route_source.index('# Real A-button boarding')])
native('VarSet',0x40d8,7)
native('VarSet',0x40d7,encode(((2,2,0),3,0,3,0,False)))
warp(51,15);m.press(4,20);m.press(8,600)
assert active('Task_YesNoMenu_HandleInput'),'service mooring prompt missing'
m.press(8,240)
m.snap('lever-mooring-feedback')
assert (value(0x40d7)>>11)&3==1,('service mooring prompt failed',hex(value(0x40d7)))
for _ in range(20):
 if m.read(m.symbols['sGlobalScriptContextStatus'],1)==b'\x02':break
 m.press(8,45)
assert (value(0x40d7)>>11)&3==1,'dismissal repeated the mooring operation'
warp(4,14);m.press(4,20);m.press(8,600)
assert active('Task_YesNoMenu_HandleInput'),'reset prompt missing'
m.press(8,300)
assert pos()==(3,48),('animated reset did not return to entrance',pos())
assert value(0x40d8)==7,'reset erased victories'
print('PASS actual mooring prompt, completion feedback and animated reset script',flush=True)
