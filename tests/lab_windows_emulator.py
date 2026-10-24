"""Actual Pallet Town lab day/night glass, including all seasonal tile pairs."""
import argparse,struct,subprocess
from pathlib import Path
import numpy as np
import havora_emulator_support as m
p=argparse.ArgumentParser();p.add_argument('--baseline',action='store_true');a=p.parse_args()
d=m.d/'lab-windows';d.mkdir(exist_ok=True)
addr=m.symbols['gDecompressionBuffer']+0x3000
def native(name,*args):
 lines=['.syntax unified','.thumb','.thumb_func','_start:','push {r4,lr}']+[f'ldr r{i},arg{i}' for i in range(len(args))]
 lines+=['ldr r3,function','bl invoke','movs r0,#1','pop {r4,pc}','invoke:','bx r3','.align 2',f'function: .word {m.symbols[name]|1}']+[f'arg{i}: .word {arg}' for i,arg in enumerate(args)]
 (d/'call.s').write_text('\n'.join(lines)+'\n');subprocess.run(['arm-none-eabi-as','-mthumb','-mcpu=arm7tdmi','-o',str(d/'call.o'),str(d/'call.s')],check=True)
 subprocess.run(['arm-none-eabi-objcopy','-O','binary','-j','.text',str(d/'call.o'),str(d/'call.bin')],check=True)
 m.write(addr,(d/'call.bin').read_bytes());m.inject(b'\x23'+struct.pack('<I',addr|1)+b'\x6b\x02')
def time(hour):
 m.write(m.symbols['sHoursOverride'],bytes([hour]));native('UpdateTimeOfDay');native('UpdatePalettesWithTime',0x1fff);m.run(90)
def pal(name):return np.frombuffer(m.read(m.symbols[name],13*32),dtype='<u2').reshape(13,16).copy()
m.inject(b'\x39'+struct.pack('<BBBHH',3,0,255,16,14)+b'\x6b\x02');m.run(180)
layout=struct.unpack('<I',m.read(m.symbols['gMapHeader'],4))[0]
for season in ['', 'Summer','Autumn','Winter']:
 m.write(m.symbols['gCurrentPrimaryTileset'],struct.pack('<I',m.symbols['gTileset_General'+season]));m.write(m.symbols['gCurrentSecondaryTileset'],struct.pack('<I',m.symbols['gTileset_PalletTown'+season]))
 native('CopyMapTilesetsToVram',layout);native('LoadMapTilesetPalettes',layout);native('DrawWholeMapView')
 time(12);day=pal('gPlttBufferFaded');m.snap('lab-'+('before-' if a.baseline else 'after-')+(season or 'Spring')+'-day')
 time(23);night=pal('gPlttBufferFaded');raw=pal('gPlttBufferUnfaded');m.snap('lab-'+('before-' if a.baseline else 'after-')+(season or 'Spring')+'-night')
 # Every blue glass quarter in the lab wall must use palette 9 (not the
 # unlit wall clone, palette 7). Inspect the actual ROM metatile words.
 tileset=m.symbols['gTileset_PalletTown'+season]
 # Struct layouts are checked from C, rather than inferred offsets.
 probe=d/'offset.c';probe.write_text('#include "global.h"\nconst u32 offsets[]={__builtin_offsetof(struct Tileset,metatiles)};\n')
 subprocess.run(['arm-none-eabi-gcc','-c','-iquote',str(m.root/'include'),'-iquote',str(m.root/'gflib'),'-DFIRERED',str(probe),'-o',str(d/'offset.o')],check=True)
 subprocess.run(['arm-none-eabi-objcopy','-O','binary','-j','.rodata',str(d/'offset.o'),str(d/'offset.bin')],check=True)
 offset=struct.unpack('<I',(d/'offset.bin').read_bytes())[0];ptr=struct.unpack('<I',m.read(tileset+offset,4))[0]
 for mid,k in [(704,5),(705,1),(707,5),(708,0),(709,4),(713,0)]:
  w=struct.unpack('<H',m.read(ptr+((mid-640)*8+k)*2,2))[0]
  if not a.baseline:assert w>>12==9,(season,hex(mid),k,'unlit lab glass')
 assert all(raw[9,j]&0x8000 for j in [8,9,10])
 for j in [8,9,10]:assert int(night[9,j]&31)>int(day[9,j]&31),(season,j,'glass not warm')
 assert all(not raw[7,j]&0x8000 for j in range(1,16)),'wall clone lit'
 print(('BASELINE' if a.baseline else 'PASS'),season or 'Spring','lab glass and dark wall separation',flush=True)
