"""Native-pixel dock joinery, Nordic lanterns and complete quay edge variants."""
from PIL import Image, ImageDraw, ImageOps

def waterfront_assets(existing):
    # FireRed/Vermilion timber shades, with the same blue-grey metal as the buildings.
    ink=(64,72,104);dark=(112,80,40);shade=(176,136,72)
    wood=(192,160,88);light=(208,192,128);cap=(224,216,160)
    metal=(120,120,128);metal_light=(200,200,216);glass=(248,224,128)
    assets={}
    def add(name,im,bank=11):assets[name]=(im,bank)
    board=Image.new('RGBA',(16,16),wood);d=ImageDraw.Draw(board)
    for y in [0,4,8,12]:
        d.line((0,y,15,y),fill=shade)
        d.line((0,y+1,15,y+1),fill=light)
        seam=4 if y%8==0 else 12
        d.line((seam,y+1,seam,y+3),fill=shade)
    add('wood',board,12)
    # The rail is continuous between posts instead of alternating bare deck and water.
    rail=Image.new('RGBA',(16,16));d=ImageDraw.Draw(rail)
    d.rectangle((1,0,4,15),fill=dark);d.line((2,0,2,15),fill=light)
    d.line((4,0,4,15),fill=shade)
    add('dock_rail_left',rail);add('dock_rail_right',ImageOps.mirror(rail))
    opening=ImageOps.mirror(rail)
    ImageDraw.Draw(opening).rectangle((0,5,15,11),fill=(0,0,0,0))
    add('dock_boarding_gate',opening)
    ramp=Image.new('RGBA',(16,16));d=ImageDraw.Draw(ramp)
    d.rectangle((0,5,15,11),fill=wood)
    d.line((0,5,15,5),fill=light);d.line((0,11,15,11),fill=dark)
    for x in [3,7,11,15]:d.line((x,6,x,10),fill=shade)
    add('boarding_ramp',ramp)
    head=Image.new('RGBA',(16,16));d=ImageDraw.Draw(head)
    d.rectangle((0,1,15,4),fill=dark);d.line((0,1,15,1),fill=light)
    d.line((0,3,15,3),fill=wood);add('dock_head',head)
    def post(water=False,side='left'):
        im=Image.new('RGBA',(16,16));d=ImageDraw.Draw(im)
        if water:
            d.rectangle((0,0,15,5),fill=wood)
            d.line((0,0,15,0),fill=light)
            d.rectangle((0,6,15,8),fill=dark)
            d.line((0,6,15,6),fill=shade)
        x=2 if side=='left' else 8
        d.rectangle((x+1,5,x+5,15),fill=dark)
        d.line((x+2,7,x+2,14),fill=shade)
        d.rectangle((x,1,x+6,8),fill=ink)
        d.rectangle((x+1,0,x+5,3),fill=cap)
        d.rectangle((x+1,4,x+5,6),fill=wood)
        d.line((x+1,4,x+1,6),fill=light)
        d.line((x+1,10,x+5,10),fill=ink)
        d.line((x+2,10,x+3,10),fill=metal_light)
        return im
    add('dock_post_left',post());add('dock_post_right',post(side='right'))
    add('dock_tip_left',post(True));add('dock_tip_right',post(True,'right'))
    # Standalone pile for west-berth corners: lower half is over water only.
    pile=Image.new('RGBA',(16,32));pile.alpha_composite(post(),(0,0));d=ImageDraw.Draw(pile)
    d.rectangle((3,16,7,28),fill=dark);d.line((4,16,4,27),fill=shade)
    d.line((2,29,8,29),fill=ink);add('pile',pile)
    face=Image.new('RGBA',(32,16));d=ImageDraw.Draw(face)
    d.rectangle((0,0,31,4),fill=wood);d.line((0,0,31,0),fill=light)
    d.rectangle((0,5,31,9),fill=dark);d.line((0,6,31,6),fill=shade)
    for x in [5,21]:
        d.rectangle((x,10,x+3,14),fill=dark);d.line((x,10,x,13),fill=shade)
    add('dock_face',face)
    rope=Image.new('RGBA',(16,16));d=ImageDraw.Draw(rope)
    d.ellipse((2,4,13,12),outline=dark,width=2)
    d.arc((3,4,12,11),180,355,fill=cap,width=2)
    d.ellipse((5,6,10,10),outline=shade)
    d.line((12,10,14,13),fill=dark);add('rope',rope)
    net=Image.new('RGBA',(16,32));d=ImageDraw.Draw(net)
    d.rectangle((7,3,8,27),fill=dark)
    d.polygon([(7,8),(2,27),(7,30),(14,26),(9,9)],fill=shade,outline=dark)
    for y in [14,19,24]:d.line((5,y,11,y),fill=light)
    d.line((6,12,5,27),fill=dark);d.line((10,12,11,27),fill=dark)
    add('net',net)
    gate=Image.new('RGBA',(16,32));d=ImageDraw.Draw(gate)
    d.rectangle((5,9,10,28),fill=dark)
    d.rectangle((6,10,9,26),fill=wood)
    d.rectangle((4,7,11,10),fill=shade,outline=dark)
    d.line((5,7,10,7),fill=cap)
    d.rectangle((4,17,11,19),fill=ink)
    d.line((5,17,10,17),fill=metal_light)
    d.rectangle((3,27,12,30),fill=ink);add('gate',gate)
    # Cast-iron shepherd-hook lantern, sized to the original 16x32 prop footprint.
    lamp=Image.new('RGBA',(16,32));d=ImageDraw.Draw(lamp)
    d.rectangle((4,4,6,28),fill=ink);d.line((5,6,5,26),fill=metal)
    d.line((5,4,8,2,12,2,14,4,14,7),fill=ink,width=2)
    d.line((8,3,11,3),fill=metal)
    d.rectangle((10,8,15,16),fill=ink)
    d.rectangle((11,10,14,14),fill=glass)
    d.line((13,10,13,14),fill=shade)
    d.line((11,10,11,12),fill=(240,240,248))
    d.rectangle((9,7,15,9),fill=ink);d.line((11,7,14,7),fill=metal)
    d.line((11,17,14,17),fill=metal)
    d.rectangle((2,27,8,30),fill=ink);d.line((3,28,7,28),fill=metal)
    add('lamp',lamp,8)
    bollard=Image.new('RGBA',(16,16));d=ImageDraw.Draw(bollard)
    d.rectangle((5,5,10,12),fill=ink);d.line((6,6,6,11),fill=metal)
    d.rectangle((3,4,12,6),fill=ink);d.line((4,4,11,4),fill=metal_light)
    d.rectangle((3,12,12,14),fill=ink);add('bollard',bollard,8)
    # Keep the approved masonry image; extend it with matching coping returns.
    wall=existing['wall'][0]
    for side in ['left','right']:
        corner=wall.crop((0 if side=='left' else 16,0,16 if side=='left' else 32,32))
        d=ImageDraw.Draw(corner)
        x=0 if side=='left' else 15
        d.line((x,3,x,25),fill=(56,56,80))
        d.line((x+(1 if side=='left' else -1),3,x+(1 if side=='left' else -1),24),fill=(104,104,128))
        add('wall_corner_'+side,corner,9)
    # North and side coping sits on paving; no water-backed holes in the promenade.
    rim_light=(200,200,216);rim_mid=(152,152,176);rim_dark=(64,64,88)
    def rim(north=False,west=False,east=False):
        im=Image.new('RGBA',(16,16));d=ImageDraw.Draw(im)
        if north:
            d.rectangle((0,0,15,5),fill=rim_dark)
            d.rectangle((0,1,15,3),fill=rim_mid)
            d.line((0,1,15,1),fill=rim_light)
            d.line((7,1,7,3),fill=rim_dark)
        for x in ([0] if west else [])+([12] if east else []):
            d.rectangle((x,0,x+3,15),fill=rim_dark)
            d.rectangle((x+1,0,x+2,15),fill=rim_mid)
            d.line((x+1,0,x+1,15),fill=rim_light)
            d.line((x+1,7,x+2,7),fill=rim_dark)
        return im
    for name,flags in [('wall_north',(True,False,False)),('wall_west',(False,True,False)),
                       ('wall_east',(False,False,True)),('wall_north_west',(True,True,False)),
                       ('wall_north_east',(True,False,True))]:add(name,rim(*flags),9)
    return assets
