"""Quest save migration, mode filtering, actual NPC offer, travel and rewards."""
import pathlib, struct
setup=pathlib.Path(__file__).with_name('avatar_wardrobe_emulator.py')
exec(compile(setup.read_text().split("fixture = b'\\x23'")[0],str(setup),'exec'))

def ptr(name): return struct.unpack('<I',m.read(m.symbols[name],4))[0]
def record(): return ptr('gSaveBlock2Ptr')+3803

def state(id): return native('QuestBook_GetState',id)
def warp(name,x,y):
 import json
 groups=json.loads((m.root/'data/maps/map_groups.json').read_text())
 group=next(i for i,k in enumerate(groups['group_order']) if name in groups[k])
 number=groups[groups['group_order'][group]].index(name)
 m.inject(b'\x39'+struct.pack('<BBBHH',group,number,255,x,y)+b'\x6b\x02');m.run(300)

def offer():
 # Execute the real optional aide script, including its original dialogue.
 script=m.symbols['PalletTown_ProfessorOaksLab_EventScript_Aide1']
 m.inject(b'\x05'+struct.pack('<I',script))
 for _ in range(12):
  if task_active('Task_GlassQuestOffer'):break
  m.press(8,30)
 wait_task('Task_GlassQuestOffer')

fixture=b'\x23'+struct.pack('<I',(m.symbols['ScrCmd_givegiftmon']|1)+0x2000000)+struct.pack('<BBHHI',0,6,1,25,0)
fixture+=b'\x29'+struct.pack('<H',0x829)+b'\x44'+struct.pack('<HH',717,1)+b'\x02'
m.inject(fixture)
before=m.read(ptr('gSaveBlock2Ptr'),3803)
# Unknown future records are preserved and never reinterpreted.
m.write(record(),b'\x5a'*144);native('QuestBook_Load')
assert m.read(record(),144)==b'\x5a'*144 and not native('QuestBook_IsReady')
assert not native('QuestBook_Discover',5) and not native('QuestBook_Accept',5)
# Older zero padding initializes without changing mode, settings or identity.
m.write(record(),bytes(144));native('QuestBook_Load')
assert native('QuestBook_IsReady')
after=m.read(ptr('gSaveBlock2Ptr'),3803)
assert after[:14]==before[:14] and after[19:]==before[19:],[(i,a,b) for i,(a,b) in enumerate(zip(before,after)) if a!=b]
assert not native('QuestBook_IsVisible',5)
assert not native('QuestBook_Discover',65535) and not native('QuestBook_ClaimReward',65535)
# Mode-specific definitions are hidden in Classic; mode is restored immediately.
mode=m.read(ptr('gSaveBlock2Ptr')+3795,8)
native('AdventureMode_SelectNewGame',0);native('AdventureMode_NewGame')
assert not native('QuestBook_GetDefinition',3) and not native('QuestBook_GetDefinition',4)
assert native('QuestBook_GetDefinition',1)
m.write(ptr('gSaveBlock2Ptr')+3795,mode)
assert native('QuestBook_GetDefinition',3)
warp('PalletTown_ProfessorOaksLab',6,9)
offer();assert m.read(record()+8+5*4,1)==b'\x01','Dialogue advance auto-accepted the optional quest'
m.snap('quest-offer');m.press(0,180)
assert state(5)==5, 'B must decline optional quest'
assert native('QuestBook_GetCompletedObjectives',5)==0
offer();m.press(8,180);assert state(5)==2
assert native('QuestBook_Track',5) and native('QuestBook_GetTracked')==5
native('QuestBook_NotifyNpc',5);assert state(5)==2,'Cannot report before visiting Route 1'
warp('Route1',10,10)
assert native('QuestBook_GetCompletedObjectives',5)==1
# Save via Flash and reset; never fabricate checksummed save bytes.
assert native('TrySavingData',0)==1
m.lib.retro_reset();m.run(360);m.press(3);m.press(8);m.press(8);m.run(180)
assert state(5)==2 and native('QuestBook_GetCompletedObjectives',5)==1
assert native('QuestBook_GetTracked')==5
warp('PalletTown_ProfessorOaksLab',6,9)
# Fill the ball pocket to exercise a failed, retryable reward.
assert native('AddBagItem',1,999)
offer();assert state(5)==3;m.snap('quest-ready-for-reward')
m.press(8,60);assert task_active('Task_GlassQuestOffer');m.snap('quest-reward-full-bag')
assert state(5)==3
m.press(0,180)
native('RemoveBagItem',1,999)
bag_before=native('CountTotalItemQuantityInBag',1) if 'CountTotalItemQuantityInBag' in m.symbols else 0
offer();m.press(8,180);assert state(5)==4
assert native('CountTotalItemQuantityInBag',1)==bag_before+3
assert not native('QuestBook_ClaimReward',5),'Reward must never duplicate'
assert native('CountTotalItemQuantityInBag',1)==bag_before+3
assert native('QuestBook_GetTracked')==255
assert native('TrySavingData',0)==1
m.lib.retro_reset();m.run(360);m.press(3);m.press(8);m.press(8);m.run(180)
assert state(5)==4 and not native('QuestBook_ClaimReward',5)
# Book UI can return to launcher and field after an NPC-owned overlay.
m.write(m.symbols['sHubCursor'],b'\x0d')
m.press(3);wait_task('Task_PokeGlassHub');m.snap('quest-launcher-third-page')
m.press(8);wait_task('Task_GlassQuestBook');m.run(60);m.snap('quest-book')
def check_borders():
 wid=m.read(m.symbols['sHubWindow'],1)[0]
 window=m.read(m.symbols['gWindows']+wid*12,12)
 data=m.read(struct.unpack_from('<I',window,8)[0],19200)
 def pixel(x,y):return data[((y//8)*30+x//8)*32+(y%8)*4+x%8//2]>>((x&1)*4)&15
 for x,y,w,h in [(12,42,96,91),(112,42,116,91)]:
  assert all(pixel(px,y)==6 and pixel(px,y+h-1)==6 for px in range(x,x+w))
  assert all(pixel(x,py)==6 and pixel(x+w-1,py)==6 for py in range(y,y+h))
for _ in range(3):
 for _ in range(16):check_borders();m.press(7,20)
 m.press(5,20)
m.snap('quest-book-detail-pages');m.press(2,30);m.press(2,30);m.snap('quest-book-side-filter')
check_borders()
m.press(0);wait_task('Task_PokeGlassHub');m.press(0)
assert m.read(m.symbols['sLockFieldControls'],1)==b'\0'
print('PASS unknown padding preserved; zero padding migration; mode filtering; real aide decline/accept; Route 1 event; Flash/reset persistence; full bag retry; exactly-once rewards; Quest Book return',flush=True)
