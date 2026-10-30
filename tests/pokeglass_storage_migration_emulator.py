"""Legacy 14-box flash migration, overflow preservation and six-box round trip."""
import ctypes as c
import pathlib
import struct

setup = pathlib.Path(__file__).with_name('avatar_wardrobe_emulator.py')
exec(compile(setup.read_text().split("fixture = b'\\x23'")[0], str(setup), 'exec'))
fixture = b'\x23' + struct.pack('<I', (m.symbols['ScrCmd_createmon'] | 1) + 0x2000000)
fixture += struct.pack('<BBHHI', 0, 6, 1, 25, 0) + b'\x02'
m.inject(fixture)
mon = m.read(m.symbols['gPlayerParty'], 100)
assert native('TrySavingData', 0) == 1
m.lib.retro_get_memory_data.argtypes = [c.c_uint]
m.lib.retro_get_memory_data.restype = c.c_void_p
m.lib.retro_get_memory_size.argtypes = [c.c_uint]
m.lib.retro_get_memory_size.restype = c.c_size_t
flash_ptr = m.lib.retro_get_memory_data(0)
flash_size = m.lib.retro_get_memory_size(0)
assert flash_ptr and flash_size >= 131072
baseline = c.string_at(flash_ptr, flash_size)
storage_size = 34144

def fixture_flash(count):
    flash = bytearray(baseline)
    payload = bytearray(storage_size)
    # The old current box and names live at their original on-flash offsets.
    payload[0] = 13
    for box in range(14):
        payload[33604 + box*9:33604 + box*9 + 5] = bytes([0xBC, 0xC9, 0xD2, 0xFF, 0])
    # Spread <=180 mons into the retired boxes first to exercise compaction.
    indexes = list(range(419, 179, -1)) + list(range(180))
    for index in indexes[:count]:
        payload[4 + index*80:4 + (index+1)*80] = mon[:80]
    payload[33744:33844] = mon  # Retained legacy fusion/recovery record.
    sectors = 0
    for physical in range(28):
        start = physical * 4096
        sid, checksum, signature, counter = struct.unpack_from('<HHII', flash, start+4084)
        if signature != 0x08012025 or not 5 <= sid <= 13:
            continue
        offset = (sid-5)*3968
        chunk = payload[offset:offset+3968]
        flash[start:start+len(chunk)] = chunk
        total = sum(struct.unpack('<'+'I'*(len(chunk)//4), chunk)) & 0xffffffff
        struct.pack_into('<H', flash, start+4086, ((total>>16)+total)&0xffff)
        sectors += 1
    assert sectors >= 9
    c.memmove(flash_ptr, bytes(flash), flash_size)
    return bytes(flash)

for count in (0, 1, 180):
    disk = fixture_flash(count)
    assert native('LoadGameSave', 0) == 1
    box = struct.unpack('<I', m.read(m.symbols['gPokemonStoragePtr'],4))[0]
    assert m.read(box,1) == b'\x00'
    assert sum(bool(m.read(box+4+i*80+19,1)[0]&2) for i in range(180)) == count
    assert m.read(box+14464,100) == mon, 'Fusion/recovery payload changed'
    assert c.string_at(flash_ptr,flash_size) == disk, 'Loading modified flash'
    print('PASS legacy migration count',count,'and preserved recovery record/flash',flush=True)

disk = fixture_flash(181)
assert native('LoadGameSave',0) == 3
assert c.string_at(flash_ptr,flash_size) == disk
m.lib.retro_reset(); m.run(360); m.press(3); m.run(300)
assert struct.unpack('<H',m.read(m.symbols['gSaveFileStatus'],2))[0] == 3
for _ in range(3): m.press(8,30)
assert c.string_at(flash_ptr,flash_size) == disk
m.snap('pokeglass-storage-legacy-overflow')
print('PASS 181-mon legacy save refuses Continue/New Game and remains byte-identical',flush=True)
