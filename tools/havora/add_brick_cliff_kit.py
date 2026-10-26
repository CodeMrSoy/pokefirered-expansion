"""Brick-material versions of the native FireRed cliff shape catalog.

Only unused metatiles in the private gym tileset are populated. The authored
map and all existing brick pieces remain unchanged. Run explicitly to rebuild.
"""
from pathlib import Path
import json,struct,sys
from PIL import Image,ImageFilter
R=Path(__file__).resolve().parents[2]
P=R/'data/tilesets/primary/havora_gym';S=R/'data/tilesets/secondary/havora_gym'
N=R/'data/tilesets/primary/general'
SHAPES=[('upper_left',0x68),('upper',0x69),('upper_right',0x6a),('rising_left',0x6b),('rising_middle',0x6c),('rising_right',0x6d),('inset_upper_left',0x6e),('inset_upper_right',0x6f),('side_left',0x70),('face',0x71),('side_right',0x72),('narrow_left',0x73),('narrow_right',0x75),('foot_left',0x78),('foot',0x79),('foot_right',0x7a),('deep_foot_left',0x7b),('deep_foot',0x7c),('deep_foot_right',0x7d),('thin_cap_left',0x83),('thin_cap_right',0x84),('inset_side_left',0x85),('inset_side_right',0x86),('inset_front',0x87),('inset_lower_left',0x8b),('inset_lower_right',0x8c),('deep_inset_left',0x8d),('deep_inset_right',0x8e)]
FIRST=0x3c5;COUNT=len(SHAPES)
def words(p,fmt='H'):
 b=p.read_bytes();return list(struct.unpack('<'+fmt*(len(b)//struct.calcsize(fmt)),b))
m=words(P/'metatiles.bin')+words(S/'metatiles.bin');attrs=words(S/'metatile_attributes.bin','I')
srcm=words(N/'metatiles.bin');srci=Image.open(N/'tiles.png')
pals=[]
for i in range(7):pals.append([tuple(map(int,l.split())) for l in (N/f'palettes/{i:02}.pal').read_text().splitlines()[3:19]])
def native(mid):
 out=Image.new('RGB',(16,16))
 for k,v in enumerate(srcm[mid*8:mid*8+8]):
  n=v&1023
  for y in range(8):
   for x in range(8):
    c=srci.getpixel((n%16*8+(7-x if v&1024 else x),n//16*8+(7-y if v&2048 else y)))
    if c or k<4:out.putpixel((k%2*8+x,k%4//2*8+y),pals[v>>12][c])
 return out
im=Image.open(P/'tiles.png').copy();kit=set(range(FIRST,FIRST+COUNT*2))
used={w&1023 for n in range(len(m)//8) if n not in kit for w in m[n*8:n*8+8]}
free=iter(i for i in range(128,640) if i not in used);packed={}
def graphic(t):
 key=t.tobytes()
 if key not in packed:
  idx=next(free);packed[key]=idx;im.paste(t,(idx%16*8,idx//16*8))
 return packed[key]
def brick(mid):
 original=native(mid);mask=Image.new('1',(16,16));lum=original.convert('L').filter(ImageFilter.BoxBlur(1))
 for y in range(16):
  for x in range(16):
   r,g,b=original.getpixel((x,y))
   if r>g+5 and r>b+5:mask.putpixel((x,y),1)
 t=Image.new('P',(16,16),0)
 for y in range(16):
  for x in range(16):
   if not mask.getpixel((x,y)):continue
   level=lum.getpixel((x,y));color=6 if level>=168 else 5 if level>=90 else 3
   # Two staggered brick courses use the source wall's plane shading.
   if y%8==7 or (x-(0 if y<8 else 6))%12==0:color=3
   elif y%8==0 and level>=115:color=6
   # Keep the native convex/concave silhouette pixel-for-pixel.
   if y<15 and not mask.getpixel((x,y+1)):color=3
   if x>0 and not mask.getpixel((x-1,y)) and color!=3:color=6
   t.putpixel((x,y),color)
 return t
catalog=[]
for i,(name,src) in enumerate(SHAPES):
 t=brick(src);overlay=[graphic(t.crop((x,y,x+8,y+8)))|0x2000 for y in [0,8] for x in [0,8]]
 entry={'shape':name,'source_cliff':hex(src)}
 for variant,base,offset in [('water',0x282,0),('wood',0x281,COUNT)]:
  mid=FIRST+i+offset;m[mid*8:mid*8+8]=m[base*8:base*8+4]+overlay;attrs[mid-640]=0x20000000;entry[variant]=hex(mid)
 catalog.append(entry)
im.save(P/'tiles.png',bits=4)
(S/'metatiles.bin').write_bytes(struct.pack('<'+'H'*(len(m)-640*8),*m[640*8:]))
(S/'metatile_attributes.bin').write_bytes(struct.pack('<'+'I'*len(attrs),*attrs))
(R/'tools/havora/brick-cliff-kit.json').write_text(json.dumps({'first':hex(FIRST),'last':hex(FIRST+COUNT*2-1),'shapes':catalog,'placement':'Manual placement in Porymap; no map cells changed','backgrounds':['animated water','original wood floor']},indent=2)+'\n')
print('Added',COUNT*2,'native cliff-shaped brick pieces at',hex(FIRST),'through',hex(FIRST+COUNT*2-1),'using',len(packed),'graphics; map untouched')
