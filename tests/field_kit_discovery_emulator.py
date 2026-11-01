"""Check all seven tool previews and badge-gated labels in both case UIs."""
import pathlib
import struct

setup = pathlib.Path(__file__).with_name('avatar_wardrobe_emulator.py')
exec(compile(setup.read_text().split("fixture = b'\\x23'")[0], str(setup), 'exec'))
m.d = m.d / 'field-kit-discovery'
m.d.mkdir(exist_ok=True)
native('FlagSet', 0x829)
native('AddBagItem', 717, 1)
native('AddBagItem', 831, 1)  # Field Item Case.
baseline_size = m.lib.retro_serialize_size()
baseline = m.c.create_string_buffer(baseline_size)
assert m.lib.retro_serialize(baseline, baseline_size)
textures = {}


def task(name):
    for i in range(16):
        address = m.symbols['gTasks'] + i * 40
        if m.read(address + 4, 1) != b'\0' and struct.unpack('<I', m.read(address, 4))[0] == m.symbols[name] | 1:
            return address
    raise AssertionError(name)


def label_colors(window, glass, ready):
    w = m.read(m.symbols['gWindows'] + window * 12, 12)
    data = m.read(struct.unpack_from('<I', w, 8)[0], w[3] * w[4] * 32)
    expected = (8 if ready else 12) if glass else (2 if ready else 3)
    other = (12 if ready else 8) if glass else (3 if ready else 2)
    for move in range(7):
        colors = []
        for y in range((31 if glass else 24) + move * 12, (31 if glass else 24) + move * 12 + 12):
            for x in range(88 if glass else 91, 207 if glass else 220):
                colors.append(data[(y // 8 * w[3] + x // 8) * 32 + y % 8 * 4 + x % 8 // 2] >> ((x & 1) * 4) & 15)
        assert expected in colors, ('Missing name color', glass, ready, move)
        # The native enabled font uses the disabled foreground as its shadow.
        if glass or not ready:
            assert other not in colors, ('Wrong name color', glass, ready, move)


for owned, badge in ((False, False), (False, True), (True, False), (True, True)):
    assert m.lib.retro_unserialize(baseline, baseline_size)
    fixture = b''
    for i in range(7):
        fixture += (b'\x29' if owned else b'\x2a') + struct.pack('<H', 0x4a7 + i)
        fixture += (b'\x29' if badge else b'\x2a') + struct.pack('<H', 0x820 + i)
    m.inject(fixture + b'\x02')
    for glass in (False, True):
        if glass:
            m.press(3)
            wait_task('Task_PokeGlassHub')
            for _ in range(15):
                if m.read(m.symbols['sHubCursor'], 1) == b'\x09':
                    break
                m.press(7, 20)
            assert m.read(m.symbols['sHubCursor'], 1) == b'\x09'
            m.press(8)
            wait_task('Task_PokeGlassFieldKit')
        else:
            native('FieldItemCase_OpenUI')
            wait_task('Task_FieldItemCase')
        m.run(30)
        window = m.read(m.symbols['sHubWindow'] if glass else m.symbols['sCaseWindow'], 1)[0]
        label_colors(window, glass, badge)
        for move in range(7):
            sprite = (struct.unpack('<h', m.read(task('Task_PokeGlassFieldKit') + 14, 2))[0]
                      if glass else m.read(m.symbols['sCasePreview'], 1)[0])
            assert sprite < 64
            oam = m.read(m.symbols['gSprites'] + sprite * 68, 8)
            attr2 = struct.unpack_from('<H', oam, 4)[0]
            palette = 256 + (attr2 >> 12) * 16
            for buffer in ('gPlttBufferUnfaded', 'gPlttBufferFaded'):
                colors = m.read(m.symbols[buffer] + palette * 2, 32)
                assert (colors != bytes(32)) == owned, ('Incorrect silhouette', glass, owned, badge, move, buffer)
            texture = m.read(0x6010000 + (attr2 & 1023) * 32, 2048)
            if move in textures:
                assert textures[move] == texture, 'Silhouette altered tool shape/transparency'
            textures[move] = texture
            if move == 0:
                m.snap(f'{"glass" if glass else "case"}-found-{int(owned)}-badge-{int(badge)}')
            if move < 6:
                m.press(5, 20)
        # Badge-locked A must keep the player in the case.
        if not (owned and badge):
            m.press(8, 30)
            assert task_active('Task_PokeGlassFieldKit' if glass else 'Task_FieldItemCase')
            label_colors(window, glass, badge)
        m.press(0)
        if glass:
            wait_task('Task_PokeGlassHub')
            m.press(0)
        else:
            wait_task('Task_BagMenu_HandleInput')
            m.press(0)
        m.run(90)
    print('PASS all seven tools, both case UIs:', 'found' if owned else 'missing', 'badge' if badge else 'no badge', flush=True)
print('PASS black silhouettes preserve art/transparency; discovery restores color; badges unlock name colors independently; locked use stays blocked', flush=True)
