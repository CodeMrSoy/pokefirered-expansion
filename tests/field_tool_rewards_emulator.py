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
    if 682 <= item <= 688:
        return native('CheckBagHasItem', item, 1)
    ptr, capacity = pocket()
    return sum(count for value, count in struct.iter_unpack('<HH', m.read(ptr, capacity * 4))
               if value == item)


base = snapshot()
rewards = [
    ('SSAnne_CaptainsOffice', 5, 5, 'Captain', 682, 0x237),
    ('Route16_House', 4, 3, 'Woman', 683, 0x238),
    ('FuchsiaCity_WardensHouse', 3, 6, 'Warden', 685, 0x23a),
    ('Route2_EastBuilding', 4, 7, 'Aide', 686, 0x23b),
    ('SaffronCity', 42, 17, 'RockHammerWorker', 687, 0x2ef),
]
for name, x, y, npc, item, flag in rewards:
    restore(base)
    native('FlagClear', flag)
    if item == 685:
        native('AddBagItem', 749, 1)  # Gold Teeth
        native('FlagSet', 0x189)  # Original Gold Teeth pickup flag
    if item == 686:
        for dex in range(1, 11):
            native('GetSetPokedexFlag', dex, 2)  # SET_SEEN
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
    assert quantity(item) == 1, (name, 'reward not collected in case')
    assert native('FlagGet', flag) == 1, (name, 'reward flag missing')
    if item == 685:
        assert not native('CheckBagHasItem', 749, 1), 'Successful gift retained Gold Teeth'
    start(label)
    finish()
    assert quantity(item) == 1, (name, 'repeat dialogue duplicated reward')
    m.snap(name + '-reward')
    print('PASS:', name, 'collects field tool', item, '; full pocket/retry/repeat safe', flush=True)

# Boundary checks, Eirik's moved reward, no-Surf island and save compatibility
# are covered by eirik_surf_progression_emulator.py. The former Celadon shop
# source was removed when the store moved to Havora; do not test stale scripts.
print('PASS current Captain/Fly/Warden/Route 2/Saffron reward scripts',flush=True)
