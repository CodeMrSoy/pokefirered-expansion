"""Verify dock-only elevation repairs; no artwork, events, collision or cliffs change."""
from pathlib import Path
import json,struct,subprocess
R=Path(__file__).resolve().parents[2]
d=json.loads((R/'tools/havora/dock-surf.json').read_text())
layouts=json.loads((R/'data/layouts/layouts.json').read_text())['layouts']
old=lambda p:subprocess.check_output(['git','show',d.get('integration_base',d['base_commit'])+':'+p],cwd=R)
count=0
for l in layouts:
 if l['id']=='LAYOUT_HAVORA_GYM':continue # Covered by check_captains_trial.py.
 for key in ['blockdata_filepath','border_filepath']:
  p=l[key];a=old(p);b=(R/p).read_bytes();expected=bytearray(a)
  if key=='blockdata_filepath':
   for f in d['changes']:
    if f['layout']!=l['id']:continue
    off=(f['y']*l['width']+f['x'])*2
    assert int.from_bytes(a[off:off+2],'little')==f['before']
    assert f['before']>>12==1 and f['after']>>12==3
    assert f['before']&4095==f['after']&4095
    struct.pack_into('<H',expected,off,f['after']);count+=1
  assert bytes(expected)==b,p
for p in subprocess.check_output(['git','ls-tree','-r','--name-only',d['base_commit'],'--','data/maps','data/tilesets'],cwd=R,text=True).splitlines():
 if p.startswith('data/maps/Havora_Gym/'):continue # Approved interior replacement.
 a=old(p);b=(R/p).read_bytes()
 if p=='data/tilesets/secondary/havora_city/metatile_attributes.bin':
  a=bytearray(a);v=d['water_alias'];assert struct.unpack_from('<I',a,(v['metatile']-640)*4)[0]==v['before'];struct.pack_into('<I',a,(v['metatile']-640)*4,v['after']);a=bytes(a)
 if p.endswith('.pal'):a=a.replace(b'\r\n',b'\n');b=b.replace(b'\r\n',b'\n')
 assert a==b,p
meta=(R/'data/tilesets/secondary/havora_city/metatiles.bin').read_bytes()
v=d['water_alias'];a=(v['metatile']-640)*16;b=(v['source']-640)*16
assert meta[a:a+16]==meta[b:b+16], 'Water alias is not the identical graphic'
assert count==15
print('PASS 15 dock-end elevations 1 -> 3; one identical water graphic gains proper water attributes; every other layout/border, graphic, attribute, collision, header, event and ferry warp preserved')
