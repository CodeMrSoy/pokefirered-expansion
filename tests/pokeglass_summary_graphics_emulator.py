"""Check rendered Summary backgrounds, details, repeated flips and mon changes."""
import pathlib, struct
setup = pathlib.Path(__file__).with_name('avatar_wardrobe_emulator.py')
exec(compile(setup.read_text().split("fixture = b'\\x23'")[0], str(setup), 'exec'))
fixture = b''
for species in (1, 4, 7):
    fixture += b'\x23' + struct.pack('<I', (m.symbols['ScrCmd_createmon'] | 1) + 0x2000000)
    fixture += struct.pack('<BBHHI', 0, 6, species, 25, 0)
m.inject(fixture + b'\x29' + struct.pack('<H', 0x829) + b'\x44' + struct.pack('<HH', 717, 1) + b'\x02')
original = m.read(m.symbols['gPlayerParty'], 300)

def tilemap(name):
    offset = m.symbols[name] - 0x08000000
    data = m.rom[offset:]
    assert data[0] == 0x10
    size = int.from_bytes(data[1:4], 'little')
    out = bytearray(); pos = 4
    while len(out) < size:
        flags = data[pos]; pos += 1
        for bit in range(7, -1, -1):
            if len(out) >= size: break
            if flags & (1 << bit):
                a, b = data[pos:pos+2]; pos += 2
                count = (a >> 4) + 3; distance = ((a & 15) << 8 | b) + 1
                for _ in range(count): out.append(out[-distance])
            else:
                out.append(data[pos]); pos += 1
    return bytes(out)

expected = {0: tilemap('gSummaryScreen_PageInfo_Tilemap'),
            2: tilemap('gSummaryScreen_PageMoves_Tilemap')}

def page():
    summary = struct.unpack('<I', m.read(m.symbols['sMonSummaryScreen'], 4))[0]
    return m.read(summary + 0x32c4, 1)[0]

def graphics(wanted):
    assert page() == wanted, (page(), wanted)
    controls = {bg: struct.unpack('<H', m.read(m.symbols['sGpuRegBuffer'] + 8 + 2*bg, 2))[0] for bg in (1, 2)}
    bg = min(controls, key=lambda b: controls[b] & 3)
    base = 0x06000000 + ((controls[bg] >> 8) & 31) * 0x800
    actual = m.read(base, 0x800)
    # Header windows use the first four rows. The body must match the actual
    # destination artwork, including the region where stale stat labels leaked.
    for y in range(4, 17):
        for x in range(15, 30):
            offset = 2*(32*y+x)
            assert actual[offset:offset+2] == expected[wanted][offset:offset+2], ('Wrong page artwork', wanted, bg, x, y)

m.press(3); wait_task('Task_PokeGlassHub'); m.press(7, 30); m.press(8)
wait_task('Task_HandleChooseMonInput'); m.press(8); m.press(8)
wait_task('Task_InputHandler_Info'); m.run(90)
graphics(0)
for cycle in range(4):
    m.press(7, 120); graphics(2)
    m.snap('summary-clean-moves-' + str(cycle))
    m.press(8, 120); assert page() == 3
    m.press(5, 60); m.snap('summary-clean-details-' + str(cycle))
    m.press(0, 120); graphics(2)
    if cycle < 2:
        m.press(5, 120); graphics(2)
    m.press(6, 120); graphics(0)
m.press(0, 180)
if task_active('Task_HandleSelectionMenuInput'): m.press(0, 90)
wait_task('Task_HandleChooseMonInput'); m.press(0, 180)
wait_task('Task_PokeGlassHub'); m.press(0)
assert m.read(m.symbols['gPlayerParty'], 300) == original
assert m.read(m.symbols['sLockFieldControls'], 1) == b'\0'

# A caller can open Moves directly; its initial layer/parity must agree with
# the normal Info -> Moves path before any animation has run.
native('SetPokemonSummaryScreenStartPage', 2)
m.press(3); wait_task('Task_PokeGlassHub'); m.press(8)
wait_task('Task_HandleChooseMonInput'); m.press(8); m.press(8)
wait_task('Task_InputHandler_Info'); m.run(90); graphics(2)
m.snap('summary-clean-direct-moves')
m.press(6, 120); graphics(0)
m.press(7, 120); graphics(2)
m.press(8, 120); assert page() == 3
m.press(0, 120); graphics(2)
m.press(0, 180)
if task_active('Task_HandleSelectionMenuInput'): m.press(0, 90)
wait_task('Task_HandleChooseMonInput'); m.press(0, 180)
wait_task('Task_PokeGlassHub'); m.press(0)
assert m.read(m.symbols['gPlayerParty'], 300) == original
assert m.read(m.symbols['sLockFieldControls'], 1) == b'\0'
print('PASS actual Info/Moves artwork, repeated page/detail transitions, direct Moves entry, mon switching, unchanged party and field return', flush=True)
