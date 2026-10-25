#!/usr/bin/env python3
"""Exercise field tools on a real ROM, with no HM moves in the party."""
import os,pathlib,struct,subprocess,json
import quantum_qol_emulator as m
source=(m.root/'tests/avatar_wardrobe_emulator.py').read_text()
exec(source[source.index('native_dir ='):source.index('avatar_var = native')])
m.d=m.d/'field-tools';m.d.mkdir(exist_ok=True)
def ptr(name):return struct.unpack('<I',m.read(m.symbols[name],4))[0]
def constant(name,header='flags.h'):
 cpp=os.environ['ARM_NM'].removesuffix('nm')+'cpp'
 out=subprocess.check_output([cpp,'-P','-I',str(m.root/'include'),'-'],input=f'#include "constants/{header}"\n{name}\n',text=True)
 return eval(out.strip().splitlines()[-1],{'__builtins__':{}},{})
def flag(name,on=True):native('FlagSet' if on else 'FlagClear',constant(name))
def finish():
 for _ in range(25):
  if m.read(m.symbols['sGlobalScriptContextStatus'],1)==b'\x02':break
  m.press(8,35)
 m.run(120)
def savedstate():
 n=m.lib.retro_serialize_size();b=m.c.create_string_buffer(n);assert m.lib.retro_serialize(b,n);return b.raw
def restore(b):
 v=m.c.create_string_buffer(b);assert m.lib.retro_unserialize(v,len(b))
def runscript(label):m.inject(b'\x05'+struct.pack('<I',m.symbols[label]))
def player():return m.symbols['gObjectEvents']+m.read(m.symbols['gPlayerAvatar']+5,1)[0]*36
def coords():return struct.unpack('<hh',m.read(player()+16,4))
groups=json.loads((m.root/'data/maps/map_groups.json').read_text())
ids={n:(g,i) for g,k in enumerate(groups['group_order']) for i,n in enumerate(groups[k])}
def warp(name,x,y,direction=2):
 g,n=ids[name];m.inject(b'\x39'+struct.pack('<BBBhh',g,n,255,x,y)+b'\x27\x6b\x02');m.run(240)
 native('ObjectEventTurn',player(),direction)
 m.press({1:5,2:4,3:6,4:7}[direction],30)
def pocket(index):
 p=m.symbols['gBagPockets']+index*8
 return struct.unpack('<I',m.read(p,4))[0],m.read(p+4,1)[0]

m.inject(b'\x23'+struct.pack('<I',(m.symbols['ScrCmd_createmon']|1)+0x2000000)+struct.pack('<BBHHI',0,6,1,25,0)+b'\x02')
for i in range(1,8):flag(f'FLAG_BADGE0{i}_GET')
for item in range(682,689):assert native('AddBagItem',item,1)==1
kp,cap=pocket(1)
keys=[struct.unpack('<H',m.read(kp+i*4,2))[0] for i in range(cap)]
assert keys.count(831)==1 and not set(range(682,689))&set(keys),'Tools took separate Bag slots'
assert native('CheckBagHasItem',831,1)==1
# Old tool shortcuts consolidate to the case without replacing unrelated slots.
save=ptr('gSaveBlock1Ptr')
m.write(save+0x296,struct.pack('<H',682))
# Registered extras share the former padding after the game stats; resolve
# the actual offset using the public C struct through the native helper fixture.
# A single registered case must open directly on Select.
native('FieldTools_MigrateInventory')
assert m.read(save+0x296,2)==struct.pack('<H',831)
m.press(2,200)
assert m.read(m.symbols['sCaseSelection'],1)==b'\0'
assets=['shears','whistle','wailmer_wailer','gloves','lantern','hammer','bait']
for i,name in enumerate(assets):
 assert m.read(m.symbols['sCaseSelection'],1)==bytes([i])
 sid=m.read(m.symbols['sCasePreview'],1)[0];assert sid<64
 sprite=m.read(m.symbols['gSprites']+sid*68,68)
 assert sprite[1]&3==0 and sprite[3]>>6==3,'Preview not native 64px'
 attr2=struct.unpack_from('<H',sprite,4)[0]
 expected=(m.root/'graphics/field_effects/field_tools'/(name+'.4bpp')).read_bytes()
 assert m.read(0x6010000+(attr2&1023)*32,2048)==expected,('Wrong preview',name)
 m.snap('case-'+name)
 if i<6:m.press(5,14)
m.press(0,240)
# Preserve unrelated wheel items while consolidating several old tool slots.
extra=native('RegisteredItemAt',1)-save
assert native('AddBagItem',706,1)==1
m.write(save+extra,struct.pack('<HHH',706,683,686))
native('FieldTools_MigrateInventory')
assert m.read(save+extra,6)==struct.pack('<HHH',706,0,0)
m.press(2,90);m.snap('case-wheel')
assert any(m.read(m.symbols['gTasks']+i*40+4,1)!=b'\0' and struct.unpack('<I',m.read(m.symbols['gTasks']+i*40,4))[0]==(m.symbols['Task_KeyItemWheel']|1) for i in range(16))
m.press(4,180)
assert struct.unpack('<I',m.read(m.symbols['gMain']+4,4))[0]==(m.symbols['CB2_FieldItemCase']|1),'Wheel did not open case'
m.press(0,240)
m.write(save+extra,b'\0'*6)
assert native('RemoveBagItem',706,1)==1
# Uncollected tools and missing badges cannot launch a field action.
assert native('RemoveBagItem',687,1)==1
m.press(2,180)
for _ in range(5):m.press(5,14)
m.press(8,60)
sid=m.read(m.symbols['sCasePreview'],1)[0];assert sid<64
attr2=struct.unpack('<H',m.read(m.symbols['gSprites']+sid*68+4,2))[0]
colors=struct.unpack('<16H',m.read(m.symbols['gPlttBufferFaded']+(0x100+(attr2>>12)*16)*2,32))
assert all(c&31==(c>>5)&31==(c>>10)&31 for c in colors),'Missing tool preview is not greyed'
assert struct.unpack('<I',m.read(m.symbols['gMain']+4,4))[0]==(m.symbols['CB2_FieldItemCase']|1)
m.snap('case-not-collected');m.press(0,240)
assert native('AddBagItem',687,1)==1
flag('FLAG_BADGE01_GET',False)
m.press(2,180)
for _ in range(4):m.press(5,14)
m.press(8,60)
assert struct.unpack('<I',m.read(m.symbols['gMain']+4,4))[0]==(m.symbols['CB2_FieldItemCase']|1)
m.snap('case-badge-needed');m.press(0,240)
flag('FLAG_BADGE01_GET')
# Actual Bag -> Use -> case, then B -> Bag.
native('GoToBagMenu',0,1,m.symbols['CB2_ReturnToField']|1);m.run(180)
caseIndex=keys.index(831)
for _ in range(caseIndex):m.press(5,12)
m.snap('case-key-items')
m.press(8,40);m.press(8,180)
assert m.read(m.symbols['sCaseSelection'],1)==b'\0'
m.press(0,180)
assert struct.unpack('<I',m.read(m.symbols['gMain']+4,4))[0]==(m.symbols['CB2_BagMenuRun']|1),'Back did not return to Bag'
m.press(0,240)
# Lantern selection delegates to the real field action from the case.
assert native('RemoveBagItem',686,1)==1
warp('Route10',8,21)
m.keys.add(4);m.run(24);m.keys.clear();m.run(100)
assert tuple(m.read(ptr('gSaveBlock1Ptr')+4,2))==ids['Route10'],'Missing Lantern allowed cave entry'
m.snap('case-lantern-entry-refused');finish()
assert native('AddBagItem',686,1)==1
warp('Route10',8,21)
m.keys.add(4);m.run(24);m.keys.clear();m.run(300)
assert tuple(m.read(ptr('gSaveBlock1Ptr')+4,2))==ids['RockTunnel_1F'],'Lantern case did not allow entry'
m.run(180);m.snap('case-lantern-pitch-black')
from PIL import ImageStat
assert max(ImageStat.Stat(m.screen).mean)<1,'Cave was not pitch black on entry'
m.snap('case-lantern-pitch-black')
m.press(2,180)
for _ in range(4):m.press(5,12)
m.press(8,500);finish()
assert native('FlagGet',constant('FLAG_SYS_FLASH_ACTIVE'))==1
assert native('GetFlashLevel')==1
assert len(set(m.read(m.symbols['sGlowSprites'],4)))==4
assert all(i<64 for i in m.read(m.symbols['sGlowSprites'],4)), 'Soft glow resources unavailable'
phases=set()
for _ in range(48):
 m.run(2);phases.add(m.read(m.symbols['sGlowPhase'],1)[0])
assert len(phases)==8, 'Lantern flicker phases stopped'
m.snap('case-lantern-glow')
# Ownership and case survive a real flash save and Continue.
warp('PalletTown',10,9)
assert native('GetSpriteTileStartByTag',0xd132)&65535==65535,'Lantern leaked tiles outside cave'
assert native('IndexOfSpritePaletteTag',0xd132)&255==255,'Lantern leaked palette outside cave'
assert native('TrySavingData',0)==1
m.lib.retro_reset();m.run(360);m.press(3);m.press(8);m.press(8);m.run(180)
for item in range(682,689):assert native('CheckBagHasItem',item,1)==1
assert native('CheckBagHasItem',831,1)==1
print('PASS: one case slot, seven native 64px previews, direct Select and wheel access, preserved unrelated registrations, missing-tool/badge locks, Bag/back navigation, Lantern entry/darkness/glow and flash-save/Continue ownership',flush=True)
