"""Import approved review sheets; export aligned native FireRed avatar art."""
from pathlib import Path
from PIL import Image
import importlib.util
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
BOXES={
'ben':[(364,26,642,456),(434,476,549,653),(631,476,742,653),(823,476,939,653),(431,665,549,856),(623,665,742,855),(823,665,943,856),(433,872,552,1083),(619,872,742,1083),(822,872,943,1083)],
'brandon':[(104,45,478,639),(180,680,324,910),(437,681,585,920),(693,681,845,919),(176,948,325,1197),(435,948,585,1206),(698,947,853,1206),(173,1224,324,1495),(433,1226,586,1496),(698,1228,852,1498)]}
def fit(im,size):
 im=im.copy();im.thumbnail(size,Image.Resampling.NEAREST)
 out=Image.new('RGBA',size);out.paste(im,((size[0]-im.width)//2,size[1]-im.height));return out
for name,boxes in BOXES.items():
 dest=ROOT/'graphics/avatars'/name;source=dest/'source'
 art=Image.open(source/'approved.png').convert('RGBA')
 # Discard faint presentation glow and alpha fringes during native conversion.
 a=np.array(art);a[:,:,3]=np.where(a[:,:,3]>=220,255,0);art=Image.fromarray(a)
 front=fit(art.crop(boxes[0]),(60,60));canvas=Image.new('RGBA',(64,64));canvas.paste(front,(2,4));canvas.save(source/'battle_front_64x64.png')
 frames=[fit(art.crop(b),(16,32)) for b in boxes[1:]]
 frames[0].save(source/'overworld_down_16x32.png')
 spec=importlib.util.spec_from_file_location(name,ROOT/f'tools/prepare_{name}_sprites.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);mod.main()
 # Native FireRed order is idle down/up/left, then the two steps per direction.
 order=[0,3,6,1,2,4,5,7,8];normal=Image.new('RGBA',(144,32))
 for i,j in enumerate(order):normal.paste(frames[j],(i*16,0))
 colors=[tuple(map(int,l.split())) for l in (dest/'overworld.pal').read_text().splitlines()[4:]]
 mod.indexed(normal,colors).save(dest/'normal.png',bits=4)
 mod.indexed(frames[0].crop((0,4,16,20)),colors).save(dest/'map.png',bits=4)
 # Match front/back running directions to the approved walking frames.
 sheet=Image.open(dest/'surf_run.png').convert('RGBA')
 for i,j in enumerate([1,2,0,4,5,3,7,8,6]):sheet.paste(frames[j],((i+3)*16,0))
 mod.indexed(sheet,colors).save(dest/'surf_run.png',bits=4)
