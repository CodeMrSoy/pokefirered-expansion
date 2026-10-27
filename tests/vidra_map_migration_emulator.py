#!/usr/bin/env python3
"""Exercise every legacy Vidra map pair and one-time save migration in mGBA."""
import json,struct,pathlib
import quantum_qol_emulator as m
helpers=pathlib.Path(__file__).with_name('rom_cleanup_migration_emulator.py').read_text().split("old=(m.root")[0].replace('import quantum_qol_emulator as m','')
exec(compile(helpers,'vidra_native_helpers','exec'))
manifest=json.loads((m.root/'docs/vidra/map-renames.json').read_text())
groups=json.loads((m.root/'data/maps/map_groups.json').read_text())
expected={name:(g,i) for g,key in enumerate(groups['group_order']) for i,name in enumerate(groups[key])}
save=ptr('gSaveBlock1Ptr');version=native('GetVarPointer',0x40fc)
assert m.read(version,2)==b'\x01\x00','New game lacks current map version'
for e in manifest['maps']:
 m.write(version,b'\0\0')
 for offset in (4,12,20,28,36):m.write(save+offset,struct.pack('<bbb x hh',manifest['legacy_group'],e['old_number'],-1,6,7))
 native('VidraMigrateMapIds')
 for offset in (4,12,20,28,36):
  assert m.read(save+offset,2)==bytes(expected[e['new']]),e
  assert m.read(save+offset+4,4)==struct.pack('<hh',6,7),'Migration changed warp coordinates'
 snapshot=m.read(save+4,40)
 native('VidraMigrateMapIds');assert m.read(save+4,40)==snapshot,'Migration applied twice'
# Vanilla locations must not be changed by the Vidra-only conversion.
m.write(version,b'\0\0');m.write(save+4,struct.pack('<bbb x hh',3,0,-1,10,9))
native('VidraMigrateMapIds');assert m.read(save+4,2)==bytes((3,0))
for name in ('Havora_WestQuadrant','Corvala_Town','Eldervale_Village','Myrdal_City','Iskora_Village'):
 group,num=expected[name]
 m.inject(b'\x39'+struct.pack('<BBBHH',group,num,255,10,10)+b'\x6b\x02');m.run(120)
 save=ptr('gSaveBlock1Ptr')
 assert m.read(save+4,2)==bytes((group,num)),name
 m.snap('vidra-'+name.lower())
print('All 50 legacy maps: five saved warps migrated, coordinates preserved, version/idempotence and vanilla location checks passed; five settlements rendered')
