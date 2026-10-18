"""Verify the new boulder's actual VRAM pixels animate only outside the stone."""
import json,struct
import numpy as np
from PIL import Image
import havora_emulator_support as m
asset=json.loads((m.root/'tools/havora/assets.json').read_text());anim=asset['animation']
m.inject(b'\x39'+struct.pack('<BBBHH',43,19,255,20,18)+b'\x6b\x02');m.run(300)
mid=asset['assets']['zz_water_boulder']['metatiles'][0][0]
path=m.root/'data/tilesets/primary/havora_harbor'
words=struct.unpack_from('<8H',(path/'metatiles.bin').read_bytes(),mid*16)
palettes=[[tuple(map(int,l.split())) for l in (path/'palettes'/f'{i:02}.pal').read_text().splitlines()[3:19]] for i in range(13)]
def decode():
 vram=m.read(0x06000000,32768);out=np.zeros((16,16,3),dtype=np.uint8)
 for k,w in enumerate(words):
  tid=w&1023;raw=vram[tid*32:tid*32+32]
  for y in range(8):
   for x in range(8):
    sx=7-x if w&1024 else x;sy=7-y if w&2048 else y
    byte=raw[sy*4+sx//2];ix=(byte>>(4*(sx%2)))&15
    if ix or k<4:out[(k%4)//2*8+y,k%2*8+x]=palettes[w>>12][ix]
 return out
phases=[];images=[]
for _ in range(8):m.run(16);phases.append(decode());images.append(m.screen.copy())
body=np.array(Image.open(m.root/'tools/havora/source_art/emerald_harbor/zz_water_boulder.png').convert('RGBA'))[:,:,3]>0
assert all(np.array_equal(a[body],phases[0][body]) for a in phases),'stone moved with waves'
assert len({a[~body].tobytes() for a in phases})==8,'boulder sea animation stalled'
assert len({a.tobytes() for a in images})==8,'sea animation not visible in gameplay'
shots=[Image.fromarray(a).resize((256,256),Image.Resampling.NEAREST) for a in phases]
shots[0].save(m.d/'havora-water-boulder.gif',save_all=True,append_images=shots[1:],duration=267,loop=0,disposal=2)
print('PASS: water boulder stone stays fixed across eight animated sea phases in actual VRAM',flush=True)
