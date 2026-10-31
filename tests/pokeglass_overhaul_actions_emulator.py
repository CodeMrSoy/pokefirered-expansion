"""Real Field Kit activation and Summary navigation without duplicate Stats."""
import pathlib,struct
setup=pathlib.Path(__file__).with_name('avatar_wardrobe_emulator.py')
exec(compile(setup.read_text().split("fixture = b'\\x23'")[0],str(setup),'exec'))
fixture=b'\x23'+struct.pack('<I',(m.symbols['ScrCmd_createmon']|1)+0x2000000)+struct.pack('<BBHHI',0,6,1,25,0)
m.inject(fixture+b'\x29'+struct.pack('<H',0x829)+b'\x44'+struct.pack('<HH',717,1)+b'\x02')
m.press(3);wait_task('Task_PokeGlassHub');m.run(40)
for _ in range(3):m.press(7,30)
m.press(8);wait_task('Task_PokeGlassFieldKit');m.run(40)
m.press(8,30);assert task_active('Task_PokeGlassFieldKit')
m.press(0,30);wait_task('Task_PokeGlassHub');m.run(30);m.press(0)
item=native('FieldTool_GetItem',4);assert native('FieldTool_Collect',item)==1
for badge in range(0x820,0x828):native('FlagSet',badge)
assert native('FieldMove_IsUnlocked',4)==1
m.press(3);wait_task('Task_PokeGlassHub');m.run(40);m.press(8);wait_task('Task_PokeGlassFieldKit');m.run(40)
for _ in range(4):m.press(5,30)
m.press(8,180)
assert not task_active('Task_PokeGlassFieldKit')
for _ in range(5):m.press(0,120)
assert m.read(m.symbols['sLockFieldControls'],1)==b'\x00'
assert native('FieldTool_IsOwned',4)==1
print('PASS Field Kit missing-tool guard, collected Lantern use, retained tool and field unlock',flush=True)
m.press(3);wait_task('Task_PokeGlassHub');m.run(40)
# Field Kit -> Storage -> Party.
for _ in range(2):m.press(6,30)
m.press(8);wait_task('Task_HandleChooseMonInput');m.run(60)
m.press(8);m.run(60);m.press(8);wait_task('Task_InputHandler_Info');m.run(90)
summary=struct.unpack('<I',m.read(m.symbols['sMonSummaryScreen'],4))[0]
def page():return m.read(summary+0x32c4,1)[0]
assert page()==0,('Summary initial page',page())
m.press(7,120);assert page()==2,('Duplicate stats page remains',page())
m.snap('overhaul-summary-moves')
m.press(6,120);assert page()==0
m.press(0,180)
if task_active('Task_HandleSelectionMenuInput'):m.press(0,90)
wait_task('Task_HandleChooseMonInput');m.press(0,180);wait_task('Task_PokeGlassHub');m.press(0)
print('PASS Summary Info/Move navigation skips duplicate stats and returns through Party/launcher',flush=True)
