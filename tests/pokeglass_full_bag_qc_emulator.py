"""Fill actual pocket capacities, traverse all cells, sort, reorder and toss."""
import pathlib,struct
setup=pathlib.Path(__file__).with_name('avatar_wardrobe_emulator.py')
exec(compile(setup.read_text().split("fixture = b'\\x23'")[0],str(setup),'exec'))
fixture=b'\x23'+struct.pack('<I',(m.symbols['ScrCmd_givegiftmon']|1)+0x2000000)+struct.pack('<BBHHI',0,6,1,25,0)
fixture+=b'\x29'+struct.pack('<H',0x829)
# Seed the real containers before filling every pocket through the item API.
for item in [717,715,716,831,706]:fixture+=b'\x44'+struct.pack('<HH',item,1)
rom=(m.root/'pokefirered.gba').read_bytes()
count=int((m.root/'include/constants/items.h').read_text().split('#define ITEMS_COUNT ')[1].splitlines()[0])
for item in range(1,count):
 pocket=rom[m.symbols['gItemsInfo']-0x08000000+item*80+65]
 if pocket<=2 and item not in range(682,689):fixture+=b'\x44'+struct.pack('<HH',item,999 if pocket!=1 else 1)
m.inject(fixture+b'\x02')
def stacks(pocket):
 record=m.symbols['gBagPockets']+pocket*8
 addr=struct.unpack('<I',m.read(record,4))[0];capacity=m.read(record+4,1)[0]
 return [(struct.unpack('<H',m.read(addr+i*4,2))[0]) for i in range(capacity)]
def stack_values(pocket):
 record=m.symbols['gBagPockets']+pocket*8
 addr=struct.unpack('<I',m.read(record,4))[0];capacity=m.read(record+4,1)[0]
 return [struct.unpack('<HH',m.read(addr+i*4,4)) for i in range(capacity)]
def selected():return struct.unpack('<i',m.read(m.symbols['sGlassGridSelection'],4))[0]
def window_ranges():
 intervals=[]
 for i in range(32):
  w=m.read(m.symbols['gWindows']+i*12,12)
  if w[0]!=0 or not struct.unpack_from('<I',w,8)[0]:continue
  start=struct.unpack_from('<H',w,6)[0];end=start+w[3]*w[4]
  assert end<=0x370,('Window overwrites shell graphics',i,start,end)
  for other,a,b in intervals:assert end<=a or start>=b,('Overlapping window tiles',i,other,start,end,a,b)
  intervals.append((i,start,end))
for pocket,capacity in [(0,42),(1,30),(2,27)]:
 assert len(stacks(pocket))==capacity and all(stacks(pocket)),('Pocket fixture not full',pocket,stacks(pocket))
m.write(m.symbols['sHubCursor'],b'\x05');m.press(3);wait_task('Task_PokeGlassHub');m.press(8);wait_task('Task_BagMenu_HandleInput');m.run(60)
for pocket,capacity in [(0,42),(1,30),(2,27)]:
 assert selected()==0,(pocket,selected())
 for index in range(capacity):
  assert selected()==index,(pocket,index,selected())
  window_ranges()
  m.press(7,12)
 assert selected()==-2,('Last cell must be Back',pocket,selected())
 m.snap('qc-full-pocket-'+str(pocket))
 m.press(7,20);assert selected()==-2,'Right of Back must stop'
 for _ in range(capacity):m.press(6,12)
 assert selected()==0
 m.press(6,20);m.press(4,20);assert selected()==0,'Left/Up of first cell must stop'
 if pocket<2:m.press(11,90)
# Return to Items; sorting and reordering must preserve every stack.
m.press(10,90);m.press(10,90)
before=sorted(stacks(0));values=sorted(stack_values(0));m.press(3,30);wait_task('Task_ItemContext_SingleRow');window_ranges();m.press(8,90);wait_task('Task_BagMenu_HandleInput')
assert sorted(stacks(0))==before,'Sort changed inventory'
for _ in range(43):m.press(6,8)
m.press(2,30);wait_task('Task_HandleSwappingItemsInput');m.press(5,20);m.press(5,20);m.press(2,90);wait_task('Task_BagMenu_HandleInput')
assert sorted(stacks(0))==before,'Sort/reorder changed inventory'
assert sorted(stack_values(0))==values,'Reorder changed item quantities'
assert selected()==5,('Downward move did not retain its moved item',selected())
# Upward move and cancel across pages preserve every item and a valid cursor.
m.press(2,30);wait_task('Task_HandleSwappingItemsInput')
for _ in range(5):m.press(6,20)
m.press(2,90);wait_task('Task_BagMenu_HandleInput')
assert selected()==0 and sorted(stacks(0))==before and sorted(stack_values(0))==values
m.press(2,30);wait_task('Task_HandleSwappingItemsInput')
for _ in range(16):m.press(7,12)
m.press(0,90);wait_task('Task_BagMenu_HandleInput')
assert selected()==16 and sorted(stacks(0))==before and sorted(stack_values(0))==values
m.press(2,30);wait_task('Task_HandleSwappingItemsInput')
for _ in range(43):m.press(7,8)
m.press(8,90);wait_task('Task_BagMenu_HandleInput')
assert selected()==41 and sorted(stacks(0))==before and sorted(stack_values(0))==values

# Toss one item from a full pocket using the actual context/quantity/Yes menu.
m.press(8,30);wait_task('Task_ItemContext_SingleRow');window_ranges();m.press(5,20);m.press(5,20);m.press(8,30)
wait_task('Task_ChooseHowManyToToss');window_ranges();m.press(8,30);window_ranges();m.snap('qc-full-bag-toss-confirm')
m.press(8,60);wait_task('Task_RemoveItemFromBag');m.press(8,90);wait_task('Task_BagMenu_HandleInput');window_ranges()
m.snap('qc-full-bag-after-toss');m.press(0);wait_task('Task_PokeGlassHub');m.press(0)
assert m.read(m.symbols['sLockFieldControls'],1)==b'\0'
print('PASS full 42/30/27 stack pockets; every grid cell/Back/boundary; sorting/reordering; native toss; live window ranges; field controls restored',flush=True)
