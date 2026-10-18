#!/usr/bin/env python3
"""Run old encrypted Pokémon through migration, storage recovery and flash reload."""
import pathlib,struct,subprocess,os,re
import quantum_qol_emulator as m
prefix=os.environ['ARM_NM'].removesuffix('nm');d=m.d/'cleanup-migration';d.mkdir(exist_ok=True)
addr=m.symbols['gDecompressionBuffer']+0x3000;result=addr+0xf00

def native(name,*args):
 lines=['.syntax unified','.thumb','.thumb_func','_start:','push {r4,lr}']
 lines += [f'ldr r{i},arg{i}' for i in range(len(args))]
 lines += ['ldr r3,function','bl invoke','ldr r3,result','str r0,[r3]','movs r0,#1','pop {r4,pc}','invoke:','bx r3','.align 2',f'function: .word {m.symbols[name]|1}',f'result: .word {result}']
 lines += [f'arg{i}: .word {v}' for i,v in enumerate(args)]
 (d/'call.s').write_text('\n'.join(lines)+'\n')
 subprocess.run([prefix+'as','-mthumb','-mcpu=arm7tdmi','-o',str(d/'call.o'),str(d/'call.s')],check=True)
 subprocess.run([prefix+'objcopy','-O','binary','-j','.text',str(d/'call.o'),str(d/'call.bin')],check=True)
 m.write(addr,(d/'call.bin').read_bytes());m.inject(b'\x23'+struct.pack('<I',addr|1)+b'\x6b\x02')
 for _ in range(40):
  if m.read(m.symbols['sGlobalScriptContextStatus'],1)==b'\x02':break
  m.run(60)
 return struct.unpack('<I',m.read(result,4))[0]

def ptr(name):return struct.unpack('<I',m.read(m.symbols[name],4))[0]
defs=dict(re.findall(r'^#define\s+(SPECIES_\w+)\s+(\w+)',pathlib.Path('include/constants/species.h').read_text(),re.M))
def species(n):
 while not n.isdigit():n=defs[n]
 return int(n)
old=(m.root/'tests/fixtures/rom_cleanup_old_form_party.bin').read_bytes()
party=m.symbols['gPlayerParty'];box=ptr('gPokemonStoragePtr');save=ptr('gSaveBlock1Ptr')
m.write(party,old);m.write(m.symbols['gPlayerPartyCount'],b'\x06')
m.write(box+4,old[0:80])
# Fusion storage follows boxes, names and wallpapers, aligned to four bytes.
fusion=box+4+14*30*80+14*9+14
fusion=(fusion+3)&~3
m.write(fusion,old[100:200])
native('QuantumMigrateLoadedPokemon')
expected=['CHARIZARD','NECROZMA','CALYREX','PIKACHU','FURFROU_NATURAL','UNOWN']
# MON_DATA_SPECIES is 18 in the stable BoxPokemon data API.
for i,n in enumerate(expected):
 assert native('GetMonData3',party+i*100,18,0)==species('SPECIES_'+n),(i,n)
 assert m.read(party+i*100,8)==old[i*100:i*100+8],'Personality/OT changed'
assert native('GetBoxMonData3',box+4,18,0)==species('SPECIES_CHARIZARD')
after=m.read(party,600);native('QuantumMigrateLoadedPokemon');assert m.read(party,600)==after
# Saved followers and recap sprites can still contain a retired graphics ID.
for old_name,new_name in [('UNOWN_B','UNOWN'),('FURFROU_HEART','FURFROU_NATURAL')]:
 for flags in (1<<14,(1<<14)|(1<<13),(1<<14)|(1<<12)):
  assert native('GetObjectEventGraphicsInfo',species('SPECIES_'+old_name)|flags)==native('GetObjectEventGraphicsInfo',species('SPECIES_'+new_name)|flags)
native('AddPCItem',13,3) # Potion
before=native('CountTotalItemQuantityInBag',13)
# A full storage must retain the hidden partner until a slot is available.
m.write(box+4,m.read(box+4,80)*(14*30))
hidden=m.read(fusion,100)
native('QuantumRecoverStoredItemsAndPokemon')
assert m.read(fusion,100)==hidden, 'Full boxes discarded the fusion partner'
m.write(box+4+80,b'\0'*80)
native('QuantumRecoverStoredItemsAndPokemon')
assert native('CountTotalItemQuantityInBag',13)==before+3
assert native('GetMonData3',fusion,18,0)==0
assert native('GetBoxMonData3',box+4+80,18,0)==species('SPECIES_NECROZMA')
native('QuantumRecoverStoredItemsAndPokemon')
assert native('CountTotalItemQuantityInBag',13)==before+3,'PC recovery duplicated items'
# A retired current location and every saved return warp get a safe destination.
for offset in (4,12,20,28,36):m.write(save+offset,struct.pack('<bbb x hh',1,72,-1,5,5))
native('QuantumMigrateLoadedWorld')
for offset in (4,12,20,28,36):assert m.read(save+offset,3)==bytes((3,0,255))
assert m.read(save,4)==struct.pack('<hh',10,9)
# Persist to actual Flash, reset the core and Continue.
m.inject(b'\x39'+struct.pack('<BBBHH',3,0,255,10,9)+b'\x6b\x02');m.run(180)
box=ptr('gPokemonStoragePtr')
expected_party=m.read(party,600);expected_box=m.read(box+4,14*30*80)
saved=native('TrySavingData',0)
print('Save result',saved,'flash',m.read(m.symbols['gFlashMemoryPresent'],1).hex(),'status',m.read(m.symbols['gSaveAttemptStatus'],1).hex(),flush=True)
assert saved==1
m.lib.retro_reset();m.run(360);m.press(3);m.press(8);m.press(8);m.run(180)
assert m.read(party,600)==expected_party
actual_box=m.read(ptr('gPokemonStoragePtr')+4,14*30*80)
diffs=[(i,a,b) for i,(a,b) in enumerate(zip(expected_box,actual_box)) if a!=b]
print('Box changes',diffs[:20],flush=True)
assert actual_box==expected_box
m.snap('cleanup-migration-continue')
print('Old encrypted forms, party/box/fusion recovery, item recovery idempotence, retired warps, flash reset/Continue passed')
