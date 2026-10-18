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
 warp(*start);walk(key,frames);print(name,loc(),flush=True);assert loc()[0]==target;m.snap(name)
warp(43,19,20,16);m.snap('havora-ferry-arrival')
for name,start,key,frames,target in [
 ('west-out',(43,19,1,2),6,35,(43,20)),('west-in',(43,20,6,10),7,35,(43,19)),
 ('north-out',(43,19,5,1),4,35,(43,21)),('north-in',(43,21,5,6),5,35,(43,19)),
 ('approach-city',(43,20,1,10),6,35,(43,0)),('city-approach',(43,0,78,10),7,35,(43,20)),
 ('approach-corner-north',(43,20,6,3),7,35,(43,21)),('north-corner-west',(43,21,1,3),6,35,(43,20))]:crossing(name,start,key,frames,target)
warp(43,19,6,6);m.snap('havora-warehouses');warp(43,19,34,24);m.snap('havora-lighthouse')
warp(43,19,36,26);walk(4,1);m.press(8);m.snap('havora-lighthouse-sign');assert loc()[0]==(43,19);m.press(0)
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
