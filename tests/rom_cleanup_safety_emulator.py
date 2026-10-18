#!/usr/bin/env python3
"""Exercise release safety on encrypted Pokemon using the release ROM code."""
import pathlib
import struct
setup = pathlib.Path(__file__).with_name('avatar_wardrobe_emulator.py')
exec(compile(setup.read_text().split("fixture = b'\\x23'")[0], str(setup), 'exec'))
fixture = b''
for species in (1, 4, 7):
    fixture += b'\x23' + struct.pack('<I', (m.symbols['ScrCmd_createmon'] | 1) + 0x2000000)
    fixture += struct.pack('<BBHHI', 0, 6, species, 25, 0)
m.inject(fixture + b'\x02')
party = m.symbols['gPlayerParty']
box = struct.unpack('<I', m.read(m.symbols['gPokemonStoragePtr'], 4))[0] + 4
original = m.read(party, 600)
def reset():
    m.write(party, original)
    m.write(m.symbols['gPlayerPartyCount'], b'\x03')
    m.write(box, b'\0' * (14 * 30 * 80))
    m.write(m.symbols['sGlassStorage'], b'\0\x1e')  # box 0, party slot 0

def setdata(field, value):
    scratch = m.symbols['gDecompressionBuffer'] + 0x2f00
    m.write(scratch, struct.pack('<I', value))
    native('SetMonData', party, field, scratch)

def release():
    cursor=m.read(m.symbols['sGlassStorage']+1,1)
    m.inject(b'\x23' + struct.pack('<I', (m.symbols['ShowPokeGlassStorage'] | 1) + 0x2000000) + b'\x27\x02')
    m.write(m.symbols['sGlassStorage']+1,cursor)
    m.press(2,30); m.press(8,30); m.press(7,30); m.press(8,30)
    assert m.read(m.symbols['sGlassStorage']+44,1)==b'\x04'
    m.press(8,30); m.press(0,60); m.press(0,60)
reset()
# MON_DATA_IS_EGG is derived from the public enum rather than a stale offset.
enums = (m.root/'include/pokemon.h').read_text().split('enum {',1)[1].split('};',1)[0]
fields = [line.strip().rstrip(',') for line in enums.splitlines() if line.strip().startswith('MON_DATA_')]
setdata(fields.index('MON_DATA_IS_EGG'), 1)
before=m.read(party,600); release(); assert m.read(party,600)==before, 'Released an Egg'
reset(); native('SetMonMoveSlot', party, 57, 0) # Surf
before=m.read(party,600); release(); assert m.read(party,600)==before, 'Released the only Surf user'
# An alternative user in another box makes release safe.
m.write(box + 29*80, m.read(party,80))
release(); assert m.read(m.symbols['gPlayerPartyCount'],1)==b'\x02'
assert native('GetMonData3',party,18,0)==4
assert native('GetBoxMonData3',box+29*80,20,0)==57
# Eggs elsewhere cannot count as a replacement field-move user.
reset(); native('SetMonMoveSlot',party,57,0)
setdata(fields.index('MON_DATA_IS_EGG'),1); m.write(box,m.read(party,80))
setdata(fields.index('MON_DATA_IS_EGG'),0)
before=m.read(party,600); release(); assert m.read(party,600)==before
# Releasing a held-item Pokemon returns exactly one item, once.
reset(); setdata(19,520) # Oran Berry
before=native('CountTotalItemQuantityInBag',520)
release(); assert native('CountTotalItemQuantityInBag',520)==before+1
assert native('GetMonData3',party,18,0)==4
# Empty boxed slot is a harmless no-op.
m.write(m.symbols['sGlassStorage']+1,b'\x00')
before=m.read(party,600); release(); assert m.read(party,600)==before
assert native('CountTotalItemQuantityInBag',520)==1
print('Egg, sole Surf user, boxed replacement, Egg replacement, held item conservation, empty slot passed')
