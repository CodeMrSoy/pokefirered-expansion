#!/usr/bin/env python3
"""Storage's fixed grid, opaque screen, preview and stable sprite ownership."""
import struct
import numpy as np
import quantum_qol_emulator as m
fixture=b''
for species in (1,4,7,25,133,143):
    fixture+=b'\x23'+struct.pack('<I',(m.symbols['ScrCmd_createmon']|1)+0x2000000)+struct.pack('<BBHHI',0,6,species,25,0)
m.inject(fixture+b'\x44'+struct.pack('<HH',717,1)+b'\x02')
party=m.read(m.symbols['gPlayerParty'],600)
storage=struct.unpack('<I',m.read(m.symbols['gPokemonStoragePtr'],4))[0]
for i in range(30):m.write(storage+4+i*80,party[(i%6)*100:(i%6)*100+80])
def call():m.inject(b'\x23'+struct.pack('<I',(m.symbols['ShowPokeGlassStorage']|1)+0x2000000)+b'\x27\x02')
def icons():return m.read(m.symbols['sGlassStorage']+7,36)
def positions(ids):return [m.read(m.symbols['gSprites']+i*68+32,4) for i in ids]
def alive():return sum(bool(m.read(m.symbols['gSprites']+i*68+62,1)[0]&1) for i in range(64))
initial_count=alive()
call()
assert struct.unpack('<H',m.read(0x4000050,2))[0]==0,'Storage screen still blends with field'
ids=icons()[:30];xy=positions(ids)
assert all(i<64 for i in ids)
portrait=struct.unpack('<H',m.read(m.symbols['sStoragePortrait'],2))[0]
assert portrait<64
m.snap('storage-redesign-preview')
shellMask=np.zeros((160,240),dtype=bool)
shellMask[10:150,12:228]=True;shellMask[23:136,20:220]=False
shellBase=np.asarray(m.screen)[shellMask].copy()
# Selecting another occupied slot reuses the existing grid sprites and preview.
m.press(7,30)
assert icons()[:30]==ids and positions(ids)==xy
assert struct.unpack('<H',m.read(m.symbols['sStoragePortrait'],2))[0]==portrait
m.snap('storage-redesign-preview-charmander')
m.press(6,30);m.press(6,30);m.press(8,30)
assert m.read(m.symbols['sGlassStorage']+4,1)==b'\x01'
assert icons()[:30]==ids and positions(ids)==xy,'Opening Party moved or rebuilt the box'
assert all(i<64 for i in icons()),'Full box/party failed to allocate icons'
assert struct.unpack('<H',m.read(m.symbols['sStoragePortrait'],2))[0]==65535
m.snap('storage-redesign-party')
# Move to a lower-right occupied slot and exercise the carry overlay.
m.press(7,30);m.press(7,30)
for _ in range(5):m.press(7,30)
for _ in range(4):m.press(5,30)
assert m.read(m.symbols['sGlassStorage']+1,1)==b'\x1d'
m.press(8,30)
assert m.read(m.symbols['sGlassStorage']+5,1)==b'\x01'
m.snap('storage-redesign-carry')
assert np.array_equal(np.asarray(m.screen)[shellMask],shellBase),'Carried last-slot icon crossed bezel'
for _ in range(8):m.press(6,30)
assert m.read(m.symbols['sGlassStorage']+1,1)==b'\x24'
assert np.array_equal(np.asarray(m.screen)[shellMask],shellBase),'Carried icon over Party button crossed bezel'
m.snap('storage-redesign-carry-party-button')
m.press(0,30);m.press(0,30);m.press(0,60)
assert alive()==initial_count,'Storage leaked sprite ownership on exit'
# Repeated entry/exit must free the portrait, its palette and all grid icons.
for _ in range(10):
    call();m.press(7,15);m.press(6,15);m.press(0,60)
    assert alive()==initial_count
    assert struct.unpack('<H',m.read(m.symbols['sStoragePortrait'],2))[0]==65535
assert m.read(m.symbols['gPlayerParty'],600)==party,'Visual navigation changed party data'
print('Opaque display, fixed grid, reused icon/preview sprites, full party, carry overlay, 10 resource-clean exits passed')

# Returning through the real launcher must restore its palette and transparency.
m.press(3);m.press(8);m.press(7,30);m.press(7,30)
hub=np.asarray(m.screen).copy()
m.press(8)
shell=np.zeros((160,240),dtype=bool)
shell[10:150,12:228]=True;shell[23:136,20:220]=False
m.keys.add(0)
for frame in range(120):
    m.run(1)
    if frame==1:m.keys.clear()
    if not np.array_equal(np.asarray(m.screen)[shell],hub[shell]):m.snap('storage-redesign-exit-error')
    assert np.array_equal(np.asarray(m.screen)[shell],hub[shell]), ('Storage exit changed tablet shell',frame)
assert np.array_equal(np.asarray(m.screen)[23:136,20:220],hub[23:136,20:220]), 'Storage changed the hub palette/blending on return'
m.snap('storage-redesign-hub-return')
m.press(0)
print('Every exit frame keeps the tablet shell; return restores launcher palette and glass blending')
