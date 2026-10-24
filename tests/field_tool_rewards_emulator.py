#!/usr/bin/env python3
"""Exercise the retained HM reward scripts and replacement shop in the ROM."""
import json
import os
import pathlib
import struct
import subprocess
import quantum_qol_emulator as m

source = (m.root / 'tests/avatar_wardrobe_emulator.py').read_text()
exec(source[source.index('native_dir ='):source.index('avatar_var = native')])
m.d = m.d / 'field-tool-rewards'
m.d.mkdir(exist_ok=True)
groups = json.loads((m.root / 'data/maps/map_groups.json').read_text())
maps = {name: (g, i) for g, key in enumerate(groups['group_order'])
        for i, name in enumerate(groups[key])}


def snapshot():
    size = m.lib.retro_serialize_size()
    state = m.c.create_string_buffer(size)
    assert m.lib.retro_serialize(state, size)
    return state.raw


def restore(state):
    buf = m.c.create_string_buffer(state)
    assert m.lib.retro_unserialize(buf, len(state))


def warp(name, x, y):
    g, n = maps[name]
    m.inject(b'\x39' + struct.pack('<BBBhh', g, n, 255, x, y) + b'\x6b\x02')
    m.run(240)


def start(label):
    m.inject(b'\x04' + struct.pack('<I', m.symbols[label]) + b'\x02')


def finish():
    for _ in range(80):
        if m.read(m.symbols['sGlobalScriptContextStatus'], 1) == b'\x02':
            return
        m.press(8, 60)
    m.snap('unfinished-script')
    raise AssertionError('Reward conversation did not finish')


def pocket():
    address = m.symbols['gBagPockets'] + 8
    return struct.unpack('<I', m.read(address, 4))[0], m.read(address + 4, 1)[0]


def quantity(item):
    ptr, capacity = pocket()
    return sum(count for value, count in struct.iter_unpack('<HH', m.read(ptr, capacity * 4))
               if value == item)


base = snapshot()
rewards = [
    ('SSAnne_CaptainsOffice', 5, 5, 'Captain', 682, 0x237),
    ('Route16_House', 4, 3, 'Woman', 683, 0x238),
    ('SafariZone_SecretHouse', 6, 6, 'Attendant', 684, 0x239),
    ('FuchsiaCity_WardensHouse', 3, 6, 'Warden', 685, 0x23a),
    ('Route2_EastBuilding', 4, 7, 'Aide', 686, 0x23b),
]
for name, x, y, npc, item, flag in rewards:
    restore(base)
    native('FlagClear', flag)
    if item == 685:
        native('AddBagItem', 749, 1)  # Gold Teeth
        native('FlagSet', 0x189)  # Original Gold Teeth pickup flag
    if item == 686:
        for dex in range(1, 11):
            native('GetSetPokedexFlag', dex, 3)  # SET_CAUGHT
    warp(name, x, y)
    ptr, capacity = pocket()
    m.write(ptr, struct.pack('<HH', 349, 1) * capacity)
    if item == 685:
        # Gold Teeth share this pocket; preserve them while filling the rest.
        m.write(ptr + 4, struct.pack('<HH', 749, 1))
    label = name + '_EventScript_' + npc
    start(label)
    finish()
    assert quantity(item) == 0, (name, 'full pocket unexpectedly received item')
    assert native('FlagGet', flag) == 0, (name, 'lost reward with full pocket')
    if item == 682:
        assert native('VarGet', 0x407e) == 0  # Vermilion scene must not advance
    if item == 685:
        assert native('CheckBagHasItem', 749, 1), 'Full pocket consumed Gold Teeth'
    m.write(ptr, b'\0' * 4)
    start(label)
    finish()
    assert quantity(item) == 1, (name, 'reward not placed in Key Items')
    assert native('FlagGet', flag) == 1, (name, 'reward flag missing')
    if item == 685:
        assert not native('CheckBagHasItem', 749, 1), 'Successful gift retained Gold Teeth'
    start(label)
    finish()
    assert quantity(item) == 1, (name, 'repeat dialogue duplicated reward')
    m.snap(name + '-reward')
    print('PASS:', name, 'gives Key Item', item, '; full pocket/retry/repeat safe', flush=True)

# The aide must still require ten caught/owned species, not just ten seen.
restore(base)
native('FlagClear', 0x23b)
for dex in range(1, 11):
    native('GetSetPokedexFlag', dex, 2)  # SET_SEEN
warp('Route2_EastBuilding', 4, 7)
start('Route2_EastBuilding_EventScript_Aide')
finish()
assert quantity(686) == 0 and native('FlagGet', 0x23b) == 0
for dex in range(1, 10):
    native('GetSetPokedexFlag', dex, 3)
start('Route2_EastBuilding_EventScript_Aide')
finish()
assert quantity(686) == 0 and native('FlagGet', 0x23b) == 0
print('PASS: Lantern keeps the ten caught/owned species requirement', flush=True)

# The retired Sevii scripts must not masquerade as live acquisition paths.
for retired in ('OneIsland_KindleRoad_EmberSpa', 'FourIsland_IcefallCave_1F'):
    assert m.symbols[retired] == m.symbols['PalletTown'], retired
assert (m.symbols['OneIsland_KindleRoad_EmberSpa_EventScript_RockSmashMan']
        == m.symbols['QuantumRetiredScript'])
inventory = []
ptr = m.symbols['CeladonCity_DepartmentStore_4F_Items']
for i in range(100):
    item = struct.unpack('<H', m.read(ptr + i * 2, 2))[0]
    if not item:
        break
    inventory.append(item)
else:
    raise AssertionError('Unterminated replacement shop')
for item in (687, 688):
    assert item in inventory and native('GetItemPocket', item) == 1
    assert native('GetItemPrice', item) == 0
    restore(base)
    warp('CeladonCity_DepartmentStore_4F', 3, 14)
    start('CeladonCity_DepartmentStore_4F_EventScript_Clerk')
    m.press(8, 240)  # Buy
    for _ in range(inventory.index(item)):
        m.press(5, 20)
    for _ in range(6):
        m.press(8, 90)
    assert quantity(item) == 1, ('Shop purchase failed', item)
    for _ in range(5):
        m.press(0, 90)
    finish()
    assert quantity(item) == 1
    print('PASS: actual Celadon 4F purchase grants reusable Key Item', item, flush=True)
print('All retained HM gifts and both relocated acquisition paths passed.', flush=True)
