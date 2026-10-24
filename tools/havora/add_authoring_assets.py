#!/usr/bin/env python3
"""Add authoring pieces, reclaiming only unplaced, unprotected catalog graphics.

This one-time migration reads the reviewed source tree. --apply refuses newer
edits. All placed map metatiles, native terrain, civic buildings, wood/docks,
named Harbor assets, animation destinations and engine fixed tiles are pinned.
"""
import argparse,io,json,struct,subprocess
from collections import defaultdict
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[2]
BASE='0673644fe7c6dd3a4d4634b9c79a96a11edc556f'
def read(p):return subprocess.check_output(['git','show',f'{BASE}:{p}'],cwd=R)
def load(p):return json.loads(read(p))
def ww(b):return list(struct.unpack('<'+'H'*(len(b)//2),b))
def flip(b,f):
 im=Image.frombytes('P',(8,8),b)
 if f&0x400:im=im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
 if f&0x800:im=im.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
 return im.tobytes()
def canon(b):return min((flip(b,f),f) for f in (0,0x400,0x800,0xc00))
def pair(kind):
 tiles=[];meta=[];attrs=[];pals=[]
 for g in ('primary','secondary'):
  p=f'data/tilesets/{g}/havora_{kind}'
  im=Image.open(io.BytesIO(read(p+'/tiles.png')))
  tiles += [im.crop((x,y,x+8,y+8)).tobytes() for y in range(0,im.height,8) for x in range(0,128,8)]
  w=ww(read(p+'/metatiles.bin'));meta += [tuple(w[i:i+8]) for i in range(0,len(w),8)]
  b=read(p+'/metatile_attributes.bin');attrs+=list(struct.unpack('<'+'I'*(len(b)//4),b))
 for i in range(13):
  p=f'data/tilesets/{"primary" if i<7 else "secondary"}/havora_{kind}/palettes/{i:02}.pal'
  pals.append([tuple(map(int,s.split())) for s in read(p).decode().splitlines()[3:19]])
 return tiles,meta,attrs,pals
T,M,A,P=pair('city');oldT=T[:];oldM=M[:];oldA=A[:]
HT,HM,HA,HP=pair('harbor')
shared=load('tools/havora/shared-tileset.json');harbor=load('tools/havora/assets.json')
hmap={int(k):v for k,v in shared['metatile_mapping']['harbor'].items()}
layouts=load('data/layouts/layouts.json')['layouts'];placed=set()
for l in layouts:
 if l['primary_tileset']=='gTileset_HavoraCityPrimary':
  for field in ('blockdata_filepath','border_filepath'):placed.update(w&1023 for w in ww(read(l[field])))
terrain=load('tools/havora/city-tileset.json')['native_general_ids']
protected=placed|set(terrain.values())|set(range(168,172))
for grid in load('tools/havora/civic-tiles.json')['assets'].values():
 for row in grid:protected.update(row)
for asset in harbor['assets'].values():
 for row in asset['metatiles']:protected.update(hmap[i] for i in row if i in hmap)
for e in harbor['catalog']:
 if e['town']=='pacifidlog' and e['havora_id'] in hmap:protected.add(hmap[e['havora_id']])
# Restore complete basic Lilycove facade/roof families (native source IDs 0x200-
# 0x28F); supplemental entries include the missing wall/window/roof connectors.
building_entries=[e for e in harbor['catalog'] if e['town']=='lilycove' and 57<=e['index']<=140]
for e in building_entries:
 if e['havora_id'] in hmap:protected.add(hmap[e['havora_id']])
# Keep every current Slateport market/umbrella catalog piece available.
market_entries=[e for e in harbor['catalog'] if 'market' in e['group'].lower()]
for e in market_entries:
 if e['havora_id'] in hmap:protected.add(hmap[e['havora_id']])
original_protected=protected.copy()
fixed=set(range(416,482))|set(range(508,512))|set(range(896,1024))|{0,20}
refs=defaultdict(set)
for mid,m in enumerate(M):
 if any(m) or A[mid]:
  for w in m:refs[w&1023].add(mid)
pinned=fixed|{w&1023 for mid in protected for w in M[mid]}
cache={}
for t,b in enumerate(T):
 if t not in fixed:
  key,f=canon(b);cache.setdefault(key,(t,f))
for t in (0,20):
 key,f=canon(T[t]);cache.setdefault(key,(t,f))
archive={'metatiles':{},'graphics':{}}
retired=set();added=[]

def retire(mid):
 assert mid not in protected
 if mid in retired:return
 archive['metatiles'][str(mid)]={'words':list(M[mid]),'attribute':A[mid]}
 for w in M[mid]:refs[w&1023].discard(mid)
 M[mid]=(0,)*8;A[mid]=0;retired.add(mid)

def allocate(key):
 if key in cache:
  t,f=cache[key];pinned.add(t);return t,f
 candidates=[t for t in range(1024) if t not in pinned]
 assert candidates,'No graphics can be reclaimed without changing protected art'
 t=min(candidates,key=lambda t:(len(refs[t]-retired),len(refs[t]),t))
 for mid in list(refs[t]):retire(mid)
 archive['graphics'][str(t)]=list(T[t])
 oldkey,_=canon(T[t])
 if cache.get(oldkey,(None,None))[0]==t:del cache[oldkey]
 T[t]=key;cache[key]=(t,0);pinned.add(t);return t,0

def import_meta(words,attr,source_tiles,source_pals):
 ds=[]
 for word in words:
  b=source_tiles[word&1023];bank=word>>12
  if source_pals[bank]!=P[bank]:
   table={0:0}
   for v in set(b)-{0}:table[v]=next(i for i in range(1,16) if source_pals[bank][v]==P[bank][i])
   b=bytes(table[v] for v in b)
  key,f=canon(b);ds.append((key,f,word&0xfc00))
 # Pin every existing match before allocating missing graphics.
 for key,_,_ in ds:
  if key in cache:pinned.add(cache[key][0])
 out=[]
 for key,f,flags in ds:
  t,cf=allocate(key);out.append(t|(flags^f^cf))
 for i,m in enumerate(M):
  if tuple(out)==m and A[i]==attr:protected.add(i);return i
 mid=next(i for i,m in enumerate(M) if not any(m) and not A[i] and i not in protected)
 M[mid]=tuple(out);A[mid]=attr;protected.add(mid);added.append(mid)
 for word in out:refs[word&1023].add(mid)
 return mid

# Stock FireRed gym Pokémon sculpture: transparent statue overlay only, with
# the current outdoor paving or grass underneath. Fit its six material colors
# to the existing gray/stone banks; no palette or placed graphic is changed.
p='data/tilesets/primary/building'
gym=ww(read('data/tilesets/secondary/pewter_gym/metatiles.bin'))
sm=gym[(0x2af-640)*8+4:(0x2af-640)*8+8]+gym[(0x2b2-640)*8+4:(0x2b2-640)*8+8]
im=Image.open(io.BytesIO(read(p+'/tiles.png')))
sp=[tuple(map(int,s.split())) for s in read(p+'/palettes/00.pal').decode().splitlines()[3:19]]
statue_tiles=[];statue_words=[];errors=[]
for word in sm:
 t=word&1023;b=im.crop((t%16*8,t//16*8,t%16*8+8,t//16*8+8)).tobytes()
 best=None
 for bank,pal in enumerate(P):
  table={0:0};error=0
  for v in set(b)-{0}:
   idx=min(range(1,16),key=lambda i:sum(((sp[v][c]>>3)-(pal[i][c]>>3))**2 for c in range(3)))
   table[v]=idx;error+=b.count(v)*sum(((sp[v][c]>>3)-(pal[idx][c]>>3))**2 for c in range(3))
  choice=(error,bank,bytes(table[v] for v in b))
  if best is None or choice[:2]<best[:2]:best=choice
 error,bank,b=best;errors.append(error);idx=len(statue_tiles);statue_tiles.append(b);statue_words.append(idx|(word&0xc00)|(bank<<12))
# Import overlay graphics separately, preserving their assigned material banks.
overlay=[]
for i,b in enumerate(statue_tiles):
 key,f=canon(b)
 if key in cache:pinned.add(cache[key][0])
for i,b in enumerate(statue_tiles):
 key,f=canon(b);t,cf=allocate(key)
 # The converted source word keeps its material palette in bits 12-15.
 overlay.append(t | (statue_words[i]&0xf000) | ((sm[i]&0xc00)^f^cf))
statues={}
for label,base in [('paving',0x280),('grass',0)]:
 statues[label]=[]
 for part in range(2):
  mid=next(i for i,m in enumerate(M) if not any(m) and not A[i] and i not in protected)
  M[mid]=tuple(M[base][:4])+tuple(overlay[part*4:part*4+4]);A[mid]=0x20000000;protected.add(mid);added.append(mid)
  for v in M[mid]:refs[v&1023].add(mid)
  statues[label].append(mid)
buildings=[]
for e in building_entries:
 old=e['havora_id']
 dest=hmap[old] if old in hmap else import_meta(HM[old],HA[old],HT,HP)
 buildings.append(dict(source_id=e['source_id'],metatile=dest,catalog_index=e['index']))
# Verify every placed metatile at every ocean frame. Animation graphic slots
# are pinned, so all other callback frames also keep identical source indices.
def pixels(tiles,m,frame=None,palette=None):
 if palette is None:palette=P
 out=[]
 for y in range(16):
  for x in range(16):
   q=y//8*2+x//8;color=None
   for k in (q,q+4):
    word=m[k];t=word&1023;b=tiles[t] if frame is None or t<896 else frame[t-896]
    idx=flip(b,word&0xc00)[y%8*8+x%8]
    if idx or k<4:color=palette[word>>12][idx]
   out.append(color)
 return out
frames=[None]
for f in range(8):
 im=Image.open(io.BytesIO(read(f'data/tilesets/secondary/havora_harbor/anim/water/{f}.png')))
 frames.append([im.crop((x,y,x+8,y+8)).tobytes() for y in range(0,im.height,8) for x in range(0,128,8)])
for mid in placed:
 assert A[mid]==oldA[mid]
 for frame in frames:assert pixels(T,M[mid],frame)==pixels(oldT,oldM[mid],frame),mid
assert all(T[t]==oldT[t] for t in fixed)
for source,target in zip(building_entries,buildings):
 assert A[target['metatile']]==HA[source['havora_id']]
 assert pixels(T,M[target['metatile']])==pixels(HT,HM[source['havora_id']],palette=HP)

# Also preserve every protected unplaced catalog piece, including native cliffs.
for mid in original_protected:
 assert mid not in retired
 assert A[mid]==oldA[mid]
 assert pixels(T,M[mid])==pixels(oldT,oldM[mid]), ('Protected catalog changed',mid)
outputs={}
for group,start,count in [('primary',0,640),('secondary',640,384)]:
 p=f'data/tilesets/{group}/havora_city';im=Image.new('P',(128,count//16*8));im.putpalette(Image.open(io.BytesIO(read(p+'/tiles.png'))).getpalette())
 for i,b in enumerate(T[start:start+count]):im.paste(Image.frombytes('P',(8,8),b),(i%16*8,i//16*8))
 buf=io.BytesIO();im.save(buf,format='PNG');outputs[p+'/tiles.png']=buf.getvalue()
 outputs[p+'/metatiles.bin']=struct.pack('<'+'H'*(count*8),*[v for m in M[start:start+count] for v in m])
 outputs[p+'/metatile_attributes.bin']=struct.pack('<'+'I'*count,*A[start:start+count])
market={name:[[hmap[v] for v in row] for row in a['metatiles']] for name,a in harbor['assets'].items() if name=='market_stall'}
report={'source_commit':BASE,'statue_metatiles':statues,'building_tiles':buildings,'market_stall':market['market_stall'],
 'new_metatiles':added,'retired_unplaced_metatiles':sorted(retired),'reclaimed_graphics':len(archive['graphics']),
 'placed_metatiles_verified':len(placed),'water_frames_verified':8,'palette_changes':False,
 'note':'No map, collision, elevation, event, warp or connection data changed. Statue uses the stock FireRed gym silhouette with current outdoor stone colors.'}
outputs['tools/havora/authoring-assets.json']=(json.dumps(report,indent=2)+'\n').encode()
outputs['tools/havora/authoring-assets-archive.json']=(json.dumps(archive,indent=2)+'\n').encode()
for kind,mp in shared['metatile_mapping'].items():shared['metatile_mapping'][kind]={k:v for k,v in mp.items() if v not in retired}
for source,target in zip(building_entries,buildings):
 shared['metatile_mapping']['harbor'][str(source['havora_id'])]=target['metatile']
shared['omitted_unplaced_harbor']=[v for v in shared['omitted_unplaced_harbor'] if str(v) not in shared['metatile_mapping']['harbor']]
shared['metatiles']=sum(bool(any(m) or a) for m,a in zip(M,A))
shared['retained_city']=len(shared['metatile_mapping']['city'])
shared['retained_harbor']=len(shared['metatile_mapping']['harbor'])
shared['authoring_expansion']={'manifest':'tools/havora/authoring-assets.json','retired_unplaced_metatiles':sorted(retired)}
outputs['tools/havora/shared-tileset.json']=(json.dumps(shared,indent=2)+'\n').encode()
args=argparse.ArgumentParser(description=__doc__);args.add_argument('--apply',action='store_true');args.add_argument('--check',action='store_true');args=args.parse_args()
if args.check:
 for p,b in outputs.items():assert (R/p).read_bytes()==b,p
if args.apply:
 for p,b in outputs.items():
  if p.endswith(('authoring-assets.json','authoring-assets-archive.json')):continue
  assert (R/p).read_bytes() in [read(p),b],('Newer edit found',p)
 for p,b in outputs.items():(R/p).write_bytes(b)
print(json.dumps({k:v for k,v in report.items() if k!='building_tiles'},indent=2));print('Building tiles available:',len(buildings))
