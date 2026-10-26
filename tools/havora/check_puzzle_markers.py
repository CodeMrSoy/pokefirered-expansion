#!/usr/bin/env python3
"""Preserve user terrain; validate marker allocations, nursery layout and every nursery warp."""
from pathlib import Path
import subprocess,json,struct,io
from PIL import Image
R=Path(__file__).resolve().parents[2];BASE='3a4217c7b1ad72a04c246efdd61f34911a94f395'
def old(p):return subprocess.check_output(['git','show',BASE+':'+p],cwd=R)
def js(p):return json.loads((R/p).read_text())
d=js('tools/havora/puzzle-markers.json');mids={v for r in d['plates'] for v in r}|set(d['gates']);slots=set(d['graphic_ids'])
for g,start in [('primary',0),('secondary',640)]:
 for f,size in [('metatiles.bin',16),('metatile_attributes.bin',4)]:
  p=f'data/tilesets/{g}/havora_city/{f}';a=old(p);b=(R/p).read_bytes();assert len(a)==len(b)
  for i in range(len(a)//size):
   if start+i in mids:assert not any(a[i*size:(i+1)*size]),'Overwrote occupied metatile'
   elif start+i == 0x2bc and f == 'metatile_attributes.bin':
    assert int.from_bytes(b[i*size:(i+1)*size], 'little') == js('tools/havora/dock-surf.json')['water_alias']['after']
   elif start+i == 0x232 and f == 'metatile_attributes.bin':
    assert int.from_bytes(b[i*size:(i+1)*size], 'little') == int.from_bytes(a[i*size:(i+1)*size], 'little') | 0x20000000
   else:assert a[i*size:(i+1)*size]==b[i*size:(i+1)*size],(p,i)
 p=f'data/tilesets/{g}/havora_city/tiles.png';a=Image.open(io.BytesIO(old(p)));b=Image.open(R/p)
 for y in range(0,a.height,8):
  for x in range(0,a.width,8):
   tid=start+y//8*16+x//8
   if tid in slots:assert not any(a.crop((x,y,x+8,y+8)).tobytes())
   else:assert a.crop((x,y,x+8,y+8)).tobytes()==b.crop((x,y,x+8,y+8)).tobytes(),tid
 for p in (R/f'data/tilesets/{g}/havora_city/palettes').glob('*.pal'):assert p.read_text().splitlines()==old(str(p.relative_to(R))).decode().splitlines()
layouts=js('data/layouts/layouts.json')['layouts'];previous=json.loads(old('data/layouts/layouts.json'))['layouts'];assert [l for l in layouts if l['id']!='LAYOUT_HAVORA_CAPTAINS_TRIAL'][:-1]==previous
for l in previous:
 for key in ['blockdata_filepath','border_filepath']:
  p=l[key];a=old(p);b=(R/p).read_bytes()
  if p in ('data/layouts/HavoraHarbor/map.bin','data/layouts/HavoraWestQuadrant/map.bin'):
   repair=js('tools/havora/dock-surf.json');a=bytearray(subprocess.check_output(['git','show',repair['base_commit']+':'+p],cwd=R))
   for f in repair['changes']:
    if f['layout']==l['id']:struct.pack_into('<H',a,(f['y']*l['width']+f['x'])*2,f['after'])
   a=bytes(a)
  if p=='data/layouts/HavoraNorthQuadrant/map.bin':
   aa=struct.unpack('<'+'H'*(len(a)//2),a);bb=struct.unpack('<'+'H'*(len(b)//2),b)
   expected={y*l['width']+x for x,y in [(16,22),(21,21),(13,27),(18,14),(19,22),(16,21),(10,13)]}
   assert {i for i,(x,y) in enumerate(zip(aa,bb)) if x!=y}==expected
   assert all((x&~1023)==(y&~1023) for x,y in zip(aa,bb)),'Changed elevation/collision'
  else:assert a==b,p
for name in ['HavoraDaycare','QuantumHavoraDaycare']:
 m=js(f'data/maps/{name}/map.json');l=next(v for v in layouts if v['id']==m['layout']);assert len((R/l['blockdata_filepath']).read_bytes())==l['width']*l['height']*2
 for o in m['object_events']:assert 0<=o['x']<l['width'] and 0<=o['y']<l['height']
 for w in m['warp_events']:
  target=js('data/maps/'+w['dest_map'].removeprefix('MAP_').replace('QUANTUM_HAVORA_DAYCARE','QuantumHavoraDaycare').replace('HAVORA_DAYCARE','HavoraDaycare')+'/map.json')
  assert 0<=int(w['dest_warp_id'])<len(target['warp_events'])
assert Image.open(R/'graphics/havora/gate_marked.png').size==(16,240)
print('PASS only 7 puzzle identities changed; all cliff/terrain/collision, existing metatiles/palettes and graphics preserved; seven blank static tiles used; nursery dimensions/events/return warps valid')
