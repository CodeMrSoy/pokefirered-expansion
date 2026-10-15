#!/usr/bin/env python3
"""Targeted Quantum QOL checks using an mGBA libretro core, Pillow and NumPy."""
import struct, subprocess
import ctypes as c, pathlib, json, sys
from PIL import Image
root=pathlib.Path(__file__).resolve().parents[1]; d=root/'build/havora-tests'; d.mkdir(parents=True, exist_ok=True)
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
for i in range(9):press(8)
press(3);press(8)
for i in range(5):press(8)
press(5);press(8)
for i in range(12):press(8)
press(0);press(0);press(0)
snap('room')
