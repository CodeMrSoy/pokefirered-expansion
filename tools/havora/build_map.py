#!/usr/bin/env python3
"""Build the approved 40x32 Havora harbor and its two seamless city approaches."""
from pathlib import Path
import struct,json,copy
R=Path(__file__).resolve().parents[2];D=json.loads((R/'tools/havora/assets.json').read_text());F=D['floors'];AS=D['assets']
def savejson(p,v):p.write_text(json.dumps(v,indent=2)+'\n')
def put(a,x,y,t,block=False):a[y][x]=0x3000|t|(0x400 if block else 0)
def fill(a,x,y,w,h,t,block=False):
 for yy in range(y,y+h):
  for xx in range(x,x+w):put(a,xx,yy,t,block)
def asset(a,name,x,y):
 for yy,row in enumerate(AS[name]['metatiles']):
  for xx,t in enumerate(row):put(a,x+xx,y+yy,t,True)
def dock(a,x,y,w,h):
 fill(a,x,y,w,h,F['wood'])
 for yy in range(y,y+h):
  a[yy][x]|=0x400;a[yy][x+w-1]|=0x400
 for xx in range(x,x+w):a[y+h-1][xx]|=0x400
 for xx,yy in [(x,y),(x+w-1,y),(x,y+h-1),(x+w-1,y+h-1)]:asset(a,'bollard',xx,yy)
def writeblocks(name,a,border=0x5d9):
 p=R/'data/layouts'/name;p.mkdir(exist_ok=True);flat=sum(a,[])
 (p/'map.bin').write_bytes(struct.pack('<'+'H'*len(flat),*flat));(p/'border.bin').write_bytes(struct.pack('<4H',*[border]*4))
def connection(direction,map,offset=0):return dict(map=map,offset=offset,direction=direction)
def main():
 h=[[0x5d9]*40 for _ in range(32)]
 for x,y,w,hh in [(0,0,40,4),(0,0,9,26),(4,19,9,8),(9,23,10,5),(17,25,15,3),(29,23,6,5),(32,22,5,5),(35,23,4,5),(36,3,4,10),(10,20,5,4)]:fill(h,x,y,w,hh,F['stone'])
 land={(x,y) for y in range(32) for x in range(40) if h[y][x]&1023==F['stone']}
 # Masonry faces sit at the land/water boundary; all faces have collision.
 for x,y in sorted(land):
  if (x,y+1) not in land and y<31:
   asset(h,'wall',x if x<39 else x-1,y)
 # Every west/north edge is open paving into the city approaches.
 for x,w,hh in [(12,4,5),(23,4,7),(30,4,5)]:dock(h,x,3,w,hh)
 dock(h,18,17,5,10);fill(h,18,24,5,3,F['wood'])
 dock(h,8,10,5,3);dock(h,8,16,4,3)
 asset(h,'warehouse',2,5);asset(h,'fish_store',2,16);asset(h,'office',11,20);asset(h,'lighthouse',35,23)
 asset(h,'crane',6,10);asset(h,'cargo',5,20);asset(h,'cargo',5,8)
 for name,x,y in [('crate',6,6),('barrel',6,18),('barrel',9,21),('net',6,14),('rope',24,7),('rope',31,6),('rope',19,18),('crate',13,5),('bollard',21,17),('gate',17,23),('gate',23,23)]:asset(h,name,x,y)
 for x,y in [(0,1),(6,3),(6,11),(0,19),(10,25),(26,24),(33,24),(38,8)]:asset(h,'lamp',x,y)
 # Keep two clear walking tiles along city boundaries, even near tall props.
 fill(h,0,0,40,1,F['stone']);fill(h,0,0,1,26,F['stone'])
 # Unobstructed Seagallop arrival and sailor interaction points.
 fill(h,19,18,3,4,F['wood'])
 fill(h,8,10,1,3,F['wood']);fill(h,8,16,1,3,F['wood'])
 fill(h,34,27,5,1,F['stone'])
 for xx in [34,36,38]:asset(h,'wall',xx,28)
 writeblocks('Quantum_Havora_Harbor_Layout',h)
 # The city is split around the harbor corner, avoiding overlapping north/west maps.
 # World origins: existing city(0,0); west approach(80,0); north(88,0); harbor(88,8).
 # Border strips use primary-only paving so the old Vermilion district can scroll
 # into this dedicated secondary tileset without showing mismatched metatiles.
 west=[[0x31c1]*8 for _ in range(40)];north=[[0x3000|F['stone']]*40 for _ in range(8)]
 for y in range(40):put(west,7,y,F['stone'])
 for x in range(40):put(north,x,0,5,True)
 writeblocks('QuantumHavoraWestQuay',west,0x31c1);writeblocks('QuantumHavoraNorthQuay',north,0x3000|F['stone'])
 ls=json.loads((R/'data/layouts/layouts.json').read_text())
 for l in ls['layouts']:
  if l['id']=='LAYOUT_QUANTUM_HAVORA_HARBOR_LAYOUT':l['secondary_tileset']='gTileset_HavoraHarbor'
 for name,w,hh,ident in [('QuantumHavoraWestQuay',8,40,'LAYOUT_QUANTUM_HAVORA_WEST_QUAY'),('QuantumHavoraNorthQuay',40,8,'LAYOUT_QUANTUM_HAVORA_NORTH_QUAY')]:
  ls['layouts']=[l for l in ls['layouts'] if l['id']!=ident]
  ls['layouts'].append(dict(id=ident,name=name+'_Layout',width=w,height=hh,border_width=2,border_height=2,primary_tileset='gTileset_General',secondary_tileset='gTileset_HavoraHarbor',border_filepath=f'data/layouts/{name}/border.bin',blockdata_filepath=f'data/layouts/{name}/map.bin'))
 savejson(R/'data/layouts/layouts.json',ls)
 hp=R/'data/maps/QuantumHarbor/map.json';m=json.loads(hp.read_text());m['warp_events']=[];m['coord_events']=[]
 m['bg_events']=[dict(type='sign',x=35,y=26,elevation=3,player_facing_dir='BG_EVENT_PLAYER_FACING_ANY',script='QuantumHarbor_LighthouseSign')]
 m['connections']=[connection('left','MAP_QUANTUM_HAVORA_WEST_QUAY',-8),connection('up','MAP_QUANTUM_HAVORA_NORTH_QUAY')]
 m['object_events'][0].update(x=25,y=20);m['object_events'][1].update(x=20,y=20)
 for obj,xy in zip(m['object_events'][2:],[(5,23),(5,12),(16,25)]):obj.update(x=xy[0],y=xy[1])
 savejson(hp,m)
 base=copy.deepcopy(m);base.update(object_events=[],warp_events=[],coord_events=[],bg_events=[],show_map_name=False)
 for name,ident,layout,connections in [
  ('QuantumHavoraWestQuay','MAP_QUANTUM_HAVORA_WEST_QUAY','LAYOUT_QUANTUM_HAVORA_WEST_QUAY',[connection('left','MAP_QUANTUM_PORT_CITY'),connection('right','MAP_QUANTUM_HAVORA_NORTH_QUAY'),connection('right','MAP_QUANTUM_HARBOR',8)]),
  ('QuantumHavoraNorthQuay','MAP_QUANTUM_HAVORA_NORTH_QUAY','LAYOUT_QUANTUM_HAVORA_NORTH_QUAY',[connection('left','MAP_QUANTUM_HAVORA_WEST_QUAY'),connection('down','MAP_QUANTUM_HARBOR')])]:
  md=R/'data/maps'/name;md.mkdir(exist_ok=True);obj=copy.deepcopy(base);obj.update(id=ident,name=name,layout=layout,connections=connections);savejson(md/'map.json',obj);(md/'scripts.inc').write_text(name+'_MapScripts::\n\t.byte 0\n')
 groups=json.loads((R/'data/maps/map_groups.json').read_text())
 for name in ['QuantumHavoraWestQuay','QuantumHavoraNorthQuay']:
  if name not in groups['gMapGroup_QuantumIsland']:groups['gMapGroup_QuantumIsland'].append(name)
 savejson(R/'data/maps/map_groups.json',groups)
 p=R/'data/event_scripts.s';s=p.read_text()
 for name in ['QuantumHavoraWestQuay','QuantumHavoraNorthQuay']:
  include=f'\t.include "data/maps/{name}/scripts.inc"'
  if include not in s:s+='\n'+include+'\n'
 p.write_text(s)
 cp=R/'data/maps/QuantumPortCity/map.json';c=json.loads(cp.read_text());c['connections']=[co for co in c['connections'] if co['map'] not in ['MAP_QUANTUM_HARBOR','MAP_QUANTUM_HAVORA_WEST_QUAY']];c['connections'].append(connection('right','MAP_QUANTUM_HAVORA_WEST_QUAY'))
 c['warp_events']=[w for w in c['warp_events'] if w['dest_map']!='MAP_QUANTUM_HARBOR'];savejson(cp,c)
 p=R/'data/layouts/QuantumPortCity/map.bin';a=list(struct.unpack('<6400H',p.read_bytes()))
 for y in range(40):
  for x in range(73,80):a[y*80+x]=0x31c1
 a[21*80+19]=0x3442 # Close the former harbor door facade; there is no door warp.
 p.write_bytes(struct.pack('<6400H',*a))
 p=R/'src/seagallop.c';s=p.read_text().replace('{MAP(MAP_QUANTUM_HARBOR), 0x08, 0x05}','{MAP(MAP_QUANTUM_HARBOR), 20, 19}');p.write_text(s)
 p=R/'data/maps/QuantumHarbor/scripts.inc';s=p.read_text().replace('The ferry boards at the west quay.','The ferry boards at the main pier.');p.write_text(s)
 print('Built 40x32 harbor, outdoor approaches, updated ferry arrival (20,19)')
if __name__=='__main__':main()
