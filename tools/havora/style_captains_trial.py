"""Private gym art pass: native ship/dock kits and small custom GBA pixel assets.
No city art changes or event relocation; the gauge reads the existing puzzle state.
"""
from pathlib import Path
import json,struct
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[2]
root=R/'data/tilesets'
def readwords(p,n=2):
 b=p.read_bytes();return list(struct.unpack('<'+('H' if n==2 else 'I')*(len(b)//n),b))
M=[];A=[];HM=[]
for g in ['primary','secondary']:
 M+=readwords(root/g/'havora_gym/metatiles.bin');A+=readwords(root/g/'havora_gym/metatile_attributes.bin',4);HM+=readwords(root/g/'havora_city/metatiles.bin')
HG=[Image.open(root/g/'havora_city/tiles.png') for g in ['primary','secondary']]
S=[root/'primary/general',root/'secondary/ss_anne'];SG=[Image.open(p/'tiles.png') for p in S];SM=readwords(S[1]/'metatiles.bin')
im=Image.open(root/'primary/havora_gym/tiles.png')
manifest=json.loads((R/'tools/havora/captains-trial.json').read_text());palmap={int(k):v for k,v in manifest['palette_mapping'].items()}
reserved={w&1023 for w in M};reserved|=set(json.loads((R/'tools/havora/fountain.json').read_text())['animation_graphic_ids'])
free=iter(i for i in range(128,640) if i not in reserved);packed={}
def graphic(raw):
 key=raw.tobytes()
 if key not in packed:
  idx=next(free);packed[key]=idx;im.paste(raw,(idx%16*8,idx//16*8))
 return packed[key]
def import_meta(dst,words,images,palette_mapping):
 out=[]
 for w in words:
  n=w&1023;g=int(n>=640);n-=640 if g else 0
  t=images[g].crop((n%16*8,n//16*8,n%16*8+8,n//16*8+8))
  out.append(graphic(t)|(w&0xc00)|(palette_mapping.get(w>>12,w>>12)<<12))
 M[dst*8:(dst+1)*8]=out;A[dst]=0x20000000
# Full S.S. Anne furniture kits and broad, readable planks replace thin stripe fill.
anne={0x281:0x298,0x318:0x298,0x319:0x2d5,0x31a:0x2f3,0x31b:0x2f4,
 0x360:0x305,0x361:0x306,0x362:0x307,0x363:0x30d,0x364:0x30e,0x365:0x30f,
 0x366:0x2a4,0x367:0x2fa,0x368:0x302,0x369:0x303,0x36a:0x2a3}
for dst,src in anne.items():import_meta(dst,SM[(src-640)*8:(src-640+1)*8],SG,palmap)
M[0x318*8:0x319*8]=HM[0x281*8:0x282*8];A[0x318]=0x20000000
# Harbour stone seawalls, mooring fixtures and two complete small hoists.
# Original stone palette 3 is relocated; palette 3 belongs to indoor props here.
harbor_map=json.loads((R/'tools/havora/shared-tileset.json').read_text())['metatile_mapping']['harbor']
assets=json.loads((R/'tools/havora/assets.json').read_text())['assets']
hmap={3:9}
for dst,name in [(0x320,'quay_north'),(0x321,'quay_south'),(0x322,'quay_west'),(0x323,'quay_east'),(0x324,'quay_sw'),(0x325,'quay_se'),(0x326,'bollard'),(0x340,'dock_west'),(0x341,'dock_east'),(0x342,'dock_foot_west'),(0x343,'dock_foot_east'),(0x344,'dock_foot')]:
 src=harbor_map[str(assets[name]['metatiles'][0][0])];import_meta(dst,HM[src*8:(src+1)*8],HG,hmap)
for y,row in enumerate(assets['crane']['metatiles']):
 for x,src in enumerate(row):
  src=harbor_map[str(src)];import_meta(0x330+y*3+x,HM[src*8:(src+1)*8],HG,hmap)
# Sluice rail: native S.S. Anne timber and metal balustrade.
M[0x327*8:0x328*8]=M[0x319*8:0x31a*8];A[0x327]=0
# Whole timber posts/rafters are cut from the existing log art and rotated.
# This preserves native pixel shading rather than inventing a new asset style.
def get_tile(w):
 n=w&1023;g=int(n>=640);n-=640 if g else 0;t=HG[g].crop((n%16*8,n//16*8,n%16*8+8,n//16*8+8))
 if w&1024:t=t.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
 if w&2048:t=t.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
 return t
post=Image.new('P',(8,16));post.paste(get_tile(HM[0x231*8+4]),(0,0));post.paste(get_tile(HM[0x231*8+6]),(0,8))
for mid,horizontal in [(0x347,False),(0x348,True)]:
 t=Image.new('P',(16,16));part=post.transpose(Image.Transpose.ROTATE_90) if horizontal else post;t.paste(part,(0,4) if horizontal else (4,0))
 words=[]
 for y in [0,8]:
  for x in [0,8]:words.append(graphic(t.crop((x,y,x+8,y+8)))|0x1000)
 M[mid*8:(mid+1)*8]=M[0x281*8:0x281*8+4]+words;A[mid]=0
# Shadow timber uses the otherwise empty native background palette. Only index
# zero was used by existing gym tiles in this palette, and stays black.
M[0x349*8:0x34a*8]=[(w&0xfff)|0x2000 if w>>12==0 else w for w in M[0x306*8:0x307*8]];A[0x349]=0
# Recess colored controls into the native riveted machinery plate.
for mid in range(0x300,0x304):M[mid*8:mid*8+4]=M[0x315*8:0x315*8+4]
# Portholes retain their native overlay but sit on timber, not white wall patches.
M[0x30b*8:0x30b*8+4]=M[0x349*8:0x349*8+4]
# Warm, weathered private palettes; water, NPC and city palettes remain unchanged.
def palette(path):return [list(map(int,l.split())) for l in path.read_text().splitlines()[3:19]]
def savepal(i,p):
 txt='JASC-PAL\n0100\n16\n'+'\n'.join(' '.join(map(str,c)) for c in p)+'\n'
 for g in ['primary','secondary']:(root/g/f'havora_gym/palettes/{i:02}.pal').write_text(txt)
p=palette(root/'primary/havora_gym/palettes/00.pal')
for i,c in {13:[88,64,40],14:[120,88,56],15:[160,128,88]}.items():p[i]=c
savepal(0,p)
shadow=[c.copy() for c in p];shadow[0]=[0,0,0]
for i,c in {13:[56,40,24],14:[80,56,32],15:[112,80,48]}.items():shadow[i]=c
savepal(2,shadow)
p=palette(root/'primary/havora_gym/palettes/05.pal')
for i,c in {6:[64,48,32],8:[88,64,40],10:[120,88,56],12:[160,128,88]}.items():p[i]=c
savepal(5,p)
p=palette(root/'primary/havora_gym/palettes/01.pal')
for i,c in enumerate([[184,152,104],[152,120,80],[128,96,64],[104,72,48],[80,56,32],[56,40,24]],9):p[i]=c
savepal(1,p)
p=palette(root/'primary/havora_gym/palettes/04.pal');p=[[v*7//8//8*8 for v in c] if max(c)-min(c)<40 and min(c)>128 else c for c in p];savepal(4,p)
savepal(9,palette(root/'primary/havora_city/palettes/03.pal'))
# Small hand-pixelled machinery kit: one GBA palette, crisp outlines, upper-left
# highlights and no antialiasing. These indices were unused in palette 2 by the
# native pieces; retain 0/1/2/4/11/13/14/15 for their existing wall/prop artwork.
p=palette(root/'primary/havora_gym/palettes/02.pal')
for i,c in {3:[40,48,56],5:[88,104,112],6:[152,168,168],7:[200,64,56],8:[56,136,208],9:[232,192,64],10:[80,176,112],12:[232,224,192]}.items():p[i]=c
savepal(2,p)
def custom(mid,canvas):
 words=[]
 for y in [0,8]:
  for x in [0,8]:words.append(graphic(canvas.crop((x,y,x+8,y+8)))|0x2000)
 M[mid*8:(mid+1)*8]=words+[0]*4;A[mid]=0x20000000
def canvas(bg=13):
 t=Image.new('P',(16,16),bg);return t,ImageDraw.Draw(t)
# Calm, framed timber replaces rows of disconnected porthole/hinge fragments.
t,d=canvas();d.rectangle((0,0,15,15),outline=13);d.rectangle((1,1,14,14),fill=14)
for x in [5,10]:d.line((x,2,x,13),fill=13)
d.line((1,1,14,1),fill=15);d.line((1,14,14,14),fill=13)
custom(0x349,t)
t,d=canvas();d.rectangle((0,4,15,12),fill=13);d.line((0,4,15,4),fill=15);d.line((0,6,15,6),fill=14)
for x in [2,13]:d.point((x,8),fill=6);d.point((x,9),fill=3)
custom(0x348,t)
# Four readable, mechanical controls: wheel winch, lift lever, bridge lever, bell.
for mid,color in [(0x300,7),(0x301,8),(0x302,9),(0x303,10)]:
 t,d=canvas(3);d.rectangle((1,1,14,14),fill=5,outline=6);d.line((2,13,13,13),fill=3)
 for x,y in [(2,2),(13,2),(2,12),(13,12)]:d.point((x,y),fill=12)
 if mid==0x300:
  d.ellipse((3,3,12,11),fill=13,outline=color);d.line((4,7,11,7),fill=color);d.line((7,4,7,10),fill=color);d.rectangle((7,6,8,7),fill=12)
 elif mid==0x303:
  d.rectangle((5,10,10,11),fill=3);d.ellipse((5,4,10,9),fill=color,outline=3);d.line((4,9,11,9),fill=12);d.point((7,3),fill=12)
 else:
  d.rectangle((6,4,9,11),fill=3);d.line((7,9,10,4),fill=12,width=2);d.rectangle((8,3,12,5),fill=color,outline=3)
 custom(mid,t)
# Boarding pads are painted on the existing floor, and stay passable.
for mid,upper in [(0x370,False),(0x371,True)]:
 # Composite the native 16x16 floor into palette 2's three wood shades.
 t,d=canvas(14)
 for y in [0,5,10,15]:d.line((0,y,15,y),fill=13)
 d.rectangle((2,2,13,13),outline=9);d.line((4,8,11,8),fill=12)
 d.line((8,5,11,8),fill=12);d.line((8,11,11,8),fill=12)
 if upper:d.point((4,4),fill=12);d.point((6,4),fill=12)
 else:d.point((4,4),fill=12)
 custom(mid,t)
 # Starboard landing points toward the boat, rather than farther into the dock.
 custom(mid+2,t.transpose(Image.Transpose.FLIP_LEFT_RIGHT))
# Two-state lock gauge has a thick frame and clearly separated LOW/HIGH stops.
for mid,high in [(0x376,False),(0x377,True)]:
 t,d=canvas(13);d.rectangle((2,1,13,14),fill=3,outline=6);d.rectangle((4,3,7,12),fill=5)
 d.rectangle((4,3 if high else 9,7,12),fill=8);d.line((9,4,11,4),fill=12);d.line((9,11,11,11),fill=12)
 d.rectangle((9,3 if high else 10,11,5 if high else 12),fill=9)
 custom(mid,t)
# Rope coil decor sits at the edge of working decks, outside the boarding lane.
t,d=canvas(14)
for y in [0,5,10,15]:d.line((0,y,15,y),fill=13)
for box in [(2,3,13,12),(4,5,11,10),(6,7,9,8)]:d.ellipse(box,outline=12)
d.line((12,10,14,14),fill=12);custom(0x378,t)
im.save(root/'primary/havora_gym/tiles.png',bits=4)
# Rebuild working surfaces, then place complete furniture at purposeful stations.
path=R/'data/layouts/HavoraCaptainsTrial/map.bin';B=readwords(path);W=40
def tile(x,y,mid,blocked=True,z=3):B[y*W+x]=(z<<12)|(0x400 if blocked else 0)|mid
def rect(x,y,w,h,mid,blocked=True,z=3):
 for yy in range(y,y+h):
  for xx in range(x,x+w):tile(xx,yy,mid,blocked,z)
def kit(x,y,grid):
 for yy,row in enumerate(grid):
  for xx,mid in enumerate(row):tile(x+xx,y+yy,mid)
for x,y,w,h,mid in [(2,3,36,6,0x281),(2,12,8,5,0x281),(2,24,8,5,0x281),(29,12,9,17,0x281),(2,30,36,5,0x280)]:rect(x,y,w,h,mid,False)
# Closed storage walls and substantial structural framing replace the black voids.
rect(2,17,8,6,0x349);rect(2,9,36,3,0x349)
for y in [1,9,17,23,29]:
 for x in (range(2,10) if y in [17,23] else range(2,38)):tile(x,y,0x348)
rect(2,2,36,1,0x349)
for x in [5,14,25,34]:tile(x,2,0x30b)
for x in [1,38]:
 for y in range(2,35):tile(x,y,0x349)
 for y in [3,8,13,18,23,28,33]:tile(x,y,0x347)
# Clear edges use the original dock waterline pieces, not floor stretching.
for y in list(range(12,17))+list(range(24,29)):tile(9,y,0x341,False)
for y in range(12,29):tile(29,y,0x340,False)
for x in range(10,29):tile(x,12,0x320,True,1)
for x in range(10,26):tile(x,19,0x327)
# Complete desks, captain's chart station and tall storage cases.
desk=[[0x360,0x361,0x362],[0x363,0x364,0x365]]
for x,y in [(4,5),(19,3),(31,5)]:kit(x,y,desk)
for x,y in [(9,3),(28,3),(35,23)]:kit(x,y,[[0x367],[0x368]])
for x,y in [(4,2),(34,2),(3,13)]:kit(x,y,[[0x31a,0x31b]])
for x,y in [(10,6),(29,6)]:tile(x,y,0x369)
# The lock hoist has a stone machinery pad; its colored console stays accessible.
rect(32,16,5,5,0x280,False)
kit(34,16,[[0x330+y*3+x for x in range(3)] for y in range(4)])
kit(6,24,[[0x330+y*3+x for x in range(3)] for y in range(4)])
for x,y in [(9,12),(30,13),(9,24),(30,25)]:tile(x,y,0x326)
for x,y,mid in [(5,31,0x300),(33,20,0x301),(5,14,0x302),(35,31,0x303)]:tile(x,y,mid)
for x,y in [(3,7),(36,7),(3,32),(37,32)]:tile(x,y,0x312)
# Beam ends and proper closed sluice shutters, with the same collision footprint.
for x,y,w,h in [(4,9,3,3),(33,9,3,3),(33,29,3,1)]:
 rect(x,y,w,h,0x349)
 for xx in range(x,x+w):tile(xx,y,0x348)
rect(4,29,3,1,0x282,True,1)
for x in [19,20,21]:tile(x,34,0x305,False)
# Give the puzzle's stations an identity without adding obstacles to its route.
for x,y,mid in [(9,26,0x370),(29,26,0x372),(9,14,0x371),(29,14,0x373)]:tile(x,y,mid,False)
tile(36,20,0x376)
for x,y in [(3,26),(31,16),(36,27),(12,7),(27,7)]:tile(x,y,0x378,False)
# Continuous upper/entrance beams and restrained upright framing.
for x in range(2,38):tile(x,1,0x348)
for x in [2,13,26,37]:tile(x,2,0x347)
for yy in range(3):
 for xx in range(3):tile(10+xx,25+yy,0x2bc+yy*3+xx)
path.write_bytes(struct.pack('<'+'H'*len(B),*B))
for group,start,end in [('primary',0,640),('secondary',640,1024)]:
 p=root/group/'havora_gym';(p/'metatiles.bin').write_bytes(struct.pack('<'+'H'*((end-start)*8),*M[start*8:end*8]));(p/'metatile_attributes.bin').write_bytes(struct.pack('<'+'I'*(end-start),*A[start:end]))
manifest.update({'art_pass':'Covered Nordic shipyard, working captain deck; readable machinery and berth markings','new_pixel_art':True,'extra_packed_graphics':len(packed),'native_imports':['Complete S.S. Anne desks, charts and storage cases','Havora dock edges, seawalls and Slateport hoists'],'derived_art':['Timber posts/rafters cut from native wood posts'],'custom_art':['Framed timber panels and beams','Winch wheel, lock and gangway levers, reset bell','Painted boarding pads, LOW/HIGH gauge, rope coil'],'private_palette_changes':'Walnut wood, weathered stone and eight previously-unused colors in private palette 2; water unchanged','review_before_commit':False})
(R/'tools/havora/captains-trial.json').write_text(json.dumps(manifest,indent=2)+'\n')
