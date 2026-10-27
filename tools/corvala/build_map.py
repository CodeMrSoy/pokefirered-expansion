#!/usr/bin/env python3
"""Build Corvala's first low-tide overworld; native GBA metatiles, not a painted backdrop.
Existing Emerald harbor cutouts are reused from Havora's checked-in source art.
Custom reef, sand, cliff and boardwalk pieces are drawn at native resolution.
"""
from pathlib import Path
import json,struct,sys,random
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'tools/havora'))
from render import atlas
S=R/'tools/havora/source_art/emerald_harbor'; D=R/'data/tilesets/secondary/corvala'
D.mkdir(parents=True,exist_ok=True);(D/'palettes').mkdir(exist_ok=True)
W,H=56,60
# Six material palettes. RGB values are reduced to the GBA's five-bit channels.
palettes=[]; tiles=[bytes(64)]; tile_lookup={bytes(64):0}; metas=[];attributes=[];meta_lookup={}; art={};kit={}
def register(im,bank,behavior=0):
    im=im.convert('RGB'); colors=palettes[bank-7]
    indices=bytes(min(range(1,16),key=lambda j:sum((c-v)**2 for c,v in zip(colors[j],rgb))) for rgb in im.getdata())
    desc=[]
    for ox,oy in [(0,0),(8,0),(0,8),(8,8)]:
        raw=bytes(indices[(oy+y)*16+ox+x] for y in range(8) for x in range(8))
        if raw not in tile_lookup:tile_lookup[raw]=len(tiles);tiles.append(raw)
        desc.append((640+tile_lookup[raw])|(bank<<12))
    key=tuple(desc)+(behavior,)
    if key not in meta_lookup:
        meta_lookup[key]=640+len(metas);metas.append(desc+[640]*4);attributes.append(behavior)
        art[meta_lookup[key]]=Image.frombytes('P',(16,16),indices);art[meta_lookup[key]].putpalette(sum((list(c) for c in colors),[])+[0]*720)
    return meta_lookup[key]
def add_palette(images):
    sheet=Image.new('RGB',(128,((sum(im.width*im.height for im in images)+127)//128+7)//8*8),(0,0,0)); pix=[]
    for im in images:pix.extend(im.convert('RGB').getdata())
    sheet.putdata(pix);q=sheet.quantize(colors=15,method=Image.Quantize.MEDIANCUT)
    cs=[tuple((v>>3)<<3 for v in q.getpalette()[i:i+3]) for i in range(0,45,3)]
    cs=[c for c in cs if len(c)==3];cs=(cs+[(0,0,0)]*15)[:15]
    palettes.append([(0,0,0)]+cs);return len(palettes)+6
def tile(bg):return Image.new('RGB',(16,16),bg)
# The sand and cliff kit uses consistent top-down lighting.
sand=tile('#e8d098');d=ImageDraw.Draw(sand)
for x,y in [(2,3),(11,9),(6,13)]:d.point((x,y),fill='#c8b080')
deep=tile('#3898b0');d=ImageDraw.Draw(deep)
for x,y in [(1,3),(9,11)]:d.line((x,y,x+4,y),fill='#58b8c0')
shallow=tile('#68c8c0');d=ImageDraw.Draw(shallow)
for x,y in [(1,3),(9,11)]:d.line((x,y,x+4,y),fill='#98e0d0')
deck=Image.open(S/'wood.png').convert('RGB')
cliff=tile('#786858');d=ImageDraw.Draw(cliff)
for box in [(1,1,8,6),(10,0,15,5),(0,8,5,14),(7,8,14,15)]:
 d.rounded_rectangle(box,radius=2,fill='#a89878',outline='#504848')
 d.line((box[0]+1,box[1]+1,box[2]-1,box[1]+1),fill='#c0b090')
grass=tile('#68a878');d=ImageDraw.Draw(grass)
for x,y in [(2,5),(10,12),(12,3)]:d.line((x,y,x+2,y-2),fill='#90c088')
reef=[]
for c,hi in [('#d878a0','#f0b0c8'),('#a890d0','#d0b8e8'),('#e8b868','#f8d898')]:
 im=shallow.copy();d=ImageDraw.Draw(im)
 for x,y in [(4,12),(11,13)]:
  d.line((x,y,x,y-9),fill=c,width=2);d.line((x,y-4,x-3,y-7),fill=c,width=2);d.line((x,y-5,x+3,y-8),fill=c,width=2);d.point((x,y-9),fill=hi)
 for x,y in [(2,5),(7,4),(12,7),(5,10)]:
  d.ellipse((x-1,y-2,x+2,y+1),fill=c);d.point((x,y-2),fill=hi)
 reef.append(im)
rock=Image.open(S/'rock.png').convert('RGBA');rockbg=shallow.convert('RGBA');rockbg.alpha_composite(rock)
materials=[sand,shallow,deck,grass,deep]
b=add_palette(materials)
for n,im in zip(['sand','shallows','deck','grass','sea'],materials):kit[n]=register(im,b)
b=add_palette([cliff]);kit['cliff']=register(cliff,b)
b=add_palette(reef+[rockbg])
for n,im in zip(['coral_pink','coral_lilac','coral_gold','rock'],reef+[rockbg]):kit[n]=register(im,b)
# Native harbor buildings keep the established game's pixel scale.
assets={n:Image.open(S/f'{n}.png').convert('RGBA') for n in ['house','warehouse','lighthouse','market_stall','planter','bollard']}
b=add_palette([im.convert('RGB') for im in assets.values()]+[deck])
for name,im in assets.items():
 rows=[]
 for y in range(0,im.height,16):
  row=[]
  for x in range(0,im.width,16):
   patch=deck.convert('RGBA');patch.alpha_composite(im.crop((x,y,x+16,y+16)));row.append(register(patch,b))
  rows.append(row)
 kit[name]=rows
# Railings and support posts are custom wood pieces, with water behind them.
rail=deck.copy();d=ImageDraw.Draw(rail);d.rectangle((0,1,15,3),fill='#684828');d.line((0,1,15,1),fill='#e8c080')
for x in [1,12]:d.rectangle((x,0,x+2,12),fill='#785030');d.point((x,0),fill='#e8c080')
post=shallow.copy();d=ImageDraw.Draw(post);d.rectangle((0,0,15,3),fill='#785030');d.rectangle((6,2,9,11),fill='#785030');d.line((6,3,6,10),fill='#c8a068')
b=add_palette([rail,deck,post]);kit['rail']=register(rail,b);kit['support']=register(post,b)
# Reuse the native FireRed Center, keeping its recognizable red roof and sign.
native=atlas('cinnabar_island','general')
# Center uses General's complete 5x4 exterior kit.
# Locate via source maps rather than guessing metatile indices.
layouts=json.loads((R/'data/layouts/layouts.json').read_text()); center=None
for l in layouts['layouts']:
 if l['id']=='LAYOUT_VERMILION_CITY':center=l
raw=struct.unpack('<'+'H'*(center['width']*center['height']),(R/center['blockdata_filepath']).read_bytes())
# Native Center kit in General; the map locates its doorway by warp destination.
vm=json.loads((R/'data/maps/VermilionCity/map.json').read_text());cw=next(w for w in vm['warp_events'] if 'POKEMON_CENTER' in w['dest_map'])
cx,cy=cw['x'],cw['y']; centerkit=[[raw[(cy-3+y)*center['width']+cx-2+x]&1023 for x in range(5)] for y in range(4)]
# Crop only the Center; adjacent street pieces are excluded.
centerkit[-1]=[0x60,0x61,0x62,0x63,0x64]
kit['center']=[row[:4] for row in centerkit]
# A walkable door using the standard warp behavior. No animation table is needed.
door=deck.copy();d=ImageDraw.Draw(door);d.rectangle((3,0,12,14),fill='#504038');d.rectangle((5,2,10,14),fill='#282830')
b=add_palette([door]);kit['door']=register(door,b,0x60)
# Compose permanent terrain, then the reef and raised town.
grid=[[kit['sea']|0x3400 for x in range(W)] for y in range(H)]
def put(x,y,mid,solid=False):grid[y][x]=mid|0x3000|(0x400 if solid else 0)
def rect(x,y,w,h,mid,solid=False):
 for yy in range(y,y+h):
  for xx in range(x,x+w):put(xx,yy,mid,solid)
# Upper headlands frame the protected bay; a north footpath is always open.
rect(0,0,W,8,kit['grass'],True);rect(9,0,5,14,kit['sand']);rect(0,8,8,17,kit['cliff'],True);rect(44,8,12,17,kit['cliff'],True)
rect(8,8,36,3,kit['cliff'],True);rect(9,8,5,3,kit['sand'])
# Northeast sea cave mouth (reserved until cave interiors are authored).
rect(46,10,6,4,kit['cliff'],True)
# Central sand shelf and broad southern reef, with curved island silhouettes.
for y in range(11,52):
 for x in range(8,48):
  if ((x-27)/23)**2+((y-30)/25)**2<1:put(x,y,kit['shallows'])
for y in range(12,38):
 for x in range(9,45):
  if ((x-27)/19)**2+((y-22)/16)**2<1:put(x,y,kit['sand'])
# Dedicated northern path joins the central island without entering water.
rect(10,9,3,14,kit['sand']);rect(12,17,7,4,kit['sand'])
rng=random.Random(174)
for cx,cy,rx,ry in [(9,41,5,4),(18,50,5,3),(30,44,5,4),(39,53,3,3),(45,39,3,3)]:
 for y in range(cy-ry,cy+ry+1):
  for x in range(cx-rx,cx+rx+1):
   if ((x-cx)/rx)**2+((y-cy)/ry)**2<=1:
    put(x,y,kit['sand'] if rng.random()<.38 else kit[['coral_pink','coral_lilac','coral_gold'][rng.randrange(3)]],True)
for x,y in [(16,40),(22,46),(35,52),(40,43),(6,35),(47,47)]:put(x,y,kit['rock'],True)
# Elevated town: wide platforms and four-tile connecting boardwalks.
platforms=[(9,18,12,12),(22,15,13,13),(36,19,10,11),(17,31,17,9),(40,36,10,9),(42,50,8,7)]
for x,y,w,h in platforms:
 rect(x,y,w,h,kit['deck']);rect(x,y,w,1,kit['rail'],True)
rect(18,25,24,4,kit['deck']);rect(25,25,4,11,kit['deck']);rect(30,35,14,4,kit['deck']);rect(43,28,4,25,kit['deck'])
# Match HarborRoad's two-tile path at y=11,12 using a permanent east approach.
rect(46,11,10,2,kit['sand']);rect(49,11,3,16,kit['sand']);rect(43,25,9,3,kit['deck'])
# Match CoastalRoad's bottom path at x=11,12.
# Exteriors stand on the permanent decks.
def place(name,x,y):
 for yy,row in enumerate(kit[name]):
  for xx,mid in enumerate(row):put(x+xx,y+yy,mid,True)
place('house',11,20);place('house',38,21);place('house',19,33);place('house',27,33);place('lighthouse',46,37)
# Center is rendered with its real General/Vermilion tiles and live warp.
place('center',24,17);put(26,20,0x62);rect(25,21,3,3,kit['deck'])
for x,y in [(16,23),(34,24),(42,32),(40,39),(20,38)]:place('planter',x,y)
place('market_stall',30,22)
# Cave entrance: dark mouth in a rocky frame and a low-tide approach.
rect(43,14,6,2,kit['sand']);rect(41,15,4,4,kit['sand']);put(46,12,0xa8,True);put(47,12,0xa8,True);put(46,13,0xa9,True);put(47,13,0xa9,True)
# A low-tide sandbar links the southern landing and reef rim.
rect(35,47,9,2,kit['sand']);rect(34,43,2,6,kit['sand'])
# Visible supports make the elevation of the boardwalk readable.
for y in range(H-1):
 for x in range(W):
  if grid[y][x]&1023==kit['deck'] and grid[y+1][x]&1023 in [kit['sea'],kit['shallows']] and x%3==0:put(x,y+1,kit['support'],True)
# Native coastal trees break up the northern headlands.
for x,y in [(1,1),(4,3),(17,1),(21,4),(27,2),(32,4),(38,1),(43,3),(49,1),(52,4)]:
 for yy,row in enumerate([[0x12,0x13],[0x1a,0x1b],[0x1c,0x1d]]):
  for xx,v in enumerate(row):put(x+xx,y+yy,v,True)
# Shorelines use foam and darker wet sand to explain tile boundaries.
shore_bank=7
edge_cache={}
for y in range(1,H-1):
 for x in range(1,W-1):
  mid=grid[y][x]&1023
  if mid!=kit['sand']:continue
  edges=tuple((grid[y+dy][x+dx]&1023) in [kit['sea'],kit['shallows']] for dx,dy in [(0,-1),(1,0),(0,1),(-1,0)])
  if not any(edges):continue
  if edges not in edge_cache:
   im=sand.copy();d=ImageDraw.Draw(im)
   for yes,box in zip(edges,[(0,0,15,1),(14,0,15,15),(0,14,15,15),(0,0,1,15)]):
    if yes:d.rectangle(box,fill='#b0d8c0')
   edge_cache[edges]=register(im,shore_bank)
  put(x,y,edge_cache[edges],bool(grid[y][x]&0x400))

assert len(tiles)<=384,(len(tiles),'secondary graphic capacity exceeded')
assert len(metas)<=384
for bank in range(16):
 colors=palettes[bank-7] if 7<=bank<7+len(palettes) else [(0,0,0)]*16
 (D/'palettes'/f'{bank:02}.pal').write_text('JASC-PAL\n0100\n16\n'+'\n'.join(' '.join(map(str,c)) for c in colors)+'\n')
sheet=Image.new('P',(128,((len(tiles)+15)//16)*8));sheet.putpalette(sum((list(c) for c in palettes[0]),[])+[0]*720)
for i,t in enumerate(tiles):sheet.paste(Image.frombytes('P',(8,8),t),(i%16*8,i//16*8))
sheet.save(D/'tiles.png');(D/'metatiles.bin').write_bytes(struct.pack('<'+'H'*len(metas)*8,*sum(metas,[])));(D/'metatile_attributes.bin').write_bytes(struct.pack('<'+'I'*len(attributes),*attributes))

# Build preview from the exact packed metatiles.
for y,row in enumerate(grid):
 for x,v in enumerate(row):
  if v&1023<640:art[v&1023]=native[v&1023]
preview=Image.new('RGB',(W*16,H*16))
for y,row in enumerate(grid):
 for x,v in enumerate(row):preview.paste(art[v&1023],(x*16,y*16))
B=R/'build/corvala';B.mkdir(parents=True,exist_ok=True);preview.save(B/'Corvala_Low_Tide_Map.png')
l=next(l for l in layouts['layouts'] if l['id']=='LAYOUT_CORVALA_TOWN');l.update(width=W,height=H,secondary_tileset='gTileset_Corvala')
(R/'data/layouts/layouts.json').write_text(json.dumps(layouts,indent=2)+'\n')
(R/l['blockdata_filepath']).write_bytes(struct.pack('<'+'H'*W*H,*sum(grid,[])))
(R/l['border_filepath']).write_bytes(struct.pack('<4H',*[kit['sea']|0x3400]*4))
mp=R/'data/maps/Corvala_Town/map.json';m=json.loads(mp.read_text());m['warp_events'][0].update(x=26,y=20,elevation=3);mp.write_text(json.dumps(m,indent=2)+'\n')
manifest={'phase':'first low-tide map; tide controller and interiors pending','dimensions':[W,H],'tiles':len(tiles),'metatiles':len(metas),'palette_banks':len(palettes),'kit':kit,'center_warp':[26,20],'always_open_exits':{'north':[[11,0],[12,0]],'east':[[55,11],[55,12]]},'source_art':'tools/havora/source_art/emerald_harbor/provenance.json'}
(R/'tools/corvala/map.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(f'Corvala: {W}x{H}, {len(tiles)}/384 graphics, {len(metas)}/384 metatiles')
