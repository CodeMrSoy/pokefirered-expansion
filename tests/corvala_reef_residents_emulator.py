"""Check reef species sprites, dialogue and hut entrances at both tides."""
from pathlib import Path
exec(Path(__file__).with_name('corvala_tides_emulator.py').read_text().split("hour(10);native('DisableWildEncounters',1)")[0])
hour(11);native('DisableWildEncounters',1);warp('Corvala_Town',49,16)
town=json.loads((m.root/'data/maps/Corvala_Town/map.json').read_text())
for npc in town['object_events']:
 if 'SPECIES(' not in npc['graphics_id']:continue
 for dx,dy,key in [(0,1,4),(-1,0,7),(1,0,6),(0,-1,5)]:
  try:follow((npc['x']+dx,npc['y']+dy));break
  except AssertionError:continue
 else:raise AssertionError(('unreachable',npc))
 m.press(key,30);m.snap(npc['script']+'-sprite');m.press(8,100)
 assert m.read(m.symbols['sMessageBoxType'],1)!=b'\0'
 m.snap(npc['script'])
 for _ in range(8):
  m.press(8,60)
  if m.read(m.symbols['sGlobalScriptContext']+1,1)==b'\0':break
 assert m.read(m.symbols['sGlobalScriptContext']+1,1)==b'\0'
for phase,clock in [('low',10),('high',11)]:
 follow((31,26));hour(clock);check_phase(phase)
 for i in range(1,6):
  follow(tuple(manifest['landmarks'][f'house{i}_approach']));m.snap(f'{phase}-hut{i}-floor')
  enter(f'Corvala_House{i}');enter('Corvala_Town',5,22);check_phase(phase)
print('PASS: Corsola/Mareanie interactions and five hut entrances/floors at both tides')
