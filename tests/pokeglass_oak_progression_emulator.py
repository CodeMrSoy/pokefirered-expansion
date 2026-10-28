#!/usr/bin/env python3
"""Fresh-game access, actual Oak parcel handoff, one-mon apps and saved unlock."""
import os, pathlib, struct, subprocess
import quantum_qol_emulator as m
m.d = m.d / 'pokeglass-oak'; m.d.mkdir(exist_ok=True)
source = (m.root / 'tests/avatar_wardrobe_emulator.py').read_text()
exec(source[source.index('native_dir ='):source.index('avatar_var = native')])

def constant(name, header='flags.h'):
    value = subprocess.check_output([tool_prefix + 'cpp', '-P', '-I', str(m.root / 'include'), '-'],
        input=f'#include "constants/{header}"\n{name}\n', text=True)
    return eval(value.strip().splitlines()[-1], {'__builtins__': {}}, {})
def ptr(name): return struct.unpack('<I', m.read(m.symbols[name], 4))[0]
def byte(name): return m.read(m.symbols[name], 1)[0]
def task(name):
    if name not in m.symbols: return False
    return any(m.read(m.symbols['gTasks'] + i*40 + 4, 1)[0] and
        struct.unpack('<I', m.read(m.symbols['gTasks'] + i*40, 4))[0] == (m.symbols[name] | 1) for i in range(16))
def field(): return byte('sGlobalScriptContextStatus') == 2 and not byte('sLockFieldControls')
def locked(label):
    m.press(3, 100)
    assert not task('Task_PokeGlassHub') and not task('Task_PokeGlassIntro'), label
    assert field(), ('Locked Start froze field', label)
    # Registered items and scripted entry share the same progression gate.
    m.inject(b'\x05' + struct.pack('<I', m.symbols['EventScript_AccessPokeGlass']))
    assert not task('Task_PokeGlassHub') and not task('Task_PokeGlassIntro'), label
    assert field(), ('Script gate froze field', label)
    print('PASS locked:', label, flush=True)
def hub():
    assert task('Task_PokeGlassHub')
    assert not task('Task_StartMenuHandleInput')

dexflag = constant('FLAG_SYS_POKEDEX_GET')
assert native('FlagGet', dexflag) == 0
assert native('CheckBagHasItem', 717, 1) == 0
assert byte('gPlayerPartyCount') == 0
locked('fresh game, no device or starter')
# Possession alone must not bypass Oak's story milestone.
assert native('AddBagItem', 717, 1)
locked('device present before Oak')
registered = native('RegisteredItemAt', 0)
m.write(registered, struct.pack('<H', 717)); m.press(2, 60); m.press(8, 100)
assert not task('Task_PokeGlassHub') and field(), 'Registered item bypassed Oak'
m.write(registered, b'\0\0')
assert native('RemoveBagItem', 717, 1)
native('FlagSet', dexflag); locked('Dex flag without the device'); native('FlagClear', dexflag)
# The ordinary givemon command supplies a single starter, rather than the old
# six-mon/unlocked-Pokedex fixture that masked the early-game problem.
m.inject(b'\x23' + struct.pack('<I', (m.symbols['ScrCmd_createmon'] | 1) + 0x2000000)
         + struct.pack('<BBHHI', 0, 6, 1, 5, 0) + b'\x02')
native('FlagSet', constant('FLAG_SYS_POKEMON_GET'))
assert byte('gPlayerPartyCount') == 1
locked('starter received, Oak parcel not delivered')

# Talk to the real Oak object. His complete parcel/Dex/PokeGlass script must
# grant access itself; do not set the Dex flag or device in this test stage.
native('FlagClear', constant('FLAG_HIDE_OAK_IN_HIS_LAB'))
native('VarSet', constant('VAR_MAP_SCENE_PALLET_TOWN_PROFESSOR_OAKS_LAB', 'vars.h'), 4)
native('VarSet', constant('VAR_MAP_SCENE_VIRIDIAN_CITY_MART', 'vars.h'), 1)
assert native('AddBagItem', constant('ITEM_OAKS_PARCEL', 'items.h'), 1)
import json
groups = json.loads((m.root / 'data/maps/map_groups.json').read_text())
ids = {name:(g,i) for g,key in enumerate(groups['group_order']) for i,name in enumerate(groups[key])}
g,i = ids['PalletTown_ProfessorOaksLab']
m.inject(b'\x39' + struct.pack('<BBBhh', g, i, 255, 6, 4) + b'\x27\x6b\x02'); m.run(120)
player = m.symbols['gObjectEvents'] + m.read(m.symbols['gPlayerAvatar'] + 5, 1)[0]*36
labvar = native('GetVarPointer', constant('VAR_MAP_SCENE_PALLET_TOWN_PROFESSOR_OAKS_LAB', 'vars.h'))
# Face Oak through ordinary field input; the tile ahead is occupied by him.
m.press(4, 12)
m.press(8, 60)
for _ in range(180):
    m.press(8, 45)
    if struct.unpack('<H', m.read(labvar, 2))[0] == 6 and field(): break
else:
    m.snap('oak-gift-timeout')
    pc = struct.unpack('<I', m.read(m.symbols['sGlobalScriptContext'] + 8, 4))[0]
    nearby = sorted([(pc - address, name) for name, address in m.symbols.items() if address <= pc and name.startswith('PalletTown_ProfessorOaksLab_')])[:3]
    print('OAK TIMEOUT', hex(pc), nearby, 'context', m.read(m.symbols['sGlobalScriptContext'], 12).hex(), flush=True)
    for slot in range(16):
        raw = m.read(m.symbols['gTasks'] + 40*slot, 40)
        if raw[4]:
            fn = struct.unpack_from('<I', raw)[0] & ~1
            print('TASK', slot, [n for n,a in m.symbols.items() if a & ~1 == fn], struct.unpack_from('<16h', raw, 8), flush=True)
    raise AssertionError('Actual Oak gift scene did not finish')
assert native('FlagGet', dexflag) == 1
assert native('CheckBagHasItem', 717, 1) == 1
assert native('CheckBagHasItem', constant('ITEM_ULTRA_BALL', 'items.h'), 5) == 1
assert native('CanUsePokeGlass') == 1
m.snap('oak-gift-complete')
print('PASS actual Oak parcel dialogue grants Pokédex, PokéGlass and five Ultra Balls', flush=True)

m.press(3, 120); hub(); assert byte('sHubCursor') == 0
m.press(8, 100); assert task('Task_PokeGlassPokedex'); m.snap('oak-dex-list')
m.press(8, 120); assert task('Task_PokeGlassPokedex'); m.snap('oak-dex-entry')
m.press(0, 60); m.press(0, 60); hub()
m.press(7, 30); assert byte('sHubCursor') == 1
m.press(8, 120); assert task('Task_HandleChooseMonInput'); m.snap('oak-party-one-starter')
m.press(8, 60); m.snap('oak-party-actions'); m.press(0, 60)
m.press(0, 120); hub(); m.press(0, 100); assert field()
print('PASS actual post-Oak save: Dex list/entry and one-starter Party/actions open and return', flush=True)

# Flash save/reload must keep Oak's unlock and both app paths working.
assert native('TrySavingData', 0) == 1
m.lib.retro_reset(); m.run(360); m.press(3); m.press(8, 240); m.press(0, 60)
assert native('CanUsePokeGlass') == 1
m.press(3, 120); hub()
# The launcher remembers its last cursor, so return to the first app.
if byte('sHubCursor') == 1: m.press(6, 30)
m.press(8, 100); assert task('Task_PokeGlassPokedex')
m.press(0, 100); hub(); m.press(7, 30); m.press(8, 120)
assert task('Task_HandleChooseMonInput')
m.press(0, 120); hub(); m.press(0, 100); assert field()
print('PASS flash-save reload retains the earned unlock and both apps', flush=True)
