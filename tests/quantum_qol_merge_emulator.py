#!/usr/bin/env python3
"""V2 island travel state and the merged tablet/candy features coexist."""
import json,os,pathlib,struct,subprocess
import quantum_qol_emulator as m
source=(m.root/'tests/avatar_wardrobe_emulator.py').read_text()
exec(source[source.index('native_dir ='):source.index('avatar_var = native')])
# The island quest and the QOL candy gift use adjacent, independent saved flags.
native('FlagSet',0x4e0);native('FlagSet',0x4e8)
m.inject(b'\x04'+struct.pack('<I',m.symbols['ViridianCity_Mart_EventScript_GiveCapCandy'])+b'\x02')
for _ in range(16):m.press(8,45)
assert native('FlagGet',0x4e0)==1,'Candy gift changed the Stellar Ticket quest flag'
assert native('FlagGet',0x4e8)==0
assert native('CheckBagHasItem',830,1)==1
fixture=b'\x23'+struct.pack('<I',(m.symbols['ScrCmd_createmon']|1)+0x2000000)+struct.pack('<BBHHI',0,6,1,25,0)
m.inject(fixture+b'\x02')
party=m.read(m.symbols['gPlayerParty'],600)
def call(name):m.inject(b'\x23'+struct.pack('<I',(m.symbols[name]|1)+0x2000000)+b'\x27\x02')
call('ShowPokeGlassMap')
assert m.read(m.symbols['sGlassMap'],1)==b'\0'
m.press(11,30)
assert m.read(m.symbols['sGlassMap'],1)==b'\x02','Island preview missing from tablet map'
m.snap('v2-qol-island-tablet-preview')
m.press(0,90)
groups=json.loads((m.root/'data/maps/map_groups.json').read_text())
ids={n:(g,i) for g,k in enumerate(groups['group_order']) for i,n in enumerate(groups[k])}
g,n=ids['Havora_Harbor']
m.inject(b'\x39'+struct.pack('<BBBHH',g,n,255,8,5)+b'\x6b\x02');m.run(240)
assert native('PokeGlassPlayerRegion')==2
call('ShowPokeGlassMap')
assert m.read(m.symbols['sGlassMap'],3)==bytes((2,15,12))
m.snap('v2-qol-havora-tablet-map');m.press(0,90)
call('ShowPokeGlassStorage')
assert m.read(m.symbols['sGlassStorage']+4,2)==b'\0\0'
m.snap('v2-qol-harbor-storage');m.press(0,90)
assert m.read(m.symbols['gPlayerParty'],600)==party
save=struct.unpack('<I',m.read(m.symbols['gSaveBlock1Ptr'],4))[0]
assert m.read(save+4,2)==bytes(ids['Havora_Harbor']),'QOL cleanup retired a new island map'
print('Independent candy/ticket flags, island tablet preview, Havora player map, storage and retained island map passed')
