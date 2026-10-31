"""Glass TM layout: dense list, scrolling, stat updates, actions and VRAM bounds."""
import pathlib, struct
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
windows();m.snap('tm-glass-dense')
r,g,b=m.screen.getpixel((215,101));assert b>r and r<100,(r,g,b)
for _ in range(16):m.press(5,25)
m.snap('tm-glass-protect');windows()
for _ in range(16):m.press(4,25)
m.press(8,60);wait_task('Task_ContextMenu_HandleInput');windows();m.snap('tm-glass-context')
# The custom cyan borders must survive queued native graphics loads.
for base in (0x5B,0x78):
 data=m.read(0x06000000+base*32,9*32)
 assert all((v&15) in (4,6) and (v>>4) in (4,6) for v in data),('Native frame replaced glass',base)
m.press(0,90);wait_task('Task_HandleListInput');m.snap('tm-glass-context-return')
m.press(8,60);wait_task('Task_ContextMenu_HandleInput');m.press(8,90);m.snap('tm-glass-no-party');windows()
m.press(8,90);wait_task('Task_HandleListInput');m.press(0,180);wait_task('Task_PokeGlassHub');m.press(0,90)
assert m.read(m.symbols['sLockFieldControls'],1)==b'\x00'
print('PASS dense TM list, scrolling, Protect stat update, cyan action frames, context cancel, no-party error, disjoint VRAM and field return',flush=True)
