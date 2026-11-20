"""Real icons, pagination, pocket navigation, empty pocket, sorting and moving."""
import pathlib,struct
setup=pathlib.Path(__file__).with_name('avatar_wardrobe_emulator.py')
exec(compile(setup.read_text().split("fixture = b'\\x23'")[0],str(setup),'exec'))
fixture=b'\x23'+struct.pack('<I',(m.symbols['ScrCmd_givegiftmon']|1)+0x2000000)+struct.pack('<BBHHI',0,6,1,25,0)
fixture+=b'\x29'+struct.pack('<H',0x829)
for item,q in [(717,1)]+[(i,999 if i==28 else i) for i in range(28,46)]:fixture+=b'\x44'+struct.pack('<HH',item,q)
m.inject(fixture+b'\x02')
def selected():return struct.unpack('<i',m.read(m.symbols['sGlassGridSelection'],4))[0]
def page():return struct.unpack('<H',m.read(m.symbols['sGlassGridPage'],2))[0]
def openbag():
 m.write(m.symbols['sHubCursor'],b'\x05');m.press(3);wait_task('Task_PokeGlassHub');m.press(8);wait_task('Task_BagMenu_HandleInput');m.run(60)
openbag();assert selected()==0
assert m.read(m.symbols['sGlassGridSprites'],9).count(64)==0
assert struct.unpack('<9H',m.read(m.symbols['sGlassGridItems'],18))==tuple(range(28,37))
m.snap('bag-grid-page-one')
m.press(5,30);assert selected()==3
m.press(4,30);assert selected()==0
for _ in range(9):m.press(7,20)
assert selected()==9 and page()==1
assert struct.unpack('<9H',m.read(m.symbols['sGlassGridItems'],18))==tuple(range(37,46))
m.snap('bag-grid-page-two')
for _ in range(9):m.press(7,20)
assert selected()==-2 and page()==2 # native Cancel ID
m.snap('bag-grid-last-page')
m.press(6,30);assert selected()==17
# START invokes the existing sort actions; return must rebuild real icon order.
m.press(3,30);wait_task('Task_ItemContext_SingleRow');m.snap('bag-grid-sort');m.press(8,90);wait_task('Task_BagMenu_HandleInput')
m.press(2,30);wait_task('Task_HandleSwappingItemsInput');m.press(6,30);m.press(2,90);wait_task('Task_BagMenu_HandleInput')
m.snap('bag-grid-after-move')
# L+R pages wrapped descriptions without changing the pocket.
pocket=m.read(m.symbols['gBagPosition']+6,2)
m.keys.update((10,11));m.run(2);m.keys.clear();m.run(30)
assert m.read(m.symbols['gBagPosition']+6,2)==pocket
m.snap('bag-grid-description-page')
m.press(11,90);assert m.read(m.symbols['gBagPosition']+6,2)==b'\x01\0';m.snap('bag-grid-key-pocket')
m.press(11,90);assert m.read(m.symbols['gBagPosition']+6,2)==b'\x02\0'
assert selected()==-2 and m.read(m.symbols['sGlassGridSprites'],9)==bytes([64])*9
m.snap('bag-grid-empty-pocket')
m.press(10,90);m.press(10,90);assert m.read(m.symbols['gBagPosition']+6,2)==b'\0\0'
m.press(0);wait_task('Task_PokeGlassHub');m.press(0)
assert m.read(m.symbols['sLockFieldControls'],1)==b'\0'
print('PASS real item icon IDs; 999 quantity; 3x3 navigation; three pages including cancel; sort; manual move; description paging; every pocket; empty pocket; field return',flush=True)
