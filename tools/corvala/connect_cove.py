"""Wire the restarted cove, its eight usable interiors, and sole access cave.

Explicit --write only. Adds maps at the end of Corvala's group and layouts at
the end of the layout table so existing map/layout identifiers do not move.
"""
import argparse,copy,json,struct
from pathlib import Path
from build_cove import R,read,write,words,rect

def warp(x,y,dest,index=0):return dict(x=x,y=y,elevation=3,dest_map=dest,dest_warp_id=str(index))
def obj(gfx,x,y,script,facing='DOWN'):
 return dict(type='object',graphics_id='OBJ_EVENT_GFX_'+gfx,x=x,y=y,elevation=3,movement_type='MOVEMENT_TYPE_FACE_'+facing,movement_range_x=0,movement_range_y=0,trainer_type='TRAINER_TYPE_NONE',trainer_sight_or_berry_tree_id='0',script=script,flag='0')
def room(name,id,layout):
 return dict(id=id,name=name,layout=layout,music='MUS_SEVII_123',region_map_section='MAPSEC_CORVALA_TOWN',requires_flash=False,weather='WEATHER_NONE',map_type='MAP_TYPE_INDOOR',allow_cycling=False,allow_escaping=False,allow_running=True,show_map_name=False,floor_number=0,battle_scene='MAP_BATTLE_SCENE_NORMAL',connections=None,object_events=[],warp_events=[],coord_events=[],bg_events=[])
def script(name,text=''):
 return name+'_MapScripts::\n\t.byte 0\n'+text
def message(name,text):return f'\n{name}::\n\tmsgbox {name}_Text, MSGBOX_NPC\n\tend\n\n{name}_Text::\n\t.string "{text}$"\n'

def main():
 m=read(R/'tools/corvala/map.json');assert m['design']=='cave-cove-v1'
 town=read(R/'data/maps/Corvala_Town/map.json');town['connections']=None
 town['warp_events']=[warp(*b['door'],dest,1 if i<2 else 0) for i,(b,dest) in enumerate(zip(m['buildings'][:4],['MAP_CORVALA_TOWN_POKEMON_CENTER_1_F','MAP_CORVALA_MART','MAP_CORVALA_HOUSE_1','MAP_CORVALA_HOUSE_2']))]
 town['warp_events'] += [warp(*m['portals']['gym'],'MAP_CORVALA_TIDAL_GYM'),warp(*m['portals']['entrance'],'MAP_CORVALA_ENTRANCE_CAVE',1)]
 town['warp_events'] += [warp(*b['door'],f'MAP_CORVALA_HOUSE_{i}') for i,b in enumerate(m['buildings'][4:],3)]
 town['object_events']=[];town['coord_events']=[];town['bg_events']=[]
 write(R/'data/maps/Corvala_Town/map.json',town)
 center=read(R/'data/maps/Corvala_Town_PokemonCenter_1F/map.json')
 for w in center['warp_events']:
  if w['dest_map']=='MAP_CORVALA_TOWN':w['dest_warp_id']='0'
 write(R/'data/maps/Corvala_Town_PokemonCenter_1F/map.json',center)
 heals=read(R/'src/data/heal_locations.json');heal=next(v for v in heals['heal_locations'] if v['id']=='HEAL_LOCATION_QUANTUM_COASTAL_CITY')
 heal.update(x=m['landmarks']['center_approach'][0],y=m['landmarks']['center_approach'][1]);write(R/'src/data/heal_locations.json',heals)
 # Add new interiors without changing any existing identifiers.
 new=[]
 mart=room('Corvala_Mart','MAP_CORVALA_MART','LAYOUT_MART')
 mart['object_events']=[obj('CLERK',2,3,'Corvala_Mart_Clerk','RIGHT')]
 mart['warp_events']=[warp(x,7,'MAP_CORVALA_TOWN',1) for x in (3,4,5)]
 stock='\nCorvala_Mart_Clerk::\n\tlock\n\tfaceplayer\n\tmessage Text_MayIHelpYou\n\twaitmessage\n\tpokemart Corvala_Mart_Items\n\tmsgbox Text_PleaseComeAgain\n\trelease\n\tend\n\n\t.align 2\nCorvala_Mart_Items::\n'+''.join('\t.2byte ITEM_'+item+'\n' for item in ['POKE_BALL','GREAT_BALL','SUPER_POTION','ANTIDOTE','PARALYZE_HEAL','ESCAPE_ROPE','REPEL','NONE'])
 new.append((mart,script(mart['name'],stock)))
 for i in range(1,6):
  name=f'Corvala_House{i}';h=room(name,f'MAP_CORVALA_HOUSE_{i}','LAYOUT_HOUSE2');h['warp_events']=[warp(x,7,'MAP_CORVALA_TOWN',i+1 if i<=2 else i+3) for x in (4,3,5)]
  h['object_events']=[obj('WOMAN_1' if i==1 else 'FISHER',2,3,name+'_Resident')]
  text='Our homes stand above the reef.\\nThe pilings reach into the sand.' if i==1 else 'The cave is our link to the mainland.\\nThese docks are the heart of CORVALA.'
  text={3:'The reef is full of color.\\nPlease watch where you step.',4:'We mend our fishing nets here.\\nThere is always another knot to tie.',5:'From here, I can see the cave\\nwhere travelers arrive.'}.get(i,text)
  new.append((h,script(name,message(name+'_Resident',text))))
 layouts=read(R/'data/layouts/layouts.json')
 for gym in (False,True):
  name='Corvala_TidalGym' if gym else 'Corvala_EntranceCave';mid='MAP_CORVALA_TIDAL_GYM' if gym else 'MAP_CORVALA_ENTRANCE_CAVE';lid='LAYOUT_CORVALA_TIDAL_GYM' if gym else 'LAYOUT_CORVALA_ENTRANCE_CAVE'
  w,h=(28,24) if gym else (30,20)
  blocks=[0x3c00|0x289]*(w*h)
  # Native cave walls and sandy floor, with a central rock/water feature.
  for y in range(3,h-2):
   for x in range(3,w-3):blocks[y*w+x]=0x3000|0x281
  for x in range(3,w-3):blocks[2*w+x]=0x3c00|0x291
  for y in range(3,h-2):
   blocks[y*w+2]=0x3c00|0x290;blocks[y*w+w-3]=0x3c00|0x292
  for x in range(2,w-2):blocks[(h-2)*w+x]=0x3c00|0x289
  for y in range(7,13):
   for x in range(9,19):blocks[y*w+x]=0x1c00|0x12b
  # Floor bridges make both rooms navigable without field tools.
  for y in range(7,13):
   for x in range(13,15):blocks[y*w+x]=0x3000|0x1be
  data=room(name,mid,lid);data['map_type']='MAP_TYPE_UNDERGROUND';data['show_map_name']=True
  if gym:
   # Two smaller tide basins flank the entrance path below the main pool.
   for cx in (7,20):
    for yy in range(15,19):
     for xx in range(cx-2,cx+3):
      if (xx-cx)**2+(yy-16.5)**2<6:blocks[yy*w+xx]=0x1c00|0x12b
   blocks[(h-3)*w+13]=0x3000|0x287
   data['warp_events']=[warp(13,h-3,'MAP_CORVALA_TOWN',4)]
   data['object_events']=[obj('MAN',13,4,name+'_Attendant')]
   scripts=script(name,message(name+'_Attendant','Welcome to CORVALA GYM.\\nThe reef arena is being prepared.'))
  else:
   for x in (5,24):blocks[2*w+x]=0x3000|0x294
   data['warp_events']=[warp(5,2,'MAP_VIDRA_COASTAL_ROAD'),warp(24,2,'MAP_CORVALA_TOWN',5)]
   scripts=script(name)
  layout=dict(id=lid,name=name+'_Layout',width=w,height=h,border_width=2,border_height=2,primary_tileset='gTileset_General',secondary_tileset='gTileset_Cave',border_filepath=f'data/layouts/{name}/border.bin',blockdata_filepath=f'data/layouts/{name}/map.bin')
  existing=next((v for v in layouts['layouts'] if v['id']==lid),None)
  if existing:existing.update(layout)
  else:layouts['layouts'].append(layout)
  write(R/layout['blockdata_filepath'],struct.pack('<'+'H'*len(blocks),*blocks));write(R/layout['border_filepath'],struct.pack('<4H',*([0x3c00|0x289]*4)))
  new.append((data,scripts))
 write(R/'data/layouts/layouts.json',layouts)
 groups=read(R/'data/maps/map_groups.json');includes=R/'data/event_scripts.s';text=includes.read_text(encoding='utf-8')
 for data,scripts in new:
  name=data['name']
  if name not in groups['gMapGroup_Corvala']:groups['gMapGroup_Corvala'].append(name)
  write(R/f'data/maps/{name}/map.json',data);write(R/f'data/maps/{name}/scripts.inc',scripts)
  inc=f'\t.include "data/maps/{name}/scripts.inc"'
  if inc not in text:text+='\n'+inc+'\n'
 write(R/'data/maps/map_groups.json',groups);write(includes,text)
 # The existing Coastal Road approach now ends at the entrance cave.
 road=read(R/'data/maps/Vidra_CoastalRoad/map.json');road['connections']=[c for c in road['connections'] if c['map']!='MAP_CORVALA_TOWN'];road['warp_events']=[warp(20,9,'MAP_CORVALA_ENTRANCE_CAVE')]
 rb=words(R/'data/layouts/Vidra_CoastalRoad/map.bin')
 for x,y in rect(17,6,7,4):rb[y*24+x]=0x3c00|0x71
 for x in range(11,23):
  for y in (10,11,12):rb[y*24+x]=0x3000|0x115
 for yy,row in enumerate([[0xa0,0xa1,0xa2],[0xa8,0xa9,0xaa]]):
  for xx,tile in enumerate(row):rb[(8+yy)*24+19+xx]=(0x3000 if (xx,yy)==(1,1) else 0x3c00)|tile
 for y in range(24):rb[y*24+23]|=0xc00
 write(R/'data/maps/Vidra_CoastalRoad/map.json',road);write(R/'data/layouts/Vidra_CoastalRoad/map.bin',struct.pack('<576H',*rb))
 harbor=read(R/'data/maps/Vidra_HarborRoad/map.json');harbor['connections']=[c for c in harbor['connections'] if c['map']!='MAP_CORVALA_TOWN'];write(R/'data/maps/Vidra_HarborRoad/map.json',harbor)
 hb=words(R/'data/layouts/Vidra_HarborRoad/map.bin')
 for y in range(24):hb[y*24]|=0xc00
 for x,y in rect(0,10,3,4):hb[y*24+x]=0x3c00|(0x71 if y<13 else 0x79)
 write(R/'data/layouts/Vidra_HarborRoad/map.bin',struct.pack('<576H',*hb))
 print('Wired nine town warps, eight service/residential interiors, Coastal Road cave approach; removed both town road seams.')

if __name__=='__main__':
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--write',action='store_true');args=ap.parse_args()
 if args.write:main()
 else:print('Use --write explicitly to install the cave-cove connections.')
