"""Pack the approved Emerald harbor into editable FireRed primary/secondary tilesets.

No external checkout is needed: native cutouts and provenance live in source_art.
Core art is preserved at GBA depth; catalog extras share material palettes per 8x8 tile.
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
    art={p.stem:rgba(Image.open(p)) for p in sorted(SOURCE.glob('*.png')) if p.stem!='catalog'}
    metas=[]; attrs=[]; images=[]; lookup={}; info={}; meta_ids=[]; id_to_index={}; image_animated=[]
    primary_slots=[i for i in range(640) if i not in [5,0x1c1,0x1d9]]
    def register(im,attribute=0,animated=True):
        im=rgba(im).convert('RGB')
        has_water=any(tuple(c) in [(80,104,208),(104,128,208)] for c in np.array(im).reshape(-1,3))
        animated=animated and has_water;key=(im.tobytes(),attribute,animated)
        if key not in lookup:
            index=len(images);mid=640+index if index<384 else primary_slots[index-384]
            lookup[key]=mid;meta_ids.append(mid);id_to_index[mid]=index;images.append(im);attrs.append(attribute);image_animated.append(animated)
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
        if name not in floors and not name.startswith('zz_'):asset(name,'water' if name in ['sailboat','rock','dock_foot','dock_foot_west','dock_foot_east'] else 'stone')
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
                base=images[id_to_index[grid[y+yy][x+xx]]].convert('RGBA');base.alpha_composite(patch)
                grid[y+yy][x+xx]=register(base)
                if not behind or yy==im.height//16-1:blocks[y+yy][x+xx]|=0x400
    for n,x,y in [('warehouse',1,4),('house',1,13),('house',11,16),('crane',6,8),('lighthouse',35,22),('market_stall',7,17)]:place(n,x,y,n=='crane')
    blocks[11][9]|=0x400
    for x,y in [(4,1),(5,18),(13,22),(24,22),(32,24),(38,5)]:place('planter',x,y)
    for x,y in [(27,11),(34,13)]:place('sailboat',x,y)
    for x,y in [(30,27),(32,29),(34,29),(36,29),(38,29)]:
        for xx in [x,x+1]:place('rock',xx,y)
    # Append the full editing catalog after the established placed pieces.
    catalog_start=len(images)
    catalog=json.loads((SOURCE/'catalog.json').read_text());sheet=rgba(Image.open(SOURCE/'catalog.png'))
    grass={(112,192,160),(96,184,144),(144,208,176)}
    for entry in catalog:
        i=entry['index'];im=sheet.crop((i%16*16,i//16*16,i%16*16+16,i//16*16+16)).convert('RGB')
        ar=np.array(im);floor=np.array(art['stone'].convert('RGB'))
        # Exterior building corners sit on harbor paving rather than grass.
        if entry['town']=='lilycove':
            for color in grass:ar[np.all(ar==color,axis=2)]=floor[np.all(ar==color,axis=2)]
        entry['havora_id']=register(Image.fromarray(ar),animated=entry['water_background'])
    # Appended decorations preserve all previously published Porymap IDs.
    for name in art:
        if name.startswith('zz_'):asset(name,'water')
    # Original sea frames. Replace only pixels using Emerald's two ocean hues;
    # dock timber, sails, foam, roof pixels and shoreline masonry stay fixed.
    frames=[np.array(rgba(Image.open(SOURCE/'water_anim'/f'{i}.png')).convert('RGB')) for i in range(8)]
    water_colors={(80,104,208),(104,128,208)}
    patches=[];chunks=[];patch_single=[]
    for image_index,im in enumerate(images):
        ch=[]
        for y in [0,8]:
            for x in [0,8]:
                ar=np.array(im.crop((x,y,x+8,y+8)));seq=np.repeat(ar[None,:,:,:],8,axis=0)
                mask=np.zeros((8,8),bool)
                for c in water_colors:mask|=np.all(ar==c,axis=2)
                if image_animated[image_index] and np.any(mask):
                    options=[]
                    for yy in [0,8]:
                        for xx in [0,8]:
                            for fy in [False,True]:
                                for fx in [False,True]:
                                    sample=frames[0][yy:yy+8,xx:xx+8]
                                    if fy:sample=sample[::-1]
                                    if fx:sample=sample[:,::-1]
                                    score=np.count_nonzero(np.all(ar==sample,axis=2)&mask)
                                    options.append((score,yy,xx,fy,fx))
                    _,yy,xx,fy,fx=max(options,key=lambda t:t[0])
                    for f in range(8):
                        sample=frames[f][yy:yy+8,xx:xx+8]
                        if fy:sample=sample[::-1]
                        if fx:sample=sample[:,::-1]
                        seq[f][mask]=sample[mask]
                ch.append(len(patches));patches.append(seq);patch_single.append(image_index>=catalog_start)
        chunks.append(ch)
    general=R/'data/tilesets/primary/general';palettes={}
    for bank in [0,1,6]:palettes[bank]=[tuple(map(int,t.split())) for t in (general/'palettes'/f'{bank:02}.pal').read_text().splitlines()[3:19]]
    bins={b:set(v[1:]) for b,v in palettes.items()}
    for bank,cs in zip([2,3,4,5,7,8,9,10,11,12],json.loads((SOURCE/'packed_palettes.json').read_text())):
        colors=[tuple(c) for c in cs];bins[bank]=set(colors)
        palettes[bank]=[(0,0,0)]+colors+[(0,0,0)]*(15-len(colors))
    # Use the spare bank for the most important missing catalog colors. Imported
    # extras share the harbor material ramps when original palettes exceed 13.
    from collections import Counter
    histogram=Counter(tuple(c) for seq in patches for c in seq[0].reshape(-1,3))
    selected=set.union(*bins.values());new=[]
    for _ in range(15):
        def distance(c):return min(sum((int(a)-int(b))**2 for a,b in zip(c,d)) for d in selected)
        c=max(histogram,key=lambda c:histogram[c]*distance(c))
        if distance(c)==0:break
        new.append(c);selected.add(c)
    assert 12 not in bins
    bins[12]=set(new);palettes[12]=[(0,0,0)]+new+[(0,0,0)]*(15-len(new))
    # FireRed uses a 640/384 tile split. General animation slots are never reused.
    raw=words(general/'metatiles.bin');keep=[5,0x1c1,0x1d9]
    reserved={0}|set(range(416,482))|set(range(508,512))
    for mid in keep:reserved|={w&1023 for w in raw[mid*8:mid*8+8]}
    original=Image.open(general/'tiles.png');tiles={}
    for tid in sorted(reserved):tiles[tid]=np.array(original.crop((tid%16*8,tid//16*8,tid%16*8+8,tid//16*8+8)),dtype=np.uint8)
    specs=[];spec_keys={};cache={};quantized=0
    def pack(seq):
        for a,flip in [(seq,0),(seq[:,:,::-1],0x400),(seq[:,::-1,:],0x800),(seq[:,::-1,::-1],0xc00)]:
            if a.tobytes() in spec_keys:return (spec_keys[a.tobytes()],flip)
        key=len(specs);specs.append(seq);spec_keys[seq.tobytes()]=key;return (key,0)
    packed=[]
    for patch_index,seq in enumerate(patches):
        single=patch_single[patch_index]
        colors,counts=np.unique(seq.reshape(-1,3),axis=0,return_counts=True);cs=set(map(tuple,colors));key=(single,tuple(sorted(cs)))
        if key not in cache:
            pairs=[(a,b) for a in bins for b in bins if cs<=bins[a]|bins[b] and (not single or a==b)]
            if pairs:
                a,b=min(pairs,key=lambda p:(not cs<=bins[p[0]],p[0]!=p[1],p));mapping={c:c for c in cs}
            else:
                candidates=[]
                for a in bins:
                    for b in bins:
                        if single and a!=b:continue
                        union=bins[a]|bins[b]
                        if cs&water_colors and not water_colors<=union:continue
                        values=np.array(sorted(union));dist=((colors.astype(int)[:,None,:]-values[None,:,:])**2).sum(2);index=dist.argmin(1)
                        error=int((dist[np.arange(len(colors)),index]*counts).sum());candidates.append((error,a,b,values,index))
                _,a,b,values,index=min(candidates,key=lambda t:(t[0],t[1],t[2]))
                mapping={tuple(c):tuple(values[i]) for c,i in zip(colors,index)};quantized+=1
            cache[key]=(a,b,mapping)
        a,b,mapping=cache[key];layers=[]
        for bank,allowed in [(a,bins[a]),(b,bins[b]-bins[a])]:
            index={c:palettes[bank].index(c,1) for c in allowed}
            arr=np.array([[[index.get(mapping[tuple(c)],0) for c in row] for row in frame] for frame in seq],dtype=np.uint8)
            layers.append((pack(arr),bank))
        packed.append(layers)
    animated=[i for i,a in enumerate(specs) if not np.all(a==a[0])]
    animation_slots=((len(animated)+15)//16)*16;animation_start=1024-animation_slots
    print('Graphics budget:',len(specs),'unique,',len(animated),'animated,',animation_slots,'reserved animation slots,',len(reserved),'General slots');assert animation_start>=640
    free=iter(i for i in range(animation_start) if i not in reserved);tile_ids={}
    for i,seq in enumerate(specs):
        if i in animated:tid=animation_start+animated.index(i)
        else:
            try:tid=next(free)
            except StopIteration:raise AssertionError('Expanded catalog exceeds the 1024-tile graphics budget')
        tile_ids[i]=tid;tiles[tid]=seq[0]
    for tid in range(animation_start,1024):tiles.setdefault(tid,np.zeros((8,8),dtype=np.uint8))
    metas=[]
    for ch in chunks:
        meta=[]
        for layer in [0,1]:
            for i in ch:
                (key,flip),bank=packed[i][layer];meta.append(tile_ids[key]|flip|(bank<<12))
        metas.append(meta)
    assert len(metas)<=1024
    animation_dir=SECONDARY/'anim/water';animation_dir.mkdir(parents=True,exist_ok=True)
    for frame in range(8):
        im=Image.new('P',(128,(animation_slots//16)*8));im.putpalette(sum((list(c) for c in palettes[2]),[])+[0]*720)
        for i,key in enumerate(animated):im.paste(Image.fromarray(specs[key][frame]),(i%16*8,i//16*8))
        im.save(animation_dir/f'{frame}.png')
    header=['/* Generated by tools/havora/build_assets.py. */',f'#define HAVORA_WATER_ANIM_START {animation_start}',f'#define HAVORA_WATER_ANIM_TILES {animation_slots}']
    for f in range(8):header.append(f'static const u16 sHavoraWaterFrame{f}[] = INCBIN_U16("data/tilesets/secondary/havora_harbor/anim/water/{f}.4bpp");')
    header.append('static const u16 *const sHavoraWaterFrames[] = {'+', '.join(f'sHavoraWaterFrame{f}' for f in range(8))+'};')
    (R/'src/data/havora_water_anim.h').write_text('\n'.join(header)+'\n')
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
    for i,mid in enumerate(meta_ids):
        if mid<640:primary[mid*8:mid*8+8]=metas[i];pa[mid*4:mid*4+4]=struct.pack('<I',attrs[i])
    (PRIMARY/'metatiles.bin').write_bytes(struct.pack('<5120H',*primary));(PRIMARY/'metatile_attributes.bin').write_bytes(pa)
    secondary=metas[:384];secondary_attrs=attrs[:384]
    (SECONDARY/'metatiles.bin').write_bytes(struct.pack('<'+'H'*(8*len(secondary)),*sum(secondary,[])));(SECONDARY/'metatile_attributes.bin').write_bytes(struct.pack('<'+'I'*len(secondary_attrs),*secondary_attrs))
    data={'style':'emerald_harbor','floors':floors,'assets':info,'tiles':max(tiles)+1,'custom_tiles':len(specs),'reserved_primary_tiles':sorted(reserved),'secondary_tiles':max(1,max(tiles)-639),'metatiles':len(secondary),'total_metatiles':len(metas),'primary_custom_metatiles':[mid for mid in meta_ids if mid<640],'catalog':catalog,'animation':{'start':animation_start,'slots':animation_slots,'active_tiles':len(animated),'frames':8},'quantized_color_sets':quantized,'palette_banks':sorted(palettes),'map_metatiles':grid,'map_collision':blocks}
    if (R/'tools/havora/layout.json').exists():data.update(json.loads((R/'tools/havora/layout.json').read_text()))
    savejson(R/'tools/havora/assets.json',data)
    # City entrances reuse existing pixels and have their own warp behavior.
    from build_market_district import install_thresholds
    install_thresholds()
    # Keep the approved unoccupied source composition for exact rendered-art checks.
    preview=Image.new('RGB',(640,512))
    for y,row in enumerate(data['map_metatiles']):
        for x,mid in enumerate(row):preview.paste(images[id_to_index[mid]],(x*16,y*16))
    (R/'build').mkdir(exist_ok=True);preview.save(R/'build/havora-approved-emerald.png')
    print(f'Packed {len(metas)} metatiles, {len(specs)} custom graphics, {len(palettes)} palette banks')

def build_map():
    data=json.loads((R/'tools/havora/assets.json').read_text())
    if (R/'tools/havora/layout.json').exists():data.update(json.loads((R/'tools/havora/layout.json').read_text()))
    a=[mid|bits for row,collision in zip(data['map_metatiles'],data['map_collision']) for mid,bits in zip(row,collision)]
    p=R/'data/layouts/Quantum_Havora_Harbor_Layout'
    (p/'map.bin').write_bytes(struct.pack('<1280H',*a));(p/'border.bin').write_bytes(struct.pack('<4H',*([0x400|data['floors']['water']]*4)))
    # Keep original map headers, objects, warps, ferry scripts and approach layouts.
    print('Built 40x32 Emerald harbor; original map headers and events retained')

if __name__=='__main__':build_assets();build_map()
