"""Native Start menu entry, Pokeglass gating, debug open/cancel and old chord."""
import argparse,struct
import havora_emulator_support as m
p=argparse.ArgumentParser();p.add_argument('--release',action='store_true');a=p.parse_args()
def debug_active():
 if 'DebugTask_HandleMenuInput_Main' not in m.symbols:return False
 f=m.symbols['DebugTask_HandleMenuInput_Main']&~1
 return any((lambda b:b[4] and struct.unpack('<I',b[:4])[0]&~1==f)(m.read(m.symbols['gTasks']+i*40,40)) for i in range(16))
def order():
 n=m.read(m.symbols['sNumStartMenuItems'],1)[0];return list(m.read(m.symbols['sStartMenuOrder'],n))
def locked():return m.read(m.symbols['sLockFieldControls'],1)[0]
m.inject(b'\x39'+struct.pack('<BBBHH',3,0,255,10,9)+b'\x6b\x02');m.run(180)
for has_glass in [False,True]:
 if has_glass:m.inject(b'\x44'+struct.pack('<HH',717,1)+b'\x02')
 m.press(3);expected=([9] if not a.release else [])+([0] if has_glass else [])+[2,3,4,5,6]
 assert order()==expected,(order(),expected);m.snap('start-menu-'+('release' if a.release else 'development')+('-glass' if has_glass else '-early'))
 if a.release:m.press(0)
 else:
  m.press(8);assert debug_active(),'Start DEBUG did not open menu';m.snap('start-debug-open');m.press(0);assert not debug_active() and not locked(),'Debug cancel stranded player'
 assert not locked()
# Holding the former debug shortcut now still opens Start, not the debug UI.
m.keys.update([3,11]);m.run(2);m.keys.clear();m.run(120)
assert not debug_active() and order()==expected;m.press(0);assert not locked()
print('PASS Start entries, early/tablet gating, '+('release debug exclusion' if a.release else 'debug launch/cancel')+', old R+START chord, and restored controls',flush=True)
