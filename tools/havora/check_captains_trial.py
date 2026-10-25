"""Preserve Havora outdoors and independently solve the native gym state graph."""
from pathlib import Path
from collections import deque
import json,struct,subprocess
R=Path(__file__).resolve().parents[2];BASE='0b13302d7807bd5df1df20712a77335a6ebf17dd'
old=lambda p:subprocess.check_output(['git','show',BASE+':'+p],cwd=R)
ls=json.loads((R/'data/layouts/layouts.json').read_text())['layouts'];before=json.loads(old('data/layouts/layouts.json'))['layouts'];assert ls[:-1]==before
for l in before:
 for k in ['blockdata_filepath','border_filepath']:assert old(l[k])==(R/l[k]).read_bytes(),l[k]
for p in subprocess.check_output(['git','ls-tree','-r','--name-only',BASE,'--','data/maps','data/tilesets'],cwd=R,text=True).splitlines():
 if p.startswith('data/maps/QuantumHavoraGym/'):continue
 a=old(p);b=(R/p).read_bytes()
 if p.endswith('.pal'):a=a.replace(b'\r\n',b'\n');b=b.replace(b'\r\n',b'\n')
 assert a==b,p
l=ls[-1];assert (l['width'],l['height'])==(80,54)
w=struct.unpack('<4320H',(R/l['blockdata_filepath']).read_bytes());m=json.loads((R/'data/maps/QuantumHavoraGym/map.json').read_text());actors={(o['x'],o['y']) for o in m['object_events']}
for e in m['object_events']+m['bg_events']+m['warp_events']:assert 0<=e['x']<80 and 0<=e['y']<54
assert len(m['warp_events'])==3 and all(e['dest_map']=='MAP_HAVORA_WEST_QUADRANT' and e['dest_warp_id']=='0' for e in m['warp_events'])

import runpy
runpy.run_path(str(R/'tools/havora/check_fixed_transfer_map.py'),run_name='__main__')
print('PASS all original outdoor maps, cliffs, tilesets, events, warps and connections preserved')
