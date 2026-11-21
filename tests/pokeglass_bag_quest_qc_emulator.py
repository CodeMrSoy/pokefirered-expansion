"""Fresh Classic/Quantum repeated Bag/Book, palette, heap and control QC.

Run separately with QUEST_QC_ADVENTURE=0 and 1.
"""
import os,pathlib,struct,json
setup=pathlib.Path(__file__).with_name('avatar_wardrobe_emulator.py')
source=setup.read_text().split("fixture = b'\\x23'")[0]
mode=int(os.environ.get('QUEST_QC_ADVENTURE','1'))
if mode==0:source=source.replace("wait_task('Task_AdventureSelection');m.press(8);m.press(8)","wait_task('Task_AdventureSelection');m.press(4);m.press(8);m.press(8)")
exec(compile(source,str(setup),'exec'))
assert native('AdventureMode_Get')==mode
fixture=b'\x23'+struct.pack('<I',(m.symbols['ScrCmd_givegiftmon']|1)+0x2000000)+struct.pack('<BBHHI',0,6,1,25,0)
fixture+=b'\x29'+struct.pack('<H',0x829)
for item,q in [(717,1),(28,3),(29,2),(715,1),(716,1),(831,1),(3,12)]:fixture+=b'\x44'+struct.pack('<HH',item,q)
m.inject(fixture+b'\x02')
def ptr(name):return struct.unpack('<I',m.read(m.symbols[name],4))[0]
def heap():
 start=ptr('sHeapStart');address=start;blocks=[]
 while True:
  flags,size,previous,following=struct.unpack('<4I',m.read(address,16))
  assert flags>>16==0xa3a3,('Corrupt heap',hex(address))
  blocks.append((bool(flags&1),size&((1<<18)-1)))
  assert len(blocks)<1024
  address=following
  if address==start:break
 return sum(size for used,size in blocks if used),sum(used for used,size in blocks)
def palette():return m.read(m.symbols['gPlttBufferFaded'],13*32)
def field():return m.read(m.symbols['sLockFieldControls'],1)==b'\0'
def unlocked_cleanup():
 assert field(),'Closing app left controls locked'
 assert ptr('sFieldBackdrop')==0,'Retained captured map after closing'
 if 'sSpriteTileTags' in m.symbols:
  tags=struct.unpack('<64H',m.read(m.symbols['sSpriteTileTags'],128))
  assert not any(0xd300<=tag<0xd309 for tag in tags),'Retained grid tiles'
 if 'sSpritePaletteTags' in m.symbols:
  tags=struct.unpack('<16H',m.read(m.symbols['sSpritePaletteTags'],32))
  assert not any(0xd300<=tag<0xd309 for tag in tags),'Retained grid palettes'
# Discover the optional quest without accepting it, to cover available/declined UI.
native('QuestBook_Discover',5)
assert native('QuestBook_GetState',5)==1
before=m.read(ptr('gSaveBlock2Ptr')+3803,144)
# Reach Quest Book through real launcher navigation, without writing its cursor.
m.write(m.symbols['sHubCursor'],b'\x05');m.press(3);wait_task('Task_PokeGlassHub')
for key, cursor in ((7, 6), (4, 9), (7, 12), (7, 13)):
 m.press(key,30)
 assert m.read(m.symbols['sHubCursor'],1)==bytes([cursor])
m.press(7,30)
assert m.read(m.symbols['sHubCursor'],1)==b'\x00'
m.press(6,30)
assert m.read(m.symbols['sHubCursor'],1)==b'\x0d'
m.snap('qc-quest-book-launcher');m.press(8);wait_task('Task_GlassQuestBook');m.run(60)
# Empty Side/Done filters must tolerate all D-pad directions and A.
for _ in range(4):
 m.press(2,20)
 for key in [4,5,6,7,8]:
  m.press(key,20)
  if task_active('Task_GlassQuestOffer'):m.press(0,30)
m.snap('qc-quest-filters');m.press(0);wait_task('Task_PokeGlassHub')
assert m.read(m.symbols['sHubCursor'],1)==b'\x0d'
m.press(0)
assert field()
# Book offer: Decline, reoffer, Accept, then Track using actual button input.
m.write(m.symbols['sHubCursor'],b'\x0d');m.press(3);wait_task('Task_PokeGlassHub');m.press(8);wait_task('Task_GlassQuestBook')
# Select Side filter regardless of its remembered previous value.
for _ in range(4):
 if m.read(m.symbols['sQuestFilter'],1)==b'\x02':break
 m.press(2,20)
m.press(8,30);wait_task('Task_GlassQuestOffer');m.press(0,30);wait_task('Task_GlassQuestBook')
m.press(8,30);wait_task('Task_GlassQuestOffer');m.press(8,30);wait_task('Task_GlassQuestBook')
m.press(8,30)
m.snap('qc-quest-tracked');m.press(0);wait_task('Task_PokeGlassHub');m.press(0)
assert native('QuestBook_GetState',5)==2 and native('QuestBook_GetTracked')==5
# Both modes hide undiscovered content; Classic also refuses Vidra IDs.
if mode==0:
 assert not native('QuestBook_GetDefinition',3) and not native('QuestBook_GetDefinition',4)
assert not native('QuestBook_IsVisible',3)
# The same real NPC offer must close cleanly at night, including its postgame branch.
groups=json.loads((m.root/'data/maps/map_groups.json').read_text())
labgroup=next(i for i,k in enumerate(groups['group_order']) if 'PalletTown_ProfessorOaksLab' in groups[k])
labnum=groups[groups['group_order'][labgroup]].index('PalletTown_ProfessorOaksLab')
m.inject(b'\x39'+struct.pack('<BBBHH',labgroup,labnum,255,6,9)+b'\x6b\x02');m.run(300)
m.write(m.symbols['sHoursOverride'],b'\x16')
native('UpdateTimeOfDay');native('ApplyWeatherColorMapToPals',0,16);native('ApplyWeatherColorMapToPals',16,16);m.run(60)
night=palette()
for postgame in [False,True]:
 if postgame:native('FlagSet',0x82c)
 m.inject(b'\x05'+struct.pack('<I',m.symbols['PalletTown_ProfessorOaksLab_EventScript_Aide1']))
 for _ in range(12):
  if task_active('Task_GlassQuestOffer'):break
  m.press(8,30)
 wait_task('Task_GlassQuestOffer');m.snap('qc-night-aide-'+str(postgame));m.press(0,180)
 assert field() and palette()==night,('NPC offer changed night colors/controls',mode,postgame)
 if postgame:native('FlagClear',0x82c)
print('PASS',mode,'nighttime aide offer and postgame branch',flush=True)
groups=json.loads((m.root/'data/maps/map_groups.json').read_text())
places=[('bedroom',4,1,6,6,(12,19,22)),('viridian',3,1,30,24,(12,19,22))]
if mode:
 group=next(i for i,k in enumerate(groups['group_order']) if 'VidraDraft_RainfallRoute' in groups[k])
 number=groups[groups['group_order'][group]].index('VidraDraft_RainfallRoute')
 places.append(('rainfall',group,number,12,10,(22,)))
results=[]
for place,group,number,x,y,hours in places:
 m.inject(b'\x39'+struct.pack('<BBBHH',group,number,255,x,y)+b'\x6b\x02');m.run(300)
 for hour in hours:
  m.write(m.symbols['sHoursOverride'],bytes([hour]))
  native('UpdateTimeOfDay');native('ApplyWeatherColorMapToPals',0,16);native('ApplyWeatherColorMapToPals',16,16);m.run(60)
  expected=palette();baseline=None
  for cycle in range(2):
   for app,task in [(5,'Task_BagMenu_HandleInput'),(13,'Task_GlassQuestBook')]:
    m.write(m.symbols['sHubCursor'],bytes([app]));m.press(3);wait_task('Task_PokeGlassHub');m.press(8);wait_task(task);m.run(60)
    if app==5:
     m.press(11,40);m.press(11,40);m.press(10,40);m.press(10,40)
    else:
     for key in [7,7,6,5,4,2,2,2,2]:m.press(key,20)
    m.snap(f'qc-{place}-{hour}-{app}-{cycle}')
    m.press(0,240);wait_task('Task_PokeGlassHub')
    assert palette()==expected,('App return changed map lighting',mode,place,hour,app,cycle)
    m.press(0,180);unlocked_cleanup()
    assert palette()==expected,('Closing glass changed map lighting',mode,place,hour,app,cycle)
    current=heap()
    if baseline is None:baseline=current
    assert current==baseline,('Heap grew after app',mode,place,hour,app,cycle,baseline,current)
    results.append({'mode':mode,'place':place,'hour':hour,'app':app,'cycle':cycle,'heap':current,'palette_preserved':True})
  print('PASS',mode,place,hour,'Bag/Quest Book palettes, cleanup and repeated returns',flush=True)
# Quest/character/adventure state must survive a real Flash save/reset/Continue.
record=m.read(ptr('gSaveBlock2Ptr')+3803,144);identity=m.read(ptr('gSaveBlock2Ptr'),14)
assert native('TrySavingData',0)==1
m.lib.retro_reset();m.run(360);m.press(3);m.press(8);m.press(8);m.run(180)
assert native('AdventureMode_Get')==mode
assert m.read(ptr('gSaveBlock2Ptr')+3803,144)==record
assert m.read(ptr('gSaveBlock2Ptr'),14)==identity
assert native('QuestBook_GetTracked')==5
(m.d/'qc-results.json').write_text(json.dumps({'mode':mode,'app_cycles':len(results),'results':results},indent=2))
print('PASS fresh adventure',mode,'launcher navigation; Book decline/accept/track/filter; repeated Bag/Book heap/palette/control checks; Flash persistence; app cycles',len(results),flush=True)
