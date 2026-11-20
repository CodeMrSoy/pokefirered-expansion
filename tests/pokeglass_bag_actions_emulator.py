"""Regular Bag actions and nested cases within the tablet session."""
import pathlib,struct
setup=pathlib.Path(__file__).with_name('avatar_wardrobe_emulator.py')
exec(compile(setup.read_text().split("fixture = b'\\x23'")[0],str(setup),'exec'))
fixture=b'\x23'+struct.pack('<I',(m.symbols['ScrCmd_givegiftmon']|1)+0x2000000)+struct.pack('<BBHHI',0,6,1,25,0)
fixture+=b'\x29'+struct.pack('<H',0x829)
for item,quantity in [(717,1),(706,1),(28,3),(715,1),(716,1),(831,1),(582,2),(520,3)]:fixture+=b'\x44'+struct.pack('<HH',item,quantity)
m.inject(fixture+b'\x02')
berry_name=m.read(native('GetItemName',520),32).split(b'\xff')[0]
party=m.symbols['gPlayerParty'];maxhp=struct.unpack('<H',m.read(party+88,2))[0]
scratch=m.symbols['gDecompressionBuffer']+0x2000;m.write(scratch,struct.pack('<I',maxhp-25));native('SetMonData',party,10,scratch)
def stacks(pocket):
 record=m.symbols['gBagPockets']+pocket*8;pointer=struct.unpack('<I',m.read(record,4))[0];count=m.read(record+4,1)[0]
 return [struct.unpack('<HH',m.read(pointer+i*4,4)) for i in range(count)]
def quantity(pocket,item):return sum(q for i,q in stacks(pocket) if i==item)
def select(item,action=0):
 pocket=struct.unpack('<H',m.read(m.symbols['gBagPosition']+6,2))[0]
 target=next(i for i,(id,q) in enumerate(stacks(pocket)) if id==item and q)
 for _ in range(50):
  base=m.symbols['gBagPosition'];row=struct.unpack('<H',m.read(base+8+pocket*2,2))[0];scroll=struct.unpack('<H',m.read(base+14+pocket*2,2))[0]
  if row+scroll==target:break
  m.press(7 if row+scroll<target else 6,25)
 else:raise AssertionError(('Bag selection failed',item,target,row,scroll))
 m.press(8);wait_task('Task_ItemContext_SingleRow');m.run(30)
 for _ in range(action):m.press(5,20)
 m.press(8)
def back_to(task):
 for _ in range(8):
  if task_active(task):m.run(50);return
  m.press(0,90)
 wait_task(task)
def bezel():
 m.run(60);r,g,b=m.screen.getpixel((3,40));assert r>150 and g<110 and b<110,('Missing red tablet bezel',r,g,b)
before=quantity(0,28)
m.press(3);wait_task('Task_PokeGlassHub');m.run(40);m.press(5,30);m.press(7,30);m.press(7,30);m.press(8)
wait_task('Task_BagMenu_HandleInput');bezel();m.snap('overhaul-bag-items')
select(28);wait_task('Task_HandleChooseMonInput');m.run(60);m.press(8,180);m.press(8,180)
back_to('Task_BagMenu_HandleInput');bezel()
assert struct.unpack('<H',m.read(party+86,2))[0]==maxhp-5
assert quantity(0,28)==before-1
select(28,2);wait_task('Task_ChooseHowManyToToss');m.press(8);m.snap('overhaul-bag-toss-confirm');m.press(8);wait_task('Task_RemoveItemFromBag');m.press(8)
wait_task('Task_BagMenu_HandleInput');assert quantity(0,28)==1
select(28,1);wait_task('Task_HandleChooseMonInput');m.press(8);m.press(8);back_to('Task_BagMenu_HandleInput')
assert quantity(0,28)==0, 'Giving the last item must remove its cell'
m.snap('overhaul-bag-after-last-item')
m.press(11,90);wait_task('Task_BagMenu_HandleInput')
assert struct.unpack('<H',m.read(m.symbols['gBagPosition']+6,2))[0]==1
m.snap('overhaul-bag-key-items')
select(706,1);wait_task('Task_RegisterDirection');m.snap('overhaul-bag-register');m.press(7);wait_task('Task_BagMenu_HandleInput')
select(715);wait_task('Task_HandleListInput');bezel();m.snap('overhaul-tm-case');m.press(0,180);wait_task('Task_BagMenu_HandleInput')
assert quantity(3,582)==2
select(716);wait_task('Task_BerryPouchMain');bezel();name_buffer=struct.unpack('<I',m.read(m.symbols['sListMenuStrbuf'],4))[0];assert berry_name in m.read(name_buffer,27),'Berry list names read the wrong pocket';m.snap('overhaul-berry-pouch');m.press(0,180);wait_task('Task_BagMenu_HandleInput')
assert quantity(4,520)==3
select(831);wait_task('Task_FieldItemCase');m.run(50);m.snap('overhaul-field-item-case');m.press(0,180);wait_task('Task_BagMenu_HandleInput')
m.press(0,180);wait_task('Task_PokeGlassHub');m.press(0)
assert m.read(m.symbols['sLockFieldControls'],1)==b'\x00'
assert native('GetMonData3',party,19,0)==28
assert struct.unpack('<H',m.read(native('RegisteredItemAt',1),2))[0]==706
print('PASS toss, give last item, register direction; native Potion healing/consumption, pocket switching, framed TM and Berry cases, retained Field Item Case and unlocked launcher return',flush=True)
