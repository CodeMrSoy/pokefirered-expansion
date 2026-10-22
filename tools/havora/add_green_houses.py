#!/usr/bin/env python3
"""One-time import of the selected Viridian homes and Celadon store.

Reads source metatile grids from ViridianCity and CeladonCity. Reclaims only
unplaced catalog definitions, archives them, and fits art to shared palettes.
Does not paint maps or change palette files, animations, events or connections.
"""
import json,struct,io,subprocess
from pathlib import Path
from collections import defaultdict
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parents[2]
manifest=R/'tools/havora/green-houses.json'
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

# Extract complete, distinct designs from the original FireRed maps.
# Preserve native geometry, layered quadrants and the full behavior/layer u32.
sources=[('viridian_garden','ViridianCity','viridian_city',(24,15,5,5)),('viridian_home','ViridianCity','viridian_city',(24,8,5,4)),('celadon_department_store','CeladonCity','celadon_city',(9,5,9,10))]
kits={};source_grids={};palette=np.array(P,dtype=np.int32);mapping_report={}
for name,town,sec,(x,y,width,height) in sources:
 l=next(l for l in js('data/layouts/layouts.json')['layouts'] if l['name']==town+'_Layout')
 blocks=words(l['blockdata_filepath']);grid=[[blocks[(y+j)*l['width']+x+i]&1023 for i in range(width)] for j in range(height)]
 st=[];sm=[];sa=[];sp=[]
 for group,folder,count in [('primary','general',640),('secondary',sec,384)]:
  p=R/f'data/tilesets/{group}/{folder}';im=Image.open(p/'tiles.png')
  st += [im.crop((i%16*8,i//16*8,i%16*8+8,i//16*8+8)).tobytes() for i in range(count)]
  w=words(str(p.relative_to(R))+'/metatiles.bin');sm += [tuple(w[i:i+8]) for i in range(0,len(w),8)];sm += [(0,)*8]*(640-len(sm)) if group=='primary' else []
  b=(p/'metatile_attributes.bin').read_bytes();sa+=list(struct.unpack('<'+'I'*(len(b)//4),b));sa += [0]*(640-len(sa)) if group=='primary' else []
 for b in range(13):
  p=R/f'data/tilesets/{"primary/general" if b<7 else "secondary/"+sec}/palettes/{b:02}.pal'
  sp.append([tuple(map(int,s.split())) for s in p.read_text().splitlines()[3:19]])
 # Choose a consistent closest shared bank per source bank, rather than allowing
 # adjacent pieces of the same roof to drift in color. No palette is edited.
 weights=defaultdict(lambda:np.zeros(16,dtype=np.int64))
 for mid in {m for row in grid for m in row}:
  for w in sm[mid]:weights[w>>12]+=np.bincount(np.frombuffer(st[w&1023],dtype=np.uint8),minlength=16)
 conversions={}
 for bank,weight in weights.items():
  weight[0]=0
  dist=((np.array(sp[bank])[:,None,:]-palette[:,None,1:,:])**2).sum(axis=3)
  errors=(dist.min(axis=2)*weight[None,:]).sum(axis=1);target=int(errors.argmin())
  # Keep the complete facade in one compatible material bank.
  target={10:10,11:9}.get(bank,target) if name.startswith('viridian') else target
  table=dist[target].argmin(axis=1)+1;table[0]=0
  conversions[bank]=(target,table.astype(np.uint8));mapping_report[name+':'+str(bank)]=target
 descriptors={}
 for mid in {m for row in grid for m in row}:
  ds=[]
  for quadrant,w in enumerate(sm[mid]):
   if quadrant<4 and (name.startswith('viridian') and mid in set(range(0x280,0x285))|set(range(0x2a8,0x2ad))):
    # Roof-edge ground must match the city grass, rather than source-town sand.
    native=M[js('tools/havora/city-tileset.json')['native_general_ids']['1']][quadrant]
    key,f=canon(T[native&1023]);ds.append((key,f^(native&0xc00),native&0xf000));continue
   bank,table=conversions[w>>12]
   if name.startswith('viridian') and w>>12==11 and (w&1023) in {0x204,0x205,0x206,0x214,0x215,0x216,0x224,0x225,0x226,0x234,0x235,0x236}:
    bank=0;dist=((np.array(sp[11])[:,None,:]-palette[bank,None,1:,:])**2).sum(axis=2);table=(dist.argmin(axis=1)+1).astype(np.uint8);table[0]=0
    for source_index,target_index in {10:1,11:2,12:2,13:3,14:4,5:5,6:6,7:6}.items():table[source_index]=target_index
   b=table[np.frombuffer(st[w&1023],dtype=np.uint8)].tobytes();key,f=canon(b);ds.append((key,f^(w&0xc00),bank<<12))
  descriptors[mid]=ds
 # Pin all reusable matches before allocating any missing graphics.
 for ds in descriptors.values():
  for key,_,_ in ds:
   if key in cache:pinned.add(cache[key][0])
 remap={}
 for mid,ds in descriptors.items():
  out=[]
  for key,f,bank in ds:
   t,cf=allocate(key);out.append(t|bank|(f^cf))
  match=next((i for i,m in enumerate(M) if m==tuple(out) and A[i]==sa[mid]),None)
  if match is None:
   match=next(i for i,m in enumerate(M) if not any(m) and not A[i] and i not in protected)
   M[match]=tuple(out);A[match]=sa[mid];new.append(match)
  protected.add(match);remap[mid]=match
  for w in out:refs[w&1023].add(match)
 kits[name]=[[remap[m] for m in row] for row in grid];source_grids[name]={'map':town,'rectangle':[x,y,width,height],'metatiles':grid}
for mid in original_protected:
 assert mid not in retired and M[mid]==oldM[mid] and A[mid]==oldA[mid]
 assert all(T[w&1023]==oldT[w&1023] for w in M[mid])
assert all(T[t]==oldT[t] for t in fixed)
for group,start,count in [('primary',0,640),('secondary',640,384)]:
 p=R/f'data/tilesets/{group}/havora_city';im=Image.new('P',(128,count//16*8));im.putpalette(Image.open(p/'tiles.png').getpalette())
 for i,b in enumerate(T[start:start+count]):im.paste(Image.frombytes('P',(8,8),b),(i%16*8,i//16*8))
 im.save(p/'tiles.png');(p/'metatiles.bin').write_bytes(struct.pack('<'+'H'*(count*8),*[w for m in M[start:start+count] for w in m]));(p/'metatile_attributes.bin').write_bytes(struct.pack('<'+'I'*count,*A[start:start+count]))
for key,m in shared['metatile_mapping'].items():shared['metatile_mapping'][key]={k:v for k,v in m.items() if v not in retired}
shared['green_houses']='tools/havora/green-houses.json';shared['metatiles']=sum(bool(any(m) or a) for m,a in zip(M,A))
(R/'tools/havora/shared-tileset.json').write_text(json.dumps(shared,indent=2)+'\n')
report={'kits':kits,'sources':source_grids,'new_metatiles':new,'retired_unplaced_metatiles':sorted(retired),'reclaimed_graphics':len(archive['graphics']),'placed_metatiles_preserved':len(placed),'protected_catalog_preserved':len(original_protected),'animation_slots_preserved':True,'palette_changes':False,'palette_bank_mapping':mapping_report,'note':'Original FireRed house designs, fitted to the existing shared palette. No map placement, collision, event, connection or border changes.'}
manifest.write_text(json.dumps(report,indent=2)+'\n');(R/'tools/havora/green-houses-archive.json').write_text(json.dumps(archive,indent=2)+'\n');print(json.dumps(report,indent=2))
