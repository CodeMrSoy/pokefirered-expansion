"""Initial tablet animation, first-open map viewport and real region round trips."""
import pathlib
import struct
import numpy as np

setup = pathlib.Path(__file__).with_name('avatar_wardrobe_emulator.py')
exec(compile(setup.read_text().split("fixture = b'\\x23'")[0], str(setup), 'exec'))
m.d = m.d / 'map-transitions'
m.d.mkdir(exist_ok=True)
native('FlagSet', 0x4e1)
m.inject(b'\x29' + struct.pack('<H', 0x829) + b'\x44' + struct.pack('<HH', 717, 1) + b'\x02')


def ptr(name):
    return struct.unpack('<I', m.read(m.symbols[name], 4))[0]


def reg(offset):
    return struct.unpack('<H', m.read(m.symbols['sGpuRegBuffer'] + offset, 2))[0]


def viewport():
    assert reg(0) & 0xe000 == 0x4000, ('Incorrect map window enables', hex(reg(0)))
    assert reg(0x42) == 0x0ae6, ('Incorrect viewport width', hex(reg(0x42)))
    assert reg(0x46) == 0x0a96, ('Incorrect viewport height', hex(reg(0x46)))
    assert reg(0x48) == 0x1f00 and reg(0x4a) == 2, ('Viewport layers', hex(reg(0x48)), hex(reg(0x4a)))
    assert reg(0x50) == 0, 'Native name-box darkening leaked into tablet'
    assert m.read(m.symbols['sNativeTransitionStage'], 1) == b'\0'


matrices = m.read(m.symbols['gOamMatrixAllocBitmap'], 4)
frames = []
intro_frames = 0
m.keys.add(3)
for frame in range(180):
    m.run(1)
    if frame == 1:
        m.keys.clear()
    frames.append(m.screen.copy())
    intro_frames += int(task_active('Task_PokeGlassIntro'))
    if task_active('Task_PokeGlassHub'):
        break
else:
    raise AssertionError('Tablet failed to reach launcher')
assert 30 <= intro_frames <= 40, ('Tablet icon animation duration', intro_frames)
assert m.read(m.symbols['gOamMatrixAllocBitmap'], 4) == matrices, 'Intro leaked an affine matrix'
frames[0].save(m.d / 'tablet-startup.gif', save_all=True, append_images=frames[1:], duration=17, loop=0)
m.run(30)
print('PASS tablet icon animation:', intro_frames, 'frames; launcher reached and affine matrix freed', flush=True)

type_offset = 19 * 2 + 5 * 600 * 2 + 3 * 0x800 * 2


def region():
    return m.read(ptr('sRegionMap') + type_offset + 5, 1)[0]


def move_to(x, y):
    for _ in range(65):
        cx, cy = struct.unpack('<hh', m.read(ptr('sMapCursor'), 4))
        if (cx, cy) == (x, y):
            viewport()
            return
        m.press(7 if cx < x else 6 if cx > x else 5 if cy < y else 4, 18)
        viewport()
    raise AssertionError(('Map cursor did not arrive', x, y))


m.press(5, 20)
m.press(8)
wait_task('Task_RegionMap')
m.run(60)
viewport()
assert region() == 0
original_map = m.read(0x600f000, 0x800)
original_tiles = m.read(0x6000000, 0x4000)
shell = np.zeros((160, 240), bool)
shell[:8, 8:232] = True
shell[152:, 8:232] = True
shell[8:152, :8] = True
shell[8:152, 232:] = True
bezel = np.asarray(m.screen)[shell].copy()
m.snap('map-first-open')
if m.read(ptr('sRegionMap') + type_offset + 1, 1) == b'\x01':
    for destination in (2, 0, 2, 0):
        move_to(21, 11)
        m.press(8, 180)
        assert ptr('sSwitchMapMenu') != 0
        m.press(5 if destination == 2 else 4, 30)
        m.press(8, 180)
        assert ptr('sSwitchMapMenu') == 0 and region() == destination
        viewport()
        assert np.array_equal(np.asarray(m.screen)[shell], bezel), 'Region switch changed bezel'
        if destination == 0:
            assert m.read(0x600f000, 0x800) == original_map, 'First Kanto map differs from returned page'
            assert m.read(0x6000000, 0x4000) == original_tiles, 'Region switch changed atlas graphics'
        m.snap('map-page-' + str(destination))
    print('PASS actual Kanto/Vidra page switches: initial/returned atlas identical and viewport stable', flush=True)
else:
    print('SKIP region switches: this snapshot has only Kanto', flush=True)
for cycle in range(3):
    move_to(4, 11)
    m.press(0)
    wait_task('Task_PokeGlassHub')
    m.run(30)
    assert m.read(m.symbols['sNativeTransitionStage'], 1) == b'\0'
    m.press(8)
    wait_task('Task_RegionMap')
    m.run(60)
    viewport()
    assert m.read(0x600f000, 0x800) == original_map
    assert np.array_equal(np.asarray(m.screen)[shell], bezel)
m.snap('map-reopened')
m.press(0)
wait_task('Task_PokeGlassHub')
m.press(0)
assert ptr('sRegionMap') == 0 and ptr('sMapCursor') == 0
assert m.read(m.symbols['sLockFieldControls'], 1) == b'\0'
print('PASS first-open map, movement, page round trips, three reopenings, viewport/bezel stability and cleanup', flush=True)
