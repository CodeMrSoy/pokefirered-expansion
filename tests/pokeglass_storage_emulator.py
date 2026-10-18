#!/usr/bin/env python3
import struct
import numpy as np
import quantum_qol_emulator as m
fixture=b''
for species in (1,4,7,25,133,143):
 fixture+=b'\x23'+struct.pack('<I',(m.symbols['ScrCmd_createmon']|1)+0x2000000)+struct.pack('<BBHHI',0,6,species,25,0)
m.inject(fixture+b'\x02')
# Start directly through the same field special used by the Storage app.
def call(name):
 m.inject(b'\x23'+struct.pack('<I',(m.symbols[name]|1)+0x2000000)+b'\x27\x02')
def state():return m.read(m.symbols['sGlassStorage'], 43)
def party():return m.read(m.symbols['gPlayerParty'],600)
call('ShowPokeGlassStorage')
m.snap('storage-box-first')
assert state()[4:7]==b'\x00\x00\x00',state().hex()
original=party()
# left edge -> Party button -> left panel. Take first party Pokémon.
m.press(6,120); assert state()[1]==36
m.press(8,120); assert state()[1]==30 and state()[4]==1
m.snap('storage-party-panel')
m.press(8,120);assert state()[5]==1
assert party()==original
# Move across left panel to first box slot, then place.
m.press(7,120);m.press(7,120);assert state()[1]==0
m.press(8,120);assert state()[5]==0
assert m.read(m.symbols['gPlayerPartyCount'],1)==b'\x05'
boxptr=struct.unpack('<I',m.read(m.symbols['gPokemonStoragePtr'],4))[0]
# Party size is 100 in this engine; first 80 bytes are the immutable boxed payload.
assert m.read(boxptr+4,80)==original[:80]
m.snap('storage-deposited')
# Pick up, move to Party button via left edge, A opens first party slot, A swaps.
m.press(8,120);m.press(6,120);m.press(6,120);m.press(6,120);assert state()[1]==36
m.snap('storage-holding-party-button')
m.press(8,120);assert state()[1]==30
m.press(8,120);assert state()[5]==0
assert party()[:80]==original[:80]
assert m.read(boxptr+4,80)==original[100:180]
# Cancel after changing boxes must leave both the source and party untouched.
m.press(8,120);before=party(); boxes=m.read(boxptr,4+14*30*80)
m.press(11,120);m.press(0,120)
assert party()==before and m.read(boxptr+4,14*30*80)==boxes[4:]
m.snap('storage-cancelled')
m.press(0);m.press(0)
print('Storage panel, carry, deposit, swap, cross-box cancel and payload integrity passed')
# A full box and party must render every icon without exhausting sprites.
m.write(boxptr,b"\x00")
for i in range(30):m.write(boxptr+4+i*80,original[(i%6)*100:(i%6)*100+80])
m.write(m.symbols['gPlayerParty'],original)
m.write(m.symbols['gPlayerPartyCount'],b'\x06')
call('ShowPokeGlassStorage')
m.press(6,120);m.press(8,120)
assert sum(x<64 for x in state()[7:43])==36
m.snap('storage-full-box-party')
m.press(0,120);m.press(0,120)
# Carrying a boxed Pokémon onto Party opens the left panel automatically.
call('ShowPokeGlassStorage')
m.press(8,120);m.press(6,120)
assert state()[4]==1 and state()[1]==30 and state()[5]==1
m.snap('storage-drag-to-party')
m.press(0,120);m.press(0,120);m.press(0,120)
# Last usable member cannot be deposited into an empty box slot.
m.write(m.symbols['gPlayerParty'],original[:100]+b'\0'*500)
m.write(m.symbols['gPlayerPartyCount'],b'\x01')
m.write(boxptr+4,b'\0'*80)
call('ShowPokeGlassStorage')
m.press(6,120);m.press(8,120);m.press(8,120)
m.press(7,120);m.press(7,120)
before=party();m.press(8,120)
assert state()[5]==1 and party()==before
assert m.read(boxptr+4,80)==b'\0'*80
m.press(0,120);m.press(0,120);m.press(0,120)
print('All 36 icons and last usable party member protection passed')
# Save through the real flash routine, reset, and Continue.
import subprocess, pathlib, os
native_dir=m.d/'storage-native';native_dir.mkdir(exist_ok=True)
native_addr=m.symbols['gDecompressionBuffer']+0x3000
result_addr=m.symbols['gDecompressionBuffer']+0x3f00
prefix=os.environ['ARM_NM'].removesuffix('nm')
assembly=['.syntax unified','.thumb','.thumb_func','_start:','push {r4, lr}','movs r0, #0','ldr r3, function','bl invoke','ldr r3, result','str r0, [r3]','movs r0, #1','pop {r4, pc}','invoke:','bx r3','.align 2',f'function: .word {m.symbols["TrySavingData"]|1}',f'result: .word {result_addr}']
(native_dir/'call.s').write_text('\n'.join(assembly)+'\n')
subprocess.run([prefix+'as','-mthumb','-mcpu=arm7tdmi','-o',str(native_dir/'call.o'),str(native_dir/'call.s')],check=True)
subprocess.run([prefix+'objcopy','-O','binary','-j','.text',str(native_dir/'call.o'),str(native_dir/'call.bin')],check=True)
m.write(native_addr,(native_dir/'call.bin').read_bytes())
expected_party=party();expected_boxes=m.read(boxptr+4,14*30*80)
m.inject(b'\x23'+struct.pack('<I',native_addr|1)+b'\x6b\x02')
for _ in range(40):
 if m.read(m.symbols['sGlobalScriptContextStatus'],1)==b'\x02':break
 m.run(60)
assert struct.unpack('<I',m.read(result_addr,4))[0]==1
m.lib.retro_reset();m.run(360);m.press(3);m.press(8);m.press(8);m.run(180)
boxptr=struct.unpack('<I',m.read(m.symbols['gPokemonStoragePtr'],4))[0]
assert party()==expected_party
assert m.read(boxptr+4,14*30*80)==expected_boxes
print('Actual flash save, reset, and Continue preserved party and all boxes')
