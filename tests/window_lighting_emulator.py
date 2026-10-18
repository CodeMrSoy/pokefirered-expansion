#!/usr/bin/env python3
"""Real outdoor maps: daytime-equivalent art, dark paths, warm building glass."""
import argparse,pathlib,struct,subprocess,os,types
import numpy as np
p=argparse.ArgumentParser();p.add_argument('--rom');p.add_argument('--baseline',action='store_true');a=p.parse_args()
harness=pathlib.Path(__file__).with_name('quantum_qol_emulator.py');source=harness.read_text();m=types.ModuleType('lighting_harness');m.__file__=str(harness)
if a.rom:source=source.replace("rom=(root/'pokefirered.gba').read_bytes()",'rom=pathlib.Path('+repr(str(pathlib.Path(a.rom).resolve()))+').read_bytes()')
exec(compile(source,str(harness),'exec'),m.__dict__)
d=m.d/('lighting-before' if a.baseline else 'lighting-after');d.mkdir(exist_ok=True)
addr=m.symbols['gDecompressionBuffer']+0x3000;prefix=os.environ.get('ARM_NM','arm-none-eabi-nm').removesuffix('nm')
def native(name,*args):
 lines=['.syntax unified','.thumb','.thumb_func','_start:','push {r4,lr}']
 lines += [f'ldr r{i},arg{i}' for i in range(len(args))]
 lines += ['ldr r3,function','bl invoke','movs r0,#1','pop {r4,pc}','invoke:','bx r3','.align 2',f'function: .word {m.symbols[name]|1}']
 lines += [f'arg{i}: .word {arg}' for i,arg in enumerate(args)]
 (d/'call.s').write_text('\n'.join(lines)+'\n')
 subprocess.run([prefix+'as','-mthumb','-mcpu=arm7tdmi','-o',str(d/'call.o'),str(d/'call.s')],check=True)
 subprocess.run([prefix+'objcopy','-O','binary','-j','.text',str(d/'call.o'),str(d/'call.bin')],check=True)
 m.write(addr,(d/'call.bin').read_bytes());m.inject(b'\x23'+struct.pack('<I',addr|1)+b'\x6b\x02')
def time(hour):
 m.write(m.symbols['sHoursOverride'],bytes([hour]));native('UpdateTimeOfDay');native('UpdatePalettesWithTime',0x1fff);m.run(120)
def palette(which):return np.frombuffer(m.read(m.symbols[which],13*32),dtype='<u2').reshape(13,16)
def rgb(c):return np.array([int(c)&31,(int(c)>>5)&31,(int(c)>>10)&31])
for name,num,x,y in [('Viridian',1,30,24),('Cerulean',3,25,22),('Lavender',4,10,11),('Saffron',10,25,35),('Pallet',0,10,9)]:
 m.inject(b'\x39'+struct.pack('<BBBHH',3,num,255,x,y)+b'\x6b\x02');m.run(300)
 time(12);day=palette('gPlttBufferFaded').copy();m.screen.resize((720,480),m.Image.Resampling.NEAREST).save(d/(name+'-day.png'))
 time(23);night=palette('gPlttBufferFaded');raw=palette('gPlttBufferUnfaded')
 if a.baseline:assert all(raw[5,j]&0x8000 for j in (6,7,8))
 else:
  assert all(not raw[5,j]&0x8000 for j in (6,7,8)),(name,'Path colors flagged as lights')
  assert all(rgb(night[5,j]).sum()<rgb(day[5,j]).sum() for j in (6,7,8)),(name,'Paths fail to darken')
  assert raw[3,8]&0x8000 and raw[2,15]&0x8000,(name,'Center/Mart glass lost its light')
  assert rgb(night[3,8])[0]>rgb(day[3,8])[0] and rgb(night[2,15])[0]>rgb(day[2,15])[0],(name,'Glass is not warmly lit')
  if name=='Lavender':assert raw[7,5]&0x8000 and raw[7,6]&0x8000
 m.screen.resize((720,480),m.Image.Resampling.NEAREST).save(d/(name+'-night.png'))
 print(name,'day/night and glass checks passed',flush=True)
print('Before/after screenshots:',d)
