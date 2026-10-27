"""Apply approved color cleanup and FireRed-sized walking sheet corrections."""
from pathlib import Path
import importlib.util
from PIL import Image,ImageDraw
import numpy as np
from scipy.ndimage import label,find_objects
ROOT=Path(__file__).resolve().parents[1]
import subprocess,sys
subprocess.run([sys.executable,str(ROOT/'tools/import_quantum_avatar_art.py')],check=True)
source=ROOT/'graphics/avatars/overworld_polish.png'
art=Image.open(source).convert('RGBA');arr=np.array(art);arr[:,:,3]=np.where(arr[:,:,3]>220,255,0);art=Image.fromarray(arr)
lab,n=label(arr[:,:,3]>220);boxes=[]
for i,s in enumerate(find_objects(lab),1):
 if s and (lab[s]==i).sum()>2000:boxes.append((s[1].start,s[0].start,s[1].stop,s[0].stop))
for row,name in enumerate(('ben','brandon')):
 spec=importlib.util.spec_from_file_location(name,ROOT/f'tools/prepare_{name}_sprites.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 dest=ROOT/'graphics/avatars'/name
 colors=[tuple(map(int,l.split())) for l in (dest/'overworld.pal').read_text().splitlines()[4:]]
 bb=sorted([b for b in boxes if (b[1]<400)==(row==0)])
 assert len(bb)==9
 sheet=Image.new('RGBA',(144,32))
 for i,b in enumerate(bb):
  im=art.crop(b);im.thumbnail((14,19),Image.Resampling.NEAREST)
  # FireRed Red is 19 visible pixels tall, feet on row 30.
  sheet.paste(im,(i*16+(16-im.width)//2,31-im.height))
 m.indexed(sheet,colors).save(dest/'normal.png',bits=4)
 m.indexed(sheet.crop((0,12,16,28)),colors).save(dest/'map.png',bits=4)
 sr=Image.open(dest/'surf_run.png').convert('RGBA')
 for i,j in enumerate((3,4,0,5,6,1,7,8,2)):
  sr.paste(sheet.crop((j*16,0,j*16+16,32)),((i+3)*16,0))
 m.indexed(sr,colors).save(dest/'surf_run.png',bits=4)
 # Match each activity silhouette to the corresponding native Red frame bounds.
 for asset,width,base in [('bike',32,'red_bike'),('item',16,'red_item'),('fish',32,'red_fish'),('vs_seeker_bike',32,'red_vs_seeker_bike')]:
  original=Image.open(ROOT/f'graphics/object_events/pics/people/{base}.png').convert('RGBA')
  current=Image.open(dest/(asset+'.png')).convert('RGBA');aligned=Image.new('RGBA',current.size)
  for k in range(current.width//width):
   frame=current.crop((k*width,0,(k+1)*width,32));bounds=frame.getbbox()
   target=original.crop((k*width,0,(k+1)*width,32)).getbbox()
   if bounds and target:
    piece=frame.crop(bounds).resize((target[2]-target[0],target[3]-target[1]),Image.Resampling.NEAREST)
    aligned.paste(piece,(k*width+target[0],target[1]))
  m.indexed(aligned,colors).save(dest/(asset+'.png'),bits=4)
 # Native palette ground shadow, kept separate from transparent leg gap.
 front=Image.open(dest/'front.png').convert('RGBA');up=Image.new('RGBA',(64,64));up.paste(front,(0,-2))
 shadow=Image.new('RGBA',(64,64));ImageDraw.Draw(shadow).ellipse((12,60,51,63),fill=(72,72,80,255));shadow.alpha_composite(up)
 m.indexed(shadow,colors).save(dest/'front.png',bits=4)
