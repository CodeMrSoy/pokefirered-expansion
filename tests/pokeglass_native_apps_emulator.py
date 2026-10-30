"""Native Town Map and six-box tablet Storage integration."""
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
fixture+=b'\x29'+struct.pack('<H',0x829)
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
m.press(4,20);m.press(7,20);m.press(7,20)
from pokeglass_storage_checks import check_storage
check_storage(m, native, wait_task, task_active, original)
print('PASS native Town Map and tablet Storage app integration', flush=True)
