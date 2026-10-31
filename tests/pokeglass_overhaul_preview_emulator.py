"""Populated emulator captures for every redesigned Pokeglass app."""
import pathlib,struct
setup=pathlib.Path(__file__).with_name('avatar_wardrobe_emulator.py')
exec(compile(setup.read_text().split("fixture = b'\\x23'")[0],str(setup),'exec'))
fixture=b''
for species in [1,4,7,25,133,58]:
 fixture+=b'\x23'+struct.pack('<I',(m.symbols['ScrCmd_createmon']|1)+0x2000000)+struct.pack('<BBHHI',0,6,species,25,0)
fixture+=b'\x29'+struct.pack('<H',0x829)+b'\x44'+struct.pack('<HH',717,1)+b'\x02'
m.inject(fixture)
for species in [1,4,7,25,133,58]: native('GetSetPokedexFlag',species,3)
box=struct.unpack('<I',m.read(m.symbols['gPokemonStoragePtr'],4))[0]
for i in range(30):m.write(box+4+i*80,m.read(m.symbols['gPlayerParty']+(i%6)*100,80))
m.press(3);wait_task('Task_PokeGlassHub');m.run(120);m.snap('overhaul-launcher-one')
def app(task,label):
 m.press(8);wait_task(task);m.run(100);m.snap('overhaul-'+label)
 m.press(0);wait_task('Task_PokeGlassHub');m.run(70)
app('Task_PokeGlassPokedex','pokedex')
m.press(7,30);app('Task_HandleChooseMonInput','party')
m.press(7,30);app('Task_PokeGlassStorage','storage')
m.press(5,30);app('Task_BagMenu_HandleInput','bag')
m.press(6,30)
m.press(8);wait_task('Task_PokeGlassStats');m.run(100);m.snap('overhaul-stats')
m.press(2,30);m.run(60);m.snap('overhaul-profile');m.press(2,30);m.run(60);m.snap('overhaul-training');m.press(0);wait_task('Task_PokeGlassHub');m.run(70)
m.press(6,30);app('Task_RegionMap','map')
m.press(6,30);m.run(60);m.snap('overhaul-launcher-two')
# Options (7) -> Save (8) -> Trainer Card (6) -> Field Kit (9).
m.press(6,30);m.press(6,30);m.press(4,30);app('Task_PokeGlassFieldKit','field-kit')
m.press(0);m.run(120)
assert m.read(m.symbols['sGlobalScriptContextStatus'],1)==b'\x02'
print('PASS populated app previews, native Bag/Map, Field Kit and unlocked field return',flush=True)
