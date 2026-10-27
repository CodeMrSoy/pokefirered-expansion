"""Use existing FireRed art at native resolution; no third-party assets imported."""
from PIL import Image,ImageDraw
import art

def material(image,bank,allowed=None):
    colors=art.PALETTES[bank-7];allowed=allowed or range(1,16)
    out=Image.new('P',image.size)
    out.putdata([min(allowed,key=lambda i:sum((a-b)**2 for a,b in zip(rgb,colors[i]))) for rgb in image.convert('RGB').getdata()])
    return out

def install(native):
    # General's actual complete broadleaf tree is 14/15, 1c/1d, 24/25.
    # Keep its canopy silhouette, leaf clusters, trunk and cast shadow intact.
    tree=Image.new('RGB',(32,48))
    for y,row in enumerate([[0x14,0x15],[0x1c,0x1d],[0x24,0x25]]):
        for x,mid in enumerate(row):tree.paste(native[mid],(x*16,y*16))
    tree=material(tree,8)
    art.coastal_tree=lambda:tree.copy()
    def cliff(mask=0,variant=0):
        # Native General ledge cap and vertical rock face establish the depth.
        mid=0x79 if mask&4 else 0x71
        result=material(native[mid],8,[1,2,3,4,5,6,7,14,15])
        d=ImageDraw.Draw(result)
        if mask&1:d.line((0,0,15,0),fill=11,width=2)
        if mask&4:d.line((0,15,15,15),fill=2)
        if variant:d.point((3,10),fill=6);d.point((12,6),fill=3)
        return result
    art.cliff=cliff
