#!/usr/bin/env python3
"""Boot the actual draft ROM and walk every new border and cave transition."""
import json,struct
from pathlib import Path
import quantum_qol_emulator as m

groups=json.loads((m.root/'data/maps/map_groups.json').read_text())
ids={name:(g,n)for g,key in enumerate(groups['group_order'])for n,name in enumerate(groups[key])}
manifest=json.loads((m.root/'tools/vidra_drafts/manifest.json').read_text())
out=m.root/'docs/vidra/drafts/emulator';out.mkdir(parents=True,exist_ok=True)
def location():
    p=struct.unpack('<I',m.read(m.symbols['gSaveBlock1Ptr'],4))[0]
    pair=tuple(m.read(p+4,2));xy=struct.unpack('<hh',m.read(p,4))
    return pair,xy
def warp(name,x,y):
    g,n=ids[name];m.inject(b'\x39'+struct.pack('<BBBHH',g,n,255,x,y)+b'\x6b\x02');m.run(120)
    assert location()[0]==(g,n),(name,location())
def walk(key,frames=48):
    m.keys.add(key);m.run(frames);m.keys.clear();m.run(60)
def check(source,x,y,key,dest):
    warp(source,x,y);walk(key)
    assert location()[0]==ids[dest],(source,dest,location())
    print('Walked',source,'->',dest,location()[1],flush=True)

# Every outdoor edge, in both directions, is reached using real player input.
cases=[('WesternForest',60,1,4,'RainfallRoute'),('RainfallRoute',24,70,5,'WesternForest'),
 ('RainfallRoute',24,1,4,'Veyden'),('Veyden',24,46,5,'RainfallRoute'),
 ('Veyden',54,20,7,'LakewoodRoute'),('LakewoodRoute',1,20,6,'Veyden'),
 ('LakewoodRoute',62,20,7,'Lyrvik'),('Lyrvik',1,20,6,'LakewoodRoute'),
 ('Veyden',24,1,4,'HighlandAscent'),('HighlandAscent',24,70,5,'Veyden'),
 ('HighlandAscent',24,1,4,'Norvyn'),('Norvyn',24,46,5,'HighlandAscent')]
for source,x,y,key,dest in cases:check('VidraDraft_'+source,x,y,key,'VidraDraft_'+dest)
check('VidraDraft_WesternForest',8,15,4,'VidraDraft_CorvalaPassage')
check('VidraDraft_CorvalaPassage',49,38,5,'VidraDraft_WesternForest')
check('VidraDraft_CorvalaPassage',8,9,4,'VidraDraft_Corvala')
corvala=next(e for e in manifest if e['map']=='VidraDraft_Corvala');cx,cy=corvala['points']['cave']
check('VidraDraft_Corvala',cx,cy+1,4,'VidraDraft_CorvalaPassage')
# Havora entry is beyond the final puzzle gate; no puzzle bypass was added.
check('Havora_NorthQuadrant',10,12,4,'VidraDraft_WesternForest')
check('VidraDraft_WesternForest',80,75,5,'Havora_NorthQuadrant')

for e in manifest:
    for key in [next(iter(e['points']))]+([{'RainfallRoute':'falls','HighlandAscent':'snowline','WesternForest':'clearing','Corvala':'village'}.get(e['map'].removeprefix('VidraDraft_'))]if e['map'].removeprefix('VidraDraft_')in ['RainfallRoute','HighlandAscent','WesternForest','Corvala']else[]):
        if not key:continue
        warp(e['map'],*e['points'][key]);m.screen.resize((720,480)).save(out/(e['map']+'-'+key+'.png'))
print('PASS: twelve outdoor walking transitions, four cave warps, Havora entrance/return; all nine maps rendered')
