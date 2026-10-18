#!/usr/bin/env python3
"""Build the approved 40x32 Havora harbor and its two seamless city approaches."""
from pathlib import Path
import struct,json,copy
R=Path(__file__).resolve().parents[2];D=json.loads((R/'tools/havora/assets.json').read_text());F=D['floors'];AS=D['assets']
def savejson(p,v):
 s=json.dumps(v,indent=2)+'\n'
 if not p.exists() or p.read_text()!=s:p.write_text(s)
def put(a,x,y,t,block=False):a[y][x]=0x3000|t|(0x400 if block else 0)
def fill(a,x,y,w,h,t,block=False):
 for yy in range(y,y+h):
  for xx in range(x,x+w):put(a,xx,yy,t,block)
def asset(a,name,x,y):
 rows=AS[name]['metatiles']
 for yy,row in enumerate(rows):
  for xx,t in enumerate(row):
   under=a[y+yy][x+xx]
   # Tall freestanding props collide at their feet; their tops can be walked behind.
   behind=name in ['lamp','gate','net','crane'] and yy<len(rows)-1 and not under&0xc00
   put(a,x+xx,y+yy,t,not behind)
def dock(a,x,y,w,h,north_tip=False):
 fill(a,x,y,w,h,F['wood'])
 for yy in range(y,y+h):
  asset(a,'dock_rail_left',x,yy);asset(a,'dock_rail_right',x+w-1,yy)
 for yy in range(y,y+h-2,3):
  asset(a,'dock_post_left',x,yy);asset(a,'dock_post_right',x+w-1,yy)
 for xx in range(x+1,x+w-1):put(a,xx,y+h-1,AS['dock_face']['metatiles'][0][xx%2],True)
 asset(a,'dock_tip_left',x,y+h-1);asset(a,'dock_tip_right',x+w-1,y+h-1)
 if north_tip:
  for xx in range(x+1,x+w-1):asset(a,'dock_head',xx,y)
def writeblocks(name,a,border=0x5d9):
 p=R/'data/layouts'/name;p.mkdir(exist_ok=True);flat=sum(a,[])
 (p/'map.bin').write_bytes(struct.pack('<'+'H'*len(flat),*flat));(p/'border.bin').write_bytes(struct.pack('<4H',*[border]*4))
def connection(direction,map,offset=0):return dict(map=map,offset=offset,direction=direction)
def main():
 h=[[0x5d9]*40 for _ in range(32)]
 # Landmark positions measured from the approved reference at 640x512 scale.
 for x,y,w,hh in [(0,0,40,4),(0,0,8,22),(5,16,6,8),(8,19,3,4),
                  (6,7,4,6),(10,15,6,8),(10,21,20,3),(15,20,15,3),
                  (29,21,4,5),(32,23,7,5),(34,19,5,9),(37,3,3,8)]:
  fill(h,x,y,w,hh,F['stone'])
 land={(x,y) for y in range(32) for x in range(40) if h[y][x]&1023==F['stone']}
 # Full two-row masonry faces; side/north coping never replaces a front corner.
 def sea(x,y):
  if x<0 or y<0:return False # Open city boundaries.
  return x>=40 or y>=32 or (x,y) not in land
 for y in range(30):
  xs=[x for x in range(40) if (x,y) in land and (x,y+1) not in land]
  for x in xs:
   side='left' if sea(x-1,y) else 'right' if sea(x+1,y) else None
   if side:asset(h,'wall_corner_'+side,x,y)
   else:
    for yy,row in enumerate(AS['wall']['metatiles']):put(h,x,y+yy,row[x%2],True)
 for x,y in sorted(land):
  if sea(x,y+1):continue
  n,w,e=sea(x,y-1),sea(x-1,y),sea(x+1,y)
  name='wall_north_west' if n and w else 'wall_north_east' if n and e else 'wall_north' if n else 'wall_west' if w else 'wall_east' if e else None
  # Thin coping leaves the paving usable; adjacent water still blocks movement.
  if name:put(h,x,y,AS[name]['metatiles'][0][0])
 # Three northern berths. Piles and dock faces extend below deck level.
 for x,w,hh in [(11,4,5),(23,4,7),(29,4,5)]:dock(h,x,3,w,hh)
 dock(h,18,13,5,9,north_tip=True)
 # Visual gangplank to Seagallop; ferry boarding remains the original sailor script.
 put(h,22,17,AS['dock_boarding_gate']['metatiles'][0][0])
 asset(h,'boarding_ramp',23,17)
 for x,y,w in [(7,8,6),(7,12,5)]:
  fill(h,x,y,w,3,F['wood'])
  for xx in range(x,x+w):asset(h,'dock_head',xx,y)
  for yy in range(y,y+3):asset(h,'dock_rail_right',x+w-1,yy)
  for xx in range(x+1,x+w-1):put(h,xx,y+2,AS['dock_face']['metatiles'][0][xx%2],True)
  asset(h,'dock_post_right',x+w-1,y);asset(h,'dock_tip_right',x+w-1,y+2)
  put(h,x,y+1,F['wood'])
 asset(h,'warehouse',1,3);asset(h,'fish_store',1,11)
 asset(h,'office',11,16);asset(h,'lighthouse',35,20)
 asset(h,'crane',6,8)
 # This narrow coping ledge belongs to the crane plinth, not the walking route.
 h[11][9]|=0x400
 for name,x,y in [('cargo',7,18),('crate',8,18),('crate',8,20),('barrel',8,16),
                  ('barrel',7,17),('net',7,15),('rope',24,7),('rope',30,6),
                  ('rope',19,14),('rope',12,6),('bollard',21,19),
                  ('crate',11,5),('crate',23,5),('net',24,4),
                  ('gate',17,20),('gate',23,20)]:asset(h,name,x,y)
 for x,y in [(0,0),(6,1),(6,7),(0,18),(12,20),(25,21),(33,24),(38,0)]:asset(h,'lamp',x,y)
 for x,y in [(4,1),(5,18),(13,22),(24,22),(32,24),(38,5)]:asset(h,'planter',x,y)
 # The lighthouse point is a rocky island foundation rather than a paved box.
 for x,y in [(30,27),(32,29),(34,29),(36,29),(38,29)]:asset(h,'rock',x,y)
 # Keep the boarding passage open through the south-facing pier entrance.
 fill(h,18,20,5,3,F['wood'])
 # The western gatepost overhangs the quay corner; only its foot blocks movement.
 h[20][17]&=~0x400
 fill(h,35,26,3,1,F['stone'])
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
  if l['id']=='LAYOUT_QUANTUM_HAVORA_HARBOR_LAYOUT':l['secondary_tileset']='gTileset_HavoraHarbor';l['primary_tileset']='gTileset_HavoraPrimary'
 for name,w,hh,ident in [('QuantumHavoraWestQuay',8,40,'LAYOUT_QUANTUM_HAVORA_WEST_QUAY'),('QuantumHavoraNorthQuay',40,8,'LAYOUT_QUANTUM_HAVORA_NORTH_QUAY')]:
  ls['layouts']=[l for l in ls['layouts'] if l['id']!=ident]
  ls['layouts'].append(dict(id=ident,name=name+'_Layout',width=w,height=hh,border_width=2,border_height=2,primary_tileset='gTileset_HavoraPrimary',secondary_tileset='gTileset_HavoraHarbor',border_filepath=f'data/layouts/{name}/border.bin',blockdata_filepath=f'data/layouts/{name}/map.bin'))
 savejson(R/'data/layouts/layouts.json',ls)
 hp=R/'data/maps/QuantumHarbor/map.json';m=json.loads(hp.read_text());m['warp_events']=[];m['coord_events']=[]
 m['bg_events']=[dict(type='sign',x=36,y=25,elevation=3,player_facing_dir='BG_EVENT_PLAYER_FACING_ANY',script='QuantumHarbor_LighthouseSign')]
 m['connections']=[connection('left','MAP_QUANTUM_HAVORA_WEST_QUAY',-8),connection('up','MAP_QUANTUM_HAVORA_NORTH_QUAY')]
 m['object_events'][0].update(x=25,y=17);m['object_events'][1].update(x=20,y=17)
 for obj,xy in zip(m['object_events'][2:],[(6,20),(5,10),(16,22)]):obj.update(x=xy[0],y=xy[1])
 for label,x,y,gfx,movement in [
  ('QuantumHarbor_Fisher',13,4,'OBJ_EVENT_GFX_FISHER','MOVEMENT_TYPE_FACE_RIGHT'),
  ('QuantumHarbor_BeaconKeeper',34,22,'OBJ_EVENT_GFX_SAILOR','MOVEMENT_TYPE_FACE_UP')]:
  existing=next((o for o in m['object_events'] if o['script']==label),None)
  if existing:existing.update(x=x,y=y)
  if existing is None:
   o=copy.deepcopy(m['object_events'][1]);o.update(script=label,x=x,y=y,graphics_id=gfx,movement_type=movement);m['object_events'].append(o)
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
 p=R/'src/seagallop.c';s=p.read_text().replace('{MAP(MAP_QUANTUM_HARBOR), 0x08, 0x05}','{MAP(MAP_QUANTUM_HARBOR), 20, 16}').replace('{MAP(MAP_QUANTUM_HARBOR), 20, 19}','{MAP(MAP_QUANTUM_HARBOR), 20, 16}');p.write_text(s)
 p=R/'data/maps/QuantumHarbor/scripts.inc';s=p.read_text().replace('The ferry boards at the west quay.','The ferry boards at the main pier.');p.write_text(s)
 print('Built 40x32 harbor, outdoor approaches, updated ferry arrival (20,16)')
if __name__=='__main__':main()
