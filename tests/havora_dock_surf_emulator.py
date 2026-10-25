"""Real Surf launch/dismount at each repaired Havora dock end (mGBA)."""
import json,struct,pathlib,os,subprocess
import havora_emulator_support as m
source=(m.root/'tests/avatar_wardrobe_emulator.py').read_text()
exec(source[source.index('native_dir ='):source.index('avatar_var = native')].replace('ldr r3, function', 'ldr r4, function').replace('bx r3', 'bx r4'))
groups=json.loads((m.root/'data/maps/map_groups.json').read_text())
ids={n:(g,i) for g,k in enumerate(groups['group_order']) for i,n in enumerate(groups[k])}
layouts={l['id']:l for l in json.loads((m.root/'data/layouts/layouts.json').read_text())['layouts']}
fixes=json.loads((m.root/'tools/havora/dock-surf.json').read_text())['changes']
# Also cover unchanged dock sides, including the duplicate-water perimeter.
for lid in ['LAYOUT_HAVORA_HARBOR','LAYOUT_HAVORA_WEST_QUADRANT']:
 l=layouts[lid];raw=(m.root/l['blockdata_filepath']).read_bytes();bs=struct.unpack('<'+'H'*(len(raw)//2),raw)
 existing={(f['x'],f['y']) for f in fixes if f['layout']==lid}
 for j,b in enumerate(bs):
  if b&1023 in [0x281,*range(0x28f,0x296)] and not b&0xc00 and (j%l['width'],j//l['width']) not in existing:
   fixes.append({'layout':lid,'x':j%l['width'],'y':j//l['width']})
# Surf's normal animation uses party slot 0. We test native traversal independently
# of the player's badge/party progression; eligibility is checked separately.
fixture=b'\x23'+struct.pack('<I',(m.symbols['ScrCmd_createmon']|1)+0x2000000)+struct.pack('<BBHHI',0,6,131,25,0)+b'\x02'
m.inject(fixture)
def obj():return m.symbols['gObjectEvents']+m.read(m.symbols['gPlayerAvatar']+5,1)[0]*36
def pos():
 x,y=struct.unpack('<hh',m.read(obj()+16,4));return x-7,y-7
def surf():return bool(m.read(m.symbols['gPlayerAvatar'],1)[0]&8)
def warp(name,x,y):
 g,n=ids[name];m.inject(b'\x39'+struct.pack('<BBBHH',g,n,255,x,y)+b'\x6b\x02');m.run(100)
 assert pos()==(x,y),(name,pos(),(x,y))
attrs=[]
for group in ['primary','secondary']:
 b=(m.root/f'data/tilesets/{group}/havora_city/metatile_attributes.bin').read_bytes();attrs+=struct.unpack('<'+'I'*(len(b)//4),b)
count=0
for fix in fixes:
 l=layouts[fix['layout']];name={'LAYOUT_HAVORA_HARBOR':'HavoraHarbor','LAYOUT_HAVORA_WEST_QUADRANT':'HavoraWestQuadrant'}[fix['layout']]
 data=(m.root/l['blockdata_filepath']).read_bytes();blocks=struct.unpack('<'+'H'*(len(data)//2),data)
 x,y=fix['x'],fix['y'];tested=0
 for dx,dy,direction,key,back in [(0,1,1,5,4),(0,-1,2,4,5),(-1,0,3,6,7),(1,0,4,7,6)]:
  nx,ny=x+dx,y+dy
  if not(0<=nx<l['width'] and 0<=ny<l['height']):continue
  b=blocks[ny*l['width']+nx]
  if not ((attrs[b&1023]>>9)&2) or b&0xc00:continue
  objects=json.loads((m.root/f'data/maps/{name}/map.json').read_text())['object_events']
  if any((o['x'],o['y'])==(nx,ny) for o in objects):continue
  warp(name,x,y)
  m.press(key,20)
  assert pos()==(x,y),('walked onto water without Surf',name,pos())
  ready=native('IsPlayerFacingSurfableFishableWater')
  assert ready==1,(name,x,y,direction,'Surf unavailable',ready,native('PlayerGetElevation'),native('GetCollisionAtCoords',obj(),nx+7,ny+7,direction),native('MapGridGetElevationAt',nx+7,ny+7),m.read(obj(),36).hex())
  m.write(m.symbols['gFieldEffectArguments'],b'\0'*4)
  native('FieldEffectStart',10);m.run(500)
  assert surf() and pos()==(nx,ny),(name,x,y,'launch failed',pos(),surf())
  if tested==0:m.snap('dock-surf-'+name+'-'+str(x)+'-'+str(y))
  m.keys.add(back);m.run(12);m.keys.clear();m.run(90)
  assert not surf() and pos()==(x,y),(name,x,y,'dismount failed',pos(),surf())
  count+=1;tested+=1
 if not tested:print('BLOCKED',name,(x,y),'adjacent decorative boat or dock, no open-water edge',flush=True)
 print('PASS',name,(x,y),'Surf launch/return',tested,'directions',flush=True)
print('PASS',len(fixes),'dock-end cells audited;',count,'native Surf launch/dismount round trips',flush=True)
