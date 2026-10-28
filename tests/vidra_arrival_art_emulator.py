#!/usr/bin/env python3
"""Native arrival art/return, tablet startup, and optional actual Vidra ferry."""
import json
import os
import subprocess
import pathlib
import re
import struct
import numpy as np
import quantum_qol_emulator as m

m.d = m.d / 'vidra-arrival-art'; m.d.mkdir(exist_ok=True)
source = (m.root / 'tests/avatar_wardrobe_emulator.py').read_text()
exec(source[source.index('native_dir ='):source.index('avatar_var = native')])

def byte(name): return m.read(m.symbols[name], 1)[0]
def ptr(name): return struct.unpack('<I', m.read(m.symbols[name], 4))[0]
def task(name):
    if name not in m.symbols: return False
    return any(m.read(m.symbols['gTasks'] + i * 40 + 4, 1)[0] and
        struct.unpack('<I', m.read(m.symbols['gTasks'] + i * 40, 4))[0] == m.symbols[name] | 1 for i in range(16))
def callback(name): return struct.unpack('<I', m.read(m.symbols['gMain'] + 4, 4))[0] == m.symbols[name] | 1

def begin(script):
    address = m.symbols['gDecompressionBuffer']; m.write(address, script)
    ctx = m.symbols['sGlobalScriptContext']; m.write(ctx, b'\0\1\0\0')
    m.write(ctx + 8, struct.pack('<I', address)); m.write(m.symbols['sGlobalScriptContextStatus'], b'\0')

def until(predicate, limit=1200):
    for frame in range(limit):
        m.run(1)
        if predicate(): return frame
    raise AssertionError(('Timed out', predicate))

def field(): return byte('sGlobalScriptContextStatus') == 2 and not byte('sLockFieldControls')

def check_art():
    expected = np.asarray(m.Image.open(m.root / 'graphics/vidra_arrival/vidra.png').convert('RGB')).astype(int)
    actual = np.asarray(m.screen).astype(int)
    assert np.max(np.abs(actual - expected)) <= 8, 'Displayed art differs from supplied native conversion'
    m.snap('vidra-arrival-full-screen')

# Script preview works even when QOL has not imported the harbor maps yet.
specials = re.findall(r'^\s*def_special\s+(\w+)', (m.root / 'data/specials.inc').read_text(), re.M)
preview = b'\x25' + struct.pack('<H', specials.index('ShowVidraArrivalArt')) + b'\x27\x6b\x02'
baseline = m.read(ptr('gSaveBlock1Ptr'), 6)
begin(preview)
until(lambda: callback('CB2_VidraArrival') and byte('sArrivalState') == 2)
# An early button press must not instantly dismiss the art.
m.keys.add(8); m.run(2); m.keys.clear(); m.run(20)
assert callback('CB2_VidraArrival') and byte('sArrivalState') == 2
until(lambda: struct.unpack('<H', m.read(m.symbols['sArrivalFrames'], 2))[0] >= 65)
check_art()
m.keys.add(8); m.run(2); m.keys.clear()
until(field)
assert m.read(ptr('gSaveBlock1Ptr'), 6) == baseline
begin(preview); until(lambda: callback('CB2_VidraArrival'))
frames = until(field)
assert 180 < frames < 360, ('Automatic artwork duration', frames)
assert m.read(ptr('gSaveBlock1Ptr'), 6) == baseline
print('PASS preview: complete image, early-input guard, deliberate skip, automatic return, same field', flush=True)

# Startup/Bag checks begin after Oak's grant.
m.inject(b'\x23' + struct.pack('<I', (m.symbols['ScrCmd_createmon'] | 1) + 0x2000000)
    + struct.pack('<BBHHI', 0, 6, 1, 5, 0)
    + b'\x29' + struct.pack('<H', 0x829) + b'\x44' + struct.pack('<HH', 717, 1) + b'\x02')
m.keys.add(3); m.run(2); m.keys.clear()
until(lambda: task('Task_PokeGlassIntro'))
# Capture the powered tablet before it yields to the launcher.
def lit_tablet():
    for i in range(16):
        address = m.symbols['gTasks'] + i * 40
        if m.read(address + 4, 1)[0] and struct.unpack('<I', m.read(address, 4))[0] == m.symbols['Task_PokeGlassIntro'] | 1:
            return struct.unpack('<hh', m.read(address + 10, 4)) == (1, 4)
    return False
until(lit_tablet); m.snap('new-pokeglass-startup')
until(lambda: task('Task_PokeGlassHub')); m.run(30); m.press(0, 100); assert field()
# Open Bag through the real launcher and select its key-item pocket.
m.press(3, 100); m.press(5, 30); m.press(7, 30); m.press(7, 30); m.press(8, 150)
assert task('Task_BagMenu_HandleInput')
m.press(7, 60)
m.snap('new-pokeglass-bag-icon')
m.press(0, 150); m.press(0, 100); assert field()
print('PASS new tablet startup, Bag app and field return', flush=True)

groups = json.loads((m.root / 'data/maps/map_groups.json').read_text())
ids = {name: (group, index) for group, key in enumerate(groups['group_order']) for index, name in enumerate(groups[key])}
if 'Havora_Harbor' not in ids:
    print('QOL has no Vidra harbor maps: actual route tested in isolated V2 integration build', flush=True)
    raise SystemExit(0)

def current(): return tuple(m.read(ptr('gSaveBlock1Ptr') + 4, 2))
def warp(name, x, y):
    g, i = ids[name]; m.inject(b'\x39' + struct.pack('<BBBhh', g, i, 255, x, y) + b'\x27\x6b\x02'); m.run(240)
    assert current() == ids[name]
def position():
    obj = m.symbols['gObjectEvents'] + m.read(m.symbols['gPlayerAvatar'] + 5, 1)[0] * 36
    x, y = struct.unpack('<hh', m.read(obj + 16, 4)); return x - 7, y - 7

assert native('AddBagItem', 829, 1)
warp('VermilionCity', 23, 30)
m.inject(b'\x05' + struct.pack('<I', m.symbols['VermilionCity_EventScript_FerrySailor']))
m.snap('vidra-ticket-prompt')
for _ in range(8):
    m.keys.add(8); m.run(2); m.keys.clear(); m.run(15)
    if callback('CB2_SetUpSeagallopScene') or callback('MainCB2_SeaGallop'):
        break
phases = []; frames = []; positions = []; unlocked_early = False
for frame in range(1000):
    m.run(1)
    if callback('MainCB2_SeaGallop'): phase = 'boat'
    elif callback('CB2_VidraArrival'): phase = 'art'
    elif task('Task_VidraDisembark'): phase = 'walking'; positions.append(position()); unlocked_early |= not byte('sLockFieldControls')
    else: phase = 'field'
    if not phases or phases[-1] != phase: phases.append(phase)
    if frame % 3 == 0: frames.append(m.screen.copy())
    if phase == 'art' and byte('sArrivalState') == 2 and struct.unpack('<H', m.read(m.symbols['sArrivalFrames'], 2))[0] == 70:
        check_art(); assert current() == ids['VermilionCity'], 'Warp happened before the artwork'
    if 'walking' in phases and phase == 'field' and field(): break
else:
    m.snap('vidra-ferry-timeout')
    raise AssertionError(('Ferry never finished', phases, positions[-5:]))
assert phases.index('boat') < phases.index('art') < phases.index('walking')
assert current() == ids['Havora_Harbor'] and position() == (20, 20), (current(), position())
assert set(positions) >= {(20, 17), (20, 18), (20, 19), (20, 20)}, set(positions)
assert not unlocked_early
assert ptr('sBg3TilemapBuffer') == 0
m.run(40)
m.snap('vidra-disembark-finished')
# The scripted landing must also be on tiles that accept ordinary player input.
for y in range(17, 21):
    assert native('MapGridGetCollisionAt', 20 + 7, y + 7) == 0, ('Blocked landing tile', y)
m.keys.add(5)
until(lambda: position()[1] >= 22, 120)
m.keys.clear(); m.run(60)
assert position() == (20, 22), ('Cannot leave the pier with normal controls', position())
assert field()
m.snap('vidra-walked-off-pier')
frames[0].save(m.d / 'boat-art-disembark.gif', save_all=True, append_images=frames[1:], duration=50, loop=0)
# Return voyages keep the ordinary ferry and never show Vidra's arrival art.
native('VarSet', 0x8004, 11); native('VarSet', 0x8006, 0)
begin(b'\x05' + struct.pack('<I', m.symbols['EventScript_SetSail']))
saw_boat = False
for _ in range(800):
    m.run(1); assert not callback('CB2_VidraArrival')
    saw_boat |= callback('MainCB2_SeaGallop')
    if saw_boat and current() == ids['VermilionCity'] and field(): break
else: raise AssertionError('Return voyage did not finish')
print('PASS real ticketed ferry: boat -> artwork -> three walking steps, controls locked, return voyage unchanged', flush=True)
# Invalid ticket/source requests must not show the art or unlock an arrival.
for origin, ticket in ((0, False), (1, True)):
    if ticket:
        assert native('AddBagItem', 829, 1)
    else:
        assert native('RemoveBagItem', 829, 1)
    native('VarSet', 0x8004, origin); native('VarSet', 0x8006, 11)
    begin(b'\x05' + struct.pack('<I', m.symbols['EventScript_SetSail']))
    sailed = False
    for _ in range(800):
        m.run(1); assert not callback('CB2_VidraArrival'), ('Invalid arrival showed artwork', origin, ticket)
        sailed |= callback('MainCB2_SeaGallop')
        if sailed and current() == ids['VermilionCity'] and field(): break
    else: raise AssertionError(('Invalid route failed to return safely', origin, ticket))
print('PASS no-ticket and wrong-departure requests return safely without arrival artwork', flush=True)
