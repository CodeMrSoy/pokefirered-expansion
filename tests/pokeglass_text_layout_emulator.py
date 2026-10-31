"""Pixel-level text/border clearance and full menu-state visual audit."""
import pathlib,struct,json
import numpy as np
setup=pathlib.Path(__file__).with_name('avatar_wardrobe_emulator.py')
exec(compile(setup.read_text().split("fixture = b'\\x23'")[0],str(setup),'exec'))
fixture=b''
for species,level in [(1,100),(25,100),(143,100),(133,100),(4,100),(7,100)]:
 fixture+=b'\x23'+struct.pack('<I',(m.symbols['ScrCmd_createmon']|1)+0x2000000)+struct.pack('<BBHHI',0,6,species,level,0)
fixture+=b'\x29'+struct.pack('<H',0x829)
for item,q in [(717,1),(28,3),(715,1),(716,1),(831,1),(582,2),(520,3),(188,1)]:fixture+=b'\x44'+struct.pack('<HH',item,q)
m.inject(fixture+b'\x02')
for species in [1,4,7,25,133,143,1025]:native('GetSetPokedexFlag',species,3)
# Max-length wide nickname and box name expose headings that otherwise look safe.
scratch=m.symbols['gDecompressionBuffer']+0x1000
m.write(scratch,b'\xd1'*12+b'\xff');native('SetMonData',m.symbols['gPlayerParty'],16,scratch)
m.write(scratch,struct.pack('<H',100));native('SetMonData',m.symbols['gPlayerParty']+100,20,scratch)
box=struct.unpack('<I',m.read(m.symbols['gPokemonStoragePtr'],4))[0]
for i in range(30):m.write(box+4+i*80,m.read(m.symbols['gPlayerParty']+(i%6)*100,80))
injected_native=native
def native(name,*args):
 context=m.read(m.symbols['sGlobalScriptContext'],116);status=m.read(m.symbols['sGlobalScriptContextStatus'],1);inject=m.inject
 def suspended(script):inject(script[:-2]+b'\x27' if script.endswith(b'\x6b\x02') else script)
 m.inject=suspended
 try:result=injected_native(name,*args)
 finally:m.inject=inject
 m.write(m.symbols['sGlobalScriptContext'],context);m.write(m.symbols['sGlobalScriptContextStatus'],status)
 return result
size=m.lib.retro_serialize_size()
def save():
 state=c.create_string_buffer(size);assert m.lib.retro_serialize(state,size);return state
def restore(state):assert m.lib.retro_unserialize(state,size)
labels=[]
def capture(label):
 m.run(60);m.snap('text-audit-'+label);labels.append(label)
def pixels():
 wid=m.read(m.symbols['sHubWindow'],1)[0];win=m.read(m.symbols['gWindows']+wid*12,12);ptr=struct.unpack_from('<I',win,8)[0];raw=m.read(ptr,19200)
 return np.array([[(raw[((y//8)*30+x//8)*32+(y%8)*4+x%8//2]>>((x%2)*4))&15 for x in range(240)] for y in range(160)])
def border(x,y,w,h):
 a=pixels();assert np.all(a[y,x:x+w]==6),('text crosses top border',x,y)
 assert np.all(a[y+h-1,x:x+w]==6),('text crosses bottom border',x,y+h-1)
 assert np.all(a[y:y+h,x]==6) and np.all(a[y:y+h,x+w-1]==6),('text crosses side border',x,y)
m.press(3);wait_task('Task_PokeGlassHub');m.run(80);base=save();capture('launcher-one')
paths={0:[],1:[7],2:[7,7],3:[5,7],4:[5],5:[5,7,7],6:[6,5,6],7:[5,6],8:[6,5],9:[6,6]}
def open_app(app,task):
 restore(base)
 for key in paths[app]:m.press(key,30)
 m.press(8);wait_task(task);m.run(100)
open_app(0,'Task_PokeGlassPokedex');capture('dex-list');border(16,41,118,81)
m.press(3,30);capture('dex-caught');border(16,41,118,81)
m.press(2,30);capture('dex-alphabetical');border(16,41,118,81)
m.press(8,60);capture('dex-entry');assert np.all(pixels()[97,18:224]==6)
m.press(8,60);capture('dex-habitats')
open_app(3,'Task_PokeGlassStats')
for view in range(3):
 capture(['stats','profile','training'][view]);border(90,32,134,76 if view==1 else 84)
 if view==0:assert np.all(pixels()[45,92:222]==6),'Stats header touches separator'
 m.press(2,30)
# Exercise the actual font renderer with strings wider than any data field.
wid=m.read(m.symbols['sHubWindow'],1)[0];scratch=m.symbols['gDecompressionBuffer']+0x1000
for x,y,width in [(46,43,78),(98,80,126),(76,109,148),(80,14,84),(88,31,119)]:
 native('FillWindowPixelBuffer',wid,0);m.write(scratch,b'\xd1'*80+b'\xff');native('StatsTextFit',x,y,width,scratch)
 a=pixels();ys,xs=np.where(a==8);assert len(xs) and min(xs)>=x and max(xs)<x+width,(x,width,min(xs),max(xs))
 assert min(ys)>=y and max(ys)<y+12
open_app(2,'Task_PokeGlassStorage');capture('pc-grid');pc=save()
def pcdata(index):
 tasks=m.read(m.symbols['gTasks'],640);i=next(i for i in range(16) if tasks[i*40+4] and struct.unpack_from('<I',tasks,i*40)[0]==(m.symbols['Task_PokeGlassStorage']|1))
 return struct.unpack_from('<h',tasks,i*40+8+index*2)[0]
m.press(3,30);assert pcdata(9)==3;capture('pc-inspect')
restore(pc);m.press(2,30);assert pcdata(9)==1,(pcdata(9),pcdata(7),pcdata(2),native('GlassBagItem',0));capture('pc-give-item')
restore(pc);m.press(8,30);assert pcdata(6)==1;capture('pc-moving');m.press(2,30);assert pcdata(9)==2;capture('pc-release')
restore(pc)
for i in range(6):capture('pc-box-'+str(i+1));m.press(11,30)
open_app(1,'Task_HandleChooseMonInput');capture('party');cancel_before=np.asarray(m.screen)[120:136,176:216].copy();m.press(8,60);capture('party-actions')
ranges=[]
for i in range(32):
 w=m.read(m.symbols['gWindows']+i*12,12)
 if struct.unpack_from('<I',w,8)[0] and w[0] in (0,2):
  start=struct.unpack_from('<H',w,6)[0];end=start+w[3]*w[4]
  for other,a,b in ranges:assert end<=a or start>=b,('Party windows share character tiles',i,other,start,end,a,b)
  ranges.append((i,start,end))
actions=save()
# Check what is actually displayed, including the font below the popup edge.
assert np.count_nonzero(np.all(np.asarray(m.screen)[128:136,176:216]>150,axis=2)) == 0,'Cancel glyphs remain under the popup'
m.press(0,60);wait_task('Task_HandleChooseMonInput');capture('party-cancel-restored')
assert np.array_equal(np.asarray(m.screen)[120:136,176:216],cancel_before),'Visible Cancel button did not return'
restore(actions)
m.press(5,30);m.press(5,30);m.press(8,60);capture('party-item-actions')
restore(actions);m.press(5,30);m.press(8,60);capture('party-switch-selection')
restore(actions);m.press(8);wait_task('Task_InputHandler_Info');capture('summary-info');m.press(7,120);capture('summary-moves');m.press(8,90);capture('summary-move-details')
open_app(1,'Task_HandleChooseMonInput');m.press(7,30);m.press(8,60);capture('party-field-actions');m.press(5,30);capture('party-field-description');m.press(4,30);capture('party-field-prompt-restored')
open_app(9,'Task_PokeGlassFieldKit');capture('field-kit');m.press(8,30);capture('field-kit-locked')
for i in range(1,7):m.press(5,30);capture('field-kit-'+str(i))
open_app(6,'Task_TrainerCard');capture('trainer-card-front');m.press(8,180);capture('trainer-card-back');m.press(8,180);capture('trainer-card-records')
open_app(7,'Task_OptionMenu')
for i in range(7):capture('options-'+str(i));m.press(5,30)
open_app(8,'task50_save_game');capture('save-confirm')
restore(base);m.press(6,30);capture('launcher-two')
(m.d/'text-audit-pages.json').write_text(json.dumps(labels,indent=2))
print('PASS border pixels intact on Dex and all Stats pages; bounded real-font stress strings; captured',len(labels),'menu/page states',flush=True)
