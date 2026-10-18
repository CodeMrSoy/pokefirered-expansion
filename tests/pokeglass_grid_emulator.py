#!/usr/bin/env python3
"""Exercise the six-tile launcher through real directional and app inputs."""
import pathlib
import struct

setup = pathlib.Path(__file__).with_name('avatar_wardrobe_emulator.py')
exec(compile(setup.read_text().split("fixture = b'\\x23'")[0], str(setup), 'exec'))
native('FlagSet', 0x829)  # FLAG_SYS_POKEDEX_GET
fixture = b'\x23' + struct.pack('<I', (m.symbols['ScrCmd_createmon'] | 1) + 0x2000000)
fixture += struct.pack('<BBHHI', 0, 6, 1, 25, 0)
m.inject(fixture + b'\x44' + struct.pack('<HH', 717, 1) + b'\x02')
m.press(3)
m.press(8)
wait_task('Task_PokeGlassHub')

def cursor():
    return m.read(m.symbols['sHubCursor'], 1)[0]

def move(key, expected):
    m.press(key, 20)
    assert cursor() == expected, (key, cursor(), expected)

assert cursor() == 0
m.snap('pokeglass-six-app-grid')
# Both rows, all vertical pairs, and each clamped edge.
for key, expected in ((4, 0), (6, 0), (7, 1), (7, 2), (7, 2),
                      (5, 5), (5, 5), (6, 3), (4, 1), (5, 3),
                      (6, 4), (6, 4), (4, 0), (5, 4), (7, 3),
                      (7, 5), (4, 2), (6, 1), (6, 0)):
    move(key, expected)

# Preserve every existing script app ID despite moving the tiles.
for app, path, task in (
    (0, (), 'Task_PokeGlassPokedex'),
    (1, (7,), 'Task_HandleChooseMonInput'),
    (2, (7,), 'Task_GlassStorage'),
    (5, (5,), 'Task_PokeGlassWardrobe'),
    (3, (6,), 'Task_PokeGlassStats'),
    (4, (6,), None),
):
    for key in path:
        m.press(key, 20)
    assert cursor() == app
    m.press(8)
    assert not task_active('Task_PokeGlassHub'), ('App did not open', app)
    if task:
        wait_task(task)
    m.snap('pokeglass-grid-app-' + str(app))
    m.press(0)
    wait_task('Task_PokeGlassHub')
    assert cursor() == app
    m.snap('pokeglass-grid-return-' + str(app))
m.press(0)
assert not task_active('Task_PokeGlassHub')
assert m.read(m.symbols['sGlobalScriptContextStatus'], 1) == b'\x02'
print('Six-app grid navigation, launches, selected-app returns, and close passed')
