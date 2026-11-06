"""Targeted final-ROM water-art and gym traversal check after pool-tile repair."""
import json,struct
import havora_emulator_support as m
m.d=m.root/'build/corvala/pool-emulator';m.d.mkdir(parents=True,exist_ok=True)
groups=json.loads((m.root/'data/maps/map_groups.json').read_text())
ids={n:(g,i) for g,k in enumerate(groups['group_order']) for i,n in enumerate(groups[k])}
layouts={v['id']:v for v in json.loads((m.root/'data/layouts/layouts.json').read_text())['layouts']}
def pos():
 obj=m.symbols['gObjectEvents']+m.read(m.symbols['gPlayerAvatar']+5,1)[0]*36
 x,y=struct.unpack('<hh',m.read(obj+16,4));return x-7,y-7
def map_id():
 p=struct.unpack('<I',m.read(m.symbols['gSaveBlock1Ptr'],4))[0];return tuple(m.read(p+4,2))
def warp(name,x,y):
 g,i=ids[name];m.inject(b'\x39'+struct.pack('<BBBHH',g,i,255,x,y)+b'\x6b\x02');m.run(120)
 assert map_id()==ids[name] and pos()==(x,y)
 data=json.loads((m.root/f'data/maps/{name}/map.json').read_text());l=layouts[data['layout']]
 raw=(m.root/l['blockdata_filepath']).read_bytes();vw,vh,ptr=struct.unpack('<iiI',m.read(m.symbols['VMap'],12));w,h=l['width'],l['height']
 for yy in range(h):assert m.read(ptr+2*((yy+7)*vw+7),w*2)==raw[yy*w*2:(yy+1)*w*2]
 assert b'\xcb\x1e' not in raw
def step(key,expected):
 before=pos();m.keys.add(key)
 for _ in range(50):
  m.run(1)
  if pos()!=before:break
 m.keys.clear();m.run(32);assert pos()==expected
warp('Corvala_TidalGym',13,20)
for y in range(19,4,-1):
 step(4,(13,y))
 if y==14:m.snap('gym-lower-tide-basins')
 if y==9:m.snap('gym-main-pool')
for y in range(6,21):step(5,(13,y))
m.keys.add(5);m.run(40);m.keys.clear();m.run(200)
assert map_id()==ids['Corvala_Town'] and pos()==(12,9)
warp('Corvala_EntranceCave',14,14);m.snap('entrance-cave-pool')
print('PASS: final ROM loads both repaired pool maps; gym crossing and return work',flush=True)
