"""Dedicated native-terrain city pair with exact compatible harbor edge graphics.

Explicit authoring command, never run by make. Preserves the harbor and west
quay blocks and source tilesets. No quantization or new pixel art is used.
"""
import json,struct,shutil
from pathlib import Path
from PIL import Image
R=Path(__file__).resolve().parents[2]
def read(p):return json.loads((R/p).read_text())
def write(p,obj):
    path=R/p;data=json.dumps(obj,indent=2)+'\n'
    if not path.exists() or path.read_text()!=data:path.write_text(data)
def words(p):
    b=(R/p).read_bytes();return list(struct.unpack('<'+'H'*(len(b)//2),b))

def build():
    blockpath='data/layouts/Havora_Market/map.bin'
    snapshot='tools/havora/market-base-blocks.json'
    # Frozen first-pass recipe, rather than repeatedly transforming authored data.
    if not (R/snapshot).exists():
        base=words(blockpath);assert len(base)==1600
        write(snapshot,{'width':40,'height':40,'blocks':base})
    base=read(snapshot)['blocks']
    oldmeta=words('data/tilesets/primary/havora_harbor/metatiles.bin')+words('data/tilesets/secondary/havora_harbor/metatiles.bin')
    oldattrs=(R/'data/tilesets/primary/havora_harbor/metatile_attributes.bin').read_bytes()+(R/'data/tilesets/secondary/havora_harbor/metatile_attributes.bin').read_bytes()
    used={v&1023 for v in base}
    # Whole west quay plus ten northern harbor rows exceed the visible seam buffer.
    for p in ['data/layouts/Quantum_Havora_Harbor_Layout/map.bin','data/layouts/Havora_River/map.bin']:
        blocks=words(p);used.update(v&1023 for v in (blocks[:400] if 'Harbor_' in p else blocks))
    asset=read('tools/havora/assets.json')
    reserved=set(asset['reserved_primary_tiles'])|set(range(896,1024))
    gfx={w&1023 for mid in used for w in oldmeta[mid*8:mid*8+8]}|reserved
    freegfx=iter(i for i in range(1024) if i not in gfx)
    freemeta=iter(i for i in range(640) if i not in used)
    metas=[0]*(1024*8);attrs=bytearray(1024*4)
    tiles=Image.new('P',(128,512),0)
    srcs=[Image.open(R/f'data/tilesets/{d}/havora_harbor/tiles.png') for d in ['primary','secondary']]
    for tid in sorted(gfx):
        src=srcs[0 if tid<640 else 1];n=tid if tid<640 else tid-640
        tiles.paste(src.crop((n%16*8,n//16*8,n%16*8+8,n//16*8+8)),(tid%16*8,tid//16*8))
    for mid in sorted(used):
        metas[mid*8:mid*8+8]=oldmeta[mid*8:mid*8+8]
        attrs[mid*4:mid*4+4]=oldattrs[mid*4:mid*4+4]
    native=words('data/tilesets/primary/general/metatiles.bin')
    na=(R/'data/tilesets/primary/general/metatile_attributes.bin').read_bytes()
    ni=Image.open(R/'data/tilesets/primary/general/tiles.png')
    mapping={};tilemap={i:i for i in asset['reserved_primary_tiles']}
    for mid in range(640):
        ws=native[mid*8:mid*8+8]
        if not set(w>>12 for w in ws)<={0,1,6}:continue
        if not any(ws):continue
        target=next(freemeta);mapping[mid]=target
        packed=[]
        for w in ws:
            source=w&1023
            if source not in tilemap:
                dest=next(freegfx);tilemap[source]=dest;gfx.add(dest)
                tiles.paste(ni.crop((source%16*8,source//16*8,source%16*8+8,source//16*8+8)),(dest%16*8,dest//16*8))
            packed.append((w&~1023)|tilemap[source])
        metas[target*8:target*8+8]=packed
        attrs[target*4:target*4+4]=na[mid*4:mid*4+4]
    # Native gray stairs use General palette 2, which the harbor uses for other
    # materials. Fit the five exact GBA colors into UNUSED city palette entries.
    # Every color actually used by the compatible edge metatiles stays unchanged.
    paluse={i:{0} for i in range(13)}
    for mid in used:
        for w in oldmeta[mid*8:mid*8+8]:
            tid=w&1023;bank=w>>12
            if tid>=896:paluse[bank].update(range(16));continue
            src=srcs[tid>=640];n=tid if tid<640 else tid-640
            paluse[bank].update(src.crop((n%16*8,n//16*8,n%16*8+8,n//16*8+8)).get_flattened_data())
    stairbank=next(p for p in range(7,13) if len(set(range(1,16))-paluse[p])>=5)
    slots=iter(sorted(set(range(1,16))-paluse[stairbank]))
    generalpal=[tuple((int(v)>>3)<<3 for v in s.split()) for s in (R/'data/tilesets/primary/general/palettes/02.pal').read_text().splitlines()[3:19]]
    colors={};stairtiles={}
    for source in [0x89,0x91]:
        target=next(freemeta);mapping[source]=target;packed=[]
        for w in native[source*8:source*8+8]:
            tid=w&1023
            if w>>12==0:packed.append((w&~1023)|tilemap[tid]);continue
            assert w>>12==2
            if tid not in stairtiles:
                dest=next(freegfx);gfx.add(dest);stairtiles[tid]=dest
                patch=ni.crop((tid%16*8,tid//16*8,tid%16*8+8,tid//16*8+8));lut=[0]*256
                for value in set(patch.get_flattened_data())-{0}:
                    color=generalpal[value]
                    if color not in colors:colors[color]=next(slots)
                    lut[value]=colors[color]
                tiles.paste(patch.point(lut),(dest%16*8,dest//16*8))
            packed.append((w&0x0C00)|(stairbank<<12)|stairtiles[tid])
        metas[target*8:target*8+8]=packed;attrs[target*4:target*4+4]=na[source*4:source*4+4]
    for directory,start,count in [('primary',0,640),('secondary',640,384)]:
        folder=R/f'data/tilesets/{directory}/havora_city';folder.mkdir(parents=True,exist_ok=True)
        shutil.copytree(R/f'data/tilesets/{directory}/havora_harbor/palettes',folder/'palettes',dirs_exist_ok=True)
        image=tiles.crop((0,start//16*8,128,(start+count)//16*8))
        image.putpalette(srcs[0].getpalette());image.save(folder/'tiles.png')
        (folder/'metatiles.bin').write_bytes(struct.pack('<'+'H'*(count*8),*metas[start*8:(start+count)*8]))
        (folder/'metatile_attributes.bin').write_bytes(attrs[start*4:(start+count)*4])
    palpath=R/f'data/tilesets/secondary/havora_city/palettes/{stairbank:02}.pal'
    lines=palpath.read_text().splitlines()
    for color,index in colors.items():lines[3+index]=' '.join(map(str,color))
    palpath.write_text('\n'.join(lines)+'\n')
    grid=[[0x3280]*40 for _ in range(64)]
    for y in range(38):
        for x in range(40):grid[y][x]=(base[y*40+x]&0xFFF)|0x4000
    def tile(x,y,source,solid=False,elevation=4):
        grid[y][x]=mapping[source]|(0x400 if solid else 0)|(elevation<<12)
    def rect(x,y,w,h,source,solid=False,elevation=4):
        for yy in range(y,y+h):
            for xx in range(x,x+w):tile(xx,yy,source,solid,elevation)
    # Grass lawns soften the former uninterrupted brick field. Building corners
    # keep their original matching stone courtyards.
    for y in range(37):
        for x in range(1,39):
            mid=grid[y][x]&1023
            if mid in [0x280,0x3F1]:tile(x,y,1)
            if mid in [0x3F8,0x3F9,0x3FA]:tile(x,y,4,True)
    buildings=read('tools/havora/market-district.json')['buildings']
    for x,y,w,h in [(4,5,4,4),(31,5,4,5),(4,13,4,5),(31,13,4,4),
                    (16,3,8,5),(3,21,8,4),(28,21,8,5)]:
        for yy in range(y-1,y+h+1):
            for xx in range(x-1,x+w+1):
                if grid[yy][xx]&1023==mapping[1]:grid[yy][xx]=0x4280
    # Garden paths through the two residential gates remain open.
    for x in [6,33]:
        for y in [10,18]:grid[y][x]=0x41C1
    def tree(x,y,e=4):
        for yy,row in enumerate([[0x0E,0x0F],[0x1C,0x1D],[0x24,0x25]]):
            for xx,mid in enumerate(row):tile(x+xx,y+yy,mid,True,e)
    for x,y in [(2,1),(10,1),(27,1),(36,1),(10,5),(27,5),
                (2,11),(12,13),(27,13),(36,11),(1,28),(36,28)]:tree(x,y)
    for x in list(range(2,13))+list(range(27,38)):
        if not grid[1][x]&0xC00:tile(x,1,5,True)
    # A true one-level transition: upper street 4, lower quay 3, stair tiles 0.
    # No hidden warp or script is involved in changing height.
    rect(1,37,38,1,1)
    for x in range(40):tile(x,38,0x87,True);tile(x,39,0x79,True,3);tile(x,40,1,False,3)
    for left in [4,19]:
        for x in range(left,left+4):
            grid[37][x]=0x41C1
            tile(x,38,0x89,False,0);tile(x,39,0x91,False,0)
            for y in range(40,44):grid[y][x]=0x31C1
    # Lower terrace gardens and a broad stair landing. New terrain stays beyond
    # the eight-tile neighbor buffer on both harbor and west-quay boundaries.
    for x in [10,27]:
        rect(x,45, 1,13,1,False,3)
        for yy in [43, 20,51]:
            for xx in [x,x+4]:tree(xx,yy,3)
        for xx in range(x,x+7):tile(xx,55,4,True,3)
        for xx in [x,x+6]:grid[56][xx]=0x3400|0x2B4
    for y in range(40,62):
        for x in range(18,25):grid[y][x]=0x31C1
    for y in range(40,62):
        for x in range(4,8):grid[y][x]=0x31C1
    # Keep a complete side boundary except where the original west quay joins.
    for y in range(51):grid[y][0]=0x32B5
    for y in range(64):grid[y][39]=0x32B5
    for x in [17,33]:
        for yy,row in enumerate(asset['assets']['house']['metatiles'][:2]):
            for xx,mid in enumerate(row):grid[62+yy][x+xx]=0x3400|mid
    (R/blockpath).write_bytes(struct.pack('<2560H',*(v for row in grid for v in row)))
    layouts=read('data/layouts/layouts.json')
    layout=next(l for l in layouts['layouts'] if l['id']=='LAYOUT_QUANTUM_HAVORA_NORTH_QUAY')
    layout.update(height=64,primary_tileset='gTileset_HavoraCityPrimary',secondary_tileset='gTileset_HavoraCity')
    write('data/layouts/layouts.json',layouts)
    city=read('data/maps/Havora_Market/map.json')
    for c in city['connections']:
        if c['direction']=='left':c['offset']=51
    for group in ['object_events','warp_events']:
        for e in city[group]:e['elevation']=4
    write('data/maps/Havora_Market/map.json',city)
    west=read('data/maps/Havora_River/map.json')
    for c in west['connections']:
        if c['map']==city['id']:c['offset']=-51
    write('data/maps/Havora_River/map.json',west)
    write('tools/havora/city-tileset.json',{'dimensions':[40,64],'native_general_ids':mapping,
          'compatible_metatiles':sorted(used),'graphics_used':len(gfx),
          'native_graphics_added':len(set(tilemap.values())-reserved)+len(stairtiles),'stair_palette_bank':stairbank,'stairs':[{'x':x,'width':4,'top_y':38,'bottom_y':39} for x in [4,19]],
          'upper_elevation':4,'lower_elevation':3,'stair_elevation':0,
          'source':'repository FireRed General; established Havora Emerald assets, exact palettes and pixels'})

if __name__=='__main__':build()
