#!/usr/bin/env python3
"""Shared shell opacity, party VRAM safety, and real app transition checks."""
import struct
import numpy as np
import quantum_qol_emulator as m

fixture = b''
for species in (1, 4, 7, 25, 133, 143):
    fixture += b'\x23' + struct.pack('<I', (m.symbols['ScrCmd_createmon'] | 1) + 0x2000000)
    fixture += struct.pack('<BBHHI', 0, 6, species, 25, 0)
m.inject(fixture + b'\x44' + struct.pack('<HH', 717, 1) + b'\x02')

def reg(offset):
    return struct.unpack('<H', m.read(m.symbols['sGpuRegBuffer'] + offset, 2))[0]

def shell_image():
    return np.asarray(m.screen).copy()

def assert_glass_window():
    assert reg(0x42) == (20 << 8) | 220
    assert reg(0x46) == (23 << 8) | 136
    assert reg(0) & 0xe000 == 0x4000
    assert reg(0x48) & 0x2000  # Blend inside WIN1.
    assert not reg(0x4a) & 0x2020  # Opaque outside the glass.

m.press(3)
assert_glass_window()
hub = shell_image()
assert tuple(hub[18,13]) == (255, 40, 57), 'Red grip is blended with the map'
assert tuple(hub[14,100]) == (230, 234, 246), 'Ivory shell is blended with the map'
m.snap('opaque-tablet-hub')
# Exclude rounded outer corners and the glass. All shell pixels must match.
shell = np.zeros((160, 240), dtype=bool)
shell[10:150, 12:228] = True
shell[23:136, 20:220] = False

m.press(7, 20)
m.keys.add(8)
frames = []
for frame in range(150):
    m.run(1)
    if frame == 1:
        m.keys.clear()
    frames.append(m.screen.resize((720, 480), m.Image.Resampling.NEAREST))
frames[0].save(m.d / 'tablet-party-transition.gif', save_all=True,
               append_images=frames[1:], duration=17, loop=0)
assert_glass_window()
party = shell_image()
m.snap('opaque-tablet-party')
assert np.array_equal(hub[shell], party[shell]), 'Party shell differs from the hub'
reserved = m.read(0x06007000, 0x1000)
# Open actions, then cancel, navigate all rows and select the Cancel button.
m.press(8, 20)
m.snap('opaque-tablet-party-actions')
assert m.read(0x06007000, 0x1000) == reserved, 'Actions overwrote the shell'
m.press(0, 20)
for key in (7, 5, 5, 5, 4, 6, 4, 4):
    m.press(key, 20)
    assert m.read(0x06007000, 0x1000) == reserved, 'Navigation overwrote the shell'
m.snap('opaque-tablet-party-navigation')
m.press(8)
m.press(8)
m.press(0)
assert_glass_window()
assert m.read(0x06007000, 0x1000) == reserved, 'Summary return changed the shell'
m.snap('opaque-tablet-party-summary-return')
m.press(0)  # Summary returns to the selected Pokémon's actions.
m.press(0)
returned = shell_image()
assert np.array_equal(hub[shell], returned[shell]), 'Return changed shell colors'
# Open the Stats dock from Party, then return, checking saved field registers.
m.press(5, 20)
m.press(5, 20)
m.press(8)
assert_glass_window()
stats = shell_image()
assert np.array_equal(hub[shell], stats[shell]), 'Stats shell differs from the hub'
m.snap('opaque-tablet-stats')
m.press(0)
m.press(0)
assert reg(0) & 0xe000 == 0x6000
assert reg(0x42) == 0xffff and reg(0x46) == 0xffff
assert m.read(m.symbols['sGlobalScriptContextStatus'], 1) == b'\x02'
print('Opaque shared hub/party/Stats shell, action/navigation VRAM, return, and field register restoration passed')
