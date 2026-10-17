#!/usr/bin/env python3
"""Run replacement encounter gates and real battle entry in the release ROM."""
import pathlib
import json
import struct
setup=pathlib.Path(__file__).with_name('avatar_wardrobe_emulator.py')
exec(compile(setup.read_text().split("fixture = b'\\x23'")[0],str(setup),'exec'))
fixture=b'\x23'+struct.pack('<I',(m.symbols['ScrCmd_createmon']|1)+0x2000000)+struct.pack('<BBHHI',0,6,6,100,0)
m.inject(fixture+b'\x02')
def warp(g,n,x,y):
    m.inject(b'\x39'+struct.pack('<BBBHH',g,n,255,x,y)+b'\x6b\x02');m.run(240)
def script(name):
    m.inject(b'\x04'+struct.pack('<I',m.symbols[name])+b'\x02')
# Retained NPC trade builders must create valid encrypted Pokemon and preserve level.
for index,requested,offered in [(0,63,122),(1,61,124),(2,32,29),(3,21,83),
                                (4,33,30),(5,55,108),(6,26,101),(7,48,114),(8,77,86)]:
    m.write(m.symbols['gSpecialVar_0x8004'],struct.pack('<H',index))
    m.write(m.symbols['gSpecialVar_0x8005'],b'\0\0')
    assert native('GetInGameTradeSpeciesInfo')==requested,(index,'wrong request')
    native('CreateInGameTradePokemon')
    assert native('GetMonData3',m.symbols['gEnemyParty'],18,0)==offered,(index,'invalid trade Pokemon')
    if index==1:
        assert native('GetMonData3',m.symbols['gEnemyParty'],19,0)==520,'Jynx did not hold Oran Berry'
print('All nine NPC trade builders and Jynx held-item replacement passed',flush=True)
# Inspect the linked shop inventory, not just the source list.
items=[];address=m.symbols['CeladonCity_DepartmentStore_4F_Items']
for offset in range(100):
    item=struct.unpack('<H',m.read(address+offset*2,2))[0]
    if item==0:break
    items.append(item)
else:raise AssertionError('Unterminated shop inventory')
assert {687,688,796}.issubset(items),'Missing HM06/HM07/Linking Cord access'
# Gate routines run exactly as map callbacks do; old fought flags remain authoritative.
for name,fought,hidden in [('MEWTWO',0x2bc,0x81),('ARTICUNO',0x2be,0x82),('MOLTRES',0x2bd,0x52)]:
    native('FlagClear',fought);native('FlagClear',0x82c)
    script('QuantumRelocated_Show_'+name)
    assert native('FlagGet',hidden)==(name=='MEWTWO'), name
    native('FlagSet',0x82c);script('QuantumRelocated_Show_'+name)
    assert native('FlagGet',hidden)==0,name
    native('FlagSet',fought);script('QuantumRelocated_Show_'+name)
    assert native('FlagGet',hidden)==1,(name,'old completion flag ignored')
    native('FlagClear',fought)
# Story rewards remain obtainable through their complete dialogue scripts.
groups=json.loads((m.root/'data/maps/map_groups.json').read_text())
def map_id(name):
    return next((g,groups[key].index(name)) for g,key in enumerate(groups['group_order']) if name in groups[key])
warp(*map_id('SafariZone_SecretHouse'),3,5)
script('SafariZone_SecretHouse_EventScript_Attendant')
for _ in range(24):m.press(8,60)
assert native('CheckBagHasItem',684,1)==1,'Surf reward missing'
native('AddBagItem',749,1);native('FlagSet',0x189)
warp(*map_id('FuchsiaCity_WardensHouse'),3,6)
script('FuchsiaCity_WardensHouse_EventScript_Warden')
for _ in range(28):m.press(8,60)
assert native('CheckBagHasItem',685,1)==1,'Strength reward missing'
assert native('CheckBagHasItem',749,1)==0,'Warden did not consume Gold Teeth'
# The League door must work before and after the ending without Celio's quest.
for cleared in (0,1):
    native('FlagSet' if cleared else 'FlagClear',0x82c)
    native('FlagClear',0x844)
    warp(*map_id('IndigoPlateau_PokemonCenter_1F'),4,2)
    m.keys.add(4);m.run(35);m.keys.clear();m.run(300)
    save=struct.unpack('<I',m.read(m.symbols['gSaveBlock1Ptr'],4))[0]
    expected=map_id('PokemonLeague_LoreleisRoom')
    assert m.read(save+4,2)==bytes(expected),('League door blocked',cleared,m.read(save+4,2),expected)
    m.snap('cleanup-league-door-'+str(cleared))
print('Surf and Strength rewards, Gold Teeth consumption, initial/replay League door without Celio passed',flush=True)
native('FlagSet',0x82c)
size=m.lib.retro_serialize_size();state=c.create_string_buffer(size)
assert m.lib.retro_serialize(state,size)
for name,group,num,x,y,species,level in [
    ('MEWTWO',1,62,4,8,150,70),
    ('ARTICUNO',3,38,67,5,144,50),
    ('MOLTRES',3,42,8,31,146,50),
]:
    assert m.lib.retro_unserialize(state,size)
    warp(group,num,x,y)
    # Interact with the placed map object, rather than calling setwildbattle directly.
    m.press(4,30);m.press(8,60)
    for _ in range(18):
        m.press(8,60)
        flags=struct.unpack('<I',m.read(m.symbols['gBattleTypeFlags'],4))[0]
        if flags & 0x2000: # BATTLE_TYPE_LEGENDARY
            break
    m.run(360)
    flags=struct.unpack('<I',m.read(m.symbols['gBattleTypeFlags'],4))[0]
    assert flags & 0x2000,(name,'not a legendary battle',hex(flags))
    # Encrypted enemy party data has already been expanded into live battle structs.
    assert struct.unpack('<H',m.read(m.symbols['gBattleMons']+96,2))[0]==species,(name,'wrong opponent')
    assert m.read(m.symbols['gBattleMons']+96+44,1)[0]==level,(name,'wrong level')
    m.snap('cleanup-battle-'+name.lower())
    print(name,'real object interaction entered battle',species,'level',level,flush=True)
print('Pre-ending Mewtwo gate, all old fought flags, and three live legendary battle entries passed')
