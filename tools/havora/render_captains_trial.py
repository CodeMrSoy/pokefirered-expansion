"""Native tile render for the private Captain's Trial pair (not Porymap)."""
from pathlib import Path
import json,struct
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[2]
def render(out):
 T=[Image.open(R/'data/tilesets/primary/havora_gym/tiles.png'),Image.open(R/'data/tilesets/secondary/havora_city/tiles.png')];pals=[];metas=[]
 for i in range(13):
  p=R/f'data/tilesets/{"primary" if i<7 else "secondary"}/havora_gym/palettes/{i:02}.pal';pals.append([tuple(map(int,l.split())) for l in p.read_text().splitlines()[3:19]])
 for group in ['primary','secondary']:
  b=(R/f'data/tilesets/{group}/havora_gym/metatiles.bin').read_bytes();w=struct.unpack('<'+'H'*(len(b)//2),b)
  for i in range(0,len(w),8):
   im=Image.new('RGB',(16,16))
   for k,v in enumerate(w[i:i+8]):
    n=v&1023;g=int(n>=640);n=n-640 if g else n;source=T[g]
    for y in range(8):
     for x in range(8):
      c=source.getpixel((n%16*8+(7-x if v&1024 else x),n//16*8+(7-y if v&2048 else y)))
      if c or k<4:im.putpixel((k%2*8+x,k%4//2*8+y),pals[v>>12][c])
   metas.append(im)
 layout=next(l for l in json.loads((R/'data/layouts/layouts.json').read_text())['layouts'] if l['id']=='LAYOUT_HAVORA_CAPTAINS_TRIAL');W,H=layout['width'],layout['height']
 b=(R/'data/layouts/HavoraCaptainsTrial/map.bin').read_bytes();w=struct.unpack('<'+'H'*(len(b)//2),b);im=Image.new('RGB',(W*16,H*16))
 for i,v in enumerate(w):im.paste(metas[v&1023],(i%W*16,i//W*16))
 im=im.convert('RGBA')
 objects=json.loads((R/'data/maps/QuantumHavoraGym/map.json').read_text())['object_events']
 for o in sorted(objects,key=lambda v:v['y']):
  root=R/'graphics/object_events';sailor=o['graphics_id']=='OBJ_EVENT_GFX_SAILOR';pic='sailor' if sailor else 'gym_guy';pal='npc_pink' if sailor else 'npc_white'
  sprite=Image.open(root/f'pics/people/{pic}.png').crop((0,0,16,32));colors=[tuple(map(int,line.split())) for line in (root/f'palettes/{pal}.pal').read_text().splitlines()[3:19]];sprite.putpalette(sum((list(c) for c in colors),[])+[0]*720);sprite.info['transparency']=0;im.alpha_composite(sprite.convert('RGBA'),(o['x']*16,o['y']*16-16))
 im=im.convert('RGB')
 im.save(Path(out).with_name('captains-trial-clean.png'))
 d=ImageDraw.Draw(im)
 for x,y,t in [(7,14,'A'),(34,14,'B'),(64,14,'C'),(39,18,'SERVICE WINCH'),(64,18,'CAPTAIN'),(1,35,'ENTRANCE')]:d.text((x*16,y*16),t,fill='white',stroke_width=2,stroke_fill='black')
 im.save(out)
if __name__=='__main__':
 p=R/'docs/havora/review/captains-trial.png';p.parent.mkdir(parents=True,exist_ok=True);render(p)
