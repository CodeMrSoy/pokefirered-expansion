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
    sheet=Image.new('P',(128,((len(p.tiles)+15)//16)*8));sheet.putpalette(existing.getpalette())
    for i,raw in enumerate(p.tiles):sheet.paste(Image.frombytes('P',(8,8),raw),(i%16*8,i//16*8))
    sheet.save(D/'tiles.png');m['tiles']=sheet.width*sheet.height//64
