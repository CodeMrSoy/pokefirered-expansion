"""Real Shears/Gloves prompts inside Havora, with no party traversal moves."""
import os,pathlib,struct,subprocess,re
import quantum_qol_emulator as m
source=(m.root/'tests/avatar_wardrobe_emulator.py').read_text()
exec(source[source.index('native_dir ='):source.index('avatar_var = native')])
def constant(name,header='flags.h'):
 out=subprocess.check_output(['arm-none-eabi-cpp','-P','-I',str(m.root/'include'),'-'],input=f'#include "constants/{header}"\n{name}\n',text=True)
 return eval(out.strip().splitlines()[-1],{'__builtins__':{}},{})
def player():return m.symbols['gObjectEvents']+m.read(m.symbols['gPlayerAvatar']+5,1)[0]*36
num,group=map(int,re.search(r'#define MAP_HAVORA_NORTH_QUADRANT\s+\((\d+) \| \((\d+) << 8\)\)',(m.root/'include/constants/map_groups.h').read_text()).groups())
def warp(x,y,direction=2):
 m.inject(b'\x39'+struct.pack('<BBBHH',group,num,255,x,y)+b'\x6b\x02');m.run(180);native('ObjectEventTurn',player(),direction);m.press({1:5,2:4,3:6,4:7}[direction],30)
def finish():
 for _ in range(40):
  if m.read(m.symbols['sGlobalScriptContextStatus'],1)==b'\x02':break
  m.press(8,40)
 m.run(90)
 assert m.read(m.symbols['sGlobalScriptContextStatus'],1)==b'\x02','Tool dialogue did not finish'
def rock_position():return native('VarGet',0x40d0)
def tile(x,y):
 width,height,ptr=struct.unpack('<iiI',m.read(m.symbols['VMap'],12));return struct.unpack('<H',m.read(ptr+2*((y+7)*width+x+7),2))[0]
m.inject(b'\x23'+struct.pack('<I',(m.symbols['ScrCmd_createmon']|1)+0x2000000)+struct.pack('<BBHHI',0,6,1,25,0)+b'\x02')
for slot in range(4):native('SetMonMoveSlot',m.symbols['gPlayerParty'],33,slot)
for flag in ['FLAG_BADGE02_GET','FLAG_BADGE04_GET']:native('FlagSet',constant(flag))
for item in [682,685]:assert native('AddBagItem',item,1)
assert native('CheckBagHasItem',831,1),'Field Item Case missing'
assert native('FieldMove_IsUnlocked',0) and native('FieldMove_IsUnlocked',3)
warp(14,26);m.press(8,80);m.press(8,80);m.press(8,1);m.run(450);finish()
assert native('VarGet',0x40d6)&1,'Shears did not persist Havora Cut state'
m.snap('merged-havora-shears-cleared')
warp(14,26);assert native('VarGet',0x40d6)&1,'Cut tree returned after reload'
assert not any((lambda b:b[0]&1 and b[8]==17 and b[9]==num and b[10]==group)(m.read(m.symbols['gObjectEvents']+i*36,36)) for i in range(16))
print('PASS native Shears clear the Havora tree and persist across reload',flush=True)
warp(15,25);assert not native('FlagGet',constant('FLAG_SYS_USE_STRENGTH'))
m.press(8,80);m.press(8,90);finish();assert native('FlagGet',constant('FLAG_SYS_USE_STRENGTH'))
# Push the first boulder east twice, then fill the first shaft. Only a grove
# boulder can enter that blocked pit; the shared controller records its loss.
for x,y,direction in [(14,24,4),(15,24,4),(16,24,4)]:
 # Same-map warp clears Strength, so restore it via the already-verified tool
 # field effect before pushing, without changing the grove's saved positions.
 warp(x,y,direction)
 m.press(8,80);m.press(8,90);finish()
 before=rock_position();m.keys.add(7);m.run(40);m.keys.clear();m.run(80);assert rock_position()!=before,(x,y,hex(before))
assert rock_position()==65535 and native('VarGet',0x40d6)>>3&1,'Gloves push did not fill pit'
assert tile(18,24)&1023==0 and not tile(18,24)&0xc00
assert native('CheckBagHasItem',682,1) and native('CheckBagHasItem',685,1)
m.snap('merged-havora-gloves-filled-pit')
print('PASS native Gloves push Havora boulders into pits without HM moves; case tools remain reusable',flush=True)
