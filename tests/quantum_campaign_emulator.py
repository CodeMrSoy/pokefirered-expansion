#!/usr/bin/env python3
"""Campaign boundaries, V1 save migration, Hall of Fame and credits in mGBA."""
import ctypes as c
import json
import os
import pathlib
import re
import struct
import subprocess

import quantum_qol_emulator as m
m.d = m.d / 'quantum_campaign_emulator'
m.d.mkdir(exist_ok=True)

fixture = b''
for species in (1, 4, 7, 25, 133, 143):
    fixture += b'\x23' + struct.pack('<I', (m.symbols['ScrCmd_createmon'] | 1) + 0x2000000)
    fixture += struct.pack('<BBHHI', 0, 6, species, 25, 0)
m.inject(fixture + b'\x02')
assert m.read(m.symbols['gPlayerPartyCount'], 1) == b'\x06'

# Reuse the native-call fixture already exercised by the Wardrobe tests.
source = (m.root / 'tests/avatar_wardrobe_emulator.py').read_text()
exec(source[source.index('native_dir ='):source.index('avatar_var = native')])

groups = json.loads((m.root / 'data/maps/map_groups.json').read_text())
map_ids = {name: (group, index) for group, key in enumerate(groups['group_order'])
           for index, name in enumerate(groups[key])}
retired = json.loads((m.root / 'docs/quantum-retired-maps.json').read_text())
for name in retired['maps']:
    data = json.loads((m.root / 'data/maps' / name / 'map.json').read_text())
    assert not any(data.get(key) for key in
                   ('connections', 'object_events', 'warp_events', 'coord_events', 'bg_events'))
    assert not (m.root / 'data/maps' / name / 'scripts.inc').exists()
    assert not (m.root / 'data/maps' / name / 'text.inc').exists()
    group, index = map_ids[name]
    assert native('IsQuantumRetiredMap', group, index) == 1, name
for name in ('PalletTown', 'PokemonLeague_ChampionsRoom', 'PokemonLeague_HallOfFame',
             'IndigoPlateau_Exterior', 'OneIsland', 'TwoIsland', 'ThreeIsland',
             'MtEmber_Summit', 'ThreeIsland_BerryForest'):
    assert native('IsQuantumRetiredMap', *map_ids[name]) == 0, name

def constant(name, header):
    # Let the project preprocessor resolve flags/vars and expansion constants.
    cpp = os.environ.get('ARM_NM', 'arm-none-eabi-nm').removesuffix('nm') + 'cpp'
    source = '#include "constants/' + header + '"\n' + name + '\n'
    output = subprocess.check_output([cpp, '-P', '-I', str(m.root/'include'), '-'],
                                     input=source, text=True)
    expression = output.strip().splitlines()[-1]
    return eval(expression, {'__builtins__': {}}, {})

save = struct.unpack('<I', m.read(m.symbols['gSaveBlock1Ptr'], 4))[0]
save2 = struct.unpack('<I', m.read(m.symbols['gSaveBlock2Ptr'], 4))[0]
identity = m.read(save2, 9)
party = m.read(m.symbols['gPlayerParty'], 600)
native('SetCurrentAvatarLook', 5)
# Saving before Oak's starter sequence must not suppress its grass triggers.
oak_var = constant('VAR_MAP_SCENE_PALLET_TOWN_OAK', 'vars.h')
for early_scene in (0, 1):
    native('VarSet', oak_var, early_scene)
    native('SanitizeQuantumCampaignSave')
    assert native('VarGet', oak_var) == early_scene
late_flags = ('FLAG_SYS_SEVII_MAP_4567', 'FLAG_SYS_CAN_LINK_WITH_RS',
              'FLAG_ENABLE_SHIP_NAVEL_ROCK', 'FLAG_ENABLE_SHIP_BIRTH_ISLAND',
              'FLAG_HIDE_CERULEAN_CAVE_GUARD', 'FLAG_WORLD_MAP_FOUR_ISLAND',
              'FLAG_WORLD_MAP_BIRTH_ISLAND_EXTERIOR')
for flag in late_flags:
    native('FlagSet', constant(flag, 'flags.h'))
for var, value in (('VAR_MAP_SCENE_PALLET_TOWN_OAK', 2),
                   ('VAR_MAP_SCENE_ONE_ISLAND_POKEMON_CENTER_1F', 6),
                   ('VAR_MAP_SCENE_PALLET_TOWN_PROFESSOR_OAKS_LAB', 7)):
    native('VarSet', constant(var, 'vars.h'), value)
native('SanitizeQuantumCampaignSave')
for flag in late_flags:
    assert native('FlagGet', constant(flag, 'flags.h')) == 0, flag
assert native('GetCurrentAvatarLook') == 5
assert m.read(save2, 9) == identity
assert m.read(m.symbols['gPlayerParty'], 600) == party

# Save in a deleted location, reset, and use the real Continue path.
group, index = map_ids['FourIsland']
for offset in (4, 12, 20, 28, 36):
    m.write(save + offset, struct.pack('<bbbxhh', group, index, -1, 16, 17))
m.write(save + 0x32, struct.pack('<H', constant('LAYOUT_FOUR_ISLAND', 'layouts.h')))
assert native('TrySavingData', 0) == 1
m.lib.retro_reset()
m.run(360)
m.press(3)
m.press(8)
m.press(8)
m.run(360)
save = struct.unpack('<I', m.read(m.symbols['gSaveBlock1Ptr'], 4))[0]
assert tuple(m.read(save + 4, 2)) == map_ids['PalletTown']
assert struct.unpack('<hh', m.read(save, 4)) == (6, 8)
assert native('GetCurrentAvatarLook') == 5
assert m.read(m.symbols['gPlayerParty'], 600) == party
m.snap('campaign-v1-save-relocated')
m.keys.add(7)
m.run(24)
m.keys.clear()
m.run(30)
assert struct.unpack('<hh', m.read(save, 4)) != (6, 8), 'Player cannot move after migration'

# Run the end-of-League script, then the real Hall of Fame and credits flow.
m.inject(b'\x04' + struct.pack('<I', m.symbols['EventScript_SetDefeatedEliteFourFlagsVars'])
         + b'\x6b\x02')
assert native('VarGet', constant('VAR_MAP_SCENE_PALLET_TOWN_OAK', 'vars.h')) == 3
assert native('FlagGet', constant('FLAG_HIDE_POSTGAME_GOSSIPERS', 'flags.h')) == 1
game_clear = constant('FLAG_SYS_GAME_CLEAR', 'flags.h')
game_clear_pointer = native('GetFlagAddr', game_clear)
native('EnterHallOfFame')
assert m.read(game_clear_pointer, 1)[0] & (1 << (game_clear & 7))
for _ in range(110):
    m.run(60)
    callback = struct.unpack('<I', m.read(m.symbols['gMain'] + 4, 4))[0]
    if callback == (m.symbols['CB2_Credits'] | 1):
        m.snap('campaign-credits')
        break
    m.press(8, 5)
else:
    raise AssertionError('Ending did not reach credits')
print('127 retired map boundaries, main/early-island preservation, V1 save relocation, movement, identity/party/skin preservation, Hall of Fame, and credits passed')
