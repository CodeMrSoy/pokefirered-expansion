"""Missing tools remain recognizable, grey, selectable, and unusable; registration retains Bag frame."""
import os,struct,pathlib,subprocess
import quantum_qol_emulator as m
source=(m.root/'tests/avatar_wardrobe_emulator.py').read_text()
exec(source[source.index('native_dir ='):source.index('avatar_var = native')])
m.d=m.d/'case-empty';m.d.mkdir(exist_ok=True)
assert native('AddBagItem',831,1)==1
native('FieldItemCase_OpenUI');m.run(180)
assert m.read(m.symbols['sCaseSelection'],1)==b'\0','Empty case should start with first tool'
for i in range(7):
 assert m.read(m.symbols['sCaseSelection'],1)==bytes([i])
 sid=m.read(m.symbols['sCasePreview'],1)[0];assert sid<64
 attr=struct.unpack('<H',m.read(m.symbols['gSprites']+sid*68+4,2))[0]
 colors=struct.unpack('<16H',m.read(m.symbols['gPlttBufferFaded']+(0x100+(attr>>12)*16)*2,32))
 assert all(c&31==(c>>5)&31==(c>>10)&31 for c in colors),'Missing preview not grayscale'
 m.press(8,30)
 assert struct.unpack('<I',m.read(m.symbols['gMain']+4,4))[0]==(m.symbols['CB2_FieldItemCase']|1),'Uncollected tool launched'
 if i==0:m.snap('empty-case')
 m.press(5,14)
m.press(0,240)
m.press(0,240)  # Direct fixture entry returns to Bag; leave it before native calls.
right_slot=native('RegisteredItemAt',1)
native('GoToBagMenu',0,1,m.symbols['CB2_ReturnToField']|1);m.run(180)
m.press(8,40);m.press(5,20);m.press(8,60)
f=m.symbols['Task_RegisterDirection']|1
assert any(m.read(m.symbols['gTasks']+i*40+4,1)!=b'\0' and struct.unpack('<I',m.read(m.symbols['gTasks']+i*40,4))[0]==f for i in range(16))
m.snap('registration-frame')
# The native selection window's frame has dark pixels at its left border;
# the old unframed description rectangle had only white here.
assert len(set(m.screen.crop((40,120,48,151)).get_flattened_data()))>2,'Missing native prompt border'
m.press(0,120)
m.press(8,40);m.press(5,20);m.press(8,60)
assert any(m.read(m.symbols['gTasks']+i*40+4,1)!=b'\0' and struct.unpack('<I',m.read(m.symbols['gTasks']+i*40,4))[0]==f for i in range(16))
m.press(7,120)
m.snap('registered-right')
assert struct.unpack('<H',m.read(right_slot,2))[0]==831,'Direction was not registered'
print('PASS all seven missing names/previews displayed, grayscale previews, action locks, empty-case default, framed direction prompt, cancel and right registration',flush=True)
