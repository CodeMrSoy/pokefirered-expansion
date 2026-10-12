#!/usr/bin/env python3
"""Targeted Quantum QOL checks using an mGBA libretro core, Pillow and NumPy."""
import struct, subprocess
import ctypes as c, pathlib, json, sys
from PIL import Image
root=pathlib.Path(__file__).resolve().parents[1]; d=root/'build/quantum-qol-tests'; d.mkdir(parents=True, exist_ok=True)
import os
lib=c.CDLL(os.environ.get('MGBA_CORE', '/usr/lib/x86_64-linux-gnu/libretro/mgba_libretro.so'))
ENV=c.CFUNCTYPE(c.c_bool,c.c_uint,c.c_void_p); VIDEO=c.CFUNCTYPE(None,c.c_void_p,c.c_uint,c.c_uint,c.c_size_t); AUDIO=c.CFUNCTYPE(None,c.c_int16,c.c_int16); BATCH=c.CFUNCTYPE(c.c_size_t,c.c_void_p,c.c_size_t); POLL=c.CFUNCTYPE(None); INPUT=c.CFUNCTYPE(c.c_int16,c.c_uint,c.c_uint,c.c_uint,c.c_uint)
class Desc(c.Structure):_fields_=[('flags',c.c_uint64),('ptr',c.c_void_p),('offset',c.c_size_t),('start',c.c_size_t),('select',c.c_size_t),('disconnect',c.c_size_t),('len',c.c_size_t),('addrspace',c.c_char_p)]
class Maps(c.Structure):_fields_=[('descriptors',c.POINTER(Desc)),('num_descriptors',c.c_uint)]
class Game(c.Structure):_fields_=[('path',c.c_char_p),('data',c.c_void_p),('size',c.c_size_t),('meta',c.c_char_p)]
fmt=0; desc=[]; keys=set(); screen=None; system=c.create_string_buffer(str(d).encode())
@ENV
def env(cmd,data):
 global fmt,desc
 cmd = cmd & 0xffff
 if cmd==10:fmt=c.cast(data,c.POINTER(c.c_int))[0];return True
 if cmd==36:
  m=c.cast(data,c.POINTER(Maps)).contents;desc=[(x.start,x.len,x.ptr,x.offset) for x in m.descriptors[:m.num_descriptors]];return True
 if cmd in [9,31]:c.cast(data,c.POINTER(c.c_void_p))[0]=c.addressof(system);return True
 if cmd==3:c.cast(data,c.POINTER(c.c_bool))[0]=False;return True
 if cmd==17:c.cast(data,c.POINTER(c.c_bool))[0]=False;return True
 return False
@VIDEO
def video(data,w,h,pitch):
 global screen
 if data and data!=c.c_void_p(-1).value:
  raw=c.string_at(data,h*pitch)
  if fmt==1:screen=Image.frombytes('RGB',(w,h),raw,'raw','BGRX',pitch)
  else:
   import numpy as np
   a=np.frombuffer(raw,dtype=np.uint16).reshape(h,pitch//2)[:,:w]
   if fmt==2:r=((a>>11)&31)*255//31;g=((a>>5)&63)*255//63;b=(a&31)*255//31
   else:r=((a>>10)&31)*255//31;g=((a>>5)&31)*255//31;b=(a&31)*255//31
   screen=Image.fromarray(np.stack([r,g,b],axis=-1).astype('uint8'))
@AUDIO
def audio(a,b):pass
@BATCH
def batch(p,n):return n
@POLL
def poll():pass
@INPUT
def inp(port,device,index,key):return int(key in keys)
for n,cb in [('environment',env),('video_refresh',video),('audio_sample',audio),('audio_sample_batch',batch),('input_poll',poll),('input_state',inp)]:getattr(lib,'retro_set_'+n)(cb)
lib.retro_init(); lib.retro_load_game.argtypes=[c.POINTER(Game)];lib.retro_load_game.restype=c.c_bool
rom=(root/'pokefirered.gba').read_bytes();buf=c.create_string_buffer(rom);game=Game(str(root/'pokefirered.gba').encode(),c.cast(buf,c.c_void_p),len(rom),None)
assert lib.retro_load_game(c.byref(game))
lib.retro_serialize_size.restype=c.c_size_t;lib.retro_serialize.argtypes=[c.c_void_p,c.c_size_t];lib.retro_serialize.restype=c.c_bool;lib.retro_unserialize.argtypes=[c.c_void_p,c.c_size_t];lib.retro_unserialize.restype=c.c_bool

symbols={}
for line in subprocess.check_output([os.environ.get('ARM_NM', 'arm-none-eabi-nm'),str(root/'pokefirered.elf')],text=True).splitlines():
 parts=line.split()
 if len(parts)==3:symbols[parts[2]]=int(parts[0],16)
def read(addr,n):
 for start,size,p,offset in desc:
  if p and start<=addr and addr+n<=start+size:return c.string_at(p+offset+addr-start,n)
 raise ValueError(hex(addr))
def write(addr,b):
 for start,size,p,offset in desc:
  if p and start<=addr and addr+len(b)<=start+size:c.memmove(p+offset+addr-start,b,len(b));return
 raise ValueError(hex(addr))
def run(n):
 for _ in range(n):lib.retro_run()
def press(key,wait=180):
 keys.add(key);run(2);keys.clear();run(wait)
def snap(name):screen.resize((720,480),Image.Resampling.NEAREST).save(d/(name+'.png'))
def inject(b):
 addr=symbols['gDecompressionBuffer'];write(addr,b)
 ctx=symbols['sGlobalScriptContext'];write(ctx,b'\x00\x01\x00\x00');write(ctx+8,struct.pack('<I',addr));write(symbols['sGlobalScriptContextStatus'],b'\x00');run(180)
run(360);press(3);press(8);snap('boot')
for i in range(8):press(8)
press(3);press(8)
for i in range(5):press(8)
press(5);press(8)
for i in range(12):press(8)
press(0);press(0);press(0)
snap('room')
if __name__=='__main__':
 fixture=b''
 for species in (1,4,7,25,133,143):
  fixture+=b'\x23'+struct.pack('<I',(symbols['ScrCmd_createmon']|1)+0x2000000)+struct.pack('<BBHHI',0,6,species,25,0)
 fixture+=b'\x44'+struct.pack('<HH',717,1)
 for slot,move in enumerate((33,52,45)):
  fixture+=b'\x7a'+struct.pack('<BBH',0,slot,move)
 inject(fixture+b'\x02')
 print('party count',read(symbols['gPlayerPartyCount'],1).hex(),'ctx',read(symbols['sGlobalScriptContext'],12).hex(),flush=True);assert read(symbols['gPlayerPartyCount'],1)==b'\x06'
 press(3);snap('start');press(8);snap('hub');press(7);press(8);snap('party')
 press(7);press(5);snap('party-navigation')
 press(4);press(6)
 originalParty=read(symbols['gPlayerParty'],600)
 press(8);press(5);press(5);press(8);press(7);press(8)
 assert read(symbols['gPlayerParty'],100)==originalParty[100:200]
 assert read(symbols['gPlayerParty']+100,100)==originalParty[:100]
 snap('party-swapped')
 press(0);press(0);press(0)
 write(symbols['gPlayerParty'],originalParty)
 # Preserve a field state for independent single/double and item checks.
 size=lib.retro_serialize_size();state=c.create_string_buffer(size);assert lib.retro_serialize(state,size)
 (d/'field.state').write_bytes(state.raw)
 inject(b'\xb6'+struct.pack('<HBHHBH',92,5,0,0,0,0)+b'\xb7\x6b\x02');run(600)
 press(8);press(8);snap('single-action');press(8);snap('physical')
 press(7);snap('special');press(6);press(5);snap('status')
 state=c.create_string_buffer((d/'field.state').read_bytes());assert lib.retro_unserialize(state,size)
 inject(b'\xb6'+struct.pack('<HBHHBH',92,5,0,25,5,0)+b'\xb7\x6b\x02');run(700)
 for _ in range(3):press(8)
 assert read(symbols['gBattlersCount'],1)==b'\x04'
 snap('double-types')
 state=c.create_string_buffer((d/'field.state').read_bytes());assert lib.retro_unserialize(state,size)
 inject(b'\x16'+struct.pack('<HH',0x8000,28)+b'\x16'+struct.pack('<HH',0x8001,1)+b'\x09\x01\x02')
 snap('pickup-description')
 for _ in range(8):
  if read(symbols['sGlobalScriptContextStatus'],1)==b'\x02':break
  press(8)
 assert read(symbols['sGlobalScriptContextStatus'],1)==b'\x02'
 gift=b'\x44'+struct.pack('<HH',717,1)
 for var,value in ((0x8000,717),(0x8001,1),(0x8002,318)):
  gift+=b'\x16'+struct.pack('<HH',var,value)
 gift+=b'\x0f\x00'+struct.pack('<I',symbols['PalletTown_ProfessorOaksLab_Text_ReceivedPokeGlassFromOak'])+b'\x09\x09\x02'
 inject(gift);snap('gift-description')
 for _ in range(8):
  if read(symbols['sGlobalScriptContextStatus'],1)==b'\x02':break
  press(8)
 assert read(symbols['sGlobalScriptContextStatus'],1)==b'\x02'
 print('Party fixture and single/double battle checks reached',flush=True)
