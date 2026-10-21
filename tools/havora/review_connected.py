import sys,json,re
from pathlib import Path
from collections import deque
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(R/'tools/havora'))
from review_market import scene
names=['QuantumHavoraNorthQuay','QuantumHarbor','QuantumHavoraWestQuay','QuantumPortCity','QuantumHavoraNorthDistrict','QuantumHavoraCoastalDaycare','QuantumHavoraNorthWalk','QuantumHavoraCliffs']
meta={n:json.loads((R/f'data/maps/{n}/map.json').read_text()) for n in names}
layouts={l['id']:l for l in json.loads((R/'data/layouts/layouts.json').read_text())['layouts']}
def constant(n):return 'MAP_'+re.sub(r'(?<!^)(?=[A-Z])','_',n).upper()
lookup={constant(n):n for n in names}
pos={names[0]:(0,0)};q=deque(pos)
while q:
 n=q.popleft();a=layouts[meta[n]['layout']];x,y=pos[n]
 for c in meta[n]['connections'] or []:
  m=lookup.get(c['map'])
  if not m:continue
  b=layouts[meta[m]['layout']];off=int(c['offset']);dr=c['direction']
  p={'right':(x+a['width'],y+off),'left':(x-b['width'],y+off),'up':(x+off,y-b['height']),'down':(x+off,y+a['height'])}[dr]
  if m in pos:assert pos[m]==p,(m,pos[m],p)
  else:pos[m]=p;q.append(m)
assert len(pos)==len(names)
x0=min(x for x,y in pos.values());y0=min(y for x,y in pos.values())
x1=max(pos[n][0]+layouts[meta[n]['layout']]['width'] for n in names)
y1=max(pos[n][1]+layouts[meta[n]['layout']]['height'] for n in names)
margin=48;top=150;bottom=106
W=(x1-x0)*16+2*margin;H=(y1-y0)*16+top+bottom
im=Image.new('RGB',(W,H),'#132530');d=ImageDraw.Draw(im)
fontpath='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
f=lambda s:ImageFont.truetype(fontpath,s)
for k in range(-H,W,40):d.line((k,top,k+H,H-bottom),fill='#203440',width=1)
d.rectangle((0,0,W,top-1),fill='#132530');d.rectangle((0,H-bottom,W,H),fill='#132530')
d.text((margin,28),'HAVORA  /  CONNECTED CITY OVERVIEW',font=f(38),fill='#f5e8cc')
d.text((margin,85),'Current map tiles + NPC sprites • Actual connection offsets • North at top',font=f(23),fill='#b9cbd1')
rects={}
for n in names:
 x,y=pos[n];px=margin+(x-x0)*16;py=top+(y-y0)*16
 s=scene(n,meta[n]['layout']);im.paste(s,(px,py));rects[n]=(px,py,px+s.width,py+s.height)
# Small inset labels identify districts without rearranging their geography.
labels={names[0]:'3  MARKET + HOMES',names[1]:'4  HAVORA HARBOR',names[2]:'7  QUAY STAIRS',names[3]:'2  WESTERN GYM HILLS',names[4]:'1  NORTH DISTRICT',names[5]:'5  COASTAL DAYCARE',names[6]:'6  NORTH WALK',names[7]:'8  COASTAL CLIFFS'}
for n,label in labels.items():
 x,y,r,b=rects[n];d.rectangle((x,y,r-1,b-1),outline='#f3d792',width=1)
 if label:
  size=10 if n==names[2] else 18 if n==names[6] else 21;ff=f(size);tw=d.textbbox((0,0),label,font=ff)[2]
  d.rectangle((x+5,y+5,x+tw+25,y+40),fill='#142935');d.text((x+15,y+9),label,font=ff,fill='#f4dfb4')
# Put explanatory key in genuinely unmapped space east of the harbor.
kx=margin+(44-x0)*16;ky=top+(26-y0)*16
key=[('READING THIS VIEW',26),('Gold lines show map boundaries.',21),('Paths cross at their real positions.',21),('',15),('Dark hatching = unmapped space.',21),('No terrain has been invented',21),('to fill the gaps between maps.',21),('',15),('1  Pokémon Center + Poké Mart',21),('2  Gym + cliffside residences',21),('3  Market + residential terrace',21),('4  Ferry + docks + lighthouse',21),('5  Daycare + coastal paddock',21),('6  Northern lookout + Minior site',21),('7  Terraced quay stair connection',21),('8  Coastal cliff extension',21)]
for line,size in key:
 d.text((kx,ky),line,font=f(size),fill='#f4dfb4' if size==26 else '#c0d1d8');ky+=39
# Identify the slim west quay, whose visible seam joins the two halves.
x,y,r,b=rects[names[2]]
d.text((kx,ky+30),'West quay joins the western hills',font=f(21),fill='#c0d1d8')
d.text((kx,ky+68),'to the market and harbor.',font=f(21),fill='#c0d1d8')
d.text((margin,H-bottom+20),'Native tile render — not a Porymap screenshot.  One square on the game map = 16 × 16 pixels here.',font=f(23),fill='#c0d1d8')
d.text((margin,H-bottom+58),'Havora-Development · Coastal neighborhood refinement · Outdoor districts shown; interiors omitted.',font=f(21),fill='#8fa8b4')
out=sys.argv[1] if len(sys.argv)>1 else str(R/'build/Havora_Connected_Overview.png');im.save(out)
print(json.dumps({'output':out,'size':im.size,'origins':pos},indent=2))
