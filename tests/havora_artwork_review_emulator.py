"""Validate the artwork-first default, independent levels and legacy migration."""
import os,pathlib,struct,subprocess,json
import havora_emulator_support as m
s=(m.root/'tests/avatar_wardrobe_emulator.py').read_text();exec(s[s.index('native_dir ='):s.index('avatar_var = native')])
import sys
sys.path.insert(0,str(m.root/'tools/havora'));import overhead_lock_geometry as geo
j=json.loads((m.root/'data/maps/map_groups.json').read_text());ids={name:(g,n) for g,k in enumerate(j['group_order']) for n,name in enumerate(j[k])}
def warp(x=3,y=25):
 g,n=ids['QuantumHavoraGym'];m.inject(b'\x39'+struct.pack('<BBBHH',g,n,255,x,y)+b'\x6b\x02');m.run(120)
def value(v):return native('VarGet',v)&65535
def encode(w):return 0x4400+w[0]+3*w[1]+9*w[2]
def command(cmd,a=0,b=0):
 for var,v in [(0x8004,cmd),(0x8005,a),(0x8006,b)]:native('VarSet',var,v)
 native('HavoraGym_Control')
 for _ in range(2000):
  if not m.read(m.symbols['gPlayerAvatar']+6,1)[0]:break
  m.run(1)
 else:raise AssertionError('preview/reset task did not finish')
 m.run(40);return value(0x800d)
def assert_map(w):
 width,height,address=struct.unpack('<iiI',m.read(m.symbols['VMap'],12));expected=geo.draw((w,0,0,4,0,False))
 for y in range(geo.H):
  got=struct.unpack('<80H',m.read(address+2*((y+7)*width+7),160))
  assert list(got)==expected[y*80:(y+1)*80],('runtime differs from authored artwork',w,y,next((x,hex(a),hex(b)) for x,(a,b) in enumerate(zip(got,expected[y*80:(y+1)*80])) if a!=b))
native('VarSet',0x40d8,63);native('VarSet',0x40d7,0xA408);warp()
assert value(0x40d7)==encode((0,0,0)),'old gym save did not migrate to all LOW'
assert value(0x40d8)==63,'migration lost trainer victories'
assert_map((0,0,0));m.snap('artwork-default-all-low')
print('PASS old-save migration and all-LOW runtime map matches restored artwork',flush=True)
for cmd,args in [(10,(0,1)),(11,(0,2)),(12,()),(13,()),(14,()),(20,(0,))]:
 before=value(0x40d7);assert command(cmd,*args)==9 and value(0x40d7)==before,('old puzzle still edits artwork',cmd)
print('PASS old transfer, sailing and mooring geometry disabled during artwork review',flush=True)
current=[0,0,0]
for levels in [(2,0,0),(1,2,1),(0,1,2),(0,0,0)]:
 for ch,target in enumerate(levels):
  while current[ch]!=target:
   current[ch]+=1 if target>current[ch] else -1
   assert command(26,ch,current[ch])==1
   assert value(0x40d7)==encode(current)
   assert_map(current)
 assert value(0x40d7)==encode(levels)
 m.snap('artwork-profile-'+''.join(map(str,levels)))
print('PASS animated independent height profiles match all three supplied references',flush=True)
native('VarSet',0x40d7,encode((2,0,0)));warp();assert value(0x40d7)==encode((2,0,0));assert_map((2,0,0))
assert command(15)==1;assert value(0x40d7)==encode((0,0,0));assert_map((0,0,0))
assert value(0x40d8)==63
warp();assert_map((0,0,0))
print('PASS re-entry and reset retain the authored default and trainer victories',flush=True)
