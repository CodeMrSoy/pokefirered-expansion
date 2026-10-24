#!/usr/bin/env python3
"""Apply the reviewed residential substitutions; never edit cliff/border cells."""
import json,struct
from pathlib import Path
R=Path(__file__).resolve().parents[2]
def js(p):return json.loads((R/p).read_text())
def save(p,v):(R/p).write_text(json.dumps(v,indent=2)+'\n')
def ww(p):
 b=(R/p).read_bytes();return list(struct.unpack('<'+'H'*(len(b)//2),b))
manifest=R/'tools/havora/green-house-placements.json'
if manifest.exists():raise SystemExit('Placement migration already applied.')
kits=js('tools/havora/green-houses.json')['kits'];cerulean=js('tools/havora/native-houses.json')['kits']['cerulean_home']
# Eight-column long house, retaining four columns to the left of its doorway.
kits['long_home']=[[row[i] for i in [0,4,4,1,2,3,5,6]] for row in cerulean]
layouts={l['name'].replace('_Layout',''):l for l in js('data/layouts/layouts.json')['layouts']}
# old rectangle, new origin, source kit, doorway in kit, existing warp index
plan=[
 ('HavoraMarket',(4,5,4,4),(5,5),'viridian_home',(1,3),0),
 ('HavoraMarket',(31,13,4,4),(31,12),'viridian_garden',(1,3),3),
 ('HavoraMarket',(16,3,8,5),(16,4),'long_home',(4,3),4),
 ('HavoraMarket',(3,21,8,4),(3,21),'long_home',(4,3),5),
 ('HavoraNorthQuadrant',(16,17,6,4),(17,17),'viridian_home',(1,3),5),
 ('HavoraNorthQuadrant',(31,16,6,4),(32,16),'viridian_garden',(1,3),6),
 ('HavoraWestQuadrant',(7,49,6,4),(8,49),'viridian_home',(1,3),8),
 ('HavoraDaycare',(3,11,8,4),(3,11),'long_home',(4,3),0),
]
# Native terrain IDs include cliffs and waterfall edges; protect every one
# except the explicit flat grass/path material used for a house plot.
terrain=js('tools/havora/city-tileset.json')['native_general_ids'];grass=terrain['1'];cliffs={v for k,v in terrain.items() if int(k)>=104}|set(range(168,172))
cache={};metas={};report=[]
for name,old,origin,kit,door,warp_index in plan:
 l=layouts[name];w=l['width'];v=cache.setdefault(name,ww(l['blockdata_filepath']));mp=f'data/maps/{name}/map.json';m=metas.setdefault(name,js(mp));x,y,ow,oh=old;nx,ny=origin;grid=kits[kit]
 oldcells={(x+i,y+j) for j in range(oh) for i in range(ow)};newcells={(nx+i,ny+j) for j,row in enumerate(grid) for i in range(len(row))}
 assert all(0<=a<w and 0<=b<l['height'] for a,b in oldcells|newcells)
 assert all(v[b*w+a]&1023 not in cliffs for a,b in oldcells|newcells),(name,'cliff overlap')
 # New footprint extensions must use bare grass/path, with no tree/NPC removal.
 for a,b in newcells-oldcells:
  assert v[b*w+a]&1023 in {grass,640,449,450,143},(name,'occupied extension',a,b,hex(v[b*w+a]))
  assert not any(e['x']==a and e['y']==b for e in m.get('object_events',[])),(name,'NPC overlap')
 for a,b in oldcells:v[b*w+a]=(v[b*w+a]&0xf000)|grass
 source=None
 if kit!='long_home':
  src=js('tools/havora/green-houses.json')['sources'][kit];sl=layouts.get(src['map'])
  sl=next(q for q in js('data/layouts/layouts.json')['layouts'] if q['name']==src['map']+'_Layout');source=ww(sl['blockdata_filepath']);sx,sy,sw,sh=src['rectangle']
 for j,row in enumerate(grid):
  for i,mid in enumerate(row):
   pos=(ny+j)*w+nx+i;collision=(source[(sy+j)*sl['width']+sx+i]>>10)&3 if source is not None else 1
   # Top row has a visible roof edge; buildings remain solid until their door.
   v[pos]=(v[pos]&0xf000)|(collision<<10)|mid
 dx,dy=nx+door[0],ny+door[1];v[dy*w+dx]&=~0xc00
 # Keep the doorstep open and join the existing local walkway.
 if (dx,dy+1) not in newcells:
  pos=(dy+1)*w+dx
  assert v[pos]&1023 not in cliffs or v[pos]&1023 in {166,167},(name,'door against cliff')
  if v[pos]&1023==grass:v[pos]=(v[pos]&0xf000)|449
  v[pos]&=~0xc00
 before=dict(m['warp_events'][warp_index]);warp=m['warp_events'][warp_index];warp.update(x=dx,y=dy,elevation=v[dy*w+dx]>>12)
 report.append({'map':name,'old_rectangle':old,'new_origin':origin,'kit':kit,'door':[dx,dy],'warp_index':warp_index,'previous_warp':before,'destination':warp['dest_map']})
for name,v in cache.items():
 p=layouts[name]['blockdata_filepath'];(R/p).write_bytes(struct.pack('<'+'H'*len(v),*v));save(f'data/maps/{name}/map.json',metas[name])
save('tools/havora/green-house-placements.json',{'placements':report,'long_home_grid':kits['long_home'],'harbor_untouched':True,'cliff_cells_untouched':True,'note':'Existing interior destination and warp indices are retained, so return warps follow the updated exterior doors. Unrelated pre-existing event placement issues remain.'})
print(json.dumps(report,indent=2))
