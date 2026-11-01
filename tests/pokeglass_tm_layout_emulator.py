"""Glass UI around the original TM case: dense list, scrolling, stat updates, actions and VRAM bounds."""
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
def stats():
 rects=[]
 for index in (4,5):
  w=m.read(m.symbols['gWindows']+index*12,12);width,height=w[3]*8,w[4]*8
  rects.append((w[1]*8,w[2]*8,width,height))
  data=m.read(struct.unpack_from('<I',w,8)[0],width*height//2)
  fg=np.zeros((height,width),bool)
  for y in range(height):
   for x in range(width):
    v=data[(y//8*w[3]+x//8)*32+(y%8)*4+x%8//2]>>((x&1)*4)&15
    fg[y,x]=v==8
  assert fg.sum()>10,('Missing stat text',index)
  assert not fg[0].any() and not fg[-1].any() and not fg[:,-1].any(),('Text clipped at window edge',index)
  screen=np.asarray(m.screen)[w[2]*8:w[2]*8+height,w[1]*8:w[1]*8+width]
  bright=(screen[:,:,0]>140)&(screen[:,:,1]>170)&(screen[:,:,2]>170)
  assert bright[fg].all(),('Stat glyph pixels obscured by another window/frame',index,int((~bright[fg]).sum()))
 a,b=rects
 assert a[0]+a[2]<=b[0] or b[0]+b[2]<=a[0] or a[1]+a[3]<=b[1] or b[1]+b[3]<=a[1],('Stat windows overlap',rects)

windows();stats();m.snap('tm-glass-original-dense')
panel=np.asarray(m.screen)[40:95,190:215]
assert ((panel[:,:,2]>panel[:,:,0])&(panel[:,:,0]<110)).sum()>500,'Glass list panel missing'
for _ in range(16):m.press(5,25)
m.snap('tm-glass-original-protect');windows();stats()
for _ in range(16):m.press(4,25)
m.press(8,60);wait_task('Task_ContextMenu_HandleInput');windows();stats();m.snap('tm-glass-original-context')
for base in (0x5B,0x78):
 data=m.read(0x06000000+base*32,9*32)
 assert all((v&15) in (4,6) and (v>>4) in (4,6) for v in data),'Glass action border replaced'
m.press(0,90);wait_task('Task_HandleListInput');m.snap('tm-glass-original-context-return');stats()
m.press(8,60);wait_task('Task_ContextMenu_HandleInput');m.press(8,90);m.snap('tm-glass-original-no-party');windows();stats()
m.press(8,90);wait_task('Task_HandleListInput');stats();m.press(0,180);wait_task('Task_PokeGlassHub');m.press(0,90)
assert m.read(m.symbols['sLockFieldControls'],1)==b'\x00'
print('PASS dense TM list, scrolling, Protect stat update, complete visible stat glyphs (list/context/error), glass action frames, context cancel, no-party error, disjoint VRAM and field return',flush=True)
