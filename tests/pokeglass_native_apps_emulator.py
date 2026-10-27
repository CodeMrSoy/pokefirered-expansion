"""Native Town Map and complete native PC behind the unchanged Pokeglass apps."""
import pathlib,struct
setup=pathlib.Path(__file__).with_name('avatar_wardrobe_emulator.py')
exec(compile(setup.read_text().split("fixture = b'\\x23'")[0],str(setup),'exec'))
# Old save flags may not resurrect removed island pages.
def constant(name):
 import subprocess
 out=subprocess.check_output(['arm-none-eabi-cpp','-P','-I',str(m.root/'include'),'-'],input='#include "constants/flags.h"\n'+name+'\n',text=True)
 return eval(out.strip().splitlines()[-1],{'__builtins__':{}},{})
for f in ['FLAG_SYS_SEVII_MAP_123','FLAG_SYS_SEVII_MAP_4567']:native('FlagSet',constant(f))
fixture=b''
for species in [1,4,7]:fixture+=b'\x23'+struct.pack('<I',(m.symbols['ScrCmd_createmon']|1)+0x2000000)+struct.pack('<BBHHI',0,6,species,25,0)
m.inject(fixture+b'\x44'+struct.pack('<HH',717,1)+b'\x02')
original=m.read(m.symbols['gPlayerParty'],300)
m.press(3);wait_task('Task_PokeGlassHub');m.run(30)
m.press(5,20);m.press(8);wait_task('Task_RegionMap');m.run(30)
p=struct.unpack('<I',m.read(m.symbols['sRegionMap'],4))[0]
# RegionMap's byte fields follow its fixed character, layout and BG buffers.
type_offset=19*2+5*600*2+3*0x800*2
assert m.read(p+type_offset,1)==b'\0','Map app opened Fly instead of Town Map'
has_vidra = (m.root/'data/maps/Havora_NorthQuadrant/map.json').exists()
assert m.read(p+type_offset+1,1)==bytes([int(has_vidra)]),'Unexpected region-switch permission'
assert m.read(p+type_offset+5,1)==b'\0','Map not on Kanto'
m.snap('native-town-map')
for key in [10,11,2,2]:m.press(key,20)
assert m.read(p+type_offset+5,1)==b'\0'
assert struct.unpack('<I',m.read(m.symbols['sSwitchMapMenu'],4))[0]==0
m.press(0);wait_task('Task_PokeGlassHub');m.run(30)
# Map tile (4) -> Pokedex (0) -> Party (1) -> Storage (2).
m.press(4,20);m.press(7,20);m.press(7,20);m.press(8);wait_task('Task_PCMainMenu');m.run(30);m.snap('native-pc-menu')
m.press(5,20);m.press(8);wait_task('Task_PokeStorageMain');m.run(30);m.snap('native-pc-deposit')
m.press(8,60);m.press(8,60);wait_task('Task_DepositMenu');m.press(8,240)
m.snap('native-deposit-result')
assert not (m.read(m.symbols['gPlayerParty']+200+19,1)[0]&2),'Native deposit did not compact the party'
box=struct.unpack('<I',m.read(m.symbols['gPokemonStoragePtr'],4))[0]
assert m.read(box+4,80)==original[:80],'Deposited payload changed'
m.press(0,60);m.press(0,240);wait_task('Task_PCMainMenu');m.run(30)
assert m.read(m.symbols['gPlayerPartyCount'],1)==b'\x02','Party count not updated on native PC exit'
m.press(5,20);m.press(8);wait_task('Task_PokeStorageMain');m.run(30);m.snap('native-pc-withdraw')
box=struct.unpack('<I',m.read(m.symbols['gPokemonStoragePtr'],4))[0]
m.press(8,60);m.press(8,240)
assert m.read(m.symbols['gPlayerParty']+200,80)==original[:80],'Native withdrawal failed'
assert m.read(box+4,80)==bytes(80),'Withdrawn slot was not cleared'
assert m.read(m.symbols['gPlayerParty']+200,80)==original[:80],'Withdrawn payload changed'
m.press(0,60);m.press(0,240);wait_task('Task_PCMainMenu');m.run(30)
m.press(5,20);m.press(8);wait_task('Task_PokeStorageMain');m.run(30);m.snap('native-pc-move-items')
m.press(0,60);m.press(0,240);wait_task('Task_PCMainMenu');m.run(30);m.press(0);wait_task('Task_PokeGlassHub');m.run(30);m.press(0)
assert m.read(m.symbols['sGlobalScriptContextStatus'],1)==b'\x02'
# Preserve the original PC's one-Pokemon deposit protection.
m.write(m.symbols['gPlayerParty'],original[:100]+bytes(500));m.write(m.symbols['gPlayerPartyCount'],b'\x01')
m.press(3);wait_task('Task_PokeGlassHub');m.run(30);m.press(8);wait_task('Task_PCMainMenu');m.run(30)
m.press(5,20);m.press(8,120)
assert task_active('Task_PCMainMenu') and not task_active('Task_PokeStorageMain')
assert m.read(m.symbols['gPlayerParty'],80)==original[:80]
m.snap('native-pc-last-mon-protected');m.press(0,30);m.press(0);wait_task('Task_PokeGlassHub');m.run(30);m.press(0)
print('PASS native Town Map with branch-appropriate region switch and legacy Sevii flags, native PC menu, actual deposit and withdrawal/payload integrity, Move Items, last-mon protection, both app returns and unlocked field exit',flush=True)
