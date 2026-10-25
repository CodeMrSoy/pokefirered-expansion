"""Sevii nursery: linked door warps, two parents, step-generated egg, collection and withdrawal."""
import os,pathlib,struct,subprocess,json
import havora_emulator_support as m
source=(m.root/'tests/avatar_wardrobe_emulator.py').read_text()
exec(source[source.index('native_dir ='):source.index('avatar_var = native')])
groups=json.loads((m.root/'data/maps/map_groups.json').read_text());ids={n:(g,i) for g,k in enumerate(groups['group_order']) for i,n in enumerate(groups[k])}
def ptr(n):return struct.unpack('<I',m.read(m.symbols[n],4))[0]
def warp(n,x,y):
 g,k=ids[n];m.inject(b'\x39'+struct.pack('<BBBHH',g,k,255,x,y)+b'\x6b\x02');m.run(180)
def mapid():return tuple(m.read(ptr('gSaveBlock1Ptr')+4,2))
def finish():
 for _ in range(30):
  if m.read(m.symbols['sGlobalScriptContextStatus'],1)==b'\x02':break
  m.press(8,45)
 m.run(90)
# A normal exterior step enters the restored 12x9 Four Island interior.
warp('HavoraDaycare',7,15);m.keys.add(4);m.run(24);m.keys.clear();m.run(200)
assert mapid()==ids['QuantumHavoraDaycare'],('Door entrance failed',mapid())
m.snap('daycare-sevii-interior')
m.keys.add(5);m.run(60);m.keys.clear();m.run(200)
assert mapid()==ids['HavoraDaycare'],('Return warp failed',mapid())
# Bulbasaur + Ditto are compatible; a third Pokemon remains in the party.
fixture=b''
for species in [1,132,25]:fixture+=b'\x23'+struct.pack('<I',(m.symbols['ScrCmd_createmon']|1)+0x2000000)+struct.pack('<BBHHI',0,6,species,25,0)
m.inject(fixture+b'\x02')
assert native('GetDaycareState')==0
for expected in [2,3]:
 m.write(m.symbols['gPartyMenu']+10,b'\0');native('StoreSelectedPokemonInDaycare');assert native('GetDaycareState')==expected
assert m.read(m.symbols['gPlayerPartyCount'],1)==b'\x01'
# Run the real step-based breeding function, without forcing a pending egg.
# Call 4096 times in one native trampoline, rather than thousands of script injections.
asm=['.syntax unified','.thumb','.thumb_func','_start:','push {r4,r5,r6,lr}','ldr r4, count','ldr r5, function','loop:','bl invoke','subs r4, #1','bne loop','movs r0, #1','pop {r4,r5,r6,pc}','invoke:','bx r5','.align 2','count: .word 4096',f"function: .word {m.symbols['ShouldEggHatch']|1}"]
p=native_dir/'steps.s';p.write_text('\n'.join(asm)+'\n');subprocess.run(['arm-none-eabi-as','-mthumb','-mcpu=arm7tdmi','-o',str(p.with_suffix('.o')),str(p)],check=True);subprocess.run(['arm-none-eabi-objcopy','-O','binary','-j','.text',str(p.with_suffix('.o')),str(p.with_suffix('.bin'))],check=True)
addr=m.symbols['gDecompressionBuffer']+0x2000;m.write(addr,p.with_suffix('.bin').read_bytes());m.inject(b'\x23'+struct.pack('<I',addr|1)+b'\x02')
assert native('GetDaycareState')==1,'Compatible parents did not produce an egg'
warp('HavoraDaycare',10,16);m.press(4,25);m.press(8,100);m.snap('daycare-egg-offer');m.press(8,120);finish()
assert m.read(m.symbols['gPlayerPartyCount'],1)==b'\x02','Caretaker did not give egg'
assert native('GetDaycareState')==3
# Both parents remain available for the Sevii withdrawal service.
for expected in [2,0]:
 m.write(m.symbols['gSpecialVar_0x8004'],b'\0\0');native('TakePokemonFromDaycare');assert native('GetDaycareState')==expected
assert m.read(m.symbols['gPlayerPartyCount'],1)==b'\x04'
print('PASS real exterior/interior door transitions, two breeding slots, compatible-parent step generation, outdoor egg offer/collection, parents retained and both withdrawals',flush=True)
