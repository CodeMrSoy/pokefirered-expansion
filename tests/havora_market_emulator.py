"""Actual mGBA crossings, seven doorway round trips, market and ferry checks."""
import json,struct
import havora_emulator_support as m

def warp(g,n,x,y):
 m.inject(b'\x39'+struct.pack('<BBBHH',g,n,255,x,y)+b'\x6b\x02');m.run(240)
def loc():
 p=struct.unpack('<I',m.read(m.symbols['gSaveBlock1Ptr'],4))[0]
 return tuple(m.read(p+4,2)),struct.unpack('<hh',m.read(p,4))
def walk(key,frames):
 m.keys.add(key);m.run(frames);m.keys.clear();m.run(90)
def step(key):
 before=loc();m.keys.add(key)
 for _ in range(50):
  m.run(1)
  if loc()!=before:break
 m.keys.clear();m.run(120)
 assert loc()!=before,('blocked',key,before)
for name,start,key,target in [
 ('market-from-harbor',(43, 11,5,1),4,(43, 14)),
 ('market-to-harbor',(43, 14,5,62),5,(43, 11)),
 ('market-from-west',(43, 27,6,54),7,(43, 14)),
 ('market-to-west',(43, 14,1,54),6,(43, 27)),
 ('harbor-west',(43, 11,1,2),6,(43, 27)),
 ('west-harbor',(43, 27,6,66),7,(43, 11)),
 ('west-old-city',(43, 27,1,67),6,(43, 0)),
 ('old-city-west',(43, 0,46,67),7,(43, 27))]:
 warp(*start);walk(key,35);assert loc()[0]==target,(name,loc());m.snap(name)
print('PASS: eight seamless outdoor crossings',flush=True)
for left in [4,19]:
 warp(43, 14,left+1,40)
 for _ in range(3):step(4)
 assert loc()==((43, 14),(left+1,37)),('stair ascent',loc())
 m.snap('terrace-stair-'+str(left))
 # Actual player object currentElevation (low nibble byte 0x0B).
 player=m.read(m.symbols['gPlayerAvatar']+5,1)[0]
 assert m.read(m.symbols['gObjectEvents']+player*36+0x0B,1)[0]&15==4
 for _ in range(3):step(5)
 assert loc()==((43, 14),(left+1,40)),('stair descent',loc())
 assert m.read(m.symbols['gObjectEvents']+player*36+0x0B,1)[0]&15==3
warp(43, 14,12,40);walk(4,35);assert loc()==((43, 14),(12,40)),'cliff wall is walkable'
print('PASS: both stairways change actual player elevation 3/4 in both directions; cliff blocks direct climbing',flush=True)
groups=json.loads((m.root/'data/maps/map_groups.json').read_text())['gMapGroup_Havora']
district=json.loads((m.root/'data/maps/Havora_Market/map.json').read_text())
for i,e in enumerate(district['warp_events']):
 warp(43, 14,e['x'],e['y']+1);step(4)
 target=(43,groups.index('QuantumHavora'+json.loads((m.root/'tools/havora/market-district.json').read_text())['buildings'][i]['name']))
 assert loc()[0]==target,('entrance',i,loc(),target)
 m.snap('market-interior-'+str(i))
 warp(*target,4,6);walk(5,20)
 assert loc()[0]==(43, 14) and loc()[1]==(e['x'],e['y']+1),('exit',i,loc())
print('PASS: seven building entrances and correct outdoor return thresholds',flush=True)
for name,x,y in [('market-square',20,30),('market-homes',20,12),('market-shops',20,24),('market-trade-hall',20,9)]:
 warp(43, 14,x,y);m.snap(name)
# Test a real stall interaction and opening the Buy screen (gMain.callback2).
warp(43, 14,5,32);walk(4,1);m.press(8)
for _ in range(4):
 m.press(8,120)
 cb=struct.unpack('<I',m.read(m.symbols['gMain']+4,4))[0]
 if cb&~1==m.symbols['CB2_BuyMenu']&~1:break
assert cb&~1==m.symbols['CB2_BuyMenu']&~1,('shop not open',hex(cb))
m.snap('market-buy-menu');m.press(0);m.press(0);m.press(0);m.press(0)
print('PASS: market vendor opens native Buy menu',flush=True)
warp(43,groups.index('Havora_Provisions'),3,3);walk(6,1);m.press(8)
for _ in range(4):
 m.press(8,120)
 cb=struct.unpack('<I',m.read(m.symbols['gMain']+4,4))[0]
 if cb&~1==m.symbols['CB2_BuyMenu']&~1:break
assert cb&~1==m.symbols['CB2_BuyMenu']&~1,('indoor shop not open',hex(cb))
m.snap('market-provisions-buy');m.press(0);m.press(0);m.press(0);m.press(0)
print('PASS: indoor provisions clerk opens native Buy menu',flush=True)
# Original ferry round-trip unchanged by the district expansion.
warp(43, 11,20,18);walk(7,1);m.press(8)
for _ in range(25):
 if loc()[0]==(3,5):break
 m.press(8,120)
assert loc()[0]==(3,5);m.run(180)
m.inject(b'\x44'+struct.pack('<HH',829,1)+b'\x02');warp(3,5,24,32);walk(5,1);m.press(8)
for _ in range(25):
 if loc()[0]==(43, 11):break
 m.press(8,120)
m.run(180);assert loc()==((43, 11),(20,18)),loc()
m.press(0);m.press(0);walk(4,18);assert loc()==((43, 11),(20,17)),loc()
m.snap('market-ferry-preserved')
print('PASS: original ferry round-trip and disembarking',flush=True)
