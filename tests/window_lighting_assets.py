#!/usr/bin/env python3
"""Check glass-only palette isolation and optional daytime equivalence."""
import argparse,json,re,struct,subprocess
from pathlib import Path
root=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser();parser.add_argument('--baseline-ref');args=parser.parse_args()
manifest=json.loads((root/'data/tilesets/window_lighting.json').read_text())
headers=(root/'src/data/tilesets/headers.h').read_text()
objects=dict(re.findall(r'const struct Tileset gTileset_(\w+)\s*=\s*\{(.*?)\};',headers,re.S))
def palette(path):
 return [tuple(int(n)//8 for n in line.split()) for line in path.read_text().splitlines()[3:]]
for name in ('General','GeneralSummer','GeneralAutumn','GeneralWinter'):
 assert int(re.search(r'lightPalettes = (0x\w+)',objects[name]).group(1),16)==0x0c,name
for r in manifest['secondary_rules']:
 folder=root/r['folder'];src=r['source_palette'];clone=r['clone_palette']
 original=palette(folder/f'palettes/{src:02}.pal');isolated=palette(folder/f'palettes/{clone:02}.pal')
 assert original[1:]==isolated[1:],(r['tileset'],'Daytime palette colors changed')
 raw=(root/r['metatiles']).read_bytes();entries=struct.unpack('<'+'H'*(len(raw)//2),raw)
 mask=int(re.search(r'lightPalettes = (0x\w+)',objects[r['tileset']]).group(1),16)
 assert bool(mask&1)==r['glass_clone'],r['tileset']
 for i,e in enumerate(entries):
  mid=640+i//8;glass=mid in r['glass_metatiles'] if r['glass_metatiles'] is not None else mid not in r['unlit_metatiles']
  if e>>12 in (src,clone):
   override=any(o['metatile']==mid and o['quadrant']==i%8 for o in r.get('glass_overrides',[]))
   expected=src if override else (clone if (glass if r['glass_clone'] else not glass) else src)
   assert e>>12==expected,(r['tileset'],hex(mid),'Wrong light isolation')
 if args.baseline_ref:
  before=subprocess.check_output(['git','show',args.baseline_ref+':'+r['metatiles']],cwd=root)
  old=struct.unpack('<'+'H'*(len(before)//2),before)
  assert len(old)==len(entries)
  for a,b in zip(old,entries):
   assert a&0xfff==b&0xfff,(r['tileset'],'Tile graphics or flips changed')
   assert a==b or {a>>12,b>>12}=={src,clone},(r['tileset'],'Unexpected palette change')
print('Glass/ground separation and identical daytime colors passed for',len(manifest['secondary_rules']),'tileset variants')
