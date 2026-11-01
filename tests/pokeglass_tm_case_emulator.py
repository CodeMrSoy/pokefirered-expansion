"""Original TM case/disc graphics, native swap animation and launcher return."""
import pathlib,struct
import numpy as np
setup=pathlib.Path(__file__).with_name('avatar_wardrobe_emulator.py')
exec(compile(setup.read_text().split("fixture = b'\\x23'")[0],str(setup),'exec'))
fixture=b'\x29'+struct.pack('<H',0x829)
for item,q in [(717,1),(582,2),(583,3),(584,4),(598,5)]:fixture+=b'\x44'+struct.pack('<HH',item,q)
m.inject(fixture+b'\x02')
m.press(3);wait_task('Task_PokeGlassHub');m.run(40);m.press(6,30);m.snap('tm-glass-original-launcher');m.press(8);wait_task('Task_HandleListInput');m.run(100)
m.snap('tm-glass-original-fighting')
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
# Every opaque case pixel and its palette must still come from the native assets.
case_gfx=unpack_lz(m.symbols['gTMCase_Gfx']);map_tiles=struct.unpack('<1024H',(m.root/'graphics/tm_case/tm_case.bin').read_bytes())
rendered=m.read(0x0600CC20,56*40//2);opaque=0
for y in range(40):
 for x in range(56):
  value=rendered[(y//8*7+x//8)*32+(y%8)*4+x%8//2]>>((x&1)*4)&15
  if not value:continue
  sx,sy=8+x,48+y;t=map_tiles[sy//8*32+sx//8];xx,yy=sx%8,sy%8
  if t&1024:xx=7-xx
  if t&2048:yy=7-yy
  expected=case_gfx[(t&1023)*32+yy*4+xx//2]>>((xx&1)*4)&15
  assert value==expected,('Case pixel changed',x,y,value,expected)
  opaque+=1
assert opaque>1000
assert m.read(m.symbols['gPlttBufferUnfaded']+12*32,32)==m.read(m.symbols['gTMCaseMenu_Male_Pal']+64,32),'Case palette changed'
p=next(m.symbols['gSprites']+i*68 for i in range(64) if (struct.unpack('<H',m.read(m.symbols['gSprites']+i*68+4,2))[0]&1023)==base and 20<=struct.unpack('<h',m.read(m.symbols['gSprites']+i*68+0x20,2))[0]<=50)
case=np.asarray(m.screen)[54:85,18:66].astype(int);assert ((case[:,:,0]>150)&(case[:,:,1]>80)&(case[:,:,2]<130)).sum()>100,'Original gold case not visible'
frames=[];offsets=[];m.keys.add(5)
for frame in range(24):
 m.run(1)
 if frame==0:m.keys.clear()
 frames.append(m.screen.copy());offsets.append(struct.unpack('<h',m.read(p+0x26,2))[0])
assert max(offsets)==20 and 10 in offsets and offsets[-1]==0,offsets
frames[0].save(m.d/'tm-glass-original-scroll.gif',save_all=True,append_images=frames[1:],duration=34,loop=0)
m.run(30);m.snap('tm-glass-original-dragon')
for _ in range(3):m.press(5,30)
assert struct.unpack('<h',m.read(p+0x26,2))[0]==20
m.snap('tm-glass-original-closed');m.press(4,40);assert struct.unpack('<h',m.read(p+0x26,2))[0]==0
for _ in range(8):m.press(4,2);m.press(5,2)
m.run(60);assert struct.unpack('<h',m.read(p+0x26,2))[0] in (0,20)
m.press(0,180);wait_task('Task_PokeGlassHub');assert m.read(m.symbols['sHubCursor'],1)==b'\x0c'
m.press(0,90);assert m.read(m.symbols['sLockFieldControls'],1)==b'\x00'
# The case continues to use the native female palette too (the two original
# banks differ in accent colors), while its tile indices stay unchanged.
save2=struct.unpack('<I',m.read(m.symbols['gSaveBlock2Ptr'],4))[0];gender=m.read(save2+8,1);m.write(save2+8,b'\x01')
m.press(3);wait_task('Task_PokeGlassHub');m.run(40);m.press(8);wait_task('Task_HandleListInput');m.run(100)
assert m.read(m.symbols['gPlttBufferUnfaded']+12*32,32)==m.read(m.symbols['gTMCaseMenu_Female_Pal']+64,32)
m.snap('tm-glass-original-female');m.press(0,180);wait_task('Task_PokeGlassHub');m.press(0,90);m.write(save2+8,gender)
print('PASS original native disc bytes, exact original case pixels and both palettes, native insert/eject offsets, CLOSE/reopen, rapid scrolling and field return',flush=True)
