"""Author the north waterfront using Havora's existing, stable metatile catalog.

Explicit opt-in authoring tool: normal ROM builds never overwrite Porymap edits.
No tileset rebuilding, source checkout, palette edits or harbor block edits.
"""
import json
import struct
from pathlib import Path

R = Path(__file__).resolve().parents[2]
NAME = 'QuantumHavoraNorthQuay'
MID = 'MAP_QUANTUM_HAVORA_NORTH_QUAY'

def load(p): return json.loads((R / p).read_text())
def save(p, value): (R / p).write_text(json.dumps(value, indent=2) + '\n')

def install_thresholds():
    """Two metatile definitions reuse existing graphics; no new 8x8 tile slots."""
    primary=R/'data/tilesets/primary/havora_harbor'
    secondary=R/'data/tilesets/secondary/havora_harbor'
    metas=bytearray((primary/'metatiles.bin').read_bytes())
    attrs=bytearray((primary/'metatile_attributes.bin').read_bytes())
    for target,source in [(0x08F,0x2A2),(0x090,0x384)]:
        metas[target*16:target*16+16]=(secondary/'metatiles.bin').read_bytes()[(source-640)*16:(source-640+1)*16]
        struct.pack_into('<I',attrs,target*4,0x60) # MB_CAVE_DOOR: native nonanimated entrance.
    (primary/'metatiles.bin').write_bytes(metas)
    (primary/'metatile_attributes.bin').write_bytes(attrs)
    a=load('tools/havora/assets.json')
    for mid in [0x08F,0x090]:
        if mid not in a['primary_custom_metatiles']:
            a['primary_custom_metatiles'].append(mid);a['total_metatiles']+=1
    a['city_thresholds']={'blue':0x08F,'orange':0x090}
    save('tools/havora/assets.json',a)

def build():
    install_thresholds()
    assets = load('tools/havora/assets.json')
    grid = [[0x3280] * 40 for _ in range(40)]
    def tile(x, y, mid, solid=True): grid[y][x] = mid | (0x3400 if solid else 0x3000)
    def rect(x, y, w, h, mid, solid=True):
        for yy in range(y, y+h):
            for xx in range(x, x+w): tile(xx, yy, mid, solid)
    def piece(name, x, y):
        for yy, row in enumerate(assets['assets'][name]['metatiles']):
            for xx, mid in enumerate(row): tile(x+xx, y+yy, mid)
    # Closed northern/eastern edges; western lower promenade joins the old city.
    rect(0, 0, 40, 1, 0x2B5)
    rect(0, 0, 1, 27, 0x2B5)
    rect(39, 0, 1, 40, 0x2B5)
    # Native FireRed flagstones distinguish public streets from the quay brick.
    rect(15,9,10,29,0x1C1,False)
    rect(1,11,38,2,0x1C1,False)
    rect(1,19,38,2,0x1C1,False)
    rect(1,25,38,2,0x1C1,False)
    rect(1,37,38,1,0x1C1,False)
    # Raised planted beds along the residential lanes, all on the same elevation.
    for x, y, w, h in [(2,2,11,1),(27,2,11,1),(2,10,11,1),
                       (27,10,11,1),(2,18,11,1),(27,18,11,1),
                       (14,14,12,1)]:
        rect(x,y,w,h,0x3F1)
        for xx in range(x+1,x+w-1): tile(xx,y,[0x3F8,0x3F9,0x3FA][xx%3])
        tile(x,y,0x2B4);tile(x+w-1,y,0x2B4)
    buildings = []
    def house(name, x, y, width=4, red=False, tall=False):
        # Original Lilycove roof/wall/corner patterns, extended only by repeating
        # their native center pieces; alternate orange roof is in the catalog.
        rows = [[0x327]+[0x328]*(width-2)+[0x329],
                [0x299]+[0x29A]*(width-2)+[0x32A],
                [0x32B]+[0x29D]*(width-2)+[0x332],
                [0x32E]+[0x2A1]*(width-2)+[0x337]]
        if red:
            rows=[[0x3D6]+[0x3D7]*(width-2)+[0x3D8],
                  [0x3DE]+[0x3DF]*(width-2)+[0x3E0],
                  [0x3E5]+[0x3E6]*(width-2)+[0x3E7],
                  [0x3E8]+[0x3D9]*(width-2)+[0x3E9],
                  [0x3EA]+[0x3E1]*(width-2)+[0x3EB]]
        if tall: rows.insert(2,rows[1].copy())
        door = width//2
        rows[-2][door]=0x3DB if red else 0x29E
        rows[-1][door]=0x090 if red else 0x08F
        for yy,row in enumerate(rows):
            for xx,mid in enumerate(row): tile(x+xx,y+yy,mid)
        # Emerald doors have normal behavior in this hybrid. Use a step-on warp
        # on the threshold, rather than claiming an unsupported door animation.
        tile(x+door,y+len(rows)-1,rows[-1][door],False)
        buildings.append(dict(name=name,x=x+door,y=y+len(rows)-1))
    house('ShipwrightHouse',4,5)
    house('WeaverHouse',31,5,red=True)
    house('FisherHouse',4,13,red=True)
    house('TraderHouse',31,13)
    house('TradeHall',16,3,8,tall=True)
    house('Outfitters',3,21,8)
    house('Provisions',28,21,8,red=True)
    # Stall aisles face south, leaving a broad north/south spine and side streets.
    for x,y in [(4,28),(9,28),(17,28),(22,28),(27,28),(32,28),
                (4,33),(9,33),(17,33),(22,33),(27,33),(32,33)]: piece('market_stall',x,y)
    # Four-sided planted square, with entrances on each axis.
    for x,y in [(17,19),(22,19),(17,24),(22,24)]: piece('planter',x,y)
    for x,y in [(18,21),(21,21),(18,22),(21,22)]: piece('planter',x,y)
    # Short fences separate private front yards without closing the public lanes.
    for x,y in [(3,9),(8,9),(30,9),(35,9),(3,17),(8,17),(30,17),(35,17)]:
        tile(x,y,0x342)
    for x in [6,33]:
        for y in [10,18]: tile(x,y,0x1C1,False)
    for x,y in [(14,6),(25,6),(2,26),(13,26),(26,26),(37,26),
                (14,30),(25,30),(2,37),(13,37),(26,37),(37,37)]: piece('planter',x,y)
    # Complete the two roofs whose facades are already authored on harbor rows 0/1.
    for x in [17,33]:
        for yy,row in enumerate(assets['assets']['house']['metatiles'][:2]):
            for xx,mid in enumerate(row): tile(x+xx,38+yy,mid)
    layoutfile='data/layouts/layouts.json'; layouts=load(layoutfile)
    layout=next(l for l in layouts['layouts'] if l['id']=='LAYOUT_QUANTUM_HAVORA_NORTH_QUAY')
    layout['height']=40
    save(layoutfile,layouts)
    (R/layout['blockdata_filepath']).write_bytes(struct.pack('<1600H',*(v for row in grid for v in row)))
    # World-space placement: west quay begins 27 tiles below district's north edge;
    # harbor begins at west-quay y13 = district y40. Keep the user's harbor offset.
    outdoor=load(f'data/maps/{NAME}/map.json')
    outdoor['show_map_name']=True
    for c in outdoor['connections']:
        if c['direction']=='left': c['offset']=27
    west=load('data/maps/QuantumHavoraWestQuay/map.json')
    for c in west['connections']:
        if c['map']==MID: c['offset']=-27
    save('data/maps/QuantumHavoraWestQuay/map.json',west)
    def npc(gfx,x,y,script,facing='DOWN'):
        return dict(type='object',graphics_id='OBJ_EVENT_GFX_'+gfx,x=x,y=y,
                    elevation=3,movement_type='MOVEMENT_TYPE_FACE_'+facing,
                    movement_range_x=0,movement_range_y=0,
                    trainer_type='TRAINER_TYPE_NONE',trainer_sight_or_berry_tree_id='0',
                    script=script,flag='0')
    outdoor['object_events']=[
        npc('MAN',20,10,NAME+'_Guide'),npc('WOMAN_1',11,15,NAME+'_Resident'),
        npc('SAILOR',26,36,NAME+'_Harbor'),npc('FISHER',23,16,NAME+'_Fisher'),
        npc('MAN',5,31,NAME+'_Supplies','UP'),npc('WOMAN_1',28,31,NAME+'_Supplies','UP'),
        npc('MAN',10,36,NAME+'_Supplies','UP'),npc('WOMAN_1',33,36,NAME+'_Supplies','UP'),
        npc('MAN',18,31,NAME+'_Supplies','UP'),npc('WOMAN_1',23,36,NAME+'_Supplies','UP')]
    outdoor['warp_events']=[]
    outdoor['bg_events']=[]
    groups=load('data/maps/map_groups.json')
    scripts=R/'data/event_scripts.s'
    includes=scripts.read_text()
    for i,b in enumerate(buildings):
        name='QuantumHavora'+b['name'];mid='MAP_QUANTUM_HAVORA_'+''.join('_'+c if c.isupper() else c for c in b['name']).strip('_').upper()
        ismart=b['name']=='Provisions'
        template='ThreeIsland_Mart' if ismart else 'TwoIsland_House'
        interior=load(f'data/maps/{template}/map.json')
        interior.update(id=mid,name=name,region_map_section='MAPSEC_QUANTUM_PORT_CITY',allow_running=True)
        if not ismart:interior['layout']='LAYOUT_HOUSE2' # House3 is retired by this repository.
        interior['object_events']=[npc('CLERK',2,3,NAME+'_Supplies','RIGHT')] if ismart else [npc('MAN',7,5,name+'_Owner')]
        interior['warp_events']=[dict(x=x,y=7,elevation=0,dest_map=MID,dest_warp_id=str(i)) for x in [4,3,5]]
        outdoor['warp_events'].append(dict(x=b['x'],y=b['y'],elevation=3,dest_map=mid,dest_warp_id='0'))
        folder=R/'data/maps'/name;folder.mkdir(exist_ok=True)
        save(f'data/maps/{name}/map.json',interior)
        dialogue={
          'ShipwrightHouse':'A good hull starts with patient work.\\nThe harbor keeps our workshop busy.',
          'WeaverHouse':'We weave warm cloth for the sailors.\\nThe north wind never takes a holiday.',
          'FisherHouse':'The fleet leaves before sunrise.\\nBy breakfast, the market is bustling.',
          'TraderHouse':'Ships bring goods from far away.\\nHAVORA gives them a home to trade.',
          'TradeHall':'Welcome to the HAVORA trade hall!\\nOur market connects sea and city.',
          'Outfitters':'Headed north? Pack something warm!\\nOur stall outside sells travel supplies.',
          'Provisions':'Safe travels!'}[b['name']]
        (folder/'scripts.inc').write_text(f'{name}_MapScripts::\n\t.byte 0\n\n{name}_Owner::\n\tmsgbox {name}_Text, MSGBOX_NPC\n\tend\n\n{name}_Text::\n\t.string "{dialogue}$"\n')
        if name not in groups['gMapGroup_QuantumIsland']:groups['gMapGroup_QuantumIsland'].append(name)
        inc=f'\t.include "data/maps/{name}/scripts.inc"'
        if inc not in includes:includes+='\n'+inc+'\n'
    save(f'data/maps/{NAME}/map.json',outdoor)
    save('data/maps/map_groups.json',groups);scripts.write_text(includes)
    out=[f'{NAME}_MapScripts::\n\t.byte 0\n']
    for label,text in [('Guide','This is HAVORA\'s market district!\\nHomes north, shops and harbor south.'),
                       ('Resident','The flower beds soften all this stone.\\nI love living near the waterfront.'),
                       ('Harbor','The ferry pier is just south of here.\\nYou can walk straight to the harbor.'),
                       ('Fisher','Fresh fish arrive with the morning tide.\\nThe market never stays quiet for long.')]:
        out.append(f'{NAME}_{label}::\n\tmsgbox {NAME}_{label}_Text, MSGBOX_NPC\n\tend\n\n{NAME}_{label}_Text::\n\t.string "{text}$"\n')
    out.append(f'''{NAME}_Supplies::
\tlock
\tfaceplayer
\tmessage Text_MayIHelpYou
\twaitmessage
\tpokemart {NAME}_Stock
\tmsgbox Text_PleaseComeAgain
\trelease
\tend

\t.align 2
{NAME}_Stock::
\t.2byte ITEM_POKE_BALL
\t.2byte ITEM_GREAT_BALL
\t.2byte ITEM_SUPER_POTION
\t.2byte ITEM_ANTIDOTE
\t.2byte ITEM_PARALYZE_HEAL
\t.2byte ITEM_REPEL
\t.2byte ITEM_ESCAPE_ROPE
\t.2byte ITEM_NONE
''')
    (R/f'data/maps/{NAME}/scripts.inc').write_text('\n'.join(out))
    save('tools/havora/market-district.json',dict(dimensions=[40,40],buildings=buildings,harbor_unchanged=True))

if __name__=='__main__': build()
