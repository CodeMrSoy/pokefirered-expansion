#!/usr/bin/env python3
"""Reproduce pre-redraw Bag icons and independent 64px transition/Bag art."""
from pathlib import Path
import numpy as np
from PIL import Image
ROOT = Path(__file__).resolve().parents[1]
NAMES = ('shears','gloves','lantern','whistle','hammer','bait','wailmer_wailer')
def convert(name,size,margin,directory):
    source=Image.open(ROOT/'tools/field_tool_sources'/(name+'.png')).convert('RGBA')
    alpha=source.getchannel('A').point(lambda a:255 if a>=128 else 0)
    source.putalpha(alpha);source=source.crop(alpha.getbbox())
    source.thumbnail((size-2*margin,size-2*margin),Image.Resampling.NEAREST)
    pixels=np.array(source);opaque=pixels[:,:,3]>=128
    foreground=(pixels[:,:,:3][opaque]>>3)<<3
    strip=Image.fromarray(foreground.reshape(1,-1,3))
    q=strip.quantize(colors=15,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE)
    palette=[0,0,0]+[(c>>3)<<3 for c in q.getpalette()[:45]]
    palette += [0]*(768-len(palette))
    indices=np.zeros(opaque.shape,dtype=np.uint8);indices[opaque]=np.asarray(q).ravel()+1
    icon=Image.fromarray(indices);icon.putpalette(palette)
    canvas=Image.new('P',(size,size));canvas.putpalette(palette)
    canvas.paste(icon,((size-icon.width)//2,(size-icon.height)//2))
    assert max(canvas.get_flattened_data())<16
    directory.mkdir(parents=True,exist_ok=True)
    canvas.save(directory/(name+'.png'),transparency=0)
    (directory/(name+'.pal')).write_text('JASC-PAL\n0100\n16\n'+'\n'.join(' '.join(map(str,palette[i:i+3])) for i in range(0,48,3))+'\n')
def import_case():
    source=Image.open(ROOT/'tools/field_tool_sources/field_item_case.png').convert('RGBA')
    assert source.size==(24,24)
    pixels=np.array(source);opaque=pixels[:,:,3]>=128
    rgb=(pixels[:,:,:3][opaque]>>3)<<3
    q=Image.fromarray(rgb.reshape(1,-1,3)).quantize(colors=15,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE)
    palette=[0,0,0]+[(c>>3)<<3 for c in q.getpalette()[:45]]
    palette += [0]*(768-len(palette))
    indices=np.zeros((24,24),dtype=np.uint8);indices[opaque]=np.asarray(q).ravel()+1
    icon=Image.fromarray(indices);icon.putpalette(palette)
    icon.save(ROOT/'graphics/items/field_item_case.png',transparency=0)
    (ROOT/'graphics/items/field_item_case.pal').write_text('JASC-PAL\n0100\n16\n'+'\n'.join(' '.join(map(str,palette[i:i+3])) for i in range(0,48,3))+'\n')

if __name__=='__main__':
    for name in NAMES:
        convert(name,64,2,ROOT/'graphics/field_effects/field_tools')
    import_case()
