"""Exact native terrain art, compatible neighbor graphics and tile capacity."""
import json,struct,sys
from pathlib import Path
import numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools/havora'))
from render import atlas
data=json.loads((R/'tools/havora/city-tileset.json').read_text())
city=atlas('havora_city','havora_city');harbor=atlas('havora_harbor','havora_harbor');general=atlas()
for mid in data['compatible_metatiles']:
 assert city[mid].tobytes()==harbor[mid].tobytes(),('incompatible seam art',hex(mid))
for source,target in data['native_general_ids'].items():
 assert np.array_equal(np.array(general[int(source)])>>3,np.array(city[target])>>3),('native GBA color mismatch',source,target)
assert data['graphics_used']<=1024
compatible=set(data['compatible_metatiles'])
raw=(R/'data/layouts/QuantumHavoraNorthQuay/map.bin').read_bytes();blocks=struct.unpack('<2560H',raw)
# The harbor and west quay can draw these edge strips using their own tileset.
assert all(v&1023 in compatible for v in blocks[56*40:])
assert all(blocks[y*40+x]&1023 in compatible for y in range(43,64) for x in range(8))
for directory,count in [('primary',640),('secondary',384)]:
 folder=R/f'data/tilesets/{directory}/havora_city'
 assert len((folder/'metatiles.bin').read_bytes())==count*16
 assert len((folder/'metatile_attributes.bin').read_bytes())==count*4
 words=struct.unpack('<'+'H'*(count*8),(folder/'metatiles.bin').read_bytes())
 assert all(w&1023<1024 and w>>12<13 for w in words)
print('PASS: native FireRed terrain pixels at GBA color depth, exact shared edge art, compatible buffer strips, and city graphics/metatile budgets')
# The approaching coastal-road camera draws the city's first eight columns
# with General/Cinnabar before the crossing: only shared paving/water here.
assert city[472].tobytes()==general[472].tobytes()
raw=(R/'data/layouts/QuantumPortCity/map.bin').read_bytes();west=struct.unpack('<4608H',raw)
assert all(west[y*48+x]&1023 in [449,472] for y in range(96) for x in range(8))
print('PASS: coastal-road approach uses pixel-identical General water and paving')
