"""Native FireRed animated sand shoreline; reuse descriptors, never flatten frames.

General's callback updates graphics 464–481 every eight engine ticks. Mixing
native quadrants preserves their tile IDs, flips, palettes and animation.
"""
import struct
from PIL import Image
SAND=0x115
# N, E, S, W masks. The diagonal-only caps are their native concave corners.
STRAIGHT={1:0x251,2:0x25a,4:0x261,8:0x258}
OUTER={(1,8):0x250,(1,2):0x252,(4,8):0x260,(4,2):0x262}
INNER={0:0x25b,1:0x25c,2:0x263,3:0x264}
QUADRANTS=[(1,8,-1,-1),(1,2,1,-1),(4,8,-1,1),(4,2,1,1)]

class NativeShore:
 def __init__(self,root,native,register):
  self.words=struct.unpack('<5120H',(root/'data/tilesets/primary/general/metatiles.bin').read_bytes())
  self.native=native;self.register=register;self.cache={}
 def descriptors(self,mid):return list(self.words[mid*8:mid*8+8])
 def shoreline(self,mask,diagonals):
  key=(mask,diagonals)
  if key in self.cache:return self.cache[key]
  descriptors=[0]*8;preview=Image.new('RGB',(16,16))
  for q,(v,h,dx,dy) in enumerate(QUADRANTS):
   a,b=bool(mask&v),bool(mask&h)
   src=OUTER[(v,h)] if a and b else STRAIGHT[v] if a else STRAIGHT[h] if b else INNER[q] if diagonals&(1<<q) else SAND
   words=self.descriptors(src);descriptors[q]=words[q];descriptors[q+4]=words[q+4]
   x=q%2*8;y=q//2*8;preview.paste(self.native[src].crop((x,y,x+8,y+8)),(x,y))
  mid=self.register(descriptors,0x21,preview)
  self.cache[key]=mid;return mid
