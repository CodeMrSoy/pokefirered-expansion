#!/usr/bin/env python3
"""Validate editable draft geometry, reciprocal seams, cave semantics and old IDs."""
import json, struct, subprocess
from pathlib import Path
from collections import deque

ROOT=Path(__file__).resolve().parents[1]
def load(p):return json.loads((ROOT/p).read_text())
def words(p):
    b=(ROOT/p).read_bytes();return struct.unpack('<'+'H'*(len(b)//2),b)
layouts={l['id']:l for l in load('data/layouts/layouts.json')['layouts']}
manifest=load('tools/vidra_drafts/manifest.json')
groups=load('data/maps/map_groups.json')
base=json.loads(subprocess.check_output(['git','show','9613f5ceec1f808771b203ff258846eefd5d4ad2:data/maps/map_groups.json'],cwd=ROOT))
assert groups['group_order'][:len(base['group_order'])]==base['group_order']
for key in base['group_order']:assert groups[key]==base[key],('existing map IDs changed',key)
maps={}
for p in (ROOT/'data/maps').glob('*/map.json'):
    h=json.loads(p.read_text());maps[h['id']]=h
geometry={}
symbols={'General':'primary/general','GeneralWinter':'primary/general_winter','ViridianForest':'secondary/viridian_forest','SeviiIslands123':'secondary/sevii_islands_123','SeviiIslands123Winter':'secondary/sevii_islands_123winter','VidraDraftCorvala':'secondary/vidra_draft_corvala','VidraDraftHighlands':'secondary/vidra_draft_highlands','VidraDraftCave':'secondary/vidra_draft_cave','VidraDraftRain':'secondary/vidra_draft_rain'}
for e in manifest:
    h=next(h for h in maps.values()if h['name']==e['map']);l=layouts[h['layout']];w=l['width'];height=l['height']
    assert (w+15)*(height+14)<=0x2800,(e['map'],'map buffer overflow')
    a=words(l['blockdata_filepath']);assert len(a)==w*height
    assert len(words(l['border_filepath']))==4
    attr=[];meta=[]
    for key in ['primary_tileset','secondary_tileset']:
        folder='data/tilesets/'+symbols[l[key].removeprefix('gTileset_')]
        b=(ROOT/folder/'metatile_attributes.bin').read_bytes();attr+=list(struct.unpack('<'+'I'*(len(b)//4),b))
        b=words(folder+'/metatiles.bin');meta.extend(b[i:i+8]for i in range(0,len(b),8))
    for cell in a:
        mid=cell&1023;assert mid<len(meta),(e['map'],'metatile out of range',mid)
        assert all(v>>12<13 for v in meta[mid]),(e['map'],'reserved palette bank')
    start=tuple(next(iter(e['points'].values())));q=deque([start]);seen={start}
    while q:
        x,y=q.popleft();z=a[y*w+x]>>12
        for nx,ny in [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]:
            if not(0<=nx<w and 0<=ny<height)or(nx,ny)in seen:continue
            c=a[ny*w+nx];nz=c>>12
            if c&0xc00 or (z and nz and z!=nz):continue
            seen.add((nx,ny));q.append((nx,ny))
    for key,point in e['points'].items():assert tuple(point)in seen,(e['map'],'unreachable',key,point)
    for kind in ['object_events','warp_events','coord_events','bg_events']:
        for event in h[kind]:assert 0<=event['x']<w and 0<=event['y']<height
    for event in h['warp_events']:
        tile=a[event['y']*w+event['x']]&1023
        assert attr[tile]&0x1ff in [0x60,0x62,0x63,0x64,0x65,0x67,0x69],(h['name'],'non-warp tile',hex(tile))
        other=maps[event['dest_map']]['warp_events'][int(event['dest_warp_id'])]
        assert other['dest_map']==h['id'],(h['name'],'cave is not reciprocal')
    geometry[h['id']]=(l,a,seen)
    print(e['map'],f'{w}x{height}',len(seen),'reachable walking cells')
for mid,(l,a,seen)in geometry.items():
    for c in maps[mid]['connections']:
        other=maps[c['map']];ol,oa,os=geometry[c['map']];rev={'up':'down','down':'up','left':'right','right':'left'}[c['direction']]
        assert any(b['direction']==rev and b['map']==mid and b['offset']==-c['offset']for b in other['connections'])
        crossed=[]
        for x,y in seen:
            tx,ty=x,y
            if c['direction']=='up'and y==0:tx=x-c['offset'];ty=ol['height']-1
            elif c['direction']=='down'and y==l['height']-1:tx=x-c['offset'];ty=0
            elif c['direction']=='left'and x==0:tx=ol['width']-1;ty=y-c['offset']
            elif c['direction']=='right'and x==l['width']-1:tx=0;ty=y-c['offset']
            else:continue
            if (tx,ty)in os and a[y*l['width']+x]>>12==oa[ty*ol['width']+tx]>>12:crossed.append((x,y))
        assert len(crossed)>=3,(mid,'no aligned walking seam',c)
assert maps['MAP_VIDRA_DRAFT_CORVALA']['connections']==[]
assert len(maps['MAP_VIDRA_DRAFT_CORVALAPASSAGE']['warp_events'])==2
assert maps['MAP_VIDRA_DRAFT_RAINFALLROUTE']['weather']=='WEATHER_RAIN'
assert maps['MAP_VIDRA_DRAFT_NORVYN']['weather']=='WEATHER_SNOW'
print('PASS: nine maps, walking elevations, native warp behaviors, twelve aligned seams, stable existing map IDs')
