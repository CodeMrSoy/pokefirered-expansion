"""Append stock FireRed service-building shapes to the existing city pair.

Existing graphics, metatiles and palette entries are preserved. New graphics
use the closest existing material palette per 8x8 tile, without dithering.
"""
import json,struct
from pathlib import Path
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parents[2]
def words(p):
 b=p.read_bytes();return list(struct.unpack('<'+'H'*(len(b)//2),b))
def build():
 city=R/'data/tilesets';paths=[city/d/'havora_city' for d in ['primary','secondary']]
 meta=words(paths[0]/'metatiles.bin')+words(paths[1]/'metatiles.bin')
 attrs=bytearray((paths[0]/'metatile_attributes.bin').read_bytes()+(paths[1]/'metatile_attributes.bin').read_bytes())
 config=json.loads((R/'tools/havora/city-tileset.json').read_text())
 previous=R/'tools/havora/civic-tiles.json'
 if previous.exists():return json.loads(previous.read_text())
 used=set(config['compatible_metatiles'])|set(config['native_general_ids'].values())
 reserved=set(json.loads((R/'tools/havora/assets.json').read_text())['reserved_primary_tiles'])|set(range(896,1024))
 usedtiles={w&1023 for m in used for w in meta[m*8:m*8+8]}|reserved
 free=iter(i for i in range(1024) if i not in usedtiles)
 freemeta=iter(i for i in range(0x100,640) if i not in used)
 full=Image.new('P',(128,512),0)
 for i,p in enumerate(paths):full.paste(Image.open(p/'tiles.png'),(0,0 if i==0 else 320))
 gp=city/'primary/general';native=words(gp/'metatiles.bin');nativeattrs=(gp/'metatile_attributes.bin').read_bytes();source=Image.open(gp/'tiles.png')
 def pals(root,i):return np.array([list(map(int,s.split())) for s in (root/'palettes'/f'{i:02}.pal').read_text().splitlines()[3:19]],dtype=np.int32)>>3<<3
 sourcep=[pals(gp,i) for i in range(13)]
 palettes=[pals(paths[0 if i<7 else 1],i) for i in range(13)]
 # Original Vermilion service exteriors, including the right Center annex.
 specs={'center':(13,3,4,4),'mart':(27,14,4,4),'gym':(11,21,7,5)}
 layouts=json.loads((R/'data/layouts/layouts.json').read_text())['layouts'];l=next(l for l in layouts if l['id']=='LAYOUT_VERMILION_CITY')
 blocks=words(R/l['blockdata_filepath']);grids={};mapping={};cached={};newtiles=[];errors=[]
 for name,(x,y,w,h) in specs.items():
  grid=[]
  for yy in range(y,y+h):
   row=[]
   for xx in range(x,x+w):
    mid=blocks[yy*48+xx]&1023
    if mid not in mapping:
     target=next(freemeta);mapping[mid]=target;out=[]
     for word in native[mid*8:mid*8+8]:
      tid=word&1023;bank=word>>12;patch=np.array(source.crop((tid%16*8,tid//16*8,tid%16*8+8,tid//16*8+8)))
      rgb=sourcep[bank][patch];mask=patch!=0
      best=None
      for destbank,pal in enumerate(palettes):
       dist=((rgb[:,:,None,:]-pal[None,None,1:,:])**2).sum(axis=3)
       idx=dist.argmin(axis=2)+1;error=float(dist.min(axis=2)[mask].sum())
       idx=np.where(mask,idx,0).astype(np.uint8)
       if best is None or error<best[0]:best=(error,destbank,idx)
      error,destbank,idx=best;key=idx.tobytes()
      if key not in cached:
       dest=next(free);cached[key]=dest;newtiles.append(dest)
       full.paste(Image.fromarray(idx),(dest%16*8,dest//16*8))
      out.append((word&0xC00)|(destbank<<12)|cached[key]);errors.append(error)
     meta[target*8:target*8+8]=out;attribute=struct.unpack_from('<I',nativeattrs,mid*4)[0]
     if mid in [0x62,0x15B]:attribute=0x60
     struct.pack_into('<I',attrs,target*4,attribute)
    row.append(mapping[mid])
   grid.append(row)
  grids[name]=grid
 for p,start,count in [(paths[0],0,640),(paths[1],640,384)]:
  im=full.crop((0,start//16*8,128,(start+count)//16*8));im.putpalette(Image.open(p/'tiles.png').getpalette());im.save(p/'tiles.png')
  (p/'metatiles.bin').write_bytes(struct.pack('<'+'H'*(count*8),*meta[start*8:(start+count)*8]));(p/'metatile_attributes.bin').write_bytes(attrs[start*4:(start+count)*4])
 result={'assets':grids,'native_general_ids':mapping,'added_graphics':len(newtiles),'graphics_slots':newtiles,'graphics_budget':config['graphics_used']+len(newtiles),'palette_note':'Native FireRed shapes; colors fitted to the existing city material palettes, no dithering.'}
 previous.write_text(json.dumps(result,indent=2)+'\n');return result
if __name__=='__main__':print(build()['graphics_budget'])
