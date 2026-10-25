"""Preserve Havora outdoors and independently solve the native gym state graph."""
from pathlib import Path
from collections import deque
import json,struct,subprocess
R=Path(__file__).resolve().parents[2];BASE='0b13302d7807bd5df1df20712a77335a6ebf17dd'
old=lambda p:subprocess.check_output(['git','show',BASE+':'+p],cwd=R)
ls=json.loads((R/'data/layouts/layouts.json').read_text())['layouts'];before=json.loads(old('data/layouts/layouts.json'))['layouts'];assert ls[:-1]==before
for l in before:
 for k in ['blockdata_filepath','border_filepath']:assert old(l[k])==(R/l[k]).read_bytes(),l[k]
for p in subprocess.check_output(['git','ls-tree','-r','--name-only',BASE,'--','data/maps','data/tilesets'],cwd=R,text=True).splitlines():
 if p.startswith('data/maps/QuantumHavoraGym/'):continue
 a=old(p);b=(R/p).read_bytes()
 if p.endswith('.pal'):a=a.replace(b'\r\n',b'\n');b=b.replace(b'\r\n',b'\n')
 assert a==b,p
l=ls[-1];assert (l['width'],l['height'])==(40,36)
w=struct.unpack('<1440H',(R/l['blockdata_filepath']).read_bytes());m=json.loads((R/'data/maps/QuantumHavoraGym/map.json').read_text());actors={(o['x'],o['y']) for o in m['object_events']}
for e in m['object_events']+m['bg_events']+m['warp_events']:assert 0<=e['x']<40 and 0<=e['y']<36
assert len(m['warp_events'])==3 and all(e['dest_map']=='MAP_HAVORA_WEST_QUADRANT' and e['dest_warp_id']=='0' for e in m['warp_events'])
# Region abstraction: keep an arbitrary reachable floor cell, normalize to the
# component's smallest cell after each action to avoid duplicate graph states.
def flood(s,p,start):
 blocked={i for i,v in enumerate(w) if v&0xc00}
 def rect(x,y,ww,hh,closed):
  for yy in range(y,y+hh):
   for xx in range(x,x+ww):
    if closed:blocked.add(yy*40+xx)
    else:blocked.discard(yy*40+xx)
 rect(4,29,3,1,not s&4);rect(4,9,3,3,not s&8);rect(33,9,3,3,not p&4);rect(33,29,3,1,not p&4)
 blocked|={y*40+x for x,y in actors};q=deque([start]);seen={start}
 while q:
  i=q.popleft();x,y=i%40,i//40
  for xx,yy in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
   j=yy*40+xx
   if 0<=xx<40 and 0<=yy<36 and j not in blocked and j not in seen:seen.add(j);q.append(j)
 return seen
start=(0,0,33*40+20);todo=deque([start]);seen={start};edges={};goals=set();hall=set()
while todo:
 s,p,i=todo.popleft();floor=flood(s,p,i)
 def near(x,y):return any(yy*40+xx in floor for xx,yy in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)] if 0<=xx<40 and 0<=yy<36)
 actions=[]
 if near(5,31):actions.append((s^4,p,i))
 if near(35,31):actions.append((0,p,i))
 if near(32,24) and not p&1:actions.append((s,p|1,i))
 if near(7,13) and not p&2:actions.append((s,p|2,i))
 if near(20,5) and not p&4:actions.append((s,p|4,i))
 if near(33,20) and p&1 and s&1:actions.append((s^2,p,i))
 if near(5,14) and p&2:actions.append((s|8,p,i))
 y=14 if s&2 else 26
 for x in [9,29]:
  if y*40+x in floor:
   same=bool(s&1)==(x==29);dest=(29 if x==9 else 9) if same else x
   actions.append((s^1,p,y*40+dest))
 if 33*40+20 in floor:hall.add((s,p,i))
 if p&4 and 33*40+20 in floor:goals.add((s,p,i))
 out=[]
 for ss,pp,j in actions:
  jj=min(flood(ss,pp,j));n=(ss,pp,jj);out.append(n)
  if n not in seen:seen.add(n);todo.append(n)
 edges[(s,p,i)]=out
assert goals,'Captain/exit unreachable'
# Every reachable state can return to the entrance hall and its reset bell.
rev={n:[] for n in seen}
for n,es in edges.items():
 for e in es:rev[e].append(n)
q=deque(hall);safe=set(hall)
while q:
 for n in rev[q.popleft()]:
  if n not in safe:safe.add(n);q.append(n)
assert seen==safe,('stranded states',seen-safe)
print(f'PASS {len(seen)} reachable puzzle states; captain and exit reachable; every state has a return/reset route; all pre-existing outdoor layouts, tilesets, events, warps and connections preserved')
