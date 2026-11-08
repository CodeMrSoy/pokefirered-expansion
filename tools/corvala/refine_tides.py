"""Append-only reef/tide pass on the user's 0c02a4ba Porymap layout.

Explicit --write only. Keep this input snapshot: never regenerate the old cove.
"""
import argparse, hashlib, struct
from collections import deque
from PIL import Image
from build_cove import R,D,Pack,read,write,words,polygon,rect,atlas
from shoreline import NativeShore

BASE=R/'tools/corvala/manual_layouts/user-0c02a4ba.bin'

def reachable(bs,start,exclude=()):
    seen={tuple(start)};q=deque(seen)
    while q:
        x,y=q.popleft();e=bs[y*64+x]>>12
        for xx,yy in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
            if not (0<=xx<64 and 0<=yy<64) or (xx,yy) in seen or (xx,yy) in exclude:continue
            v=bs[yy*64+xx];ee=v>>12
            if v&0xc00 or ee==1 or (e and ee and e!=ee):continue
            seen.add((xx,yy));q.append((xx,yy))
    return seen

def main():
    m=read(R/'tools/corvala/map.json');raw=BASE.read_bytes()
    current=(R/'data/layouts/Corvala_Town/map.bin').read_bytes()
    assert current==raw or hashlib.sha256(current).hexdigest()==m['result_sha256'], 'New manual edits: incorporate them before running this pass'
    low=words(BASE);p=Pack()
    ds=words(D/'metatiles.bin')[:222*8]
    p.metas=[ds[i:i+8] for i in range(0,len(ds),8)];p.attrs=words(D/'metatile_attributes.bin',4)[:222]
    p.ml={tuple(d)+(a,):640+i for i,(d,a) in enumerate(zip(p.metas,p.attrs))}
    shore=NativeShore(R,atlas('cinnabar_island'),p.meta)
    def sand(v):return p.attr(v&1023)&511==0x21
    land={(i%64,i//64) for i,v in enumerate(low) if sand(v)}
    # Broaden the southern crossing and round the exposed lobes. Only water
    # changes here; retain every user-authored dock, cliff and building tile.
    additions=polygon([(28,47),(31,47),(34,48),(37,48),(38,51),(35,51),(32,50),(29,50)])
    additions|=polygon([(4,40),(6,38),(9,38),(8,42),(7,45),(5,44)])
    additions|=polygon([(49,39),(53,39),(55,41),(54,43),(50,43)])
    additions|=rect(25,17,3,2)|rect(35,17,2,2)
    for x,y in additions:
        if low[y*64+x]==0x112b:low[y*64+x]=0x3115;land.add((x,y))
    # A designated stair connects the permanent gym beach to the raised dock.
    for x in (21,22):low[24*64+x]=m['labels']['Stairs'] # elevation zero joins 3/4
    # Align the moved visible doorways and their elevations with the events.
    low[15*64+49]=(low[15*64+49]&0x0fff)|0x4000
    town=read(R/'data/maps/Corvala_Town/map.json')
    town['warp_events'][4].update(x=10,y=14,elevation=5)
    town['warp_events'][5].update(x=49,y=15,elevation=4)
    for ev in town['warp_events']:ev['elevation']=low[ev['y']*64+ev['x']]>>12
    m['portals'].update(gym=[10,14],entrance=[49,15])
    m['landmarks'].update(gym_approach=[10,15],entrance_approach=[49,16])
    m['gym_terraces']={'source':'user-0c02a4ba','stairs':[[9,18],[10,18],[14,16],[15,16]]}
    # Small clusters, with room to walk between them; retain the existing reefs.
    for cx,cy in [(12,23),(17,24),(31,16),(41,16),(53,24),(53,33),(49,38),(32,49),(6,41)]:
        for dx,dy,k in [(-1,0,0),(1,1,6),(0,2,3)]:
            x,y=cx+dx,cy+dy
            if low[y*64+x]==0x3115:low[y*64+x]=0x3c00|m['labels'][f'Coral{k}']
    # Full high tide: no dry sand islands or exposed dock supports/stairs.
    # Native sand/grass seam tiles have NORMAL behavior, not MB_SAND.
    sand_seams={0x100,0x101,0x102,0x104,0x105,0x106,0x10c,0x10d,0x10e,0x114,0x115,0x116,0x11c,0x11d,0x11e}
    land|={(i%64,i//64) for i,v in enumerate(low) if v&1023 in sand_seams and i//64>=12}
    lower_terrace=rect(0,17,19,2)
    high=low.copy()
    for x,y in land|lower_terrace:high[y*64+x]=0x1c00|0x12b if x==0 else 0x112b
    submerged=[]
    for i,v in enumerate(low):
        mid=v&1023
        if mid in (667,668,669,670,m['labels']['Stairs']):
            high[i]=0x112b;submerged.append([i%64,i//64])
    # The upper gym steps remain above water, but cannot be swum onto as
    # elevation-zero ground. The gym walking route is LOW-only.
    for x in (14,15):high[16*64+x]=(high[16*64+x]&0x0fff)|0x5000
    # High water meets these existing dock edges. Native Surf requires a
    # level-three landing; an invisible level-zero join connects the deck.
    # Graphics do not change, and no global Surf rules need changing.
    landings=[]
    for x,y in [(21,23),(22,23),(35,43),(36,43),(45,41),(46,41)]:
        assert not high[y*64+x]&0xc00 and high[(y+1)*64+x]==0x112b
        high[y*64+x]=(high[y*64+x]&0x0fff)|0x3000
        high[(y-1)*64+x]&=0x0fff
        landings.append([x,y])
    # Reuse native coastal rock art: brown boulders exposed on sand, plus
    # Vermilion's complete two-by-two sea rocks in permanently wet locations.
    rock_art=[[0x1cb,0x1cc],[0x1d3,0x1d4]]
    wet_pebble=p.meta(p.desc(0x12b)[:4]+p.desc(0xaf)[4:],0x20000000)
    rock_sites=[]
    for cx,cy in [(8,24),(30,14),(53,29),(33,48),(49,38)]:
        candidates=[]
        for y in range(cy-4,cy+5):
            for x in range(cx-4,cx+5):
                if all(low[yy*64+xx]==0x3115 for xx,yy in rect(x,y,2,2)):
                    candidates.append((abs(x-cx)+abs(y-cy),x,y))
        assert candidates,('rock placement',cx,cy)
        _,x,y=min(candidates);rock_sites.append([x,y,1])
        low[y*64+x]=0x3c00|0xaf;high[y*64+x]=0x1c00|wet_pebble
    for x,y in [(14,22),(21,17),(34,17),(55,24),(51,39),(8,44),(24,53),(41,55)]:
        if low[y*64+x]!=0x3115:continue
        low[y*64+x]=0x3c00|0xaf;high[y*64+x]=0x1c00|wet_pebble;rock_sites.append([x,y,1])
    for x,y in [(4,34),(17,56),(50,53),(57,36)]:
        assert all(low[yy*64+xx]==0x112b for xx,yy in rect(x,y,2,2)),('sea rock',x,y)
        for dy,row in enumerate(rock_art):
            for dx,mid in enumerate(row):low[(y+dy)*64+x+dx]=high[(y+dy)*64+x+dx]=0x1c00|mid
        rock_sites.append([x,y,2])
    # Flood whole lower sea-facing tiles, preserving the upper cliff backing.
    # Select against a snapshot so water cannot erode successive cliff layers.
    rim=[];coast=high.copy()
    cliff_ids={0x70,0x71,0x72,0x78,0x79,0x7a,0x90,0x92,0xa0,0xa8,0xb2}
    for y in range(8,35):
        for x in range(18,64):
            i=y*64+x;v=coast[i];mid=v&1023
            if mid not in cliff_ids or not v&0xc00 or (48<=x<=50 and 14<=y<=15):continue
            if not any(0<=x+dx<64 and 0<=y+dy<64
                       and coast[(y+dy)*64+x+dx]&1023==0x12b
                       for dx,dy in [(-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1)]):continue
            high[i]=0x1c00|0x12b if x==63 else 0x112b
            rim.append([x,y,15])
    # Lower outside corners and the two faces beside the cave dock, marked
    # in the user's shoreline review. These are not upper cliff backing.
    for x,y in [(39,10),(43,11),(46,12),(47,16),(51,16),(56,15),
                (58,16),(59,18),(60,20),(61,23),(62,27),(63,31)]:
        assert low[y*64+x]&1023 in (0xb3,0x79)
        high[y*64+x]=0x1d2b if x==63 else 0x112b
        rim.append([x,y,15])
    def edge_and_encounters(bs):
        lands={(i%64,i//64) for i,v in enumerate(bs) if sand(v)}
        for x,y in sorted(lands):
            i=y*64+x;v=bs[i]
            # Keep coral graphics; update only bare sand/shore quadrants.
            if v&0xc00 or 845<=v&1023<=861:continue
            def wet(xx,yy):return 0<=xx<64 and 0<=yy<64 and bs[yy*64+xx]&1023==0x12b
            mask=sum(1<<j for j,(dx,dy) in enumerate([(0,-1),(1,0),(0,1),(-1,0)]) if wet(x+dx,y+dy))
            diag=sum(1<<j for j,(dx,dy) in enumerate([(-1,-1),(1,-1),(-1,1),(1,1)]) if wet(x+dx,y+dy))
            mid=shore.shoreline(mask,diag) if mask or diag else 0x115
            # FireRed stores encounter type separately from sand behavior.
            mid=p.meta(p.desc(mid),(p.attr(mid)&~0x07000000)|0x01000000)
            bs[i]=(v&0xfc00)|mid
    edge_and_encounters(low);edge_and_encounters(high)
    from pacifidlog_huts import install
    install(p,low,high,town,m)
    doors={(v['x'],v['y']) for v in town['warp_events']}
    for phase,bs in [('low',low),('high',high)]:
        seen=reachable(bs,(49,16),doors)
        for name,xy in m['landmarks'].items():
            if phase=='high' and name in ('reef_walk','gym_approach'):continue
            assert tuple(xy) in seen,(phase,name,xy,'unreachable')
    safe=reachable(high,(49,16),doors)&reachable(low,(49,16),doors)
    safe={xy for xy in safe if low[xy[1]*64+xy[0]]==high[xy[1]*64+xy[0]]}
    # Warps initially spawn on the doorway before their automatic step out.
    # Include these unchanged, connected tiles so HIGH is drawn before fade-in.
    for x,y in doors:
        if low[y*64+x]==high[y*64+x] and any(q in safe for q in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]):safe.add((x,y))
    mask=bytearray(512)
    for x,y in safe:mask[(y*64+x)//8]|=1<<((y*64+x)%8)
    deltas=[(i%64,i//64,a,b) for i,(a,b) in enumerate(zip(low,high)) if a!=b]
    assert len(p.metas)<=384
    write(D/'metatiles.bin',struct.pack('<'+'H'*(len(p.metas)*8),*sum(p.metas,[])))
    write(D/'metatile_attributes.bin',struct.pack('<'+'I'*len(p.attrs),*p.attrs))
    for phase,bs in [('low',low),('high',high)]:write(R/f'tools/corvala/tide_states/{phase}.bin',struct.pack('<4096H',*bs))
    write(R/'data/layouts/Corvala_Town/map.bin',struct.pack('<4096H',*low))
    write(R/'data/maps/Corvala_Town/map.json',town)
    m.update(result_sha256=hashlib.sha256(struct.pack('<4096H',*low)).hexdigest(),metatiles=len(p.metas),walkable_cells=len(reachable(low,(49,16),doors)))
    m['tide_states']={'installed':'low','runtime_switching':True,'hour_parity':{'even':'low','odd':'high'},'changed_cells':len(deltas),'safe_cells':len(safe),'source_commit':'0c02a4ba','full_flood':True,'submerged_supports_and_steps':submerged,'submerged_cliff_cells':sorted(lower_terrace),'surf_landings':landings,'rock_sites':rock_sites,'low_only_landmarks':['reef_walk','gym_approach']}
    m['tide_states']['flooded_cliff_rim']=rim
    m['shoreline']['generated_metatiles']=sorted(set(shore.cache.values()))
    write(R/'tools/corvala/map.json',m)
    header='// Generated by tools/corvala/refine_tides.py. ROM data only.\n'
    header+='static const struct CorvalaTideTile sCorvalaTideTiles[] = {\n'+''.join(f'    {{{x}, {y}, 0x{a:04X}, 0x{b:04X}}},\n' for x,y,a,b in deltas)+'};\n'
    header+='static const u8 sCorvalaTideSafe[512] = {\n'+''.join('    '+', '.join(f'0x{x:02X}' for x in mask[i:i+16])+',\n' for i in range(0,512,16))+'};\n'
    write(R/'src/data/corvala_tides.h',header)
    images=atlas('corvala')
    for phase,bs in [('low',low),('high',high)]:
        im=Image.new('RGB',(1024,1024))
        for i,v in enumerate(bs):im.paste(images[v&1023],(i%64*16,i//64*16))
        im.save(R/f'docs/corvala/{phase}-tide-playable.png')
    print('PASS: user layout preserved; LOW/HIGH connectivity;',len(deltas),'tide cells;',len(p.metas),'metatiles;',len(safe),'safe transition cells')

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--write',action='store_true');args=ap.parse_args()
    if not args.write:ap.error('--write is required')
    main()
