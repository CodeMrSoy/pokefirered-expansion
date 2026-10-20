"""Explicit authoring recipe for Havora's western hills and northern services.

Normal builds never run this script or overwrite Porymap edits.
"""
import copy,json,struct
from pathlib import Path
from add_civic_tiles import build as add_art
R=Path(__file__).resolve().parents[2]
def read(p):return json.loads((R/p).read_text())
def save(p,x):
 p=R/p;p.parent.mkdir(parents=True,exist_ok=True);s=json.dumps(x,indent=2)+'\n'
 if not p.exists() or p.read_text()!=s:p.write_text(s)
def text(p,s):
 p=R/p;p.parent.mkdir(parents=True,exist_ok=True)
 if not p.exists() or p.read_text()!=s:p.write_text(s)
NAT={int(k):v for k,v in read('tools/havora/city-tileset.json')['native_general_ids'].items()}
ASSETS=read('tools/havora/assets.json')['assets']
ART=add_art()['assets']
class Map:
 def __init__(self,name,w,h,z):
  self.name=name;self.w=w;self.h=h;self.a=[[NAT[1]|z<<12 for _ in range(w)] for _ in range(h)]
 def rect(self,x,y,w,h,mid,z,solid=False):
  for yy in range(y,y+h):
   for xx in range(x,x+w):self.a[yy][xx]=mid|z<<12|(0x400 if solid else 0)
 def native(self,x,y,w,h,source,z,solid=False):self.rect(x,y,w,h,NAT[source],z,solid)
 def path(self,x,y,w,h,z):self.rect(x,y,w,h,0x1C1,z)
 def tree(self,x,y,z):
  for yy,row in enumerate([[0xE,0xF],[0x1C,0x1D],[0x24,0x25]]):
   for xx,m in enumerate(row):self.native(x+xx,y+yy,1,1,m,z,True)
 def flowers(self,x,y,w,z):self.native(x,y,w,1,4,z,True)
 def boundary(self,z):
  for x,y,w,h in [(0,0,self.w,1),(0,self.h-1,self.w,1),(0,0,1,self.h),(self.w-1,0,1,self.h)]:self.native(x,y,w,h,5,z,True)
 def cliff(self,y,left,right,top,bottom,stairs):
  self.native(left,y,right-left,1,0x87,top,True);self.native(left,y+1,right-left,1,0x79,bottom,True)
  for x in stairs:
   self.path(x,y-2,4,2,top)
   self.native(x,y,4,1,0x89,0);self.native(x,y+1,4,1,0x91,0)
   self.path(x,y+2,4,2,bottom)
 def place(self,grid,x,y,z,door=None):
  w=len(grid[0]);h=len(grid)
  self.rect(x-1,y-1,w+2,h+2,0x280,z)
  for yy,row in enumerate(grid):
   for xx,m in enumerate(row):self.rect(x+xx,y+yy,1,1,m,z,True)
  if door:self.rect(x+door[0],y+door[1],1,1,grid[door[1]][door[0]],z)
 def house(self,x,y,z,width=4):
  rows=ASSETS['house']['metatiles'];g=[[r[0]]+[r[1]]*(width-2)+[r[-1]] for r in rows]
  g[-2][width//2]=0x29E;g[-1][width//2]=0x08F
  self.place(g,x,y,z,(width//2,3));return (x+width//2,y+3)
 def write(self,layout):
  folder=R/'data/layouts'/self.name;folder.mkdir(parents=True,exist_ok=True)
  (folder/'map.bin').write_bytes(struct.pack('<'+'H'*(self.w*self.h),*(v for row in self.a for v in row)))
  (folder/'border.bin').write_bytes(struct.pack('<4H',*([0x3400|0x1C1]*4)))
  return dict(id=layout,name=self.name+'_Layout',width=self.w,height=self.h,border_width=2,border_height=2,
   primary_tileset='gTileset_HavoraCityPrimary',secondary_tileset='gTileset_HavoraCity',
   border_filepath=f'data/layouts/{self.name}/border.bin',blockdata_filepath=f'data/layouts/{self.name}/map.bin')
def npc(gfx,x,y,z,script,face='DOWN'):
 return dict(type='object',graphics_id='OBJ_EVENT_GFX_'+gfx,x=x,y=y,elevation=z,
  movement_type='MOVEMENT_TYPE_FACE_'+face,movement_range_x=0,movement_range_y=0,
  trainer_type='TRAINER_TYPE_NONE',trainer_sight_or_berry_tree_id='0',script=script,flag='0')
def warp(x,y,z,dest,i=0):return dict(x=x,y=y,elevation=z,dest_map=dest,dest_warp_id=str(i))
def connection(direction,mid,offset=0):return dict(map=mid,offset=offset,direction=direction)
def scripts(name,dialogues):
 out=[f'{name}_MapScripts::\n\t.byte 0\n']
 for key,value in dialogues.items():out.append(f'{name}_{key}::\n\tmsgbox {name}_{key}_Text, MSGBOX_NPC\n\tend\n\n{name}_{key}_Text::\n\t.string "{value}$"\n')
 text(f'data/maps/{name}/scripts.inc','\n'.join(out))
def build():
 groups=read('data/maps/map_groups.json');layouts=read('data/layouts/layouts.json')
 ids={'west':'MAP_QUANTUM_PORT_CITY','north':'MAP_QUANTUM_HAVORA_NORTH_DISTRICT',
      'coast':'MAP_QUANTUM_HAVORA_COASTAL_DAYCARE','walk':'MAP_QUANTUM_HAVORA_NORTH_WALK',
      'gym':'MAP_QUANTUM_HAVORA_GYM','mart':'MAP_QUANTUM_HAVORA_MART','daycare':'MAP_QUANTUM_HAVORA_DAYCARE'}
 template=read('data/maps/QuantumHavoraNorthQuay/map.json')
 def register(m,mid,con,events,warps):
  lid='LAYOUT_'+mid.removeprefix('MAP_');layout=m.write(lid)
  existing=next((i for i,l in enumerate(layouts['layouts']) if l['id']==lid),None)
  if existing is None:layouts['layouts'].append(layout)
  else:layouts['layouts'][existing]=layout
  header=copy.deepcopy(template);header.update(id=mid,name=m.name,layout=lid,show_map_name=True,
     connections=con,object_events=events,warp_events=warps,coord_events=[],bg_events=[])
  save(f'data/maps/{m.name}/map.json',header)
  if m.name not in groups['gMapGroup_QuantumIsland']:groups['gMapGroup_QuantumIsland'].append(m.name)
 # Western district: two rises from the low waterfront to the gym plateau.
 w=Map('QuantumPortCity',48,96,3)
 w.native(8,0,32,28,1,5);w.native(8,30,32,32,1,4)
 w.path(0,0,8,96,3);w.path(40,0,8,96,3)
 w.cliff(28,8,40,5,4,[16]);w.cliff(62,8,40,4,3,[28])
 for x in [8,39]:
  w.native(x,0,1,28,0x83,5,True);w.native(x,30,1,32,0x83,4,True)
 w.path(16,0,4,28,5);w.path(12,5,24,3,5);w.path(22,14,4,12,5)
 w.path(16,30,4,26,4);w.path(12,34,26,3,4);w.path(12,54,26,4,4);w.path(28,54,4,8,4)
 w.path(4,68,40,4,3);w.path(28,64,4,18,3)
 w.place(ART['gym'],20,9,5,(3,4));w.house(12,42,4);w.house(30,43,4)
 for x,y,z in [(10,3,5),(32,2,5),(35,13,5),(10,20,5),(29,20,5),
                (10,32,4),(33,32,4),(22,43,4),(10,50,4),(35,50,4),
                (10,73,3),(15,74,3),(34,74,3)]:w.tree(x,y,z)
 for x,y,width,z in [(20,26,16,5),(10,39,7,4),(26,39,11,4),(10,59,13,4),(10,80,15,3)]:w.flowers(x,y,width,z)
 w.cliff(86,8,40,3,1,[]);w.rect(8,88,32,8,0x282,1,True)
 for x,y in [(11,90),(17,93),(30,91),(36,94)]:w.rect(x,y,1,1,142,1,True)
 # Both sides of the old-route seam use the already shared General flagstone.
 w.rect(0,0,1,96,0x1C1,3,True);w.rect(47,0,1,96,0x1C1,3,True)
 w.path(0,8,1,4,3);w.path(47,64,1,8,3)
 w.rect(0,0,48,1,0x1C1,5,True);w.path(16,0,4,1,5)
 # Right edge remains low for the existing quay, regardless of plateau elevation.
 w.rect(40,0,8,1,0x1C1,3,True)
 register(w,ids['west'],[connection('left','MAP_QUANTUM_HARBOR_ROAD'),connection('right','MAP_QUANTUM_HAVORA_WEST_QUAY',51),connection('up',ids['north'])],
   [npc('GYM_GUY',26,17,5,'QuantumPortCity_GymGuide'),npc('SAILOR',42,66,3,'QuantumPortCity_Guide'),npc('MAN',23,49,4,'QuantumPortCity_Trader')],
   [warp(23,13,5,ids['gym'],1),warp(14,45,4,'MAP_QUANTUM_HAVORA_WEST_HOUSE1'),warp(32,46,4,'MAP_QUANTUM_HAVORA_WEST_HOUSE2')])
 scripts('QuantumPortCity',{'GymGuide':'HAVORA GYM stands above the port.\\nThe view is worth every step!',
   'Guide':'East leads to the ferry harbor.\\nThe stairs climb into HAVORA.',
   'Trader':'Our homes rise with the cliffs.\\nThe northern square has the shops.'})
 quay=read('data/maps/QuantumHavoraWestQuay/map.json')
 for c in quay['connections']:
  if c['map']==ids['west']:c['offset']=-51
 save('data/maps/QuantumHavoraWestQuay/map.json',quay)
 # Update a narrow, event-free old-route boundary strip; retain its other cells.
 road=read('data/maps/QuantumHarborRoad/map.json');rl=next(l for l in layouts['layouts'] if l['id']==road['layout']);rw,rh=rl['width'],rl['height']
 ra=list(struct.unpack('<'+'H'*(rw*rh),(R/rl['blockdata_filepath']).read_bytes()))
 for y in range(rh):
  for x in range(rw-8,rw):ra[y*rw+x]=0x31C1
  ra[y*rw+rw-1]=0x31C1 if 8<=y<12 else 0x35C1
 (R/rl['blockdata_filepath']).write_bytes(struct.pack('<'+'H'*len(ra),*ra))
 # Broad northern quadrant, spanning the gym hills and the existing market.
 n=Map('QuantumHavoraNorthDistrict',96,40,5)
 n.native(0,0,96,10,1,6);n.cliff(10,0,96,6,5,[24,68])
 n.path(68,0,4,10,6);n.path(24,3,48,3,6);n.path(24,12,4,12,5)
 n.path(8,20,88,6,5);n.path(68,12,4,16,5)
 n.native(56,30,40,10,1,4);n.cliff(28,56,96,5,4,[68]);n.path(68,30,4,10,4)
 n.path(16,24,4,16,5);n.place(ART['center'],62,14,5,(2,3));n.place(ART['mart'],80,14,5,(2,3))
 for x,y in [(12,13),(31,13),(46,14)]:n.house(x,y,5)
 for x,y,z in [(3,2,6),(12,2,6),(40,1,6),(51,2,6),(80,2,6),(91,3,6),
                (3,14,5),(20,13,5),(37,14,5),(54,14,5),(74,14,5),(90,14,5),
                (3,29,5),(11,31,5),(25,29,5),(37,31,5),(47,30,5),(59,33,4),(80,33,4),(90,32,4)]:n.tree(x,y,z)
 for x,y,width,z in [(3,7,16,6),(37,7,22,6),(78,7,15,6),(3,18,17,5),(30,18,22,5),(60,19,6,5),(79,19,7,5)]:n.flowers(x,y,width,z)
 n.path(48,18,1,2,5)
 n.boundary(5);n.path(68,0,4,1,6);n.path(16,39,4,1,5);n.path(68,39,4,1,4);n.path(95,22,1,4,5)
 register(n,ids['north'],[connection('down',ids['west']),connection('down','MAP_QUANTUM_HAVORA_NORTH_QUAY',56),connection('right',ids['coast']),connection('up',ids['walk'],62)],
  [npc('WOMAN_1',74,23,5,'QuantumHavoraNorthDistrict_Coast'),npc('MAN',60,23,5,'QuantumHavoraNorthDistrict_Services'),npc('SAILOR',29,6,6,'QuantumHavoraNorthDistrict_North')],
  [warp(64,17,5,'MAP_QUANTUM_PORT_CITY_POKEMON_CENTER1_F',1),warp(82,17,5,ids['mart']),
   warp(14,16,5,'MAP_QUANTUM_HAVORA_NORTH_HOUSE1'),warp(33,16,5,'MAP_QUANTUM_HAVORA_NORTH_HOUSE2'),warp(48,17,5,'MAP_QUANTUM_HAVORA_NORTH_HOUSE3')])
 scripts(n.name,{'Coast':'The DAY CARE is east of the square,\\nright above the coastal cliffs.',
  'Services':'Welcome to the northern square!\\nThe CENTER and MART are right here.',
  'North':'The northern walk follows the cliffs.\\nYou can see the whole port from there.'})
 market=read('data/maps/QuantumHavoraNorthQuay/map.json')
 market['connections']=[c for c in market['connections'] if c['direction']!='up']+[connection('up',ids['north'],-56)]
 save('data/maps/QuantumHavoraNorthQuay/map.json',market)
 ml=next(l for l in layouts['layouts'] if l['id']==market['layout']);ma=list(struct.unpack('<2560H',(R/ml['blockdata_filepath']).read_bytes()))
 for y in range(12):
  for x in range(12,16):ma[y*40+x]=0x41C1
 (R/ml['blockdata_filepath']).write_bytes(struct.pack('<2560H',*ma))
 # Eastern coastal parcel, with the house above its fenced grounds.
 d=Map('QuantumHavoraCoastalDaycare',48,40,5)
 d.native(8,0,27,26,1,6);d.native(7,0,1,28,0x83,6,True)
 d.cliff(26,8,35,6,5,[22]);d.path(22,28,4,7,5);d.path(0,30,34,4,5)
 d.house(26,10,6,8);d.path(30,14,2,12,6);d.path(22,24,4,2,6)
 for x,y,fw,fh in [(18,17,16,1),(18,25,16,1),(18,17,1,9),(33,17,1,9)]:d.rect(x,y,fw,fh,0x2B5,6,True)
 d.path(30,17,2,1,6);d.path(22,25,4,1,6)
 for x,y,z in [(10,3,6),(17,4,6),(24,2,6),(31,3,6),(10,14,6),(11,21,6),(10,35,5),(30,35,5)]:d.tree(x,y,z)
 d.flowers(21,8,13,6);d.flowers(10,24,7,6)
 d.native(35,0,1,40,0x83,6,True);d.native(36,0,1,40,0x79,3,True);d.rect(37,0,11,40,0x282,1,True)
 for x,y in [(39,5),(43,12),(40,23),(45,31),(42,36)]:d.rect(x,y,1,1,142,1,True)
 d.native(0,0,1,40,5,5,True);d.path(0,22,1,4,5);d.path(1,22,5,12,5)
 d.native(1,0,34,1,5,6,True);d.native(1,39,34,1,5,5,True)
 register(d,ids['coast'],[connection('left',ids['north'])],
  [npc('GENTLEMAN',29,15,6,'QuantumHavoraCoastalDaycare_Caretaker'),npc('NIDORAN_F',21,20,6,'QuantumHavoraCoastalDaycare_Mon'),npc('PIDGEY',29,22,6,'QuantumHavoraCoastalDaycare_Mon')],
  [warp(30,13,6,ids['daycare'],1)])
 scripts(d.name,{'Caretaker':'The sea breeze keeps this place calm.\\nCome inside if your partner needs care.',
   'Mon':'The POKéMON looks happy and relaxed.$'.removesuffix('$')})
 # Northern promenade: a real connected outdoor walk and elevated lookout.
 p=Map('QuantumHavoraNorthWalk',16,32,6);p.native(0,0,16,10,1,7);p.cliff(10,1,15,7,6,[6]);p.path(6,12,4,20,6);p.path(4,3,8,5,7)
 for x,y,z in [(1,1,7),(12,1,7),(1,6,7),(12,6,7),(1,14,6),(12,14,6),(1,20,6),(12,20,6),(1,26,6),(12,26,6)]:p.tree(x,y,z)
 p.boundary(6);p.path(6,31,4,1,6)
 register(p,ids['walk'],[connection('down',ids['north'],-62)],
  [npc('FISHER',10,6,7,'QuantumHavoraNorthWalk_View')],[])
 scripts(p.name,{'View':'The whole coast opens out below us.\\nHAVORA is a city of sea and stone.'})
 # Preserve the existing Center scripts and upper floor; relocate only exits.
 center=read('data/maps/QuantumPortCityPokemonCenter1F/map.json')
 for e in center['warp_events'][:3]:e.update(dest_map=ids['north'],dest_warp_id='0')
 save('data/maps/QuantumPortCityPokemonCenter1F/map.json',center)
 heal=read('src/data/heal_locations.json')
 entries=heal['heal_locations'] if 'heal_locations' in heal else next(v for v in heal.values() if isinstance(v,list))
 target=next(e for e in entries if e['id']=='HEAL_LOCATION_QUANTUM_PORT_CITY');target.update(map=ids['north'],x=64,y=18)
 save('src/data/heal_locations.json',heal)
 path=R/'src/region_map.c';s=path.read_text();s=s.replace('{MAP(MAP_QUANTUM_PORT_CITY), HEAL_LOCATION_QUANTUM_PORT_CITY}',f'{{MAP({ids["north"]}), HEAL_LOCATION_QUANTUM_PORT_CITY}}');text('src/region_map.c',s)
 # Private interiors use active stock layouts; original Kanto maps are untouched.
 interiors=[('QuantumHavoraGym',ids['gym'],'PewterCity_Gym',ids['west'],0),
            ('QuantumHavoraMart',ids['mart'],'QuantumHavoraProvisions',ids['north'],1),
            ('QuantumHavoraDaycare',ids['daycare'],'Route5_PokemonDayCare',ids['coast'],0),
            ('QuantumHavoraWestHouse1','MAP_QUANTUM_HAVORA_WEST_HOUSE1','QuantumHavoraTraderHouse',ids['west'],1),
            ('QuantumHavoraWestHouse2','MAP_QUANTUM_HAVORA_WEST_HOUSE2','QuantumHavoraTraderHouse',ids['west'],2),
            ('QuantumHavoraNorthHouse1','MAP_QUANTUM_HAVORA_NORTH_HOUSE1','QuantumHavoraTraderHouse',ids['north'],2),
            ('QuantumHavoraNorthHouse2','MAP_QUANTUM_HAVORA_NORTH_HOUSE2','QuantumHavoraTraderHouse',ids['north'],3),
            ('QuantumHavoraNorthHouse3','MAP_QUANTUM_HAVORA_NORTH_HOUSE3','QuantumHavoraTraderHouse',ids['north'],4)]
 for name,mid,source,dest,wi in interiors:
  m=read(f'data/maps/{source}/map.json');m.update(id=mid,name=name,region_map_section='MAPSEC_QUANTUM_PORT_CITY')
  for e in m['warp_events']:e.update(dest_map=dest,dest_warp_id=str(wi))
  if name.endswith('Gym'):
   m['object_events']=[npc('GYM_GUY',7,12,3,name+'_Welcome')];m['bg_events']=[];m['coord_events']=[]
   scripts(name,{'Welcome':'Welcome to HAVORA GYM!\\nEvery great battle starts with a plan.'})
  elif name.endswith('Mart'):
   m['object_events']=[npc('CLERK',2,3,0,'QuantumHavoraNorthQuay_Supplies','RIGHT')];scripts(name,{})
  else:scripts(name,{})
  save(f'data/maps/{name}/map.json',m)
  if name not in groups['gMapGroup_QuantumIsland']:groups['gMapGroup_QuantumIsland'].append(name)
 save('data/maps/map_groups.json',groups);save('data/layouts/layouts.json',layouts)
 includes=(R/'data/event_scripts.s').read_text()
 for name in [n.name,d.name,p.name]+[i[0] for i in interiors]:
  line=f'\t.include "data/maps/{name}/scripts.inc"'
  if line not in includes:includes+='\n'+line+'\n'
 text('data/event_scripts.s',includes)
 save('tools/havora/civic-districts.json',{'maps':ids,'west_dimensions':[48,96],'north_dimensions':[96,40],
   'daycare_dimensions':[48,40],'north_walk_dimensions':[16,32],
   'entrances':{'gym':[23,13,5],'center':[64,17,5],'mart':[82,17,5],'daycare':[30,13,6]},
   'stairs':[{'map':w.name,'x':16,'y':28,'upper':5,'lower':4},{'map':w.name,'x':28,'y':62,'upper':4,'lower':3},
    {'map':n.name,'x':24,'y':10,'upper':6,'lower':5},{'map':n.name,'x':68,'y':10,'upper':6,'lower':5},
    {'map':n.name,'x':68,'y':28,'upper':5,'lower':4},{'map':d.name,'x':22,'y':26,'upper':6,'lower':5},
    {'map':p.name,'x':6,'y':10,'upper':7,'lower':6}],
   'gym_status':'Enterable stock training hall; leader/team/badge progression not assigned.',
   'daycare_service':'Existing FireRed Route 5 single-Pokemon raising service and save storage.'})
if __name__=='__main__':build()
