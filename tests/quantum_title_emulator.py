#!/usr/bin/env python3
"""Check the Quantum title's meteor-form trio, formation, looping, and Start."""
import struct
import types
from pathlib import Path

harness = Path(__file__).with_name('quantum_qol_emulator.py')
m = types.ModuleType('title_harness')
m.__file__ = str(harness)
source = harness.read_text().split('run(360);press(3);press(8);snap(\'boot\')')[0]
exec(compile(source, str(harness), 'exec'), m.__dict__)
m.run(360)

def sprites(callback):
    expected = m.symbols[callback] | 1
    out = []
    for index in range(64):
        address = m.symbols['gSprites'] + index * 68
        data = m.read(address, 68)
        if data[62] & 1 and struct.unpack_from('<I', data, 28)[0] == expected:
            out.append((index, struct.unpack_from('<hh', data, 32), bool(data[62] & 4)))
    return out

m.snap('title-initial')
assert len(sprites('SpriteCB_QuantumMinior')) == 3
assert len(sprites('SpriteCB_QuantumTrail')) == 18
m.write(m.symbols['sMiniorFlightFrame'], struct.pack('<H', 0))
frames = []
previous = None
for frame in range(520):
    m.run(1)
    phase = struct.unpack('<H', m.read(m.symbols['sMiniorFlightFrame'], 2))[0]
    members = sprites('SpriteCB_QuantumMinior')
    assert len(members) == 3
    if phase < 400:
        leader = members[0][1]
        assert tuple(a-b for a,b in zip(members[1][1], leader)) == (-8, -40)
        assert tuple(a-b for a,b in zip(members[2][1], leader)) == (-42, -6)
        assert all(not member[2] for member in members)
        if previous is not None and phase > previous[0]:
            assert leader[0] >= previous[1][0] and leader[1] >= previous[1][1]
        previous = phase, leader
    else:
        assert all(member[2] for member in members)
        assert all(member[2] for member in sprites('SpriteCB_QuantumTrail'))
        previous = None
    if phase in (110, 210, 245, 410):
        m.snap('minior-v-' + str(phase))
    if frame % 3 == 0:
        frames.append(m.screen.resize((720,480),m.Image.Resampling.NEAREST))
frames[0].save(m.d/'minior-v-flight.gif', save_all=True, append_images=frames[1:], duration=50, loop=0)
m.press(3, 180)
assert not sprites('SpriteCB_QuantumMinior')
m.snap('minior-v-main-menu')
print('Three meteor Minior, 18 trails, diagonal V, synchronized pause/loop, and Start passed')
