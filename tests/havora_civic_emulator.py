"""mGBA civic services, connected districts, every new stair and building door."""
import json,struct,subprocess,os
import havora_emulator_support as m
groups=json.loads((m.root/'data/maps/map_groups.json').read_text())['gMapGroup_Havora']
def number(name):return groups.index(name)
def warp(name,x,y):
 m.inject(b'\x39'+struct.pack('<BBBHH',43,number(name),255,x,y)+b'\x6b\x02');m.run(240)
def loc():
 p=struct.unpack('<I',m.read(m.symbols['gSaveBlock1Ptr'],4))[0]
 return tuple(m.read(p+4,2)),struct.unpack('<hh',m.read(p,4))
def elevation():
 o=m.read(m.symbols['gPlayerAvatar']+5,1)[0]
 return m.read(m.symbols['gObjectEvents']+36*o+11,1)[0]&15
def walk(key,frames):
 m.keys.add(key);m.run(frames);m.keys.clear();m.run(90)
def step(key):
 before=loc();m.keys.add(key)
 for _ in range(50):
  m.run(1)
  if loc()!=before:break
 m.keys.clear();m.run(100);assert loc()!=before,('blocked',before,key)
for source,x,y,key,dest in [
 ('Havora_WestQuadrant',1,69,6,'Vidra_HarborRoad'),('Vidra_HarborRoad',22,9,7,'Havora_WestQuadrant'),
 ('Havora_River',1,67,6,'Havora_WestQuadrant'),('Havora_WestQuadrant',46,67,7,'Havora_River'),
 ('Havora_River',3,1,4,'Havora_NorthQuadrant'),('Havora_NorthQuadrant',51,38,5,'Havora_River'),
 ('Havora_WestQuadrant',17,1,4,'Havora_NorthQuadrant'),('Havora_NorthQuadrant',17,38,5,'Havora_WestQuadrant'),
 ('Havora_Market',13,1,4,'Havora_NorthQuadrant'),('Havora_NorthQuadrant',69,38,5,'Havora_Market'),
 ('Havora_NorthQuadrant',94,23,7,'Havora_DaycareExterior'),('Havora_DaycareExterior',1,23,6,'Havora_NorthQuadrant'),
 ('Havora_NorthQuadrant',69,1,4,'Havora_Lookout'),('Havora_Lookout',7,30,5,'Havora_NorthQuadrant')]:
 warp(source,x,y);walk(key,35);assert loc()[0]==(43,number(dest)),(source,dest,loc())
 m.snap('civic-connection-'+source+'-'+dest)
print('PASS: fourteen seamless civic and coastal-road crossings',flush=True)
for stair in json.loads((m.root/'tools/havora/civic-districts.json').read_text())['stairs']:
 name,x,y=stair['map'],stair['x']+1,stair['y'];warp(name,x,y+2)
 assert elevation()==stair['lower']
 for _ in range(3):step(4)
 assert loc()[1]==(x,y-1) and elevation()==stair['upper'],('ascent',stair,loc(),elevation())
 m.snap('civic-stairs-'+name+'-'+str(y))
 for _ in range(3):step(5)
 assert loc()[1]==(x,y+2) and elevation()==stair['lower'],('descent',stair,loc(),elevation())
print('PASS: all nine civic stairs change actual player elevations in both directions',flush=True)
allmaps={json.loads((m.root/f'data/maps/{n}/map.json').read_text())['id']:n for n in groups}
for source in ['Havora_WestQuadrant','Havora_NorthQuadrant','Havora_DaycareExterior']:
 outdoor=json.loads((m.root/f'data/maps/{source}/map.json').read_text())
 for i,e in enumerate(outdoor['warp_events']):
  warp(source,e['x'],e['y']+1);step(4);dest=allmaps[e['dest_map']]
  assert loc()[0]==(43,number(dest)),('door',source,i,loc())
  interior=json.loads((m.root/f'data/maps/{dest}/map.json').read_text());exit=interior['warp_events'][int(e['dest_warp_id'])]
  warp(dest,exit['x'],exit['y']-1);walk(5,35)
  assert loc()==((43,number(source)),(e['x'],e['y']+1)),('return',source,i,loc())
print('PASS: all civic service and home entrance/return trips',flush=True)
# This project's shared Center first-floor artwork has no upstairs escalator.
# Keep that QOL interior and the legacy upper-floor map unchanged; test the
# accessible ground-floor services rather than claiming an upstairs route.
# Add two test-only party members with the game's standard createmon command.
for species in [25,1]:
 m.inject(b'\x23'+struct.pack('<I',(m.symbols['ScrCmd_createmon']|1)+0x02000000)+struct.pack('<BBHHI',0,6,species,10,0)+b'\x02')
count=lambda:m.read(m.symbols['gPlayerPartyCount'],1)[0]
assert count()>=2,('test party creation',count())
nm=subprocess.check_output([os.environ.get('ARM_NM','arm-none-eabi-nm'),'-S',str(m.root/'pokefirered.elf')],text=True)
partybytes=int(next(l.split()[1] for l in nm.splitlines() if l.endswith(' gPlayerParty')),16)
size=partybytes//6;hp=m.symbols['gPlayerParty']+size-14
maxhp=struct.unpack('<H',m.read(hp+2,2))[0];assert maxhp>1
m.write(hp,struct.pack('<H',1))
m.inject(b'\x29'+struct.pack('<H',0x4E1)+b'\x02') # FLAG_QUANTUM_ARRIVED
warp('Havora_PokemonCenter_1F',7,4);walk(4,1);m.press(8)
for _ in range(18):
 m.press(8,150)
 if struct.unpack('<H',m.read(hp,2))[0]==maxhp:break
assert struct.unpack('<H',m.read(hp,2))[0]==maxhp,'Center nurse did not heal'
save=struct.unpack('<I',m.read(m.symbols['gSaveBlock1Ptr'],4))[0]
assert tuple(m.read(save+0x1C,2))==(43,number('Havora_NorthQuadrant')),'wrong outdoor respawn map'
m.snap('civic-center-healing');m.press(0);m.press(0);m.press(0)
print('PASS: real nurse healing and relocated outdoor respawn storage',flush=True)
warp('Havora_Mart',3,3);walk(6,1);m.press(8)
for _ in range(5):
 m.press(8,120);cb=struct.unpack('<I',m.read(m.symbols['gMain']+4,4))[0]
 if cb&~1==m.symbols['CB2_BuyMenu']&~1:break
assert cb&~1==m.symbols['CB2_BuyMenu']&~1
m.snap('civic-mart-buy');m.press(0);m.press(0);m.press(0);m.press(0)
print('PASS: northern Pokemart opens the native Buy menu',flush=True)
# The coastal attendant reuses the live FireRed raising service and save slot.
before=count();identities={m.read(m.symbols['gPlayerParty']+i*size,4) for i in range(before)}
levels={m.read(m.symbols['gPlayerParty']+i*size,4):m.read(m.symbols['gPlayerParty']+(i+1)*size-16,1)[0] for i in range(before)}
warp('Havora_DaycareInterior',4,5);walk(4,1);m.press(8)
for _ in range(35):
 m.press(8,110)
 if count()==before-1:break
assert count()==before-1,('daycare deposit',before,count())
m.snap('civic-daycare-deposit');m.press(0);m.press(0);m.press(0)
warp('Havora_DaycareExterior',2,31)
for _ in range(20):walk(7,192);walk(6,192)
warp('Havora_DaycareInterior',4,5);walk(4,1);m.press(8)
for _ in range(35):
 m.press(8,110)
 if count()==before:break
assert count()==before,('daycare withdrawal',before,count())
after={m.read(m.symbols['gPlayerParty']+i*size,4) for i in range(before)}
assert identities==after,'daycare did not return the original Pokemon'
assert any(m.read(m.symbols['gPlayerParty']+(i+1)*size-16,1)[0]>levels[m.read(m.symbols['gPlayerParty']+i*size,4)] for i in range(before)),'daycare walking did not increase a returned Pokemon level'
m.snap('civic-daycare-return');m.press(0);m.press(0);m.press(0)
print('PASS: coastal daycare deposits, raises while walking, and returns the same Pokemon through the actual attendant UI',flush=True)
for name,x,y in [('Havora_WestQuadrant',23,16),('Havora_NorthQuadrant',69,22),('Havora_DaycareExterior',29,16),('Havora_Lookout',7,6)]:
 warp(name,x,y);m.snap('civic-overview-'+name)
