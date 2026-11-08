"""Native Pacifidlog hut pixels from pret/pokeemerald, fitted without scaling."""
from PIL import Image,ImageDraw
from build_cove import R,D,words,write

def install(p,low,high,town,m):
    root=R/'tools/corvala/assets/pacifidlog'
    source=Image.open(root/'tiles.png');descs=words(root/'metatiles.bin')
    existing=Image.open(D/'tiles.png')
    # Preserve the original graphic indices used by the manual layout.
    p.tiles=[existing.crop((x,y,x+8,y+8)).tobytes()
             for y in range(0,existing.height,8) for x in range(0,128,8)]
    p.lookup={raw:640+i for i,raw in enumerate(p.tiles)}
    # Native service buildings contain grass in some foreground corner tiles.
    # Remove only grass-colored pixels, retaining every roof/wall pixel.
    from build_cove import atlas
    native=atlas('corvala')
    palettes=[]
    for bank in range(13):
        folder=R/'data/tilesets/primary/general' if bank<7 else D
        palettes.append([tuple(map(int,row.split())) for row in (folder/f'palettes/{bank:02}.pal').read_text().splitlines()[3:19]])
    def grass(c):return c[1]>c[0]*1.10 and c[1]>c[2]*1.06
    repaired=[]
    for building in m['buildings'][:2]:
        for y in range(building['y'],building['y']+building['h']):
            for x in range(building['x'],building['x']+building['w']):
                i=y*64+x;v=low[i];image=native[v&1023]
                if not any(grass(c) for c in image.getdata()):continue
                foreground=[]
                for q,(ox,oy) in enumerate([(0,0),(8,0),(0,8),(8,8)]):
                    colors=[image.getpixel((ox+xx,oy+yy)) for yy in range(8) for xx in range(8)]
                    visible=[c for c in colors if not grass(c)]
                    def error(bank):return sum(min(sum((a-b)**2 for a,b in zip(c,pal)) for pal in palettes[bank][1:]) for c in visible)
                    bank=min(range(13),key=error)
                    tile=Image.new('P',(16,16))
                    for n,c in enumerate(colors):
                        if not grass(c):
                            idx=min(range(1,16),key=lambda k:sum((a-b)**2 for a,b in zip(c,palettes[bank][k])))
                            tile.putpixel((ox+n%8,oy+n//8),idx)
                    foreground.append(p.pixels(tile,bank)[q])
                floor=m['labels']['DeckA' if x%2==0 else 'DeckB']
                mid=p.meta(p.desc(floor)[:4]+foreground,p.attr(v&1023))
                low[i]=high[i]=(v&0xfc00)|mid;repaired.append([x,y])
    m['service_building_floor_repairs']=repaired
    palette=root.joinpath('09.pal').read_text().splitlines()
    colors=[tuple(int(v)//8*8 for v in row.split()) for row in palette[3:]]
    write(D/'palettes/10.pal','JASC-PAL\n0100\n16\n'+''.join(' '.join(map(str,c))+'\n' for c in colors))
    art=Image.new('P',(48,48))
    for row in range(3):
        for col in range(3):
            mid=0x209+row*8+col
            for j,v in enumerate(descs[(mid-512)*8:(mid-511)*8]):
                if v>>12!=9:continue
                n=(v&1023)-512
                tile=source.crop((n%16*8,n//16*8,n%16*8+8,n//16*8+8))
                if v&1024:tile=tile.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
                if v&2048:tile=tile.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
                x=col*16+j%2*8;y=row*16+(j%4)//2*8
                for yy in range(8):
                    for xx in range(8):
                        value=tile.getpixel((xx,yy))
                        if value:art.putpixel((x+xx,y+yy),value)
    for ev in town['warp_events']:
        if not ev['dest_map'].startswith('MAP_CORVALA_HOUSE_'):continue
        dx,dy=ev['x'],ev['y']
        for y in range(dy-5,dy+1):
            for x in range(dx-3,dx+4):
                floor=0x2a3 if x%2 else 0x2a6
                low[y*64+x]=high[y*64+x]=0x4000|floor
        for row in range(3):
            for col in range(3):
                x,y=dx-1+col,dy-2+row
                floor=low[y*64+x]&1023
                door=(col,row)==(1,2)
                mid=p.overlay(floor,art.crop((col*16,row*16,col*16+16,row*16+16)),10,0x60 if door else 0)
                low[y*64+x]=high[y*64+x]=0x4000|(0 if door else 0xc00)|mid
    from art import lamp
    lantern=lamp()
    for x,y in [(26,22),(37,27),(40,20),(13,32),(22,39),(36,39)]:
        for row in range(2):
            i=(y+row)*64+x;v=low[i]
            assert v==high[i] and not v&0xc00
            mid=p.overlay(v&1023,lantern.crop((0,row*16,16,row*16+16)),9,0)
            low[i]=high[i]=(v&0xf000)|(0xc00 if row else 0)|mid
    bench=Image.new('P',(32,16));d=ImageDraw.Draw(bench)
    for x in (4,25):d.rectangle((x,7,x+2,15),fill=2)
    d.rectangle((1,2,30,6),fill=2);d.rectangle((2,3,29,5),fill=6)
    d.rectangle((0,8,31,11),fill=2);d.line((1,8,30,8),fill=7);d.line((2,9,29,9),fill=5)
    for x,y in [(27,23),(43,38),(18,38)]:
        for col in range(2):
            i=y*64+x+col;v=low[i];assert v==high[i] and not v&0xc00
            mid=p.overlay(v&1023,bench.crop((col*16,0,col*16+16,16)),9,0)
            low[i]=high[i]=(v&0xf000)|0xc00|mid
    # Light timber surrounds a dark weathered-plank walking route.
    original=[(0,0,0),(56,56,56),(88,64,48),(120,80,56),(152,104,64),
              (184,136,88),(208,168,112),(232,200,144),(64,104,144),
              (88,144,184),(120,176,208),(152,208,224),(64,104,144),
              (112,168,192),(24,40,56),(192,224,232)]
    cool=original.copy();cool[2:8]=[(48,64,64),(64,80,80),(88,104,96),
                                  (112,128,120),(144,160,144),(176,192,168)]
    for bank,colors in [(9,original),(11,cool)]:
        write(D/f'palettes/{bank:02}.pal','JASC-PAL\n0100\n16\n'+''.join(' '.join(map(str,c))+'\n' for c in colors))
    from art import coral
    pots=[]
    for j,(x,y) in enumerate([(41,23),(47,31),(8,34),(17,41),(34,41),(34,26)]):
        plant=Image.new('P',(16,16));growth=coral(3+j%3)
        for yy in range(12):
            for xx in range(16):
                value=growth.getpixel((xx,yy+3))
                if value!=3:plant.putpixel((xx,yy),value)
        d=ImageDraw.Draw(plant);d.polygon([(3,10),(12,10),(10,15),(5,15)],fill=12)
        d.line((4,12,11,12),fill=13);d.line((5,13,10,13),fill=14)
        d.rectangle((2,9,13,10),fill=13);d.line((3,9,12,9),fill=14)
        i=y*64+x;v=low[i];assert v==high[i] and not v&0xc00
        mid=p.overlay(v&1023,plant,12,0x20000000);low[i]=high[i]=(v&0xf000)|0xc00|mid;pots.append([x,y])
    from collections import deque
    avoid={(ev['x'],ev['y']) for ev in town['object_events']+town['warp_events']}
    route=set();start=(31,26)
    for goal in [(49,16)]+[(ev['x'],ev['y']+1) for ev in town['warp_events'] if 'HOUSE_' in ev['dest_map'] or 'MART' in ev['dest_map']]:
        parents={start:None};q=deque([start])
        while q and goal not in parents:
            x,y=q.popleft()
            for xx,yy in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
                if not (0<=xx<64 and 0<=yy<64) or (xx,yy) in parents or (xx,yy) in avoid:continue
                i=yy*64+xx;v=low[i]
                if v!=high[i] or v&0xc00 or v>>12!=4:continue
                parents[xx,yy]=(x,y);q.append((xx,yy))
        assert goal in parents,('dock route',goal)
        pos=goal
        while pos is not None:route.add(pos);pos=parents[pos]
    for x,y in route:
        i=y*64+x;v=low[i];ds=p.desc(v&1023)
        # Only recolor floor pixels; preserve collision and graphic layering.
        mid=p.meta([(w&0x0fff)|0xb000 if w>>12==9 else w for w in ds],p.attr(v&1023))
        low[i]=high[i]=(v&0xfc00)|mid
    m['dock_details']={'potted_coral':pots,'pathway':sorted(route),'timber':'light timber with dark sage-gray walking planks'}
    sheet=Image.new('P',(128,((len(p.tiles)+15)//16)*8));sheet.putpalette(existing.getpalette())
    for i,raw in enumerate(p.tiles):sheet.paste(Image.frombytes('P',(8,8),raw),(i%16*8,i//16*8))
    sheet.save(D/'tiles.png');m['tiles']=sheet.width*sheet.height//64
