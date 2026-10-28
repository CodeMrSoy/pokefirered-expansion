#!/usr/bin/env python3
"""Actual early ferry, market conversation, gym return and saved progression."""
import ctypes as c
import collections
import re
import json
import os
import pathlib
import struct
import subprocess
import quantum_qol_emulator as m

m.d = m.d / 'havora-koga'; m.d.mkdir(exist_ok=True)
source = (m.root / 'tests/avatar_wardrobe_emulator.py').read_text()
exec(source[source.index('native_dir ='):source.index('avatar_var = native')])

def constant(name, header='flags.h'):
    value = subprocess.check_output([tool_prefix + 'cpp', '-P', '-I', str(m.root / 'include'), '-'],
        input=f'#include "constants/{header}"\n{name}\n', text=True)
    return eval(value.strip().splitlines()[-1], {'__builtins__': {}}, {})
def byte(name): return m.read(m.symbols[name], 1)[0]
def ptr(name): return struct.unpack('<I', m.read(m.symbols[name], 4))[0]
def field(): return byte('sGlobalScriptContextStatus') == 2 and not byte('sLockFieldControls')
def callback(name): return ptr('gMain') == (m.symbols[name] | 1) or struct.unpack('<I', m.read(m.symbols['gMain'] + 4, 4))[0] == (m.symbols[name] | 1)
def task(name):
    return any(m.read(m.symbols['gTasks']+i*40+4,1)[0] and
        struct.unpack('<I',m.read(m.symbols['gTasks']+i*40,4))[0] == (m.symbols[name]|1) for i in range(16))
def flag(name): return native('FlagGet', constant(name))
def setflag(name, value): native('FlagSet' if value else 'FlagClear', constant(name))
def until(predicate, limit=1000):
    for _ in range(limit):
        m.run(1)
        if predicate(): return
    m.snap('timeout'); raise AssertionError('Timed out')
def finish():
    for _ in range(45):
        m.press(8, 40)
        if field(): return
    m.snap('dialogue-timeout'); raise AssertionError('Dialogue did not release controls')

groups = json.loads((m.root / 'data/maps/map_groups.json').read_text())
ids = {name:(g,i) for g,key in enumerate(groups['group_order']) for i,name in enumerate(groups[key])}
def current(): return tuple(m.read(ptr('gSaveBlock1Ptr') + 4, 2))
def warp(name, x, y):
    g,i = ids[name]
    m.inject(b'\x39' + struct.pack('<BBBhh', g,i,255,x,y) + b'\x27\x6b\x02'); m.run(120)
    assert current() == ids[name] and field(), (name, current())
def present(name, local):
    g,i = ids[name]
    return native('GetObjectEventIdByLocalIdAndMap', local, i, g) < 16

def position():
    obj = m.symbols['gObjectEvents'] + m.read(m.symbols['gPlayerAvatar'] + 5, 1)[0] * 36
    x,y = struct.unpack('<hh', m.read(obj + 16, 4))
    return x-7,y-7

def walk_to(name, x, y):
    # Plan on map geometry, then traverse every step through ordinary controls.
    layouts = {d['id']:d for d in json.loads((m.root / 'data/layouts/layouts.json').read_text())['layouts']}
    attributes = []
    for kind in ('primary','secondary'):
        b = (m.root / f'data/tilesets/{kind}/havora_city/metatile_attributes.bin').read_bytes()
        attributes.append(struct.unpack('<'+'I'*(len(b)//4), b))
    attributes = attributes[0][:640] + attributes[1]
    maps = {}
    for district in ('Havora_Harbor','Havora_Market'):
        d = json.loads((m.root / f'data/maps/{district}/map.json').read_text()); l = layouts[d['layout']]
        b = (m.root / l['blockdata_filepath']).read_bytes()
        maps[district] = d,l,struct.unpack('<'+'H'*(len(b)//2),b)
    def tile(n,x,y):
        d,l,t = maps[n]; v = t[y*l['width']+x]
        return v,attributes[v&1023]&511
    start = next(n for n in maps if ids[n] == current()), *position()
    goal = name,x,y
    queue = collections.deque([start]); previous = {start:None}
    while queue:
        n,x,y = queue.popleft()
        if (n,x,y) == goal: break
        for dx,dy,key in ((0,1,5),(0,-1,4),(1,0,7),(-1,0,6)):
            nn=n; xx=x+dx; yy=y+dy; d,l,t=maps[n]
            if xx<0 or xx>=l['width']: continue
            if yy<0 and n=='Havora_Harbor': nn='Havora_Market'; yy=maps[nn][1]['height']-1
            elif yy>=l['height'] and n=='Havora_Market': nn='Havora_Harbor'; yy=0
            elif yy<0 or yy>=l['height']: continue
            v,behavior=tile(nn,xx,yy); v0,_=tile(n,x,y)
            if (v>>10)&3 or 0x10<=behavior<=0x15 or 0x30<=behavior<=0x3f: continue
            if v>>12 != v0>>12 and v>>12 and v0>>12: continue
            if any(e['x']==xx and e['y']==yy for e in maps[nn][0]['object_events']): continue
            state=nn,xx,yy
            if state not in previous:
                previous[state]=(n,x,y),key; queue.append(state)
    assert goal in previous, ('No land route',start,goal)
    path=[]; state=goal
    while previous[state]:
        old,key=previous[state]; path.append((state,key)); state=old
    for (n,x,y),key in reversed(path):
        m.keys.add(key)
        try:
            # Give wandering residents time to yield a shared pavement tile.
            until(lambda: current()==ids[n] and position()==(x,y), 900)
        except AssertionError:
            raise AssertionError(('Blocked land step',n,x,y,'actual',current(),position()))
        finally: m.keys.clear()
        m.run(20)
        assert current()==ids[n] and position()==(x,y), ('Wrong land step', n,x,y,position())
    assert field()

gym = json.loads((m.root / 'data/maps/FuchsiaCity_Gym/map.json').read_text())
market = json.loads((m.root / 'data/maps/Havora_Market/map.json').read_text())
gym_koga = next(i for i,e in enumerate(gym['object_events'], 1) if e['graphics_id'] == 'OBJ_EVENT_GFX_KOGA')
market_koga = next(i for i,e in enumerate(market['object_events'], 1) if e['script'] == 'Havora_Market_Koga')
for name in ('FLAG_BADGE04_GET', 'FLAG_BADGE05_GET', 'FLAG_DEFEATED_KOGA', 'FLAG_KOGA_RETURNED_FROM_HAVORA'):
    setflag(name, False)
warp('FuchsiaCity_Gym', 11, 20)
assert not present('FuchsiaCity_Gym', gym_koga)
m.press(4, 12); m.press(8, 90); m.snap('gym-koga-away'); finish()
print('PASS Koga absent before encounter; gym guide directs player to Havora ferry', flush=True)

# Arrival guard still rejects an unqualified request.
native('VarSet', 0x8004, 0); native('VarSet', 0x8006, 11)
assert native('IsVidraArrival') == 0
setflag('FLAG_BADGE04_GET', True)
assert flag('FLAG_BADGE05_GET') == 0
assert native('CheckBagHasItem', constant('ITEM_STELLAR_TICKET', 'items.h'), 1) == 0
native('VarSet', 0x8004, 0); native('VarSet', 0x8006, 11)
assert native('IsVidraArrival') == 1
native('VarSet', 0x8004, 1)
assert native('IsVidraArrival') == 0
warp('VermilionCity', 23, 30)
m.inject(b'\x05' + struct.pack('<I', m.symbols['VermilionCity_EventScript_FerrySailor']))
m.snap('rainbowbadge-ferry-prompt')
for _ in range(15):
    m.press(8, 15)
    if callback('CB2_SetUpSeagallopScene') or callback('MainCB2_SeaGallop'): break
phases = set()
for _ in range(1600):
    m.run(1)
    if callback('MainCB2_SeaGallop'): phases.add('boat')
    if callback('CB2_VidraArrival'): phases.add('art')
    if task('Task_VidraDisembark'): phases.add('walking')
    if 'walking' in phases and not task('Task_VidraDisembark') and current() == ids['Havora_Harbor'] and field(): break
else: raise AssertionError(('Badge-four ferry failed', phases))
assert phases == {'boat','art','walking'}
assert position() == (20,20)
assert flag('FLAG_QUANTUM_ARRIVED') == 1
m.snap('early-havora-landing')
print('PASS real Rainbow Badge ferry, no Stellar Ticket or Soul Badge: boat, art, landing', flush=True)

walk_to('Havora_Harbor', 15, 24)
m.press(4, 12); m.press(8, 90); assert not field(); m.snap('harbor-koga-market-clue'); finish()
walk_to('Havora_Market', 2, 49)
print('PASS ordinary walking from ferry to harbor clue and market without Surf', flush=True)
assert present('Havora_Market', market_koga)
assert native('MapGridGetCollisionAt', 9, 55) == 0
# Use the actual object from all four approach directions. Each test restores
# the same pre-conversation save state, including the incomplete quest flags.
size = m.lib.retro_serialize_size(); state = c.create_string_buffer(size)
assert m.lib.retro_serialize(state, size)
for x,y,direction in ((2,49,4), (1,48,7), (3,48,6), (2,47,5)):
    assert m.lib.retro_unserialize(state, size)
    warp('Havora_Market', x,y)
    assert present('Havora_Market', market_koga)
    m.press(direction, 12); m.press(8, 90); m.snap(f'koga-shopping-{direction}'); finish()
    assert flag('FLAG_KOGA_RETURNED_FROM_HAVORA') == 1
    assert flag('FLAG_HIDE_FUCHSIA_GYM_KOGA') == 0
    assert flag('FLAG_BADGE05_GET') == 0, 'Talking awarded an unearned badge'
    assert not present('Havora_Market', market_koga)
    assert field()
print('PASS actual Koga conversation and ninja departure from all four sides; no battle/badge granted', flush=True)

warp('FuchsiaCity_Gym', 7, 14)
assert present('FuchsiaCity_Gym', gym_koga)
m.snap('koga-back-at-gym')
# Battle only needs to begin; his unchanged standard trainerbattle script owns
# the existing victory/badge/TM behavior.
size = m.lib.retro_serialize_size(); returned = c.create_string_buffer(size)
assert m.lib.retro_serialize(returned, size)
m.press(4, 12); m.press(8, 90)
for _ in range(30):
    m.press(8, 30)
    if ptr('gBattleTypeFlags') & 8: break
else: raise AssertionError('Returned Koga did not begin his gym battle')
assert m.lib.retro_unserialize(returned, size)
print('PASS Koga returns to his original gym position and starts the existing leader battle', flush=True)
warp('Havora_Harbor', 15, 24)
m.press(4, 12); m.press(8, 90); assert not field(); m.snap('harbor-koga-returned'); finish()
warp('Havora_Market', 2, 49)
assert not present('Havora_Market', market_koga)
assert native('TrySavingData', 0) == 1
m.lib.retro_reset(); m.run(360); m.press(3); m.press(8, 240); m.press(0, 60)
assert flag('FLAG_KOGA_RETURNED_FROM_HAVORA') == 1
assert not present('Havora_Market', market_koga)
warp('FuchsiaCity_Gym', 7,14)
assert present('FuchsiaCity_Gym', gym_koga)
print('PASS save/reload and repeat visits preserve Koga at gym, absent from market', flush=True)

# Upgrade existing saves whether the badge or leader-defeated flag was saved.
for earned in ('FLAG_BADGE05_GET','FLAG_DEFEATED_KOGA'):
    for name in ('FLAG_BADGE05_GET','FLAG_DEFEATED_KOGA','FLAG_KOGA_RETURNED_FROM_HAVORA'):
        setflag(name, False)
    setflag(earned, True)
    warp('Havora_Market', 2,49)
    assert not present('Havora_Market', market_koga)
    warp('FuchsiaCity_Gym', 7,14)
    assert present('FuchsiaCity_Gym', gym_koga)
print('PASS existing post-Koga saves skip the shopping event safely', flush=True)


# Measure the actual encoded new dialogue with the game's normal font.
for label in ('Havora_Market_Text_KogaShopping','Havora_Harbor_Text_KogaClue',
              'Havora_Harbor_Text_KogaReturned','FuchsiaCity_Gym_Text_KogaAway',
              'VermilionCity_Text_VidraFerry'):
    start=m.symbols[label]-0x08000000
    text=m.rom[start:m.rom.index(b'\xff',start)]
    for line in re.split(b'[\xfe\xfb\xfa]',text):
        address=m.symbols['gDecompressionBuffer']+0x2800
        m.write(address,line+b'\xff')
        width=native('GetStringWidth',2,address,0)
        assert width<=208, ('Dialogue too wide',label,width,line)
print('PASS new dialogue stays within the normal 208-pixel text area', flush=True)
