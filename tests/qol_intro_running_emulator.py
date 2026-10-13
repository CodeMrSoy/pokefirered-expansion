#!/usr/bin/env python3
"""Check rival advice flags, the candy gift, and compiled running-frame mappings."""
import pathlib
import struct

setup = pathlib.Path(__file__).with_name('avatar_wardrobe_emulator.py')
exec(compile(setup.read_text().split("fixture = b'\\x23'")[0], str(setup), 'exec'))

# Verify the compiled frame table, including the source graphics offsets.
for name, image, order in (
    ('Brendan', 'running', [0, 3, 4, 1, 5, 6, 2, 7, 8]),
    ('May', 'running', [0, 3, 4, 1, 5, 6, 2, 7, 8]),
):
    frames = m.symbols['sAvatar' + name + 'NormalFrames']
    pixels = m.symbols['sAvatar' + name + '_' + image]
    for index, expected in enumerate(order, 9):
        pointer, size = struct.unpack('<IH', m.read(frames + index * 8, 6))
        assert pointer == pixels + expected * 256, (name, index, expected, hex(pointer))
        assert size == 256
print('Both Emerald running frame tables match directional animation order', flush=True)

native('FlagSet', 0x4e8)
m.inject(b'\x04' + struct.pack('<I', m.symbols['ViridianCity_Mart_EventScript_GiveCapCandy']) + b'\x02')
m.snap('qol-cap-candy-reason')
for _ in range(15):
    m.press(8, 45)
assert native('CheckBagHasItem', 830, 1) == 1
assert native('FlagGet', 0x4e8) == 0
assert native('RemoveBagItem', 830, 1) == 1
assert native('CheckBagHasItem', 830, 1) == 0
native('VarSet', 0x4057, 1)  # Parcel is awaiting delivery; no shop menu.
m.inject(b'\x05' + struct.pack('<I', m.symbols['ViridianCity_Mart_EventScript_Clerk']))
for _ in range(8):
    m.press(8, 45)
assert native('CheckBagHasItem', 830, 1) == 0, 'Clerk gave a duplicate gift'
print('Candy gift displays its reason, grants the item, and clears the pending flag', flush=True)

fixture = b'\x23' + struct.pack('<I', (m.symbols['ScrCmd_createmon'] | 1) + 0x2000000)
fixture += struct.pack('<BBHHI', 0, 6, 1, 5, 0) + b'\x02'
m.inject(fixture)
size = m.lib.retro_serialize_size()
state = c.create_string_buffer(size)
assert m.lib.retro_serialize(state, size)
for starter in ('Squirtle', 'Charmander', 'Bulbasaur'):
    assert m.lib.retro_unserialize(state, size)
    addr = m.symbols['PalletTown_ProfessorOaksLab_EventScript_RivalBattle' + starter]
    # The compiled macro must retain only the independent heal-after flag.
    assert struct.unpack('<H', m.read(addr + 40, 2))[0] == 1
    m.inject(b'\x05' + struct.pack('<I', addr))
    m.run(600)
    flags = struct.unpack('<I', m.read(m.symbols['gBattleTypeFlags'], 4))[0]
    assert flags & 8, (starter, flags)  # Trainer battle.
    assert not flags & 16, (starter, flags)  # No Oak coaching.
    m.snap('qol-regular-rival-' + starter.lower())
print('All three lab rival battles remain trainer battles without Oak tutorial flags', flush=True)
