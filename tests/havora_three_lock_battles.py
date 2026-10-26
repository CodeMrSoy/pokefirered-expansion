"""Launch all six curated doubles encounters from the overhead gym in mGBA."""
import os,pathlib,struct,subprocess,json
import havora_emulator_support as m
s=(m.root/'tests/avatar_wardrobe_emulator.py').read_text();exec(s[s.index('native_dir ='):s.index('avatar_var = native')])
native('VarSet',0x40d7,0x8408)
groups=json.loads((m.root/'data/maps/map_groups.json').read_text());g,n=next((g,groups[k].index('QuantumHavoraGym')) for g,k in enumerate(groups['group_order']) if 'QuantumHavoraGym' in groups[k])
m.inject(b'\x39'+struct.pack('<BBBHH',g,n,255,3,27)+b'\x6b\x02')
fixture=b''
for species in [131,68,131,68,131,68]:fixture+=b'\x23'+struct.pack('<I',(m.symbols['ScrCmd_createmon']|1)+0x2000000)+struct.pack('<BBHHI',0,6,species,60,0)
m.inject(fixture+b'\x02')
native('VarSet',0x40d8,59)
size=m.lib.retro_serialize_size();snap=m.c.create_string_buffer(size);assert m.lib.retro_serialize(snap,size)
for name,count in [('Crew',2),('Navigator',3),('Engineer',3),('Diver',4),('FirstMate',4),('Captain',6)]:
 assert m.lib.retro_unserialize(snap,size)
 m.inject(b'\x05'+struct.pack('<I',m.symbols['HavoraTrial_'+name]))
 for _ in range(8):
  m.press(8,120)
  if m.read(m.symbols['gBattlersCount'],1)==b'\x04':break
 flags=struct.unpack('<I',m.read(m.symbols['gBattleTypeFlags'],4))[0]
 assert flags&1 and m.read(m.symbols['gBattlersCount'],1)==b'\x04',name
 assert m.read(m.symbols['gEnemyPartyCount'],1)==bytes([count]),('wrong encounter party size',name)
 print('PASS native double battle launch:',name,count,'opponent Pokemon',flush=True)
