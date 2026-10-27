"""Explicit coastal-neighborhood authoring pass; never called by normal builds.

Run only against the documented civic baseline. Existing service coordinates,
interiors and harbor are retained. Do not rerun over later Porymap edits.
"""
import copy,json,struct
from build_civic_districts import R,Map,NAT,read,save,text,npc,warp,connection

def load(name):
 header=read(f'data/maps/{name}/map.json');layout=next(l for l in read('data/layouts/layouts.json')['layouts'] if l['id']==header['layout'])
 m=Map(name,layout['width'],layout['height'],3)
 a=struct.unpack('<'+'H'*(m.w*m.h),(R/layout['blockdata_filepath']).read_bytes())
 m.a=[list(a[y*m.w:(y+1)*m.w]) for y in range(m.h)]
 return m,header,layout

def write(m,h,l):
 (R/l['blockdata_filepath']).write_bytes(struct.pack('<'+'H'*(m.w*m.h),*(v for row in m.a for v in row)))
 save(f'data/maps/{m.name}/map.json',h)

def dialogue(name,key,lines):
 p=R/f'data/maps/{name}/scripts.inc';s=p.read_text();label=name+'_'+key
 if label+'::' not in s:s+=f'\n{label}::\n\tmsgbox {label}_Text, MSGBOX_NPC\n\tend\n\n{label}_Text::\n\t.string "'+r'\n'.join(lines)+'$"\n'
 text(str(p.relative_to(R)),s);return label

def resident(m,h,g,x,y,z,key,lines,roam=False):
 if any(o['script']==m.name+'_'+key for o in h['object_events']):return
 o=npc(g,x,y,z,dialogue(m.name,key,lines))
 if roam:o.update(movement_type='MOVEMENT_TYPE_WANDER_LEFT_AND_RIGHT',movement_range_x=1,movement_range_y=0)
 h['object_events'].append(o)

def home(m,h,x,y,z,suffix,lines,width=4):
 dx,dy=m.house(x,y,z,width);name='QuantumHavora'+suffix;mid='MAP_QUANTUM_HAVORA_'+''.join(('_'+c if c.isupper() else c.upper()) for c in suffix).lstrip('_')
 # Use append-only map registration, retaining every established map number.
 if not any(e['dest_map']==mid for e in h['warp_events']):h['warp_events'].append(warp(dx,dy,z,mid))
 wi=next(i for i,e in enumerate(h['warp_events']) if e['dest_map']==mid)
 inside=read('data/maps/Havora_TraderHouse/map.json');inside.update(id=mid,name=name)
 for e in inside['warp_events']:e.update(dest_map=h['id'],dest_warp_id=str(wi))
 text(f'data/maps/{name}/scripts.inc',f'{name}_MapScripts::\n\t.byte 0\n')
 label=dialogue(name,'Resident',lines);inside['object_events']=[npc('WOMAN_1',2,3,3,label)]
 save(f'data/maps/{name}/map.json',inside)
 groups=read('data/maps/map_groups.json')
 if name not in groups['gMapGroup_Havora']:groups['gMapGroup_Havora'].append(name)
 save('data/maps/map_groups.json',groups)
 p=R/'data/event_scripts.s';s=p.read_text();inc=f'\t.include "data/maps/{name}/scripts.inc"'
 if inc not in s:text('data/event_scripts.s',s+'\n'+inc+'\n')
 return dx,dy

def grove(m,points,z):
 for x,y in points:m.tree(x,y,z)

def sculpt_west():
 # Shared General water is visible correctly before either tileset transition.
 for fn,stride in [('metatiles.bin',16),('metatile_attributes.bin',4)]:
  gp=R/'data/tilesets/primary/general'/fn;cp=R/'data/tilesets/primary/havora_city'/fn
  a=bytearray(cp.read_bytes());a[472*stride:473*stride]=gp.read_bytes()[472*stride:473*stride];cp.write_bytes(a)
 w,h,l=load('Havora_WestQuadrant')
 for y in range(96):
  left=14 if y<7 else 10 if y<28 else 12 if y<40 else 10 if y<62 else 14 if y<67 else 10 if y<82 else 14
  z=5 if y<28 else 4 if y<62 else 3
  w.rect(0,y,left-2,1,0x282,1,True)
  w.native(left-2,y,1,1,0x75,z,True)
  w.native(left-1,y,1,1,0x83,z,True)
  if y>=88:w.rect(0,y,40,1,0x282,1,True)
 # The coastal road now reaches the low waterfront, not a flat strip beside the gym.
 w.path(0,68,48,4,3)
 for x,y in [(2,4),(5,20),(1,33),(6,44),(3,57),(6,80),(11,91),(24,94),(34,90)]:w.rect(x,y,1,1,142,1,True)
 for y,row in enumerate(w.a):
  for x,v in enumerate(row):
   if v&1023==0x282 or (x<8 and v&1023==142):row[x]=(v&0xfc00)|472
 for c in h['connections']:
  if c['map']=='MAP_VIDRA_HARBOR_ROAD':c['offset']=60
 write(w,h,l)
 road=read('data/maps/Vidra_HarborRoad/map.json')
 for c in road['connections']:
  if c['map']==h['id']:c['offset']=-60
 save('data/maps/Vidra_HarborRoad/map.json',road)

def build():
 assert load('Havora_River')[0].h==40, 'Refinement already applied; do not overwrite Porymap edits.'
 w,wh,wl=load('Havora_WestQuadrant')
 # An exposed lower coastal walk under the western residential cliffs.
 # The original west route retains its four-tile landing at y8..11.
 for y in range(96):
  coast=3 if y<18 else (2 if y<42 else (3 if y<62 else 1))
  w.rect(0,y,coast,1,0x282,1,True)
  w.native(coast,y,1,1,0x83,3,True)
  w.path(coast+1,y,8-coast-1,1,3)
  if y<62 and y not in (28,29):
   z=5 if y<28 else 4
   w.native(8,y,1,1,0x75,z,True)
   w.native(9,y,1,1,0x83,z,True)
 w.path(0,8,8,4,3)
 # Deliberate waterside boulders, with an unbroken promenade behind them.
 for x,y in [(0,3),(1,16),(0,24),(0,39),(1,55),(0,79),(0,91)]:w.rect(x,y,1,1,142,1,True)
 # Replace the huge right-hand paving band with a narrower street and gardens.
 w.native(44,1,3,62,1,3)
 w.native(44,72,3,14,1,3)
 for y in range(96):
  if not 64<=y<72:w.rect(47,y,1,1,0x2B5,3,True)
 w.path(40,64,8,8,3)
 for y in [4,13,23,35,45,56,75,81]:w.tree(44,y,3)
 # Give the two plateaus stepped, planted shoulders rather than long rectangles.
 for x,y,ww,hh,z in [(10,0,4,5,5),(34,17,5,9,5),(10,30,4,8,4),(34,57,5,5,4)]:
  w.native(x,y,ww,hh,1,z)
  for yy in range(y,y+hh-2,3):w.tree(x,yy,z)
 # Original buildings/doors stay in place; new houses form compact clusters.
 for x,y,z,suffix,lines,width in [
 (10,9,5,'CliffHouse1',['The wind is strongest here.','Our stone walls keep us warm.'],4),
 (30,9,5,'CliffHouse2',['My partner works at the docks.','We watch the ferry from up here.'],6),
 (23,31,4,'CliffHouse3',['The market wakes before sunrise.','I take bread down each morning.'],6),
 (10,50,4,'CliffHouse4',['These gardens shelter from the wind.','The flowers love this little court.'],6),
 (29,50,4,'CliffHouse5',['The GYM overlooks the old houses.','Follow the stairs to reach it.'],6),
 (20,74,3,'HarborInn',['Welcome to the harbor guesthouse.','Travelers come from every coast.'],8)]:
  dx,dy=home(w,wh,x,y,z,suffix,lines,width);w.path(dx,dy+1,2,2,z)
 w.path(12,14,8,2,5);w.path(26,14,10,2,5)
 w.path(23,36,8,2,4);w.path(18,36,6,2,4)
 w.path(10,55,26,3,4);w.path(24,72,3,2,3);w.path(24,80,3,3,3)
 grove(w,[(21,19),(23,22),(31,21)],5)
 grove(w,[(21,40),(23,40),(25,43)],4)
 grove(w,[(9,74),(12,76),(33,76),(35,79)],3)
 w.flowers(21,24,6,5);w.flowers(20,48,6,4);w.flowers(29,79,6,3)
 # Visible rail at the long outer boundary, never invisible pavement walls.
 for y in range(96):
  if not 8<=y<12 and (w.a[y][0]&1023)==0x1C1:w.rect(0,y,1,1,0x2B5,3,True)
 # Keep historic object positions and introduce local activities off stair landings.
 for args in [
 ('WOMAN_1',13,16,5,'CliffGardener',['Sea winds make sturdy gardens.','The trees shelter our homes.'],False),
 ('MAN',32,15,5,'GymVisitor',['A short climb before a battle','is a fine way to warm up!'],True),
 ('WOMAN_1',26,38,4,'Baker',['Fresh bread for the morning boats!','The market is down the stairs.'],True),
 ('GENTLEMAN',12,56,4,'Neighbor',['These houses grew with the port.','No two little gardens are alike.'],False),
 ('MAN',33,56,4,'Resident',['The northern square is uphill.','There is another stair by the quay.'],False),
 ('SAILOR',26,80,3,'InnGuest',['A warm room after a long voyage.','That is all a sailor needs.'],False),
 ('PIDGEY',34,82,3,'CoastBird',['The POKéMON watches the waves.'],False)]:resident(w,wh,*args)
 write(w,wh,wl)
 # Extend the existing quay northward into the former empty eight-tile strip.
 # Its old cells move down 51 rows, preserving the existing harbor approaches.
 q,qh,ql=load('Havora_River');old=q.a
 assert q.h==40,'This pass expects the original 8x40 west quay.'
 q=Map(q.name,8,96,3)
 for y,row in enumerate(old):q.a[y+51]=row[:]
 for y in range(51):
  z=5 if y<16 else (4 if y<36 else 3)
  q.native(0,y,8,1,1,z);q.path(2,y,4,1,z)
  q.native(0,y,1,1,0x83,z,True);q.native(7,y,1,1,0x84,z,True)
 for y in [3,9,21,27,41]:q.native(1,y,1,2,5,5 if y<16 else 4 if y<36 else 3,True)
 q.cliff(16,0,8,5,4,[2]);q.cliff(36,0,8,4,3,[2])
 # Same elevations on all legacy crossings, with a visible western railing.
 for y in range(51,91):
  if not 64<=y<72:q.rect(0,y,1,1,0x2B5,3,True)
 q.path(0,64,8,8,3)
 q.rect(0,91,8,5,0x282,1,True)
 ql.update(height=96,primary_tileset='gTileset_HavoraCityPrimary',secondary_tileset='gTileset_HavoraCity')
 qh['connections']=[connection('left','MAP_QUANTUM_PORT_CITY',0),connection('right','MAP_QUANTUM_HAVORA_NORTH_QUAY',0),connection('right','MAP_QUANTUM_HARBOR',64),connection('up','MAP_QUANTUM_HAVORA_NORTH_DISTRICT',-48)]
 layouts=read('data/layouts/layouts.json');layouts['layouts']=[ql if l['id']==ql['id'] else l for l in layouts['layouts']];save('data/layouts/layouts.json',layouts)
 write(q,qh,ql)
 for name in ['Havora_WestQuadrant','Havora_Market','Havora_Harbor']:
  h=read(f'data/maps/{name}/map.json')
  for c in h['connections']:
   if c['map']==qh['id']:c['offset']=-64 if name=='Havora_Harbor' else 0
  save(f'data/maps/{name}/map.json',h)
 # Northern street frontage: preserve services and doors while filling long gaps.
 n,nh,nl=load('Havora_NorthQuadrant')
 for x,y,z,suffix,lines,width in [
 (23,29,5,'NorthHouse4',['We mend the fishing crews coats.','Salt and wind are hard on cloth.'],6),
 (38,28,5,'NorthHouse5',['Look up on a clear mountain night.','Sometimes the stars come to us.'],6),
 (78,3,6,'NorthLodge',['The mountain trail starts nearby.','Rest before you begin the climb.'],6)]:
  # Clear the footprint and its court before placing an enterable building.
  n.native(x-1,y-1,width+2,8,1,z)
  dx,dy=home(n,nh,x,y,z,suffix,lines,width);n.path(dx,dy+1,2,2,z)
 n.path(24,26,4,3,5);n.path(40,26,3,2,5);n.path(48,24,6,16,5)
 n.path(72,7,11,1,6);n.path(80,7,3,3,6)
 # Reduce the visual width of the avenue; retain roomy service forecourts.
 for x in range(8,94):
  if not (16<=x<20 or 24<=x<28 or 48<=x<54 or 60<=x<86):n.native(x,25,1,1,1,5)
 grove(n,[(5,27),(7,30),(3,34),(6,35),(29,29),(31,33),(7,7),(9,7),(44, 0),(45,5),(87,28),(89,30)],5)
 # Correct the upper grove's metadata to the upper promenade level.
 for x,y in [(7,7),(9,7),(44, 0),(45,5)]:n.tree(x,y,6)
 n.flowers(29,36,5,5);n.flowers(4,37,8,5)
 n.path(50,39,4,1,5)
 nh['connections'].append(connection('down',qh['id'],48))
 for args in [
 ('WOMAN_1',65,22,5,'Patient',['My partner is feeling better.','We are off to the market now.'],False),
 ('MAN',84,23,5,'Shopper',['Supplies for the mountain trail.','I always stop here before a climb.'],False),
 ('GENTLEMAN',27,34,5,'Tailor',['Strong cloth and a good coat','will see you through a sea wind.'],False),
 ('WOMAN_1',42,34,5,'Stargazer',['One old impact rests by the lookout.','The great craters are farther uphill.'],False),
 ('MAN',52,30,5,'QuayWalker',['These stairs wind down to the quay.','I like the quieter way home.'],True),
 ('SAILOR',81,8,6,'Hiker',['The mountain can wait until morning.','Tonight I will stay at the lodge.'],False),
 ('PIDGEY',8,33,5,'GardenBird',['The POKéMON rustles in the garden.'],False)]:resident(n,nh,*args)
 write(n,nh,nl)
 # Daycare: sheltered tree groups and flower beds around the unchanged paddock.
 d,dh,dl=load('Havora_DaycareExterior')
 grove(d,[(9,5),(11,7),(14,4),(16,7),(10,17),(12,19),(20,3)],6)
 grove(d,[(8,34),(12,36),(26,35),(28,36)],5)
 d.flowers(20,15,5,6);d.flowers(20,23,2,6);d.flowers(31,23,2,6)
 resident(d,dh,'WOMAN_1',27,15,6,'Visitor',['My partner loves this quiet garden.','We can hear the sea below the cliffs.'])
 resident(d,dh,'MAN',29,32,5,'CoastView',['The cliffs protect the little field.','Please keep the gate clear.'])
 write(d,dh,dl)
 # One small old impact hollow: an explicitly solid landscaped story landmark.
 p,ph,pl=load('Havora_Lookout')
 p.native(1,14,4,10,1,6)
 bowl=[[0x68,0x69,0x6A,0x6B],[0x70,0xBD,0xBE,0x73],[0x78,0x79,0x79,0x7A]]
 for yy,row in enumerate(bowl):
  for xx,mid in enumerate(row):p.native(1+xx,16+yy,1,1,mid,6,True)
 p.flowers(1,20,3,6);p.native(4,21,1,1,3,6,True)
 label=dialogue(p.name,'Impact',['An old MINIOR landing site.','Larger craters lie in the mountains.'])
 ph['bg_events']=[dict(type='sign',x=4,y=21,elevation=6,player_facing_dir='BG_EVENT_PLAYER_FACING_ANY',script=label)]
 # A reachable spur lets the player read the marker without leaving the trail.
 p.path(5,21,1,2,6)
 write(p,ph,pl)
 # Preserve market activity and services; add intimate planted courtyards.
 m,mh,ml=load('Havora_Market')
 for x,y in [(29,42),(31,45),(29,48),(11,47),(13,50)]:
  # Only replace existing grass, never a building, stair or established path.
  if all((m.a[yy][xx]&1023)==NAT[1] for yy in range(y,y+3) for xx in range(x,x+2)):m.tree(x,y,3)
 resident(m,mh,'WOMAN_1',13,28,4,'MarketCustomer',['A gift from HAVORA for my family.','Which stall would you choose?'])
 resident(m,mh,'MAN',25,34,4,'MarketTraveler',['The houses climb right up the cliffs.','I have never seen a port like it.'])
 write(m,mh,ml)
 data=read('tools/havora/civic-districts.json');data['west_quay_dimensions']=[8,96]
 data['stairs'] += [dict(map=q.name,x=2,y=16,upper=5,lower=4),dict(map=q.name,x=2,y=36,upper=4,lower=3)]
 save('tools/havora/civic-districts.json',data)
 sculpt_west()
 for name in ['Havora_WestQuadrant','Havora_River']:
  mm,hh,ll=load(name)
  for row in mm.a:
   for x,v in enumerate(row):
    if (v&1023)==0x1c1 and v&0xc00:row[x]=(v&0xfc00)|0x2b5
  write(mm,hh,ll)

if __name__=='__main__':build()
