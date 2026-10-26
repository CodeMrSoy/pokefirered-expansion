"""Overhead yard geometry. Importing is read-only; build() writes the gym."""
from pathlib import Path
import struct,json
R=Path(__file__).resolve().parents[2]
W,H=80,40
BANK=[1,22,28,49,74,55];SHORE=[5,22,32,49,74,59]
DIR=[1,-1,1,-1,-1,1];STAIR=[2,26,28,53,78,55]
POOLS=[(6,16),(33,16),(60,14)];CORE=[13,35,72]
BERTH_ROW=19;CHANNEL_ROW=34;ENTRY=(3,35)
DOCK=[{0,1,2},{1},{0,1,2},{2},{0,1,2},{1,2}]
ANCHORS=[(3,14),(24,14),(30,14),(51,15),(76,13),(57,14),(41,22),(65,23)]
ACTOR_DEFS=[('GYM_GUY',3,33,9,'Welcome'),('SAILOR',31,20,9,'Crew'),('SAILOR',76,20,9,'Navigator'),('SAILOR',51,17,9,'Engineer'),('SAILOR',40,21,9,'Diver'),('SAILOR',57,17,9,'FirstMate'),('SAILOR',67,24,9,'Captain')]
ACTORS={(x,y) for _,x,y,_,_ in ACTOR_DEFS}
base=[0x97b0]*(W*H)
def cell(b,x,y,t,block=False,z=9):b[y*W+x]=(z<<12)|(0x400 if block else 0)|t
def rect(b,x,y,w,h,t,block=False,z=9):
 for yy in range(y,y+h):
  for xx in range(x,x+w):cell(b,xx,yy,t,block,z)
def line(b,points,t,z=9):
 for (x,y),(xx,yy) in zip(points,points[1:]):
  assert x==xx or y==yy
  for a in range(min(x,xx),max(x,xx)+1):
   for v in range(min(y,yy),max(y,yy)+1):cell(b,a,v,t,False,z)
rect(base,0,8,W,2,0x349,True);rect(base,0,9,W,1,0x348,True)
rect(base,0,10,W,26,0x380,True)
for x in [0,20,40,60,79]:cell(base,x,9,0x347,True)
for x,width in POOLS:
 rect(base,x,17,width,19,0x282,True,1);rect(base,x,16,width,1,0x3b1,True)
# Fixed high decks, short south-facing retaining walls, lower floodable aprons.
for n,x in enumerate(BANK):
 rect(base,x,13 if n==5 else 11,5,11 if n==5 else 13,0x281);rect(base,x,25,5,4,0x281,False,5)
 for dx in range(5):
  cell(base,x+dx,24,0x3c0+dx,True);cell(base,x+dx,29,0x3c0+dx,True,5)
 cell(base,STAIR[n],24,0x386,False,0)
# A dry entrance corridor is structurally independent of the submerged shelves.
rect(base,1,24,2,13,0x281);cell(base,2,25,0x386,False,0)
rect(base,1,35,5,2,0x281)
for x in [2,3,4]:cell(base,x,37,0x305)
paths={'permanent':[(30,13),(30,12),(51,12),(51,13)],'shoreA':[(5,28),(22,28)],'shoreC':[(59,28),(74,28)],'midAB':[(26,17),(28,17)],'midBC':[(30,13),(30,10),(76,10),(76,13)],'service':[(49,22),(44,22)],'final':[(53,22),(64,22)]}
for key in ['permanent','midAB','midBC']:line(base,paths[key],0x318)
# Galleries remain visible; physical gates control access.
cell(base,27,17,0x385,True);cell(base,54,10,0x385,True)
for x in [22,49]:rect(base,x,33,11,3,0x282,True,1)
# Service island: the same low winch shelf is exposed and submerged in place.
rect(base,39,20,6,6,0x380,True);rect(base,40,21,4,2,0x281)
rect(base,40,24,3,2,0x281,False,5)
cell(base,40,23,0x386,False,0);cell(base,40,24,0x386,False,0)
for x in [39,44]:cell(base,x,25,0x3c0 if x==39 else 0x3c4,True)
# Three water cells, rather than an invented eleven-cell vessel, separate this
# captain's quay from the cargo berth. The staging gangway is a separate hinge.
rect(base,63,21,7,5,0x380,True);rect(base,64,22,5,3,0x281)
for x in range(63,70):cell(base,x,25,0x3c0 if x==63 else 0x3c4 if x==69 else 0x3c2,True)
consoles=[]
def console(n,x,y,script,mid):
 cell(base,x,y,mid,True);consoles.append((n,x,y,script))
for n in [0,1,2,5]:
 x=BANK[n]+2;pair='AB' if n<2 else 'BC'
 console(n,x,13,pair+'Forward',0x300 if pair=='AB' else 0x301)
 console(n,x,15,pair+'Reverse',0x302 if pair=='AB' else 0x301)
for x,y,s,t in [(75,13,'ABForward',0x300),(77,13,'ABReverse',0x302),(75,15,'BCForward',0x301),(77,15,'BCReverse',0x301)]:console(4,x,y,s,t)
console(3,51,14,'ServiceMoor',0x302);console(4,76,14,'FinalMoor',0x302)
console(6,41,21,'BCForward',0x301);console(6,42,21,'BCReverse',0x301)
consoles.append((6,41,25,'Chain'))
for n,x in enumerate(BANK):
 console(n,x+(4 if n in [0,1,2,5] else 1),14,'Status',0x377)
 if n!=4:console(n,x+3,13 if n in [0,1,2,5] else 14,'Reset',0x303)
console(6,43,21,'Reset',0x303)
def berth(node,boat):return SHORE[node],BERTH_ROW+boat*3
def draw(state,include_boats=True):
 levels,p,a,c,moor,released=state;b=base.copy()
 for n,x in enumerate(BANK):
  w=levels[n//2];cut=30 if w==0 else 27 if w==1 else 25
  if cut<30:rect(b,x,cut,5,30-cut,0x282,True,1)
  if w==2:cell(b,STAIR[n],24,0x3c0+STAIR[n]-x,True)
  cell(b,x+(4 if n in [0,1,2,5] else 1),14,[0x376,0x387,0x377][w],True)
  for boat in range(2):
   y=BERTH_ROW+boat*3;valid=w in DOCK[n]
   cell(b,SHORE[n],y,(0x370 if DIR[n]>0 else 0x372) if valid else 0x385,not valid)
 rect(b,1,24,2,13,0x281);cell(b,2,25,0x386,False,0)
 if levels[0]==0:line(b,paths['shoreA'],0x280,5)
 if levels[2]==0:line(b,paths['shoreC'],0x280,5)
 cell(b,27,17,0x318 if levels[0]==levels[1]==1 else 0x385,not(levels[0]==levels[1]==1))
 cell(b,54,10,0x318 if levels[1]==levels[2]==1 else 0x385,not(levels[1]==levels[2]==1))
 for x,ch in [(22,0),(49,1)]:
  if levels[ch]!=levels[ch+1]:rect(b,x+5,33,1,3,0x385,True,1)
 if levels[1]==2:rect(b,40,24,3,2,0x282,True,1)
 else:cell(b,41,25,0x302,True,5)
 if include_boats:
  for boat,node in [(0,a),(1,c)]:
   cx=SHORE[node]+2*DIR[node];cy=BERTH_ROW+boat*3
   for yy in range(3):
    for xx in range(3):cell(b,cx+xx-1,cy+yy-1,(0x2bc if boat==0 else 0x390)+yy*3+xx,True,1)
 if moor==1 and c==3 and levels[1]==2:line(b,paths['service'],0x318)
 if moor==2 and c==5 and levels[1]==levels[2]==2:line(b,paths['final'],0x318)
 for n in range(6):
  for y in range(17,24):
   at=y*W+SHORE[n]
   if b[at]&1023==0x281:b[at]=(b[at]&~1023)|(0x3b2 if DIR[n]>0 else 0x3b3)
 return b
def build():
 layout=R/'data/layouts/HavoraCaptainsTrial'
 for name,tiles in [('base',base),('map',draw(((2,2,0),0,0,4,0,False)))]:
  (layout/(name+'.bin')).write_bytes(struct.pack('<'+'H'*len(tiles),*tiles))
 (layout/'border.bin').write_bytes(struct.pack('<4H',*[0x97b0]*4))
 ls=R/'data/layouts/layouts.json';j=json.loads(ls.read_text());l=next(l for l in j['layouts'] if l['id']=='LAYOUT_HAVORA_CAPTAINS_TRIAL');l.update(width=W,height=H);ls.write_text(json.dumps(j,indent=2)+'\n')
 mp=R/'data/maps/QuantumHavoraGym/map.json';j=json.loads(mp.read_text())
 for i,warp in enumerate(j['warp_events']):warp.update(x=2+i,y=37,elevation=9)
 j['object_events']=[dict(type='object',graphics_id='OBJ_EVENT_GFX_'+g,x=x,y=y,elevation=z,movement_type='MOVEMENT_TYPE_FACE_DOWN',movement_range_x=0,movement_range_y=0,trainer_type='TRAINER_TYPE_NONE',trainer_sight_or_berry_tree_id='0',script='HavoraTrial_'+s,flag='0') for g,x,y,z,s in ACTOR_DEFS]
 bgs=[dict(type='sign',x=x,y=y,elevation=5 if s=='Chain' else 9,player_facing_dir='BG_EVENT_PLAYER_FACING_ANY',script='HavoraLock_'+s) for n,x,y,s in consoles]
 for n in range(6):
  for boat in range(2):bgs.append(dict(type='sign',x=SHORE[n]+DIR[n],y=BERTH_ROW+boat*3,elevation=9,player_facing_dir='BG_EVENT_PLAYER_FACING_ANY',script='HavoraLock_Board'+str(boat)))
 j['bg_events']=bgs;mp.write_text(json.dumps(j,indent=2)+'\n')
 header='// Generated by overhead_lock_geometry.py.\n#define LOCK_WIDTH 80\n#define LOCK_HEIGHT 40\n#define LOCK_BERTH_ROW 19\n#define LOCK_CHANNEL_ROW 34\n#define LOCK_ENTRY_X 3\n#define LOCK_ENTRY_Y 35\n'
 for typ,name,values in [('u8','sBank',BANK),('u8','sStair',STAIR),('u8','sShore',SHORE),('s8','sBankDirection',DIR),('u8','sCoreX',CORE)]:header+=f'static const {typ} {name}[] = {{'+','.join(map(str,values))+'};\n'
 header+='static const u8 sDockMask[] = {7,2,7,4,7,6};\n'
 controls={'ABForward':(10,0,1),'ABReverse':(10,1,0),'BCForward':(10,1,2),'BCReverse':(10,2,1),'ServiceMoor':(12,0,0),'Chain':(13,0,0),'FinalMoor':(14,0,0),'Reset':(15,0,0)}
 header+='static const u8 sLockControls[][5] = {\n'
 for n,x,y,s in consoles:
  if s in controls:header+=' {'+','.join(map(str,(x,y,*controls[s])))+'},\n'
 header+='};\n';(R/'src/data/havora_lock_geometry.h').write_text(header)
 # RLE map overlays make Python validation and native rendering share one
 # geometry source. Six legal water configurations need only a few KB of runs.
 runs=[];offsets=[]
 for value in range(27):
  levels=(value%3,value//3%3,value//9)
  if sum(levels)!=4:offsets.append(0);continue
  offsets.append(len(runs))
  tiles=draw((levels,0,0,4,0,False),include_boats=False)
  for tile in tiles:
   if runs and len(runs)>offsets[-1] and runs[-1][1]==tile:runs[-1][0]+=1
   else:runs.append([1,tile])
 header+='struct LockMapRun {u16 count;u16 tile;};\nstatic const u16 sLockMapOffsets[] = {'+','.join(map(str,offsets))+'};\n'
 header+='static const struct LockMapRun sLockMapRuns[] = {\n'+''.join(' {%d,0x%04x},\n'%tuple(v) for v in runs)+'};\n'
 (R/'src/data/havora_lock_geometry.h').write_text(header)
 (R/'tools/havora/fixed-lock-geometry.json').write_text(json.dumps(dict(width=W,height=H,banks=BANK,shore=SHORE,direction=DIR,berth_row=BERTH_ROW,channel_row=CHANNEL_ROW,paths=paths,consoles=consoles),indent=2)+'\n')
 print('Built overhead lock yard',W,H,'with fixed berths and',len(bgs),'controls')
if __name__=='__main__':build()
