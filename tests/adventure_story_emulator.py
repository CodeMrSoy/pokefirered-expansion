"""Execute Classic/Quantum Koga, Safari, store, ferry, warp and Bill boundaries."""
import re
import json
import os
import struct
import subprocess
import quantum_qol_emulator as m

mode = int(os.environ.get('ADVENTURE_TEST_MODE', '1'))
m.d = m.d / ('adventure-story-' + str(mode)); m.d.mkdir(exist_ok=True)
source = (m.root / 'tests/rom_cleanup_migration_emulator.py').read_text().split('old=(m.root')[0]
exec(compile(source.replace('import quantum_qol_emulator as m', ''), 'adventure_story_native', 'exec'))
assert native('AdventureMode_SelectNewGame', mode)
native('AdventureMode_NewGame')
assert native('AdventureMode_Get') == mode

groups = json.loads((m.root / 'data/maps/map_groups.json').read_text())
ids = {n: (g, i) for g, key in enumerate(groups['group_order']) for i, n in enumerate(groups[key])}

def constant(name, header='flags.h'):
    if header == 'field_move.h':
        enum = (m.root / 'include/constants/field_move.h').read_text().split('enum FieldMove')[1]
        return re.findall(r'\bFIELD_MOVE_\w+', enum).index(name)
    cpp = os.environ['ARM_NM'].removesuffix('nm') + 'cpp'
    value = subprocess.check_output([cpp, '-P', '-I', str(m.root / 'include'), '-'],
        input=f'#include "constants/{header}"\n{name}\n', text=True)
    return eval(value.strip().splitlines()[-1], {'__builtins__': {}}, {})

def flag(name): return native('FlagGet', constant(name))
def change_flag(name, on): native('FlagSet' if on else 'FlagClear', constant(name))
def field(): return m.read(m.symbols['sGlobalScriptContextStatus'], 1) == b'\x02' and m.read(m.symbols['sLockFieldControls'], 1) == b'\0'
def current(): return tuple(m.read(ptr('gSaveBlock1Ptr') + 4, 2))
def finish():
    for _ in range(70):
        m.press(8, 30)
        if field(): return
    raise AssertionError('Dialogue did not release field controls')
def warp(name, x, y):
    g, i = ids[name]
    m.inject(b'\x39' + struct.pack('<BBBhh', g, i, 255, x, y) + b'\x27\x6b\x02')
    m.run(180)
    assert current() == ids[name] and field(), (name, current())
def event(name):
    m.inject(b'\x04' + struct.pack('<I', m.symbols[name]) + b'\x02')
    finish()
def owns(name): return native('CheckBagHasItem', constant(name, 'items.h'), 1)

def object_position(local):
    g, i = current()
    obj = native('GetObjectEventIdByLocalIdAndMap', local, i, g)
    assert obj < 16, (local, obj)
    return tuple(n - 7 for n in struct.unpack('<hh', m.read(m.symbols['gObjectEvents'] + obj * 36 + 16, 4)))

# No extra Vidra flags may be needed to enter/fight Koga in Classic.
for f in ('FLAG_BADGE05_GET', 'FLAG_DEFEATED_KOGA', 'FLAG_KOGA_RETURNED_FROM_HAVORA'):
    change_flag(f, False)
warp('FuchsiaCity_Gym', 5, 15)
assert bool(flag('FLAG_HIDE_FUCHSIA_GYM_KOGA')) == bool(mode)
assert not flag('FLAG_KOGA_RETURNED_FROM_HAVORA')
m.snap('koga-gym-state')

# Gold Teeth retain their item flag/ID but use the mode's authored position.
change_flag('FLAG_HIDE_SAFARI_ZONE_WEST_GOLD_TEETH', False)
warp('SafariZone_West', 28 if mode == 0 else 12, 15 if mode == 0 else 18)
assert object_position(1) == ((28, 14) if mode == 0 else (11, 17))
m.snap('safari-gold-teeth-position')

warp('SafariZone_SecretHouse', 6, 6)
assert not owns('ITEM_WAILMER_WAILER')
event('SafariZone_SecretHouse_EventScript_Attendant')
assert bool(owns('ITEM_WAILMER_WAILER')) == (mode == 0)
assert bool(flag('FLAG_GOT_HM03')) == (mode == 0)
event('SafariZone_SecretHouse_EventScript_StellarTraveler')
assert bool(owns('ITEM_STELLAR_TICKET')) == bool(mode)
assert bool(flag('FLAG_RECEIVED_SAFARI_STELLAR_TICKET')) == bool(mode)
m.snap('safari-mode-rewards')

# Classic must obtain Strength with the retained tool system, without visiting Vidra.
if mode == 0:
    native('AddBagItem', constant('ITEM_GOLD_TEETH', 'items.h'), 1)
    change_flag('FLAG_HIDE_SAFARI_ZONE_WEST_GOLD_TEETH', True)
    warp('FuchsiaCity_WardensHouse', 3, 6)
    event('FuchsiaCity_WardensHouse_EventScript_Warden')
    assert owns('ITEM_POWER_GLOVES') and flag('FLAG_GOT_HM04')
    # Defeat checks on retained field moves are the traditional Kanto badges.
    change_flag('FLAG_BADGE05_GET', True)
    assert native('FieldMove_IsUnlocked', constant('FIELD_MOVE_SURF', 'field_move.h'))
    change_flag('FLAG_BADGE04_GET', True)
    assert native('FieldMove_IsUnlocked', constant('FIELD_MOVE_STRENGTH', 'field_move.h'))

# Ferry allowlist: no Tri/Rainbow pass, old destination ID or stale flag can sail Sevii.
for destination in range(14):
    expected = 11 if mode == 1 and destination == 11 else 0
    assert native('AdventureMode_FerryDestination', 0, destination, 1) == expected
assert native('AdventureMode_FerryDestination', 0, 11, 0) == 0
for name in ('OneIsland', 'TwoIsland', 'ThreeIsland', 'FourIsland', 'BirthIsland_Exterior'):
    assert native('QuantumIsRetiredMap', *ids[name]) == 1
for name in ('Havora_Harbor', 'Corvala_Town', 'VidraDraft_Veyden'):
    if name in ids:
        assert native('QuantumIsRetiredMap', *ids[name]) == (mode == 0)

# Actual sailing/return script is retained for Quantum, while Classic's forged
# warp still cannot enter Vidra.
if mode == 0:
    g, i = ids['Havora_Harbor']
    m.inject(b'\x39' + struct.pack('<BBBhh', g, i, 255, 12, 17) + b'\x27\x6b\x02'); m.run(180)
    assert current() == ids['PalletTown']
    warp('CeladonCity', 12, 15)
    event('CeladonCity_DepartmentStoreRelocated')
    assert current() == ids['CeladonCity_DepartmentStore_1F']
    sections = re.findall(r'\bMAPSEC_\w+', (m.root / 'include/constants/region_map_sections.h').read_text().split('enum {')[1].split('};')[0])
    assert m.read(m.symbols['gMapHeader'] + 20, 1)[0] == sections.index('MAPSEC_CELADON_CITY')
    # Test the real exit warp to the shared shop's Quantum location.
    m.inject(b'\x39' + struct.pack('<BBBhh', *ids['Havora_Market'], 255, 12, 16) + b'\x27\x6b\x02'); m.run(180)
    assert current() == ids['CeladonCity']
    m.snap('classic-department-store-return')

# Retained shared-layout houses must load their actual interior, not a retired
# layout alias to Pallet Town, and their existing exits must work.
if mode == 1:
    for house in ('Havora_WeaverHouse', 'Havora_FisherHouse', 'Havora_CliffHouse_3'):
        data = json.loads((m.root / 'data/maps' / house / 'map.json').read_text())
        exit = data['warp_events'][0]
        warp(house, exit['x'], exit['y'] - 1)
        layout = struct.unpack('<I', m.read(m.symbols['gMapHeader'], 4))[0]
        assert struct.unpack('<II', m.read(layout, 8)) == (11, 9)
        m.snap(house + '-shared-layout')
        m.keys.add(5); m.run(16); m.keys.clear(); m.run(180)
        target = next(n for n, pair in ids.items() if json.loads((m.root / 'data/maps' / n / 'map.json').read_text())['id'] == exit['dest_map'])
        assert current() == ids[target], (house, current(), target)

# Bill stays absent with stale invitation variables and after the real Blaine
# victory/reward script (without simulating a completed campaign).
for f in ('FLAG_HIDE_CINNABAR_BILL', 'FLAG_HIDE_CINNABAR_POKECENTER_BILL'):
    change_flag(f, False)
native('VarSet', constant('VAR_MAP_SCENE_CINNABAR_ISLAND', 'vars.h'), 1)
warp('CinnabarIsland', 18, 12)
assert flag('FLAG_HIDE_CINNABAR_BILL') and flag('FLAG_HIDE_CINNABAR_POKECENTER_BILL')
assert native('VarGet', constant('VAR_MAP_SCENE_CINNABAR_ISLAND', 'vars.h')) == 4
assert field()
warp('CinnabarIsland_Gym', 15, 17)
event('CinnabarIsland_Gym_EventScript_DefeatedBlaine')
assert flag('FLAG_BADGE07_GET') and flag('FLAG_DEFEATED_BLAINE')
assert flag('FLAG_HIDE_CINNABAR_BILL') and flag('FLAG_HIDE_CINNABAR_POKECENTER_BILL')
assert native('VarGet', constant('VAR_MAP_SCENE_CINNABAR_ISLAND', 'vars.h')) == 4
warp('CinnabarIsland', 18, 12)
assert field()
m.snap('cinnabar-no-sevii-invitation')
assert native('IsNationalPokedexEnabled') == 1
# Exercise the retained League/ending integration in each mode. This is a
# scripted end-state fixture, not a claim that all Gym battles were played.
fixture = b''
for species in (1, 4, 7, 25, 133, 143):
    fixture += b'\x23' + struct.pack('<I', (m.symbols['ScrCmd_createmon'] | 1) + 0x2000000)
    fixture += struct.pack('<BBHHI', 0, 6, species, 25, 0)
m.inject(fixture + b'\x02')
for i in range(8): native('FlagSet', constant('FLAG_BADGE01_GET') + i)
change_flag('FLAG_SYS_CAN_LINK_WITH_RS', False)
warp('IndigoPlateau_PokemonCenter_1F', 5, 5)
event('IndigoPlateau_PokemonCenter_1F_EventScript_DoorGuard')
assert field(), 'Classic League needs no Celio/Sevii state'
m.inject(b'\x04' + struct.pack('<I', m.symbols['EventScript_SetDefeatedEliteFourFlagsVars']) + b'\x6b\x02')
assert native('VarGet', constant('VAR_MAP_SCENE_PALLET_TOWN_OAK', 'vars.h')) == 3
clear_flag = constant('FLAG_SYS_GAME_CLEAR')
flag_bytes = (constant('FLAGS_COUNT') + 7) // 8
clear_pointer = native('GetVarPointer', 0x4000) - flag_bytes + clear_flag // 8
native('EnterHallOfFame')
assert m.read(clear_pointer, 1)[0] & (1 << (clear_flag & 7))
for _ in range(110):
    m.run(60)
    callback = struct.unpack('<I', m.read(m.symbols['gMain'] + 4, 4))[0]
    if callback == (m.symbols['CB2_Credits'] | 1):
        m.snap('adventure-league-credits')
        break
    m.press(8, 5)
else:
    raise AssertionError('League ending did not reach credits')
print('PASS: mode story seams, Classic Surf/Strength/store, Quantum rewards, restricted travel, no Sevii, shared houses and scripted League/Hall of Fame/credits', mode)
