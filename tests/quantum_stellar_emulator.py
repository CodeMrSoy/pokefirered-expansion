#!/usr/bin/env python3
"""Giovanni quest, bag-full recovery, real ferry/Center/Fly and save persistence."""
import json, os, struct, subprocess
import quantum_qol_emulator as m
m.d = m.d / 'quantum_stellar_emulator'
m.d.mkdir(exist_ok=True)
source=(m.root/'tests/avatar_wardrobe_emulator.py').read_text()
exec(source[source.index('native_dir ='):source.index('avatar_var = native')])
def constant(name,header='flags.h'):
 cpp=os.environ['ARM_NM'].removesuffix('nm')+'cpp'
 out=subprocess.check_output([cpp,'-P','-I',str(m.root/'include'),'-'],input=f'#include "constants/{header}"\n{name}\n',text=True)
 return eval(out.strip().splitlines()[-1],{'__builtins__':{}},{})
def ptr(name):return struct.unpack('<I',m.read(m.symbols[name],4))[0]
groups=json.loads((m.root/'data/maps/map_groups.json').read_text())
ids={n:(g,i) for g,k in enumerate(groups['group_order']) for i,n in enumerate(groups[k])}
def current():return tuple(m.read(ptr('gSaveBlock1Ptr')+4,2))
def warp(name,x=11,y=15):
 g,i=ids[name];m.inject(b'\x39'+struct.pack('<BBBhh',g,i,255,x,y)+b'\x27\x6b\x02');m.run(240)
 assert current()==ids[name],(name,current())
def script(name):m.inject(b'\x05'+struct.pack('<I',m.symbols[name]))
def finish():
 for _ in range(22):
  if m.read(m.symbols['sGlobalScriptContextStatus'],1)==b'\x02':break
  m.press(8,35)
 m.run(120)
def walk(key,frames):m.keys.add(key);m.run(frames);m.keys.clear();m.run(240)
def flag(name):return native('FlagGet',constant('FLAG_'+name))
def ferry(origin,destination):
 native('VarSet',0x8004,origin);native('VarSet',0x8006,destination)
 script('EventScript_SetSail');m.run(1200)
# A party is needed for the nurse, Fly and blackout behavior.
m.inject(b'\x23'+struct.pack('<I',(m.symbols['ScrCmd_createmon']|1)+0x2000000)+struct.pack('<BBHHI',0,6,1,25,0)+b'\x02')
for i in range(1,8):native('FlagSet',constant(f'FLAG_BADGE0{i}_GET'))
assert flag('BADGE08_GET')==0
assert native('GetItemPocket',829)==1
# Viewing/warping to a Center without a ticketed arrival cannot unlock Fly.
warp('QuantumPortCityPokemonCenter1F',7,7)
assert flag('QUANTUM_PORT_CENTER')==0
# No ticket and wrong embarkation port are independently rejected by the ferry.
ferry(0,11);assert current()==ids['VermilionCity'];assert flag('QUANTUM_ARRIVED')==0
assert native('AddBagItem',829,1)==1
ferry(1,11);assert current()==ids['VermilionCity'];assert flag('QUANTUM_ARRIVED')==0
native('RemoveBagItem',829,1)
warp('ViridianCity_Gym',3,3)
assert flag('HIDE_STELLAR_TICKET')==1
script('ViridianCity_Gym_EventScript_DefeatedGiovanni');finish()
assert flag('DEFEATED_LEADER_GIOVANNI')==1
assert flag('BADGE08_GET')==0
assert flag('STELLAR_TICKET_DROPPED')==1
assert flag('HIDE_STELLAR_TICKET')==0
assert flag('HIDE_VIRIDIAN_GIOVANNI')==1
m.snap('stellar-giovanni-ticket-drop')
# Fill the real Key Item pocket and prove the dropped ticket remains recoverable.
pocket=m.symbols['gBagPockets']+1*8
slots=struct.unpack('<I',m.read(pocket,4))[0];capacity=m.read(pocket+4,1)[0]
original=m.read(slots,capacity*4)
for i in range(capacity):m.write(slots+i*4,struct.pack('<HH',349,1))
assert native('CheckBagHasSpace',829,1)==0
script('ViridianCity_Gym_EventScript_StellarTicket');finish()
assert native('CheckBagHasItem',829,1)==0
assert flag('HIDE_STELLAR_TICKET')==0
m.write(slots,original)
script('ViridianCity_Gym_EventScript_StellarTicket');finish()
assert native('CheckBagHasItem',829,1)==1
assert flag('HIDE_STELLAR_TICKET')==1
warp('ViridianCity_Gym',3,3);assert flag('HIDE_STELLAR_TICKET')==1
# Use the actual Vermilion sailor prompt, not a synthetic destination unlock.
warp('VermilionCity',23,30)
script('VermilionCity_EventScript_FerrySailor');m.snap('stellar-vermilion-ticket-prompt')
m.press(8);finish();m.run(1200)
m.snap('stellar-after-ferry');assert current()==ids['QuantumHarbor'],current()
assert flag('QUANTUM_ARRIVED')==1
assert native('CheckBagHasItem',829,1)==1
m.snap('stellar-island-arrival')
# Walk from the ferry pier, through the port, and into its real Center door.
walk(4,55);assert current()==ids['QuantumPortCity'],current()
warp('QuantumPortCity',11,11);m.snap('stellar-port-before-door');walk(4,40);m.snap('stellar-port-after-door')
assert current()==ids['QuantumPortCityPokemonCenter1F'],current()
assert flag('QUANTUM_PORT_CENTER')==1
assert flag('QUANTUM_COASTAL_CENTER')==0
m.snap('stellar-port-center')
# Every Center has independent flags, a valid healing location, and working exits.
sections=['PORT_CITY','COASTAL_CITY','FOREST_TOWN','LAKE_TOWN','SNOW_TOWN']
towns=['PortCity','CoastalCity','ForestTown','LakeTown','SnowTown']
entries=json.loads((m.root/'src/data/region_map/region_map_sections.json').read_text())['map_sections']
for town,sec in zip(towns,sections):
 n='Quantum'+town;center=n+'PokemonCenter1F'
 warp(center,7,7)
 assert flag('QUANTUM_'+sec.split('_')[0]+'_CENTER')==1
 heal=1+next(i for i,e in enumerate(json.loads((m.root/'src/data/heal_locations.json').read_text())['heal_locations']) if e['id']=='HEAL_LOCATION_QUANTUM_'+sec)
 native('SetWarpDestinationToLastHealLocation')
 expected=m.read(m.symbols['sWarpDestination'],8)
 native('SetWarpDestinationToHealLocation',heal)
 assert m.read(m.symbols['sWarpDestination'],8)==expected
 walk(5,40);assert current()==ids[n],(n,current())
 m.snap('stellar-'+sec.lower())
 # Actual Center staircase also returns to its own Center, not Viridian.
 warp(center,2,6);walk(6,40);m.snap('stellar-stairs-'+sec.lower());assert current()==ids[n+'PokemonCenter2F'],current()
 walk(6,40);assert current()==ids[center],current()
# Connected routes must actually cross both ways without an unintended Kanto exit.
for a,b,route,key in [('PortCity','CoastalCity','HarborRoad',6),('CoastalCity','ForestTown','CoastalRoad',4),('ForestTown','LakeTown','WoodlandLink',7),('LakeTown','SnowTown','MountainPass',4)]:
 x,y=(1,11) if key==6 else (22,11) if key==7 else (11,1)
 warp('Quantum'+a,x,y);walk(key,55);assert current()==ids['Quantum'+route],(a,current())
 x,y=(1,11) if key==6 else (22,11) if key==7 else (11,1)
 warp('Quantum'+route,x,y);walk(key,55);assert current()==ids['Quantum'+b],(b,current())
# The return boat works and does not consume the Stellar Ticket.
warp('QuantumHarbor',8,5);ferry(11,0);assert current()==ids['VermilionCity']
assert native('CheckBagHasItem',829,1)==1
# Fly the unlocked port from Kanto using the real map cursor and selection task.
native('CB2_OpenFlyMapWithExitCB',m.symbols['CB2_ReturnToField']|1);m.run(240)
m.write(m.symbols['sLockFieldControls'],b'\x01')
def move_to(x,y):
 for _ in range(55):
  cx,cy=struct.unpack('<hh',m.read(ptr('sMapCursor'),4))
  if (cx,cy)==(x,y):return
  m.press(7 if cx<x else 6 if cx>x else 5 if cy<y else 4,18)
 raise AssertionError(('cursor',x,y))
move_to(21,11);m.press(8);m.press(5,30);m.press(5,30);m.press(8)
move_to(15,12);m.snap('stellar-fly-unlocked');m.press(8);m.run(600)
assert current()==ids['QuantumPortCity'],current()
assert flag('BADGE08_GET')==0
assert native('TrySavingData',0)==1
m.lib.retro_reset();m.run(360);m.press(3);m.press(8);m.press(8);m.run(360)
m.snap('stellar-continue-recap');m.press(0);m.run(600);m.snap('stellar-continue-island')
assert current()==ids['QuantumPortCity'],current()
assert native('CheckBagHasItem',829,1)==1
assert flag('BADGE08_GET')==0
for sec in sections:assert flag('QUANTUM_'+sec.split('_')[0]+'_CENTER')==1
# Legacy eight-badge saves can collect the new ticket without losing their badge.
native('FlagSet',constant('FLAG_BADGE08_GET'))
native('FlagClear',constant('FLAG_STELLAR_TICKET_DROPPED'))
native('RemoveBagItem',829,1)
native('SanitizeQuantumCampaignSave')
warp('ViridianCity_Gym',3,3)
assert flag('BADGE08_GET')==1
assert flag('STELLAR_TICKET_DROPPED')==1
assert flag('HIDE_STELLAR_TICKET')==0
print('Stellar quest, full-bag retry, ticketed ferry, five Centers/exits/stairs, connected routes, return boat, Kanto-to-island Fly and save persistence passed')
