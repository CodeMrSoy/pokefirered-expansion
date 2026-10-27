"""Native-resolution Nordic silhouettes with FireRed material ramps and details.

General roofs/windows and Vermilion walls/door 0x29e are the material references.
No resampled concept-image pixels enter these buildings.
"""
from PIL import Image, ImageDraw
from render import atlas

def gba(rgb):
    return tuple((v >> 3) << 3 for v in rgb)

def exteriors():
    native = atlas('vermilion_city', 'general')
    # Exact colors from General roofing/windows and Vermilion wall metatiles.
    ink = gba((65,74,106))
    roof_shadow = gba((74,131,197))
    roof = gba((98,164,222))
    roof_light = gba((115,189,246))
    roof_edge = gba((156,213,255))
    timber_shadow = gba((197,164,90))
    timber = gba((238,205,123))
    timber_light = gba((255,230,131))
    stone = gba((123,123,131))
    frame = gba((205,205,222))
    pale = gba((246,246,255))
    # Timber frame shades from Vermilion secondary banks 10 and 02.
    beam = gba((115,82,41))
    beam_light = gba((156,123,98))
    palette = [ink,roof_shadow,roof,roof_light,roof_edge,timber_shadow,
               timber,timber_light,stone,frame,pale,beam,beam_light]
    def native_detail(mid, box=None):
        tile = native[mid].crop(box) if box else native[mid]
        out = tile.convert('RGBA')
        for y in range(out.height):
            for x in range(out.width):
                rgb = out.getpixel((x,y))[:3]
                color = min(palette,key=lambda c:sum((a-b)**2 for a,b in zip(c,rgb)))
                out.putpixel((x,y),(*color,255))
        return out
    window = native_detail(0x006,(0,0,13,10))
    door = native_detail(0x29e)
    def crate(d,x,y):
        d.rectangle((x,y,x+11,y+11),fill=timber,outline=ink)
        d.rectangle((x+2,y+2,x+9,y+9),outline=timber_shadow)
        d.line((x+2,y+8,x+8,y+2),fill=timber_shadow,width=2)
        d.line((x+1,y+1,x+10,y+1),fill=timber_light)
    def gabled_house(fish=False):
        im=Image.new('RGBA',(80,96));d=ImageDraw.Draw(im)
        d.rectangle((62,14,69,39),fill=stone,outline=ink)
        d.rectangle((61,12,70,15),fill=frame,outline=ink)
        d.line((64,17,64,29),fill=frame)
        # A 28px-deep ridge preserves the tall gable instead of a flat roof rectangle.
        left=[(42,4),(5,34),(5,62),(42,32)]
        right=[(42,4),(74,34),(74,62),(42,32)]
        d.polygon(left,fill=roof,outline=ink)
        d.polygon(right,fill=roof_shadow,outline=ink)
        for offset in [7,14,21]:
            d.line((6,34+offset,41,5+offset),fill=roof_light)
            d.line((44, 2+offset,73,34+offset),fill=roof)
            for x in range(12+(offset//7%2)*4,39,8):
                y=34-(x-5)*30//37+offset-4
                d.line((x,y,x,y+2),fill=roof_shadow)
            for x in range(49+(offset//7%2)*4,71,8):
                y=4+(x-42)*30//32+offset-4
                d.line((x,y,x,y+2),fill=roof)
        d.line((6,34,41,5),fill=roof_edge)
        d.line((42,5,42,31),fill=roof_light)
        d.polygon([(8,62),(42,33),(71,62),(71,91),(8,91)],fill=timber,outline=ink)
        for y in [55,61,69,77,85]:
            if y<62:
                half=(y-33)*33//29
                d.line((max(10,42-half),y,min(69,42+half),y),fill=timber_shadow)
            else:d.line((10,y,69,y),fill=timber_shadow)
        d.line((8,61,42,33,71,61),fill=ink,width=3)
        d.line((8,59,41,31),fill=roof_light)
        d.line((43, 15,72,61),fill=roof)
        d.rectangle((9,62,70,65),fill=beam)
        d.line((10,62,69,62),fill=beam_light)
        d.line((18,59,39,39),fill=beam,width=2)
        d.line((45,39,64,59),fill=beam,width=2)
        for x in [10,29,52,68]:
            d.rectangle((x,65,x+2,90),fill=beam)
            d.line((x,66,x,89),fill=beam_light)
        d.line((11,89,69,89),fill=beam,width=2)
        im.alpha_composite(window,(14,70));im.alpha_composite(window,(54,70))
        d.line((13,81,27,81),fill=ink);d.line((54,81,67,81),fill=ink)
        d.rectangle((32,69,51,91),fill=ink)
        d.rectangle((34,71,49,75),fill=timber_shadow)
        im.alpha_composite(door,(34,76))
        d.line((33,93,52,93),fill=frame,width=2)
        d.line((8,92,30,92),fill=stone,width=2)
        d.line((54,92,71,92),fill=stone,width=2)
        if fish:
            d.rectangle((28,49,55,60),fill=ink)
            d.rectangle((29,50,54,59),fill=timber_light)
            d.polygon([(32,54),(36,51),(46,51),(50,54),(46,57),(36,57)],fill=roof_shadow)
            d.polygon([(48,54),(52,51),(52,57)],fill=roof_shadow)
            d.point((36,53),fill=pale)
        else:
            d.rectangle((36,46,48,59),fill=timber_shadow)
            d.rectangle((37,47,47,58),fill=ink)
            d.rectangle((38,48,46,56),fill=roof_shadow)
            d.rectangle((38,48,46,50),fill=roof_light)
            d.line((42,48,42,57),fill=frame)
            d.line((38,52,46,52),fill=frame)
        crate(d,4,83)
        if fish:
            d.rectangle((61,84,75,93),fill=timber_shadow,outline=ink)
            d.line((62,87,74,87),fill=timber_light)
            d.line((62,90,74,90),fill=timber_light)
        else:crate(d,64,83)
        return im
    def dock_office():
        im=Image.new('RGBA',(64,64));d=ImageDraw.Draw(im)
        d.rectangle((7,30,57,59),fill=timber,outline=ink)
        for y in [37,45,53]:d.line((9,y,55,y),fill=timber_shadow)
        d.polygon([(10,9),(53,9),(62,32),(2,32)],fill=roof,outline=ink)
        for y in [15,21,27]:d.line((9-(y-9)//4,y,54+(y-9)//4,y),fill=roof_light)
        d.line((11,10,52,10),fill=roof_edge)
        d.rectangle((4,32,59,35),fill=roof_shadow)
        d.polygon([(18,34),(32,19),(46,34)],fill=timber,outline=ink)
        d.line((18,33,32,18,46,33),fill=ink,width=3)
        d.line((19,31,32,17),fill=roof_light)
        d.rectangle((29,26,35,31),fill=roof_shadow,outline=ink)
        for x in [9,23,40,54]:d.rectangle((x,36,x+1,58),fill=beam)
        im.alpha_composite(window,(9,39));im.alpha_composite(window,(42,39))
        d.rectangle((23,37,40,60),fill=ink);im.alpha_composite(door,(24,44))
        d.line((7,61,22,61),fill=stone,width=2)
        d.line((24,62,40,62),fill=frame,width=2)
        d.line((42,61,57,61),fill=stone,width=2)
        return im
    lamp=Image.new('RGBA',(16,32));d=ImageDraw.Draw(lamp)
    d.rectangle((7,11,8,28),fill=ink);d.line((7,12,7,27),fill=stone)
    d.rectangle((5,28,10,30),fill=ink);d.line((6,28,9,28),fill=frame)
    d.rectangle((4,4,11,10),fill=ink);d.rectangle((5,5,10,8),fill=timber_light)
    d.line((7,5,7,8),fill=timber_shadow)
    d.polygon([(3,4),(7,1),(8,1),(12,4)],fill=ink)
    d.line((6,3,9,3),fill=stone);d.rectangle((5,10,10,11),fill=stone)
    return {'warehouse':gabled_house(),'fish_store':gabled_house(True),
            'office':dock_office(),'lamp':lamp}
