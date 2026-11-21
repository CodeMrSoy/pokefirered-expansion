"""Audit every compiled Bag-grid item using actual GBA text rendering.

TM, Berry and Field Item Case descriptions use their existing separate UIs.
"""
import pathlib,struct,json,subprocess
setup=pathlib.Path(__file__).with_name('avatar_wardrobe_emulator.py')
exec(compile(setup.read_text().split("fixture = b'\\x23'")[0],str(setup),'exec'))
fixture=b'\x23'+struct.pack('<I',(m.symbols['ScrCmd_givegiftmon']|1)+0x2000000)+struct.pack('<BBHHI',0,6,1,25,0)
fixture+=b'\x29'+struct.pack('<H',0x829)
for item,q in [(717,1),(28,3),(422,1),(423,1),(831,1),(3,20)]:fixture+=b'\x44'+struct.pack('<HH',item,q)
m.inject(fixture+b'\x02')
field_tools={native('FieldTool_GetItem',move) for move in range(16)}-{0}
m.write(m.symbols['sHubCursor'],b'\x05');m.press(3);wait_task('Task_PokeGlassHub');m.press(8);wait_task('Task_BagMenu_HandleInput');m.run(60)
rom=(m.root/'pokefirered.gba').read_bytes()
def readrom(addr,n):return rom[addr-0x08000000:addr-0x08000000+n]
def uncompress(addr):
 data=readrom(addr,2048);assert data[0]==0x10
 size=int.from_bytes(data[1:4],'little');out=bytearray();i=4
 while len(out)<size:
  flags=data[i];i+=1
  for bit in range(7,-1,-1):
   if flags&(1<<bit):
    a,b=data[i:i+2];i+=2;length=(a>>4)+3;distance=((a&15)<<8|b)+1
    for _ in range(length):out.append(out[-distance])
   else:out.append(data[i]);i+=1
   if len(out)>=size:break
 return out[:size]
def check_icons():
 sprites=m.read(m.symbols['sGlassGridSprites'],9)
 items=struct.unpack('<9H',m.read(m.symbols['sGlassGridItems'],18))
 for sprite,item in zip(sprites,items):
  if not item:continue
  record=m.read(m.symbols['gSprites']+sprite*68,8)
  tile=struct.unpack_from('<H',record,4)[0]&1023
  pic=struct.unpack('<I',readrom(m.symbols['gItemsInfo']+item*80+72,4))[0]
  original=uncompress(pic);expected=bytearray(512)
  for row in range(3):expected[row*128:row*128+96]=original[row*96:row*96+96]
  assert m.read(0x06010000+tile*32,512)==expected,('Stale item graphic',item,sprite)
check_icons()
m.snap('bag-description-potion')
m.press(7,30);m.snap('bag-description-power-lens');m.press(7,30);m.snap('bag-description-power-band')
m.press(11,90);check_icons();m.snap('bag-description-pokeglass');m.press(11,90);check_icons();m.snap('bag-description-ultra-ball')
# A reusable RAM trampoline avoids recompiling and waiting 180 frames per item.
address=m.symbols['gDecompressionBuffer']+0x3000
args=address+0x800;result=args+8
asm=['.syntax unified','.thumb','.thumb_func','_start:','push {r4,lr}',
     'ldr r4,args','ldr r0,[r4]','ldr r1,[r4,#4]','movs r2,#0',
     'ldr r3,function','bl invoke','str r0,[r4,#8]','movs r0,#1',
     'pop {r4,pc}','invoke:','bx r3','.align 2',f'args: .word {args}',
     f'function: .word {m.symbols["PokeGlassPrintBagDescription"]|1}']
(native_dir/'description-audit.s').write_text('\n'.join(asm)+'\n')
subprocess.run([tool_prefix+'as','-mthumb','-mcpu=arm7tdmi','-o',str(native_dir/'description-audit.o'),str(native_dir/'description-audit.s')],check=True)
subprocess.run([tool_prefix+'objcopy','-O','binary','-j','.text',str(native_dir/'description-audit.o'),str(native_dir/'description-audit.bin')],check=True)
m.write(address,(native_dir/'description-audit.bin').read_bytes())
tasks=m.symbols['gTasks']
original=m.symbols['Task_BagMenu_HandleInput']|1
slot=next(i for i in range(16) if m.read(tasks+i*40+4,1)!=b'\0' and struct.unpack('<I',m.read(tasks+i*40,4))[0]==original)
callback=tasks+slot*40
window=m.read(m.symbols['gWindows']+12,12);width=window[3]*8;height=window[4]*8
buffer=struct.unpack_from('<I',window,8)[0];assert (width,height)==(88,40)
rom=(m.root/'pokefirered.gba').read_bytes()
def word(addr):return struct.unpack_from('<I',rom,addr-0x08000000)[0]
def string(addr):return rom[addr-0x08000000:addr-0x08000000+512].split(b'\xff')[0]
count=int((m.root/'include/constants/items.h').read_text().split('#define ITEMS_COUNT ')[1].splitlines()[0])
records=[]
for item in range(count):
 row=m.symbols['gItemsInfo']+item*80
 pocket=rom[row-0x08000000+65]
 if pocket>2 or item in field_tools:continue
 raw=string(word(row+12));assert len(raw)<511
 m.write(buffer,bytes(width*height//2))
 m.write(args,struct.pack('<III',1,item,0xffffffff))
 m.write(callback,struct.pack('<I',address|1))
 for _ in range(120):
  m.run(1)
  pages=struct.unpack('<I',m.read(result,4))[0]
  if pages!=0xffffffff:break
 else:raise AssertionError(('Renderer did not finish',item))
 m.write(callback,struct.pack('<I',original))
 assert pages==1,('Description needs another page',item,pages)
 pixels=m.read(buffer,width*height//2)
 def pixel(x,y):return pixels[((y//8)*(width//8)+x//8)*32+(y%8)*4+x%8//2]>>((x&1)*4)&15
 assert all(pixel(x,0)==0 and pixel(x,height-1)==0 for x in range(width)),('Text reaches horizontal border',item)
 assert all(pixel(0,y)==0 and pixel(width-1,y)==0 for y in range(height)),('Text reaches vertical border',item)
 assert 8 in [pixel(x,y) for y in range(height) for x in range(width)],('Missing description',item)
 records.append({'item':item,'pages':pages,'border_clear':True})
 if len(records)%100==0:print('Audited',len(records),'Bag item descriptions',flush=True)
(m.d/'bag-description-audit.json').write_text(json.dumps({'items_count':count,'bag_items_checked':len(records),'case_items_excluded':count-len(records),'results':records},indent=2))
assert len(records)==656
print('PASS all 656 compiled Bag-grid item descriptions fit one page with all four border gutters clear; 176 case-only entries retain their separate interfaces',flush=True)
