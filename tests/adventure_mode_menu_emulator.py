"""Real title/Oak/avatar/Flash checks for the two adventures and V2 migration.

Run separately with ADVENTURE_TEST_MODE=0 and 1. The legacy case uses an
unmodified V2 Flash image via ADVENTURE_LEGACY_SAVE; it never fabricates a save
checksum or writes the mode tag into the fixture.
"""
import ctypes as c
import os
import pathlib
import struct
import types

root = pathlib.Path(__file__).resolve().parents[1]
mode = int(os.environ.get('ADVENTURE_TEST_MODE', '1'))
legacy = os.environ.get('ADVENTURE_LEGACY_SAVE')
p = root / 'tests/quantum_qol_emulator.py'
source = p.read_text().split("run(360);press(3);press(8);snap('boot')")[0]
output = root / 'build/v3-adventure-tests' / ('legacy' if legacy else str(mode))
source = source.replace("d=root/'build/quantum-qol-tests'", f'd=pathlib.Path({str(output)!r})')
os.environ.setdefault('QUANTUM_QA_OUTPUT', str(output))
m = types.ModuleType('adventure_menu_harness'); m.__file__ = str(p)
exec(compile(source, str(p), 'exec'), m.__dict__)

def ptr(name):
    return struct.unpack('<I', m.read(m.symbols[name], 4))[0]

def task(name):
    fn = m.symbols[name] & ~1
    return next((i for i in range(16) if m.read(m.symbols['gTasks'] + i * 40 + 4, 1) != b'\0'
                 and struct.unpack('<I', m.read(m.symbols['gTasks'] + i * 40, 4))[0] & ~1 == fn), None)

def wait(name):
    for _ in range(1200):
        if task(name) is not None:
            return task(name)
        m.run(1)
    raise AssertionError('Missing task ' + name)

def record():
    return m.read(ptr('gSaveBlock2Ptr') + 3795, 8)

m.lib.retro_get_memory_data.argtypes = [c.c_uint]
m.lib.retro_get_memory_data.restype = c.c_void_p
m.lib.retro_get_memory_size.argtypes = [c.c_uint]
m.lib.retro_get_memory_size.restype = c.c_size_t
if legacy:
    flash = pathlib.Path(legacy).read_bytes()
    assert b'QADV' not in flash, 'Fixture must be an original V2 save'
    assert len(flash) == m.lib.retro_get_memory_size(0)
    c.memmove(m.lib.retro_get_memory_data(0), flash, len(flash))
    m.lib.retro_reset()
m.run(360); m.press(3); wait('Task_HandleMenuInput')
if legacy:
    assert record() == b'QADV\x01\x01\xfe\xa7'
    sectors = [flash[i:i+4096] for i in range(0, len(flash), 4096)]
    valid = [b for b in sectors if struct.unpack_from('<H', b, 4084)[0] == 0
             and struct.unpack_from('<I', b, 4088)[0] == 0x08012025]
    old = max(valid, key=lambda b: struct.unpack_from('<I', b, 4092)[0])
    save = ptr('gSaveBlock2Ptr')
    assert m.read(save + 3756, 39) == old[3756:3795], 'V2 seed/settings/history changed'
    m.snap('v2-save-migrated-quantum')
    # Existing gameplay settings and encounter history retain their old offsets.
    save = ptr('gSaveBlock2Ptr')
    before = m.read(save + 3756, 39)
    # A pending Classic choice and cancellation cannot relabel Continue.
    m.press(5); m.press(8); wait('Task_AdventureSelection')
    m.press(4); m.press(8); m.press(8); wait('Task_RandomizedOptions')
    m.press(0); wait('Task_AdventureSelection'); m.press(0); wait('Task_HandleMenuInput')
    assert record() == b'QADV\x01\x01\xfe\xa7'
    assert m.read(ptr('gSaveBlock2Ptr') + 3756, 39) == before
    m.press(4); m.press(8); m.run(500)
else:
    m.press(8); t = wait('Task_AdventureSelection')
    assert struct.unpack('<h', m.read(m.symbols['gTasks'] + t * 40 + 8 + 13 * 2, 2))[0] == 1
    original = record()
    # Selection and confirmation can both be canceled, with no save mutation.
    m.snap('adventure-default-quantum')
    m.press(8); m.snap('adventure-confirmation'); m.press(0); m.press(0)
    wait('Task_HandleMenuInput'); assert record() == original
    m.press(8); wait('Task_AdventureSelection')
    if mode == 0:
        m.press(4)
    m.snap('adventure-selection')
    m.press(8); m.press(8); wait('Task_RandomizedOptions')
    m.snap('adventure-gameplay-options')
    assert record() == original, 'Pending choice changed the active save'
    # Test independent category controls, then select the explicit Begin row.
    m.press(8); m.press(5); m.press(7); m.press(5); m.press(7)
    m.press(5); m.press(6); m.press(5); m.press(7)
    # Pokemon, moves, abilities, Nuzlocke ON, caps OFF. Items remain OFF.
    assert m.read(ptr('gSaveBlock2Ptr') + 3762, 1)[0] == 23
    if mode == 1:
        m.press(5); m.press(5); m.press(7)
        assert m.read(ptr('gSaveBlock2Ptr') + 3762, 1)[0] == 87
        m.snap('quantum-vidra-gym-option')
        m.press(5)
    else:
        m.press(5); m.press(5)  # Classic skips Vidra gyms and reaches Begin.
    m.snap('adventure-begin')
    m.press(8); wait('Task_OakSpeech_HandleGenderInput')
    m.press(8); wait('Task_AvatarChoice_Input'); m.snap('adventure-character-selection'); m.press(8)
    for _ in range(7): m.press(8)
    m.press(3); m.press(8)
    for _ in range(5): m.press(8)
    m.press(5); m.press(8)
    for _ in range(12): m.press(8)
    m.press(0); m.press(0); m.press(0)
    assert record() == b'QADV\x01' + bytes((mode, mode ^ 255, 0xA7))
    expected_bits = 87 if mode == 1 else 23
    assert m.read(ptr('gSaveBlock2Ptr') + 3762, 1)[0] == expected_bits
    m.snap('adventure-new-game-field')

helpers = (root / 'tests/rom_cleanup_migration_emulator.py').read_text().split('old=(m.root')[0]
helpers = helpers.replace('import quantum_qol_emulator as m', '')
exec(compile(helpers, 'adventure_native_helpers', 'exec'))
assert native('AdventureMode_Get') == (1 if legacy else mode)
# Nuzlocke's first-encounter history and game options must survive real Flash.
native('Nuzlocke_BeginEncounter', 16, 0)
native('Nuzlocke_BeginEncounter', 16, 0)
assert native('Nuzlocke_CanCatch') == 0
history = m.read(ptr('gSaveBlock2Ptr') + 3763, 32)
seed = m.read(ptr('gSaveBlock2Ptr') + 3756, 4)
expected_record = record()
assert native('TrySavingData', 0) == 1
flash = c.string_at(m.lib.retro_get_memory_data(0), m.lib.retro_get_memory_size(0))
(m.d / 'adventure.sav').write_bytes(flash)
m.lib.retro_reset(); m.run(360); m.press(3); wait('Task_HandleMenuInput')
assert record() == expected_record
assert m.read(ptr('gSaveBlock2Ptr') + 3763, 32) == history
assert m.read(ptr('gSaveBlock2Ptr') + 3756, 4) == seed
m.snap('adventure-continue-label')
# Read-only adventure: Randomized Options on a loaded save has no Begin/choice.
m.press(5); m.press(5); m.press(8); wait('Task_RandomizedOptions')
m.snap('adventure-loaded-options')
m.press(0); wait('Task_HandleMenuInput')
assert record() == expected_record
m.press(4); m.press(4); m.press(8); m.run(500)
assert native('AdventureMode_Get') == (1 if legacy else mode)
assert m.read(ptr('gSaveBlock2Ptr') + 3763, 32) == history
print('PASS: adventure flow, cancellation, immutable loaded mode, options, avatar intro, Flash save/reset/Continue', 'legacy V2' if legacy else mode)
