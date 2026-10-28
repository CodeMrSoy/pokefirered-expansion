#!/usr/bin/env python3
"""Seen-only Lantern, Eirik-earned Surf tool and Surf-gated Gold Teeth/Strength."""
import collections
import json
import os
import pathlib
import re
import struct
import subprocess
import quantum_qol_emulator as m
m.d=m.d/'eirik-surf-progression';m.d.mkdir(exist_ok=True)
source=(m.root/'tests/avatar_wardrobe_emulator.py').read_text()
exec(source[source.index('native_dir ='):source.index('avatar_var = native')])
def constant(name,header='flags.h'):
    s=subprocess.check_output([tool_prefix+'cpp','-P','-I',str(m.root/'include'),'-'],input=f'#include "constants/{header}"\n{name}\n',text=True)
    return eval(s.strip().splitlines()[-1],{'__builtins__':{}},{})
def flag(name,on):native('FlagSet' if on else 'FlagClear',constant(name))
def owns(item):return native('CheckBagHasItem',item,1)
def ptr(name):return struct.unpack('<I',m.read(m.symbols[name],4))[0]
def field():return m.read(m.symbols['sGlobalScriptContextStatus'],1)==b'\x02' and not m.read(m.symbols['sLockFieldControls'],1)[0]
def finish():
    for _ in range(80):
        m.press(8,35)
        if field():return
    m.snap('timeout');raise AssertionError('Dialogue did not finish')
def value(v):return native('VarGet',v)&65535
def script(label):m.inject(b'\x05'+struct.pack('<I',m.symbols[label]))
def pos():
    p=m.symbols['gObjectEvents']+m.read(m.symbols['gPlayerAvatar']+5,1)[0]*36
    x,y=struct.unpack('<hh',m.read(p+16,4));return x-7,y-7
def task(name):
    return any(m.read(m.symbols['gTasks']+i*40+4,1)[0] and struct.unpack('<I',m.read(m.symbols['gTasks']+i*40,4))[0]==(m.symbols[name]|1) for i in range(16))
def until(predicate,limit=1200):
    for _ in range(limit):
        m.run(1)
        if predicate():return
    m.snap('timeout');raise AssertionError('Timed out')
groups=json.loads((m.root/'data/maps/map_groups.json').read_text())
ids={n:(g,i) for g,k in enumerate(groups['group_order']) for i,n in enumerate(groups[k])}
def warp(name,x,y):
    g,i=ids[name];m.inject(b'\x39'+struct.pack('<BBBhh',g,i,255,x,y)+b'\x27\x6b\x02');m.run(120)
    assert tuple(m.read(ptr('gSaveBlock1Ptr')+4,2))==ids[name] and field()
def pocket():
    p=m.symbols['gBagPockets']+8
    return struct.unpack('<I',m.read(p,4))[0],m.read(p+4,1)[0]
def inventory():
    p,n=pocket()
    ids={item for item,count in struct.iter_unpack('<HH',m.read(p,n*4)) if item}
    return {item:native('CountTotalItemQuantityInBag',item) for item in ids}
def talk(up=True):
    if up:m.press(4,12)
    m.press(8,90);assert not field();finish()
def snapshot():
    n=m.lib.retro_serialize_size();b=m.c.create_string_buffer(n);assert m.lib.retro_serialize(b,n);return b.raw
def restore(b):
    v=m.c.create_string_buffer(b);assert m.lib.retro_unserialize(v,len(b))
wailer=constant('ITEM_WAILMER_WAILER','items.h');lantern=constant('ITEM_LANTERN','items.h')
gloves=constant('ITEM_POWER_GLOVES','items.h');teeth=constant('ITEM_GOLD_TEETH','items.h')

# Nine seen is insufficient; ten seen with zero caught must succeed. Include
# non-Kanto species so the wording really means ten species across Quantum.
for dex in list(range(1,6))+list(range(252,256)):native('GetSetPokedexFlag',dex,2)
warp('Route2_EastBuilding',4,7);talk()
assert not owns(lantern)
assert native('FlagGet',constant('FLAG_GOT_HM05'))==0
native('GetSetPokedexFlag',256,2)
assert native('GetNationalPokedexCount',1)==0
slots,cap=pocket();original=m.read(slots,cap*4)
m.write(slots,struct.pack('<HH',349,1)*cap);talk()
assert not owns(lantern) and native('FlagGet',constant('FLAG_GOT_HM05'))==0
m.write(slots,original);talk();assert owns(lantern)
before=m.read(slots,cap*4);talk();assert m.read(slots,cap*4)==before
m.snap('lantern-ten-seen-zero-caught')
print('PASS nine seen rejected; ten national species seen/zero caught accepted; full-bag retry and repeats',flush=True)

warp('SafariZone_SecretHouse',6,6);talk()
assert not owns(wailer) and native('FlagGet',constant('FLAG_GOT_HM03'))==0
print('PASS Safari attendant only supplies guidance, not the Wailmer Wailer',flush=True)

# Without Eirik's tool even a Soul Badge holder cannot enter the pond.
flag('FLAG_BADGE04_GET',True);flag('FLAG_BADGE05_GET',True)
warp('SafariZone_West',10,15)
m.keys.add(5);m.run(50);m.keys.clear();m.run(30)
assert pos()==(10,15)
m.press(8,90);finish();assert pos()==(10,15) and not owns(teeth)
# Prove no entry warp is in the island's dry connected component.
layout=next(l for l in json.loads((m.root/'data/layouts/layouts.json').read_text())['layouts'] if l['id']=='LAYOUT_SAFARI_ZONE_WEST')
words=struct.unpack('<1728H',(m.root/layout['blockdata_filepath']).read_bytes())
seen={(11,17)};queue=collections.deque(seen)
while queue:
    x,y=queue.popleft()
    for xx,yy in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
        if not(0<=xx<48 and 0<=yy<36) or (xx,yy) in seen:continue
        v=words[yy*48+xx]
        if v&0xc00 or v>>12!=3:continue
        seen.add((xx,yy));queue.append((xx,yy))
west=json.loads((m.root/'data/maps/SafariZone_West/map.json').read_text())
assert len(seen)==6 and all((w['x'],w['y']) not in seen for w in west['warp_events'])
assert next(o for o in west['object_events'] if o['script']=='SafariZone_West_EventScript_ItemGoldTeeth')['x']==11
print('PASS Gold Teeth island is isolated from every entrance; badge without Wailer cannot cross',flush=True)

# A healthy party is needed for the gym trial and to exclude random pond fights.
fixture=b''
for species in (1,4,7,25,133,143):
    fixture+=b'\x23'+struct.pack('<I',(m.symbols['ScrCmd_createmon']|1)+0x2000000)+struct.pack('<BBHHI',0,6,species,100,0)
m.inject(fixture+b'\x02')
for i in range(6):
    for move in range(4):native('SetMonMoveSlot',m.symbols['gPlayerParty']+i*100,33,move)
# The uncleared captain must not award the tool merely for being talked to.
native('VarSet',constant('VAR_HAVORA_GYM_PROGRESS','vars.h'),0)
native('ClearTrainerFlag',constant('TRAINER_HAVORA_CAPTAIN','opponents.h'))
warp('Havora_Gym',65,21)
m.press(4,12);m.press(8,90);finish()
assert not owns(wailer)
print('PASS captain refuses an unfinished trial without granting Surf',flush=True)

# Exercise the actual victory continuation: the battle engine normally calls
# this label after the captain loses. Do not grant the reward in the fixture.
# A full pocket with no case must keep the earned reward claimable afterward.
slots,cap=pocket();original=m.read(slots,cap*4)
m.write(slots,struct.pack('<HH',349,1)*cap)
script('HavoraTrial_CaptainWon');finish()
assert not owns(wailer) and native('FlagGet',constant('FLAG_GOT_HM03'))==0
assert value(constant('VAR_VIDRA_CRESTS','vars.h'))&1
assert value(constant('VAR_HAVORA_GYM_PROGRESS','vars.h'))&4
slots,cap=pocket();m.write(slots,original)
warp('Havora_Gym',65,21);m.press(4,12);m.press(8,90);finish()
assert owns(wailer) and native('FlagGet',constant('FLAG_GOT_HM03'))==1
assert native('FieldMove_IsUnlocked',2)==1
before=inventory()
warp('Havora_Gym',65,21);m.press(4,12);m.press(8,90);finish()
assert inventory()==before
print('PASS Eirik victory grants crest; full-Bag reward retries without rematch; repeats give no duplicate',flush=True)

# Now make the complete real shoreline -> Surf -> island -> pickup -> return trip.
warp('SafariZone_West',10,15);native('VarSet',0x4020,255)
m.press(5,12);m.press(8,80);m.press(8,80);m.run(500);finish()
assert m.read(m.symbols['gPlayerAvatar'],1)[0]&8,'Eirik Wailer did not start Surf'
for y in (16,17):
    if pos()==(10,y):continue
    m.keys.add(5)
    try:until(lambda:pos()==(10,y),200)
    finally:m.keys.clear()
    m.run(20)
assert not m.read(m.symbols['gPlayerAvatar'],1)[0]&8
m.run(80)  # Let the Surf dismount finish before turning toward the item.
m.press(7,20);m.press(8,90);assert not field();finish()
m.snap('teeth-pickup-check')
assert owns(teeth) and native('FlagGet',constant('FLAG_HIDE_SAFARI_ZONE_WEST_GOLD_TEETH'))==1
m.snap('surf-island-gold-teeth-collected')
m.press(4,12);m.press(8,80);m.press(8,80);m.run(500);finish()
for y in (16,15):
    if pos()==(10,y):continue
    m.keys.add(4)
    try:until(lambda:pos()==(10,y),200)
    finally:m.keys.clear()
    m.run(20)
assert not m.read(m.symbols['gPlayerAvatar'],1)[0]&8
assert not owns(gloves) and native('FieldMove_IsUnlocked',3)==0
warp('FuchsiaCity_WardensHouse',3,6);talk()
assert owns(gloves) and not owns(teeth) and native('FieldMove_IsUnlocked',3)==1
print('PASS actual Surf crossing, dismount, Gold Teeth pickup, safe return and Warden Strength reward',flush=True)

assert native('TrySavingData',0)==1
m.lib.retro_reset();m.run(360);m.press(3);m.press(8,240);m.press(0,60)
assert owns(wailer) and owns(gloves) and owns(lantern)
assert native('FieldMove_IsUnlocked',2)==1 and native('FieldMove_IsUnlocked',3)==1
print('PASS flash save/reload retains Lantern, Eirik Wailer and Strength progression',flush=True)

for label in ('Route2_EastBuilding_Text_GiveHM05IfSeen10Mons','Route2_EastBuilding_Text_GreatHereYouGo',
              'Route2_EastBuilding_Text_NotEnoughSeen','Route2_EastBuilding_Text_DeclineSeenCheck',
              'SafariZone_SecretHouse_Text_AskEirikForWailer','SafariZone_SecretHouse_Text_ExplainSurf',
              'HavoraTrial_WailmerWailerGift','HavoraTrial_WailmerWailerInstructions','HavoraTrial_WailmerWailerNoRoom',
              'SafariZone_West_Text_PleaseFindWardensLostTeeth'):
    start=m.symbols[label]-0x08000000;text=m.rom[start:m.rom.index(b'\xff',start)]
    # Expand dynamic player/count/item placeholders before measuring.
    text=text.replace(b'\xfd\x01',b'\xd1'*7).replace(b'\xfd\x04',b'\xa2\xa1')
    for line in re.split(b'[\xfe\xfb\xfa]',text):
        address=m.symbols['gDecompressionBuffer']+0x2800;m.write(address,line+b'\xff')
        assert native('GetStringWidth',2,address,0)<=208,('Text overflow',label,line)
print('PASS progression dialogue fits normal text borders',flush=True)
