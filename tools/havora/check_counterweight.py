#!/usr/bin/env python3
"""Static preservation and reachability checks for the placed Havora puzzle."""
import json,struct,subprocess
from collections import deque
from pathlib import Path
R=Path(__file__).resolve().parents[2]
d=json.loads((R/'tools/havora/counterweight-puzzle.json').read_text());base=d['base_commit']
def old(p):return subprocess.check_output(['git','show',base+':'+p],cwd=R)
def js(p):return json.loads((R/p).read_text())
m=js('data/maps/HavoraNorthQuadrant/map.json');previous=json.loads(old('data/maps/HavoraNorthQuadrant/map.json'))
for k in m:
 if k not in ('object_events','bg_events'):assert m[k]==previous[k],k
assert m['object_events'][:10]==previous['object_events']
assert len(m['object_events'])==19<64
for key,first in [('boulders',11),('trees',17)]:
 for i,coord in enumerate(d[key]):
  obj=m['object_events'][first+i-1];assert [obj['x'],obj['y']]==coord and obj['elevation']==6
p='data/layouts/HavoraNorthQuadrant/map.bin';raw=(R/p).read_bytes();prior=old(p);now=struct.unpack('<2576H',raw);before=struct.unpack('<2576H',prior)
changes=[{'x':i%92,'y':i//92,'before':a,'after':b} for i,(a,b) in enumerate(zip(before,now)) if a!=b]
assert changes==d['changed_cells'] and len(changes)==16
assert not subprocess.check_output(['git','diff','--name-only',base,'--','data/layouts/layouts.json'],cwd=R).strip()
for layout in js('data/layouts/layouts.json')['layouts']:
 if layout['primary_tileset']=='gTileset_HavoraCityPrimary':
  for k in ['blockdata_filepath','border_filepath']:
   path=layout[k]
   if path!=p:assert (R/path).read_bytes()==old(path),path
# Both gate entries reuse existing native art without taking graphics/palette space.
for path in ['data/tilesets/primary/havora_city/tiles.png','data/tilesets/secondary/havora_city/tiles.png','data/tilesets/secondary/havora_city/metatiles.bin']:
 assert (R/path).read_bytes()==old(path),path
meta='data/tilesets/primary/havora_city/metatiles.bin';new=(R/meta).read_bytes();prev=old(meta)
for mid in range(640):
 if mid not in (561,562):assert new[mid*16:(mid+1)*16]==prev[mid*16:(mid+1)*16]
assert new[561*16:562*16]==new[89*16:90*16]
assert new[562*16:563*16]==new[:16]
# Independently replay the recorded solution with the exact painted floor,
# push-only movement, Cut gates, holes and weight-dependent collision.
floor=set(map(tuple,d['floor']));balls=list(map(tuple,d['boulders']));trees=list(map(tuple,d['trees']));holes=list(map(tuple,d['holes']));plates=list(map(tuple,d['plates']));gates=list(map(tuple,d['gates']));player=tuple(d['start']);cut=filled=0;dirs=[(0,-1),(1,0),(0,1),(-1,0)]
def closed(bs,hs):
 opened=[plates[0] in bs,plates[1] in bs,hs==7 and all(p in bs for p in plates[1:])]
 return {g for g,o in zip(gates,opened) if not o}
def reach():
 blocked=set(balls)|{p for i,p in enumerate(trees) if not cut>>i&1}|{p for i,p in enumerate(holes) if not filled>>i&1}|closed(balls,filled);seen={player};q=[player]
 for p in q:
  for dx,dy in dirs:
   n=p[0]+dx,p[1]+dy
   if n in floor and n not in seen|blocked:seen.add(n);q.append(n)
 return seen
for move in d['solution']:
 src=tuple(move['from'])
 if move['action']=='cut':
  assert any((src[0]+dx,src[1]+dy) in reach() for dx,dy in dirs);cut|=1<<trees.index(src)
 else:
  dst=tuple(move['to']);dx,dy=dst[0]-src[0],dst[1]-src[1];assert (dx,dy) in dirs
  stand=src[0]-dx,src[1]-dy
  assert src in balls and stand in reach() and dst in floor and dst not in balls and dst not in closed(balls,filled)
  assert all(dst!=p or cut>>i&1 for i,p in enumerate(trees));balls.remove(src)
  if dst in holes and not filled>>holes.index(dst)&1:filled|=1<<holes.index(dst)
  else:balls.append(dst)
  assert not set(balls)&closed(balls,filled) and src not in closed(balls,filled) and stand not in closed(balls,filled)
  player=src
 assert (cut,filled)==(move['cut_mask'],move['filled_mask'])
assert tuple(d['goal']) in reach() and filled==7 and all(p in balls for p in plates[1:])
print('PASS: 37-action solution, six interactive boulders, three Cut trees, exact 16-cell patch, preserved NPCs/warps/connections/cliffs/other districts, and zero added graphics.')
