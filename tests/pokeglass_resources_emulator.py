#!/usr/bin/env python3
"""Ensure repeated real app visits release their session and portrait allocations."""
import pathlib
setup = pathlib.Path(__file__).with_name('pokeglass_benchmark_emulator.py')
exec(compile(setup.read_text().split('field=save()')[0], str(setup), 'exec'))

def heap_state():
    head = struct.unpack('<I', m.read(m.symbols['sHeapStart'], 4))[0]
    address = head
    blocks = []
    while True:
        flags, size, previous, following = struct.unpack('<4I', m.read(address, 16))
        assert flags >> 16 == 0xA3A3, ('Corrupt heap header', hex(address))
        size &= (1 << 18) - 1
        blocks.append((bool(flags & 1), size))
        assert len(blocks) < 1024, 'Heap list did not terminate'
        address = following
        if address == head:
            break
    return sum(size for allocated, size in blocks if allocated), sum(allocated for allocated, size in blocks)

def cycle():
    m.press(3, 100)
    assert hub()
    # Dex, Party and Stats allocate the largest embedded app resources.
    for app, path, taskname in ((0, [], 'Task_PokeGlassPokedex'),
            (1, [7], 'Task_HandleChooseMonInput'),
            (2, [7], 'Task_PokeGlassStorage'),
            (3, [5, 6], 'Task_PokeGlassStats')):
        for key in path:
            m.press(key, 30)
        assert byte('sHubCursor') == app
        before = heap_state()
        m.press(8, 100)
        assert ready(taskname), taskname
        if app == 2:
            assert struct.unpack('<I',m.read(m.symbols['sGlassStorageIcons'],4))[0] != 0
        m.press(0, 100)
        assert hub()
        if app == 2:
            assert heap_state() == before, ('Storage retained its sprite view',before,heap_state())
            assert m.read(m.symbols['sGlassStorageIcons'],4) == bytes(4)
    # Restore the remembered launcher cursor for the next real session.
    m.press(4, 30)
    m.press(6, 30)
    assert byte('sHubCursor') == 0
    m.press(6,30);m.press(6,30)
    assert byte('sHubCursor') == 9
    before = heap_state()
    m.press(8,100);assert ready('Task_PokeGlassFieldKit')
    m.press(5,30);m.press(0,100);assert hub()
    assert heap_state() == before, ('Field Kit retained resources',before,heap_state())
    m.press(5,30);assert byte('sHubCursor') == 12
    m.press(8,180);assert ready('Task_HandleListInput')
    m.press(0,180);assert hub();m.press(4,30);assert byte('sHubCursor') == 9
    m.press(7,30);m.press(7,30);assert byte('sHubCursor') == 0
    m.press(5,30);m.press(7,30);m.press(7,30);assert byte('sHubCursor') == 5
    m.press(8,180);assert ready('Task_BagMenu_HandleInput')
    m.press(7,90);m.press(6,90);m.press(0,180);assert hub()
    m.press(4,30);m.press(6,30);m.press(6,30);assert byte('sHubCursor') == 0
    m.press(0, 100)
    assert byte('sGlobalScriptContextStatus') == 2
    assert not byte('sLockFieldControls')
    assert struct.unpack('<I', m.read(m.symbols['sFieldBackdrop'], 4))[0] == 0
    return heap_state()

baseline = cycle()
for iteration in range(8):
    current = cycle()
    print('HEAP', iteration, current, flush=True)
    assert current == baseline, ('Heap grew after app visit', baseline, current)
print('PASS eight repeated sessions: no retained backdrop, heap growth, or field lock', flush=True)
