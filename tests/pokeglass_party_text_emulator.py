#!/usr/bin/env python3
"""Check digit growth, HP updates, and the real candy/stat-window path."""
import struct,subprocess,os,re
import numpy as np
import quantum_qol_emulator as m
fixture=b''
for species,level in ((1,9),(113,99),(25,25),(143,100),(4,9),(7,99)):
 fixture+=b'\x23'+struct.pack('<I',(m.symbols['ScrCmd_createmon']|1)+0x2000000)+struct.pack('<BBHHI',0,6,species,level,0)
fixture+=b'\x44'+struct.pack('<HH',717,1)+b'\x44'+struct.pack('<HH',102,5)
m.inject(fixture+b'\x02');m.press(3);m.press(7);m.press(8)
root=m.root;call_dir=m.d/'party-text-native';call_dir.mkdir(exist_ok=True)
address=m.symbols['gDecompressionBuffer']+0x3000;result=address+0x800;value_addr=address+0x900
prefix=os.environ.get('ARM_NM','arm-none-eabi-nm').removesuffix('nm')
fields=re.findall(r'^\s*(MON_DATA_\w+)\s*,', (root/'include/pokemon.h').read_text().split('// Property labels')[1].split('};')[0],re.M)
fields={name:i for i,name in enumerate(fields)}
def native(name,*args):
 # Temporarily replace the existing input task; restore it before making the
 # call so item handlers can deliberately install their own task continuation.
 tasks=m.read(m.symbols['gTasks'],16*40)
 active=[i for i in range(16) if tasks[i*40+4]]
 task=active[0];task_addr=m.symbols['gTasks']+task*40
 previous=struct.unpack_from('<I',tasks,task*40)[0]
 code=['.syntax unified','.thumb','.thumb_func','_start:','push {r4,lr}',
       'ldr r1, task','ldr r2, previous','str r2,[r1]']
 code += [f'ldr r{i},arg{i}' for i in range(len(args))]
 code += ['ldr r3,function','bl invoke','ldr r3,result','str r0,[r3]','pop {r4,pc}',
          'invoke:','bx r3','.align 2',f'task: .word {task_addr}',f'previous: .word {previous}',
          f'function: .word {m.symbols[name]|1}',f'result: .word {result}']
 code += [f'arg{i}: .word {a}' for i,a in enumerate(args)]
 (call_dir/'call.s').write_text('\n'.join(code)+'\n')
 subprocess.run([prefix+'as','-mthumb','-mcpu=arm7tdmi','-o',str(call_dir/'call.o'),str(call_dir/'call.s')],check=True)
 subprocess.run([prefix+'objcopy','-O','binary','-j','.text',str(call_dir/'call.o'),str(call_dir/'call.bin')],check=True)
 m.write(address,(call_dir/'call.bin').read_bytes());m.write(task_addr,struct.pack('<I',address|1));m.run(100)
 return struct.unpack('<I',m.read(result,4))[0]
def setfield(slot,field,value):
 m.write(value_addr,struct.pack('<I',value));native('SetMonData',m.symbols['gPlayerParty']+slot*100,fields[field],value_addr)
def pixels(slot):
 boxes=struct.unpack('<I',m.read(m.symbols['sPartyMenuBoxes'],4))[0]
 win=m.read(boxes+slot*16+8,1)[0]
 # GetWindowAttribute TILE_DATA is 7 in this engine.
 ptr=native('GetWindowAttribute',win,7)
 return m.read(ptr,96*32//2)
def refresh(slot):native('DisplayPartyPokemonDataForPokeGlass',slot)
def canonical(slot):native('RenderPartyMenuBox',slot);return pixels(slot)
original_first=m.read(m.symbols['gPlayerParty'],100)
for slot,level,maxhp in ((0,10,100),(1,100,714)):
 setfield(slot,'MON_DATA_LEVEL',level);setfield(slot,'MON_DATA_MAX_HP',maxhp);setfield(slot,'MON_DATA_HP',maxhp)
 refresh(slot);updated=pixels(slot);fresh=canonical(slot)
 assert updated==fresh,('Level-up redraw differs from fresh card',slot)
 m.snap('party-text-level-'+str(level))
 for hp in (maxhp,maxhp//2,maxhp//5,1,0,maxhp):
  setfield(slot,'MON_DATA_HP',hp)
  boxes=struct.unpack('<I',m.read(m.symbols['sPartyMenuBoxes'],4))[0]
  native('DisplayPartyPokemonHPCheck.part.0',m.symbols['gPlayerParty']+slot*100,boxes+slot*16,1)
  native('DisplayPartyPokemonHPBarCheck',m.symbols['gPlayerParty']+slot*100,boxes+slot*16)
  updated=pixels(slot);fresh=canonical(slot)

  def decode(raw):
   a=np.zeros((32,96),dtype=np.uint8)
   for y in range(32):
    for x in range(96):
     pos=(y//8*12+x//8)*32+(y%8)*4+(x%8)//2
     a[y,x]=(raw[pos]>>((x%2)*4))&15
   return a
  aa,bb=decode(updated),decode(fresh)
  # Status/level text changes separately when a Pokémon faints or revives.
  # The HP redraw must always match a fresh card in both HP regions.
  assert np.array_equal(aa[14:18,30:94],bb[14:18,30:94]),('HP track',slot,hp)
  assert np.array_equal(aa[18:30,56:94],bb[18:30,56:94]),('HP numbers',slot,hp)
 m.snap('party-text-HP-'+str(maxhp))
# Long nicknames must fit before the gender symbol.
before_name=decode(canonical(2))
encoded=bytes([0xd1])*12+b'\xff' # W in the FireRed character map.
m.write(value_addr,encoded);native('SetMonData',m.symbols['gPlayerParty']+200,fields['MON_DATA_NICKNAME'],value_addr)
native('RenderPartyMenuBox',2);m.snap('party-text-long-nickname')
after_name=decode(pixels(2))
assert np.array_equal(before_name[1:12,85:94], after_name[1:12,85:94]), 'Nickname overwrote gender column'
# Genuine item-use animation and two-page stat popup at the 9 -> 10 boundary.
setfield(0,'MON_DATA_LEVEL',9)
# Reset EXP consistently through a fresh copy of a level-nine party member.
m.write(m.symbols['gPlayerParty'],original_first)
refresh(0)
m.write(m.symbols['gSpecialVar_ItemId'],struct.pack('<H',102))
tasks=m.read(m.symbols['gTasks'],16*40);task=next(i for i in range(16) if tasks[i*40+4])
native('ItemUseCB_RareCandy',task,m.symbols['Task_ClosePartyMenuAfterText']|1)
m.run(500)
def task_active(name):
 tasks=m.read(m.symbols['gTasks'],16*40)
 return any(tasks[i*40+4] and struct.unpack_from('<I',tasks,i*40)[0]==(m.symbols[name]|1) for i in range(16))
for _ in range(30):
 if task_active('Task_DisplayLevelUpStatsPg1'):break
 m.press(8,120)
assert task_active('Task_DisplayLevelUpStatsPg1'),'Did not return from the item animation to the level-up message'
m.run(180);m.snap('party-text-actual-level-up')
assert native('GetMonData3',m.symbols['gPlayerParty'],fields['MON_DATA_LEVEL'],0)==10
updated=pixels(0);fresh=canonical(0)
assert updated==fresh,'Actual candy level-up left stale card text'
m.press(8);m.snap('party-text-stat-gains');m.press(8);m.snap('party-text-stat-totals')
print('Digit growth, HP thresholds/healing, long names, actual candy level-up and stat pages checked')
