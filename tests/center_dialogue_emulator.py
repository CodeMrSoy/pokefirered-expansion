"""Native nurse flow: healing, dismissing dialogue and restored field movement."""
import json,struct,subprocess
import numpy as np
import havora_emulator_support as m

def locked():return m.read(m.symbols['sLockFieldControls'],1)[0]
def warp(name,x,y):
 raw=(m.root/'include/constants/map_groups.h').read_text();import re
 num,group=map(int,re.search(r'#define MAP_'+name+r'\s+\((\d+) \| \((\d+) << 8\)\)',raw).groups())
 m.inject(b'\x39'+struct.pack('<BBBHH',group,num,255,x,y)+b'\x6b\x02');m.run(180)
for species in [25,1]:m.inject(b'\x23'+struct.pack('<I',(m.symbols['ScrCmd_createmon']|1)+0x02000000)+struct.pack('<BBHHI',0,6,species,10,0)+b'\x02')
nm=subprocess.check_output(['arm-none-eabi-nm','-S',str(m.root/'pokefirered.elf')],text=True)
size=int(next(l.split()[1] for l in nm.splitlines() if l.endswith(' gPlayerParty')),16)//6
hp=m.symbols['gPlayerParty']+size-14;maxhp=struct.unpack('<H',m.read(hp+2,2))[0]
for name in ['QUANTUM_PORT_CITY_POKEMON_CENTER1_F','VIRIDIAN_CITY_POKEMON_CENTER_1F']:
 warp(name,7,4);m.keys.add(4);m.run(1);m.keys.clear();m.run(40)
 empty=np.array(m.screen)[128:].copy();m.write(hp,struct.pack('<H',1));m.press(8,30)
 healed=False
 for tick in range(2500):
  if tick%35==0:m.keys.add(8)
  if tick%35==2:m.keys.clear()
  m.run(1)
  healed|=struct.unpack('<H',m.read(hp,2))[0]==maxhp
  if healed and not locked():break
 m.keys.clear();m.run(45);m.snap('center-after-'+name)
 print(name,'healed',healed,'locked',locked(),'ctx',m.read(m.symbols['sGlobalScriptContext'],4).hex(),'changed bottom pixels',np.count_nonzero(empty!=np.array(m.screen)[128:]),flush=True)
 assert healed and not locked(),name
 # NPC idle animation can change a few floor pixels in Viridian. A stuck
 # dialogue changes most of this region (19,152 components in reproduction).
 assert np.count_nonzero(empty!=np.array(m.screen)[128:])<empty.size//100,'Healing dialogue remains visible: '+name
 assert m.read(m.symbols['sMessageBoxType'],1)==b'\x00','Message printer still active'
 obj=m.read(m.symbols['gPlayerAvatar']+5,1)[0];pos=m.symbols['gObjectEvents']+36*obj+16;before=struct.unpack('<hh',m.read(pos,4))
 m.keys.add(5);m.run(20);m.keys.clear();m.run(60);after=struct.unpack('<hh',m.read(pos,4));assert after[1]>before[1],'Player cannot walk after healing'
print('PASS native healing text clears and field controls resume in Havora and Viridian',flush=True)
