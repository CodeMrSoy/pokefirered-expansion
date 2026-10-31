"""TM Case app: empty entry, direct teaching/cancel, Bag route and flash Continue."""
import pathlib,struct,re
setup=pathlib.Path(__file__).with_name('avatar_wardrobe_emulator.py')
exec(compile(setup.read_text().split("fixture = b'\\x23'")[0],str(setup),'exec'))
m.inject(b'\x29'+struct.pack('<H',0x829)+b'\x44'+struct.pack('<HH',717,1)+b'\x02')
def cursor():return m.read(m.symbols['sHubCursor'],1)[0]
def open_app():
 m.press(3)
 try:wait_task('Task_PokeGlassHub')
 except AssertionError:
  m.snap('tm-app-open-error');print('OPEN ERROR',m.read(m.symbols['sLockFieldControls'],1),m.read(m.symbols['sGlobalScriptContextStatus'],1),flush=True);raise
 m.run(40)
 if cursor()==0:m.press(5,30);m.press(6,30)
 assert cursor()==12,cursor()
 m.snap('tm-app-launcher');m.press(8);wait_task('Task_HandleListInput');m.run(90)
def close_app():
 m.run(90) # The list task exists before the native fade-in finishes.
 m.press(0,180);wait_task('Task_PokeGlassHub');m.run(40);assert cursor()==12
 m.press(0,90);assert m.read(m.symbols['sLockFieldControls'],1)==b'\x00'
# No case or TMs is safe: app remains available and close restores the field.
open_app();m.snap('tm-app-empty');close_app()
fixture=b'\x23'+struct.pack('<I',(m.symbols['ScrCmd_createmon']|1)+0x2000000)+struct.pack('<BBHHI',0,6,66,5,0)
for id,q in [(715,1),(582,2)]:fixture+=b'\x44'+struct.pack('<HH',id,q)
m.inject(fixture+b'\x02')
party=m.symbols['gPlayerParty'];scratch=m.symbols['gDecompressionBuffer']+0x2000;m.write(scratch,bytes(4));native('SetMonData',party,23,scratch)
move=native('ItemIdToBattleMoveId',582)
orders={int(n):tuple(map(int,v)) for n,*v in re.findall(r'SUBSTRUCT_CASE\(\s*(\d+),(\d+),(\d+),(\d+),(\d+)\)',(m.root/'src/pokemon.c').read_text(encoding='utf-8'))}
def moves():
 mon=m.read(party,80);pid,ot=struct.unpack_from('<II',mon);data=struct.pack('<12I',*(x^pid^ot for x in struct.unpack_from('<12I',mon,32)))
 return struct.unpack_from('<4H',data,orders[pid%24][1]*12)
def quantity():
 record=m.symbols['gBagPockets']+3*8;p=struct.unpack('<I',m.read(record,4))[0];n=m.read(record+4,1)[0]
 return sum(q for id,q in (struct.unpack('<HH',m.read(p+i*4,4)) for i in range(n)) if id==582)
assert move not in moves() and quantity()==2
open_app();m.snap('tm-app-list')
def choose_use():
 m.run(90)
 m.press(8,60);wait_task('Task_ContextMenu_HandleInput');m.snap('tm-app-actions');m.press(8,180);wait_task('Task_HandleChooseMonInput');m.run(60)
choose_use();m.snap('tm-app-party');m.press(0,180);wait_task('Task_HandleListInput');assert quantity()==2
choose_use();m.press(8,240)
for _ in range(12):
 if task_active('Task_HandleListInput'):break
 m.press(8,120)
wait_task('Task_HandleListInput');assert move in moves(),('Move not learned',move,moves());assert quantity()==1
m.run(90);m.snap('tm-app-after-teaching');close_app()
# Repeated direct launches preserve the selected tile and release all native buffers.
for _ in range(4):open_app();close_app()
assert native('TrySavingData',0)==1
m.lib.retro_reset();m.run(360);m.press(3);m.press(8,240);m.press(0,60)
assert move in moves() and quantity()==1
open_app();m.snap('tm-app-continue');close_app()
print('PASS empty TM app, direct open/close, teaching cancellation, real learned move and TM consumption, repeated returns, and flash Continue',flush=True)
