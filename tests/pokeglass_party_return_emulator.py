#!/usr/bin/env python3
"""Check every exit frame, repeated app visits, and field controls after closing."""
import struct
import numpy as np
import quantum_qol_emulator as m

fixture = b''
for species in (1, 4, 7, 25, 133, 143):
    fixture += b'\x23' + struct.pack('<I', (m.symbols['ScrCmd_createmon'] | 1) + 0x2000000)
    fixture += struct.pack('<BBHHI', 0, 6, species, 25, 0)
m.inject(fixture + b'\x44' + struct.pack('<HH', 717, 1) + b'\x02')
size = m.lib.retro_serialize_size()
field = m.c.create_string_buffer(size)
assert m.lib.retro_serialize(field, size)
mask = np.zeros((160, 240), dtype=bool)
mask[10:150, 12:228] = True
mask[23:136, 20:220] = False

def callback():
    return struct.unpack('<I', m.read(m.symbols['gMain'] + 4, 4))[0]

def flag(name):
    return bool(m.read(m.symbols[name], 1)[0])

for name, count, warp in [('bedroom-one', 1, None), ('bedroom-six', 6, None),
                          ('viridian', 6, (3, 1, 30, 24)),
                          ('cerulean', 6, (3, 3, 25, 22))]:
    assert m.lib.retro_unserialize(field, size)
    if count == 1:
        m.write(m.symbols['gPlayerParty'] + 100, b'\0' * 500)
        m.write(m.symbols['gPlayerPartyCount'], b'\x01')
    if warp:
        group, num, x, y = warp
        m.inject(b'\x39' + struct.pack('<BBBHH', group, num, 255, x, y) + b'\x6b\x02')
        m.run(300)
    m.write(m.symbols['sHubCursor'], b'\x00')
    m.press(3)
    m.press(8)
    m.press(7, 60)
    for cycle in range(3):
        m.press(8, 180)
        assert callback() == (m.symbols['CB2_UpdatePartyMenu'] | 1), (name, cycle, 'Party not ready')
        base = np.asarray(m.screen).copy()
        frames, cover, cover_frames, released = [], None, 0, False
        m.keys.add(0)
        for frame in range(240):
            m.run(1)
            if frame == 1:
                m.keys.clear()
            current = np.asarray(m.screen).copy()
            assert np.array_equal(current[mask], base[mask]), (name, cycle, frame, 'Bezel changed')
            assert len(np.unique(current.reshape(-1, 3), axis=0)) > 8, (name, cycle, frame, 'Blank frame')
            if flag('sReturnCoverActive'):
                cover_frames += 1
                if cover is None:
                    cover = current
                assert np.array_equal(current, cover), (name, cycle, frame, 'Cover flickered')
            elif cover is not None:
                released = True
            if cycle == 0 and frame < 130:
                frames.append(m.screen.resize((480, 320), m.Image.Resampling.NEAREST))
        assert 5 < cover_frames < 200 and released, (name, cycle, cover_frames, released)
        assert callback() == (m.symbols['CB2_Overworld'] | 1)
        assert flag('sTabletActive') and not flag('sTabletNative')
        assert m.read(m.symbols['gPlayerPartyCount'], 1) == bytes([count])
        if frames:
            frames[0].save(m.d / ('party-return-' + name + '.gif'), save_all=True,
                           append_images=frames[1:], duration=17, loop=0)
        print(name, 'cycle', cycle + 1, 'stable cover frames', cover_frames, flush=True)
    m.press(0, 180)
    assert not flag('sTabletActive') and not flag('sReturnCoverActive')
    m.press(3, 60)
    assert callback() == (m.symbols['CB2_Overworld'] | 1), (name, 'Field controls lost')
    m.press(0, 60)
print('Every exit frame, 12 repeated returns, Party counts and closing to field passed')
