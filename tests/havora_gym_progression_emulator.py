"""Clearance, literal 6v6 readiness, healer, reset and completed-save migration."""
from pathlib import Path
s=Path(__file__).with_name('havora_three_lock_emulator.py').read_text()
exec(compile(s[:s.index('for i,step in enumerate')],'gym-setup','exec'))
native('VarSet',0x40d8,0)
assert command(24)==2,'captain accepted an uncleared crew'
for bit,expected in [(1,1),(2,3),(8,11),(16,27),(32,59)]:
 assert command(23,expected)==0
 command(22,bit);assert value(0x40d8)==expected
 assert command(23,expected)==1
assert command(24)==3,'captain accepted fewer than six usable Pokemon'
fixture=b''
for species in [131,68,131,68,131,68]:
 fixture+=b'\x23'+struct.pack('<I',(m.symbols['ScrCmd_createmon']|1)+0x2000000)+struct.pack('<BBHHI',0,6,species,60,0)
m.inject(fixture+b'\x02')
assert command(24)==1,'captain rejected six healthy Pokemon'
pointer=m.symbols['gDecompressionBuffer']+0x2500
m.write(pointer,b'\0\0\0\0');native('SetMonData',m.symbols['gPlayerParty'],10,pointer)
assert command(24)==3,'fainted Pokemon counted as usable'
assert command(25)==1 and command(24)==1,'free healer did not restore readiness'
command(15);assert value(0x40d8)==59,'reset erased clearances'
native('VarSet',0x40d8,7);native('VarSet',0x40d7,0x8408)
warp(20,33)
assert pos()==geo.ENTRY and value(0x40d8)==63,'completed legacy gym migration'
assert command(24)==1,'completed captain dialogue blocked'
print('PASS five ordered clearance bits, six usable Pokemon check, free healing, reset and legacy completed gym')
