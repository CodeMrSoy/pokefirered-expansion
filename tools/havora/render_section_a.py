"""Render the current Section A profiles directly from native metatiles."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import sys
import render,overhead_lock_geometry as g
R=Path(__file__).resolve().parents[2]
p=R/'data/tilesets/secondary/havora_gym/tiles.png';created=not p.exists()
if created:p.symlink_to('../havora_city/tiles.png')
try:tiles=render.atlas('havora_gym','havora_gym')
finally:
 if created:p.unlink()
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',22)
out=Image.new('RGB',(1344,480),'#152232');d=ImageDraw.Draw(out)
for level,name in enumerate(['LOW','MID','HIGH']):
 b=g.draw(((level,0,0),0,0,4,0,False))
 for y in range(27):
  for x in range(28):out.paste(tiles[b[y*80+x]&1023],(level*448+x*16,48+y*16))
 d.text((level*448+14,10),'SECTION A — '+name,font=font,fill='white')
p=Path(sys.argv[1]) if len(sys.argv)>1 else R/'docs/havora/review/section-a-low-mid-high.png'
out.save(p);print(p.resolve())
