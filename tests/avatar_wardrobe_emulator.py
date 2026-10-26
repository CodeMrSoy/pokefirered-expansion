#!/usr/bin/env python3
"""Real new-game choice, Wardrobe, avatar states, portraits, and flash-save checks."""
import ctypes as c
import os
import pathlib
import struct
import subprocess
import types

harness = pathlib.Path(__file__).with_name('quantum_qol_emulator.py')
m = types.ModuleType('avatar_harness')
m.__file__ = str(harness)
source = harness.read_text().split('run(360);press(3);press(8);snap(\'boot\')')[0]
exec(compile(source, str(harness), 'exec'), m.__dict__)

def task_active(name):
    expected = m.symbols[name] | 1
    return any(m.read(m.symbols['gTasks'] + i*40 + 4, 1) != b'\x00'
               and struct.unpack('<I', m.read(m.symbols['gTasks'] + i*40, 4))[0] == expected
               for i in range(16))

def wait_task(name, frames=600):
    for _ in range(frames):
        if task_active(name):
            return
        m.run(1)
    raise AssertionError('Did not reach ' + name)

m.run(360)
m.press(3)
m.press(8)
for _ in range(12):
    if task_active('Task_OakSpeech_HandleGenderInput'):
        break
    m.press(8)
wait_task('Task_OakSpeech_HandleGenderInput')
m.press(8)
wait_task('Task_AvatarChoice_Input')
for look in range(7):
    m.snap('new-game-avatar-' + str(look))
    m.press(7, 20)
# Wrap, then choose Emerald Brendan while keeping the logical gender male.
m.press(7, 20)
m.press(7, 20)
m.press(8)
for _ in range(7):
    m.press(8)
m.press(3)
m.press(8)
for _ in range(5):
    m.press(8)
m.press(5)
m.press(8)
for _ in range(12):
    m.press(8)
m.press(0)
m.press(0)
m.press(0)
m.snap('avatar-new-game-field')

native_dir = m.d / ('avatar-native-calls-' + pathlib.Path(__file__).stem)
native_dir.mkdir(exist_ok=True)
native_addr = m.symbols['gDecompressionBuffer'] + 0x3000
result_addr = m.symbols['gDecompressionBuffer'] + 0x3f00
tool_prefix = os.environ.get('ARM_NM', 'arm-none-eabi-nm').removesuffix('nm')

def native(name, *args):
    assembly = ['.syntax unified', '.thumb', '.thumb_func', '_start:', 'push {r4, lr}']
    assembly += [f'ldr r{i}, arg{i}' for i in range(len(args))]
    assembly += ['ldr r3, function', 'bl invoke', 'ldr r3, result', 'str r0, [r3]',
                 'movs r0, #1', 'pop {r4, pc}', 'invoke:', 'bx r3', '.align 2',
                 f'function: .word {m.symbols[name] | 1}', f'result: .word {result_addr}']
    assembly += [f'arg{i}: .word {arg}' for i, arg in enumerate(args)]
    (native_dir / 'call.s').write_text('\n'.join(assembly) + '\n')
    subprocess.run([tool_prefix + 'as', '-mthumb', '-mcpu=arm7tdmi',
                    '-o', str(native_dir / 'call.o'), str(native_dir / 'call.s')], check=True)
    subprocess.run([tool_prefix + 'objcopy', '-O', 'binary', '-j', '.text',
                    str(native_dir / 'call.o'), str(native_dir / 'call.bin')], check=True)
    m.write(native_addr, (native_dir / 'call.bin').read_bytes())
    m.inject(b'\x23' + struct.pack('<I', native_addr | 1) + b'\x6b\x02')
    if name == 'TrySavingData':
        # Flash programming may occupy the CPU across several video frames.
        for _ in range(40):
            if m.read(m.symbols['sGlobalScriptContextStatus'], 1) == b'\x02':
                break
            m.run(60)
    return struct.unpack('<I', m.read(result_addr, 4))[0]

avatar_var = native('GetVarPointer', 0x40fd)
assert struct.unpack('<H', m.read(avatar_var, 2))[0] == 3, 'New game cleared the selected look'
save2 = struct.unpack('<I', m.read(m.symbols['gSaveBlock2Ptr'], 4))[0]
identity = m.read(save2, 9)
assert identity[8] == 0

# Previously saved Ruby/Sapphire appearances migrate to matching Emerald looks.
for saved, expected in ((5, 2), (6, 3)):
    native('VarSet', 0x40fd, saved)
    assert native('GetCurrentAvatarLook') == expected
    assert struct.unpack('<H', m.read(avatar_var, 2))[0] == expected + 1
    assert m.read(save2, 9) == identity
# Cody uses 7; zero and invalid values retain the gender default.
for saved, expected in ((0, 0), (7, 4), (8, 5), (9, 6), (65535, 0)):
    native('VarSet', 0x40fd, saved)
    assert native('GetCurrentAvatarLook') == expected
native('SetCurrentAvatarLook', 4)
assert struct.unpack('<H', m.read(avatar_var, 2))[0] == 7
native('SetCurrentAvatarLook', 2)

fixture = b'\x23' + struct.pack('<I', (m.symbols['ScrCmd_createmon'] | 1) + 0x2000000)
fixture += struct.pack('<BBHHI', 0, 6, 1, 25, 0)
fixture += b'\x44' + struct.pack('<HH', 717, 1) + b'\x02'
m.inject(fixture)
m.press(3)
m.press(8)
for key in (7, 5, 5, 7):
    m.press(key, 20)
assert m.read(m.symbols['sHubCursor'], 1) == b'\x05'
m.snap('wardrobe-hub')
m.press(8)
for look in (2, 3, 4, 5, 6, 0, 1):
    assert m.read(m.symbols['sWardrobeLook'], 1) == bytes([look])
    m.snap('wardrobe-look-' + str(look))
    assert struct.unpack('<H', m.read(avatar_var, 2))[0] == 3, 'Preview altered the saved avatar'
    m.press(7, 20)
# Cancel must leave the original look; reopening preserves it.
m.press(0)
m.press(8)
assert m.read(m.symbols['sWardrobeLook'], 1) == b'\x02'
m.press(7, 20)
m.press(8)
assert struct.unpack('<H', m.read(avatar_var, 2))[0] == 4
m.press(0)
assert m.read(save2, 9) == identity, 'Wardrobe changed name or gender'

names = ['Red', 'Green', 'Brendan', 'May', 'Cody', 'Ben', 'Brandon']
states = [(0, 'Normal'), (1, 'Bike'), (3, 'Surf'), (10, 'Fish'), (8, 'FieldMove')]
for look, name in enumerate(names):
    native('SetCurrentAvatarLook', look)
    assert native('GetCurrentAvatarFrontPic') == [135, 136, 148, 149, 150, 151, 152][look]
    assert native('GetCurrentAvatarBackPic') == [0, 1, 7, 8, 9, 10, 11][look]
    for state, suffix in states:
        gfx = native('GetPlayerAvatarGraphicsIdByStateId', state)
        expected = look*7 + {'Normal':0, 'Bike':1, 'Surf':2, 'FieldMove':3, 'Fish':4}[suffix] if look < 2 else 157 + (look-2)*7 + {'Normal':0, 'Bike':1, 'Surf':2, 'FieldMove':3, 'Fish':4}[suffix]
        if look >= 4:
            expected = 185 + (look-4)*7 + {'Normal':0, 'Bike':1, 'Surf':2, 'FieldMove':3, 'Fish':4}[suffix]
        assert gfx == expected, (look, state, gfx, expected)
    for state, suffix in states:
        native('SetPlayerAvatarStateMask', 1 << state)
        native('ApplyAvatarLookToField', look)
        if suffix in ('Fish', 'FieldMove'):
            # These are action graphics, not persistent avatar-state bits.
            obj = m.symbols['gObjectEvents'] + m.read(m.symbols['gPlayerAvatar'] + 5, 1)[0] * 36
            native('ObjectEventSetGraphicsId', obj, native('GetPlayerAvatarGraphicsIdByStateId', state))
            native('ObjectEventTurn', obj, 1)
        sprite = m.read(m.symbols['gPlayerAvatar'] + 4, 1)[0]
        frames = struct.unpack('<I', m.read(m.symbols['gSprites'] + sprite*68 + 12, 4))[0]
        symbol = 'sPicTable_' + name + ('Item' if suffix == 'FieldMove' else suffix) if look < 2 else 'sAvatar' + name + ('Item' if suffix == 'FieldMove' and look >= 4 else suffix) + 'Frames'
        assert frames == m.symbols[symbol], (look, suffix, hex(frames))
        if look >= 4:
            player_object = m.symbols['gObjectEvents'] + m.read(m.symbols['gPlayerAvatar'] + 5, 1)[0] * 36
            oam2 = struct.unpack('<H', m.read(m.symbols['gSprites'] + sprite*68 + 4, 2))[0]
            palette = (oam2 >> 12) & 15
            expected_palette = (m.root / ('graphics/avatars/' + name.lower() + '/overworld.gbapal')).read_bytes()
            assert m.read(m.symbols['gPlttBufferUnfaded'] + 512 + palette*32, 32) == expected_palette, ('Stale avatar palette', name)
            asset, frame_size = {'Normal': ('normal', 256), 'Bike': ('bike', 512), 'Surf': ('surf_run', 256), 'Fish': ('fish', 512), 'FieldMove': ('item', 256)}[suffix]
            tiles = (m.root / ('graphics/avatars/' + name.lower() + '/' + asset + '.4bpp')).read_bytes()
            actual_tiles = m.read(0x6010000 + (oam2 & 1023)*32, frame_size)
            assert any(actual_tiles == tiles[i:i+frame_size] for i in range(0, len(tiles), frame_size)), ('Stale/incorrect avatar tiles', name, suffix)
        m.snap('avatar-state-' + str(look) + '-' + suffix.lower())
        if look >= 5 and suffix == 'Normal':
            native('ObjectEventTurn', player_object, 1)
            m.snap('avatar-front-facing-' + str(look))
# Save the last look on foot and reload through the real Continue menu.
for saved_look, saved_value in ((4, 7), (5, 8), (6, 9)):
    native('SetPlayerAvatarStateMask', 1)
    native('ApplyAvatarLookToField', saved_look)
    save_result = native('TrySavingData', 0)
    assert save_result == 1, (save_result, m.read(m.symbols['gFlashMemoryPresent'], 1),
                              m.read(m.symbols['gSaveAttemptStatus'], 2))
    m.lib.retro_reset()
    m.run(360)
    m.press(3)
    m.press(8)
    m.press(8)  # Reset may still be completing the title transition on the first A.
    m.run(180)
    m.snap('avatar-reload-debug')
    avatar_var = native('GetVarPointer', 0x40fd)
    assert struct.unpack('<H', m.read(avatar_var, 2))[0] == saved_value, ('Saved avatar did not survive reload', hex(avatar_var), m.read(avatar_var, 2), m.read(m.symbols['gSaveFileStatus'], 1), m.read(m.symbols['sGlobalScriptContextStatus'], 1))
    assert native('GetCurrentAvatarLook') == saved_look
    save2 = struct.unpack('<I', m.read(m.symbols['gSaveBlock2Ptr'], 4))[0]
    assert m.read(save2, 9) == identity
    m.snap('avatar-save-reload-' + str(saved_look))
m.press(3)
m.press(8)
m.press(5, 20)  # Map is the lower-left app in the six-app grid.
m.press(8)
wait_task('Task_RegionMap')
m.snap('avatar-town-map')
m.press(0)
m.press(0)

size = m.lib.retro_serialize_size()
field = c.create_string_buffer(size)
assert m.lib.retro_serialize(field, size)
(m.d/'avatar-field.state').write_bytes(field.raw)
backs = ['Red', 'Leaf', 'QuantumBrendan', 'QuantumMay', 'QuantumCody', 'QuantumBen', 'QuantumBrandon']
for look, back in enumerate(backs):
    assert m.lib.retro_unserialize(field, size)
    native('ApplyAvatarLookToField', look)
    battle = b'\xb6' + struct.pack('<HBHHBH', 92, 5, 0, 0, 0, 0) + b'\xb7\x6b\x02'
    address = m.symbols['gDecompressionBuffer']
    m.write(address, battle)
    ctx = m.symbols['sGlobalScriptContext']
    m.write(ctx, b'\x00\x01\x00\x00')
    m.write(ctx + 8, struct.pack('<I', address))
    m.write(m.symbols['sGlobalScriptContextStatus'], b'\x00')
    for _ in range(600):
        m.run(1)
        if any(m.read(m.symbols['gSprites'] + i*68 + 62, 1)[0] & 1
               and struct.unpack('<I', m.read(m.symbols['gSprites'] + i*68 + 12, 4))[0]
               == m.symbols['gTrainerBackPicTable_' + back] for i in range(64)):
            m.run(90)
            m.snap('avatar-battle-back-' + str(look))
            break
    else:
        raise AssertionError('Battle did not use ' + back + ' back portrait')
for look in range(2, 7):
    assert m.lib.retro_unserialize(field, size)
    native('ApplyAvatarLookToField', look)
    native('StopPlayerAvatar')
    player_object = m.symbols['gObjectEvents'] + m.read(m.symbols['gPlayerAvatar'] + 5, 1)[0] * 36
    native('ObjectEventClearHeldMovementIfActive', player_object)
    native('UnfreezeObjectEvents')
    # The real Fly map callback locks input while its landing task runs.
    native('FldEff_FlyIn')
    # Native injection ends its script and releases controls; restore the real
    # Fly callback's lock after that helper has returned.
    m.write(m.symbols['sLockFieldControls'], b'\x01')
    m.run(600)
    if task_active('Task_FlyIn'):
        m.snap('avatar-fly-debug')
        active = [(i, m.read(m.symbols['gTasks'] + i*40 + 8, 32).hex()) for i in range(16)
                  if struct.unpack('<I', m.read(m.symbols['gTasks'] + i*40, 4))[0] == (m.symbols['Task_FlyIn'] | 1)]
        raise AssertionError(('Fly landing did not finish', look, active))
    assert m.read(m.symbols['gPlayerAvatar'] + 6, 1) == b'\x00'
    assert native('GetCurrentAvatarLook') == look
    native('UnlockPlayerFieldControls')
print('Seven creation/Wardrobe previews, cancel/confirm, identity, movement, actual battle backs, tablet map, Fly landing, and real save/reload passed')
