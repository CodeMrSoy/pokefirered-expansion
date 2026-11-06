"""Corvala-specific timber/stilt silhouettes from the supplied concept.

Roof planes, timber framing, recessed doors and porch rails are authored at
native scale. Shared glass colors stay blue under every roof palette.
"""
from PIL import Image,ImageDraw
from houses import kit as native_kit

def timber_house(hip=False):
 """Timber cottage at native scale with roof-independent blue glass."""
 a=Image.new('P',(112,96));d=ImageDraw.Draw(a)
 # Warm plaster panels sit behind a restrained structural timber frame.
 d.polygon([(94,44),(103,39),(103,87),(94,91)],fill=3,outline=2)
 d.rectangle((14,43,94,87),fill=7,outline=2)
 d.rectangle((16,46,92,62),fill=6)
 for y in (54,76,83):d.line((17,y,91,y),fill=5)
 # The roof has a lit top plane, darker side plane, and a deep eave.
 if hip:
  d.polygon([(30,3),(79,3),(103,25),(103,45),(8,45),(8,25)],fill=8,outline=1)
  d.polygon([(30,4),(79,4),(94,24),(17,24)],fill=9)
  d.polygon([(17,25),(94,25),(102,43),(9,43)],fill=10)
  for y in (11,18):
   left=30-(y-4)*13//20;right=79+(y-4)*15//20
   d.line((left,y,right,y),fill=8);d.line((left+1,y+1,right-1,y+1),fill=11)
  for y in (29,36,42):
   d.line((13,y,98,y),fill=9);d.line((13,y+1,99,y+1),fill=11)
   for x in range(20+(y%2)*5,96,16):d.line((x,y+2,x,y+5),fill=9)
  d.line((30,3,79,3),fill=11)
 else:
  d.polygon([(55,27),(8,45),(103,45)],fill=6,outline=2)
  d.polygon([(55,2),(8,19),(8,44),(55,27)],fill=10,outline=1)
  d.polygon([(55,2),(103,19),(103,44),(55,27)],fill=9,outline=1)
  for off in (7,15,23):
   d.line((9,19+off,54,3+off),fill=9);d.line((10,20+off,54,4+off),fill=11)
   d.line((57,3+off,102,19+off),fill=8)
  for x in (21,38,72,89):
   y=19-(x-8)*17//47 if x<55 else 3+(x-55)*17//48
   d.line((x,y+4,x,y+22),fill=9 if x<55 else 8)
  d.line((55,2,55,27),fill=11)
  d.rectangle((51,33,59,40),fill=2);d.rectangle((53,34,57,38),fill=13);d.point((53,34),fill=15)
 # Continuous floor beams and corner posts give the front wall depth.
 d.rectangle((10,44,101,47),fill=2);d.line((10,44,100,44),fill=7)
 d.rectangle((14,63,94,66),fill=3);d.line((15,63,94,63),fill=7)
 for x in (15,44,67,92):
  d.rectangle((x,48,x+2,87),fill=3);d.line((x,48,x,85),fill=6)
 # Every roof variant shares the same four glass colors (indices 12-15).
 for x in (24,73):
  for y in (50,70):
   d.rectangle((x-2,y-1,x+14,y+12),fill=2)
   d.rectangle((x,y,x+12,y+10),fill=12)
   d.rectangle((x+1,y+1,x+11,y+5),fill=13)
   d.line((x+1,y+1,x+5,y+1),fill=15)
   d.line((x+6,y,x+6,y+10),fill=7)
   d.line((x-2,y+12,x+14,y+12),fill=7)
 # Recessed door and a clean porch: the external dock supplies the stilts.
 d.rectangle((48,68,64,90),fill=2);d.rectangle((50,70,62,89),fill=4)
 d.line((51,71,51,87),fill=6);d.line((56,71,56,87),fill=3);d.point((60,81),fill=7)
 d.rectangle((8,88,104,92),fill=5);d.line((8,88,104,88),fill=7)
 d.rectangle((8,93,104,95),fill=2);d.line((9,93,103,93),fill=4)
 for left,right in ((9,42),(69,103)):
  d.line((left,85,right,85),fill=2);d.line((left,84,right,84),fill=6)
  for x in range(left,right+1,11):d.line((x,82,x,91),fill=3);d.point((x,82),fill=7)
 return a

def kit(root,atlas):
 _,provenance=native_kit(root,atlas)
 out={'cerulean':timber_house(),'sevii':timber_house(True),'pallet':timber_house()}
 for name,p in provenance.items():
  p.update(native_reference_column=p['door_column'],reference_only=True,door_column=3,door_row=5,wall_start_row=3,design='Corvala concept: timber frame, two levels, porch and short stilts')
 return out,provenance
