#!/usr/bin/env python3
"""Complete Slateport stalls, Bond Bridge forest mouth, and court chalk.

One-time shared-tileset migration. All placed art and animation slots are pinned;
only unplaced obsolete catalog fragments can be archived and reclaimed.
"""
import json,struct,hashlib
from pathlib import Path
from collections import defaultdict
from PIL import Image,ImageDraw
import numpy as np
R=Path(__file__).resolve().parents[2];S=R/'tools/havora/source_art/editor_kits';OUT=R/'tools/havora/editor-kits.json'
assert not OUT.exists(),'Already installed; edit these kits in Porymap.'
def js(p):return json.loads((R/p).read_text())
def words(p):
 b=(R/p).read_bytes();return list(struct.unpack('<'+'H'*(len(b)//2),b))
def gfx(path):
 im=Image.open(path);return [im.crop((x,y,x+8,y+8)).tobytes() for y in range(0,im.height,8) for x in range(0,128,8)]
def flip(b,f):
 im=Image.frombytes('P',(8,8),b)
 if f&1024:im=im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
 if f&2048:im=im.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
 return im.tobytes()
def canon(b):return min((flip(b,f),f) for f in (0,1024,2048,3072))
T=[];M=[];A=[];P=[]
for g in ('primary','secondary'):
 p=f'data/tilesets/{g}/havora_city/';T+=gfx(R/p/'tiles.png');v=words(p+'metatiles.bin');M += [tuple(v[i:i+8]) for i in range(0,len(v),8)];b=(R/p/'metatile_attributes.bin').read_bytes();A+=list(struct.unpack('<'+'I'*(len(b)//4),b))
for i in range(13):P.append([tuple(map(int,l.split())) for l in (R/f'data/tilesets/{"primary" if i<7 else "secondary"}/havora_city/palettes/{i:02}.pal').read_text().splitlines()[3:19]])
oldT=T[:];oldM=M[:];oldA=A[:];placed=set();protected=set()
for l in js('data/layouts/layouts.json')['layouts']:
 if l['primary_tileset']=='gTileset_HavoraCityPrimary':
  for key in ('blockdata_filepath','border_filepath'):placed|={v&1023 for v in words(l[key])}
protected |= placed | set(js('tools/havora/city-tileset.json')['native_general_ids'].values()) | set(range(168,172))
for f,key in [('civic-tiles','assets'),('green-houses','kits'),('native-houses','kits'),('fountain','kits')]:
 for grid in js('tools/havora/'+f+'.json')[key].values():
  for row in grid:protected.update(row)
extra=js('tools/havora/authoring-assets.json')
for ids in extra['statue_metatiles'].values():protected.update(ids)
shared=js('tools/havora/shared-tileset.json');hm={int(k):v for k,v in shared['metatile_mapping']['harbor'].items()};harbor=js('tools/havora/assets.json')
for asset in harbor['assets'].values():
 for row in asset['metatiles']:protected.update(hm[i] for i in row if i in hm)
for e in harbor['catalog']:
 if (e['town']=='pacifidlog' or e['town']=='slateport' and e['source_id']<0x260) and e['havora_id'] in hm:protected.add(hm[e['havora_id']])
# Every blank metatile that a different pending feature has reserved is protected
# by its named kit above or by its placed map use.
fixed=set(range(416,482))|set(range(508,512))|set(range(896,1024))|{0,20}|set(js('tools/havora/fountain.json')['animation_graphic_ids'])
refs=defaultdict(set)
for i,m in enumerate(M):
 if any(m) or A[i]:
  for v in m:refs[v&1023].add(i)
pinned=fixed|{v&1023 for i in protected for v in M[i]};cache={}
for i,b in enumerate(T):
 if i not in fixed or i in (0,20):key,f=canon(b);cache.setdefault(key,(i,f))
archive={'metatiles':{},'graphics':{}};retired=set();added=[]
def allocate(key):
 if key in cache:
  i,f=cache[key];pinned.add(i);return i,f
 free=[i for i in range(1024) if i not in pinned and not(refs[i]&protected)]
 assert free,('No safe static graphic slots',len(archive['graphics']),len(pinned))
 i=min(free,key=lambda i:(len(refs[i]),i))
 for mid in list(refs[i]):
  assert mid not in protected;archive['metatiles'][str(mid)]={'words':M[mid],'attribute':A[mid]};retired.add(mid)
  for v in M[mid]:refs[v&1023].discard(mid)
  M[mid]=(0,)*8;A[mid]=0
 archive['graphics'][str(i)]=list(T[i]);oldkey,_=canon(T[i])
 if cache.get(oldkey,(None,None))[0]==i:del cache[oldkey]
 T[i]=key;cache[key]=(i,0);pinned.add(i);return i,0

def add(ds,attr=0):
 for b,_,_ in ds:
  key,_=canon(b)
  if key in cache:pinned.add(cache[key][0])
 out=[]
 for b,flags,bank in ds:
  key,f=canon(b);i,cf=allocate(key);out.append(i|(flags^f^cf)|(bank<<12))
 for i,m in enumerate(M):
  if m==tuple(out) and A[i]==attr:protected.add(i);return i
 mid=next(i for i,m in enumerate(M) if not any(m) and not A[i] and i not in protected)
 M[mid]=tuple(out);A[mid]=attr;protected.add(mid);added.append(mid)
 for v in out:refs[v&1023].add(mid)
 return mid
pal=np.array(P,dtype=np.int32)
def converted(src,palette):
 a=np.frombuffer(src,dtype=np.uint8);rgb=np.array(palette)[a];dist=((rgb[:,None,None,:]-pal[None,:,1:,:])**2).sum(3);bank=int(dist.min(2)[a!=0].sum(0).argmin());idx=(dist[:,bank].argmin(1)+1).astype('uint8');idx[a==0]=0;return idx.tobytes(),bank
# Recover full left/right awning legs and counter ends from the exact native
# Emerald source that supplied the existing harbor art.
ET=gfx(S/'general-tiles.png')+gfx(S/'slateport-tiles.png');v=words(str((S/'slateport-metatiles.bin').relative_to(R)));EM=[tuple(v[i:i+8]) for i in range(0,len(v),8)];EP={i:[tuple(map(int,l.split())) for l in (S/f'emerald-{i}.pal').read_text().splitlines()[3:19]] for i in (0,2,6,7,8,9)}
stall_source={'wide':[[0x205,0x20d,0x20e,0x20f,0x227],[0x235,0x2f8,0x2f9,0x2fa,0x22f],[0x23d,0x21b,0x21b,0x285,0x26c]],'narrow':[[0x225,0x20d,0x20f,0x207],[0x22d,0x2f8,0x2fa,0x237],[0x26b,0x285,0x285,0x23f]]}
# Add all associated goods/frontage already present in the source editor sheet.
extras=[0x20b,0x20c,0x213,0x214,0x21b,0x21c,0x220,0x221,0x222,0x223,0x224,0x228,0x229,0x22a,0x22b,0x230,0x231,0x238,0x239,0x23b]
sourceids={v for grid in stall_source.values() for row in grid for v in row}|set(extras);edesc={}
for sid in sorted(sourceids):
 ds=[]
 for v in EM[sid-512]:
  b,bank=converted(ET[v&1023],EP[v>>12]);ds.append((b,v&0xc00,bank))
 edesc[sid]=ds
# Pre-pin every existing descriptor match before any source allocation.
for ds in edesc.values():
 for b,_,_ in ds:
  key,_=canon(b)
  if key in cache:pinned.add(cache[key][0])
stallmap={sid:add(ds) for sid,ds in edesc.items()}
stalls={n:[[stallmap[v] for v in row] for row in grid] for n,grid in stall_source.items()}
# FireRed Bond Bridge's four-by-three shadowed entrance: this is the reference
# supplied by the user, not the Viridian Forest gatehouse.
FT=gfx(R/'data/tilesets/primary/general/tiles.png')+gfx(R/'data/tilesets/secondary/sevii_islands_123/tiles.png');v=words('data/tilesets/secondary/sevii_islands_123/metatiles.bin');FM=[tuple(v[i:i+8]) for i in range(0,len(v),8)];FP=[]
for i in range(13):FP.append([tuple(map(int,l.split())) for l in (R/f'data/tilesets/{"primary/general" if i<7 else "secondary/sevii_islands_123"}/palettes/{i:02}.pal').read_text().splitlines()[3:19]])
forest_source=[[0x330,0x331,0x332,0x333],[0x338,0x339,0x33a,0x33b],[0x340,0x341,0x342,0x343]];forest=[]
for row in forest_source:
 out=[]
 for sid in row:
  ds=[]
  for v in FM[sid-640]:
   b,bank=converted(FT[v&1023],FP[v>>12]);ds.append((b,v&0xc00,bank))
  # Visual kit only; entrance warps must be attached to the intended route.
  out.append(add(ds))
 forest.append(out)
# Crisp two-pixel white chalk at native GBA resolution, packed into ordinary
# metatiles; the court's sand underlayer and collision/elevation stay intact.
chalk=Image.new('P',(128,96),0);d=ImageDraw.Draw(chalk)
d.rectangle((6,6,121,89),outline=1,width=2);d.ellipse((48,32,80,64),outline=1,width=2);d.ellipse((59,43,69,53),outline=1,width=2)
d.line((6,48,48,48),fill=1,width=2);d.line((80,48,121,48),fill=1,width=2);d.line((50,48,59,48),fill=1,width=2);d.line((69,48,78,48),fill=1,width=2)
white=min(((sum((int(c)-248)**2 for c in P[b][i]),b,i) for b in range(13) for i in range(1,16)));_,whitebank,whiteidx=white
l=next(l for l in js('data/layouts/layouts.json')['layouts'] if l['name']=='Havora_WestQuadrant_Layout');blocks=words(l['blockdata_filepath']);oldblocks=blocks[:];court=[];sand=js('tools/havora/gym-garden.json')['added_metatiles']['sand']
for y in range(6):
 row=[]
 for x in range(8):
  ds=[(T[v&1023],v&0xc00,v>>12) for v in M[sand][:4]]
  for yy,xx in ((0,0),(0,8),(8,0),(8,8)):
   a=np.array(chalk.crop((x*16+xx,y*16+yy,x*16+xx+8,y*16+yy+8)),dtype=np.uint8);a[a==1]=whiteidx;ds.append((a.tobytes(),0,whitebank))
  mid=add(ds);idx=(6+y)*l['width']+21+x;assert blocks[idx]&1023==sand;blocks[idx]=(blocks[idx]&~1023)|mid;row.append(mid)
 court.append(row)
# Verify every original placed definition and its referenced pixels still match.
for mid in placed:
 assert M[mid]==oldM[mid] and A[mid]==oldA[mid]
 assert all(T[v&1023]==oldT[v&1023] for v in M[mid])
assert all(T[i]==oldT[i] for i in fixed)
# No other district map data is painted by this migration.
for group,offset,count in [('primary',0,640),('secondary',640,384)]:
 p=R/f'data/tilesets/{group}/havora_city';im=Image.new('P',(128,count//16*8));im.putpalette(Image.open(p/'tiles.png').getpalette())
 for i,b in enumerate(T[offset:offset+count]):im.paste(Image.frombytes('P',(8,8),b),(i%16*8,i//16*8))
 im.save(p/'tiles.png');(p/'metatiles.bin').write_bytes(struct.pack('<'+'H'*(count*8),*[v for m in M[offset:offset+count] for v in m]));(p/'metatile_attributes.bin').write_bytes(struct.pack('<'+'I'*count,*A[offset:offset+count]))
(R/l['blockdata_filepath']).write_bytes(struct.pack('<'+'H'*len(blocks),*blocks))
for kind,mapping in shared['metatile_mapping'].items():shared['metatile_mapping'][kind]={k:v for k,v in mapping.items() if v not in retired}
(R/'tools/havora/shared-tileset.json').write_text(json.dumps(shared,indent=2)+'\n')
extra['building_tiles']=[e for e in extra['building_tiles'] if e['metatile'] not in retired];extra['complete_market_stalls']=stalls;extra['forest_entrance']=forest;(R/'tools/havora/authoring-assets.json').write_text(json.dumps(extra,indent=2)+'\n')
report={'stalls':stalls,'slateport_source_mapping':{str(k):v for k,v in stallmap.items()},'forest_entrance':forest,'forest_collision':[[1,1,1,1],[1,1,1,1],[1,0,0,1]],'forest_note':'Decorative kit; middle two bottom cells are the approach. Attach a destination warp separately when placing a functional entrance.','court':court,'court_origin':[21,6],'white_palette':[whitebank,whiteidx],'new_metatiles':added,'retired_unplaced':sorted(retired),'new_graphics':len(archive['graphics']),'original_placed_verified':len(placed),'protected_metatiles':len(protected),'archive':archive}
OUT.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:report[k] for k in ('new_graphics','retired_unplaced','original_placed_verified','stalls','forest_entrance')}))
