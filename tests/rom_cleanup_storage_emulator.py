#!/usr/bin/env python3
"""Tablet release/rename replaces PC actions without losing Pokémon/items."""
import struct
import quantum_qol_emulator as m
fixture=b''
for species in (1,4,7,25,133,143):
    fixture+=b'\x23'+struct.pack('<I',(m.symbols['ScrCmd_createmon']|1)+0x2000000)+struct.pack('<BBHHI',0,6,species,25,0)
m.inject(fixture+b'\x02')
original=m.read(m.symbols['gPlayerParty'],600)
boxptr=struct.unpack('<I',m.read(m.symbols['gPokemonStoragePtr'],4))[0]
def call(name):m.inject(b'\x23'+struct.pack('<I',(m.symbols[name]|1)+0x2000000)+b'\x27\x02')
def mode():return m.read(m.symbols['sGlassStorage']+44,1)[0]
call('ShowPokeGlassStorage')
m.press(6,60);m.press(8,60)
m.press(2,60);assert mode()==1
m.press(8,60);assert mode()==2
m.press(8,60);assert mode()==0
assert m.read(m.symbols['gPlayerParty'],600)==original,'Default No changed party'
m.press(2,60);m.press(8,60);m.press(7,60);m.press(8,60)
assert mode()==4 and m.read(m.symbols['gPlayerPartyCount'],1)==b'\x05'
assert m.read(m.symbols['gPlayerParty'],100)==original[100:200]
m.snap('cleanup-storage-released');m.press(8,60)
# Last usable party member is never releasable.
m.write(m.symbols['gPlayerParty'],original[:100]+b'\0'*500)
m.write(m.symbols['gPlayerPartyCount'],b'\x01')
m.press(2,60);m.press(8,60);m.press(7,60);m.press(8,60)
assert m.read(m.symbols['gPlayerPartyCount'],1)==b'\x01'
assert m.read(m.symbols['gPlayerParty'],100)==original[:100]
m.snap('cleanup-storage-protected');m.press(8,60)
# Rename in-place inside the tablet, then verify cancellation does not change it.
name_addr=boxptr+4+14*30*80
before=m.read(name_addr,9)
m.press(2,60);m.press(5,60);m.press(8,60);assert mode()==3
m.press(4,60);m.press(8,60);assert mode()==0
changed=m.read(name_addr,9);assert changed!=before and 255 in changed
m.press(2,60);m.press(5,60);m.press(8,60);m.press(4,60);m.press(0,60)
assert m.read(name_addr,9)==changed,'Cancelled name changed the saved box name'
m.snap('cleanup-storage-renamed')
# Release from a box; a boxed payload has no party Mail field.
m.press(0,60);m.press(0,60)
m.write(boxptr+4,original[100:180])
call('ShowPokeGlassStorage')
m.press(2,60);m.press(8,60);m.press(7,60);m.press(8,60)
assert m.read(boxptr+4,80)==b'\0'*80,'Box release failed'
assert m.read(m.symbols['gPlayerPartyCount'],1)==b'\x01'
print('Default-No, party/box release, last usable protection, rename save/cancel passed')
