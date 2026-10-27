#!/usr/bin/env python3
"""Build editable Corvala metatiles and tide artwork from the supplied concept.

The game uses the low-tide layout. Mid/high maps are authoring previews only;
no tide clock or runtime tile replacement is installed by this map builder.
"""
from pathlib import Path
from collections import deque
import struct,json,sys,hashlib
from PIL import Image,ImageDraw
import art as A
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'tools/havora'))
from render import atlas
from native_reference import install
from shoreline import NativeShore, SAND
from stilt_houses import kit as house_kit
native=atlas('cinnabar_island');install(native)
W,H=56,60
D=R/'data/tilesets/secondary/corvala';B=R/'build/corvala';B.mkdir(parents=True,exist_ok=True)
T=[bytes(64)];lookup={T[0]:(0,0)};M=[];attrs=[];ml={};pixels={};kit={}
# Deduplicate all four reflected orientations across banks, preserving each bank.
def reg(im,bank,behavior=0):
 desc=[]
 for x,y in [(0,0),(8,0),(0,8),(8,8)]:
  patch=im.crop((x,y,x+8,y+8));raw=patch.tobytes()
  if raw not in lookup:
   tid=len(T);T.append(raw)
   for f,flip in [(0,patch),(1024,patch.transpose(Image.Transpose.FLIP_LEFT_RIGHT)),(2048,patch.transpose(Image.Transpose.FLIP_TOP_BOTTOM)),(3072,patch.transpose(Image.Transpose.FLIP_LEFT_RIGHT).transpose(Image.Transpose.FLIP_TOP_BOTTOM))]:lookup.setdefault(flip.tobytes(),(tid,f))
  tid,f=lookup[raw];desc.append((640+tid)|f|(bank<<12))
 k=tuple(desc)+(behavior,)
 if k not in ml:
  ml[k]=640+len(M);M.append(desc+[640]*4);attrs.append(behavior)
  p=im.copy();p.putpalette(sum((list(c) for c in A.PALETTES[bank-7]),[])+[0]*720);pixels[ml[k]]=p.convert('RGB')
 return ml[k]
def asset(im,bank,bg=None):
 rows=[]
 for y in range(0,im.height,16):
  row=[]
  for x in range(0,im.width,16):
   p=im.crop((x,y,x+16,y+16))
   if bg is not None:
    out=bg.copy();out.paste(p,(0,0),Image.frombytes('L',p.size,p.tobytes()).point(lambda v:255 if v else 0));p=out
   row.append(reg(p,bank))
  rows.append(row)
 return rows
def native_meta(desc,behavior,preview):
 key=tuple(desc)+(behavior,)
 if key not in ml:
  ml[key]=640+len(M);M.append(desc);attrs.append(behavior);pixels[ml[key]]=preview.convert('RGB')
 return ml[key]
shoreline=NativeShore(R,native,native_meta)
kit['sea']=[0x12b,0x12b]
kit['shallow']=[native_meta(shoreline.descriptors(0x12b),0x17,native[0x12b])]*2
kit['sand']=SAND;kit['grass']=reg(A.grass(),8)
# Match the native ocean beneath small reef/rock props without recoloring any primary palette.
A.PALETTES[5][3]=(72,120,216)
kit['cliff']=[reg(A.cliff(mask,v),8) for mask,v in [(0,0),(0,1),(1,0),(4,1)]]
kit['cave']=asset(A.cave(),8)
kit['deck']=reg(A.board(),9);kit['stairs']=reg(A.stairs(),9)
# Piling pixels are an overlay over the original animated ocean, not painted water.
post=A.support();post.putdata([0 if v in [10,14] else v for v in post.getdata()])
post_mid=reg(post,9);desc=shoreline.descriptors(0x12b)[:4]+M[post_mid-640][:4]
preview=native[0x12b].copy();colored=post.copy();colored.putpalette(sum((list(c) for c in A.PALETTES[2]),[])+[0]*720)
preview.paste(colored.convert('RGB'),(0,0),Image.frombytes('L',post.size,post.tobytes()).point(lambda v:255 if v else 0))
kit['support']=native_meta(desc,0x22000415,preview)
kit['lamp']=asset(A.lamp(),9,A.board())
house_art,house_sources=house_kit(R,atlas)
def house_asset(name,roofbank):
 im=house_art[name];split=house_sources[name]['wall_start_row']
 return [asset(im.crop((0,y*16,112,y*16+16)),roofbank if y<split else 7,A.board())[0] for y in range(6)]
kit['house_blue']=house_asset('cerulean',9)
kit['house_green']=house_asset('sevii',10)
kit['house_gold']=house_asset('pallet',11)
kit['lodge']=house_asset('pallet',9)
kit['lighthouse']=asset(A.lighthouse(),9,A.board())
house_shapes={'house_blue':'cerulean','house_green':'sevii','house_gold':'pallet','lodge':'pallet'}
house_doors={'house_blue':house_sources['cerulean']['door_column'],'house_green':house_sources['sevii']['door_column'],'house_gold':house_sources['pallet']['door_column'],'lodge':house_sources['pallet']['door_column']}
kit['reefbeds']=[asset(A.reefpatch(i//2).transpose(Image.Transpose.FLIP_LEFT_RIGHT) if i%2 else A.reefpatch(i//2),12) for i in range(4)]
kit['tree']=asset(A.coastal_tree(),8,A.grass())
kit['coral']=[reg(A.coral(i),12) for i in range(6)];kit['rock']=reg(A.rock(),12)
kit['center']=[[0x48,0x49,0x49,0x4a,0x4a,0x4b],[0x48,0x49,0x49,0x4a,0x4a,0x4b],[0x50,0x51,0x51,0x52,0x52,0x53],[0x58,0x59,0x59,0x5a,0x59,0x5b],[0x60,0x61,0x4d,0x62,0x4e,0x63]]
rails={};reefedges={}
# Reusable topology masks, shared by all three tide illustrations.
def edge(kind,mask):
 cache,fn,bank={'rail':(rails,A.deckedge,9),'reef':(reefedges,A.reefedge,12)}[kind]
 if mask not in cache:cache[mask]=reg(fn(mask),bank)
 return cache[mask]
# Geography is authored as explicit elevation bands, reefs and individual piers.
import geography as G
decks=G.decks;permanent=G.permanent;buildings=G.buildings;landmarks=G.landmarks

def build(tide):
 g=[[kit['sea'][0]|0x3400 for x in range(W)] for y in range(H)]
 def put(x,y,mid,solid=False):
  if 0<=x<W and 0<=y<H:g[y][x]=mid|0x3000|(0x400 if solid else 0)
 def place(name,x,y,solid=True):
  for yy,row in enumerate(kit[name]):
   for xx,mid in enumerate(row):
    blocks=solid
    if name in house_shapes:blocks=solid and house_art[house_shapes[name]].crop((xx*16,yy*16,xx*16+16,yy*16+16)).getbbox() is not None
    put(x+xx,y+yy,mid,blocks)
 # Eastern mountain mass and northern bluffs have forest tops and short south faces.
 for x,y in G.cliffs:
  depth=sum((x,y+dy) in G.cliffs for dy in [1,2,3])
  put(x,y,kit['grass'] if depth==3 else kit['cliff'][2 if depth==2 else 3 if depth==0 else (x+y)%2],True)
 active_sand={p for p,height in G.heights.items() if height>=tide}
 for x,y in active_sand:
  if (x,y) not in G.cliffs:put(x,y,kit['sand'])
 for x,y in G.pools:put(x,y,kit['shallow'][0] if tide==0 else kit['sea'][0],tide>0)
 # Clusters have ragged outlines; low-tide footpaths remain clear through the reef.
 for x,y in sorted(G.reefs):
  if (x,y) in G.reef_route or (x,y) in decks:continue
  interior=all((x+dx,y+dy) in G.reefs for dx,dy in [(0,-1),(1,0),(0,1),(-1,0)])
  if tide==2:
   if (x*3+y)%7==0:put(x,y,kit['coral'][(x+y)%6],True)
  elif (x+y*3)%5<3:
   mid=kit['reefbeds'][(x//3+y//3)%4][y%2][x%2] if interior and (x,y) in active_sand else kit['coral'][(x+y)%6]
   put(x,y,mid,True)
 for x,y in [(15,35),(18,43),(29,51),(33,44),(43,44),(9,49),(30,29),(43,25)]:
  if (x,y) not in G.reef_route|G.cave_route|G.mid_route|decks:put(x,y,kit['rock'],True)
 for x,y in decks:
  mask=sum(1<<i for i,(dx,dy) in enumerate([(0,-1),(1,0),(0,1),(-1,0)]) if (x+dx,y+dy) not in decks and (x+dx,y+dy) not in permanent and (x+dx,y+dy) not in active_sand)
  # Rails occupy the outer few pixels; the tile center is a walkable board.
  # Adjacent ocean/cliff collision supplies the physical boundary.
  put(x,y,edge('rail',mask) if mask else kit['deck'])
 # Raised northwest residence and its short stair flight.
 for x in range(4,16):
  for y in range(3,14):put(x,y,kit['sand'])
 for x in range(4,16):
  for y in [12,13,14]:put(x,y,kit['cliff'][3 if y==14 else (x+y)%2],True)
 for y in range(12,21):
  for x in [11,12]:put(x,y,kit['stairs'])
 for name,x,y in buildings:place(name,x,y)
 for x,y in [(3,26),(13,23),(31,21),(44,35),(16,39),(34,39),(42,43),(52,56)]:place('lamp',x,y)
 for name,x,y in buildings:
  if name in house_doors:
   for yy in [y+5,y+6]:g[yy][x+house_doors[name]]&=~0xc00
 put(28,18,0x62);put(28,19,kit['deck'])
 # Visible sea-cave mouth is the intended Gym entrance. Its interior is still pending.
 place('cave',*G.cave_origin)
 for x,y in [(0,0),(4,0),(8,0),(21,0),(25,1),(29,0),(34,1),(39,2),(43,4),(47,2),(50,6),(45,10)]:place('tree',x,y)
 for x,y in [(30,20),(18,27),(41,35),(44,43),(13,12)]:put(x,y,0x3,True)
 for x,y in sorted(decks):
  if y<H-1 and (x,y+1) not in decks and (x,y+1) not in active_sand and x%3==0 and (g[y+1][x]&1023) in kit['sea']+kit['shallow']:put(x,y+1,kit['support'],True)
 for x,y in permanent:put(x,y,kit['sand'])
 # Native animated shoreline is applied only after all solid terrain and piers.
 before=[row[:] for row in g];water=set(kit['sea']+kit['shallow'])
 def wet(x,y):return 0<=x<W and 0<=y<H and (before[y][x]&1023) in water
 for y in range(H):
  for x in range(W):
   if before[y][x]&1023!=SAND:continue
   mask=sum(1<<i for i,(dx,dy) in enumerate([(0,-1),(1,0),(0,1),(-1,0)]) if wet(x+dx,y+dy))
   diagonals=sum(1<<i for i,(dx,dy) in enumerate([(-1,-1),(1,-1),(-1,1),(1,1)]) if wet(x+dx,y+dy))
   if mask or diagonals:put(x,y,shoreline.shoreline(mask,diagonals))
 return g
maps=[build(i) for i in range(3)]
assert len(T)<=384,(len(T),'tile budget exceeded');assert len(M)<=384
# Render the exact indexed graphics used in the native metatile definitions.
for i,n in enumerate(['Low','Mid','High']):
 out=Image.new('RGB',(W*16,H*16))
 for y,row in enumerate(maps[i]):
  for x,v in enumerate(row):out.paste(pixels[v&1023] if v&1023>=640 else native[v&1023],(x*16,y*16))
 out.save(B/f'Corvala_{n}_Tide_Map.png')
# Core services and permanent piers must remain accessible in every artwork state.
counts=[];tidal_access=[]
for tide,g in enumerate(maps):
 seen={(11,0)};q=deque(seen)
 while q:
  x,y=q.popleft()
  for xx,yy in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
   if 0<=xx<W and 0<=yy<H and (xx,yy) not in seen and not g[yy][xx]&0xc00:seen.add((xx,yy));q.append((xx,yy))
 for name,p in landmarks.items():assert tuple(p) in seen,('unreachable',tide,name,p)
 for name,x,y in buildings:
  if name in house_doors:assert (x+house_doors[name],y+6) in seen,('house entrance unreachable',tide,name,x,y)
 counts.append(len(seen));tidal_access.append({name:tuple(p) in seen for name,p in G.tidal_goals.items()})
assert [a['cave_approach'] for a in tidal_access]==[True,False,False],tidal_access
assert [a['reef_walk'] for a in tidal_access]==[True,False,False],tidal_access
assert [a['pool_lookout'] for a in tidal_access]==[True,True,False],tidal_access
g=maps[0]
# Persist all three authoring states; only map.bin is loaded by the game today.
state_dir=R/'tools/corvala/tide_states';state_dir.mkdir(exist_ok=True)
for name,state in zip(['low','mid','high'],maps):(state_dir/f'{name}.bin').write_bytes(struct.pack('<'+'H'*W*H,*sum(state,[])))
# Pack only after geometry and budget checks pass.
D.mkdir(parents=True,exist_ok=True);(D/'palettes').mkdir(exist_ok=True)
for bank in range(16):
 cs=A.PALETTES[bank-7] if 7<=bank<=12 else [(0,0,0)]*16
 (D/'palettes'/f'{bank:02}.pal').write_text('JASC-PAL\n0100\n16\n'+'\n'.join(' '.join(map(str,c)) for c in cs)+'\n')
sheet=Image.new('P',(128,((len(T)+15)//16)*8));sheet.putpalette(sum((list(c) for c in A.PALETTES[0]),[])+[0]*720)
for i,t in enumerate(T):sheet.paste(Image.frombytes('P',(8,8),t),(i%16*8,i//16*8))
sheet.save(D/'tiles.png');(D/'metatiles.bin').write_bytes(struct.pack('<'+'H'*(len(M)*8),*sum(M,[])));(D/'metatile_attributes.bin').write_bytes(struct.pack('<'+'I'*len(attrs),*attrs))
layouts=json.loads((R/'data/layouts/layouts.json').read_text());l=next(l for l in layouts['layouts'] if l['id']=='LAYOUT_CORVALA_TOWN');l.update(width=W,height=H,secondary_tileset='gTileset_Corvala')
(R/'data/layouts/layouts.json').write_text(json.dumps(layouts,indent=2)+'\n');(R/l['blockdata_filepath']).write_bytes(struct.pack('<'+'H'*W*H,*sum(g,[])));(R/l['border_filepath']).write_bytes(struct.pack('<4H',*[kit['sea'][0]|0x3400]*4))
p=R/'data/maps/Corvala_Town/map.json';m=json.loads(p.read_text());m['warp_events'][0].update(x=28,y=18,elevation=3);p.write_text(json.dumps(m,indent=2)+'\n')
manifest={'phase':'reference-driven overworld refinement; game uses LOW; MID/HIGH are previews','dimensions':[W,H],'tiles':len(T),'metatiles':len(M),'palette_banks':6,'kit':kit,'landmarks':landmarks,'buildings':buildings,'permanent_decks':sorted(decks),'walkable_cells_by_tide':counts,'tidal_access':tidal_access,'tidal_goals':G.tidal_goals,'geography':{'deck_cells':len(decks),'previous_deck_cells':945,'authoring_states_only':True,'cliff_cells':len(G.cliffs),'height_bands':{str(i):sum(v==i for v in G.heights.values()) for i in [0,1,2]}},'house_sources':house_sources,'house_doors':house_doors,'shoreline':{'native_sand':SAND,'primary_animation':'InitTilesetAnim_General','animation_graphics':[464,481],'frames':8,'ticks_per_frame':8,'generated_metatiles':sorted(set(shoreline.cache.values()))}}
(R/'tools/corvala/map.json').write_text(json.dumps(manifest,indent=2)+'\n');print(f'{len(T)}/384 tiles; {len(M)}/384 metatiles; all {len(landmarks)} landmarks connected.')
