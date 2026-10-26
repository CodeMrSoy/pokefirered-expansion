#!/usr/bin/env python3
"""Verify only the intended service buildings and unused catalog slots changed."""
import io,json,struct,subprocess
from pathlib import Path
from PIL import Image
R=Path(__file__).resolve().parents[2];BASE='ac291bc1'
def source(p):return subprocess.check_output(['git','show',BASE+':'+p],cwd=R)
def js(p):return json.loads((R/p).read_text())
def ww(b):return list(struct.unpack('<'+'H'*(len(b)//2),b))
T=[];OT=[];M=[];OM=[];A=[];OA=[]
for g,count in [('primary',640),('secondary',384)]:
 p=f'data/tilesets/{g}/havora_city/'
 for out,data in [(T,(R/p/'tiles.png').read_bytes()),(OT,source(p+'tiles.png'))]:
  im=Image.open(io.BytesIO(data));out.extend(im.crop((i%16*8,i//16*8,i%16*8+8,i//16*8+8)).tobytes() for i in range(count))
 M+=ww((R/p/'metatiles.bin').read_bytes());OM+=ww(source(p+'metatiles.bin'))
 A+=list(struct.unpack('<'+'I'*count,(R/p/'metatile_attributes.bin').read_bytes()));OA+=list(struct.unpack('<'+'I'*count,source(p+'metatile_attributes.bin')))
 for path in (R/p/'palettes').glob('*.pal'):
  before=source(str(path.relative_to(R))).decode().splitlines();after=path.read_text().splitlines()
  for i,(a,b) in enumerate(zip(before,after)):
   if a!=b:assert path.name=='00.pal' and i==10 and b=='172 32 41'
old=json.loads(source('tools/havora/civic-tiles.json'));new=js('tools/havora/civic-tiles.json');repair=js('tools/havora/civic-repair.json');allowed={v for which in [old,new] for n in ['center','mart'] for row in which['assets'][n] for v in row}|set(repair['retired_unplaced'])
for mid in range(1024):
 if mid in allowed:continue
 assert M[mid*8:(mid+1)*8]==OM[mid*8:(mid+1)*8] and A[mid]==OA[mid],mid
 for word in M[mid*8:(mid+1)*8]:assert T[word&1023]==OT[word&1023],mid
fixed=set(range(416,482))|set(range(508,512))|set(range(896,1024))|{0,20}|set(js('tools/havora/fountain.json')['animation_graphic_ids'])
assert all(T[i]==OT[i] for i in fixed)
assert not any(7 in OT[w&1023] for w in OM if w>>12==0)
assert not any(7 in Image.open(p).tobytes() for p in (R/'data/tilesets/primary/general/anim/flower').glob('*.png'))
assert not any(w>>12==0 and 416<=w&1023<482 for w in OM)
assert len(new['assets']['center'])==4 and all(len(row)==5 for row in new['assets']['center'])
assert len(new['assets']['mart'])==4 and all(len(row)==4 for row in new['assets']['mart'])
l=next(l for l in js('data/layouts/layouts.json')['layouts'] if l['name']=='Havora_NorthQuadrant_Layout');v=ww((R/l['blockdata_filepath']).read_bytes())
for name,x,y in [('center',73,5),('mart',80,5)]:
 for j,row in enumerate(new['assets'][name]):
  for i,mid in enumerate(row):assert v[(y+j)*90+x+i]&1023==mid
h=next(l for l in js('data/layouts/layouts.json')['layouts'] if l['name']=='Havora_Harbor_Layout');used={v&1023 for v in ww((R/h['blockdata_filepath']).read_bytes())}
assert used.isdisjoint(allowed)
print(json.dumps({'center_complete_size':[5,4],'mart_complete_size':[4,4],'unused_palette_entry_repurposed':'0:7 dark red','all_other_existing_metatiles_and_graphics_preserved_except_archived_unplaced_modules':True,'all_water_flower_and_fountain_animation_graphics_preserved':True,'harbor_graphics_and_attributes_unchanged':True},indent=2))
