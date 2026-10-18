"""Assemble harbor exteriors from native FireRed tiles, without pixel scaling."""
from PIL import Image, ImageDraw
from render import atlas

def exteriors():
    native = atlas('vermilion_city', 'general')
    # Original Vermilion roof ends, eaves, windows and closed door facade.
    rows = [
        [0x2bb, 0x2bc, 0x2bc, 0x2bc, 0x2bd],
        [0x2a8, 0x2a9, 0x2a9, 0x2a9, 0x2aa],
        [0x2b0, 0x2a7, 0x2b1, 0x2a7, 0x2b2],
        [0x2b8, 0x2ab, 0x29e, 0x2ac, 0x2ba],
    ]
    result = {}
    # Four discrete coastal roof shades; retain the native roof pixel patterns.
    roof_colors = {
        'warehouse': [(64, 88, 120), (72, 120, 168), (104, 152, 192), (144, 184, 216)],
        'fish_store': [(56, 96, 88), (64, 136, 120), (96, 168, 144), (144, 200, 168)],
        'office': [(64, 88, 120), (72, 120, 168), (104, 152, 192), (144, 184, 216)],
    }
    for name, colors in roof_colors.items():
        grid = rows if name != 'office' else [
            [0x2bb, 0x2bc, 0x2bc, 0x2bd],
            [0x2b0, 0x2a7, 0x2a7, 0x2b2],
            [0x2b8, 0x2ab, 0x29e, 0x2ba],
        ]
        im = Image.new('RGBA', (len(grid[0])*16, len(grid)*16))
        for y, row in enumerate(grid):
            for x, mid in enumerate(row):
                tile = native[mid].convert('RGBA')
                for py in range(16):
                    for px in range(16):
                        r,g,b,a = tile.getpixel((px,py))
                        # Native grass visible outside roof corners is transparent.
                        if g > r*1.15 and g > b*1.08:
                            tile.putpixel((px,py),(0,0,0,0))
                        elif y < len(grid)-1 and r > 160 and g > 100 and b < 110:
                            # Recolor only orange/yellow roofing; keep native pixel pattern.
                            tone = 0 if g < 136 else 1 if g < 168 else 2 if g < 200 else 3
                            tile.putpixel((px,py),(*colors[tone],255))
                im.alpha_composite(tile,(x*16,y*16))
        result[name] = im

    # A small GBA fixture: one-pixel silhouette, three metal shades, no glow/texture.
    lamp = Image.new('RGBA',(16,32))
    d = ImageDraw.Draw(lamp)
    outline='#384850';dark='#586870';light='#98a8a8'
    d.rectangle((7,10,8,28),fill=outline)
    d.line((7,11,7,27),fill=light)
    d.rectangle((5,27,10,30),fill=outline)
    d.rectangle((6,28,9,29),fill=dark)
    d.rectangle((4,3,11,10),fill=outline)
    d.rectangle((5,4,10,8),fill='#f8e8a0')
    d.line((7,4,7,8),fill='#b0a878')
    d.rectangle((5,2,10,3),fill=dark)
    d.line((6,1,9,1),fill=outline)
    d.line((5,10,10,10),fill=dark)
    result['lamp'] = lamp
    return result
