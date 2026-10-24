#!/usr/bin/env python3
"""Import Celadon fountain with independently reserved animation graphics.

Reads Celadon fountain metatiles and its five native frames. Reclaims only
unplaced catalog definitions, archives them, and fits art to shared palettes.
Does not paint maps or change palettes, events or connections. Existing animation
slots remain pinned; the generated fountain frames use six additional slots.
"""
import json,struct,io,subprocess
from pathlib import Path
from collections import defaultdict
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parents[2]
manifest=R/'tools/havora/fountain.json'
if manifest.exists():
 print('Native houses already exist; edit the current tileset in Porymap.')
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
# Retain the requested long house; unplaced obsolete house catalog is reclaimable.
for row in js('tools/havora/native-houses.json')['kits']['cerulean_home']:protected.update(row)
for ids in extra['statue_metatiles'].values():protected.update(ids)
for e in extra['building_tiles']:protected.add(e['metatile'])
for kit in js('tools/havora/green-houses.json')['kits'].values():
 for row in kit:protected.update(row)
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

# Use six safe destinations. Scattered slots preserve all existing graphic
# indices. The callback queues six 32-byte transfers; even a simultaneous
# primary update plus ocean transfer stays below the engine's 20-entry buffer.
slots=sorted((t for t in range(1024) if t not in pinned),key=lambda t:(len(refs[t]),t))[:6]
assert len(slots)==6,'No six safe fountain animation slots'
for t in slots:
 for mid in list(refs[t]):
  assert mid not in protected
  archive['metatiles'][str(mid)]={'words':list(M[mid]),'attribute':A[mid]};retired.add(mid)
  for w in M[mid]:refs[w&1023].discard(mid)
  M[mid]=(0,)*8;A[mid]=0
 archive['graphics'][str(t)]=list(T[t]);key,_=canon(T[t])
 if cache.get(key,(None,None))[0]==t:del cache[key]
fixed.update(slots);pinned.update(slots)
source=R/'data/tilesets/secondary/celadon_city'
srcpal=[tuple(map(int,s.split())) for s in (source/'palettes/08.pal').read_text().splitlines()[3:19]]
frames=[Image.open(source/f'anim/fountain/{i}.png') for i in range(5)]
# Fit one bank consistently across the basin and all animation frames.
sw=words('data/tilesets/secondary/celadon_city/metatiles.bin');sm=[tuple(sw[i:i+8]) for i in range(0,len(sw),8)]
st=[]
for group,folder,count in [('primary','general',640),('secondary','celadon_city',384)]:
 im=Image.open(R/f'data/tilesets/{group}/{folder}/tiles.png');st.extend(im.crop((i%16*8,i//16*8,i%16*8+8,i//16*8+8)).tobytes() for i in range(count))
weight=np.zeros(16,dtype=np.int64)
for mid in range(0x2cd,0x2d9):
 for w in sm[mid-640][4:]:weight+=np.bincount(np.frombuffer(st[w&1023],dtype=np.uint8),minlength=16)
for im in frames:weight+=np.bincount(np.frombuffer(im.tobytes(),dtype=np.uint8),minlength=16)
weight[0]=0;palette=np.array(P,dtype=np.int32);dist=((np.array(srcpal)[:,None,:]-palette[:,None,1:,:])**2).sum(axis=3);errors=(dist.min(axis=2)*weight[None,:]).sum(axis=1);bank=int(errors.argmin());table=(dist[bank].argmin(axis=1)+1).astype('uint8');table[0]=0
outdir=R/'data/tilesets/secondary/havora_city/anim/fountain';outdir.mkdir(parents=True,exist_ok=True)
converted=[]
for i,im in enumerate(frames):
 a=table[np.frombuffer(im.tobytes(),dtype=np.uint8)];frame=Image.frombytes('P',im.size,a.tobytes());frame.putpalette([c for rgb in P[bank] for c in rgb]+[0]*720);frame.save(outdir/f'{i}.png');converted.append(frame)
for i in range(2,8):T[slots[i-2]]=converted[0].crop((i%2*8,i//2*8,i%2*8+8,i//2*8+8)).tobytes()
descriptors={}
for mid in range(0x2cd,0x2d9):
 ds=[]
 for w in sm[mid-640][4:]:
  if 746<=w&1023<752:ds.append(('animated',slots[(w&1023)-746],w&0xc00,bank<<12))
  elif 744<=w&1023<746:
   i=(w&1023)-744;b=converted[0].crop((i*8,0,i*8+8,8)).tobytes();key,f=canon(b);ds.append(('static',key,f^(w&0xc00),bank<<12))
  elif w&1023==0:ds.append(('static',bytes(64),w&0xc00,0))
  else:
   b=table[np.frombuffer(st[w&1023],dtype=np.uint8)].tobytes();key,f=canon(b);ds.append(('static',key,f^(w&0xc00),bank<<12))
 descriptors[mid]=ds
for ds in descriptors.values():
 for kind,key,_,_ in ds:
  if kind=='static' and key in cache:pinned.add(cache[key][0])
ab=(source/'metatile_attributes.bin').read_bytes();srcattrs=struct.unpack('<'+'I'*(len(ab)//4),ab)
kits={}
for label,ground in [('grass',0),('paving',449)]:
 grid=[]
 for row in range(4):
  mids=[]
  for col in range(3):
   srcmid=0x2cd+row*3+col;out=list(M[ground][:4])
   for kind,key,f,pal in descriptors[srcmid]:
    if kind=='animated':out.append(key|f|pal)
    else:
     t,cf=allocate(key);out.append(t|(f^cf)|pal)
   mid=next(i for i,m in enumerate(M) if not any(m) and not A[i] and i not in protected)
   M[mid]=tuple(out);A[mid]=srcattrs[srcmid-640];protected.add(mid);new.append(mid);mids.append(mid)
   for w in out:refs[w&1023].add(mid)
  grid.append(mids)
 kits[label]=grid
for mid in original_protected:
 assert mid not in retired and M[mid]==oldM[mid] and A[mid]==oldA[mid]
 assert all(T[w&1023]==oldT[w&1023] for w in M[mid])
assert all(T[t]==oldT[t] for t in fixed-set(slots))
for group,offset,count in [('primary',0,640),('secondary',640,384)]:
 p=R/f'data/tilesets/{group}/havora_city';im=Image.new('P',(128,count//16*8));im.putpalette(Image.open(p/'tiles.png').getpalette())
 for i,b in enumerate(T[offset:offset+count]):im.paste(Image.frombytes('P',(8,8),b),(i%16*8,i//16*8))
 im.save(p/'tiles.png');(p/'metatiles.bin').write_bytes(struct.pack('<'+'H'*(count*8),*[w for m in M[offset:offset+count] for w in m]));(p/'metatile_attributes.bin').write_bytes(struct.pack('<'+'I'*count,*A[offset:offset+count]))
for key,m in shared['metatile_mapping'].items():shared['metatile_mapping'][key]={k:v for k,v in m.items() if v not in retired}
shared['fountain']='tools/havora/fountain.json';shared['metatiles']=sum(bool(any(m) or a) for m,a in zip(M,A))
(R/'tools/havora/shared-tileset.json').write_text(json.dumps(shared,indent=2)+'\n')
header='/* Generated by tools/havora/add_fountain.py. */\n#define HAVORA_FOUNTAIN_ANIM_TILES 6\n#define HAVORA_FOUNTAIN_FRAME_TILE_OFFSET 2\n'
header+='static const u16 sHavoraFountainTileIds[] = {'+', '.join(map(str,slots))+'};\n'
for i in range(5):header+=f'static const u16 sHavoraFountainFrame{i}[] = INCBIN_U16("data/tilesets/secondary/havora_city/anim/fountain/{i}.4bpp");\n'
header+='static const u16 *const sHavoraFountainFrames[] = {'+', '.join(f'sHavoraFountainFrame{i}' for i in range(5))+'};\n';(R/'src/data/havora_fountain_anim.h').write_text(header)
report={'kits':kits,'source':'CeladonCity fountain 0x2CD-0x2D8','animation_graphic_ids':slots,'animation_tiles':6,'constant_frame_tiles':2,'palette_bank':bank,'frames':5,'ticks_per_frame':12,'combined_cycle_ticks':1920,'placed_metatiles_preserved':len(placed),'protected_catalog_preserved':len(original_protected),'new_metatiles':new,'retired_unplaced_metatiles':sorted(retired),'reclaimed_static_graphics':len(archive['graphics'])-6,'note':'Shared-tileset authoring kit; no map placements, events, warps, palettes or existing animation destinations modified.'}
layout=next(l for l in js('data/layouts/layouts.json')['layouts'] if l['name']=='CeladonCity_Layout');blocks=words(layout['blockdata_filepath']);report['collision_mask']=[[(blocks[(18+y)*layout['width']+12+x]>>10)&3 for x in range(3)] for y in range(4)]
manifest.write_text(json.dumps(report,indent=2)+'\n');(R/'tools/havora/fountain-archive.json').write_text(json.dumps(archive,indent=2)+'\n');print(json.dumps(report,indent=2))
