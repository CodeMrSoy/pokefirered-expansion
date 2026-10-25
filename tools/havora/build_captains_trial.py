"""Build a private gym pair from native Havora/FR artwork; never edits city art."""
from pathlib import Path
import json,struct,shutil
R=Path(__file__).resolve().parents[2]
M=[];A=[]
for g in ['primary','secondary']:
 p=R/f'data/tilesets/{g}/havora_city';b=(p/'metatiles.bin').read_bytes();M+=list(struct.unpack('<'+'H'*(len(b)//2),b));b=(p/'metatile_attributes.bin').read_bytes();A+=list(struct.unpack('<'+'I'*(len(b)//4),b))
# Private metatile definitions reuse the exact city graphics and palettes.
# Existing native wood, water, posts and boat pixels are not redrawn.
for mid,base,overlay in [(0x300,0x281,0x233),(0x301,0x281,0x235),(0x302,0x281,0x237),(0x303,0x281,0x23c)]:
 M[mid*8:(mid+1)*8]=M[base*8:base*8+4]+M[overlay*8+4:overlay*8+8];A[mid]=0x20000000
for mid in range(0x2bc,0x2c5):A[mid]=0x20000000
# Sinking gate posts serve as the shipyard's sluice barrier.
M[0x304*8:0x305*8]=M[0x281*8:0x281*8+4]+M[0x231*8+4:0x232*8];A[0x304]=0
# Exit uses native warp-down behavior over the stone entrance floor.
M[0x305*8:0x306*8]=M[0x280*8:0x281*8];A[0x305]=0x65
for g,start,end in [('primary',0,640),('secondary',640,1024)]:
 p=R/f'data/tilesets/{g}/havora_gym';p.mkdir(parents=True,exist_ok=True)
 (p/'metatiles.bin').write_bytes(struct.pack('<'+'H'*((end-start)*8),*M[start*8:end*8]));(p/'metatile_attributes.bin').write_bytes(struct.pack('<'+'I'*(end-start),*A[start:end]))
W,H=40,36;blocked=lambda t:0x3400|t;b=[blocked(0x33)]*(W*H)
def rect(x,y,w,h,t,collision=False,elevation=3):
 for yy in range(y,y+h):
  for xx in range(x,x+w):b[yy*W+xx]=(elevation<<12)|(0x400 if collision else 0)|t
rect(2,3,36,6,0x281);rect(2,30,36,5,0x280)
rect(10,12,19,17,0x282,True,elevation=1)
rect(2,24,8,5,0x281);rect(2,12,8,5,0x281);rect(29,12,9,17,0x281)
# Main entrance gangway, upper captain gangway and final shortcut start closed.
rect(4,29,3,1,0x282,True,1);rect(4,9,3,3,0x304,True)
rect(33,9,3,3,0x304,True);rect(33,29,3,1,0x304,True)
# Native mooring posts, machinery controls, shrubs and patterned gangways.
for x,y,t in [(5,31,0x300),(33,20,0x301),(5,14,0x302),(35,31,0x303)]:rect(x,y,1,1,t,True)
for x,y in [(2,3),(37,3),(2,8),(37,8),(2,24),(2,28),(37,12),(37,28)]:rect(x,y,1,1,0x304,True)
for x in [19,20,21]:rect(x,34,1,1,0x305)
p=R/'data/layouts/HavoraCaptainsTrial';p.mkdir(exist_ok=True);(p/'map.bin').write_bytes(struct.pack('<'+'H'*len(b),*b));(p/'border.bin').write_bytes(struct.pack('<4H',*[blocked(0x33)]*4))
p=R/'data/layouts/layouts.json';ls=json.loads(p.read_text());ls['layouts']=[l for l in ls['layouts'] if l['id']!='LAYOUT_HAVORA_CAPTAINS_TRIAL'];ls['layouts'].append({'id':'LAYOUT_HAVORA_CAPTAINS_TRIAL','name':'HavoraCaptainsTrial_Layout','width':W,'height':H,'border_width':2,'border_height':2,'primary_tileset':'gTileset_HavoraGymPrimary','secondary_tileset':'gTileset_HavoraGym','border_filepath':'data/layouts/HavoraCaptainsTrial/border.bin','blockdata_filepath':'data/layouts/HavoraCaptainsTrial/map.bin'});p.write_text(json.dumps(ls,indent=2)+'\n')
p=R/'data/maps/QuantumHavoraGym/map.json';m=json.loads(p.read_text());m['layout']='LAYOUT_HAVORA_CAPTAINS_TRIAL';m['allow_running']=True
m['object_events']=[]
for gfx,x,y,script in [('GYM_GUY',17,32,'Welcome'),('SAILOR',32,24,'Crew'),('SAILOR',7,13,'Navigator'),('SAILOR',20,5,'Captain')]:
 m['object_events'].append({'type':'object','graphics_id':'OBJ_EVENT_GFX_'+gfx,'x':x,'y':y,'elevation':3,'movement_type':'MOVEMENT_TYPE_FACE_DOWN','movement_range_x':0,'movement_range_y':0,'trainer_type':'TRAINER_TYPE_NONE','trainer_sight_or_berry_tree_id':'0','script':'HavoraTrial_'+script,'flag':'0'})
for i,w in enumerate(m['warp_events']):w.update(x=19+i,y=34)
m['bg_events']=[]
for x,y,script in [(5,31,'Gangway'),(33,20,'Tide'),(5,14,'UpperGangway'),(35,31,'Reset'),(10,26,'Board'),(28,26,'Board'),(10,14,'Board'),(28,14,'Board')]:
 m['bg_events'].append({'type':'sign','x':x,'y':y,'elevation':3,'player_facing_dir':'BG_EVENT_PLAYER_FACING_ANY','script':'HavoraTrial_'+script})
p.write_text(json.dumps(m,indent=2)+'\n')
# Add canonical SS Anne wall panels/porthole without touching the shared art.
# Only private gym tile slots 64+ and otherwise-unused palette banks are used.
from PIL import Image
source=[R/'data/tilesets/primary/general',R/'data/tilesets/secondary/ss_anne']
gfx=[Image.open(p/'tiles.png') for p in source]
b=(source[1]/'metatiles.bin').read_bytes();sm=struct.unpack('<'+'H'*(len(b)//2),b)
pg=R/'data/tilesets/primary/havora_gym';sg=R/'data/tilesets/secondary/havora_gym'
im=Image.open(R/'data/tilesets/primary/havora_city/tiles.png');palmap={};freep=iter([0,2,3,6,7,9,10,11]);tilemap={};tid=64
for dst,src in [(0x306,0x2bd),(0x307,0x283),(0x308,0x288),(0x309,0x284),(0x30a,0x285),(0x30b,0x282),(0x310,0x302),(0x311,0x303),(0x312,0x313),(0x313,0x2f4),(0x314,0x2d4),(0x315,0x2ea),(0x316,0x2eb)]:
 out=[]
 for w in sm[(src-640)*8:(src-640+1)*8]:
  sp=w>>12
  if sp not in palmap:palmap[sp]=next(freep)
  n=w&1023;group=int(n>=640);i=n-640 if group else n;raw=gfx[group].crop((i%16*8,i//16*8,i%16*8+8,i//16*8+8));key=(group,i)
  if key not in tilemap:
   tilemap[key]=tid;im.paste(raw,(tid%16*8,tid//16*8));tid+=1
  out.append(tilemap[key]|(w&0xc00)|(palmap[sp]<<12))
 M[dst*8:(dst+1)*8]=out;A[dst]=0
im.save(pg/'tiles.png',bits=4)
for group in ['primary','secondary']:
 dest=R/f'data/tilesets/{group}/havora_gym/palettes';dest.mkdir(exist_ok=True)
 for i in range(16):
  original=R/f'data/tilesets/{group}/havora_city/palettes/{i:02}.pal'
  if original.exists():shutil.copyfile(original,dest/f'{i:02}.pal')
for sourcepal,destpal in palmap.items():
 src=source[0 if sourcepal<7 else 1]/'palettes'/f'{sourcepal:02}.pal'
 for group in ['primary','secondary']:(R/f'data/tilesets/{group}/havora_gym/palettes/{destpal:02}.pal').write_bytes(src.read_bytes())
# Rewrite private metatiles after the canonical interior imports.
for group,start,end in [('primary',0,640),('secondary',640,1024)]:
 p=R/f'data/tilesets/{group}/havora_gym';(p/'metatiles.bin').write_bytes(struct.pack('<'+'H'*((end-start)*8),*M[start*8:end*8]));(p/'metatile_attributes.bin').write_bytes(struct.pack('<'+'I'*(end-start),*A[start:end]))
# Give the outline a dark void, ship wall panels, and matching corner trim.
p=R/'data/layouts/HavoraCaptainsTrial/map.bin';raw=p.read_bytes();blocks=list(struct.unpack('<'+'H'*(len(raw)//2),raw))
for i,v in enumerate(blocks):
 if v&1023==0x33:blocks[i]=(v&~1023)|0x308
for yy in [2,11,23,29]:
 for xx in (range(2,10) if yy in [11,23] else range(2,38)):
  i=yy*40+xx
  if blocks[i]&0x400:blocks[i]=0x3400|0x306
for xx in range(2,38):blocks[2*40+xx]=0x3400|(0x307 if xx==2 else 0x30a if xx==37 else 0x309)
for xx in [4,10,16,23,29,35]:blocks[3*40+xx]=0x3400|0x30b
for yy in range(3):
 for xx in range(3):blocks[(25+yy)*40+10+xx]=0x3400|0x2bc+yy*3+xx
for xx in range(10,26):blocks[19*40+xx]=0x3400|0x304
# Existing ship furnishings give the crew stations a lived-in working identity.
for xx,yy,t in [(4,5,0x310),(5,5,0x310),(10,5,0x313),(11,5,0x311),(29,5,0x313),(30,5,0x311),(34,5,0x310),(35,5,0x310),(3,7,0x312),(36,7,0x312),(3,14,0x313),(3,25,0x314),(36,14,0x314),(35,17,0x315),(36,17,0x316),(35,22,0x315),(36,22,0x316),(35,26,0x314),(3,32,0x312),(37,32,0x312)]:blocks[yy*40+xx]=0x3400|t
p.write_bytes(struct.pack('<'+'H'*len(blocks),*blocks));(p.with_name('border.bin')).write_bytes(struct.pack('<4H',*[0x3400|0x308]*4))
(R/'tools/havora/captains-trial.json').write_text(json.dumps({'width':40,'height':36,'imported_graphics':len(tilemap),'palette_mapping':palmap,'state_var':'0x40D7','progress_var':'0x40D8','sources':['Havora/Pacifidlog docks and boat','FireRed SS Anne wall panels and porthole'],'new_pixel_art':False},indent=2)+'\n')

keep={0x280,0x281,0x282,*range(0x2bc,0x2c5),*range(0x300,0x30c),*range(0x310,0x317)}
for mid in range(1024):
 if mid not in keep:M[mid*8:(mid+1)*8]=[0]*8;A[mid]=0
for group,start,end in [('primary',0,640),('secondary',640,1024)]:
 p=R/f'data/tilesets/{group}/havora_gym';(p/'metatiles.bin').write_bytes(struct.pack('<'+'H'*((end-start)*8),*M[start*8:end*8]));(p/'metatile_attributes.bin').write_bytes(struct.pack('<'+'I'*(end-start),*A[start:end]))
