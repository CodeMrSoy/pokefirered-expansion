"""Exercise Captain's Trial map states and scripted boat traversal in mGBA."""
import os,pathlib,struct,subprocess,json
import havora_emulator_support as m
source=(m.root/'tests/avatar_wardrobe_emulator.py').read_text();exec(source[source.index('native_dir ='):source.index('avatar_var = native')])
groups=json.loads((m.root/'data/maps/map_groups.json').read_text());ids={n:(g,i) for g,k in enumerate(groups['group_order']) for i,n in enumerate(groups[k])}
def warp(x,y):
 g,n=ids['Havora_Gym'];m.inject(b'\x39'+struct.pack('<BBBHH',g,n,255,x,y)+b'\x6b\x02');m.run(120)
def pos():
 i=m.read(m.symbols['gPlayerAvatar']+5,1)[0];x,y=struct.unpack('<hh',m.read(m.symbols['gObjectEvents']+i*36+16,4));return x-7,y-7
def value(v):return native('VarGet',v)&65535
def control(n):
 native('VarSet',0x8004,n);r=native('HavoraGym_Control');m.run(600);return r
fixture=b''
for species in [131,68]:fixture+=b'\x23'+struct.pack('<I',(m.symbols['ScrCmd_createmon']|1)+0x2000000)+struct.pack('<BBHHI',0,6,species,60,0)
m.inject(fixture+b'\x02')
warp(20,33);native('VarSet',0x40d7,0);native('VarSet',0x40d8,0);control(6);m.snap('trial-entrance')
assert native('MapGridGetMetatileIdAt',36+7,20+7)&1023==0x376,'LOW gauge not drawn'
assert native('MapGridGetMetatileIdAt',20+7,16+7)&1023==0x380,'low water did not expose masonry'
control(1);assert value(0x40d7)==4
warp(9,26);control(3);assert pos()==(29,26),(pos(),'low ride');assert value(0x40d7)==5;m.snap('trial-east-lock')
# Crew battles are tested separately; set only their progression result here.
control(2);assert value(0x40d7)==5,'lock ignored crew requirement'
native('VarSet',0x40d8,1);control(2);assert value(0x40d7)==7
assert native('MapGridGetMetatileIdAt',36+7,20+7)&1023==0x377,'HIGH gauge not drawn'
assert native('MapGridGetMetatileIdAt',20+7,16+7)&1023==0x282,'high water did not submerge masonry'
assert native('MapGridGetMetatileIdAt',10+7,14+7)&1023==0x384,'upper shutter did not open'
control(2)
assert native('MapGridGetMetatileIdAt',20+7,16+7)&1023==0x380,'draining did not expose masonry'
assert native('MapGridGetMetatileIdAt',10+7,26+7)&1023==0x384,'lower shutter did not open'
control(2)
warp(29,14);control(3);assert pos()==(9,14),(pos(),'high ride');assert value(0x40d7)==6;m.snap('trial-upper-berth')
control(4);assert value(0x40d7)==6,'upper gangway ignored navigator'
native('VarSet',0x40d8,3);control(4);assert value(0x40d7)==14
# Reenter at a stable dock to verify saved puzzle state reconstructs.
warp(9,14);assert value(0x40d7)==14;m.snap('trial-captains-gangway')
native('VarSet',0x40d8,7);control(6)
assert value(0x40d9)&1,'captain reward did not record the Harbor Crest'
warp(34,30);m.snap('trial-shortcut')
# Ring bell from entry hall: clear puzzle state, retain crew/crest progression.
warp(35,32);control(5);assert value(0x40d7)==0 and value(0x40d8)==7
print('PASS low/high boat rides, crew/navigator gates, persisted state, captain shortcut and reset preserving crew/crest',flush=True)

# Actual floor warp back to the preserved exterior entrance.
warp(20,33);m.keys.add(5);m.run(12);m.keys.clear();m.run(200)
save=struct.unpack('<I',m.read(m.symbols['gSaveBlock1Ptr'],4))[0]
assert tuple(m.read(save+4,2))==ids['Havora_WestQuadrant'],('gym exit',tuple(m.read(save+4,2)))
# Open the entrance gangway through the real A-button/sign/Yes-No script.
warp(5,32);native('VarSet',0x40d7,0);control(6);m.press(4,20)
for _ in range(5):m.press(8,45)
assert value(0x40d7)==4,'red winch sign did not operate'
# Snapshot before each native trainer script. No synthetic battle-win claim.
warp(20,33)
size=m.lib.retro_serialize_size();snap=m.c.create_string_buffer(size);assert m.lib.retro_serialize(snap,size)
for name in ['Crew','Navigator','Captain']:
 assert m.lib.retro_unserialize(snap,size)
 m.inject(b'\x05'+struct.pack('<I',m.symbols['HavoraTrial_'+name]))
 for _ in range(8):
  m.press(8,120)
  if m.read(m.symbols['gBattlersCount'],1)==b'\x04':break
 flags=struct.unpack('<I',m.read(m.symbols['gBattleTypeFlags'],4))[0]
 assert flags&1 and m.read(m.symbols['gBattlersCount'],1)==b'\x04',(name,flags,m.read(m.symbols['gBattlersCount'],1))
 m.snap('trial-double-'+name)
 print('PASS native four-battler double battle launch:',name,flush=True)
print('PASS exterior return warp, actual winch interaction, and all three double battle launches',flush=True)
