"""Pack the approved Emerald harbor into editable FireRed primary/secondary tilesets.

No external checkout is needed: native cutouts and provenance live in source_art.
All pixels are encoded exactly at GBA color depth; palettes are shared per 8x8 tile.
General animation destinations and seam graphics stay reserved in the primary.
"""
from pathlib import Path
import json, struct
import numpy as np
from PIL import Image

R=Path(__file__).resolve().parents[2]
SOURCE=R/'tools/havora/source_art/emerald_harbor'
PRIMARY=R/'data/tilesets/primary/havora_harbor'
SECONDARY=R/'data/tilesets/secondary/havora_harbor'

def words(p):
    b=p.read_bytes(); return list(struct.unpack('<'+'H'*(len(b)//2),b))
def savejson(p,obj):p.write_text(json.dumps(obj,indent=2,default=int)+'\n')
def rgba(im):
    a=np.array(im.convert('RGBA')); a[:,:,:3]=(a[:,:,:3]>>3)<<3
    return Image.fromarray(a)

def build_assets():
    art={p.stem:rgba(Image.open(p)) for p in sorted(SOURCE.glob('*.png'))}
    metas=[]; attrs=[]; images=[]; lookup={}; info={}
    def register(im,attribute=0):
        im=rgba(im).convert('RGB'); key=(im.tobytes(),attribute)
        if key not in lookup:
            lookup[key]=640+len(images);images.append(im);attrs.append(attribute)
        return lookup[key]
    # Stable first IDs retain the north approach's paving reference.
    floors={n:register(art[n],0x22000415 if n=='water' else 0) for n in ['stone','wood','water']}
    def opaque(im,bg):
        out=Image.new('RGBA',im.size)
        for y in range(0,im.height,16):
            for x in range(0,im.width,16):out.alpha_composite(art[bg],(x,y))
        out.alpha_composite(im);return out
    def asset(name,background='stone'):
        im=opaque(art[name],background);ids=[]
        for y in range(0,im.height,16):
            ids.append([register(im.crop((x,y,x+16,y+16))) for x in range(0,im.width,16)])
        info[name]={'metatiles':ids,'size':[im.width//16,im.height//16]}
        return ids
    for name in art:
        if name not in floors:asset(name,'water' if name in ['sailboat','rock','dock_foot','dock_foot_west','dock_foot_east'] else 'stone')
    for name in floors:info[name]={'metatiles':[[floors[name]]],'size':[1,1]}
    # Compose the map from reusable pieces. Only mixed-background prop variants
    # create extra metatiles; the building parts remain ordinary Porymap blocks.
    grid=[[floors['water'] for _ in range(40)] for _ in range(32)]
    blocks=[[0x400 for _ in range(40)] for _ in range(32)]
    land=set()
    for x,y,w,h in [(0,0,40,4),(0,0,8,22),(5,16,6,8),(8,19,3,4),(6,7,4,6),(10,15,6,8),(10,21,20,3),(15,20,15,3),(29,21,4,5),(32,23,7,5),(34,19,5,9),(37,3,3,8)]:
        land|={(xx,yy) for yy in range(y,y+h) for xx in range(x,x+w)}
    docks=[(11,3,4,5),(23,3,4,7),(29,3,4,5),(18,13,5,10),(7,8,6,3),(7,12,5,3)]
    walk=land.copy()
    for x,y,w,h in docks:walk|={(xx,yy) for yy in range(y,y+h) for xx in range(x,x+w)}
    def tile(n,x,y,solid=False):
        grid[y][x]=info[n]['metatiles'][0][0];blocks[y][x]=0x3000|(0x400 if solid else 0)
    for x,y in sorted(walk):tile('stone',x,y)
    for x,y in sorted(walk):
        if (x,y+1) not in walk:tile('quay_south',x,y,True)
        elif y>0 and (x,y-1) not in walk:tile('quay_north',x,y)
        elif x>0 and (x-1,y) not in walk:tile('quay_west',x,y)
        elif (x+1,y) not in walk:tile('quay_east',x,y)
    for x,y,w,h in docks:
        for yy in range(y,y+h):
            for xx in range(x,x+w):
                name='dock_west' if xx==x else 'dock_east' if xx==x+w-1 else 'wood'
                if yy==y+h-1 and (xx,yy+1) not in land:name='dock_sw' if xx==x else 'dock_se' if xx==x+w-1 else 'wood'
                if (xx,yy) in land:name='wood'
                # Preserve a collision lip at the outer edge of each pier.
                edge=(xx in [x,x+w-1] and (xx,yy) not in land)
                tile(name,xx,yy,edge or (x==18 and yy==13))
        for xx in range(x,x+w):
            if (xx,y+h) not in walk:
                name='dock_foot_west' if xx==x else 'dock_foot_east' if xx==x+w-1 else 'dock_foot'
                tile(name,xx,y+h,True)
    def place(name,x,y,behind=False):
        im=art[name]
        for yy in range(im.height//16):
            for xx in range(im.width//16):
                patch=im.crop((xx*16,yy*16,xx*16+16,yy*16+16))
                base=images[grid[y+yy][x+xx]-640].convert('RGBA');base.alpha_composite(patch)
                grid[y+yy][x+xx]=register(base)
                if not behind or yy==im.height//16-1:blocks[y+yy][x+xx]|=0x400
    for n,x,y in [('warehouse',1,4),('house',1,13),('house',11,16),('crane',6,8),('lighthouse',35,22)]:place(n,x,y,n=='crane')
    blocks[11][9]|=0x400
    for x,y in [(4,1),(5,18),(13,22),(24,22),(32,24),(38,5)]:place('planter',x,y)
    for x,y in [(27,11),(34,13)]:place('sailboat',x,y)
    for x,y in [(30,27),(32,29),(34,29),(36,29),(38,29)]:
        for xx in [x,x+1]:place('rock',xx,y)
    # Keep original Emerald material palettes. A flattened patch can use two
    # banks (lower/upper hardware layer), preserving every approved GBA color.
    patches=[]; chunks=[]
    for im in images:
        ch=[]
        for y in [0,8]:
            for x in [0,8]:
                ar=np.array(im.crop((x,y,x+8,y+8)))
                ch.append(len(patches));patches.append((ar,frozenset(tuple(v) for v in ar.reshape(-1,3))))
        chunks.append(ch)
    general=R/'data/tilesets/primary/general'
    palettes={}
    for bank in [0,1,6]:palettes[bank]=[tuple(map(int,s.split())) for s in (general/'palettes'/f'{bank:02}.pal').read_text().splitlines()[3:19]]
    bins={bank:frozenset(v[1:]) for bank,v in palettes.items()}
    # Committed palette plan keeps regeneration deterministic and solver-free.
    for bank,cs in zip([2,3,4,5,7,8,9,10,11,12],json.loads((SOURCE/'packed_palettes.json').read_text())):
        colors=[tuple(c) for c in cs];assert len(colors)<=15
        bins[bank]=frozenset(colors)
        palettes[bank]=[(0,0,0)]+colors+[(0,0,0)]*(15-len(colors))
    # FireRed uses a 640/384 tile split. General animation slots are never reused.
    raw=words(general/'metatiles.bin');keep=[5,0x1c1,0x1d9]
    reserved={0}|set(range(416,482))|set(range(508,512))
    for mid in keep:reserved|={w&1023 for w in raw[mid*8:mid*8+8]}
    original=Image.open(general/'tiles.png');tiles={};tilekeys={}
    for tid in sorted(reserved):tiles[tid]=np.array(original.crop((tid%16*8,tid//16*8,tid%16*8+8,tid//16*8+8)),dtype=np.uint8)
    free=iter(i for i in range(1024) if i not in reserved)
    def pack(ar):
        for a,flip in [(ar,0),(ar[:,::-1],0x400),(ar[::-1,:],0x800),(ar[::-1,::-1],0xc00)]:
            if a.tobytes() in tilekeys:return tilekeys[a.tobytes()]|flip
        tid=next(free);tiles[tid]=ar.copy();tilekeys[ar.tobytes()]=tid;return tid
    packed=[]
    for ar,colors in patches:
        pairs=[(a,b) for a in bins for b in bins if colors<=bins[a]|bins[b]]
        a,b=min(pairs,key=lambda p:(not colors<=bins[p[0]],p[0]!=p[1],p))
        layers=[]
        for bank,cs in [(a,colors&bins[a]),(b,colors-bins[a])]:
            indices={c:palettes[bank].index(c,1) for c in cs}
            image=np.array([[indices.get(tuple(c),0) for c in row] for row in ar],dtype=np.uint8)
            layers.append(pack(image)|(bank<<12))
        packed.append(layers)
    metas=[[packed[i][layer] for layer in [0,1] for i in ch] for ch in chunks]
    assert len(metas)<=384
    for p in [PRIMARY,SECONDARY]:
        (p/'palettes').mkdir(parents=True,exist_ok=True)
        for b in range(16):
            colors=palettes.get(b,[(0,0,0)]*16)
            (p/'palettes'/f'{b:02}.pal').write_text('JASC-PAL\n0100\n16\n'+'\n'.join(' '.join(map(str,c)) for c in colors)+'\n')
    for p,start,count in [(PRIMARY,0,640),(SECONDARY,640,max(1,max(tiles)-639))]:
        im=Image.new('P',(128,((count+15)//16)*8),0);im.putpalette(sum((list(c) for c in palettes[2]),[])+[0]*720)
        for tid,ar in tiles.items():
            if start<=tid<start+count:im.paste(Image.fromarray(ar),((tid-start)%16*8,(tid-start)//16*8))
        im.save(p/'tiles.png')
    primary=[0]*5120;pa=bytearray(2560);ga=(general/'metatile_attributes.bin').read_bytes()
    for mid in keep:primary[mid*8:mid*8+8]=raw[mid*8:mid*8+8];pa[mid*4:mid*4+4]=ga[mid*4:mid*4+4]
    (PRIMARY/'metatiles.bin').write_bytes(struct.pack('<5120H',*primary));(PRIMARY/'metatile_attributes.bin').write_bytes(pa)
    (SECONDARY/'metatiles.bin').write_bytes(struct.pack('<'+'H'*(8*len(metas)),*sum(metas,[])));(SECONDARY/'metatile_attributes.bin').write_bytes(struct.pack('<'+'I'*len(attrs),*attrs))
    data={'style':'emerald_harbor','floors':floors,'assets':info,'tiles':max(tiles)+1,'custom_tiles':len(tilekeys),'reserved_primary_tiles':sorted(reserved),'secondary_tiles':max(1,max(tiles)-639),'metatiles':len(metas),'palette_banks':sorted(palettes),'map_metatiles':grid,'map_collision':blocks}
    savejson(R/'tools/havora/assets.json',data)
    # Keep the approved unoccupied source composition for exact rendered-art checks.
    preview=Image.new('RGB',(640,512))
    for y,row in enumerate(grid):
        for x,mid in enumerate(row):preview.paste(images[mid-640],(x*16,y*16))
    (R/'build').mkdir(exist_ok=True);preview.save(R/'build/havora-approved-emerald.png')
    print(f'Packed {len(metas)} metatiles, {len(tilekeys)} custom graphics, {len(palettes)} palette banks')

def build_map():
    data=json.loads((R/'tools/havora/assets.json').read_text())
    a=[mid|bits for row,collision in zip(data['map_metatiles'],data['map_collision']) for mid,bits in zip(row,collision)]
    p=R/'data/layouts/Quantum_Havora_Harbor_Layout'
    (p/'map.bin').write_bytes(struct.pack('<1280H',*a));(p/'border.bin').write_bytes(struct.pack('<4H',*([0x400|data['floors']['water']]*4)))
    # Keep original map headers, objects, warps, ferry scripts and approach layouts.
    print('Built 40x32 Emerald harbor; original map headers and events retained')

if __name__=='__main__':build_assets();build_map()
