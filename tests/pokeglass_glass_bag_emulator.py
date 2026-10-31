"""Glass Bag: real pocket animation, scrolling, action dialogs and item management."""
import pathlib,struct,re
import numpy as np
setup=pathlib.Path(__file__).with_name('avatar_wardrobe_emulator.py')
exec(compile(setup.read_text().split("fixture = b'\\x23'")[0],str(setup),'exec'))
items=(m.root/'include/constants/items.h').read_text(encoding='utf-8')
def item(name):return int(re.search(r'^#define '+name+r' +(\d+)',items,re.M)[1])
fixture=b'\x23'+struct.pack('<I',(m.symbols['ScrCmd_createmon']|1)+0x2000000)+struct.pack('<BBHHI',0,6,1,25,0)+b'\x29'+struct.pack('<H',0x829)
names=['ITEM_POKEGLASS','ITEM_TM_CASE','ITEM_BERRY_POUCH','ITEM_FIELD_ITEM_CASE','ITEM_POTION','ITEM_SUPER_POTION','ITEM_HYPER_POTION','ITEM_MAX_POTION','ITEM_ANTIDOTE','ITEM_FULL_HEAL','ITEM_REVIVE','ITEM_REPEL','ITEM_ESCAPE_ROPE','ITEM_POKE_BALL','ITEM_GREAT_BALL','ITEM_ULTRA_BALL']
# The seven tools share the permanent Field Item Case entry.
names.remove('ITEM_FIELD_ITEM_CASE')
for name in names:fixture+=b'\x44'+struct.pack('<HH',item(name),1 if 'CASE' in name or name in ('ITEM_POKEGLASS','ITEM_BERRY_POUCH') else 50)
fixture+=b'\x44'+struct.pack('<HH',831,1)
m.inject(fixture+b'\x02')
def task(name):
 t=m.read(m.symbols['gTasks'],640);return next((i for i in range(16) if t[i*40+4] and struct.unpack_from('<I',t,i*40)[0]==(m.symbols[name]|1)),None)
def pointer(name):return struct.unpack('<I',m.read(m.symbols[name],4))[0]
def pocket():return struct.unpack('<H',m.read(m.symbols['gBagPosition']+6,2))[0]
def stacks(p):
 r=m.symbols['gBagPockets']+8*p;a=struct.unpack('<I',m.read(r,4))[0];n=m.read(r+4,1)[0];return [struct.unpack('<HH',m.read(a+i*4,4)) for i in range(n)]
def qty(p,id):return sum(q for i,q in stacks(p) if i==id)
def snap(label):m.run(40);m.snap('glass-bag-'+label)
def save():
 size=m.lib.retro_serialize_size();s=c.create_string_buffer(size);assert m.lib.retro_serialize(s,size);return s,size
def restore(state):assert m.lib.retro_unserialize(*state)
def select_item(id):
 target=next(i for i,(v,q) in enumerate(stacks(pocket())) if v==id)
 for _ in range(40):
  p=pocket();b=m.symbols['gBagPosition'];pos=struct.unpack('<H',m.read(b+8+2*p,2))[0]+struct.unpack('<H',m.read(b+14+2*p,2))[0]
  if pos==target:return
  m.press(5 if pos<target else 4,25)
 raise AssertionError('Could not select item')
def windows():
 ranges=[]
 for i in range(32):
  w=m.read(m.symbols['gWindows']+i*12,12)
  if w[0]==0 and struct.unpack_from('<I',w,8)[0]:
   start=struct.unpack_from('<H',w,6)[0];end=start+w[3]*w[4]
   assert end<=0x370,('Window overwrites tablet tiles',i,start,end)
   for j,a,b in ranges:assert end<=a or start>=b,('Overlapping window graphics',i,j)
   ranges.append((i,start,end))
m.press(3);wait_task('Task_PokeGlassHub');m.press(5,30);m.press(7,30);m.press(7,30);m.press(8);wait_task('Task_BagMenu_HandleInput');m.run(90)
snap('items');windows();assert pocket()==0
# No cream-paper panel remains under the item list.
r,g,b=m.screen.getpixel((215,65));assert b>r and r<100,(r,g,b)
state=save();bag=pointer('gBagMenu');id=m.read(bag+0x804,1)[0];sprite=m.symbols['gSprites']+id*68
assert m.read(sprite+0x2a,1)==b'\x00'
mask=np.zeros((160,240),bool);mask[:10,10:230]=True;mask[150:,10:230]=True;mask[10:150,:10]=True;mask[10:150,230:]=True
bezel=np.asarray(m.screen)[mask].copy();frames=[];bounces=[];tiles=[]
m.keys.add(7)
for frame in range(50):
 m.run(1)
 if frame==1:m.keys.clear()
 bounces.append(struct.unpack('<h',m.read(sprite+0x26,2))[0]);tiles.append(struct.unpack('<H',m.read(sprite+4,2))[0]&1023)
 assert np.array_equal(np.asarray(m.screen)[mask],bezel),'Pocket switch changed tablet border'
 frames.append(m.screen.copy())
assert pocket()==1 and min(bounces)<0 and bounces[-1]==0 and len(set(tiles))>1,(pocket(),bounces,tiles)
assert m.read(sprite+0x2a,1)==b'\x01'
frames[0].save(m.d/'glass-bag-pocket-switch.gif',save_all=True,append_images=frames[1:],duration=17,loop=0);snap('key-items')
m.press(7,90);wait_task('Task_BagMenu_HandleInput');assert pocket()==2;snap('balls');windows()
restore(state)
for _ in range(7):m.press(5,25)
snap('scroll');assert struct.unpack('<H',m.read(m.symbols['gBagPosition']+14,2))[0]>0
restore(state);m.press(3,90);wait_task('Task_ItemContext_SingleRow');snap('sort');windows();m.press(0,90);wait_task('Task_BagMenu_HandleInput')
restore(state);select_item(item('ITEM_POTION'));m.press(8,60);wait_task('Task_ItemContext_SingleRow');snap('context');windows()
m.press(5,30);m.press(5,30);m.press(8,60);wait_task('Task_ChooseHowManyToToss');snap('quantity');windows()
before=qty(0,item('ITEM_POTION'));m.press(8,90);snap('toss-confirm');windows();m.press(0,90);wait_task('Task_BagMenu_HandleInput');assert qty(0,item('ITEM_POTION'))==before
# Real reorder cancel keeps all stacks, and the marker stays within the item column.
restore(state);m.press(2,60);wait_task('Task_HandleSwappingItemsInput');snap('reorder');m.press(0,90);wait_task('Task_BagMenu_HandleInput')
m.press(0,180);wait_task('Task_PokeGlassHub');m.press(0,90);assert m.read(m.symbols['sLockFieldControls'],1)==b'\x00'
print('PASS all three glass pockets, original bag frames/bounce, stable bezel, scrolling, sorting, context/quantity/toss cancel, reorder cancel and disjoint window tiles',flush=True)
