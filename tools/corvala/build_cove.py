"""Corvala restart: a cave-access reef cove, authored at LOW tide.

Explicit --write rebuilds this design; default only checks/produces a preview.
Never invoked by make. An output hash guard protects later Porymap edits.
"""
from pathlib import Path
from collections import deque
import argparse, json, struct, hashlib, sys
from PIL import Image, ImageDraw
import art as A
from stilt_houses import kit as house_art
from shoreline import NativeShore

R=Path(__file__).resolve().parents[2];D=R/'data/tilesets/secondary/corvala'
sys.path.insert(0,str(R/'tools/havora'))
from render import atlas
W=H=64
def read(p):return json.loads(p.read_text())
def write(p,data):
 p.parent.mkdir(parents=True,exist_ok=True)
 if isinstance(data,str) and p.suffix=='.pal':data=data.replace('\r\n','\n').replace('\n','\r\n')
 if not isinstance(data,bytes):data=(json.dumps(data,indent=2)+'\n').encode() if not isinstance(data,str) else data.encode()
 if not p.exists() or p.read_bytes()!=data:p.write_bytes(data)
def words(p,n=2):
 b=p.read_bytes();return list(struct.unpack('<'+('H' if n==2 else 'I')*(len(b)//n),b))
def rect(x,y,w,h):return {(xx,yy) for yy in range(y,y+h) for xx in range(x,x+w)}
def polygon(points):
 im=Image.new('1',(W,H));ImageDraw.Draw(im).polygon(points,fill=1)
 return {(x,y) for y in range(H) for x in range(W) if im.getpixel((x,y))}
def flood(blocks,w,h,start,exclude=()):
 seen={tuple(start)};q=deque(seen)
 while q:
  x,y=q.popleft()
  for p in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
   xx,yy=p
   if 0<=xx<w and 0<=yy<h and p not in seen and p not in exclude and not blocks[yy*w+xx]&0xc00 and blocks[yy*w+xx]>>12==3:seen.add(p);q.append(p)
 return seen

class Pack:
 def __init__(self):
  self.tiles=[bytes(64)];self.lookup={bytes(64):640};self.metas=[];self.attrs=[];self.ml={}
  self.primary=words(R/'data/tilesets/primary/general/metatiles.bin');self.pa=words(R/'data/tilesets/primary/general/metatile_attributes.bin',4)
 def desc(self,mid):return self.primary[mid*8:mid*8+8] if mid<640 else self.metas[mid-640]
 def attr(self,mid):return self.pa[mid] if mid<640 else self.attrs[mid-640]
 def meta(self,ds,a=0,*unused):
  key=tuple(ds)+(a,)
  if key not in self.ml:self.ml[key]=640+len(self.metas);self.metas.append(ds);self.attrs.append(a)
  return self.ml[key]
 def pixels(self,im,bank):
  ds=[]
  for x,y in [(0,0),(8,0),(0,8),(8,8)]:
   tile=im.crop((x,y,x+8,y+8));raw=tile.tobytes()
   if raw not in self.lookup:
    tid=640+len(self.tiles);assert tid<1024,'secondary graphics exhausted';self.tiles.append(raw)
    for f,v in [(0,tile),(1024,tile.transpose(Image.Transpose.FLIP_LEFT_RIGHT)),(2048,tile.transpose(Image.Transpose.FLIP_TOP_BOTTOM)),(3072,tile.transpose(Image.Transpose.ROTATE_180))]:self.lookup.setdefault(v.tobytes(),tid|f)
   ds.append(self.lookup[raw]|bank<<12)
  return ds
 def overlay(self,base,im,bank,a=None):return self.meta(self.desc(base)[:4]+self.pixels(im,bank),self.attr(base) if a is None else a)
 def full(self,im,bank,a=0):return self.meta(self.pixels(im,bank)+[640]*4,a)

def build():
 p=Pack();native=atlas('cinnabar_island');shore=NativeShore(R,native,p.meta)
 blocks=[0x1000|0x12b]*(W*H)
 def put(x,y,mid,solid=False,e=3):
  assert 0<=x<W and 0<=y<H
  blocks[y*W+x]=mid|(0xc00 if solid else 0)|(e<<12)
 # A sheltered bowl, with no east/west road seams and no departure pier.
 # Native cliff tops are thick, then drop through a complete two-row face.
 rim=[18,18,18,18,18,18,18,17,17,17,17,16,16,16,16,15,15,14,14,13,13,12,12,11,11,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,11,11,11,12,12,12,13,13,14,14,14,14,14,14,15,15,16,16,18,20,23,27,31,34]
 # Both cave mouths are carved INTO connected headlands.
 for x in range(9,17):rim[x]=20 if 10<=x<=14 else 19
 for x in range(46,54):rim[x]=16
 cliffs={(x,y) for x in range(W) for y in range(rim[x]+1)}
 beach=polygon([(7,20),(17,17),(22,14),(30,13),(40,14),(51,17),(57,23),(57,31),(53,37),(48,39),(45,43),(40,45),(35,44),(31,46),(27,45),(24,42),(19,42),(16,39),(10,37),(8,31)])-cliffs
 # Exposed reef shelves are lumpy islands, linked by narrow low-tide paths.
 shelves=[polygon([(6,39),(9,37),(14,38),(17,41),(16,45),(12,47),(7,45),(5,42)]),
 polygon([(20,46),(23,43),(27,44),(30,48),(29,53),(25,55),(20,53),(18,49)]),
 polygon([(36,49),(40,46),(45,47),(48,50),(46,55),(41,57),(36,54)]),
 polygon([(51,42),(54,40),(58,42),(59,46),(56,49),(52,47)])]
 for s in shelves:beach|=s
 beach|=rect(14,38,3,5)|rect(23,40,3,8)|rect(28,48,10,2)|rect(43,41,3,8)|rect(48,39,6,3)
 # Small pools leave readable negative space between coral beds.
 pools=rect(12,25,3,3)|rect(47,30,3,3)|rect(30,40,3,2)
 pools|=polygon([(24,16),(29,14),(39,15),(44,18),(43,22),(39,25),(27,25),(23,22)])
 beach-=pools
 for x,y in beach:put(x,y,0x115)
 for x,y in cliffs:
  bottom=rim[x]
  if y==bottom:mid=0x79
  elif y==bottom-1:mid=0x71
  else:mid=0x8
  put(x,y,mid,True)
 # Rock strata on the headland silhouette; plants grow on the crown.
 for x,y in cliffs:
  if y<rim[x]-1 and (y<3 or x<3 or x>60):put(x,y,0x71,True)
 # Complete live shore quadrants around the low-tide land (before decks).
 for x,y in beach:
  mask=sum(1<<i for i,(dx,dy) in enumerate([(0,-1),(1,0),(0,1),(-1,0)]) if (x+dx,y+dy) not in beach|cliffs)
  diagonals=sum(1<<i for i,(dx,dy) in enumerate([(-1,-1),(1,-1),(-1,1),(1,1)]) if (x+dx,y+dy) not in beach|cliffs)
  if mask or diagonals:put(x,y,shore.shoreline(mask,diagonals))
 # Hand-arranged dock silhouette: broad house platforms, an open plaza and
 # narrow walkways. The permanent route reaches every service at any tide.
 decks=rect(26,21,12,12)|rect(15,26,10,9)|rect(40,25,11,10)|rect(27,35,12,9)
 decks|=rect(23,30,19,4)|rect(31,31,4,7)|rect(48,18,3,10)|rect(46,17,7,3)
 decks|=rect(18,24,3,6)
 # A small observation landing replaces the previous lighthouse/arrival pier.
 decks|=rect(39,38,8,4)|rect(37,37,4,3)
 # Five homes in total: west, southwest and northeast additions have their
 # own landings and join the existing permanent dock network.
 decks|=rect(6,28,9,9)|rect(14,32,3,3)|rect(15,35,11,9)|rect(20,33,4,3)|rect(39,17,9,9)
 floors=[]
 for variant in range(2):
  im=Image.new('P',(16,16),5);d=ImageDraw.Draw(im)
  for y in (0,8):
   d.line((0,y,15,y),fill=3);d.line((0,y+1,15,y+1),fill=6)
   if y//8==variant:d.line((5,y+1,5,y+7),fill=4)
   d.line((9,y+5,13,y+5),fill=4)
  floors.append(p.full(im,9))
 buildings=[dict(name='center',x=29,y=21,w=5,h=5,door=[31,25]),dict(name='mart',x=17,y=27,w=4,h=4,door=[19,30]),dict(name='house1',x=42,y=26,w=7,h=6,door=[45,31]),dict(name='house2',x=29,y=36,w=7,h=6,door=[32,41])]
 buildings += [dict(name='house3',x=7,y=29,w=7,h=6,door=[10,34]),dict(name='house4',x=16,y=36,w=7,h=6,door=[19,41]),dict(name='house5',x=40,y=18,w=7,h=6,door=[43,23])]
 occupied=set().union(*(rect(b['x'],b['y'],b['w'],b['h']) for b in buildings))
 edges={};support={};labels={}
 for wet,base in [(False,0x115),(True,0x12b)]:
  for post in (False,True):
   im=Image.new('P',(16,16));d=ImageDraw.Draw(im)
   d.rectangle((0,0,15,2),fill=2);d.line((0,0,15,0),fill=4)
   d.line((0,3,15,3),fill=3)
   if post:
    end=10 if wet else 14
    if not wet:d.ellipse((2,12,12,15),fill=3)
    d.rectangle((4,1,10,end),fill=2)
    d.rectangle((5,2,8,end-1),fill=4);d.line((5,2,5,end-2),fill=6)
    d.line((8,4,8,end-2),fill=3);d.line((6,6,6,9),fill=5)
    # A dark iron fastening sits below the beam; no detached wedge brace.
    d.line((4,4,10,4),fill=1);d.point((5,4),fill=7)
    if wet:d.line((2,end,12,end),fill=12)
   support[wet,post]=p.overlay(base,im,9)
   labels[('Water' if wet else 'Sand')+('Pilings' if post else 'Underside')]=support[wet,post]
 for x,y in sorted(decks):
  mask=sum(1<<i for i,(dx,dy) in enumerate([(0,-1),(1,0),(0,1),(-1,0)]) if (x+dx,y+dy) not in decks|occupied)
  key=x%2,mask
  if key not in edges:
   im=Image.new('P',(16,16));d=ImageDraw.Draw(im)
   if mask&1:d.line((0,0,15,0),fill=2);d.line((0,1,15,1),fill=7)
   if mask&2:d.rectangle((14,0,15,15),fill=2)
   if mask&8:d.line((0,0,0,15),fill=2);d.line((1,1,1,14),fill=6)
   if mask&4:
    d.rectangle((0,10,15,15),fill=2);d.line((0,10,15,10),fill=7);d.line((0,12,15,12),fill=4);d.line((0,15,15,15),fill=1)
   edges[key]=p.overlay(floors[x%2],im,9)
  put(x,y,edges[key])
 for x,y in sorted(decks):
  if (x,y+1) not in decks|occupied and (x,y+1) not in cliffs:
   wet=(x,y+1) not in beach
   put(x,y+1,support[wet,x%2==0],True,1 if wet else 3)
 # Three designated stairs down to LOW sand; all other front supports are solid.
 stairs=p.full(A.stairs(),9);labels['Stairs']=stairs
 for x,y in [(22,35),(23,35),(35,44),(36,44),(45,42),(46,42)]:put(x,y,stairs)
 # Native red Center and blue Mart, including the engine's animated door.
 # Exact five-by-five native Pewter Center, including roof cap and right wall.
 center=[[0x17b,0x17c,0x17d,0x17e,0x17f],[0x48,0x49,0x4a,0x4b,0x187],[0x50,0x51,0x52,0x53,0x18f],[0x58,0x59,0x5a,0x5b,0x197],[0x60,0x61,0x62,0x186,0x19f]]
 mart=[[0x28,0x29,0x2a,0x2b],[0x30,0x31,0x32,0x33],[0x38,0x39,0x3a,0x3b],[0x40,0x41,0x62,0x63]]
 for b,art in zip(buildings[:2],[center,mart]):
  for yy,row in enumerate(art):
   for xx,mid in enumerate(row):
    # Native roof caps and right walls have a separate grass backing. Keep
    # every building pixel while placing those transparent edges on timber.
    if b['name']=='center' and (yy==0 or xx==4):
     mid=p.meta(p.desc(floors[(b['x']+xx)%2])[:4]+p.desc(mid)[4:],p.attr(mid))
    put(b['x']+xx,b['y']+yy,mid,[b['x']+xx,b['y']+yy]!=b['door'])
 art,_=house_art(R,atlas)
 for b,style,bank in [(buildings[2],'pallet',11),(buildings[3],'sevii',10),(buildings[4],'cerulean',9),(buildings[5],'pallet',11),(buildings[6],'sevii',10)]:
  for yy in range(6):
   for xx in range(7):
    im=art[style].crop((xx*16,yy*16,xx*16+16,yy*16+16))
    mid=p.overlay(floors[(b['x']+xx)%2],im,bank,0x60 if [b['x']+xx,b['y']+yy]==b['door'] else 0)
    put(b['x']+xx,b['y']+yy,mid,[b['x']+xx,b['y']+yy]!=b['door'])
 # Two distinct portals: the sole town entrance and the local tidal gym.
 # Three visible terrace faces rise from the boardwalk toward the gym cave.
 # Their collision permits movement only through the two-cell stone stairs.
 terrace_specs=[(7,19,14,5,18),(6,14,13,5,9),(5,9,13,5,15)]
 stone=Image.new('P',(32,16),3);sd=ImageDraw.Draw(stone)
 for sy in (0,4,8,12):
  sd.rectangle((3,sy,28,sy+2),fill=5);sd.line((3,sy,28,sy),fill=7);sd.line((3,sy+3,28,sy+3),fill=2)
 sd.rectangle((0,0,2,15),fill=4);sd.line((0,0,0,15),fill=6)
 sd.rectangle((29,0,31,15),fill=2);sd.line((29,0,29,15),fill=5)
 stone_steps=[p.full(stone.crop((x,0,x+16,16)),8) for x in (0,16)]
 labels.update(StoneStairsLeft=stone_steps[0],StoneStairsRight=stone_steps[1])
 terrace_steps=[]
 terrace_cells=set().union(*(rect(tx,ty,tw,th) for tx,ty,tw,th,sx in terrace_specs))
 for tx,ty,tw,th,sx in terrace_specs:
  for yy in range(ty,ty+th):
   for xx in range(tx,tx+tw):
    front=yy>=ty+th-2;side=xx in (tx,tx+tw-1)
    exposed_top=yy==ty and (xx,yy-1) not in terrace_cells and ty!=9
    if front:
     if yy==ty+th-2:mid=0x70 if xx==tx else 0x72 if xx==tx+tw-1 else 0x71
     else:mid=0x78 if xx==tx else 0x7a if xx==tx+tw-1 else 0x79
    elif side:mid=0x70 if xx==tx else 0x72
    elif exposed_top:mid=0x71
    else:mid=0x8
    put(xx,yy,mid,front or side or exposed_top)
  for yy in range(ty+th-2,ty+th):
   for xx in (sx,sx+1):put(xx,yy,stone_steps[xx-sx]);terrace_steps.append([xx,yy])
 for xx in range(5,18):
  put(xx,7,0x70 if xx==5 else 0x72 if xx==17 else 0x71,True)
  put(xx,8,0x78 if xx==5 else 0x7a if xx==17 else 0x79,True)
 portals={'entrance':[49,16],'gym':[12,8]}
 for name,(cx,cy) in portals.items():
  for yy,row in enumerate([[0xa0,0xa1,0xa2],[0xa8,0xa9,0xaa]]):
   for xx,mid in enumerate(row):put(cx-1+xx,cy-1+yy,mid,not(xx==1 and yy==1))
  # Rock shoulders give the arch a proper cliff frame, not a freestanding hole.
  for xx in range(cx-3,cx+4):
   if xx not in range(cx-1,cx+2):
    put(xx,cy-1,0x71,True);put(xx,cy,0x79,True)
 # GYM plaque at native pixel size, perched on the cave landing.
 sign=Image.new('P',(16,16));sd=ImageDraw.Draw(sign);sd.rectangle((1,3,14,12),fill=2);sd.rectangle((2,4,13,10),fill=7);sd.rectangle((7,12,9,15),fill=3)
 glyph={'G':['111','100','101','101','111'],'Y':['101','101','010','010','010'],'M':['101','111','111','101','101']}
 for j,c in enumerate('GYM'):
  for yy,row in enumerate(glyph[c]):
   for xx,v in enumerate(row):
    if v=='1':sd.point((2+j*4+xx,5+yy),fill=2)
 labels['GymSign']=p.overlay(0x8,sign,9);put(13,10,labels['GymSign'],True)
 # Dense reef gardens follow the shelves instead of scattering identical dots.
 coral_ids=[]
 for kind in range(7):
  im=A.coral(kind if kind<6 else 3)
  pixels=[0 if v==3 else v for v in im.getdata()]
  if kind==6:pixels=[{9:1,10:2,11:4}.get(v,v) for v in pixels]
  im.putdata(pixels);coral_ids.append(p.overlay(0x115,im,12))
 reef=Image.new('P',(32,32));rd=ImageDraw.Draw(reef)
 rd.ellipse((1,18,30,31),fill=12);rd.ellipse((0,10,31,28),fill=5);rd.ellipse((1,8,30,25),fill=13)
 for x,y,rr,k in [(7,16,5,9),(19,16,6,5),(25,22,4,9),(14,23,5,5)]:
  rd.ellipse((x-rr,y-rr,x+rr,y+rr),fill=k+1,outline=k);rd.arc((x-rr+1,y-rr+1,x+rr-1,y+rr-1),180,300,fill=k+2,width=2)
 for pts in [[(9,18),(8,10),(5,6),(5,2)],[(8,12),(13,7),(13,3)],[(21,18),(23,10),(27,6),(27,2)],[(23,12),(20,7),(20,3)]]:
  rd.line(pts,fill=9,width=3);rd.line([(x-1,y) for x,y in pts],fill=11)
 heads=[[p.overlay(0x115,reef.crop((xx,yy,xx+16,yy+16)),12) for xx in (0,16)] for yy in (0,16)]
 coral_cells=set()
 for cx,cy in [(8,40),(12,42),(21,48),(25,51),(38,50),(43,52),(53,43)]:
  for yy in range(2):
   for xx in range(2):put(cx+xx,cy+yy,heads[yy][xx],True);coral_cells.add((cx+xx,cy+yy))
 for i,s in enumerate(shelves):
  for x,y in sorted(s):
   if (x,y) in coral_cells or (x,y) in decks or blocks[y*W+x]&1023!=0x115:continue
   if (x*5+y*3)%11<4 and all((x+dx,y+dy) in s for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]):
    put(x,y,coral_ids[(x+2*y)%7],True);coral_cells.add((x,y))
 # Tall palms stay on the cliff crowns. Lower palms flank the cave landings.
 palm=A.palm()
 for cx,cy in [(3,6),(18,5),(22,5),(34,4),(43,6),(53,8),(58,16)]:
  for yy in range(3):
   for xx in range(2):put(cx+xx,cy+yy,p.overlay(0x8,palm.crop((xx*16,yy*16,xx*16+16,yy*16+16)),8),True)
 # Seal the outer edge even to Surf. The only route warp out is the cave.
 for x,y in rect(0,0,W,H)-rect(1,1,W-2,H-2):blocks[y*W+x]|=0xc00
 landmarks={'entrance_approach':[49,17],'gym_approach':[12,9],**{b['name']+'_approach':[b['door'][0],b['door'][1]+1] for b in buildings},'reef_walk':[24,46],'lookout':[43,40]}
 warps=[b['door'] for b in buildings]+list(portals.values())
 seen=flood(blocks,W,H,landmarks['entrance_approach'],{tuple(v) for v in warps})
 for name,xy in landmarks.items():assert tuple(xy) in seen,('unreachable',name,xy)
 assert len(p.tiles)<=384 and len(p.metas)<=384,(len(p.tiles),len(p.metas))
 labels.update(DeckA=floors[0],DeckB=floors[1],**{f'Coral{i}':mid for i,mid in enumerate(coral_ids)})
 manifest=dict(design='cave-cove-v1',phase='LOW',dimensions=[W,H],tiles=len(p.tiles),metatiles=len(p.metas),buildings=buildings,portals=portals,landmarks=landmarks,permanent_decks=sorted(decks),walkable_cells=len(seen),shoreline={'generated_metatiles':sorted(set(shore.cache.values()))},tide_states={'installed':'low','runtime_switching':False},labels=labels)
 manifest['gym_terraces']={'tiers':terrace_specs,'stairs':terrace_steps}
 return p,blocks,manifest

def install(p,blocks,m):
 raw=struct.pack('<'+'H'*len(blocks),*blocks)
 m['result_sha256']=hashlib.sha256(raw).hexdigest()
 write(R/'data/layouts/Corvala_Town/map.bin',raw);write(R/'data/layouts/Corvala_Town/border.bin',struct.pack('<4H',*([0x1c00|0x12b]*4)))
 write(R/'tools/corvala/tide_states/low.bin',raw);write(R/'tools/corvala/map.json',m)
 im=Image.new('P',(128,((len(p.tiles)+15)//16)*8));im.putpalette(sum((list(c) for c in A.PALETTES[0]),[])+[0]*720)
 for i,t in enumerate(p.tiles):im.paste(Image.frombytes('P',(8,8),t),(i%16*8,i//16*8))
 im.save(D/'tiles.png');write(D/'metatiles.bin',struct.pack('<'+'H'*(len(p.metas)*8),*sum(p.metas,[])));write(D/'metatile_attributes.bin',struct.pack('<'+'I'*len(p.attrs),*p.attrs))
 for i,colors in enumerate(A.PALETTES,7):write(D/f'palettes/{i:02}.pal','JASC-PAL\n0100\n16\n'+'\n'.join(' '.join(map(str,c)) for c in colors)+'\n')
 labels=R/'include/constants/metatile_labels.h';s=labels.read_text()
 for marker in ['// Corvala raised walkway kit','// Corvala cave-cove kit']:
  if marker in s:s=s.split(marker)[0]+'#endif // GUARD_METATILE_LABELS_H\n'
 block='// Corvala cave-cove kit. Previous experimental IDs retired.\n'+''.join(f'#define METATILE_Corvala_{n:30} 0x{mid:03X}\n' for n,mid in m['labels'].items())+'\n'
 write(labels,s.replace('#endif // GUARD_METATILE_LABELS_H',block+'#endif // GUARD_METATILE_LABELS_H'))
 ls=read(R/'data/layouts/layouts.json');l=next(v for v in ls['layouts'] if v['id']=='LAYOUT_CORVALA_TOWN');l.update(width=W,height=H);write(R/'data/layouts/layouts.json',ls)
 write(R/'tools/corvala/manual-layout.json',{'design':'cave-cove-v1','generator_locked':True,'authoritative':'data/layouts/Corvala_Town/map.bin','generator':'tools/corvala/build_cove.py'})

def render():
 m=read(R/'tools/corvala/map.json');w,h=m['dimensions'];bs=words(R/'data/layouts/Corvala_Town/map.bin');tiles=atlas('corvala');im=Image.new('RGB',(w*16,h*16))
 for i,b in enumerate(bs):im.paste(tiles[b&1023],(i%w*16,i//w*16))
 for f in ['docs/corvala/low-tide-playable.png','build/corvala/Corvala_Low_Tide_Map.png']:
  path=R/f;path.parent.mkdir(parents=True,exist_ok=True);im.save(path)
 im.crop((128,224,864,752)).save(R/'docs/corvala/cove-village-detail.png')
 im.crop((64,96,352,400)).resize((576,608),Image.Resampling.NEAREST).save(R/'docs/corvala/terraced-gym-detail.png')
 print('Rendered actual packed map:',w,h)

if __name__=='__main__':
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--write',action='store_true');args=ap.parse_args()
 if args.write:
  old=read(R/'tools/corvala/map.json')
  if old.get('design')=='cave-cove-v1':assert hashlib.sha256((R/'data/layouts/Corvala_Town/map.bin').read_bytes()).hexdigest()==old['result_sha256'],'Manual edits detected; backport them before regenerating'
  p,blocks,m=build();install(p,blocks,m);print('Installed cove:',len(p.tiles),'tiles,',len(p.metas),'metatiles')
 render()
