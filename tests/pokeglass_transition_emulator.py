import struct
import numpy as np
import quantum_qol_emulator as m
fixture=b''
for species in (1,4,7,25,133,143):
 fixture+=b'\x23'+struct.pack('<I',(m.symbols['ScrCmd_createmon']|1)+0x2000000)+struct.pack('<BBHHI',0,6,species,25,0)
fixture+=b'\x29'+struct.pack('<H',0x829)
fixture+=b'\x44'+struct.pack('<HH',717,1)
m.inject(fixture+b'\x02')
m.press(3);m.press(8)
mask=np.zeros((160,240),dtype=bool);mask[10:150,12:228]=True;mask[23:136,20:220]=False
base=np.asarray(m.screen).copy();m.snap('transition-base')
size=m.lib.retro_serialize_size();st=m.c.create_string_buffer(size);assert m.lib.retro_serialize(st,size)
for name, seq in [('pokedex',[]),('storage',[7,7]),('stats',[5,7]),('wardrobe',[5,7,7]),('party',[7]),('map',[5])]:
 assert m.lib.retro_unserialize(st,size)
 for k in seq:m.press(k,60)
 m.keys.add(8);bad=[];black=[];frames=[]
 for frame in range(180):
  m.run(1)
  if frame==1:m.keys.clear()
  a=np.asarray(m.screen)
  if not np.array_equal(a[mask],base[mask]):bad.append(frame)
  if a[mask].mean()<10:black.append(frame)
  if frame<80:frames.append(m.screen.resize((720,480),m.Image.Resampling.NEAREST))
 m.snap('transition-'+name)
 frames[0].save(m.d/('transition-'+name+'.gif'),save_all=True,append_images=frames[1:],duration=17,loop=0)
 print(name,'shell changes',bad[:20],len(bad),'black',black,flush=True)

 assert not bad and not black, (name,bad,black)
