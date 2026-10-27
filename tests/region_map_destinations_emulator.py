#!/usr/bin/env python3
"""Real Sky Whistle/case, retired-page rejection and optional Vidra travel."""
import json, os, pathlib, struct, subprocess
setup=pathlib.Path(__file__).with_name('avatar_wardrobe_emulator.py')
exec(compile(setup.read_text().split("fixture = b'\\x23'")[0],str(setup),'exec'))
m.d=m.d/'region-map-destinations';m.d.mkdir(exist_ok=True)
def ptr(name):return struct.unpack('<I',m.read(m.symbols[name],4))[0]
def constant(name,header='flags.h'):
 out=subprocess.check_output([tool_prefix+'cpp','-P','-I',str(m.root/'include'),'-'],input=f'#include "constants/{header}"\n{name}\n',text=True)
 return eval(out.strip().splitlines()[-1],{'__builtins__':{}},{})
def flag(name,on=True):native('FlagSet' if on else 'FlagClear',constant(name))
groups=json.loads((m.root/'data/maps/map_groups.json').read_text())
ids={n:(g,i) for g,k in enumerate(groups['group_order']) for i,n in enumerate(groups[k])}
has_vidra='Havora_NorthQuadrant' in ids
def current():return tuple(m.read(ptr('gSaveBlock1Ptr')+4,2))
def warp(name,x=10,y=9):
 g,i=ids[name];m.inject(b'\x39'+struct.pack('<BBBhh',g,i,255,x,y)+b'\x27\x6b\x02');m.run(240)
 assert current()==ids[name]
def move_to(x,y):
 for _ in range(60):
  cx,cy=struct.unpack('<hh',m.read(ptr('sMapCursor'),4))
  if (cx,cy)==(x,y):return
  m.press(7 if cx<x else 6 if cx>x else 5 if cy<y else 4,18)
 raise AssertionError(('cursor',x,y))
def region():return m.read(ptr('sRegionMap')+type_offset+5,1)[0]
def icons(which):
 result=[]
 for i in range(25):
  p=ptr('sMapIcons')+0x140+25*16+i*16
  r=m.read(p,16);sprite=struct.unpack_from('<I',r,8)[0]
  if sprite and r[4]==which:result.append((sprite,struct.unpack_from('<H',r,14)[0]))
 return result
def visible(sprite):return not (m.read(sprite+62,1)[0]&4)
def assert_frame():
 # Compare rendered pixels with the real Town Map, not a separate mockup.
 for box,expected in native_frame:
  assert m.screen.crop(box).tobytes()==expected,('Town Map frame/header mismatch',box)
def open_whistle():
 m.press(2,200)
 assert m.read(m.symbols['sCaseSelection'],1)==b'\x01','Case did not select owned whistle'
 m.press(8,500);wait_task('Task_FlyMap');m.run(60);assert_frame()
def switch_menu():
 move_to(21,11);m.press(8,200)
 assert ptr('sSwitchMapMenu')!=0
# Old save flags must not resurrect retired Sevii map pages or icons.
for name in ['FLAG_SYS_SEVII_MAP_123','FLAG_SYS_SEVII_MAP_4567','FLAG_WORLD_MAP_ONE_ISLAND','FLAG_WORLD_MAP_FOUR_ISLAND']:
 flag(name)
# No HM move is needed. Select -> real case -> Sky Whistle -> native Fly picker.
m.inject(b'\x23'+struct.pack('<I',(m.symbols['ScrCmd_createmon']|1)+0x2000000)+struct.pack('<BBHHI',0,6,1,25,0)+b'\x02')
for i in range(4):native('SetMonMoveSlot',m.symbols['gPlayerParty'],33,i)
flag('FLAG_BADGE03_GET');assert native('AddBagItem',683,1)
m.write(native('RegisteredItemAt',0),struct.pack('<H',831))
type_offset=19*2+5*600*2+3*0x800*2
warp('PalletTown')
native('InitRegionMapWithExitCB',0,m.symbols['CB2_ReturnToField']|1);m.run(300)
native_frame=[(box,m.screen.crop(box).tobytes()) for box in
              [(0,0,140,14),(0,40,16,160),(224,40,240,160)]]
m.snap('town-map-frame-reference');m.press(0,400)
open_whistle();assert region()==0
assert len(icons(0))==13,('Kanto town/Center markers',len(icons(0)))
assert not icons(1) and not icons(3),'Retired Sevii icons remain'
assert all(visible(s) for s,_ in icons(0))
m.snap('kanto-whistle-all-cities')
if not has_vidra:
 assert m.read(ptr('sRegionMap')+type_offset+1,1)==b'\0'
 m.press(0,500)
 assert ptr('sRegionMap')==0 and current()==ids['PalletTown']
 print('PASS QOL: native Town Map frame/header pixel match, real case-to-whistle, all 13 Kanto town/Center markers, locked styling, legacy Sevii flags cannot restore pages, cancel cleanup',flush=True)
else:
 assert len(icons(2))==5,'Every Vidra city needs a visible Fly marker'
 switch_menu();m.snap('kanto-vidra-picker')
 m.press(5,60);m.press(8,160);assert region()==2;assert_frame()
 assert all(visible(s) and tag==11 for s,tag in icons(2))
 assert not any(visible(s) for s,_ in icons(0))
 move_to(15,12);m.snap('vidra-whistle-locked');before=current();m.press(8,120)
 assert task_active('Task_FlyMap') and current()==before,'Unvisited island town allowed Fly'
 # A two-entry picker clamps down; cancel restores island marker visibility.
 switch_menu();m.press(5,60);m.press(5,60);m.press(0,160)
 assert region()==2 and all(visible(s) for s,_ in icons(2));assert_frame()
 m.press(0,500)
 assert ptr('sRegionMap')==0
 # The real Center script unlocks only its own town, after ticketed arrival.
 flag('FLAG_QUANTUM_ARRIVED')
 centers=['Havora_PokemonCenter_1F','Corvala_Town_PokemonCenter_1F',
          'Eldervale_Village_PokemonCenter_1F','Myrdal_City_PokemonCenter_1F','Iskora_Village_PokemonCenter_1F']
 towns=['Havora_NorthQuadrant','Corvala_Town','Eldervale_Village','Myrdal_City','Iskora_Village']
 points=[(15,12),(4,10),(6,7),(14,7),(10,2)]
 flags=['PORT','COASTAL','FOREST','LAKE','SNOW']
 warp(centers[0],7,7)
 for i,f in enumerate(flags):assert native('FlagGet',constant('FLAG_QUANTUM_'+f+'_CENTER'))==int(i==0)
 warp('PalletTown');open_whistle();switch_menu();m.press(5,60);m.press(8,160)
 assert sum(tag==10 for _,tag in icons(2))==1
 m.snap('vidra-whistle-one-unlocked');m.press(0,500)
 for center in centers[1:]:warp(center,7,7)
 # Select each of the five real Fly markers and finish native flight.
 for town,point in zip(towns,points):
  warp('PalletTown');open_whistle();switch_menu();m.press(5,60);m.press(8,160)
  assert region()==2 and all(visible(s) and tag==10 for s,tag in icons(2));assert_frame()
  move_to(*point);m.snap('fly-'+town);m.press(8,900);m.run(600)
  assert current()==ids[town],(town,current())
  assert ptr('sRegionMap')==0 and ptr('sMapIcons')==0 and ptr('sMapOpenCloseAnim')==0,'Fly resources leaked'
 # Starting on Vidra opens its own map; flight back to Kanto remains possible.
 open_whistle();assert region()==2;m.snap('vidra-whistle-unlocked')
 switch_menu();m.press(4,60);m.press(8,160);assert region()==0;assert_frame()
 move_to(4,11);m.press(8,900);m.run(600);assert current()==ids['PalletTown']
 # Plain Town Map uses the same two-region picker, not only Fly.
 native('InitRegionMapWithExitCB',0,m.symbols['CB2_ReturnToField']|1);m.run(300)
 switch_menu();m.press(5,60);m.press(8,160);assert region()==2;assert_frame()
 m.snap('vidra-town-map');m.press(0,400)
 assert ptr('sRegionMap')==0
 print('PASS Vidra: native frame/header pixel match across regions and modes, two-region picker, five locked/one unlocked/all unlocked markers, independent actual Center unlocks, all five case-to-whistle flights, Kanto return, Town Map, cancel/switch cleanup',flush=True)
