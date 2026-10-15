from pathlib import Path
from PIL import Image
import numpy as np,struct
p=Path('.');d=p/'graphics/poke_glass_maps';d.mkdir(exist_ok=True)
tiles=(p/'graphics/region_map/region_map.4bpp').read_bytes()
pal=np.frombuffer((p/'graphics/region_map/region_map.gbapal').read_bytes(),dtype='<u2')
rgb=np.stack([(pal&31)*255//31,((pal>>5)&31)*255//31,((pal>>10)&31)*255//31],axis=1).astype(np.uint8)
images=[]
for name in ('kanto','sevii_123','sevii_45','sevii_67'):
 a=np.zeros((160,240,3),dtype=np.uint8)
 tm=struct.unpack('<600H',(p/f'graphics/region_map/{name}.bin').read_bytes())
 for y in range(160):
  for x in range(240):
   t=tm[y//8*30+x//8];tx=x%8;ty=y%8
   if t&0x400:tx=7-tx
   if t&0x800:ty=7-ty
   byte=tiles[(t&1023)*32+ty*4+tx//2]
   ci=(byte>>(tx%2*4))&15
   a[y,x]=rgb[(t>>12)*16+ci]
 images.append(Image.fromarray(a).resize((192,80),Image.Resampling.NEAREST))
combined=Image.new('RGB',(192,320))
for i,im in enumerate(images):combined.paste(im,(0,i*80))
q=combined.quantize(colors=15,method=Image.Quantize.MEDIANCUT)
colors=q.getpalette()[:45]+[255,255,255]
(d/'atlas_palette.bin').write_bytes(b''.join(struct.pack('<H',(colors[i]//8)|((colors[i+1]//8)<<5)|((colors[i+2]//8)<<10)) for i in range(0,48,3)))
for i,name in enumerate(('kanto','sevii_123','sevii_45','sevii_67')):
 a=np.asarray(q)[i*80:(i+1)*80]
 # GBA bitmaps are stored in eight-pixel tiles, as expected by the window blitter.
 data=bytearray()
 for ty in range(10):
  for tx in range(24):
   for y in range(8):
    for x in range(0,8,2):data.append(int(a[ty*8+y,tx*8+x])|(int(a[ty*8+y,tx*8+x+1])<<4))
 (d/f'{name}.bin').write_bytes(data)
 images[i].save(d/f'{name}_reference.png')
