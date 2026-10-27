"""Verify the ten households and dialogue-only, safe outdoor patrols."""
from pathlib import Path
from collections import Counter
import json,re,struct
R=Path(__file__).resolve().parents[1]
def read(p):return json.loads((R/p).read_text())
def words(p):
 b=Path(p).read_bytes();return struct.unpack('<'+'H'*(len(b)//2),b)
p=read('tools/havora/interior-access.json');assert len(p['private_interiors'])==10 and len(p['locked_doors'])==8
assert Counter(p['household_types'].values())=={'family':3,'couple':4,'solo':3}
assert set(p['household_types'])==set(p['private_interiors'])
gfx=set(re.findall(r'^#define (OBJ_EVENT_GFX_\w+)',(R/'include/constants/event_objects.h').read_text(),re.M))
for name in p['private_interiors']:
 j=read(f'data/maps/{name}/map.json');s=(R/f'data/maps/{name}/scripts.inc').read_text();people=[o for o in j['object_events'] if not o['script'].endswith('_Pokemon')]
 assert len(people)>0
 for o in j['object_events']:
  assert o['graphics_id'] in gfx and o['trainer_type']=='TRAINER_TYPE_NONE'
  assert o['script']+'::' in s
 for person in people:
  block=s.split(person['script']+'::',1)[1].split('\n\n',1)[0];assert 'msgbox ' in block
 assert not re.search(r'^\s*trainerbattle',s,re.M)
assert len(p['household_pokemon'])==8
for pet in p['household_pokemon']:
 s=(R/f'data/maps/{pet["map"]}/scripts.inc').read_text();block=s.split(pet['script']+'::',1)[1]
 assert 'playmoncry SPECIES_'+pet['species']+', CRY_MODE_NORMAL' in block and 'waitmoncry' in block
 j=read(f'data/maps/{pet["map"]}/map.json');o=next(o for o in j['object_events'] if o['script']==pet['script']);assert o['graphics_id']=='OBJ_EVENT_GFX_'+pet['species']
print('PASS ten distinct households: three families, four couples, three solo homes; eight matching Pokemon sprites/cries; no trainer encounters')
ls={l['id']:l for l in read('data/layouts/layouts.json')['layouts']};attrs=[]
for kind in ['primary','secondary']:
 b=(R/f'data/tilesets/{kind}/havora_city/metatile_attributes.bin').read_bytes();attrs+=list(struct.unpack('<'+'I'*(len(b)//4),b))
assert len(p['walking_residents'])==8
for e in p['walking_residents']:
 j=read(f'data/maps/{e["map"]}/map.json');l=ls[j['layout']];W,H=l['width'],l['height'];b=words(R/l['blockdata_filepath']);o=next(o for o in j['object_events'] if o['script']==e['script']);x,y=e['spawn'];dx,dy=e['range']
 assert o['trainer_type']=='TRAINER_TYPE_NONE' and o['trainer_sight_or_berry_tree_id']=='0' and o['flag']=='0'
 assert (o['x'],o['y'])==(x,y) and (o['movement_range_x'],o['movement_range_y'])==(dx,dy)
 assert (dx,dy) in [(1,0),(0,1)] and o['movement_type']=='MOVEMENT_TYPE_WANDER_'+('LEFT_AND_RIGHT' if dx else 'UP_AND_DOWN')
 events={(q['x'],q['y']) for kind in ['warp_events','bg_events','coord_events'] for q in j[kind]}
 others={(q['x'],q['y']) for q in j['object_events'] if q['script']!=e['script']}
 for t in [-1,0,1]:
  xx,yy=x+dx*t,y+dy*t
  assert 0<xx<W-1 and 0<yy<H-1
  tile=b[yy*W+xx];assert not tile&0xc00 and attrs[tile&1023]&0x1ff==0 and tile>>12==o['elevation']
  assert (xx,yy) not in events|others
  # A second clear lane lets the player pass when the pedestrian pauses.
  side=b[(yy+dx)*W+xx+dy];assert not side&0xc00 and attrs[side&1023]&0x1ff==0
  assert all(abs(xx-ex)+abs(yy-ey)>=3 for ex,ey in events)
 s=(R/f'data/maps/{e["map"]}/scripts.inc').read_text();block=s.split(e['script']+'::',1)[1].split('\n\n',1)[0]
 assert 'MSGBOX_NPC' in block and not re.search(r'\b(trainerbattle|giveitem|givemon|warp)\b',block)
print('PASS eight dialogue-only walkers; dry level patrols, clear passing lanes, doors/stairs/water avoided, correct movement ranges')
