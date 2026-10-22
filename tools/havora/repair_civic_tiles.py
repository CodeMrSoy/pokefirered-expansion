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
manifest=R/'tools/havora/civic-repair.json'
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
# Unplaced obsolete Lilycove modules may supply the final repair slots.
# Named harbor assets and every placed piece remain pinned.
for kit in js('tools/havora/green-houses.json')['kits'].values():
 for row in kit:protected.update(row)
for grid in js('tools/havora/fountain.json')['kits'].values():
 for row in grid:protected.update(row)
service={v for name in ['center','mart'] for row in js('tools/havora/civic-tiles.json')['assets'][name] for v in row}
protected-=service
original_protected=protected.copy()
fixed=set(range(416,482))|set(range(508,512))|set(range(896,1024))|{0,20}|set(js('tools/havora/fountain.json')['animation_graphic_ids'])
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

# Palette 0 slot 7 was an unused magenta placeholder. No static metatile uses
# it, no General flower frame uses it, and water animations use other banks.
assert not any(7 in T[w&1023] for m in oldM for w in m if w>>12==0)
assert not any(7 in Image.open(p).tobytes() for p in (R/'data/tilesets/primary/general/anim/flower').glob('*.png'))
assert not any(w>>12==0 and 416<=w&1023<482 for m in oldM for w in m)
P[0][7]=(172,32,41)
for mid in service:
 archive['metatiles'][str(mid)]={'words':list(M[mid]),'attribute':A[mid]}
 for w in M[mid]:refs[w&1023].discard(mid)
 M[mid]=(0,)*8;A[mid]=0
# Keep all service metatile IDs stable; only the missing right column needs four
# extra definitions. Source roof texture is retained with separate shade indices.
civic=js('tools/havora/civic-tiles.json');mapping={int(k):v for k,v in civic['native_general_ids'].items()};native=words('data/tilesets/primary/general/metatiles.bin');sm=[tuple(native[i:i+8]) for i in range(0,len(native),8)];im=Image.open(R/'data/tilesets/primary/general/tiles.png');st=[im.crop((i%16*8,i//16*8,i%16*8+8,i//16*8+8)).tobytes() for i in range(640)];sp=[]
for bank in range(13):sp.append([tuple(map(int,l.split())) for l in (R/f'data/tilesets/primary/general/palettes/{bank:02}.pal').read_text().splitlines()[3:19]])
b=(R/'data/tilesets/primary/general/metatile_attributes.bin').read_bytes();sa=struct.unpack('<'+'I'*(len(b)//4),b);l=next(l for l in js('data/layouts/layouts.json')['layouts'] if l['name']=='VermilionCity_Layout');blocks=words(l['blockdata_filepath']);sourcegrids={}
for name,(x,y,w,h) in {'center':(13,3,5,4),'mart':(27,14,4,4)}.items():sourcegrids[name]=[[blocks[(y+j)*l['width']+x+i]&1023 for i in range(w)] for j in range(h)]
descriptors={};pal=np.array(P,dtype=np.int32)
redroof={0xd0,0xd1,0xd2,0xe0,0xf0,0xf1,0xf2,0xf3}
blueroof={0xc0,0xc1,0xc2,0xc3,0xd0,0xd1,0xd2,0xe0,0xf3}
for mid in {v for g in sourcegrids.values() for row in g for v in row}:
 ds=[]
 for w in sm[mid]:
  tid=w&1023;bank=w>>12;a=np.frombuffer(st[tid],dtype=np.uint8);rgb=np.array(sp[bank])[a];dist=((rgb[:,None,None,:]-pal[None,:,1:,:])**2).sum(axis=3);mask=a!=0;errors=dist.min(axis=2)[mask].sum(axis=0);target=int(errors.argmin());idx=(dist[:,target].argmin(axis=1)+1).astype('uint8');idx[~mask]=0
  if bank==2 and tid in redroof:
   target=0;table=(np.sum((np.array(sp[bank])[:,None,:]-pal[target,None,1:,:])**2,axis=2).argmin(axis=1)+1).astype('uint8');table[0]=0
   for src,dst in {10:9,11:10,12:11,13:7,14:7}.items():table[src]=dst
   idx=table[a]
  if bank==3 and tid in blueroof:
   target=6;table=(np.sum((np.array(sp[bank])[:,None,:]-pal[target,None,1:,:])**2,axis=2).argmin(axis=1)+1).astype('uint8');table[0]=0
   for src,dst in {10:2,11:3,12:4,13:5,14:6}.items():table[src]=dst
   idx=table[a]
  if bank==2 and tid in {0x103,0x113}:
   target=1;table=(np.sum((np.array(sp[bank])[:,None,:]-pal[target,None,1:,:])**2,axis=2).argmin(axis=1)+1).astype('uint8');table[0]=0;idx=table[a]
  key,f=canon(idx.tobytes());ds.append((key,f^(w&0xc00),target<<12))
 descriptors[mid]=ds
for ds in descriptors.values():
 for key,_,_ in ds:
  if key in cache:pinned.add(cache[key][0])
for mid,ds in descriptors.items():
 if mid not in mapping:
  target=next(i for i,m in enumerate(M) if not any(m) and not A[i] and i not in protected and i not in service);mapping[mid]=target
 else:target=mapping[mid]
 out=[]
 for key,f,bank in ds:
  t,cf=allocate(key);out.append(t|(f^cf)|bank)
 M[target]=tuple(out);A[target]=oldA[target] if target in service else sa[mid];protected.add(target)
 for w in out:refs[w&1023].add(target)
for mid in original_protected:
 assert M[mid]==oldM[mid] and A[mid]==oldA[mid]
 assert all(T[w&1023]==oldT[w&1023] for w in M[mid])
assert all(T[t]==oldT[t] for t in fixed)
for group,offset,count in [('primary',0,640),('secondary',640,384)]:
 p=R/f'data/tilesets/{group}/havora_city';im=Image.new('P',(128,count//16*8));im.putpalette(Image.open(p/'tiles.png').getpalette())
 for i,b in enumerate(T[offset:offset+count]):im.paste(Image.frombytes('P',(8,8),b),(i%16*8,i//16*8))
 im.save(p/'tiles.png');(p/'metatiles.bin').write_bytes(struct.pack('<'+'H'*(count*8),*[w for m in M[offset:offset+count] for w in m]));(p/'metatile_attributes.bin').write_bytes(struct.pack('<'+'I'*count,*A[offset:offset+count]))
 # Only unused palette entry 0:7 changes; all established color entries retain values.
 pp=p/'palettes/00.pal';lines=pp.read_text().splitlines();lines[3+7]='172 32 41';pp.write_text('\n'.join(lines)+'\n')
for name,grid in sourcegrids.items():civic['assets'][name]=[[mapping[v] for v in row] for row in grid]
civic['native_general_ids']={str(k):v for k,v in mapping.items()};civic['repair_note']='Full five-column Center; native roof texture restored. Shared palette0 unused slot7 supplies dark red.';(R/'tools/havora/civic-tiles.json').write_text(json.dumps(civic,indent=2)+'\n')
for kind,m in shared['metatile_mapping'].items():shared['metatile_mapping'][kind]={k:v for k,v in m.items() if v not in retired}
(R/'tools/havora/shared-tileset.json').write_text(json.dumps(shared,indent=2)+'\n')
extra['building_tiles']=[e for e in extra['building_tiles'] if e['metatile'] not in retired]
extra['new_metatiles']=[i for i in extra['new_metatiles'] if i not in retired]
(R/'tools/havora/authoring-assets.json').write_text(json.dumps(extra,indent=2)+'\n')
manifest.write_text(json.dumps({'assets':{n:civic['assets'][n] for n in sourcegrids},'protected_metatiles_preserved':len(original_protected),'palette0_slot7_previously_unused':True,'retired_unplaced':sorted(retired)},indent=2)+'\n');(R/'tools/havora/civic-repair-archive.json').write_text(json.dumps(archive,indent=2)+'\n')
print('Complete Center/Mart designs imported with roof shade contrast.')
