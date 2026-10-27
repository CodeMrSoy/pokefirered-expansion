"""Corvala-specific timber/stilt silhouettes from the supplied concept.

Native FireRed window and door pixels are reused at 1x. Roofs, framing and
porches are new code-native tiles; these are not unmodified Kanto houses.
"""
from PIL import Image,ImageDraw
from houses import kit as native_kit

def timber_house(window,door,hip=False):
 a=Image.new('P',(112,96));d=ImageDraw.Draw(a)
 # Small exposed side face and a dark underside give the facade thickness.
 d.polygon([(96,44),(102,41),(102,86),(96,90)],fill=3,outline=2)
 d.rectangle((14,40,97,86),fill=6,outline=2)
 for x in range(18,96,6):d.line((x,43,x,85),fill=5)
 # Deep roof planes: ridge runs away from the viewer; its front sits lower.
 if hip:
  d.polygon([(32,3),(79,3),(104,25),(104,46),(7,46),(7,25)],fill=8,outline=1)
  d.polygon([(32,4),(79,4),(96,24),(15,24)],fill=9)
  d.polygon([(15,25),(96,25),(103,44),(8,44)],fill=10)
  for y in [29,35,41]:
   d.line((13,y,98,y),fill=9);d.line((13,y+1,99,y+1),fill=11)
   for x in range(20+(y%2)*4,95,12):d.line((x,y+2,x+1,y+5),fill=9)
  for y in [11,19]:
   left=32-(y-4)*17//20;right=79+(y-4)*17//20
   d.line((left,y,right,y),fill=8);d.line((left+1,y+1,right-1,y+1),fill=11)
  d.line((32,3,79,3),fill=11,width=2)
 else:
  # Timber front gable lies below two visible sloping roof planes.
  d.polygon([(56,27),(8,46),(104,46)],fill=6,outline=2)
  for x in range(18,98,7):d.line((x,44,x,44-(abs(56-x)//3)),fill=5)
  d.polygon([(56,2),(8,20),(8,46),(56,28)],fill=10,outline=1)
  d.polygon([(56,2),(103,20),(103,46),(56,28)],fill=9,outline=1)
  for i in [7,14,21]:
   d.line((10,20+i,54,3+i),fill=11);d.line((58,3+i,101,20+i),fill=8)
  for x in range(17,53,9):
   y=20-(x-8)*18//48
   d.line((x,y+2,x,y+23),fill=9)
  for x in range(64,101,9):
   y=3+(x-56)*18//47
   d.line((x,y+2,x,y+23),fill=8)
  d.line((56,2,56,28),fill=11,width=2)
  d.rectangle((51,33,60,41),fill=3);d.rectangle((53,34,58,39),fill=14)
  d.line((55,34,55,39),fill=7);d.line((53,37,58,37),fill=7)
 # Overhang, raised framing, and corner braces are consistently lit from upper-left.
 d.line((10,46,101,46),fill=2,width=3);d.line((11,45,100,45),fill=7)
 for x in [15,44,67,94]:
  d.rectangle((x,48,x+2,86),fill=3);d.line((x,48,x,85),fill=7)
 for x in [17,82]:
  d.line((x,64,x+10,75),fill=3,width=3);d.line((x+1,64,x+11,75),fill=7)
 d.rectangle((15,63,96,66),fill=3);d.line((16,63,95,63),fill=7)
 # Native-size windows: two levels, independent blue glass in the timber bank.
 for x in [23,74]:
  for y in [49,70]:a.paste(window,(x,y))
 d.rectangle((48,68,64,86),fill=2);a.paste(door,(49,70))
 # Usable porch with solid timber fascia and short stilt ends underneath.
 d.rectangle((8,86,104,90),fill=5);d.line((8,86,104,86),fill=7)
 d.line((8,90,104,90),fill=2,width=2)
 for x in [12,32,80,100]:
  d.rectangle((x,91,x+2,95),fill=2);d.line((x,91,x,94),fill=6)
 # Low porch railing leaves a native-width gap directly in front of the door.
 for left,right in [(10,43),(69,102)]:
  d.line((left,83,right,83),fill=3);d.line((left,82,right,82),fill=7)
  for x in range(left,right+1,8):d.line((x,81,x,87),fill=3);d.point((x,81),fill=7)
 return a

def kit(root,atlas):
 native,provenance=native_kit(root,atlas)
 window=native['pallet'].crop((16,62,32,74))
 door=native['sevii'].crop((16,80,32,96))
 out={'cerulean':timber_house(window,door),'sevii':timber_house(window,door,True),'pallet':timber_house(window,door)}
 for name,p in provenance.items():
  p.update(native_reference_column=p['door_column'],reference_only=True,door_column=3,door_row=5,wall_start_row=3,design='Corvala concept: timber frame, two levels, porch and short stilts')
 return out,provenance
