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
# Persistent deck footprint follows the concept's individual house platforms.
decks=set();bridges=set()
def footprint(target,x,y,w,h):target.update((xx,yy) for yy in range(y,y+h) for xx in range(x,x+w))
platforms=[(3,20,9,10),(13,16,10,11),(23,13,11,14),(34,17,9,10),(43,20,9,10),(20,31,18,9),(41,37,11,8),(43,54,11,5)]
for rect in platforms:footprint(decks,*rect)
for rect in [(10,25,35,3),(25,26,3,8),(35,27,11,3),(46,29,3,12),(47,43,3,14)]:footprint(bridges,*rect)
decks|=bridges
# Right approach remains on high ground; north route descends beside the lodge.
permanent=set();footprint(permanent,10,0,3,3);footprint(permanent,13,2,5,3);footprint(permanent,16,4,3,10);footprint(permanent,16,12,11,2)
footprint(permanent,51,10,5,3);footprint(permanent,52,11,3,14);footprint(permanent,48,24,6,3)
# Reef islands: coordinate-stable silhouettes across tide states.
reefs=[]
for cx,cy,rx,ry in [(8,39,6,4),(12,52,5,4),(26,46,5,5),(36,53,3,3),(35,40,2,3),(44,48,2,2)]:
 cells=set()
 for y in range(cy-ry,cy+ry+1):
  for x in range(cx-rx,cx+rx+1):
   if ((x-cx)/rx)**2+((y-cy)/ry)**2<1:cells.add((x,y))
 reefs.append(cells)
reef_union=set().union(*reefs)
# Main low-tide beach has narrow channels rather than one large flat oval.
sand=set()
for y in range(10,45):
 for x in range(3,53):
  if ((x-27)/25)**2+((y-24)/21)**2<1 and not (y>32 and x>27):sand.add((x,y))
for rect in [(6,33,5,7),(11,39,6,3),(16,40,8,3),(23,39,5,7),(27,44,4,3)]:footprint(sand,*rect)
# Headland boundary varies by column, with a natural notch for the northeast cave.
cliff_bottom=[10+((x//4)%3) for x in range(W)]
for x in range(4,20):cliff_bottom[x]=14
for x in range(20,40):cliff_bottom[x]=8+(x//3)%3
for x in range(40,56):cliff_bottom[x]=15+(x//3)%3
buildings=[('lodge',6,4),('house_green',4,21),('house_blue',14,17),('center',25,14),('house_green',35,18),('house_gold',44,21),('house_green',21,32),('house_gold',30,32),('lighthouse',49,31)]
landmarks={'center_door':[28,18],'north_exit':[11,0],'east_exit':[55,11],'lighthouse_approach':[49,39],'arrival_pier':[48,56]}
# Build a tide artwork state; only the low state is installed into the game.
def build(tide):
 g=[[kit['sea'][(x//3+y//4)%2]|0x3400 for x in range(W)] for y in range(H)]
 def put(x,y,mid,solid=False):
  if 0<=x<W and 0<=y<H:g[y][x]=mid|0x3000|(0x400 if solid else 0)
 def place(name,x,y,solid=True):
  for yy,row in enumerate(kit[name]):
   for xx,mid in enumerate(row):
    blocks=solid
    if name in house_shapes:blocks=solid and house_art[house_shapes[name]].crop((xx*16,yy*16,xx*16+16,yy*16+16)).getbbox() is not None
    put(x+xx,y+yy,mid,blocks)
 # Shallow lagoon forms a blue-green rim around the islands.
 for y in range(9,H):
  for x in range(1,W-1):
   if tide<2 and ((x-26)/28)**2+((y-34)/28)**2<1:put(x,y,kit['shallow'][(x//4+y//3)%2],tide>0)
 for x in range(W):
  for y in range(cliff_bottom[x]):
   if y<cliff_bottom[x]-3:put(x,y,kit['grass'],True)
   else:put(x,y,kit['cliff'][2 if y==cliff_bottom[x]-3 else 3 if y==cliff_bottom[x]-1 else (x+y)%2],True)
 # Western edge tapers into the lower bay, leaving breathing room around the reefs.
 for y in range(12,33):
  for x in range(max(1,5-(y-12)//7)):
   put(x,y,kit['cliff'][(x+y)%2],True)
 # Lighthouse rock remains exposed at every tide.
 lighthouse_land={(x,y) for y in range(33,42) for x in range(48,56) if ((x-52)/5)**2+((y-37)/5)**2<1}
 active_sand=(sand if tide==0 else {(x,y) for x,y in sand if y<19 and x<22} if tide==1 else set())|permanent|lighthouse_land
 for x,y in active_sand:
  put(x,y,kit['sand'])
 for idx,cells in enumerate(reefs):
  for x,y in cells:
   outside=sum(1<<i for i,(dx,dy) in enumerate([(0,-1),(1,0),(0,1),(-1,0)]) if (x+dx,y+dy) not in cells)
   # At high tide only the tall coral crowns break the surface.
   if tide==2 and outside:continue
   put(x,y,edge('reef',outside) if outside else kit['reefbeds'][(idx+(x//2)*3+y//2)%4][(y+idx)%2][(x+idx)%2],True)
 # Coral gardens extend off the reef shelves into the shallow western lagoon.
 for x,y in [(2,35),(3,38),(4,43),(6,45),(7,48),(2,50),(3,54),(18,40),(21,44),(22,49),(30,50),(32,46),(38,49),(37,43)]:
  if (x,y) not in decks and (x,y) not in reef_union:put(x,y,kit['coral'][(x+y)%6],True)
 # Rock accents have deliberate spacing and never occupy a bridge.
 for x,y in [(17,43),(20,51),(33,55),(39,45),(45,50),(7,47),(34,35)]:put(x,y,kit['rock'],True)
 for x,y in decks:
  mask=sum(1<<i for i,(dx,dy) in enumerate([(0,-1),(1,0),(0,1),(-1,0)]) if (x+dx,y+dy) not in decks and (x+dx,y+dy) not in permanent)
  # Walkways meet platforms through the same tile footprint, so rails never sever them.
  put(x,y,edge('rail',mask) if mask else kit['deck'],bool(mask))
 # Lodge has a separate stone terrace, with a stairway down to the town.
 for x in range(4,16):
  for y in range(3,14):
   if not (6<=x<13 and 4<=y<10):put(x,y,kit['sand'])
 for x in range(4,16):
  for y in [12,13,14]:put(x,y,kit['cliff'][3 if y==14 else (x+y)%2],True)
 for y in range(13,20):
  for x in [11,12]:put(x,y,kit['stairs'])
 # Small wooden stairs connect to the lighthouse's lower landing.
 for y in range(43,45):
  for x in [47,48,49]:put(x,y,kit['stairs'])
 for name,x,y in buildings:place(name,x,y)
 for x,y in [(3,27),(13,24),(32,24),(42,25),(20,37),(37,37),(41,42),(52,56)]:place('lamp',x,y)
 # Front-door approaches on every platform stay open for later interior warps.
 for name,x,y in buildings:
  if name in ['center','lighthouse']:continue
  for yy in [y+5,y+6]:g[yy][x+house_doors[name]]&=~0xc00
 # The native Center door retains its standard animation and warp behavior.
 put(28,18,0x62);put(28,19,kit['deck'])
 # A recessed cave spans three tiles; entry behavior/warp will come with the interior.
 place('cave',47,7);put(48,10,kit['sand'])
 # Coastal trees/mangroves appear on high ground, never across paths or roof silhouettes.
 for x,y in [(0,0),(3,0),(6,0),(20,0),(23,0),(26,0),(29,0),(32,1),(35,0),(38,0),(41,1),(44,0),(47,0),(50,0),(53,1)]:place('tree',x,y)
 # Native signposts and barrels retain FireRed proportions.
 for x,y in [(29,19),(19,26),(43,28),(44,41),(13,12)]:put(x,y,0x3,True)
 # Visible pilings only appear below the deck, never over a walkable shore tile.
 for x,y in sorted(decks):
  if y<H-1 and (x,y+1) not in decks and (x,y+1) not in active_sand and x%3==0 and (g[y+1][x]&1023) in kit['sea']+kit['shallow']:put(x,y+1,kit['support'],True)
 # Preserve exact route seam coordinates from the existing Vidra route maps.
 for x,y in permanent:put(x,y,kit['sand'])
 # Autotile the final visible beach. Piers/cliffs/objects are not water neighbors.
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
counts=[]
for tide,g in enumerate(maps):
 seen={(11,0)};q=deque(seen)
 while q:
  x,y=q.popleft()
  for xx,yy in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
   if 0<=xx<W and 0<=yy<H and (xx,yy) not in seen and not g[yy][xx]&0xc00:seen.add((xx,yy));q.append((xx,yy))
 for name,p in landmarks.items():assert tuple(p) in seen,('unreachable',tide,name,p)
 for name,x,y in buildings:
  if name in house_doors:assert (x+house_doors[name],y+6) in seen,('house entrance unreachable',tide,name,x,y)
 counts.append(len(seen))
g=maps[0]
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
manifest={'phase':'reference-driven overworld refinement; game uses LOW; MID/HIGH are previews','dimensions':[W,H],'tiles':len(T),'metatiles':len(M),'palette_banks':6,'kit':kit,'landmarks':landmarks,'buildings':buildings,'permanent_decks':sorted(decks),'walkable_cells_by_tide':counts,'house_sources':house_sources,'house_doors':house_doors,'shoreline':{'native_sand':SAND,'primary_animation':'InitTilesetAnim_General','animation_graphics':[464,481],'frames':8,'ticks_per_frame':8,'generated_metatiles':sorted(set(shoreline.cache.values()))}}
(R/'tools/corvala/map.json').write_text(json.dumps(manifest,indent=2)+'\n');print(f'{len(T)}/384 tiles; {len(M)}/384 metatiles; all {len(landmarks)} landmarks connected.')
