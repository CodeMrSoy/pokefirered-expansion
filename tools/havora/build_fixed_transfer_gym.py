"""Build the mapped three-lock prototype; only the dedicated gym is changed."""
from pathlib import Path
import struct,json
R=Path(__file__).resolve().parents[2]
W,H=80,54
BANK=[1,22,28,49,74,55];SHORE=[5,22,32,49,74,59];DIR=[1,-1,1,-1,-1,1];STAIR=[1,26,28,53,78,55]
POOLS=[(6,16),(33,16),(60,14)];CORE=[13,35,72];ROWS=[35,27,19]
base=[0x9400|0x3b0]*(W*H)
def cell(b,x,y,t,block=False,z=9):b[y*W+x]=(z<<12)|(0x400 if block else 0)|t
def rect(b,x,y,w,h,t,block=False,z=9):
 for yy in range(y,y+h):
  for xx in range(x,x+w):cell(b,xx,yy,t,block,z)
def line(b,points,t,z=9):
 for (x,y),(xx,yy) in zip(points,points[1:]):
  assert x==xx or y==yy
  for a in range(min(x,xx),max(x,xx)+1):
   for v in range(min(y,yy),max(y,yy)+1):cell(b,a,v,t,False,z)
# A compact perimeter surrounds the working space; the unused exterior is dark.
rect(base,1,10,78,34,0x380,True,9)
rect(base,0,8,W,2,0x349,True,9)
rect(base,0,9,W,1,0x348,True,9)
rect(base,0,44,W,2,0x380,True,9)
rect(base,0,44,W,1,0x3b1,True,9)
for x in [0,79]:rect(base,x,10,1,34,0x380,True,9)
for x in [0,20,40,60,79]:cell(base,x,9,0x347,True,9)
for i,x in enumerate(BANK):
 rect(base,x,13,5,28,0x280,False,3)
 for y,h,z in [(11 if i!=5 else 13,5 if i!=5 else 3,9),(17,7,7),(25,7,5),(33,8,3)]:rect(base,x,y,5,h,0x281,False,z)
 for y in [16,24,32]:
  for dx in range(5):cell(base,x+dx,y,0x3c0+dx,True,7 if y==16 else 5 if y==24 else 3)
 rect(base,STAIR[i],15,1,35 if i==0 else 24,0x281,False,0)
 for yy in [16,24,32]:cell(base,STAIR[i],yy,0x386,False,0)
for x,width in POOLS:
 rect(base,x,17,width,27,0x282,True,1)
 rect(base,x,16,width,1,0x3b1,True,1)
# Channels are navigable only when neighboring levels match.
rect(base,22,42,11,1,0x385,True,1);rect(base,49,42,11,1,0x385,True,1)
line(base,[(30,13),(30,12),(51,12),(51,13)],0x318,9)
# A west entrance retains all three exterior warp indices.
rect(base,1,41,5,9,0x280,False,3)
for x in [2,3,4]:cell(base,x,50,0x305,False,3)
# Service island: upper pump deck and a genuinely lower, floodable winch ledge.
rect(base,39,21,6,5,0x380,True,9)
rect(base,40,21,4,2,0x281,False,9)
rect(base,40,24,3,2,0x281,False,5)
rect(base,40,22,1,4,0x386,False,0);cell(base,43,22,0x386,False,0)
# Captain island has no boat landing: its seawall opens only onto the cargo bridge.
rect(base,64,21,7,5,0x380,True,9);rect(base,65,22,5,3,0x281,False,9)
# Rounded fronts finish the two isolated platforms without changing access.
for xx in range(64,71):cell(base,xx,25,0x3c0 if xx==64 else 0x3c4 if xx==70 else 0x3c2,True,9)
cell(base,39,25,0x3c0,True,9);cell(base,44,25,0x3c4,True,9)
# Stations: explicit physical consoles, not hidden floor/menu interactions.
consoles=[]
def console(node,x,y,script,mid):
 cell(base,x,y,mid,True,9);consoles.append((node,x,y,script))
for n in [0,1,2,5]:
 x=BANK[n]+2;pair='AB' if n<2 else 'BC'
 console(n,x,13,pair+'Forward',0x300 if pair=='AB' else 0x301)
 console(n,x,15,pair+'Reverse',0x302 if pair=='AB' else 0x301)
for x,y,s,t in [(75,13,'ABForward',0x300),(77,13,'ABReverse',0x302),(75,15,'BCForward',0x301),(77,15,'BCReverse',0x301)]:console(4,x,y,s,t)
console(3,51,14,'ServiceMoor',0x302)
console(4,76,14,'FinalMoor',0x302)
console(6,41,21,'BCForward',0x301);console(6,42,21,'BCReverse',0x301)
# The winch below HIGH is drawn dynamically, so its flooded form is water.
consoles.append((6,41,25,'Chain'))
for n,x in enumerate(BANK):
 # Status is a gauge beside the stairs, reset is a distinct green lever.
 console(n,x+(4 if n in [0,1,2,5] else 1),14,'Status',0x377)
 if n!=4:console(n,x+3,13 if n in [0,1,2,5] else 14,'Reset',0x303)
console(6,43,21,'Reset',0x303)
# Persist neutral base separately so redraws never retain previous boats/bridges.
layout=R/'data/layouts/HavoraCaptainsTrial';(layout/'base.bin').write_bytes(struct.pack('<'+'H'*len(base),*base))
paths={
 'permanent':[(30,13),(30,12),(51,12),(51,13)],
 'shoreA':[(5,32),(22,32)],'shoreC':[(59,32),(74,32)],
 'midAB':[(26,28),(28,28)],
 'midBC':[(30,13),(30,10),(76,10),(76,13)],
 'service':[(49,22),(43,22)],
 'final':[(53,22),(64,22)],
}
# Python reference drawing is also used for physical-connectivity verification.
def draw(state,include_boats=True):
 levels,p,a,c,moor,released=state;b=base.copy()
 for ch,(x,width) in enumerate(POOLS):
  surface=19-levels[ch]
  rect(b,x,17,width,27,0x282,True,levels[ch]*2+3)
  rect(b,x,17,width,surface-17,0x380,True,1)
  rect(b,x,surface,width,1,0x381,True,1)
 # Reapply isolated platforms after water covers its retaining walls.
 for yy in range(21,26):
  for xx in range(39,45):b[yy*W+xx]=base[yy*W+xx]
 for yy in range(21,26):
  for xx in range(64,71):b[yy*W+xx]=base[yy*W+xx]
 if levels[1]==2:rect(b,40,24,3,2,0x282,True,1)
 else:cell(b,41,25,0x302,True,5)
 for ch,(x,width) in enumerate(POOLS):
  # Canal extensions are already water, and get the actual water elevation.
  rect(b,x,41,width,3,0x282,True,levels[ch]*2+3)
 for x,ch in [(22,0),(49,1)]:
  rect(b,x,42,11,1,0x282 if levels[ch]==levels[ch+1] else 0x385,True,levels[ch]*2+3)
 for i,xx in enumerate(BANK):
  w=levels[i//2];cut=24 if w==2 else 32 if w==1 else 41
  if cut<41:rect(b,xx,cut,5,41-cut,0x282,True,1)
  rect(b,STAIR[i],15,1,35 if i==0 else 24,0x281,False,0)
  for yy in [16,24,32]:cell(b,STAIR[i],yy,0x386,False,0)
  cell(b,xx+(4 if i in [0,1,2,5] else 1),14,[0x376,0x387,0x377][w],True,9)
 line(b,paths['permanent'],0x318,9)
 if levels[0]==0:line(b,paths['shoreA'],0x280,3)
 if levels[2]==0:line(b,paths['shoreC'],0x280,3)
 if levels[0]==levels[1]==1:line(b,paths['midAB'],0x318,5)
 if levels[1]==levels[2]==1:line(b,paths['midBC'],0x318,9)
 if moor==1 and c==3 and levels[1]==2:line(b,paths['service'],0x318,7);cell(b,43,22,0x386,False,0)
 if moor==2 and c==5 and levels[1]==levels[2]==2:
  line(b,paths['final'],0x318,7);cell(b,64,22,0x386,False,0)
 # Disallowed landing heights have closed iron barriers on shore.
 docksets=[{0,1,2},{1},{0,1,2},{2},{0,1,2},{1,2}]
 for n in range(6):
  for lev in range(3):
   for boat in range(2):
    y=ROWS[lev]+boat*3
    cell(b,SHORE[n],y,0x282,True,1) if levels[n//2]>lev else cell(b,SHORE[n],y,(0x370 if DIR[n]>0 else 0x372) if lev in docksets[n] else 0x385,lev not in docksets[n],lev*2+3)
 if include_boats:
  for boat,n in [(0,a),(1,c)]:
   cx=SHORE[n]+2*DIR[n];cy=ROWS[levels[n//2]]+boat*3
   for yy in range(3):
    for xx in range(3):cell(b,cx+xx-1,cy+yy-1,(0x2bc if boat==0 else 0x390)+yy*3+xx,True,levels[n//2]*2+3)
 if moor==1 and c==3 and levels[1]==2:line(b,paths['service'],0x318,7);cell(b,43,22,0x386,False,0)
 if moor==2 and c==5 and levels[1]==levels[2]==2:line(b,paths['final'],0x318,7);cell(b,64,22,0x386,False,0)
 for n in range(6):
  for yy in range(17,41):
   at=yy*W+SHORE[n]
   if b[at]&1023==0x281:b[at]=(b[at]&~1023)|(0x3b2 if DIR[n]>0 else 0x3b3)
 return b
start=((2,2,0),0,0,4,0,False)
initial=draw(start);(layout/'map.bin').write_bytes(struct.pack('<'+'H'*len(initial),*initial))
(layout/'border.bin').write_bytes(struct.pack('<4H',*[0x9400|0x3b0]*4))
ls=R/'data/layouts/layouts.json';j=json.loads(ls.read_text());l=next(l for l in j['layouts'] if l['id']=='LAYOUT_HAVORA_CAPTAINS_TRIAL');l.update(width=W,height=H);ls.write_text(json.dumps(j,indent=2)+'\n')
mp=R/'data/maps/QuantumHavoraGym/map.json';j=json.loads(mp.read_text())
for i,warp in enumerate(j['warp_events']):warp.update(x=2+i,y=50,elevation=3)
actors=[('GYM_GUY',3,47,3,'Welcome'),('SAILOR',31,20,7,'Crew'),('SAILOR',76,20,7,'Navigator'),('SAILOR',67,24,9,'Captain')]
j['object_events']=[dict(type='object',graphics_id='OBJ_EVENT_GFX_'+g,x=x,y=y,elevation=z,movement_type='MOVEMENT_TYPE_FACE_DOWN',movement_range_x=0,movement_range_y=0,trainer_type='TRAINER_TYPE_NONE',trainer_sight_or_berry_tree_id='0',script='HavoraTrial_'+s,flag='0') for g,x,y,z,s in actors]
bgs=[]
for n,x,y,s in consoles:bgs.append(dict(type='sign',x=x,y=y,elevation=5 if s=='Chain' else 9,player_facing_dir='BG_EVENT_PLAYER_FACING_ANY',script='HavoraLock_'+s))
for n in range(6):
 for lev in range(3):
  for boat in range(2):
   bgs.append(dict(type='sign',x=SHORE[n]+DIR[n],y=ROWS[lev]+boat*3,elevation=lev*2+3,player_facing_dir='BG_EVENT_PLAYER_FACING_ANY',script='HavoraLock_Board'+str(boat)))
j['bg_events']=bgs;mp.write_text(json.dumps(j,indent=2)+'\n')
# Shared numeric geometry for the runtime and tests.
header='// Generated by build_fixed_transfer_gym.py.\n#define LOCK_WIDTH 80\n#define LOCK_HEIGHT 54\n'
for typ,name,values in [('u8','sBank',BANK),('u8','sStair',STAIR),('u8','sShore',SHORE),('s8','sBankDirection',DIR),('u8','sPoolX',[6,33,60]),('u8','sPoolWidth',[16,16,14]),('u8','sCoreX',CORE),('u8','sWaterRow',ROWS)]:header+=f'static const {typ} {name}[] = {{'+','.join(map(str,values))+'};\n'
header+='static const u8 sDockMask[] = {7,2,7,4,7,6};\n'
controls={'ABForward':(10,0,1),'ABReverse':(10,1,0),'BCForward':(10,1,2),'BCReverse':(10,2,1),'ServiceMoor':(12,0,0),'Chain':(13,0,0),'FinalMoor':(14,0,0),'Reset':(15,0,0)}
header+='static const u8 sLockControls[][5] = {\n'
for n,x,y,script in consoles:
 if script in controls:header+=' {'+','.join(map(str,(x,y,*controls[script])))+'},\n'
header+='};\n'

(R/'src/data/havora_lock_geometry.h').write_text(header)
(R/'tools/havora/fixed-lock-geometry.json').write_text(json.dumps(dict(width=W,height=H,banks=BANK,shore=SHORE,direction=DIR,rows=ROWS,paths=paths,consoles=consoles),indent=2)+'\n')
print('Built three-lock gym',W,H,'with',len(bgs),'physical interactions')
