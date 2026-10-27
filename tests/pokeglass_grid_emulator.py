#!/usr/bin/env python3
"""Exercise the Start replacement, both app pages, native apps and save in mGBA."""
import pathlib
import struct
setup = pathlib.Path(__file__).with_name('avatar_wardrobe_emulator.py')
exec(compile(setup.read_text().split("fixture = b'\\x23'")[0], str(setup), 'exec'))
native('FlagSet', 0x829)
fixture = b'\x23' + struct.pack('<I', (m.symbols['ScrCmd_createmon'] | 1) + 0x2000000)
fixture += struct.pack('<BBHHI', 0, 6, 1, 25, 0)
m.inject(fixture + b'\x44' + struct.pack('<HH', 717, 1) + b'\x02')
avatar_offset = avatar_var - struct.unpack('<I',m.read(m.symbols['gSaveBlock1Ptr'],4))[0]
def current_look():
    save = struct.unpack('<I',m.read(m.symbols['gSaveBlock1Ptr'],4))[0]
    return m.read(save + avatar_offset,2)
original_look = current_look()
m.press(3)
wait_task('Task_PokeGlassHub')
m.run(30)
assert 'Task_StartMenuHandleInput' not in m.symbols or not task_active('Task_StartMenuHandleInput')

def cursor(): return m.read(m.symbols['sHubCursor'], 1)[0]
def move(key, expected):
    m.press(key, 20)
    assert cursor() == expected, (key, cursor(), expected)
def app(task, label):
    selected = cursor()
    m.press(8)
    wait_task(task)
    m.run(60)
    m.snap('phone-' + label)
    m.press(0)
    wait_task('Task_PokeGlassHub')
    m.run(30)
    assert cursor() == selected
    assert current_look() == original_look

assert cursor() == 0
m.snap('phone-page-one')
# Every app on page one and native return paths.
app('Task_PokeGlassPokedex', 'pokedex')
move(7, 1); app('Task_HandleChooseMonInput', 'party')
move(7, 2); app('Task_PCMainMenu', 'pc')
move(5, 5); app('Task_BagMenu_HandleInput', 'bag')
move(6, 3); app('Task_PokeGlassStats', 'stats')
move(6, 4); app('Task_RegionMap', 'map')
# Left beyond the lower row enters page two, skipping unused slots.
development = 'Debug_ShowMainMenu' in m.symbols
move(6, 9 if development else 8)
m.snap('phone-page-two')
if development:
    app('DebugTask_HandleMenuInput_Main', 'debug')
    move(4, 6)
else:
    move(6, 7);move(6, 6)
app('Task_TrainerCard', 'trainer-card')
move(7, 7); app('Task_OptionMenu', 'options')
move(7, 8)
# Cancel Save and return to the same page/tile.
m.press(8);wait_task('task50_save_game');m.run(120);m.snap('phone-save-prompt')
m.press(0);wait_task('Task_PokeGlassHub');m.run(30)
assert cursor() == 8
# Confirm a real flash save via the launcher (including any overwrite prompt).
m.press(8);wait_task('task50_save_game');m.run(120)
for _ in range(8):
    if task_active('Task_PokeGlassHub'): break
    m.press(8,180)
wait_task('Task_PokeGlassHub');m.run(30)
assert m.read(m.symbols['gSaveAttemptStatus'],2) == b'\x01\x00'
assert current_look() == original_look
# Right past page two returns to page one, and left goes back.
move(7,0);move(6,8);move(7,0)
# Exit releases scripts/controls and Start reopens PokéGlass directly.
m.press(0)
assert m.read(m.symbols['sGlobalScriptContextStatus'],1) == b'\x02'
assert m.read(m.symbols['sLockFieldControls'],1) == b'\x00'
m.press(3);wait_task('Task_PokeGlassHub');m.run(30)
assert 'Task_StartMenuHandleInput' not in m.symbols or not task_active('Task_StartMenuHandleInput')
m.press(0)
# Retired wardrobe special cannot mutate the fixed starting outfit.
native('ShowPokeGlassWardrobe')
assert current_look() == original_look
assert 'Task_PokeGlassWardrobe' not in m.symbols
# Field-item native callbacks must reopen the launcher, never the old list.
native('CB2_ReturnToFieldWithOpenMenu')
wait_task('Task_PokeGlassHub');m.run(30)
assert 'Task_StartMenuHandleInput' not in m.symbols or not task_active('Task_StartMenuHandleInput')
m.press(0)
assert m.read(m.symbols['sLockFieldControls'],1) == b'\x00'
print('PASS direct Start, two-page horizontal paging, all available apps, native returns, Save cancel/flash write, fixed outfit, field unlock and reopening',flush=True)
