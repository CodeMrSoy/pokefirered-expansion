#!/usr/bin/env python3
"""Reproduce the shared Havora pair from the pre-merge tree; assert visual parity.

Run without arguments for a dry run, or --apply to write. Source assets are read
from Git, so repeated runs never remap an already migrated map. City metatile IDs
stay fixed. Harbor IDs are translated, preserving block collision/elevation bits.
"""
import argparse, io, json, struct, subprocess
from pathlib import Path
from PIL import Image
R=Path(__file__).resolve().parents[2]
BASE='1e49f05b8e46803773587e4d03f212c403063fc6'
def read(p): return subprocess.check_output(['git','show',f'{BASE}:{p}'],cwd=R)
def js(p): return json.loads(read(p))
def words(b): return list(struct.unpack('<'+'H'*(len(b)//2),b))
def packed(w): return struct.pack('<'+'H'*len(w),*w)
def flip(b,f):
 im=Image.frombytes('P',(8,8),b)
 if f&0x400: im=im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
 if f&0x800: im=im.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
 return im.tobytes()
def canonical(b): return min((flip(b,f),f) for f in (0,0x400,0x800,0xc00))
layouts=js('data/layouts/layouts.json');assets=js('tools/havora/assets.json')
sets={}
for kind in ('city','harbor'):
 paths=[f'data/tilesets/{g}/havora_{kind}' for g in ('primary','secondary')]
 tiles=[];meta=[];attrs=[];pals=[]
 for p in paths:
  im=Image.open(io.BytesIO(read(p+'/tiles.png')))
  tiles += [im.crop((x,y,x+8,y+8)).tobytes() for y in range(0,im.height,8) for x in range(0,im.width,8)]
  ww=words(read(p+'/metatiles.bin'));meta += [tuple(ww[i:i+8]) for i in range(0,len(ww),8)]
  b=read(p+'/metatile_attributes.bin');attrs+=list(struct.unpack('<'+'I'*(len(b)//4),b))
 for i in range(13):pals.append([tuple(map(int,s.split())) for s in read(paths[i>=7]+f'/palettes/{i:02}.pal').decode().splitlines()[3:19]])
 used=set()
 for l in layouts['layouts']:
  if l['primary_tileset']==('gTileset_HavoraCityPrimary' if kind=='city' else 'gTileset_HavoraPrimary'):
   for field in ('blockdata_filepath','border_filepath'):used.update(w&1023 for w in words(read(l[field])))
 sets[kind]=dict(tiles=tiles,meta=meta,attrs=attrs,pals=pals,used=used)
city=sets['city'];harbor=sets['harbor'];pals=city['pals']
# Fixed VRAM destinations overwritten by existing callbacks must never be packed.
animated=set(range(416,482))|set(range(508,512))|set(range(896,1024))
fixed=animated|{0,20}  # field_camera.c uses transparent tile 0 and backdrop tile 20.
outtiles=[bytes(64) for _ in range(1024)]
for i in fixed:
 if i in animated:assert city['tiles'][i]==harbor['tiles'][i],('animation initial frame differs',i)
 outtiles[i]=city['tiles'][i]
free=[i for i in range(1024) if i not in fixed];cache={};cursor=0
for i in (0,20):
 key,f=canonical(outtiles[i])
 if f==0:cache[key]=i
assert outtiles[0]==bytes(64)
outmeta=[(0,)*8 for _ in range(1024)];outattrs=[0]*1024;occupied=set();mapping={'city':{},'harbor':{}}
# Earlier four unplaced mirrored-ledge prototypes have invalid packed attributes.
# Exclude those prototypes; never touch a placed map cell to do so.
bad={'city':set(range(168,172)),'harbor':set(range(145,149))}
for k in sets:assert not bad[k]&sets[k]['used']
def descriptors(kind,mid):
 s=sets[kind];result=[]
 for w in s['meta'][mid]:
  t=w&1023;bank=w>>12;b=s['tiles'][t]
  # Exact palette conversion, keeping transparent index zero distinct.
  if s['pals'][bank]!=pals[bank]:
   table={0:0}
   for v in set(b)-{0}:
    table[v]=next(i for i in range(1,16) if pals[bank][i]==s['pals'][bank][v])
   b=bytes(table[v] for v in b)
  if t in animated:
   assert b==s['tiles'][t]
   result.append(('anim',t,w&0xfc00))
  else:
   key,f=canonical(b);result.append(('static',key,(w&0xfc00)^f))
 return result

def add(kind,mid,fixed=False):
 global cursor
 ds=descriptors(kind,mid)
 needed={d[1] for d in ds if d[0]=='static' and d[1] not in cache}
 if cursor+len(needed)>len(free):return False
 for key in sorted(needed):
  t=free[cursor];cursor+=1;cache[key]=t;outtiles[t]=key
 m=tuple((d[1] if d[0]=='anim' else cache[d[1]])|d[2] for d in ds)
 a=sets[kind]['attrs'][mid]
 if fixed:dest=mid
 else:
  dest=next((i for i in sorted(occupied) if outmeta[i]==m and outattrs[i]==a),None)
  if dest is None:dest=next(i for i in range(1024) if i not in occupied and i not in bad['city'])
 outmeta[dest]=m;outattrs[dest]=a;occupied.add(dest);mapping[kind][mid]=dest
 return True
# Keep the entire valid City catalog and all City IDs, especially its cliffs.
for i,m in enumerate(city['meta']):
 if i not in bad['city'] and (any(m) or city['attrs'][i] or i in city['used']):assert add('city',i,True)
mandatory=set(harbor['used'])|set(assets['primary_custom_metatiles'])
for a in assets['assets'].values():
 for row in a['metatiles']:mandatory.update(row)
mandatory.update(e['havora_id'] for e in assets['catalog'] if e['town']=='pacifidlog')
for i in sorted(mandatory):assert add('harbor',i),('Required Harbor asset will not fit',i,cursor)
# Water-backed native cliff corners: preserve each cliff silhouette, removing
# only its green ground pixels. Keep the packed native cliff attribute intact.
water_corners={}
for label,source,dest in [('nw',33,168),('ne',33,169),('sw',47,170),('se',49,171)]:
 # Resolve the two source layers per pixel, including per-tile flips.
 pixels=[]
 m=city['meta'][source]
 for y in range(16):
  for x in range(16):
   q=(y//8)*2+x//8;v=None
   for k in (q,q+4):
    w=m[k];idx=flip(city['tiles'][w&1023],w&0xc00)[(y%8)*8+x%8]
    if idx or k<4:v=city['pals'][w>>12][idx]
   # Grass uses green hues; preserve every grey/brown cliff pixel exactly.
   if v[1]>v[0] and v[1]>v[2]:pixels.append(0)
   else:
    assert v in pals[1], ('cliff color missing',v)
    pixels.append(pals[1].index(v))
 if label=='ne':pixels=[pixels[y*16+15-x] for y in range(16) for x in range(16)]
 upper=[]
 for q in range(4):
  b=bytes(pixels[(q//2*8+y)*16+q%2*8+x] for y in range(8) for x in range(8))
  key,f=canonical(b)
  if key not in cache:
   assert cursor<len(free), 'No space for correct water cliff corners'
   t=free[cursor];cursor+=1;cache[key]=t;outtiles[t]=key
  upper.append(cache[key]|f|0x1000)
 outmeta[dest]=outmeta[mapping['harbor'][642]][:4]+tuple(upper)
 outattrs[dest]=city['attrs'][source];occupied.add(dest);water_corners[label]=dest
required_graphics=cursor+len(fixed)
# Retain additional unused catalog entries when they fit. Entire old Harbor
# source remains in the repository, with omitted IDs listed in the report.
optional=[i for i,m in enumerate(harbor['meta']) if i not in mandatory|bad['harbor'] and (any(m) or harbor['attrs'][i])]
# Prefer entries that share graphics already included, rather than arbitrary IDs.
while optional:
 optional.sort(key=lambda i:(len({d[1] for d in descriptors('harbor',i) if d[0]=='static' and d[1] not in cache}),i))
 i=optional.pop(0)
 if not add('harbor',i):optional.insert(0,i);break

def render(tiles,m,palette,frame=None):
 out=Image.new('RGB',(16,16))
 for k,w in enumerate(m):
  t=w&1023;b=tiles[t]
  if frame is not None and t>=896:b=frame[t-896]
  b=flip(b,w&0xc00)
  for q,v in enumerate(b):
   if v or k<4:out.putpixel(((k%2)*8+q%8,((k%4)//2)*8+q//8),palette[w>>12][v])
 return out.tobytes()
frames=[None]
for n in range(8):
 im=Image.open(io.BytesIO(read(f'data/tilesets/secondary/havora_harbor/anim/water/{n}.png')))
 frames.append([im.crop((x,y,x+8,y+8)).tobytes() for y in range(0,im.height,8) for x in range(0,im.width,8)])
# NORMAL layers expose fixed backdrop graphic 20 through double-transparent
# pixels. No placed source tile has such holes; retaining City slot 20 is safe.
for kind,s in sets.items():
 for mid in s['used']:
  if (s['attrs'][mid]>>29)&3:continue
  m=s['meta'][mid]
  for q in range(4):
   lo=flip(s['tiles'][m[q]&1023],m[q]&0xc00)
   hi=flip(s['tiles'][m[q+4]&1023],m[q+4]&0xc00)
   assert all(a or b for a,b in zip(lo,hi)), ('Backdrop exposed',kind,mid)
checks=0
for kind,s in sets.items():
 for old,new in mapping[kind].items():
  assert s['attrs'][old]==outattrs[new]
  for frame in frames:
   assert render(s['tiles'],s['meta'][old],s['pals'],frame)==render(outtiles,outmeta[new],pals,frame),(kind,old,new)
   checks+=1
# Source block flags, all map headers, connections, scripts, events and ferry
# warps remain unchanged. Only Harbor's low ten-bit metatile indices migrate.
outputs={};cells=0
for l in layouts['layouts']:
 if l['primary_tileset'] not in ('gTileset_HavoraPrimary','gTileset_HavoraCityPrimary'):continue
 kind='harbor' if l['primary_tileset']=='gTileset_HavoraPrimary' else 'city'
 for field in ('blockdata_filepath','border_filepath'):
  old=words(read(l[field]));new=[(w&0xfc00)|mapping[kind][w&1023] for w in old]
  assert all((a&0xfc00)==(b&0xfc00) for a,b in zip(old,new));cells+=len(old)
  if kind=='city':assert old==new
  if old!=new:outputs[l[field]]=packed(new)
 l['primary_tileset']='gTileset_HavoraCityPrimary';l['secondary_tileset']='gTileset_HavoraCity'
# Avoid whole-file reformatting: only the Harbor pair changes in layouts.json.
b=read('data/layouts/layouts.json').replace(b'"gTileset_HavoraPrimary"',b'"gTileset_HavoraCityPrimary"').replace(b'"gTileset_Havora_Harbor"',b'"gTileset_HavoraCity"')
outputs['data/layouts/layouts.json']=b
for group,start,count in [('primary',0,640),('secondary',640,384)]:
 path=f'data/tilesets/{group}/havora_city'
 im=Image.new('P',(128,count//16*8));im.putpalette([v for c in pals[0] for v in c]+[0]*720)
 for local,t in enumerate(outtiles[start:start+count]):im.paste(Image.frombytes('P',(8,8),t),((local%16)*8,(local//16)*8))
 buf=io.BytesIO();im.save(buf,format='PNG');outputs[path+'/tiles.png']=buf.getvalue()
 outputs[path+'/metatiles.bin']=packed([w for m in outmeta[start:start+count] for w in m])
 outputs[path+'/metatile_attributes.bin']=struct.pack('<'+'I'*count,*outattrs[start:start+count])
report=dict(source_tree=BASE,shared_primary='gTileset_HavoraCityPrimary',shared_secondary='gTileset_HavoraCity',graphics_used=cursor+len(fixed),graphics_required=required_graphics,animation_slots=len(animated),metatiles=len(occupied),water_cliff_corners=water_corners,retained_city=len(mapping['city']),retained_harbor=len(mapping['harbor']),omitted_unplaced_harbor=optional,removed_invalid_prototypes={k:sorted(v) for k,v in bad.items()},verified_render_comparisons=checks,verified_map_and_border_cells=cells,metatile_mapping=mapping)
outputs['tools/havora/shared-tileset.json']=(json.dumps(report,indent=2)+'\n').encode()
print(json.dumps({k:v for k,v in report.items() if k not in ('metatile_mapping','omitted_unplaced_harbor')},indent=2));print('Omitted unused Harbor definitions:',len(optional))
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--apply',action='store_true')
parser.add_argument('--check',action='store_true')
args=parser.parse_args()
if args.check:
 for p,b in outputs.items():assert (R/p).read_bytes()==b, ('On-disk migration differs',p)
 print('On-disk shared pair matches the verified migration.')
if args.apply:
 # Refuse to replace subsequent Porymap work with this frozen migration recipe.
 for p,b in outputs.items():
  if p=='tools/havora/shared-tileset.json':continue
  current=(R/p).read_bytes()
  assert current in (read(p),b), ('Preserve newer edits; migration stopped',p)
 for p,b in outputs.items():(R/p).write_bytes(b)
 print('Applied shared pair; all parity assertions passed.')
