#!/usr/bin/env python3
"""Read-only Stats app checks; uses the QOL harness's mGBA core and ROM/ELF."""
import re
import struct
import quantum_qol_emulator as m

fixture = b''
for species, level in ((1, 25), (25, 50), (143, 75)):
    fixture += b'\x23' + struct.pack('<I', (m.symbols['ScrCmd_createmon'] | 1) + 0x2000000)
    fixture += struct.pack('<BBHHI', 0, 6, species, level, 0)
m.inject(fixture + b'\x44' + struct.pack('<HH', 717, 1) + b'\x02')
assert m.read(m.symbols['gPlayerPartyCount'], 1) == b'\x03'

# Distinct EV/IV values expose swapped Speed/Sp. Atk/Sp. Def columns visually.
orders = {int(n): tuple(map(int, v)) for n, *v in re.findall(
    r'SUBSTRUCT_CASE\(\s*(\d+),(\d+),(\d+),(\d+),(\d+)\)',
    (m.root / 'src/pokemon.c').read_text())}
def set_fixture_values(slot, egg=False):
    address = m.symbols['gPlayerParty'] + slot * 100
    mon = bytearray(m.read(address, 100))
    pid, otid = struct.unpack_from('<II', mon)
    words = struct.unpack_from('<12I', mon, 32)
    data = bytearray(struct.pack('<12I', *(v ^ pid ^ otid for v in words)))
    order = orders[pid % 24]
    data[order[2]*12:order[2]*12+6] = bytes((252, 128, 0, 4, 96, 30))
    offset = order[3]*12+4
    old = struct.unpack_from('<I', data, offset)[0]
    ivs = sum(v << (5*i) for i, v in enumerate((31, 0, 15, 7, 23, 29)))
    struct.pack_into('<I', data, offset, (old & 0x80000000) | ivs | (int(egg) << 30))
    if egg:
        mon[19] |= 4
    struct.pack_into('<H', mon, 28, sum(struct.unpack('<24H', data)) & 0xffff)
    encrypted = struct.pack('<12I', *(v ^ pid ^ otid for v in struct.unpack('<12I', data)))
    mon[32:80] = encrypted
    m.write(address, bytes(mon))
set_fixture_values(0)
set_fixture_values(2, egg=True)
original = m.read(m.symbols['gPlayerParty'], 300)

m.press(3); m.press(8); m.press(5); m.press(5); m.press(8)
def slot(): return m.read(m.symbols['sStatsPartySlot'], 1)[0]
def pic_count():
    return sum(m.read(m.symbols['sSpritePics'] + i*12 + 11, 1)[0] for i in range(8))
assert slot() == 0
assert pic_count() == 1
m.snap('stats-values')
m.press(7, 20); assert slot() == 1; m.snap('stats-second')
m.press(7, 20); assert slot() == 2; m.snap('stats-egg')
m.press(7, 20); assert slot() == 0
m.press(6, 20); assert slot() == 2
for switch in range(36):
    m.press(7, 20)
    assert pic_count() == 1, (switch, slot())
    assert struct.unpack('<H', m.read(m.symbols['sStatsMonSprite'], 2))[0] < 64
assert m.read(m.symbols['gPlayerParty'], 300) == original
m.press(0)
assert pic_count() == 0
assert m.read(m.symbols['sStatsMonSprite'], 2) == b'\xff\xff'
m.snap('stats-return-hub')
# Reopening and closing releases the portrait and resumes the field script.
for _ in range(8):
    m.press(8, 20); assert pic_count() == 1
    m.press(0, 20); assert pic_count() == 0
m.press(0)
assert m.read(m.symbols['sGlobalScriptContextStatus'], 1) == b'\x02'
assert m.read(m.symbols['gPlayerParty'], 300) == original
print('Stats values, eggs, party wrap, repeated portrait cleanup, and hub/field return passed')
