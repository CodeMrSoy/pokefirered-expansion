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
# One healthy party member with no traversal moves. Use real give-mon script.
m.inject(b'\x23'+struct.pack('<I',(m.symbols['ScrCmd_createmon']|1)+0x2000000)+struct.pack('<BBHHI',0,6,1,25,0)+b'\x02')
assert m.read(m.symbols['gPlayerPartyCount'],1)==b'\x01'
for slot in range(4): native('SetMonMoveSlot',m.symbols['gPlayerParty'],33,slot)
for move,item,badge in [(0,682,2),(1,683,3),(2,684,5),(3,685,4),(4,686,1),(5,687,6),(6,688,7)]:
 flag(f'FLAG_BADGE0{badge}_GET',False)
 assert native('FieldMove_IsUnlocked',move)==0
 assert native('AddBagItem',item,1)==1
 assert native('GetItemPocket',item)==1
 assert native('FieldMove_IsUnlocked',move)==0,'Missing badge allowed tool'
 flag(f'FLAG_BADGE0{badge}_GET')
 assert native('FieldMove_IsUnlocked',move)==1,'Tool required a Pokémon move'
 assert native('RemoveBagItem',item,1)==1
 assert native('FieldMove_IsUnlocked',move)==0,'Badge alone authorized a missing tool'
 assert native('AddBagItem',item,1)==1
 assert native('IsItemHM',item)==0 and native('IsItemTMHM',item)==0
 assert native('AddBagItem',item,99)==1
 assert native('CheckBagHasItem',item,2)==0,'Tool duplicated'
print('PASS: all seven tools require ownership/badges, occupy Key Items, are unique and need no HM user',flush=True)
# Recover old HM inventory in the original slots without changing unrelated TMs.
kp,kcap=pocket(1);tp,tcap=pocket(3)
base=savedstate()
m.write(kp,b'\0'*(kcap*4));m.write(tp,b'\0'*(tcap*4))
for i,item in enumerate(range(682,689)):m.write(tp+i*4,struct.pack('<HH',item,1))
m.write(tp+7*4,struct.pack('<HH',582,3))
native('FieldTools_MigrateInventory')
for item in range(682,689):assert native('CheckBagHasItem',item,1)==1
assert native('CheckBagHasItem',582,3)==1
before=m.read(kp,kcap*4);native('FieldTools_MigrateInventory');assert m.read(kp,kcap*4)==before
# Full key pocket: keep the old slot and access; recover when one slot opens.
m.write(kp,struct.pack('<HH',349,1)*kcap);m.write(tp,b'\0'*(tcap*4));m.write(tp,struct.pack('<HH',682,1))
native('FieldTools_MigrateInventory');assert m.read(tp,4)==struct.pack('<HH',682,1)
assert native('FieldMove_IsUnlocked',0)==1
# Deferred tools remain behind real TMs, keeping the TM Case's list valid.
m.write(tp+4,struct.pack('<HH',582,3));m.write(tp+8,struct.pack('<HH',689,1))
native('FieldTools_MigrateInventory')
assert m.read(tp,12)==struct.pack('<HHHHHH',582,3,689,1,682,1)
full_pocket_state=savedstate()
native('InitTMCase',0,m.symbols['CB2_ReturnToField']|1,0);m.run(180)
assert m.read(ptr('sTMCaseDynamicResources')+6,1)==b'\x02','TM Case exposed a deferred tool'
m.snap('tm-case-deferred-tools-hidden')
restore(full_pocket_state)
m.write(kp,b'\0'*4);native('FieldTools_MigrateInventory')
assert native('CheckBagHasItem',682,1)==1 and m.read(tp,8)==struct.pack('<HHHH',582,3,689,1)
restore(base)
print('PASS: legacy HM migration, full pocket fallback/retry, unrelated TMs and repeat safety',flush=True)
# Real A interaction at a Route 2 cut tree: decline, then use the shears.
warp('Route2',16,63)
matrices_before_cut=m.read(m.symbols['gOamMatrixAllocBitmap'],4)
base=savedstate();m.press(8,80);m.snap('cut-prompt');m.press(0,90)
assert coords()==(23,70),'Cancel moved player'
restore(base);m.press(8,80);m.press(8,80);m.press(8,1)
# Find the item icon while the field-move banner is on screen.
seen=False
for _ in range(250):
 for i in range(64):
  s=m.read(m.symbols['gSprites']+i*68,68)
  if s[62]&1 and 100<=struct.unpack_from('<h',s,32)[0]<=140 and struct.unpack_from('<h',s,0x2e+5*2)[0]==1 and struct.unpack_from('<H',s,0x2e)[0]==(8192|682):
   assert s[1]&3==3,'Tool banner did not use double-size affine OAM'
   matrix=(struct.unpack_from('<H',s,2)[0]>>9)&31
   assert m.read(m.symbols['gOamMatrices']+matrix*8,8)==struct.pack('<hhhh',128,0,0,128),'Tool banner was not scaled 2x'
   seen=True;m.snap('shears-banner')
 if seen:break
 m.run(1)
if not seen:
 m.snap('cut-debug')
 print('Cut debug',m.read(player(),36).hex(),m.read(m.symbols['gFieldEffectArguments'],16).hex(),m.read(m.symbols['sGlobalScriptContextStatus'],1).hex(),flush=True)
assert seen,'Tool icon banner did not appear'
m.run(400);finish();m.snap('cut-cleared')
assert m.read(m.symbols['gOamMatrixAllocBitmap'],4)==matrices_before_cut,'Outdoor tool banner leaked an affine matrix'
# The object must have been removed; the player can walk into its old square.
m.keys.add(4);m.run(20);m.keys.clear();m.run(90)
assert coords()[1]<70,'Tree was not cleared'
assert native('CheckBagHasItem',682,1)==1
print('PASS: cut prompt, cancellation, item banner, actual tree clearing and reusable shears',flush=True)
# Cave lighting from the registered-item path.
warp('RockTunnel_1F',15,16)
flag('FLAG_SYS_FLASH_ACTIVE',False)
matrices_before_lantern=m.read(m.symbols['gOamMatrixAllocBitmap'],4)
m.write(m.symbols['gSpecialVar_ItemId'],struct.pack('<H',686))
task=native('CreateTask',m.symbols['TaskDummy']|1,8)
m.write(m.symbols['gTasks']+task*40+8+3*2,struct.pack('<h',1))
native('ItemUseOutOfBattle_FieldTool',task)
m.run(500);finish()
assert m.read(m.symbols['gOamMatrixAllocBitmap'],4)==matrices_before_lantern,'Indoor tool banner leaked an affine matrix'
assert native('FlagGet',constant('FLAG_SYS_FLASH_ACTIVE'))==1
m.snap('lantern-lit')
print('PASS: registered Lantern illuminates cave',flush=True)
def registered(item):
 m.write(m.symbols['gSpecialVar_ItemId'],struct.pack('<H',item))
 task=native('CreateTask',m.symbols['TaskDummy']|1,8)
 m.write(m.symbols['gTasks']+task*40+8+3*2,struct.pack('<h',1))
 native('ItemUseOutOfBattle_FieldTool',task)
 m.run(500)
def object_at(x,y):
 return next((m.symbols['gObjectEvents']+i*36 for i in range(16)
              if m.read(m.symbols['gObjectEvents']+i*36,1)[0]&1
              and struct.unpack('<hh',m.read(m.symbols['gObjectEvents']+i*36+16,4))==(x+7,y+7)),None)
# A interaction activates gloves, then normal walking pushes a real boulder.
warp('FuchsiaCity_WardensHouse',12,6,3)
flag('FLAG_SYS_USE_STRENGTH',False)
boulder=object_at(11,6);assert boulder is not None
m.press(8,80);m.press(8,90);finish()
assert native('FlagGet',constant('FLAG_SYS_USE_STRENGTH'))==1
old=struct.unpack('<hh',m.read(boulder+16,4))
m.keys.add(6);m.run(40);m.keys.clear();m.run(120)
assert struct.unpack('<hh',m.read(boulder+16,4))!=old,'Gloves did not enable pushing'
m.snap('gloves-pushed-boulder')
print('PASS: gloves activate Strength state and push a real boulder',flush=True)
# The living Kanto caves retain real smashable rocks.
warp('RockTunnel_B1F',1,21)
rock=object_at(1,20);assert rock is not None
native('VarSet',0x4020,255) # A real Repel prevents the optional rock encounter.
m.press(8,80);m.press(8,80);m.press(8,1);m.run(500);finish()
assert not m.read(rock,1)[0]&1,'Rock Hammer did not remove the rock'
assert native('CheckBagHasItem',687,1)==1
print('PASS: Rock Hammer breaks a real rock without a move user',flush=True)
# Launch from Pallet's actual shoreline, cancel once, then board.
warp('PalletTown',8,16,1)
base=savedstate();m.press(8,80);m.press(0,90)
assert not m.read(m.symbols['gPlayerAvatar'],1)[0]&8
restore(base);m.press(8,80);m.press(8,80);m.press(8,1);m.run(500);finish()
assert m.read(m.symbols['gPlayerAvatar'],1)[0]&8,'Wailmer Wailer did not board'
m.snap('wailmer-on-water')
assert native('CheckBagHasItem',684,1)==1
surf_state=savedstate()
m.keys.add(4);m.run(25);m.keys.clear();m.run(180)
assert not m.read(m.symbols['gPlayerAvatar'],1)[0]&8,'Wailmer Wailer did not dismount'
print('PASS: actual shore prompt/cancel, Wailmer Wailer boarding, movement and dismount',flush=True)
# No retained Kanto map has a waterfall. Build a transient RAM-only three-tile
# waterfall from the water we just boarded; no shipped map data is changed.
restore(surf_state)
layout=ptr('gMapHeader');primary=ptr('gCurrentPrimaryTileset')
attrs=struct.unpack('<I',m.read(primary+20,4))[0]
scratch=m.symbols['gDecompressionBuffer']+0x600
m.write(scratch,m.read(attrs,640*4))
tileset=scratch+0xa00;newlayout=tileset+32
m.write(tileset,m.read(primary,24));m.write(tileset+20,struct.pack('<I',scratch))
m.write(newlayout,m.read(layout,28));m.write(newlayout+16,struct.pack('<I',tileset))
m.write(m.symbols['gMapHeader'],struct.pack('<I',newlayout))
m.write(m.symbols['gCurrentPrimaryTileset'],struct.pack('<I',tileset))
# Copy ordinary water attributes, changing just the behavior to MB_WATERFALL.
water=struct.unpack('<I',m.read(scratch+0x12b*4,4))[0]
m.write(scratch+0x12a*4,struct.pack('<I',(water&~0x1ff)|0x13))
x,y=coords();width=struct.unpack('<I',m.read(m.symbols['VMap'],4))[0]
grid=struct.unpack('<I',m.read(m.symbols['VMap']+8,4))[0]
for offset in (1,2,3):m.write(grid+2*(x+(y-offset)*width),struct.pack('<H',0x112a))
m.write(grid+2*(x+(y-4)*width),struct.pack('<H',0x112b))
m.press(4,30)
base=savedstate();m.press(8,80);m.press(0,90);assert coords()==(x,y)
restore(base);m.press(8,80);m.press(8,80);m.press(8,1);m.run(700);finish()
assert coords()[1]<y-2,('Waterfall failed',coords(),(x,y))
assert native('CheckBagHasItem',688,1)==1
print('PASS: waterfall prompt/cancel, Basculegion Bait cut-in, climb and retained bait (RAM fixture)',flush=True)
# Whistle works with only Tackle and retains real visited-town restrictions.
warp('PalletTown',10,9)
registered(683);m.snap('sky-whistle-destinations')
assert any(m.read(m.symbols['gTasks']+i*40+4,1)!=b'\0' and
           struct.unpack('<I',m.read(m.symbols['gTasks']+i*40,4))[0]==(m.symbols['Task_FlyMap']|1) for i in range(16))
m.press(0,120);m.run(180)
assert coords()==(17,16),'Cancelling Fly moved the player'
# Pallet is the current/default cursor destination and is always visited.
registered(683);m.press(8,900);m.run(600);m.snap('sky-whistle-landed')
save=ptr('gSaveBlock1Ptr');assert tuple(m.read(save+4,2))==ids['PalletTown']
assert native('CheckBagHasItem',683,1)==1
print('PASS: Sky Whistle map, cancel and completed native flight without Fly in party',flush=True)
for move in ('MOVE_CUT','MOVE_FLY','MOVE_SURF','MOVE_STRENGTH','MOVE_FLASH','MOVE_ROCK_SMASH','MOVE_WATERFALL','MOVE_DIVE'):
 assert native('IsMoveHM',constant(move,'moves.h'))==0
print('PASS: former HM moves are freely forgettable',flush=True)
# Use the Lantern through the real Bag UI, then through Select registration.
warp('RockTunnel_1F',15,16)
flag('FLAG_SYS_FLASH_ACTIVE',False)
kp,kcap=pocket(1)
keyids=[struct.unpack('<H',m.read(kp+i*4,2))[0] for i in range(kcap)]
lantern=keyids.index(686)
native('GoToBagMenu',0,1,m.symbols['CB2_ReturnToField']|1);m.run(180)
for _ in range(lantern):m.press(5,12)
m.snap('tools-key-items-bag');m.press(8,40);m.press(8,500);finish()
assert native('FlagGet',constant('FLAG_SYS_FLASH_ACTIVE'))==1,'Bag Lantern failed'
flag('FLAG_SYS_FLASH_ACTIVE',False)
save=ptr('gSaveBlock1Ptr')
m.write(save+0x296,struct.pack('<H',686))
# Save field registeredItemsExtra is exposed through the public structure; use
# the first single registration that the new game starts with.
m.press(2,500);finish()
assert native('FlagGet',constant('FLAG_SYS_FLASH_ACTIVE'))==1,'Select Lantern failed'
print('PASS: actual Bag Use and Select registration invoke the Lantern',flush=True)
# A real old-style HM entry saved to flash migrates on Continue, not only when
# directly invoking the migration function in a fixture.
warp('PalletTown',10,9)
assert native('RemoveBagItem',682,1)==1
tp,tcap=pocket(3)
slot=next(i for i in range(tcap) if m.read(tp+i*4,4)==b'\0'*4)
m.write(tp+slot*4,struct.pack('<HH',682,1))
assert native('TrySavingData',0)==1
m.lib.retro_reset();m.run(360);m.press(3);m.press(8);m.press(8);m.run(180)
for item in range(682,689):assert native('CheckBagHasItem',item,1)==1,('Continue lost tool',item)
assert native('FieldMove_IsUnlocked',0)==1
m.snap('tools-after-continue')
print('PASS: flash save, Continue, automatic old-HM migration and all seven retained tools',flush=True)
