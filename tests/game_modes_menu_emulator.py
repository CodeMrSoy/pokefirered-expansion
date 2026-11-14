"""Exercise the real title menu, mode controls, New Game and Flash persistence."""
import pathlib, types, struct, ctypes as c
p=pathlib.Path(__file__).with_name('quantum_qol_emulator.py').resolve()
m=types.ModuleType('mode_menu_harness');m.__file__=str(p)
exec(compile(p.read_text().split("run(360);press(3);press(8);snap('boot')")[0],str(p),'exec'),m.__dict__)
def task(name):
    fn=m.symbols[name]&~1
    return next((i for i in range(16) if m.read(m.symbols['gTasks']+i*40+4,1)!=b'\0'
        and struct.unpack('<I',m.read(m.symbols['gTasks']+i*40,4))[0]&~1==fn),None)
def ptr(name):return struct.unpack('<I',m.read(m.symbols[name],4))[0]
def wait(name):
    for _ in range(1000):
        if task(name) is not None:return
        m.run(1)
    raise AssertionError('Missing task '+name)
m.run(360);m.press(3);wait('Task_HandleMenuInput');m.snap('game-modes-main-menu')
save=ptr('gSaveBlock2Ptr');blob=m.read(save,0xf80)
needle=bytes([0x71,8])+bytes(32)
indices=[i for i in range(len(blob)) if blob.startswith(needle,i)]
assert len(indices)==1,indices
version=indices[0];options=version+1;seedoff=version-5
m.press(5);m.press(8);wait('Task_RandomizedOptions');m.snap('game-modes-options-default')
def mask():return m.read(ptr('gSaveBlock2Ptr')+options,1)[0]
assert mask()==8
# Independent controls: Pokemon on, moves off, abilities on, cap off, Nuzlocke on.
m.press(8);assert mask()==9
seed=m.read(ptr('gSaveBlock2Ptr')+seedoff,4);assert seed!=bytes(4)
m.press(5);m.press(7);assert mask()==11
m.press(6);assert mask()==9
m.press(5);m.press(8);assert mask()==13
m.press(5);m.press(6);assert mask()==5
m.press(5);m.press(8);assert mask()==21
m.snap('game-modes-options-selected')
# Toggle all randomness off/on without rerolling its stable seed.
m.press(4);m.press(4);m.press(8);assert mask()==17
m.press(4);m.press(4);m.press(8);assert mask()==16
m.press(8);assert mask()==17
assert m.read(ptr('gSaveBlock2Ptr')+seedoff,4)==seed
# Exit/reopen repeatedly to expose window leaks, cursor loss and stale tilemaps.
for _ in range(4):
    m.press(0);wait('Task_HandleMenuInput');m.press(8);wait('Task_RandomizedOptions');assert mask()==17
m.snap('game-modes-options-reopened')
for _ in range(6):m.press(5)
assert mask()==17
m.snap('game-modes-vidra-warning-off')
m.press(7);assert mask()==81
m.press(6);assert mask()==17
m.press(8);assert mask()==81
m.snap('game-modes-vidra-warning-on')
m.press(0);wait('Task_HandleMenuInput')
# General options must preserve game-mode selections as well.
m.press(5);m.press(8);m.run(180);m.press(0);m.run(180);wait('Task_HandleMenuInput');assert mask()==81
m.press(4);m.press(4);m.press(8)
wait('Task_OakSpeech_HandleGenderInput');assert mask()==81,'New Game lost mode selections'
# Complete character setup, as the existing avatar emulator fixtures do.
m.press(8);wait('Task_AvatarChoice_Input');m.press(8)
for _ in range(7):m.press(8)
m.press(3);m.press(8)
for _ in range(5):m.press(8)
m.press(5);m.press(8)
for _ in range(12):m.press(8)
m.press(0);m.press(0);m.press(0)
assert mask()==81,'Field initialization lost modes'
m.snap('game-modes-new-game-field')
# Call real save code through an overworld native-call trampoline.
helpers=pathlib.Path(__file__).with_name('rom_cleanup_migration_emulator.py').read_text().split('old=(m.root')[0]
helpers=helpers.replace('import quantum_qol_emulator as m','')
exec(compile(helpers,'mode_save_helpers','exec'))
# Native wrapper is 32-bit; settings are checked directly in saved memory.
sections=(m.root/'include/constants/region_map_sections.h').read_text().split('enum {')[1].split('};')[0]
import re
route1=re.findall(r'\bMAPSEC_\w+',sections).index('MAPSEC_ROUTE_1')
native('Nuzlocke_BeginEncounter',route1,0);assert native('Nuzlocke_CanCatch')==1
native('Nuzlocke_BeginEncounter',route1,0);assert native('Nuzlocke_CanCatch')==0
history=m.read(ptr('gSaveBlock2Ptr')+version+2,32)
assert any(history)
assert native('TrySavingData',0)==1,'Flash save failed' 
m.lib.retro_get_memory_data.argtypes=[c.c_uint];m.lib.retro_get_memory_data.restype=c.c_void_p
m.lib.retro_get_memory_size.argtypes=[c.c_uint];m.lib.retro_get_memory_size.restype=c.c_size_t
flash=c.string_at(m.lib.retro_get_memory_data(0),m.lib.retro_get_memory_size(0))
(m.d/'game-modes-save.sav').write_bytes(flash)
# Reset core while retaining Flash, then Continue and reopen the modes screen.
m.lib.retro_reset();m.run(360);m.press(3);wait('Task_HandleMenuInput');assert mask()==81
m.snap('game-modes-continue-menu');m.press(5);m.press(5);m.press(8);wait('Task_RandomizedOptions');assert mask()==81
m.snap('game-modes-continue-options')
assert m.read(ptr('gSaveBlock2Ptr')+version+2,32)==history,'Flash reload lost encounter history'
m.press(0);m.press(4);m.press(4);m.press(8);m.run(500)
native('Nuzlocke_BeginEncounter',route1,0);assert native('Nuzlocke_CanCatch')==0,'Continue reset encounter history' 
print('PASS: title modes, independent toggles, stable seed, Vidra gym warning/toggle, repeat open/close, general Options, New Game and Flash reload')
