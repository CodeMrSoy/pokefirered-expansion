"""Headless mGBA gameplay checks using an injected warp only for test setup."""
import struct
import havora_emulator_support as m

def warp(g,n,x,y):
 m.inject(b'\x39'+struct.pack('<BBBHH',g,n,255,x,y)+b'\x6b\x02');m.run(240)
def loc():
 p=struct.unpack('<I',m.read(m.symbols['gSaveBlock1Ptr'],4))[0]
 return tuple(m.read(p+4,2)),struct.unpack('<hh',m.read(p,4))
def walk(key,frames):
 m.keys.add(key);m.run(frames);m.keys.clear();m.run(60)
warp(43,19,8,5);assert loc()[0]==(43,19);m.snap('harbor-ferry-arrival')
warp(43,0,78,2);walk(7,48);print('East crossing:',loc(),flush=True);assert loc()[0]==(43,19);m.snap('harbor-city-seam-east')
walk(6,70);print('West crossing:',loc(),flush=True);assert loc()[0]==(43,0);m.snap('harbor-city-seam-west')
warp(43,19,24,15);m.snap('harbor-market')
warp(43,0,43,14);m.snap('havora-east-district')
warp(43,19,8,5);walk(5,1);m.press(8);m.snap('harbor-sailor-prompt')
# Agree to the existing return prompt; dismiss departure text.
for _ in range(7):m.press(8,120)
m.run(900);print('Ferry return:',loc(),flush=True);m.snap('ferry-return-vermilion');assert loc()[0]==(3,5)
print('PASS: Harbor and city load; outdoor seam crosses both ways; original sailor returns to Vermilion',flush=True)

# Give only the ticket fixture, then use the unmodified Vermilion sailor.
m.inject(b'\x44'+struct.pack('<HH',829,1)+b'\x02')
warp(3,5,24,32);walk(5,1);m.press(8)
for _ in range(7):m.press(8,120)
m.run(900);print('Ferry outward:',loc(),flush=True);m.snap('ferry-round-trip-arrival');assert loc()==((43,19),(8,5))
print('PASS: Stellar Ticket ferry round trip returns to the original Havora landing',flush=True)
