"""mGBA gameplay: native asset loading, seamless connections and ferry round trip."""
import struct
import havora_emulator_support as m

def warp(g,n,x,y):
 m.inject(b'\x39'+struct.pack('<BBBHH',g,n,255,x,y)+b'\x6b\x02');m.run(240)
def loc():
 p=struct.unpack('<I',m.read(m.symbols['gSaveBlock1Ptr'],4))[0]
 return tuple(m.read(p+4,2)),struct.unpack('<hh',m.read(p,4))
def walk(key,frames):
 m.keys.add(key);m.run(frames);m.keys.clear();m.run(60)
def step(key):
 before=loc();m.keys.add(key)
 for _ in range(40):
  m.run(1)
  if loc()!=before:break
 m.keys.clear();m.run(60)
 assert loc()!=before,("blocked step",key,before)
def ferry_to(target):
 for _ in range(20):
  if loc()[0]==target:break
  m.press(8,120)
 assert loc()[0]==target
 m.run(180)
 assert loc()[0]==target
def crossing(name,start,key,frames,target):
 warp(*start);walk(key,frames);print(name,loc(),flush=True);assert loc()[0]==target
 active=struct.unpack('<I',m.read(m.symbols['sSecondaryTilesetAnimCallback'],4))[0]
 havora=m.symbols['TilesetAnim_HavoraHarbor']
 assert ((active&~1)==(havora&~1))==(target in [(43,19),(43,20),(43,21)]),(name,'animation callback',hex(active))
 m.snap(name)
warp(43,19,20,16);m.snap('havora-ferry-arrival')
for name,start,key,frames,target in [
 ('west-out',(43,19,1,2),6,35,(43,20)),('west-in',(43,20,6,10),7,35,(43,19)),
 ('north-out',(43,19,5,1),4,35,(43,21)),('north-in',(43,21,5,6),5,35,(43,19)),
 ('approach-city',(43,20,1,10),6,35,(43,0)),('city-approach',(43,0,78,10),7,35,(43,20)),
 ('approach-corner-north',(43,20,6,3),7,35,(43,21)),('north-corner-west',(43,21,1,3),6,35,(43,20))]:crossing(name,start,key,frames,target)
warp(43,19,6,6);m.snap('havora-warehouses');warp(43,19,34,24);m.snap('havora-lighthouse')
warp(43,19,36,26);walk(4,1);m.press(8);m.snap('havora-lighthouse-sign');assert loc()[0]==(43,19);m.press(0)
# The lighthouse coping remains a continuous walking loop, including the new corners.
warp(43,19,36,26)
for _ in range(2):step(7)
for _ in range(7):step(4)
for _ in range(4):step(6)
for _ in range(2):step(5)
assert loc()==((43,19),(34,21));m.snap('havora-cape-coping')
# Walk the entire south promenade to the open-air boarding gate, without setup warps.
warp(43,19,15,21);step(4)
for _ in range(5):step(7)
for _ in range(2):step(4)
print('Boarding walk:',loc(),flush=True);assert loc()==((43,19),(20,18))
# Talk to the unchanged sailor prompt at its new central pier location.
walk(4,1);m.press(8);m.snap('havora-sailor-prompt')
ferry_to((3,5));print('Ferry return:',loc(),flush=True);m.snap('havora-return-vermilion');assert loc()[0]==(3,5)
m.inject(b'\x44'+struct.pack('<HH',829,1)+b'\x02');warp(3,5,24,32);walk(5,1);m.press(8)
ferry_to((43,19));print('Ferry outward:',loc(),flush=True);m.snap('havora-ferry-round-trip');assert loc()==((43,19),(20,16))
print('PASS: eight seamless crossings, harbor loading and original Stellar Ticket sailor/ferry round trip',flush=True)
# Verify that the returned player can actually disembark and walk.
m.press(0);m.press(0);walk(4,18)
print('After disembarking:',loc(),flush=True);assert loc()[0]==(43,19) and loc()[1][1]<16
m.snap('havora-ferry-free-control')
# Solid end lips and side lips must stop the player at the deck boundary.
assert loc()==((43,19),(20,14));walk(4,20);assert loc()==((43,19),(20,14))
warp(43,19,19,15);walk(6,20);assert loc()==((43,19),(19,15));m.snap('havora-dock-rails')
print('PASS: lighthouse coping loop and solid pier end/side boundaries',flush=True)
# Verify eight real DMA animation phases and keep a gameplay GIF for review.
import json
from PIL import Image
asset=json.loads((m.root/'tools/havora/assets.json').read_text())
anim=asset['animation'];address=0x06000000+anim['start']*32
warp(43,19,20,16);m.run(160)
# A house's actual graphics must remain fixed while the sea changes.
mid=asset['assets']['house']['metatiles'][1][1]
source=m.root/('data/tilesets/primary/havora_harbor/metatiles.bin' if mid<640 else 'data/tilesets/secondary/havora_harbor/metatiles.bin')
index=mid if mid<640 else mid-640
words=struct.unpack_from('<8H',source.read_bytes(),index*16)
roof=next(w&1023 for w in words if w&1023 not in asset['reserved_primary_tiles'] and w&1023<anim['start'])
roof_before=m.read(0x06000000+roof*32,32)
phases=[];screens=[]
for _ in range(8):
 m.run(16);phases.append(m.read(address,anim['slots']*32));screens.append(m.screen.copy().resize((720,480),Image.Resampling.NEAREST))
assert len(set(phases))==8,('water animation stalled',len(set(phases)))
assert len({s.tobytes() for s in screens})==8,'water animation not visible'
assert m.read(0x06000000+roof*32,32)==roof_before,'water animation overwrote a building'
screens[0].save(m.d/'havora-water-animation.gif',save_all=True,append_images=screens[1:],duration=267,loop=0,disposal=2)
m.snap('havora-expanded-waterfront')
print('PASS: eight water animation phases in VRAM and on screen; roof graphics unchanged',flush=True)
