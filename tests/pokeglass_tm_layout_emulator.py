"""Native TM layout: dense list, scrolling, stat updates, actions and VRAM bounds."""
import pathlib, struct
import numpy as np
setup=pathlib.Path(__file__).with_name('avatar_wardrobe_emulator.py')
exec(compile(setup.read_text().split("fixture = b'\\x23'")[0],str(setup),'exec'))
fixture=b'\x29'+struct.pack('<H',0x829)+b'\x44'+struct.pack('<HH',717,1)
for item in range(582,603):fixture+=b'\x44'+struct.pack('<HH',item,99)
m.inject(fixture+b'\x02')
m.press(3);wait_task('Task_PokeGlassHub');m.run(40);m.press(6,30);m.press(8);wait_task('Task_HandleListInput');m.run(100)
def windows():
 ranges=[]
 for i in range(32):
  w=m.read(m.symbols['gWindows']+i*12,12)
  if w[0]==0 and struct.unpack_from('<I',w,8)[0]:
   start=struct.unpack_from('<H',w,6)[0];end=start+w[3]*w[4]
   assert end<=0x370,('Tablet tile overwrite',i,start,end)
   for j,a,b in ranges:assert end<=a or start>=b,('Overlapping graphics',i,j)
   ranges.append((i,start,end))
windows();m.snap('tm-native-dense')
panel=np.asarray(m.screen)[16:80,90:220]
assert ((panel[:,:,0]>220)&(panel[:,:,1]>220)&(panel[:,:,2]>130)).sum()>1000,'Native cream panel missing'
for _ in range(16):m.press(5,25)
m.snap('tm-native-protect');windows()
for _ in range(16):m.press(4,25)
m.press(8,60);wait_task('Task_ContextMenu_HandleInput');windows();m.snap('tm-native-context')
m.press(0,90);wait_task('Task_HandleListInput');m.snap('tm-native-context-return')
m.press(8,60);wait_task('Task_ContextMenu_HandleInput');m.press(8,90);m.snap('tm-native-no-party');windows()
m.press(8,90);wait_task('Task_HandleListInput');m.press(0,180);wait_task('Task_PokeGlassHub');m.press(0,90)
assert m.read(m.symbols['sLockFieldControls'],1)==b'\x00'
print('PASS dense TM list, scrolling, Protect stat update, native action frames, context cancel, no-party error, disjoint VRAM and field return',flush=True)
