"""Original TM case/disc graphics, native swap animation and launcher return."""
import pathlib,struct
import numpy as np
setup=pathlib.Path(__file__).with_name('avatar_wardrobe_emulator.py')
exec(compile(setup.read_text().split("fixture = b'\\x23'")[0],str(setup),'exec'))
fixture=b'\x29'+struct.pack('<H',0x829)
for item,q in [(717,1),(582,2),(583,3),(584,4),(598,5)]:fixture+=b'\x44'+struct.pack('<HH',item,q)
m.inject(fixture+b'\x02')
m.press(3);wait_task('Task_PokeGlassHub');m.run(40);m.press(6,30);m.snap('tm-native-launcher');m.press(8);wait_task('Task_HandleListInput');m.run(100)
m.snap('tm-native-fighting')
def unpack_lz(address):
 data=m.read(address,4096);size=int.from_bytes(data[1:4],'little');out=bytearray();i=4
 assert data[0]==0x10
 while len(out)<size:
  flags=data[i];i+=1
  for bit in range(7,-1,-1):
   if len(out)>=size:break
   if flags&(1<<bit):
    a,b=data[i:i+2];i+=2;distance=((a&15)<<8)+b+1
    for _ in range((a>>4)+3):out.append(out[-distance])
   else:out.append(data[i]);i+=1
 return bytes(out[:size])
tags=struct.unpack('<64H',m.read(m.symbols['sSpriteTileRangeTags'],128))
base=struct.unpack('<H',m.read(m.symbols['sSpriteTileRanges']+tags.index(400)*4,2))[0]
original=unpack_lz(m.symbols['gTMCaseDisc_Gfx'])
assert m.read(0x06010000+base*32,len(original))==original,'Disc graphics differ from original'
p=next(m.symbols['gSprites']+i*68 for i in range(64) if (struct.unpack('<H',m.read(m.symbols['gSprites']+i*68+4,2))[0]&1023)==base and 20<=struct.unpack('<h',m.read(m.symbols['gSprites']+i*68+0x20,2))[0]<=50)
case=np.asarray(m.screen)[54:84,10:58].astype(int);assert ((case[:,:,0]>150)&(case[:,:,1]>80)&(case[:,:,2]<130)).sum()>100,'Original gold case not visible'
frames=[];offsets=[];m.keys.add(5)
for frame in range(24):
 m.run(1)
 if frame==0:m.keys.clear()
 frames.append(m.screen.copy());offsets.append(struct.unpack('<h',m.read(p+0x26,2))[0])
assert max(offsets)==20 and 10 in offsets and offsets[-1]==0,offsets
frames[0].save(m.d/'tm-native-scroll.gif',save_all=True,append_images=frames[1:],duration=34,loop=0)
m.run(30);m.snap('tm-native-dragon')
for _ in range(3):m.press(5,30)
assert struct.unpack('<h',m.read(p+0x26,2))[0]==20
m.snap('tm-native-closed');m.press(4,40);assert struct.unpack('<h',m.read(p+0x26,2))[0]==0
for _ in range(8):m.press(4,2);m.press(5,2)
m.run(60);assert struct.unpack('<h',m.read(p+0x26,2))[0] in (0,20)
m.press(0,180);wait_task('Task_PokeGlassHub');assert m.read(m.symbols['sHubCursor'],1)==b'\x0c'
m.press(0,90);assert m.read(m.symbols['sLockFieldControls'],1)==b'\x00'
print('PASS original native disc bytes, original gold case, native insert/eject offsets, CLOSE/reopen, rapid scrolling and field return',flush=True)
