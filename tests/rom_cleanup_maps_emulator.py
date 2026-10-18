#!/usr/bin/env python3
"""Inspect retired entrances, the Route 20 crossing and replacement encounters."""
import struct
import quantum_qol_emulator as m

def warp(g,n,x,y):
 m.inject(b'\x39'+struct.pack('<BBBHH',g,n,255,x,y)+b'\x6b\x02');m.run(240)
def position():
 p=struct.unpack('<I',m.read(m.symbols['gSaveBlock1Ptr'],4))[0]
 return struct.unpack('<hh',m.read(p,4))
warp(5,4,10,4);m.snap('cleanup-center-finished')
warp(5,4,2,6);m.snap('cleanup-center-stairs-removed')
m.press(6,240)
p=struct.unpack('<I',m.read(m.symbols['gSaveBlock1Ptr'],4))[0]
assert m.read(p+4,2)==bytes((5,4)),'Retired stairs changed maps'
warp(3,38,72,15);m.keys.add(4);m.run(20);m.keys.clear();m.run(300);left=position();m.snap('cleanup-route20-crossing-west')
assert abs(left[0]-60)<=1 and 8<=left[1]<=10,('West crossing',left)
warp(3,38,60,9);m.keys.add(4);m.run(20);m.keys.clear();m.run(300);right=position();m.snap('cleanup-route20-crossing-east')
assert abs(right[0]-72)<=1 and 14<=right[1]<=16,('East crossing',right)
warp(1,62,4,9);m.snap('cleanup-mewtwo-pre-ending')
# FLAG_SYS_GAME_CLEAR = SYS_FLAGS (0x800) + 0x2c.
m.inject(b'\x29'+struct.pack('<H',0x82c)+b'\x02')
warp(1,62,4,9);m.snap('cleanup-mewtwo-post-ending')
warp(3,38,67,5);m.snap('cleanup-articuno')
warp(3,42,8,32);m.snap('cleanup-moltres')
warp(3,12,10,9)
p=struct.unpack('<I',m.read(m.symbols['gSaveBlock1Ptr'],4))[0]
assert m.read(p+4,2)==bytes((3,0)) and position()==(10,9),'Retired runtime warp was not recovered'
print('Retired stairs stay closed; Route20 crosses both ways; replacement encounter map screens rendered')
