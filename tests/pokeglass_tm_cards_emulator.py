"""SD card presentation and visible insert/eject animation in the glass case."""
import pathlib,struct
import numpy as np
from PIL import Image,ImageDraw
setup=pathlib.Path(__file__).with_name('avatar_wardrobe_emulator.py')
exec(compile(setup.read_text().split("fixture = b'\\x23'")[0],str(setup),'exec'))
fixture=b'\x29'+struct.pack('<H',0x829)
for item,q in [(717,1),(582,2),(583,3),(584,4),(598,5)]:fixture+=b'\x44'+struct.pack('<HH',item,q)
m.inject(fixture+b'\x02')
m.press(3);wait_task('Task_PokeGlassHub');m.run(40);m.press(6,30);m.press(8);wait_task('Task_HandleListInput');m.run(100)
m.snap('tm-sd-card-fighting');first_card=np.asarray(m.screen)[28:46,32:59].copy()
def sprite():
 # Find the card from its callback/template-independent position and tile tag.
 for i in range(64):
  p=m.symbols['gSprites']+i*68
  if struct.unpack('<h',m.read(p+0x20,2))[0]==44:return p
 raise AssertionError('Missing SD card sprite')
p=sprite();case=np.asarray(m.screen)[46:56,25:64].copy();frames=[];offsets=[];tiles=[]
m.keys.add(5)
for frame in range(28):
 m.run(1)
 if frame==0:m.keys.clear()
 frames.append(m.screen.copy());offsets.append(struct.unpack('<h',m.read(p+0x26,2))[0]);tiles.append(struct.unpack('<H',m.read(p+4,2))[0]&1023)
 assert np.array_equal(case,np.asarray(m.screen)[46:56,25:64]),('Case moved or card escaped slot',frame)
assert max(offsets)==20 and offsets[-1]==0 and len(set(tiles))==6,(offsets,tiles)
assert any(not np.array_equal(np.asarray(frames[0])[28:46,32:59],np.asarray(f)[28:46,32:59]) for f in frames[1:])
frames[0].save(m.d/'tm-sd-card-scroll.gif',save_all=True,append_images=frames[1:],duration=34,loop=0)
sheet=Image.new('RGB',(240*3,180*2));draw=ImageDraw.Draw(sheet)
for i,n in enumerate([0,3,5,7,9,13]):
 x=i%3*240;y=i//3*180;sheet.paste(frames[n],(x,y+20));draw.text((x+4,y+4),'Frame '+str(n+1),fill='white')
sheet.resize((1440,720)).save(m.d/'tm-sd-card-animation.png')
m.run(40);m.snap('tm-sd-card-dragon');assert not np.array_equal(first_card,np.asarray(m.screen)[28:46,32:59]),'Type color unchanged'
# Cancel/CLOSE retracts the card fully; scrolling back raises it again.
for _ in range(3):m.press(5,30)
assert struct.unpack('<h',m.read(p+0x26,2))[0]==20
m.snap('tm-sd-card-closed');m.press(4,40);assert struct.unpack('<h',m.read(p+0x26,2))[0]==0
m.snap('tm-sd-card-normal')
# Rapid navigation settles on the final selection without leaking the card below its slot.
for _ in range(8):m.press(4,2);m.press(5,2)
m.run(60);assert struct.unpack('<h',m.read(p+0x26,2))[0] in (0,20)
m.press(0,180);wait_task('Task_PokeGlassHub');m.press(0,90)
assert m.read(m.symbols['sLockFieldControls'],1)==b'\x00'
print('PASS colored SD cards, six visible insertion/ejection positions, stable case/slot clipping, CLOSE/reopen, rapid scroll and field return',flush=True)
