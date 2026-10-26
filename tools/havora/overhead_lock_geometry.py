"""Artwork-first water profiles for the user's 80x27 Havora gym.

No puzzle paths, cliff-kit placement, or boat approaches are generated here.
The independent LOW/MID/HIGH profiles come from the three supplied pictures.
"""
from pathlib import Path
import json,struct
R=Path(__file__).resolve().parents[2]
ARTWORK_REVIEW=True
W,H=80,27
BANK=[1,23,28,50,75,55];SHORE=[4,23,31,50,75,58]
DIR=[1,-1,1,-1,-1,1];STAIR=[2,25,29,52,78,55]
POOLS=[(5,18),(32,18),(59,16)];CORE=[14,40,66]
BERTH_ROW=8;CHANNEL_ROW=22;HULL_OFFSET=4;ENTRY=(3,25)
DOCK=[{0,1,2},{1},{0,1,2},{2},{0,1,2},{1,2}]
ANCHORS=[(2,6),(25,6),(29,6),(52,6),(77,6),(56,6),(40,10),(65,20)]
layout=R/'data/layouts/Havora_Gym';mp=R/'data/maps/Havora_Gym/map.json'
def words(p):
 b=p.read_bytes();return list(struct.unpack('<'+'H'*(len(b)//2),b))
authored=words(layout/'authored.bin')
# Independent complete height snapshots aligned to the latest Porymap map.
refs=[words(layout/'reference_states'/f'all-{name}.bin') for name in ['low','mid','high']]
SECTION_COLUMNS=[(0,27),(28,54),(55,80)]
objects=json.loads(mp.read_text())['object_events']
ACTOR_DEFS=[(o['graphics_id'].removeprefix('OBJ_EVENT_GFX_'),o['x'],o['y'],o['elevation'],o['script'].removeprefix('HavoraTrial_')) for o in objects]
ACTORS={(x,y) for _,x,y,_,_ in ACTOR_DEFS}
consoles=[]
for e in json.loads(mp.read_text())['bg_events']:
 s=e['script'].removeprefix('HavoraLock_');x,y=e['x'],e['y']
 if s.startswith('Board'):continue
 n=0 if x<=4 else 1 if x<=26 else 2 if x<=31 else 4 if x>=75 else 5 if x>=55 else 3 if x>=49 else 6
 consoles.append((n,x,y,s))
base=authored.copy();paths={}
def berth(node,boat):return SHORE[node],BERTH_ROW+boat*3
def draw(state,include_boats=True):
 levels=state[0];b=authored.copy()
 for ch,(left,right) in enumerate(SECTION_COLUMNS):
  ref=refs[levels[ch]]
  for y in range(3,H):
   for x in range(left,right):b[y*W+x]=ref[y*W+x]
 for n,x,y,s in consoles:
  if s=='Status' and n<6 and authored[y*W+x]&1023 in (0x376,0x387,0x377):b[y*W+x]=(authored[y*W+x]&~1023)|[0x376,0x387,0x377][levels[n//2]]
 # Preserve the author's boat positions and pixels; sailing is deferred until
 # the new puzzle is designed. Never stamp boats using the previous offsets.
 if not include_boats:
  for i,v in enumerate(b):
   if 0x2bc<=v&1023<=0x2c4 or 0x390<=v&1023<=0x398:b[i]=0x1682
 return b

def build():
 default=draw(((0,0,0),0,0,4,0,False))
 for name,tiles in [('base',authored),('map',default)]:
  (layout/(name+'.bin')).write_bytes(struct.pack('<'+'H'*len(tiles),*tiles))
 header='// Generated from section water artwork. All 27 independent height combinations.\n'
 captain=next(i+1 for i,o in enumerate(objects) if o['script']=='HavoraTrial_Captain')
 header+=f'#define LOCK_CAPTAIN_LOCAL_ID {captain}\n'
 for key,value in [('WIDTH',W),('HEIGHT',H),('BERTH_ROW',BERTH_ROW),('CHANNEL_ROW',CHANNEL_ROW),('ENTRY_X',ENTRY[0]),('ENTRY_Y',ENTRY[1]),('HULL_OFFSET',HULL_OFFSET)]:header+=f'#define LOCK_{key} {value}\n'
 for typ,name,values in [('u8','sBank',BANK),('u8','sStair',STAIR),('u8','sShore',SHORE),('s8','sBankDirection',DIR),('u8','sCoreX',CORE)]:header+=f'static const {typ} {name}[] = {{'+','.join(map(str,values))+'};\n'
 header+='static const u8 sDockMask[] = {7,2,7,4,7,6};\n'
 controls={'ABForward':(10,0,1),'ABReverse':(10,1,0),'BCForward':(10,1,2),'BCReverse':(10,2,1),'ServiceMoor':(12,0,0),'Chain':(13,0,0),'FinalMoor':(14,0,0),'Reset':(15,0,0)}
 header+='static const u8 sLockControls[][5] = {\n'
 for n,x,y,s in consoles:
  if s in controls:header+=' {'+','.join(map(str,(x,y,*controls[s])))+'},\n'
 header+='};\n';runs=[];offsets=[]
 for value in range(27):
  levels=(value%3,value//3%3,value//9);offsets.append(len(runs))
  for tile in draw((levels,0,0,4,0,False)):
   if runs and len(runs)>offsets[-1] and runs[-1][1]==tile:runs[-1][0]+=1
   else:runs.append([1,tile])
 header+='struct LockMapRun {u16 count;u16 tile;};\nstatic const u16 sLockMapOffsets[] = {'+','.join(map(str,offsets))+'};\n'
 header+='static const struct LockMapRun sLockMapRuns[] = {\n'+''.join(' {%d,0x%04x},\n'%tuple(v) for v in runs)+'};\n'
 (R/'src/data/havora_lock_geometry.h').write_text(header)
 (R/'tools/havora/fixed-lock-geometry.json').write_text(json.dumps(dict(width=W,height=H,default_water=[0,0,0],mode='artwork review; puzzle pending',banks=BANK,shore=SHORE,direction=DIR,berth_row=BERTH_ROW,channel_row=CHANNEL_ROW,paths={},consoles=consoles),indent=2)+'\n')
 print('Built LOW/LOW/LOW default and all 27 independent artwork profiles; no puzzle paths added')
if __name__=='__main__':build()
