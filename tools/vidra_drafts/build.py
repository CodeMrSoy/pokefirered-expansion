#!/usr/bin/env python3
"""Authored Vidra blockouts. Explicit opt-in; never invoked by make.

Backport manual Porymap edits before rerunning. All cells are native metatiles.
The draft group is appended so existing map numbers and campaign maps survive.
"""
from pathlib import Path
import json, math, random, struct, sys
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools/havora'))
from render import atlas

def read(path): return json.loads((ROOT/path).read_text())
def write(path, value):
    p=ROOT/path; p.parent.mkdir(parents=True,exist_ok=True)
    data=(json.dumps(value,indent=2,ensure_ascii=False)+'\n').encode() if not isinstance(value,(str,bytes)) else value.encode() if isinstance(value,str) else value
    if not p.exists() or p.read_bytes()!=data: p.write_bytes(data)
def words(path):
    b=(ROOT/path).read_bytes(); return list(struct.unpack('<'+'H'*(len(b)//2),b))
def binary(a): return struct.pack('<'+'H'*len(a),*a)
def rect(x,y,w,h): return {(xx,yy) for yy in range(y,y+h) for xx in range(x,x+w)}
def line(points,width=3):
    out=set()
    for (ax,ay),(bx,by) in zip(points,points[1:]):
        n=max(abs(ax-bx),abs(ay-by))
        for i in range(n+1):
            x=round(ax+(bx-ax)*i/max(1,n));y=round(ay+(by-ay)*i/max(1,n))
            out |= rect(x-width//2,y-width//2,width,width)
    return out
def ellipse(cx,cy,rx,ry):
    return {(x,y) for y in range(int(cy-ry),int(cy+ry+1)) for x in range(int(cx-rx),int(cx+rx+1)) if ((x-cx)/rx)**2+((y-cy)/ry)**2<=1}

ALL=[]
class Map:
    def __init__(self,key,title,w,h,secondary='sevii_islands_123',primary='general',kind='ROUTE',weather='SUNNY'):
        self.key=key;self.name='VidraDraft_'+key;self.id='MAP_VIDRA_DRAFT_'+key.upper()
        self.title=title;self.w=w;self.h=h;self.primary=primary;self.secondary=secondary
        self.a=[[0x3001 for _ in range(w)]for _ in range(h)]
        self.header=dict(id=self.id,name=self.name,layout='LAYOUT_VIDRA_DRAFT_'+key.upper(),music='MUS_SEVII_123',region_map_section='MAPSEC_VIDRA_DRAFT_'+key.upper(),requires_flash=False,weather='WEATHER_'+weather,map_type='MAP_TYPE_'+kind,allow_cycling=False,allow_escaping=False,allow_running=True,show_map_name=True,floor_number=0,battle_scene='MAP_BATTLE_SCENE_NORMAL',connections=[],object_events=[],warp_events=[],coord_events=[],bg_events=[])
        self.points={};self.scripts=[];ALL.append(self)
        self.trees=[]
    def put(self,x,y,t,z=3,solid=False):
        if 0<=x<self.w and 0<=y<self.h:self.a[y][x]=t|(z<<12)|(0x400 if solid else 0)
    def paint(self,cells,t,z=3,solid=False):
        for x,y in cells:self.put(x,y,t,z,solid)
    def box(self,x,y,w,h,t,z=3,solid=False):self.paint(rect(x,y,w,h),t,z,solid)
    def path(self,points,width=3,t=0xd9,z=3):self.paint(line(points,width),t,z)
    def patch(self,grid,x,y,z=3,solid=True):
        for dy,row in enumerate(grid):
            for dx,t in enumerate(row):self.put(x+dx,y+dy,t,z,solid)
    def tree(self,x,y):
        self.trees.append((x,y));self.patch([[0xe,0xf],[0x1c,0x1d],[0x24,0x25]],x,y)
    def woods(self,clear,seed=0):
        rng=random.Random(seed)
        for y in range(0,self.h-2,2):
            for x in range((y//2%2),self.w-1,2):
                area=rect(x,y,2,3)
                if not area & clear:self.tree(x,y)
        # Scattered leaf litter and flowers; no obstruction of authored corridors.
        for _ in range(self.w*self.h//32):
            x=rng.randrange(2,self.w-2);y=rng.randrange(2,self.h-2)
            if (x,y) in clear and self.a[y][x]&0x3ff==1:self.put(x,y,4 if rng.random()<.2 else 0xb)
    def boundary(self):
        for x,y in rect(0,0,self.w,2)|rect(0,self.h-2,self.w,2)|rect(0,0,2,self.h)|rect(self.w-2,0,2,self.h):self.put(x,y,5,solid=True)
    def shore(self,cells):
        # Select native coast pieces by their actual blue/land pixel silhouette.
        # This avoids assuming that adjacent metatile IDs form an autotile set.
        for x,y in cells:
            l=(x-1,y)not in cells;r=(x+1,y)not in cells;u=(x,y-1)not in cells;d=(x,y+1)not in cells
            t=BANKS[(l,r,u,d)] if self.key!='CorvalaPassage' else 0x1e0
            self.put(x,y,t,z=1,solid=True)
    def cliff(self,y,stairs,zup=4,zdown=3,left=2,right=None):
        right=right or self.w-2
        self.box(left,y,right-left,1,0x87,zup,True);self.box(left,y+1,right-left,1,0x79,zdown,True)
        for x in stairs:
            self.box(x-1,y,3,1,0x89,0);self.box(x-1,y+1,3,1,0x91,0)
    def sign(self,x,y,text):
        label=self.name+'_Sign'+str(len(self.header['bg_events']))
        self.put(x,y,3,solid=True)
        self.header['bg_events'].append(dict(type='sign',x=x,y=y,elevation=3,player_facing_dir='BG_EVENT_PLAYER_FACING_ANY',script=label))
        self.scripts.append(f'{label}::\n\tmsgbox {label}_Text, MSGBOX_SIGN\n\tend\n\n{label}_Text::\n\t.string "{text}$"\n')
    def trigger(self,x,y,label,z=3):
        self.header['coord_events'].append(dict(type='trigger',x=x,y=y,elevation=z,var='VAR_TEMP_0',var_value='0',script=label))
    def portal(self,x,y,dest,dx,dy,z=3):
        label=self.name+'_Travel'+str(len(self.header['coord_events']))
        self.trigger(x,y,label,z)
        self.scripts.append(f'{label}::\n\tlockall\n\twarp {dest}, 255, {dx}, {dy}\n\twaitstate\n\treleaseall\n\tend\n')
    def point(self,k,x,y):self.points[k]=[x,y]

def connect(a,direction,b,offset=0):
    rev={'up':'down','down':'up','left':'right','right':'left'}
    a.header['connections'].append(dict(map=b.id,direction=direction,offset=offset))
    b.header['connections'].append(dict(map=a.id,direction=rev[direction],offset=-offset))

def house(m,x,y,w=5,roof='blue',kind='home'):
    # Reusable native General building pieces; interiors are deliberately pending.
    a,b,c,d=(0x48,0x49,0x4a,0x4b) if roof=='red' else (0x28,0x29,0x2a,0x2b)
    m.patch([[a]+[b]*(w-2)+[d],[a+8]+[b+8]*(w-2)+[d+8],[0x44]+[0x45]*(w-2)+[0x46],[0x54]+[0x55]*(w-2)+[0x56]],x,y)
    door=x+w//2;m.put(door,y+3,0x3d,solid=True)
    # Door inspection clearly explains the status instead of a broken doorway.
    label=m.name+'_Door'+str(len(m.header['bg_events']))
    text={'center':'POKEMON CENTER site.\\nInterior planned for the next pass.','gym':'GYM site.\\nPuzzle and leader come later.','mart':'MART site.\\nInterior planned for the next pass.','home':'A village home.\\nInterior planned for the next pass.'}[kind]
    m.header['bg_events'].append(dict(type='sign',x=door,y=y+3,elevation=3,player_facing_dir='BG_EVENT_PLAYER_FACING_ANY',script=label))
    m.scripts.append(f'{label}::\n\tmsgbox {label}_Text, MSGBOX_SIGN\n\tend\n\n{label}_Text::\n\t.string "{text}$"\n')
    if kind=='center':m.put(x,y+2,0x60,solid=True)
    if kind=='mart':m.put(x,y+2,0x40,solid=True)
    if kind=='gym':m.put(x-1,y+3,0x168,solid=True)
    m.point(kind+str(x),door,y+4)
    return door,y+4

def forest():
    m=Map('WesternForest','WESTERN FOREST',88,80,'viridian_forest')
    # Deliberately authored junction graph: two destination branches, loops and dead ends.
    trails=[[(80,75),(80,66),(67,66),(67,54),(55,54),(55,43),(43,43),(43,31),(31,31),(31,19),(19,19),(19,14),(8,14)],
      [(43,43),(43,55),(31,55),(31,67),(19,67),(19,55),(8,55),(8,42),(19,42),(19,31),(31,31)],
      [(55,43),(67,43),(67,31),(79,31),(79,19),(67,19),(67,7),(60,7),(60,0)],
      [(31,19),(43,19),(43,7),(55,7),(55,19),(67,19)],
      [(19,31),(8,31),(8,23)],[(31,67),(43,67),(43,73)],
      [(67,54),(79,54),(79,43)],[(19,67),(8,67),(8,73)],[(43,31),(55,31),(55,24)],
      [(31,55),(31,43)],[(55,54),(55,66),(60,66)]]
    clear=set().union(*(line(p,6) for p in trails))|ellipse(43,43,8,7)|ellipse(17,56,8,6)|ellipse(66,19,8,7)|rect(3,9,12,10)
    m.woods(clear,1)
    for p in trails:m.path(p,3)
    m.paint(ellipse(43,43,6,5),1);m.path([(43,37),(43,49)],3);m.path([(37,43),(49,43)],3)
    m.shore(ellipse(16,57,4,3));m.path([(8,55),(8,62),(20,62)],3)
    # Ancient-tree clearing uses the larger native Viridian Forest tree.
    m.patch([[0x14,0x15,0x16,0x17],[0x1a,0x1b,0x1e,0x1f],[0x24,0x25,0x26,0x27]],64,16)
    m.patch([[0xa0,0xa1,0xa2],[0xa8,0xa9,0xaa]],7,13);m.put(8,14,0xa9)
    m.sign(76,71,'HAVORA lies beyond the grove.\\nThe forest splits farther inside.')
    m.sign(41,40,'WEST: CORVALA PASSAGE\\nNORTH: RAINFALL ROUTE')
    m.point('havora',80,74);m.point('cave',8,15);m.point('rain',60,2);m.point('clearing',43,43)
    return m

def cave():
    m=Map('CorvalaPassage','CORVALA PASSAGE',56,48,'vidra_draft_cave',kind='UNDERGROUND',weather='NONE')
    m.box(0,0,m.w,m.h,0x28c,solid=True)
    paths=[[(49,38),(42,38),(42,29),(31,29),(31,17),(20,17),(20,9),(8,9)],[(31,29),(21,29),(21,38),(9,38),(9,30)],[(31,17),(43,17),(43,8),(49,8)],[(20,17),(9,17),(9,23)]]
    floor=set().union(*(line(p,5)for p in paths))|ellipse(31,29,8,5)|ellipse(20,17,7,5)
    m.paint(floor,0x281)
    for x,y in floor:
        if (x,y-1)not in floor:m.put(x,y-1,0x291,solid=True)
        if (x,y+1)not in floor:m.put(x,y+1,0x289,solid=True)
    m.shore(ellipse(12,38,3,2))
    for x,y in [(38,27),(24,15),(47,8),(7,29),(19,37)]:m.put(x,y,0x282,solid=True)
    m.put(8,8,0x2c9);m.put(49,39,0x2c9)
    m.point('forest',49,37);m.point('corvala',8,10)
    return m

def rainfall():
    m=Map('RainfallRoute','RAINFALL ROUTE',56,72,'vidra_draft_rain',weather='RAIN')
    trails=[[(24,71),(24,65),(12,65),(12,54),(41,54),(41,34),(14,34),(14,14),(24,14),(24,0)],[(14,34),(7,34),(7,24)],[(41,54),(49,54),(49,63)]]
    clear=set().union(*(line(p,8)for p in trails))|rect(25,2,10,68)
    m.woods(clear,3)
    for p in trails:m.path(p,3)
    # River with three native animated waterfall curtains and three footbridges.
    river={(x,y)for y in range(2,70)for x in range(27+(y//17%2),34+(y//17%2))}
    m.shore(river)
    for yy in [18,38,58]:
        m.cliff(yy,[],left=3,right=53)
        for dy in range(3):
            for dx in range(6):m.put(28+dx,yy+dy,640+dy*4+(0 if dx==0 else 3 if dx==5 else 1+(dx%2)),z=1,solid=True)
        # Stair paths on alternating banks remain continuous on foot.
        sx=14 if yy==18 else 41 if yy==38 else 12
        m.box(sx-1,yy,3,1,0x89,0);m.box(sx-1,yy+1,3,1,0x91,0)
    for y in [14,34,54]:
        m.box(26,y-1,10,3,0x1c6);m.box(26,y-2,10,1,0xe8,solid=True);m.box(26,y+2,10,1,0xe8,solid=True)
    # Cliffs are two-cell rock ribbons with stairs at the actual path crossings.
    m.sign(20,65,'RAINFALL ROUTE\\nNorth to VEYDEN.')
    m.point('south',24,69);m.point('north',24,2);m.point('falls',40,35)
    return m

def veyden():
    m=Map('Veyden','VEYDEN',56,48,kind='TOWN')
    clear=rect(7,7,42,34)|line([(24,47),(24,0)],8)|line([(24,20),(55,20)],8)
    m.woods(clear,5)
    m.path([(24,47),(24,0)],4,t=0x1c6);m.path([(8,20),(55,20)],4,t=0x1c6)
    m.path([(10,34),(44,34),(44,9),(10,9),(10,34)],3,t=0x1c6)
    for x,y,k in [(9,12,'home'),(36,11,'home'),(8,27,'center'),(36,27,'mart'),(22,7,'gym'),(20,35,'home'),(39,35,'home')]:house(m,x,y,roof='red'if k=='center'else'blue',kind=k)
    # Central grove island, with paths on every side.
    for x,y in [(23,17),(25,17),(23,19),(25,19)]:m.tree(x,y)
    m.path([(19,16),(19,26),(31,26),(31,16)],3,t=0x1c6)
    m.path([(19,16),(31,16)],3,t=0x1c6)
    for x,y in [(15,39),(46,24),(8,8),(33,37)]:m.tree(x,y)
    m.sign(29,29,'VEYDEN\\nEast: LYRVIK / North: NORVYN')
    m.point('south',24,45);m.point('east',53,20);m.point('north',24,2);m.point('square',20,25)
    return m

def lake_route():
    m=Map('LakewoodRoute','LAKEWOOD ROUTE',64,40)
    trails=[[(0,20),(10,20),(10,12),(25,12),(25,20),(41,20),(41,12),(54,12),(54,20),(63,20)],[(10,20),(10,29),(24,29),(24,21)],[(25,12),(25,6),(36,6)]]
    clear=set().union(*(line(p,7)for p in trails))|ellipse(45,30,17,12)
    m.woods(clear,9)
    for p in trails:m.path(p,3)
    m.shore(ellipse(46,31,15,9));m.paint(ellipse(46,31,3,2),1,solid=True);m.tree(45,29)
    for x,y in [(16,6),(34,9),(16,27),(57,25)]:m.box(x,y,4,3,0x12)
    m.sign(5,23,'WEST: VEYDEN\\nEAST: LYRVIK')
    m.point('west',2,20);m.point('east',61,20);m.point('lake',40,19)
    return m

def lyrvik():
    m=Map('Lyrvik','LYRVIK TOWN',56,48,kind='TOWN')
    m.woods(rect(5,8,47,29)|line([(0,20),(50,20)],8),12)
    water={(x,y)for y in range(30,48)for x in range(3,56)}|ellipse(50,26,9,11)
    m.shore(water)
    m.path([(0,20),(39,20),(39,28),(10,28),(10,12),(40,12)],4,t=0x1c6)
    for x,y,k in [(8,12,'center'),(24,12,'mart'),(38,10,'gym'),(8,23,'home'),(24,23,'home')]:house(m,x,y,roof='red'if k=='center'else'blue',kind=k)
    m.box(17,29,3,13,0x1c6);m.box(16,40,8,2,0x1c6);m.box(35,29,3,9,0x1c6)
    for x in [16,20,34,38]:m.box(x,31,1,5,0xe8,z=1,solid=True)
    m.sign(5,23,'LYRVIK TOWN\\nA quiet home beside the lake.')
    m.point('west',2,20);m.point('pier',18,39);m.point('square',22,20)
    return m

def ascent():
    m=Map('HighlandAscent','HIGHLAND ASCENT',56,72,'vidra_draft_highlands')
    trails=[[(24,71),(24,64),(12,64),(12,51),(43,51),(43,36),(13,36),(13,20),(39,20),(39,8),(24,8),(24,0)],[(43,51),(49,51),(49,59)],[(13,36),(7,36),(7,29)],[(39,20),(48,20),(48,14)]]
    clear=set().union(*(line(p,8)for p in trails))
    m.woods(clear,7)
    for p in trails:m.path(p,3)
    for y,stairs in [(57,[12]),(42,[43]),(27,[13]),(13,[39])]:
        m.cliff(y,stairs)
    # Snow uses native GeneralWinter metatiles copied into a secondary bank.
    treecells=set().union(*(rect(x,y,2,3)for x,y in m.trees))
    for y in range(0,32):
        for x in range(m.w):
            w=m.a[y][x];mid=w&1023
            if (x,y)not in treecells and y<25+round(3*math.sin(x/8)):
                if mid in SNOW_IDS:m.a[y][x]=(w&~1023)|SNOW_IDS[mid]
    # Convert a whole tree at a time so snow never cuts individual canopies in half.
    # Neighboring tree rows overlap; the final stamp owns each cell consistently.
    for x,y in m.trees:
        snowy=y+1<25+round(3*math.sin(x/8))
        grid=[[0xe,0xf],[0x1c,0x1d],[0x24,0x25]]
        if snowy:grid=[[SNOW_IDS[t]for t in row]for row in grid]
        m.patch(grid,x,y)
    m.sign(20,65,'HIGHLAND ASCENT\\nThe trail climbs toward NORVYN.')
    m.point('south',24,69);m.point('north',24,2);m.point('snowline',39,23)
    return m

def norvyn():
    m=Map('Norvyn','NORVYN TOWN',56,48,'sevii_islands_123winter','general_winter',kind='TOWN',weather='SNOW')
    clear=rect(6,6,44,35)|line([(24,47),(24,5)],8)
    m.woods(clear,8)
    m.path([(24,47),(24,8)],4,t=0x1c6);m.path([(9,18),(45,18)],4,t=0x1c6);m.path([(10,34),(45,34)],4,t=0x1c6)
    m.cliff(24,[24]);m.path([(24,26),(24,33)],3,t=0x1c6)
    for x,y,k in [(9,10,'home'),(35,10,'home'),(22,6,'gym'),(8,27,'center'),(35,27,'mart'),(10,36,'home'),(37,36,'home')]:house(m,x,y,roof='red'if k=='center'else'blue',kind=k)
    m.sign(28,40,'NORVYN TOWN\\nShelter beneath the frozen peaks.')
    m.point('south',24,45);m.point('square',24,19)
    return m

SNOW_IDS={}
def highland_tileset():
    base=ROOT/'data/tilesets/primary/general';snow=ROOT/'data/tilesets/primary/general_winter'
    selected=[1,4,5,0xb,0xc,0xd,0xe,0xf,0x12,0x13,0x14,0x15,0x16,0x17,0x1a,0x1b,0x1c,0x1d,0x22,0x23,0x24,0x25,0x26,0x27,0x68,0x69,0x6a,0x79,0x87,0x89,0x91,0xd9]
    source=words('data/tilesets/primary/general_winter/metatiles.bin');attrs=(snow/'metatile_attributes.bin').read_bytes();m=[];a=bytearray()
    banks=sorted({v>>12 for mid in selected for v in source[mid*8:mid*8+8]});assert len(banks)<=6
    mapping={p:7+i for i,p in enumerate(banks)}
    folder='data/tilesets/secondary/vidra_draft_highlands'
    for i,mid in enumerate(selected):
        SNOW_IDS[mid]=640+i;m.extend((v&4095)|(mapping[v>>12]<<12)for v in source[mid*8:mid*8+8]);a.extend(attrs[mid*4:mid*4+4])
    write(folder+'/metatiles.bin',binary(m));write(folder+'/metatile_attributes.bin',bytes(a))
    for i in range(16):
        original=next((p for p,n in mapping.items()if n==i),0)
        write(folder+f'/palettes/{i:02}.pal',(snow/f'palettes/{original:02}.pal').read_bytes())
    # Tiles reference the already loaded primary tiles exclusively.
    write(folder+'/tiles.png',(ROOT/'data/tilesets/secondary/dummy_1/tiles.png').read_bytes())
    return folder

def register_tileset(symbol,folder):
    # Native assets; no generated illustration is used in the game.
    g=f'\nconst u32 gTilesetTiles_{symbol}[] = INCBIN_U32("{folder}/tiles.4bpp.lz");\nconst u16 gTilesetPalettes_{symbol}[][16] = {{\n'+''.join(f'    INCBIN_U16("{folder}/palettes/{i:02}.gbapal"),\n'for i in range(16))+'};\n'
    mt=f'\nconst u16 gMetatiles_{symbol}[] = INCBIN_U16("{folder}/metatiles.bin");\nconst u32 gMetatileAttributes_{symbol}[] = INCBIN_U32("{folder}/metatile_attributes.bin");\n'
    h=f'\nconst struct Tileset gTileset_{symbol} = {{\n    .isCompressed = TRUE,\n    .isSecondary = TRUE,\n    .tiles = gTilesetTiles_{symbol},\n    .palettes = gTilesetPalettes_{symbol},\n    .metatiles = gMetatiles_{symbol},\n    .metatileAttributes = gMetatileAttributes_{symbol},\n    .callback = NULL,\n}};\n'
    for path,s in [('graphics',g),('metatiles',mt),('headers',h)]:
        p=f'src/data/tilesets/{path}.h';old=(ROOT/p).read_text()
        if symbol not in old:write(p,old+s)

BANKS={}
def coast_pieces():
    import itertools
    ims=atlas('sevii_islands_123')
    def water(c):r,g,b=c;return b>r*1.18 and b>g*.98
    candidates=[]
    for mid in range(0x100,0x280):
        colors=list(ims[mid].get_flattened_data());mask=[water(c)for c in colors]
        if sum(mask)<40:continue
        bad=sum(not water(c)and not(c[0]>140 and c[1]>125 and c[2]<210)and not(c[1]>c[0]*1.1 and c[1]>c[2]) for c in colors)
        candidates.append((mid,mask,bad))
    for l,r,u,d in itertools.product([False,True],repeat=4):
        expected=[not((l and x<3)or(r and x>12)or(u and y<3)or(d and y>12))for y in range(16)for x in range(16)]
        BANKS[(l,r,u,d)]=min(candidates,key=lambda v:sum(a!=b for a,b in zip(v[1],expected))+v[2]*2)[0] if any([l,r,u,d])else 0x1e0

def rain_tileset():
    im=Image.open(ROOT/'tools/vidra_drafts/reference/waterfall.png').convert('RGB')
    colors=[(0,0,0)]+sorted(set(im.get_flattened_data()));assert len(colors)<=16
    pal=colors+[(0,0,0)]*(16-len(colors));ids=[];tiles=[bytes(64)];lookup={tiles[0]:0}
    for y in range(3):
        for x in range(4):
            meta=[]
            for dy,dx in [(0,0),(0,8),(8,0),(8,8)]:
                b=bytes(colors.index(im.getpixel((x*16+dx+xx,y*16+dy+yy)))for yy in range(8)for xx in range(8))
                if b not in lookup:lookup[b]=len(tiles);tiles.append(b)
                meta.append(0x7000|640|lookup[b])
            ids.extend(meta+[0x7000|640]*4)
    sheet=Image.new('P',(128,math.ceil(len(tiles)/16)*8));sheet.putpalette([v for c in pal for v in c]+[0]*(768-48))
    for i,b in enumerate(tiles):
        t=Image.frombytes('P',(8,8),b);sheet.paste(t,((i%16)*8,(i//16)*8))
    folder='data/tilesets/secondary/vidra_draft_rain';(ROOT/folder).mkdir(parents=True,exist_ok=True);sheet.save(ROOT/folder/'tiles.png')
    write(folder+'/metatiles.bin',binary(ids));write(folder+'/metatile_attributes.bin',struct.pack('<12I',*([0x20000013]*12)))
    for i in range(16):write(folder+f'/palettes/{i:02}.pal','JASC-PAL\n0100\n16\n'+'\n'.join(' '.join(map(str,c))for c in pal)+'\n')
    register_tileset('VidraDraftRain',folder)

def cave_tileset():
    folder='data/tilesets/secondary/vidra_draft_cave'
    for p in (ROOT/'data/tilesets/secondary/cave').rglob('*'):
        if p.is_file()and p.suffix in ['.png','.pal','.bin']:write(folder+'/'+str(p.relative_to(ROOT/'data/tilesets/secondary/cave')),p.read_bytes())
    p=ROOT/folder/'metatile_attributes.bin';b=bytearray(p.read_bytes());old=struct.unpack_from('<I',b,(0x2c9-640)*4)[0];struct.pack_into('<I',b,(0x2c9-640)*4,(old&~0x1ff)|0x60);write(folder+'/metatile_attributes.bin',bytes(b))
    register_tileset('VidraDraftCave',folder)

def corvala():
    # Snapshot of Corvala-dev's authored LOW layout; original branch stays intact.
    ref=ROOT/'tools/vidra_drafts/reference/corvala'
    folder='data/tilesets/secondary/vidra_draft_corvala'
    for p in ref.rglob('*'):
        if p.is_file()and p.name not in ['map.bin','provenance.json']:write(folder+'/'+str(p.relative_to(ref)),p.read_bytes())
    register_tileset('VidraDraftCorvala',folder)
    m=Map('Corvala','CORVALA TOWN',64,64,'vidra_draft_corvala',kind='TOWN')
    a=words('tools/vidra_drafts/reference/corvala/map.bin');assert len(a)==64*64
    m.a=[a[y*64:(y+1)*64]for y in range(64)]
    # Draft cave connection is placed at an existing native cave mouth.
    cavecells=[(x,y)for y,row in enumerate(m.a)for x,v in enumerate(row)if v&1023==0xa9]
    if not cavecells:raise ValueError('Corvala reference no longer has its native cave mouth')
    m.point('cave',*cavecells[0]);m.point('village',26,22)
    return m

def main():
    coast_pieces();rain_tileset();cave_tileset()
    highland_tileset();register_tileset('VidraDraftHighlands','data/tilesets/secondary/vidra_draft_highlands')
    f=forest();c=cave();r=rainfall();v=veyden();l=lake_route();t=lyrvik();a=ascent();n=norvyn();co=corvala()
    connect(f,'up',r,36);connect(r,'up',v);connect(v,'right',l);connect(l,'right',t);connect(v,'up',a);connect(a,'up',n)
    # Cave doors use native warp behavior and real, reciprocal map events.
    f.header['warp_events']=[dict(x=8,y=14,elevation=3,dest_map=c.id,dest_warp_id='0')]
    c.header['warp_events']=[dict(x=49,y=39,elevation=3,dest_map=f.id,dest_warp_id='0'),dict(x=8,y=8,elevation=3,dest_map=co.id,dest_warp_id='0')]
    cx,cy=co.points['cave'];co.header['warp_events']=[dict(x=cx,y=cy,elevation=(co.a[cy][cx]>>12),dest_map=c.id,dest_warp_id='1')]
    co.a[cy][cx]&=~0x400
    f.portal(80,76,'MAP_HAVORA_NORTH_QUADRANT',10,12)
    # Access is behind the existing puzzle gate, at the end of its walkable lane.
    havora=read('data/maps/Havora_NorthQuadrant/map.json')
    label='VidraDraft_EnterForest'
    havora['coord_events']=[e for e in havora['coord_events']if e.get('script')!=label]
    havora['coord_events'].append(dict(type='trigger',x=10,y=10,elevation=6,var='VAR_TEMP_0',var_value='0',script=label))
    write('data/maps/Havora_NorthQuadrant/map.json',havora)
    scripts=f'{label}::\n\tlockall\n\twarp {f.id}, 255, 80, 74\n\twaitstate\n\treleaseall\n\tend\n\n'
    groups=read('data/maps/map_groups.json');group='gMapGroup_VidraDrafts'
    if group not in groups['group_order']:groups['group_order'].append(group)
    groups[group]=[m.name for m in ALL]
    layouts=read('data/layouts/layouts.json');layouts['layouts']=[l for l in layouts['layouts']if not l['id'].startswith('LAYOUT_VIDRA_DRAFT_')]
    sections=read('src/data/region_map/region_map_sections.json');sections['map_sections']=[s for s in sections['map_sections']if not s['id'].startswith('MAPSEC_VIDRA_DRAFT_')]
    symbols={'general':'General','general_winter':'GeneralWinter','viridian_forest':'ViridianForest','cave':'Cave','sevii_islands_123':'SeviiIslands123','sevii_islands_123winter':'SeviiIslands123Winter','vidra_draft_highlands':'VidraDraftHighlands','vidra_draft_corvala':'VidraDraftCorvala','vidra_draft_cave':'VidraDraftCave','vidra_draft_rain':'VidraDraftRain'}
    report=[]
    for m in ALL:
        p='data/layouts/'+m.name
        write(p+'/map.bin',binary([v for row in m.a for v in row]));write(p+'/border.bin',binary([0x3405]*4))
        layouts['layouts'].append(dict(id=m.header['layout'],name=m.name+'_Layout',width=m.w,height=m.h,border_width=2,border_height=2,primary_tileset='gTileset_'+symbols[m.primary],secondary_tileset='gTileset_'+symbols[m.secondary],border_filepath=p+'/border.bin',blockdata_filepath=p+'/map.bin'))
        sections['map_sections'].append(dict(id=m.header['region_map_section'],name=m.title,x=9,y=7,width=1,height=1))
        write('data/maps/'+m.name+'/map.json',m.header)
        scripts+=f'{m.name}_MapScripts::\n\t.byte 0\n\n'+ '\n'.join(m.scripts)+'\n'
        ims=atlas(m.secondary,m.primary);im=Image.new('RGB',(m.w*16,m.h*16))
        for y,row in enumerate(m.a):
            for x,w in enumerate(row):im.paste(ims[w&1023],(x*16,y*16))
        out=ROOT/'docs/vidra/drafts'/f'{m.key}.png';out.parent.mkdir(parents=True,exist_ok=True);im.save(out)
        report.append(dict(map=m.name,title=m.title,width=m.w,height=m.h,points=m.points,preview=str(out.relative_to(ROOT))))
    write('data/maps/map_groups.json',groups);write('data/layouts/layouts.json',layouts);write('src/data/region_map/region_map_sections.json',sections)
    write('data/scripts/vidra_drafts.inc',scripts.rstrip()+'\n')
    p='data/event_scripts.s';s=(ROOT/p).read_text();inc='\t.include "data/scripts/vidra_drafts.inc"'
    if inc not in s:write(p,s+'\n'+inc+'\n')
    write('tools/vidra_drafts/manifest.json',report)
    print('Wrote',len(ALL),'native editable draft maps')

if __name__=='__main__':main()
