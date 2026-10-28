#!/usr/bin/env python3
"""Party handoff: hardware sprite cleanup and persistent field backdrop."""
import struct
import numpy as np
import quantum_qol_emulator as m
fixture=b''
for species in (1,4,7,25,133,143):
 fixture+=b'\x23'+struct.pack('<I',(m.symbols['ScrCmd_createmon']|1)+0x2000000)+struct.pack('<BBHHI',0,6,species,25,0)
# App-only fixture represents a player who already received Oak's device.
fixture += b'\x29' + struct.pack('<H', 0x829)
m.inject(fixture+b'\x44'+struct.pack('<HH',717,1)+b'\x02')
m.press(3);m.press(7,60)
size=m.lib.retro_serialize_size();st=m.c.create_string_buffer(size);assert m.lib.retro_serialize(st,size)
def reg(offset):return struct.unpack('<H',m.read(m.symbols['sGpuRegBuffer']+offset,2))[0]
for count in (1,6):
 assert m.lib.retro_unserialize(st,size)
 if count==1:
  m.write(m.symbols['gPlayerParty']+100,b'\0'*500)
  m.write(m.symbols['gPlayerPartyCount'],b'\x01')
 m.keys.add(8);frames=[];ready=0;loading=0;blank=[]
 for frame in range(240):
  m.run(1)
  if frame==1:m.keys.clear()
  callback=struct.unpack('<I',m.read(m.symbols['gMain']+4,4))[0]
  state=m.read(m.symbols['gMain']+0x438,1)[0]
  if callback==(m.symbols['CB2_InitPartyMenu']|1) and state>=4:
   # Old field objects must never be displayed using new Pokémon icon tiles.
   oam=m.read(0x07000000,1024)
   attrs=[struct.unpack_from('<H',oam,i*8)[0] for i in range(128)]
   assert all(a&0x300==0x200 or (a&0xff)>=160 for a in attrs),('stale OAM',count,frame,state,attrs[:8])
   loading+=1
  if callback==(m.symbols['CB2_UpdatePartyMenu']|1):
   assert reg(0)&0x800,('Backdrop hidden by window update',count,frame)
   expected=m.read(m.symbols['sFieldBackdropPalette'],32)
   assert m.read(m.symbols['gPlttBufferUnfaded']+10*32,32)==expected,('Backdrop palette replaced',count,frame)
   ready+=1
  if np.asarray(m.screen)[24:128,24:216].mean()<15:blank.append(frame)
  if frame<110:frames.append(m.screen.resize((720,480),m.Image.Resampling.NEAREST))
 assert ready>60 and loading>0,(ready,loading)
 assert not blank,(count,blank)
 m.snap('party-visual-'+str(count))
 frames[0].save(m.d/('party-visual-'+str(count)+'.gif'),save_all=True,append_images=frames[1:],duration=17,loop=0)
 print('Party',count,'loading frames',loading,'ready frames',ready,'blank glass frames',blank,flush=True)
 m.press(8,60);m.press(0,60);m.press(0,240)
 m.snap('party-visual-return-'+str(count))
