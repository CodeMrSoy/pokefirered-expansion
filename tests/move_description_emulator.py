#!/usr/bin/env python3
"""Render formerly clipped Summary descriptions and the battle popup in mGBA."""
import pathlib
import struct
setup = pathlib.Path(__file__).with_name('avatar_wardrobe_emulator.py')
exec(compile(setup.read_text().split("fixture = b'\\x23'")[0], str(setup), 'exec'))
fixture = b'\x23' + struct.pack('<I', (m.symbols['ScrCmd_createmon'] | 1) + 0x2000000)
fixture += struct.pack('<BBHHI', 0, 6, 1, 50, 0)
m.inject(fixture + b'\x02')
size = m.lib.retro_serialize_size()
field = c.create_string_buffer(size)
assert m.lib.retro_serialize(field, size)
moves = [50, 139, 161, 178, 253, 294, 63, 344, 416, 439, 751, 2]
for batch in range(3):
    assert m.lib.retro_unserialize(field, size)
    selected = moves[batch * 4:batch * 4 + 4]
    script = b''.join(b'\x7a' + struct.pack('<BBH', 0, slot, move) for slot, move in enumerate(selected))
    m.inject(script + b'\x02')
    m.press(3);wait_task('Task_PokeGlassHub');m.press(7);m.press(8)
    wait_task('Task_HandleChooseMonInput');m.press(8);m.press(8)
    wait_task('Task_InputHandler_Info');m.run(90)
    m.press(7);m.press(7);m.press(8)
    wait_task('Task_HandleInput_SelectMove');m.run(30)
    for slot, move in enumerate(selected):
        assert m.read(m.symbols['sMoveSelectionCursorPos'],1) == bytes([slot])
        m.snap(f'move-description-summary-{move}')
        if slot < 3:m.press(5)

assert m.lib.retro_unserialize(field, size)
# Karate Chop's four-line description exercises the popup's maximum height.
m.inject(b'\x7a' + struct.pack('<BBH',0,0,2) + b'\x02')
battle = b'\xb6' + struct.pack('<HBHHBH', 92, 5, 0, 0, 0, 0) + b'\xb7\x6b\x02'
m.inject(battle)
def wait_controller(name):
    expected = m.symbols[name] | 1
    for _ in range(1500):
        if expected in struct.unpack('<4I',m.read(m.symbols['gBattlerControllerFuncs'],16)):return
        m.run(1)
    raise AssertionError('Did not reach ' + name)
for _ in range(30):
    controllers = struct.unpack('<4I',m.read(m.symbols['gBattlerControllerFuncs'],16))
    if (m.symbols['HandleInputChooseAction'] | 1) in controllers:
        m.press(8);break
    if (m.symbols['HandleInputChooseMove'] | 1) in controllers:break
    m.press(8,60)
wait_controller('HandleInputChooseMove');m.run(30)
move_panel = m.screen.crop((0,112,240,160)).tobytes()
m.press(10)
m.snap('move-description-battle-four-lines')
# The enlarged popup must clear and return to move selection normally.
m.press(0);wait_controller('HandleInputChooseMove')
m.snap('move-description-battle-closed')
assert m.screen.crop((0,112,240,160)).tobytes() == move_panel, 'Description damaged the move selection panel'
print('PASS twelve Summary renders, four-line battle popup, and closing to move selection',flush=True)
