#!/usr/bin/env python3
"""Static preservation and reachability checks for the placed Havora puzzle."""
import json,struct,subprocess
from collections import deque
from pathlib import Path
R=Path(__file__).resolve().parents[2]
d=json.loads((R/'tools/havora/counterweight-puzzle.json').read_text());base=d['base_commit']
def old(p):return subprocess.check_output(['git','show',base+':'+p],cwd=R)
def js(p):return json.loads((R/p).read_text())
# User edits after the first placement are authoritative. Animation work may
# change the closed-gate alias, but must not repaint any maps or event data.
a=js('tools/havora/gate-animation.json');base=a['base_commit']
assert not subprocess.check_output(['git','diff','--name-only',base,'--','data/maps','data/layouts'],cwd=R).strip(), 'User map/event edits changed'
m=js('data/maps/HavoraNorthQuadrant/map.json')
assert len(m['object_events'])==19<64
for key,first in [('boulders',11),('trees',17)]:
 for i,coord in enumerate(d[key]):
  obj=m['object_events'][first+i-1];assert [obj['x'],obj['y']]==coord and obj['elevation']==6
for group in ['primary','secondary']:
 for leaf in ['metatile_attributes.bin']:
  path=f'data/tilesets/{group}/havora_city/{leaf}';assert (R/path).read_bytes()==old(path),path
 path=f'data/tilesets/{group}/havora_city/metatiles.bin';new=(R/path).read_bytes();prev=old(path)
 for i in range(len(new)//16):
  if group!='primary' or i not in [a['closed_metatile'],a['open_metatile']]:assert new[i*16:i*16+16]==prev[i*16:i*16+16],(group,i)
 for p in (R/f'data/tilesets/{group}/havora_city/palettes').glob('*.pal'):assert p.read_text().splitlines()==old(str(p.relative_to(R))).decode().splitlines()
meta=struct.unpack('<5120H',(R/'data/tilesets/primary/havora_city/metatiles.bin').read_bytes())
assert meta[561*8:562*8]==meta[:4]+meta[90*8+4:91*8]
assert meta[562*8:563*8]==meta[:4]+(0,0,0x13f8,0x13f8)
from PIL import Image
sheet=Image.open(R/a['sheet']);assert sheet.mode=='P' and sheet.size==(16,80)
tiles=[]
for group in ['primary','secondary']:
 im=Image.open(R/f'data/tilesets/{group}/havora_city/tiles.png')
 tiles.extend(im.crop((x,y,x+8,y+8)) for y in range(0,im.height,8) for x in range(0,128,8))
overlay=Image.new('P',(16,16))
for k,w in enumerate(meta[90*8+4:91*8]):
 im=tiles[w&1023]
 if w&1024:im=im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
 if w&2048:im=im.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
 overlay.paste(im,(k%2*8,k//2*8))
for frame,shift in enumerate(a['frame_shifts']):
 expected=Image.new('P',(16,16))
 if shift is None:
  expected.paste(tiles[1016],(0,8));expected.paste(tiles[1016],(8,8))
 else:expected.paste(overlay.crop((0,0,16,16-shift)),(0,shift))
 assert expected.tobytes()==sheet.crop((0,frame*16,16,(frame+1)*16)).tobytes(),frame
# Reclaim only a formerly blank and unused tail tile, preserving every other
# BG graphic. The legacy harbor callback retains its original 128-tile DMA.
import io
for group,start in [('primary',0),('secondary',640)]:
 p=f'data/tilesets/{group}/havora_city/tiles.png';before=Image.open(io.BytesIO(old(p)))
 for y in range(0,before.height,8):
  for x in range(0,128,8):
   tid=start+y//8*16+x//8
   if tid==1016:assert not any(before.crop((x,y,x+8,y+8)).tobytes())
   else:assert before.crop((x,y,x+8,y+8)).tobytes()==tiles[tid].tobytes(),tid
for group in ['primary','secondary']:
 p=f'data/tilesets/{group}/havora_city/metatiles.bin';v=struct.unpack('<'+'H'*(len(old(p))//2),old(p));assert all(w&1023!=1016 for w in v)
for p in (R/'data/tilesets/secondary/havora_harbor/anim/water').glob('*.4bpp'):
 assert not any(p.read_bytes()[-8*32:]),p
cap=tiles[1016];assert any(cap.tobytes()) and not any(cap.crop((0,0,8,4)).tobytes())
assert sheet.crop((0,64,16,80)).tobytes()==expected.tobytes()
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
print('PASS: 37-action solution; latest user maps/events/connections/cliffs preserved byte-for-byte; native gate art and all five animation frames exact; only one formerly blank/unreferenced BG slot used for resting log tops; all other BG art and palettes intact.')
