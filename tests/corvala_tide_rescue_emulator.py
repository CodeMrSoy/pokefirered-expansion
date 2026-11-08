"""Live RTC tide warnings freeze movement and return beach/Surf players safely."""
from pathlib import Path
exec(Path(__file__).with_name('corvala_tides_emulator.py').read_text().split("hour(10);native('DisableWildEncounters',1)")[0])
def rescue(clock,old,new,label):
 before=pos();hour(clock);m.run(100);check_phase(old)
 assert m.read(m.symbols['sMessageBoxType'],1)!=b'\0'
 assert m.read(m.symbols['sGlobalScriptContext']+1,1)!=b'\0'
 m.press(7,40);assert pos()==before,'warning must stop player movement'
 m.snap(label+'-warning')
 for _ in range(10):
  m.press(8,60);m.run(100)
  if pos()==(31,26) and m.read(m.symbols['sGlobalScriptContext']+1,1)==b'\0':break
 assert pos()==(31,26),(label,pos())
 assert not m.read(m.symbols['gPlayerAvatar'],1)[0]&8,'Surf must end on rescue'
 check_phase(new);m.snap(label+'-safe')
 step(7,(32,26));step(6,(31,26))
 print('PASS:',label,'warning, movement lock, Center rescue and correct tide',flush=True)
hour(10);native('DisableWildEncounters',1);warp('Corvala_Town',49,16)
follow((24,46));rescue(11,'low','high','rising-sand')
# A saved view loaded across an hour boundary must take the same rescue path.
hour(10);follow((24,46));native('SaveMapView')
native('RtcInitLocalTimeOffset',11,0);native('InitMapFromSavedGame')
rescue(11,'low','high','rising-saved-sand')
fixture=b'\x23'+struct.pack('<I',(m.symbols['ScrCmd_createmon']|1)+0x2000000)+struct.pack('<BBHHI',0,6,131,30,0)+b'\x02';m.inject(fixture)
follow((21,23));m.press(5,30);m.write(m.symbols['gFieldEffectArguments'],b'\0'*4);native('FieldEffectStart',10);m.run(500)
assert pos()==(21,24) and m.read(m.symbols['gPlayerAvatar'],1)[0]&8
rescue(12,'high','low','receding-surf')
# Ordinary permanent ground changes phase without a rescue or message.
for clock,phase in [(13,'high'),(14,'low'),(23,'high'),(0,'low')]:
 hour(clock);check_phase(phase);assert pos()==(31,26)
 assert m.read(m.symbols['sGlobalScriptContext']+1,1)==b'\0'
print('PASS: normal dock transitions and midnight rollover')
