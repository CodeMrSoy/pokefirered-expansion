#!/usr/bin/env python3
"""Create complete roof/frontage variants without modifying placed map tiles.

One-time authoring migration. Reclaims only unplaced, unprotected definitions;
archives every retired definition and overwritten graphic. Does not paint maps.
"""
import json,struct,io,colorsys
from pathlib import Path
from collections import defaultdict
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parents[2]
manifest=R/'tools/havora/house-variants.json'
if manifest.exists():
 print('House variants already exist; edit the current tileset in Porymap.')
 raise SystemExit(0)
def js(p):return json.loads((R/p).read_text())
def words(p):
 b=(R/p).read_bytes();return list(struct.unpack('<'+'H'*(len(b)//2),b))
def flip(b,f):
 a=Image.frombytes('P',(8,8),b)
 if f&1024:a=a.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
 if f&2048:a=a.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
 return a.tobytes()
def canon(b):return min((flip(b,f),f) for f in [0,1024,2048,3072])
T=[];M=[];A=[];P=[]
for group in ['primary','secondary']:
 p=f'data/tilesets/{group}/havora_city';im=Image.open(R/p/'tiles.png')
 T += [im.crop((x,y,x+8,y+8)).tobytes() for y in range(0,im.height,8) for x in range(0,128,8)]
 w=words(p+'/metatiles.bin');M += [tuple(w[i:i+8]) for i in range(0,len(w),8)]
 b=(R/p/'metatile_attributes.bin').read_bytes();A+=list(struct.unpack('<'+'I'*(len(b)//4),b))
for i in range(13):
 p=R/f'data/tilesets/{"primary" if i<7 else "secondary"}/havora_city/palettes/{i:02}.pal'
 P.append([tuple(map(int,l.split())) for l in p.read_text().splitlines()[3:19]])
oldT=T[:];oldM=M[:];oldA=A[:]
shared=js('tools/havora/shared-tileset.json');old=js('tools/havora/assets.json');extra=js('tools/havora/authoring-assets.json');mp={int(k):v for k,v in shared['metatile_mapping']['harbor'].items()}
base=[[mp[x] for x in row] for row in old['assets']['house']['metatiles']]
placed=set()
for l in js('data/layouts/layouts.json')['layouts']:
 if l['primary_tileset']=='gTileset_HavoraCityPrimary':
  for field in ['blockdata_filepath','border_filepath']:placed.update(v&1023 for v in words(l[field]))
protected=placed|set(js('tools/havora/city-tileset.json')['native_general_ids'].values())|set(range(168,172))
for grid in js('tools/havora/civic-tiles.json')['assets'].values():
 for row in grid:protected.update(row)
for grid in old['assets'].values():
 for row in grid['metatiles']:protected.update(mp[x] for x in row if x in mp)
for e in old['catalog']:
 if (e['town']=='pacifidlog' or 'market' in e['group'].lower()) and e['havora_id'] in mp:protected.add(mp[e['havora_id']])
for e in extra['building_tiles']:protected.add(e['metatile'])
for ids in extra['statue_metatiles'].values():protected.update(ids)
original_protected=protected.copy()
fixed=set(range(416,482))|set(range(508,512))|set(range(896,1024))|{0,20}
pinned=fixed|{w&1023 for mid in protected for w in M[mid]};refs=defaultdict(set);cache={}
for mid,m in enumerate(M):
 if any(m) or A[mid]:
  for w in m:refs[w&1023].add(mid)
for t,b in enumerate(T):
 if t not in fixed or t in (0,20):
  key,f=canon(b);cache.setdefault(key,(t,f))
archive={'metatiles':{},'graphics':{}};retired=set();new=[]
def allocate(key):
 if key in cache:
  t,f=cache[key];pinned.add(t);return t,f
 candidates=[t for t in range(1024) if t not in pinned];assert candidates,'No safe graphic slot available'
 t=min(candidates,key=lambda t:(len(refs[t]),t))
 for mid in list(refs[t]):
  assert mid not in protected
  archive['metatiles'][str(mid)]={'words':list(M[mid]),'attribute':A[mid]};retired.add(mid)
  for w in M[mid]:refs[w&1023].discard(mid)
  M[mid]=(0,)*8;A[mid]=0
 archive['graphics'][str(t)]=list(T[t]);oldkey,_=canon(T[t])
 if cache.get(oldkey,(None,None))[0]==t:del cache[oldkey]
 T[t]=key;cache[key]=(t,0);pinned.add(t);return t,0
source=Image.open(R/'tools/havora/source_art/emerald_harbor/house.png').convert('RGBA')
palette=np.array(P,dtype=np.int32)
def recolor(mid,col,row,hue):
 descriptors=[]
 for k,w in enumerate(oldM[mid]):
  b=flip(oldT[w&1023],w&0xc00);a=np.frombuffer(b,dtype=np.uint8).reshape(8,8);rgb=palette[w>>12][a].copy();mask=a!=0;changed=False
  for y in range(8):
   for x in range(8):
    sx=col*16+(k%2)*8+x;sy=row*16+(k%4//2)*8+y;r,g,bl,alpha=source.getpixel((sx,sy))
    if alpha and bl>r+12 and bl>g+8 and mask[y,x]:
     _,light,_=colorsys.rgb_to_hls(*[v/255 for v in rgb[y,x]])
     rgb[y,x]=[int(v*255) for v in colorsys.hls_to_rgb(hue,light,0.62)];changed=True
  if not changed:
   key,f=canon(bytes(a.flatten()));descriptors.append((key,f,(w>>12)<<12));continue
  best=None
  for bank,pal in enumerate(palette):
   dist=((rgb[:,:,None,:]-pal[None,None,1:,:])**2).sum(axis=3);idx=dist.argmin(axis=2)+1
   error=int(dist.min(axis=2)[mask].sum());idx=np.where(mask,idx,0).astype('uint8')
   if best is None or error<best[0]:best=(error,bank,idx.tobytes())
  _,bank,b=best;key,f=canon(b);descriptors.append((key,f,bank<<12))
 for key,_,_ in descriptors:
  if key in cache:pinned.add(cache[key][0])
 out=[]
 for key,f,bank in descriptors:
  t,cf=allocate(key);out.append(t|bank|(f^cf))
 for mid,m in enumerate(M):
  if tuple(out)==m and A[mid]==oldA[base[row][col]]:protected.add(mid);return mid
 mid=next(i for i,m in enumerate(M) if not any(m) and not A[i] and i not in protected)
 M[mid]=tuple(out);A[mid]=oldA[base[row][col]];protected.add(mid);new.append(mid)
 for w in out:refs[w&1023].add(mid)
 return mid
kits={}
for name,hue in [('brick_red',0.015),('coastal_teal',0.46)]:
 grid=[r[:] for r in base]
 for y in range(2):
  for x in range(4):grid[y][x]=recolor(base[y][x],x,y,hue)
 kits[name+'_house']=grid
 kits[name+'_cottage']=[[r[x] for x in [0,1,3]] for r in grid]
# Snapshot equality includes source graphic indices/flip/material usage for all
# protected meta definitions. Reclaimed slots can never be referenced by them.
for mid in original_protected:
 assert mid not in retired and M[mid]==oldM[mid] and A[mid]==oldA[mid]
 assert all(T[w&1023]==oldT[w&1023] for w in M[mid])
assert all(T[t]==oldT[t] for t in fixed)
for group,start,count in [('primary',0,640),('secondary',640,384)]:
 p=R/f'data/tilesets/{group}/havora_city';im=Image.new('P',(128,count//16*8));im.putpalette(Image.open(p/'tiles.png').getpalette())
 for i,b in enumerate(T[start:start+count]):im.paste(Image.frombytes('P',(8,8),b),(i%16*8,i//16*8))
 im.save(p/'tiles.png');(p/'metatiles.bin').write_bytes(struct.pack('<'+'H'*(count*8),*[w for m in M[start:start+count] for w in m]));(p/'metatile_attributes.bin').write_bytes(struct.pack('<'+'I'*count,*A[start:start+count]))
for key,m in shared['metatile_mapping'].items():shared['metatile_mapping'][key]={k:v for k,v in m.items() if v not in retired}
shared['house_variants']='tools/havora/house-variants.json';shared['metatiles']=sum(bool(any(m) or a) for m,a in zip(M,A))
(R/'tools/havora/shared-tileset.json').write_text(json.dumps(shared,indent=2)+'\n')
report={'kits':kits,'new_metatiles':new,'retired_unplaced_metatiles':sorted(retired),'reclaimed_graphics':len(archive['graphics']),'placed_metatiles_preserved':len(placed),'protected_catalog_preserved':len(original_protected),'animation_slots_preserved':True,'palette_changes':False,'note':'Roof colors use existing material banks. The narrow cottages reuse the door frontage and outer wall; all lower wall modules are existing tiles.'}
manifest.write_text(json.dumps(report,indent=2)+'\n');(R/'tools/havora/house-variants-archive.json').write_text(json.dumps(archive,indent=2)+'\n');print(json.dumps(report,indent=2))
