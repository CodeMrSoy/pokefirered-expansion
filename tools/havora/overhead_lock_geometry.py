"""Runtime water overlays for the 80x29 Porymap-authored Havora gym.

The authored plan is never regenerated. Reference maps provide the three local
water silhouettes; only masonry/water cells are imported, not screenshot props.
Run build() explicitly after changing authored.bin or the geometry below.
"""
from pathlib import Path
import struct,json
R=Path(__file__).resolve().parents[2]
W,H=80,29
BANK=[1,23,28,50,75,55];SHORE=[4,23,31,50,75,58]
DIR=[1,-1,1,-1,-1,1];STAIR=[2,25,29,52,78,55]
POOLS=[(5,18),(32,18),(59,16)];CORE=[14,40,66]
BERTH_ROW=10;CHANNEL_ROW=24;HULL_OFFSET=4;ENTRY=(3,27)
DOCK=[{0,1,2},{1},{0,1,2},{2},{0,1,2},{1,2}]
ANCHORS=[(2,8),(25,8),(29,8),(52,8),(77,8),(56,8),(40,12),(65,22)]
mp=R/'data/maps/QuantumHavoraGym/map.json'
objects=json.loads(mp.read_text())['object_events']
ACTOR_DEFS=[(o['graphics_id'].removeprefix('OBJ_EVENT_GFX_'),o['x'],o['y'],o['elevation'],o['script'].removeprefix('HavoraTrial_')) for o in objects]
ACTORS={(x,y) for _,x,y,_,_ in ACTOR_DEFS}
layout=R/'data/layouts/HavoraCaptainsTrial'
def words(p):
 b=p.read_bytes();return list(struct.unpack('<'+'H'*(len(b)//2),b))
authored=words(layout/'authored.bin')
refs=[words(layout/'reference_states'/f) for f in ['high-low-low.bin','mid-high-mid.bin','low-mid-high.bin']]
# Each picture supplies one water profile for each pool.
PROFILE=[[2,1,0],[0,2,1],[0,1,2]]
STRUCTURE={0x282,0x380,0x3b1,0x3c0,0x3c1,0x3c2,0x3c3,0x3c4}
base=authored.copy()
for i,v in enumerate(base):
 if 0x2bc<=v&1023<=0x2c4 or 0x390<=v&1023<=0x398:base[i]=0x1682
# Correct the cargo's accidentally varying elevation and use the original
# platform elevation for every person on the authored decks.
def cell(b,x,y,t,block=False,z=5):b[y*W+x]=(z<<12)|(0x400 if block else 0)|t
def rect(b,x,y,w,h,t,block=False,z=5):
 for yy in range(y,y+h):
  for xx in range(x,x+w):cell(b,xx,yy,t,block,z)
def line(b,points,t,z=5):
 for (x,y),(xx,yy) in zip(points,points[1:]):
  assert x==xx or y==yy
  for a in range(min(x,xx),max(x,xx)+1):
   for v in range(min(y,yy),max(y,yy)+1):cell(b,a,v,t,False,z)
paths={'permanent':[(29,6),(29,4),(52,4),(52,6)],'shoreA':[(2,17),(25,17)],'shoreC':[(56,17),(77,17)],'midAB':[(26,8),(28,8)],'midBC':[(52,4),(77,4),(77,6)],'service':[(50,13),(42,13)],'final':[(52,17),(67,17),(67,21)]}
consoles=[]
for e in json.loads(mp.read_text())['bg_events']:
 s=e['script'].removeprefix('HavoraLock_');x,y=e['x'],e['y']
 if s.startswith('Board'):continue
 if x<=4:n=0
 elif x<=26:n=1
 elif x<=31:n=2
 elif x>=75:n=4
 elif x>=55:n=5
 elif x>=49:n=3
 else:n=6
 consoles.append((n,x,y,s))
# A compact leader quay, below section 3, matching the supplied reference.
rect(base,63,21,6,3,0x281,False,3)
for x in range(63,69):cell(base,x,24,0x3b1,True,2)
for y in [19,20]:cell(base,67,y,0x386,False,0)
# Reroute the entry's existing ladder down to its authored exit.
rect(base,1,18,2,9,0x281,False,3)
rect(base,1,26,5,2,0x281,False,3)
for x in [2,3,4]:cell(base,x,28,0x305,False,3)
for y in [15,16,17]:cell(base,2,y,0x386,False,0)
def berth(node,boat):return SHORE[node],BERTH_ROW+boat*3
def draw(state,include_boats=True):
 levels,p,a,c,moor,released=state;b=base.copy()
 for x in range(6,79):cell(b,x,27,0x282,True,1)
 for ch,(left,right) in enumerate([(1,27),(28,54),(55,79)]):
  ref=refs[PROFILE[ch][levels[ch]]]
  for y in range(5,19):
   for x in range(left,right):
    i=y*W+x;old=base[i]&1023;new=ref[i]&1023
    if old in STRUCTURE and new in STRUCTURE:
     b[i]=0x1682 if new==0x282 else (base[i]&0xf000)|0x400|new
 # Permanent upper gallery joins the two B quays, with solid supports underneath.
 line(b,paths['permanent'],0x318)
 for x in [29,52]:cell(b,x,5,0x386,False,0)
 for key,x,ch in [('midAB',27,0),('midBC',54,1)]:
  line(b,paths[key],0x318)
  cell(b,x,8 if ch==0 else 4,0x318 if levels[ch]==levels[ch+1]==1 else 0x385,not(levels[ch]==levels[ch+1]==1))
  if ch==1:cell(b,77,5,0x386,False,0)
 if levels[0]==0:
  line(b,paths['shoreA'],0x318)
  for x in [2,25]:cell(b,x,16,0x386,False,0)
 else:
  for x in range(5,23):cell(b,x,17,0x282,True,1)
 cell(b,2,17,0x386,False,0)
 if levels[2]==0:
  line(b,paths['shoreC'],0x281,4)
  for x in [56,77]:cell(b,x,16,0x386,False,0)
 else:
  for x in range(59,75):cell(b,x,17,0x282,True,1)
 # Service deck remains above water. Its lower chain shelf floods in place.
 rect(b,39,12,3,2,0x281,False,4)
 for x in [39,40,41]:cell(b,x,14,0x282 if levels[1]==2 else 0x281,levels[1]==2,1 if levels[1]==2 else 3)
 if levels[1]!=2:cell(b,39,14,0x302,True,3);cell(b,40,13,0x386,False,0)
 # Gates at the lock mouths span the navigable opening, below the authored baffles.
 for x,ch in [(27,0),(54,1)]:
  for y in range(21,28):cell(b,x,y,0x282 if levels[ch]==levels[ch+1] else 0x385,True,1)
 # Gangplanks cover only the fixed side-face approach to each berth. The hull
 # sits beyond the widest LOW profile, so sailing never cuts through masonry.
 for n in range(6):
  for boat in range(2):
   y=BERTH_ROW+boat*3;valid=levels[n//2] in DOCK[n]
   cell(b,SHORE[n],y,(0x370 if DIR[n]>0 else 0x372) if valid else 0x385,not valid)
   for step in range(1,HULL_OFFSET-1):
    cell(b,SHORE[n]+step*DIR[n],y,0x318 if valid else 0x380,True,5)
 if moor==1 and c==3 and levels[1]==2:
  line(b,paths['service'],0x318)
  cell(b,42,13,0x386,False,0)
 # Final walkway exists visually from the start, with explicit locked access.
 for x in range(52,68):cell(b,x,17,0x281,False,4)
 for x in [52,56]:
  for y in [15,16]:cell(b,x,y,0x386,False,0)
 cell(b,67,18,0x386,False,0)
 final=moor==2 and c==5 and levels[1]==levels[2]==2
 cell(b,54,17,0x318 if final else 0x385,not final,4)
 cell(b,67,18,0x386 if final else 0x385,not final,0 if final else 4)
 # Keep C's low shore route isolated from B until the final bridge is tensioned.
 if levels[2]!=0 and not final:
  for x in range(59,75):cell(b,x,17,0x282,True,1)
  cell(b,54,17,0x385,True,4)
 # The lower C apron floods with its central span, leaving a hull-width
 # opening through the submerged wall rather than an invisible water barrier.
 if levels[2]!=0:
  for x in range(59,75):
   if x!=67 or not final:cell(b,x,18,0x282,True,1)
 # Level gauges keep the manually placed coordinates.
 for n,x,y,s in consoles:
  if s=='Status' and n<6:cell(b,x,y,[0x376,0x387,0x377][levels[n//2]],True)
 # Dress exposed masonry boundaries with the private cliff kit. This changes
 # only art: the authored collision and elevation bits remain intact.
 snapshot=b.copy();walls={0x380,0x3b1,0x3c0,0x3c1,0x3c2,0x3c3,0x3c4}
 for y in range(5,25):
  for x in range(1,79):
   i=y*W+x
   if snapshot[i]&1023 not in walls:continue
   wet=lambda xx,yy:snapshot[yy*W+xx]&1023==0x282
   left,right,below,above=wet(x-1,y),wet(x+1,y),wet(x,y+1),wet(x,y-1)
   mid=None
   if left:mid=0x3c9 if below else 0x3c7 if above else 0x3c5
   elif right:mid=0x3ca if below else 0x3c8 if above else 0x3c6
   elif below:mid=0x3cd
   if mid is not None:b[i]=(b[i]&~1023)|mid
 if include_boats:
  for boat,node in [(0,a),(1,c)]:
   cx=SHORE[node]+HULL_OFFSET*DIR[node];cy=BERTH_ROW+boat*3
   for yy in range(3):
    for xx in range(3):cell(b,cx+xx-1,cy+yy-1,(0x2bc if boat==0 else 0x390)+yy*3+xx,True,1)
 if moor==1 and c==3 and levels[1]==2:
  line(b,paths['service'],0x318)
  cell(b,42,13,0x386,False,0)
 return b

def build():
 for name,tiles in [('base',base),('map',draw(((2,2,0),0,0,4,0,False)))]:
  (layout/(name+'.bin')).write_bytes(struct.pack('<'+'H'*len(tiles),*tiles))
 j=json.loads(mp.read_text())
 for o in j['object_events']:
  o['elevation']=3 if o['script'].endswith(('Captain','Welcome')) else 5
  o['trainer_type']='TRAINER_TYPE_NONE'
  o['trainer_sight_or_berry_tree_id']='0'
 for e in j['bg_events']:
  if e['script'].startswith('HavoraLock_Board'):continue
  e['elevation']=3 if e['script'].endswith('Chain') else 4 if 37<=e['x']<=43 else 5
 j['bg_events']=[e for e in j['bg_events'] if not e['script'].startswith('HavoraLock_Board')]
 for n in range(6):
  for boat in range(2):j['bg_events'].append(dict(type='sign',x=SHORE[n]+DIR[n],y=BERTH_ROW+boat*3,elevation=5,player_facing_dir='BG_EVENT_PLAYER_FACING_ANY',script='HavoraLock_Board'+str(boat)))
 for warp in j['warp_events']:warp['elevation']=3
 mp.write_text(json.dumps(j,indent=2)+'\n')
 header='// Generated from the Porymap-authored 80x29 plan.\n'
 for key,value in [('WIDTH',W),('HEIGHT',H),('BERTH_ROW',BERTH_ROW),('CHANNEL_ROW',CHANNEL_ROW),('ENTRY_X',ENTRY[0]),('ENTRY_Y',ENTRY[1]),('HULL_OFFSET',HULL_OFFSET)]:header+=f'#define LOCK_{key} {value}\n'
 for typ,name,values in [('u8','sBank',BANK),('u8','sStair',STAIR),('u8','sShore',SHORE),('s8','sBankDirection',DIR),('u8','sCoreX',CORE)]:header+=f'static const {typ} {name}[] = {{'+','.join(map(str,values))+'};\n'
 header+='static const u8 sDockMask[] = {7,2,7,4,7,6};\n'
 controls={'ABForward':(10,0,1),'ABReverse':(10,1,0),'BCForward':(10,1,2),'BCReverse':(10,2,1),'ServiceMoor':(12,0,0),'Chain':(13,0,0),'FinalMoor':(14,0,0),'Reset':(15,0,0)}
 header+='static const u8 sLockControls[][5] = {\n'
 for n,x,y,s in consoles:
  if s in controls:header+=' {'+','.join(map(str,(x,y,*controls[s])))+'},\n'
 header+='};\n'
 runs=[];offsets=[]
 for value in range(27):
  levels=(value%3,value//3%3,value//9)
  if sum(levels)!=4:offsets.append(0);continue
  offsets.append(len(runs));tiles=draw((levels,0,0,4,0,False),include_boats=False)
  for tile in tiles:
   if runs and len(runs)>offsets[-1] and runs[-1][1]==tile:runs[-1][0]+=1
   else:runs.append([1,tile])
 header+='struct LockMapRun {u16 count;u16 tile;};\nstatic const u16 sLockMapOffsets[] = {'+','.join(map(str,offsets))+'};\n'
 header+='static const struct LockMapRun sLockMapRuns[] = {\n'+''.join(' {%d,0x%04x},\n'%tuple(v) for v in runs)+'};\n'
 (R/'src/data/havora_lock_geometry.h').write_text(header)
 (R/'tools/havora/fixed-lock-geometry.json').write_text(json.dumps(dict(width=W,height=H,banks=BANK,shore=SHORE,direction=DIR,berth_row=BERTH_ROW,channel_row=CHANNEL_ROW,paths=paths,consoles=consoles),indent=2)+'\n')
 print('Built authored 80x29 water overlays; Porymap source preserved in authored.bin')
if __name__=='__main__':build()
