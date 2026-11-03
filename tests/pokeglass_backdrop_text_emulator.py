"""Text on a shared field BG must not be captured into the glass scenery."""
import pathlib, struct
setup = pathlib.Path(__file__).with_name('avatar_wardrobe_emulator.py')
exec(compile(setup.read_text().split("fixture = b'\\x23'")[0], str(setup), 'exec'))

# Give a spare BG its own transparent map/characters, then add high-contrast
# window glyphs. Both captures start from the same core snapshot, so animation,
# palette selection, sprite frames and allocation state are identical.
native('SetGpuReg', 0x0A, (26 << 8) | (2 << 2))
native('SetGpuReg', 0x14, 0)
native('SetGpuReg', 0x16, 0)
native('SetGpuReg', 0, native('GetGpuReg', 0) | 0x200)
m.write(0x06008000, bytes(32) + bytes([0x12, 0x21, 0x12, 0x21] * 8))
blank = struct.pack('<1024H', *([0xF000] * 1024))
m.write(0x0600D000, blank)
colors = struct.pack('<16H', 0, 0x7FFF, 0x7C1F, *([0] * 13))
for name in ('gPlttBufferFaded', 'gPlttBufferUnfaded'):
    m.write(m.symbols[name] + 15 * 32, colors)
size = m.lib.retro_serialize_size()
state = c.create_string_buffer(size)
assert m.lib.retro_serialize(state, size)

def capture():
    native('CapturePokeGlassBackdrop')
    address = struct.unpack('<I', m.read(m.symbols['sFieldBackdrop'], 4))[0]
    assert address
    return m.read(address, 19200), m.read(m.symbols['sFieldBackdropPalette'], 32)

clean = capture()
assert m.lib.retro_unserialize(state, size)
overlay = bytearray(blank)
# The field camera continues updating BG scroll registers. Place the glyphs
# in the viewport rather than assuming tilemap row zero is on screen.
scroll_x, scroll_y = struct.unpack('<HH', m.read(m.symbols['sGpuRegBuffer'] + 0x14, 4))
for y in range(1, 4):
    for x in range(4, 26):
        row, col = (y + scroll_y // 8) & 31, (x + scroll_x // 8) & 31
        struct.pack_into('<H', overlay, 2 * (row * 32 + col), 0xF001)
m.write(0x0600D000, bytes(overlay))
with_text = capture()
assert with_text == clean, 'Menu text was baked into the glass backdrop'
print('PASS shared-BG window glyphs do not alter captured scenery or its palette', flush=True)
