#!/usr/bin/env python3
"""Live Saffron gift, bag recovery, badge gate, rock clearing and save reload."""
import json
import os
import pathlib
import re
import struct
import subprocess
import quantum_qol_emulator as m

m.d = m.d / 'saffron-rock-hammer'; m.d.mkdir(exist_ok=True)
source = (m.root / 'tests/avatar_wardrobe_emulator.py').read_text()
exec(source[source.index('native_dir ='):source.index('avatar_var = native')])

def constant(name, header='flags.h'):
    out = subprocess.check_output([tool_prefix+'cpp','-P','-I',str(m.root/'include'),'-'],
        input=f'#include "constants/{header}"\n{name}\n',text=True)
    return eval(out.strip().splitlines()[-1],{'__builtins__':{}},{})
def flag(name, value): native('FlagSet' if value else 'FlagClear', constant(name))
def ptr(name): return struct.unpack('<I',m.read(m.symbols[name],4))[0]
def field(): return m.read(m.symbols['sGlobalScriptContextStatus'],1)==b'\x02' and not m.read(m.symbols['sLockFieldControls'],1)[0]
def finish():
    for _ in range(50):
        m.press(8,40)
        if field(): return
    m.snap('timeout'); raise AssertionError('Conversation did not finish')
groups=json.loads((m.root/'data/maps/map_groups.json').read_text())
ids={n:(g,i) for g,k in enumerate(groups['group_order']) for i,n in enumerate(groups[k])}
def warp(name,x,y):
    g,i=ids[name]
    m.inject(b'\x39'+struct.pack('<BBBhh',g,i,255,x,y)+b'\x27\x6b\x02');m.run(120)
    assert tuple(m.read(ptr('gSaveBlock1Ptr')+4,2))==ids[name] and field()
def pocket():
    p=m.symbols['gBagPockets']+8
    return struct.unpack('<I',m.read(p,4))[0],m.read(p+4,1)[0]
def talk():
    m.press(4,12);m.press(8,90)
    assert not field(), 'Worker did not respond to ordinary input'
    m.snap('worker-dialogue');finish()
def worker_present():
    objects=json.loads((m.root/'data/maps/SaffronCity/map.json').read_text())['object_events']
    local=next(i for i,e in enumerate(objects,1) if e['script']=='SaffronCity_EventScript_RockHammerWorker')
    g,i=ids['SaffronCity']
    return native('GetObjectEventIdByLocalIdAndMap',local,i,g)<16

hammer=constant('ITEM_ROCK_HAMMER','items.h')
case=constant('ITEM_FIELD_ITEM_CASE','items.h')
moves=re.findall(r'^\s*(FIELD_MOVE_\w+)\s*[,=]',(m.root/'include/constants/field_move.h').read_text(),re.M)
move=moves.index('FIELD_MOVE_ROCK_SMASH')
flag('FLAG_BADGE06_GET',False);flag('FLAG_GOT_HM06',False)
flag('FLAG_HIDE_SAFFRON_ROCKETS',False);flag('FLAG_HIDE_SAFFRON_CIVILIANS',True)
warp('SaffronCity',42,17)
assert worker_present()
assert native('MapGridGetCollisionAt',49,23)==0
slots,capacity=pocket();original=m.read(slots,capacity*4)
m.write(slots,struct.pack('<HH',349,1)*capacity)
assert native('CheckBagHasSpace',hammer,1)==0
talk()
assert native('CheckBagHasItem',hammer,1)==0
assert native('FlagGet',constant('FLAG_GOT_HM06'))==0
m.write(slots,original)
talk()
assert native('CheckBagHasItem',hammer,1)==1
assert native('CheckBagHasItem',case,1)==1
assert native('FlagGet',constant('FLAG_GOT_HM06'))==1
assert native('FieldMove_IsUnlocked',move)==0
assert native('CheckBagHasItem',constant('ITEM_BASCULEGION_BAIT','items.h'),1)==0
before=m.read(slots,capacity*4);talk();assert m.read(slots,capacity*4)==before
m.snap('worker-before-sabrina')
print('PASS live worker during Rocket occupation: full-bag retry, unique case/tool gift, Sabrina gate',flush=True)

# Existing owners can talk safely after Silph without receiving another case or tool.
flag('FLAG_HIDE_SAFFRON_ROCKETS',True);flag('FLAG_HIDE_SAFFRON_CIVILIANS',False)
flag('FLAG_GOT_HM06',False)
warp('SaffronCity',42,17);assert worker_present()
before=m.read(slots,capacity*4);talk()
assert m.read(slots,capacity*4)==before
assert native('FlagGet',constant('FLAG_GOT_HM06'))==1
print('PASS post-Silph worker remains available; existing owners receive no duplicate',flush=True)

# Use the NPC-earned hammer on an actual retained rock with no HM move user.
m.inject(b'\x23'+struct.pack('<I',(m.symbols['ScrCmd_createmon']|1)+0x2000000)
    +struct.pack('<BBHHI',0,6,1,100,0)+b'\x02')
for slot in range(4):native('SetMonMoveSlot',m.symbols['gPlayerParty'],33,slot)
warp('RockTunnel_B1F',1,21)
m.press(4,12)
rock=next(m.symbols['gObjectEvents']+i*36 for i in range(16)
    if m.read(m.symbols['gObjectEvents']+i*36,1)[0]&1 and
    struct.unpack('<hh',m.read(m.symbols['gObjectEvents']+i*36+16,4))==(8,27))
m.press(8,90);finish();assert m.read(rock,1)[0]&1, 'Rock broke without Marsh Badge'
flag('FLAG_BADGE06_GET',True)
assert native('FieldMove_IsUnlocked',move)==1
native('VarSet',0x4020,255)  # Repel prevents an optional wild rock encounter.
m.press(4,12);m.press(8,80);m.press(8,80);m.press(8,1);m.run(500);finish()
assert not m.read(rock,1)[0]&1
assert native('CheckBagHasItem',hammer,1)==1
m.snap('npc-hammer-cleared-rock')
print('PASS Sabrina gate on a real rock, then successful reusable hammer use with Tackle-only party',flush=True)

warp('SaffronCity',42,17);talk();m.snap('worker-after-sabrina')
assert native('TrySavingData',0)==1
m.lib.retro_reset();m.run(360);m.press(3);m.press(8,240);m.press(0,60)
assert native('CheckBagHasItem',hammer,1)==1
assert native('FlagGet',constant('FLAG_GOT_HM06'))==1
assert native('FieldMove_IsUnlocked',move)==1
slots,capacity=pocket();before=m.read(slots,capacity*4)
talk();assert m.read(slots,capacity*4)==before
print('PASS flash save/reload retains hammer and repeat dialogue',flush=True)

for label in ('SaffronCity_Text_RockHammerOffer','SaffronCity_Text_RockHammerNeedsBadge',
              'SaffronCity_Text_RockHammerReady','SaffronCity_Text_RockHammerNoRoom'):
    start=m.symbols[label]-0x08000000;text=m.rom[start:m.rom.index(b'\xff',start)]
    for line in re.split(b'[\xfe\xfb\xfa]',text):
        address=m.symbols['gDecompressionBuffer']+0x2800;m.write(address,line+b'\xff')
        assert native('GetStringWidth',2,address,0)<=208, ('Text overflow',label,line)
print('PASS worker dialogue fits normal text borders',flush=True)
