"""Keep real field scenery through repeated Party/Stats/Dex/Map/Bag visits."""
import pathlib, struct
setup = pathlib.Path(__file__).with_name('avatar_wardrobe_emulator.py')
exec(compile(setup.read_text().split("fixture = b'\\x23'")[0], str(setup), 'exec'))
fixture = b'\x23' + struct.pack('<I', (m.symbols['ScrCmd_createmon'] | 1) + 0x2000000)
fixture += struct.pack('<BBHHI', 0, 6, 1, 25, 0)
m.inject(fixture + b'\x29' + struct.pack('<H', 0x829) + b'\x44' + struct.pack('<HH', 717, 1) + b'\x02')

def cache_pointer():
    return struct.unpack('<I', m.read(m.symbols['sFieldBackdrop'], 4))[0]

def cache():
    address = cache_pointer()
    assert address, 'Missing field snapshot'
    header = m.read(address - 16, 16)
    assert struct.unpack_from('<H', header, 2)[0] == 0xA3A3, 'Snapshot points into a reset heap'
    assert header[0] & 1, 'Snapshot allocation was freed'
    assert struct.unpack_from('<I', header, 4)[0] & 0x3FFFF >= 19200, 'Snapshot allocation was reused'
    for i in range(32):
        window = m.read(m.symbols['gWindows'] + i*12, 12)
        ptr = struct.unpack_from('<I', window, 8)[0]
        if window[0] != 255 and ptr:
            end = ptr + window[3]*window[4]*32
            assert end <= address or ptr >= address + 19200, ('Window reuses snapshot allocation', i)
    return m.read(address, 19200), m.read(m.symbols['sFieldBackdropPalette'], 32)

m.press(3); wait_task('Task_PokeGlassHub'); m.run(60)
initial = cache()
for cycle in range(3):
    for app, ready in ((1, 'Task_HandleChooseMonInput'), (3, 'Task_PokeGlassStats'),
                       (0, 'Task_PokeGlassPokedex'), (4, 'Task_RegionMap'),
                       (5, 'Task_BagMenu_HandleInput')):
        before = cache()
        m.write(m.symbols['sHubCursor'], bytes([app]))
        m.press(8, 180); wait_task(ready); m.run(60)
        assert cache() == before, ('UI contaminated the field snapshot', cycle, app)
        if app == 5:
            assert m.read(0x06008000, 19200) == before[0], 'Bag scenery differs from clean snapshot'
            m.snap('bag-frozen-scenery-cycle-' + str(cycle))
        for _ in range(8):
            if task_active('Task_PokeGlassHub'): break
            m.press(0, 120)
        wait_task('Task_PokeGlassHub'); m.run(60)
        after = cache()
        if app in (0, 3):
            assert after == before, ('Embedded app changed the field snapshot', cycle, app)
    print('PASS stable scenery through complete app cycle', cycle + 1, flush=True)

m.press(0, 180)
assert not cache_pointer(), 'Closing the tablet retained its snapshot allocation'
assert m.read(m.symbols['sLockFieldControls'], 1) == b'\0'
# Start a new session in a different real map: retaining the old snapshot must
# not prevent the next session from capturing the current field.
m.inject(b'\x39' + struct.pack('<BBBHH', 3, 1, 255, 30, 24) + b'\x6b\x02')
m.run(180); m.press(3); wait_task('Task_PokeGlassHub'); m.run(60)
assert cache() != initial, 'New tablet session reused the old map scenery'
m.snap('bag-new-session-new-scenery')
m.press(0, 180)
assert not cache_pointer()
print('PASS snapshot preserved across fifteen app visits, freed on close, refreshed on the next map/session', flush=True)
