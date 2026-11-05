#!/usr/bin/env python3
"""Build the editable 80x64 Corvala LOW map, assets and reciprocal route seams.

geography.py is authoritative. Backport Porymap edits there before regenerating.
MID/HIGH redesign and runtime tide replacement are deferred to composition review.
"""
from pathlib import Path
from collections import deque
import struct,json,sys
from io import BytesIO
from PIL import Image, ImageDraw
import art as A
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'tools/havora'))
from render import atlas
from native_reference import install
from shoreline import NativeShore, SAND
from stilt_houses import kit as house_kit
native=atlas('cinnabar_island');install(native)
import geography as G
W,H=G.W,G.H
D=R/'data/tilesets/secondary/corvala';B=R/'build/corvala';B.mkdir(parents=True,exist_ok=True)
def write(path,data):
 """Keep identical files untouched: no spurious Porymap reloads or ROM rebuilds."""
 if isinstance(data,str):
  if path.suffix=='.pal':data=data.replace('\n','\r\n')
  data=data.encode('utf-8')
 if not path.exists() or path.read_bytes()!=data:path.write_bytes(data)
def save_image(im,path):
 buffer=BytesIO();im.save(buffer,format='PNG');write(path,buffer.getvalue())
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
kit['rock_top']=0x1f7
# Match the native ocean beneath small reef/rock props without recoloring any primary palette.
A.PALETTES[5][3]=(72,120,216)
kit['cliff']=[0x71,0x71,0x71,0x79]
kit['cave']=[[0xa0,0xa1,0xa2],[0xa8,0xa9,0xaa]]
kit['deck']=reg(A.board(),9);kit['stairs']=reg(A.stairs(),9)
# Piling pixels are an overlay over the original animated ocean, not painted water.
post=A.support();post.putdata([0 if v in [10,14] else v for v in post.getdata()])
post_mid=reg(post,9);desc=shoreline.descriptors(0x12b)[:4]+M[post_mid-640][:4]
preview=native[0x12b].copy();colored=post.copy();colored.putpalette(sum((list(c) for c in A.PALETTES[2]),[])+[0]*720)
preview.paste(colored.convert('RGB'),(0,0),Image.frombytes('L',post.size,post.tobytes()).point(lambda v:255 if v else 0))
kit['support']=native_meta(desc,0x22000415,preview)
house_art,house_sources=house_kit(R,atlas)
def definitions(mid):
 return M[mid-640] if mid>=640 else shoreline.descriptors(mid)
def preview(mid):return pixels[mid] if mid>=640 else native[mid]
primary_sheet=Image.open(R/'data/tilesets/primary/general/tiles.png')
primary_palettes=[]
for bank in range(7):
 rows=(R/f'data/tilesets/primary/general/palettes/{bank:02}.pal').read_text().splitlines()[3:19]
 primary_palettes.append([tuple(map(int,row.split())) for row in rows])
bottom_cache={}

def bottom_preview(base):
 # New objects occupy the foreground; only retain the ground layer beneath.
 if base in bottom_cache:return bottom_cache[base].copy()
 out=Image.new('RGB',(16,16))
 for q,w in enumerate(definitions(base)[:4]):
  tid=w&1023;bank=w>>12
  colors=primary_palettes[bank] if bank<7 else A.PALETTES[bank-7]
  for y in range(8):
   for x in range(8):
    xx=7-x if w&1024 else x;yy=7-y if w&2048 else y
    value=(primary_sheet.getpixel(((tid%(primary_sheet.width//8))*8+xx,
            (tid//(primary_sheet.width//8))*8+yy)) if tid<640
           else T[tid-640][yy*8+xx])
    out.putpixel((q%2*8+x,q//2*8+y),colors[value])
 bottom_cache[base]=out
 return out.copy()

def overlay(im,bank,base):
 raw=reg(im,bank);desc=definitions(base)[:4]+M[raw-640][:4]
 out=bottom_preview(base);colored=im.copy()
 colored.putpalette(sum((list(c) for c in A.PALETTES[bank-7]),[])+[0]*720)
 out.paste(colored.convert('RGB'),(0,0),Image.frombytes('L',im.size,im.tobytes()).point(lambda v:255 if v else 0))
 return native_meta(desc,0,out)
# Composite each placed house over its actual terrain. Packing a second,
# unused sand-backed copy of every facade wastes the metatile budget.
for name in ('house_blue','house_green','house_gold','lodge'):
 kit[name]=[[0]*7 for _ in range(6)]
lighthouse_art=A.lighthouse()
kit['lighthouse']=[[0]*3 for _ in range(7)]
house_shapes={'house_blue':'cerulean','house_green':'sevii','house_gold':'pallet','lodge':'pallet'}
house_doors={'house_blue':house_sources['cerulean']['door_column'],'house_green':house_sources['sevii']['door_column'],'house_gold':house_sources['pallet']['door_column'],'lodge':house_sources['pallet']['door_column']}
# Unused legacy trees, reef carpets and painted-water props are not packed.
# Their source art remains available in art.py for future composition work.
kit['center']=[[0x48,0x49,0x49,0x4a,0x4a,0x4b],[0x50,0x51,0x51,0x52,0x52,0x53],[0x58,0x59,0x59,0x5a,0x59,0x5b],[0x60,0x61,0x4d,0x62,0x4e,0x63]]

# Terrain and art are generated together. MID/HIGH are deliberately deferred:
# old 56x60 authoring binaries are archived, never presented as resized states.
rails={}
def edge(mask):
 if mask not in rails:rails[mask]=reg(A.deckedge(mask),9)
 return rails[mask]

def build_low():
 # Native Surf requires clear collision bits and elevation 1 water adjacent to
 # elevation 3 land. Elevation mismatch prevents walking into the sea.
 g=[[0x12b|0x1000 for _ in range(W)] for _ in range(H)]
 def put(x,y,mid,solid=False,elevation=3):
  if 0<=x<W and 0<=y<H:g[y][x]=mid|(elevation<<12)|(0x400 if solid else 0)
 def place(name,x,y):
  for yy,row in enumerate(kit[name]):
   for xx,mid in enumerate(row):
    blocks=True
    if name in house_shapes:
     blocks=house_art[house_shapes[name]].crop((xx*16,yy*16,xx*16+16,yy*16+16)).getbbox() is not None
    if name in house_shapes:
     im=house_art[house_shapes[name]].crop((xx*16,yy*16,xx*16+16,yy*16+16))
     bank={'house_blue':9,'house_green':10,'house_gold':11,'lodge':9}[name] if yy<3 else 7
     mid=overlay(im,bank,g[y+yy][x+xx]&1023)
    if name=='lighthouse':
     im=lighthouse_art.crop((xx*16,yy*16,xx*16+16,yy*16+16))
     if im.getbbox() is None:continue
     mid=overlay(im,9,g[y+yy][x+xx]&1023)
    if name in house_shapes or name=='lighthouse':kit[name][yy][xx]=mid
    put(x+xx,y+yy,mid,blocks)
 # Sandy rock plateaus, with two-cell faces and a separate northern terrace.
 for region in [G.cliffs,G.terrace]:
  for x,y in sorted(region):
   depth=sum((x,y+dy) in region for dy in [1,2])
   top=kit['grass'] if (x,y) in G.grass else kit['rock_top']
   mid=top if depth==2 else kit['cliff'][0 if depth else 3]
   put(x,y,mid,not (region is G.cliffs and (x,y) in G.bluff and depth==2))
 for x,y in sorted(G.beach-G.cliffs):put(x,y,kit['grass'] if (x,y) in G.grass else SAND)
 for x,y in sorted(G.pools-G.cliffs-G.beach):put(x,y,kit['shallow'][0])
 for x,y in sorted(G.lagoon):put(x,y,0x12b,elevation=1)
 # Feather turf into sand/rock, instead of hard square color changes.
 for x,y in sorted(G.grass):
  if g[y][x]&1023!=kit['grass']:continue
  mask=sum(1<<i for i,(dx,dy) in enumerate([(0,-1),(1,0),(0,1),(-1,0)])
           if (x+dx,y+dy) not in G.grass)
  if not mask:continue
  land=A.grass();edge_color=7 if (x,y) in G.cliffs else 6
  for py in range(16):
   for px in range(16):
    dist=[py,15-px,15-py,px]
    if any(mask&(1<<i) and dist[i] < (1+(px+py)%3) for i in range(4)):
     land.putpixel((px,py),edge_color)
  put(x,y,reg(land,8),bool(g[y][x]&0xc00))
 # Sparse stone impressions guide the central village without paving the beach.
 for x,y in sorted(G.village_paths-G.cliffs-G.pools-G.decks):
  if g[y][x]&1023 not in (SAND,kit['grass']):continue
  paving=A.im();d=ImageDraw.Draw(paving)
  for px,py in [(3,5),(10,11)]:
   d.line((px,py,px+3,py),fill=5);d.line((px+1,py+1,px+4,py+1),fill=7)
  put(x,y,overlay(paving,8,g[y][x]&1023))
 # Native coral pixels have transparent surrounds over the sand or animated sea.
 for x,y in sorted(G.reefs-G.reef_route):
  if not any(((x-cx)/rx)**2+((y-cy)/ry)**2<.8 for cx,cy,rx,ry in G.reef_gardens):continue
  if (x+3*y)%5>=3:continue
  im=A.coral((x+y)%6);im.putdata([0 if v==3 else v for v in im.getdata()])
  put(x,y,overlay(im,12,g[y][x]&1023),True)
 for x,y in sorted(G.decks):
  mask=sum(1<<i for i,(dx,dy) in enumerate([(0,-1),(1,0),(0,1),(-1,0)])
           if (x+dx,y+dy) not in G.decks|G.beach)
  put(x,y,edge(mask) if mask else kit['deck'])
 for x,y in sorted(G.stairs):put(x,y,kit['stairs'])
 for name,x,y in G.buildings:place(name,x,y)
 for name,x,y in G.buildings:
  if name in house_doors:
   for yy in [y+5,y+6]:g[yy][x+house_doors[name]]&=~0xc00
 cx,cy=G.landmarks['center_door'];put(cx,cy,0x62);put(cx,cy+1,SAND)
 # A small native opening; a working Gym interior and cave warp are a later pass.
 for yy,row in enumerate(kit['cave']):
  for xx,mid in enumerate(row):put(G.cave_origin[0]+xx-1,G.cave_origin[1]+yy-1,mid,True)
 # Palm canopies stay passable over their existing ground; only trunks block.
 palm=A.palm()
 for px,py in G.palms:
  assert all((g[py+2][px+xx]&1023) not in kit['sea']+kit['shallow'] for xx in range(2)),('palm trunk in water',px,py)
  for yy in range(3):
   for xx in range(2):
    x,y=px+xx,py+yy
    if not (0<=x<W and 0<=y<H):continue
    base=g[y][x]&1023
    if base in kit['sea']+kit['shallow']:continue
    im=palm.crop((xx*16,yy*16,xx*16+16,yy*16+16))
    put(x,y,overlay(im,8,base),bool(g[y][x]&0xc00) or yy==2)
 for x,y in G.rocks:
  if (x,y) in G.east_route|G.west_route|G.reef_route|G.decks:continue
  im=A.rock();im.putdata([0 if v==3 else v for v in im.getdata()])
  put(x,y,overlay(im,12,g[y][x]&1023),True)
 # Paired lanterns give the service square and lighthouse landing a human scale.
 lamp=A.lamp()
 for x,y in G.lamps:
  if (x,y) in G.landmarks.values():continue
  for dy in range(2):
   base=g[y+dy][x]&1023
   if base in kit['sea']+kit['shallow']:continue
   put(x,y+dy,overlay(lamp.crop((0,dy*16,16,dy*16+16)),9,base),dy==1 or bool(g[y+dy][x]&0xc00))
 # Pilings keep the original animated primary water beneath their overlay.
 for x,y in sorted(G.decks):
  if y+1<H and x%3==0 and (g[y+1][x]&1023) in kit['sea']:
   put(x,y+1,kit['support'],True)
 # Native animated surf is assembled last, only against actual visible water.
 before=[row[:] for row in g];water=set(kit['sea']+kit['shallow'])
 def wet(x,y):return 0<=x<W and 0<=y<H and before[y][x]&1023 in water
 for y in range(H):
  for x in range(W):
   if before[y][x]&1023!=SAND:continue
   mask=sum(1<<i for i,(dx,dy) in enumerate([(0,-1),(1,0),(0,1),(-1,0)]) if wet(x+dx,y+dy))
   diagonals=sum(1<<i for i,(dx,dy) in enumerate([(-1,-1),(1,-1),(-1,1),(1,1)]) if wet(x+dx,y+dy))
   if mask or diagonals:put(x,y,shoreline.shoreline(mask,diagonals))
 return g

g=build_low()
assert len(T)<=384,(len(T),'tile budget exceeded')
assert len(M)<=384,(len(M),'metatile budget exceeded')
# Always emit the candidate for visual review, even if navigation rejects it.
out=Image.new('RGB',(W*16,H*16))
for y,row in enumerate(g):
 for x,v in enumerate(row):out.paste(preview(v&1023),(x*16,y*16))
save_image(out,B/'Corvala_Low_Tide_Map.png')
save_image(out,R/'docs/corvala/low-tide-playable.png')
# Check real collision bits from the western approach, including every doorway.
start=tuple(G.landmarks['west_exit']);seen={start};q=deque(seen)
while q:
 x,y=q.popleft()
 for xx,yy in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
  if 0<=xx<W and 0<=yy<H and (xx,yy) not in seen and not g[yy][xx]&0xc00 and g[yy][xx]>>12==3:
   seen.add((xx,yy));q.append((xx,yy))
for name,p in G.landmarks.items():assert tuple(p) in seen,('unreachable',name,p)
for name,x,y in G.buildings:
 if name in house_doors:assert (x+house_doors[name],y+6) in seen,('house entrance unreachable',name,x,y)

# Keep legacy states intact, but clearly outside the active state directory.
state_dir=R/'tools/corvala/tide_states';legacy=state_dir/'legacy_56x60'
legacy.mkdir(exist_ok=True)
for name in ['low','mid','high']:
 p=state_dir/f'{name}.bin'
 if p.exists() and p.stat().st_size==56*60*2:
  target=legacy/p.name
  if not target.exists():p.rename(target)
raw=struct.pack('<'+'H'*W*H,*sum(g,[]));write(state_dir/'low.bin',raw)
D.mkdir(parents=True,exist_ok=True);(D/'palettes').mkdir(exist_ok=True)
for bank in range(16):
 cs=A.PALETTES[bank-7] if 7<=bank<=12 else [(0,0,0)]*16
 write(D/'palettes'/f'{bank:02}.pal','JASC-PAL\n0100\n16\n'+'\n'.join(' '.join(map(str,c)) for c in cs)+'\n')
sheet=Image.new('P',(128,((len(T)+15)//16)*8));sheet.putpalette(sum((list(c) for c in A.PALETTES[0]),[])+[0]*720)
for i,t in enumerate(T):sheet.paste(Image.frombytes('P',(8,8),t),(i%16*8,i//16*8))
save_image(sheet,D/'tiles.png')
write(D/'metatiles.bin',struct.pack('<'+'H'*(len(M)*8),*sum(M,[])))
write(D/'metatile_attributes.bin',struct.pack('<'+'I'*len(attrs),*attrs))
layouts=json.loads((R/'data/layouts/layouts.json').read_text())
l=next(l for l in layouts['layouts'] if l['id']=='LAYOUT_CORVALA_TOWN')
l.update(width=W,height=H,secondary_tileset='gTileset_Corvala')
write(R/'data/layouts/layouts.json',json.dumps(layouts,indent=2)+'\n')
write(R/l['blockdata_filepath'],raw)
write(R/l['border_filepath'],struct.pack('<4H',*[0x12b|0x1000]*4))
# Explicit, reciprocal seams: town y26 = Coastal Road y11; town y27 = Harbor y11.
# Coastal Road already has a two-cell eastern outlet. Its north/Eldervale link
# stays untouched; only its former south/Corvala connection is redirected east.
connections=[{'map':'MAP_VIDRA_COASTAL_ROAD','offset':15,'direction':'left'},
             {'map':'MAP_VIDRA_HARBOR_ROAD','offset':16,'direction':'right'}]
p=R/'data/maps/Corvala_Town/map.json';m=json.loads(p.read_text())
cx,cy=G.landmarks['center_door']
m['connections']=connections;m['warp_events'][0].update(x=cx,y=cy,elevation=3)
write(p,json.dumps(m,indent=2)+'\n')
heal_path=R/'src/data/heal_locations.json'
heal=json.loads(heal_path.read_text())
landing=next(v for v in heal['heal_locations'] if v['id']=='HEAL_LOCATION_QUANTUM_COASTAL_CITY')
landing.update(x=cx,y=cy+1)
write(heal_path,json.dumps(heal,indent=2)+'\n')
for name,direction,offset in [('Vidra_CoastalRoad','right',-15),('Vidra_HarborRoad','left',-16)]:
 p=R/f'data/maps/{name}/map.json';m=json.loads(p.read_text())
 for c in m['connections']:
  if c['map']=='MAP_CORVALA_TOWN':c.update(direction=direction,offset=offset)
 write(p,json.dumps(m,indent=2)+'\n')
manifest={'phase':'80x64 LOW cliff-and-palm redesign; MID/HIGH deferred',
 'dimensions':[W,H],'tiles':len(T),'metatiles':len(M),'palette_banks':6,'kit':kit,
 'landmarks':G.landmarks,'buildings':G.buildings,'permanent_decks':sorted(G.decks),
 'walkable_cells':len(seen),'connections':connections,
 'geography':{'deck_cells':len(G.decks),'previous_deck_cells':712,
              'cliff_cells':len(G.cliffs),'palm_count':len(G.palms)},
 'house_sources':house_sources,'house_doors':house_doors,
 'tide_states':{'installed':'low','runtime_switching':False,'legacy_dimensions':[56,60],
                'legacy_directory':'tools/corvala/tide_states/legacy_56x60'},
 'shoreline':{'native_sand':SAND,'primary_animation':'InitTilesetAnim_General',
 'animation_graphics':[464,481],'frames':8,'ticks_per_frame':8,
 'generated_metatiles':sorted(set(shoreline.cache.values()))}}
write(R/'tools/corvala/map.json',json.dumps(manifest,indent=2)+'\n')
print(f'{len(T)}/384 tiles; {len(M)}/384 metatiles; {len(seen)} connected cells; LOW only.')
