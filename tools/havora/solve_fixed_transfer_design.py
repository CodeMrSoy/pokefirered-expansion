"""Abstract fixed-transfer puzzle design. Does not alter the ROM or map assets.
Nodes are raised dry deck groups; available boat landings vary by water height.
A deck group may have two mooring slots so crews can change boats there.
Each action is one decision, not a step/frame. Battles are excluded from search.
"""
from collections import deque
from pathlib import Path
import json
NAMES=['A west quay','A inner landing','B west quay','B upper service berth','C control quay','C outer mooring','Service platform','Captain deck']
DOCK=[{0,1,2},{1},{0,1,2},{2},{0,1,2},{1,2}]
# Water, foot position, launch berth, cargo berth, mooring (0/free,1/service,2/final), release
START=((2,2,0),0,0,4,0,False)
PUMPS={0:(0,1),1:(0,1),2:(1,2),4:(0,1),5:(1,2),6:(1,2)}
def edges(s):
 w,p,a,b,m,r=s
 # controls always on dry raised platforms; boarding uses level-specific docks.
 if p in PUMPS:
  pairs=[PUMPS[p]]+([(1,2)] if p==4 else [])
  for src,dst in [direction for i,j in pairs for direction in [(i,j),(j,i)]]:
   if w[src]>0 and w[dst]<2:
    ww=list(w);ww[src]-=1;ww[dst]+=1
    yield f'Transfer {"ABC"[src]} > {"ABC"[dst]} at {NAMES[p]}',(tuple(ww),p,a,b,m,r)
 # Exposed low service floors and middle catwalk between A/B.
 walks=[(2,3)]
 if w[0]==0:walks.append((0,1))
 if w[1]==0:walks.append((2,3))
 if w[2]==0:walks.append((4,5))
 if w[0]==w[1]==1:walks.append((1,2))
 if w[1]==w[2]==1:walks.append((2,4))
 if m==1 and b==3 and w[1]==2:walks.append((3,6))
 if m==2 and b==5 and w[1]==w[2]==2:walks.extend([(3,5),(3,7),(5,7)])
 for x,y in walks:
  if p in (x,y):
   dest=y if p==x else x
   yield f'Walk to {NAMES[dest]}',(w,dest,a,b,m,r)
 if p==3 and b==3 and w[1]==2:
  if m==0:yield 'Secure cargo boat as service bridge',(w,p,a,b,1,r)
  if m==1:yield 'Release cargo boat from service bridge',(w,p,a,b,0,r)
 if p==6 and w[1]<2 and not r:
  yield 'Release captain-islet mooring chain',(w,p,a,b,m,True)
 if p==4 and b==5 and w[1]==w[2]==2 and m==0 and r:
  yield 'Tension cargo boat as final bridge from control quay',(w,p,a,b,2,r)
 if p<6:
  for boat,at in [(0,a),(1,b)]:
   if at!=p or (boat==1 and m):continue
   if w[p//2] not in DOCK[p]:continue
   reachable={p//2}
   for _ in range(2):
    for ch in list(reachable):
     for c in [ch-1,ch+1]:
      if 0<=c<3 and w[c]==w[ch]:reachable.add(c)
   for dest in range(6):
    if dest==p or dest//2 not in reachable or w[dest//2] not in DOCK[dest]:continue
    aa,bb=(dest,b) if boat==0 else (a,dest)
    yield f'Ride {"launch" if boat==0 else "cargo"} to {NAMES[dest]}',(w,dest,aa,bb,m,r)
def goal(s):return s[1]==7

def search(reject=None):
    q=deque([START]);previous={START:None};labels={};adj={};goals=[]
    while q:
        state=q.popleft()
        outgoing=[(a,n) for a,n in edges(state) if reject is None or not reject(state,a,n)]
        adj[state]=outgoing
        if goal(state):goals.append(state)
        for action,n in outgoing:
            assert sum(n[0])==4 and all(0<=v<=2 for v in n[0])
            assert not(n[0][0]==n[0][1] and n[0][1]==n[0][2])
            if n not in previous:
                previous[n]=state;labels[n]=action;q.append(n)
    path=[]
    if goals:
        state=goals[0]
        while previous[state] is not None:
            path.append({'action':labels[state],'state':state})
            state=previous[state]
        path.reverse()
    return previous,adj,goals,path

def main():
    previous,adj,goals,path=search()
    assert goals
    reverse={state:[] for state in previous}
    for state,es in adj.items():
        for _,n in es:reverse[n].append(state)
    safe=set(goals);todo=deque(goals)
    while todo:
        for state in reverse[todo.popleft()]:
            if state not in safe:safe.add(state);todo.append(state)
    assert safe==set(previous),'Natural recovery requires a reset in some states'
    checks={
      'cargo_must_move':lambda s,a,n:a.startswith('Ride cargo'),
      'AB_transfers_required':lambda s,a,n:a.startswith('Transfer A > B') or a.startswith('Transfer B > A'),
      'low_C_shore_required':lambda s,a,n:a.startswith('Walk') and {s[1],n[1]}=={4,5} and s[0][2]==0,
      'launch_must_be_reused_from_C':lambda s,a,n:a.startswith('Ride launch') and s[2]//2==2,
      'maintenance_release_required':lambda s,a,n:a.startswith('Release captain'),
    }
    for label,reject in checks.items():
        _,_,g,_=search(reject)
        assert not g,label+' is bypassable'
    assert len(path)==25
    result={
      'status':'mapped three-lock prototype; emulator evidence in docs/havora/three-lock-prototype.md',
      'reachable_states':len(previous),'goal_states':len(goals),
      'naturally_recoverable_states':len(safe),'shortest_decision_count':len(path),
      'transfers_on_shortest_route':sum(p['action'].startswith('Transfer') for p in path),
      'water_levels':['LOW','MID','HIGH'],'transferable_units_above_LOW':4,
      'node_names':NAMES,'dock_levels':{NAMES[i]:sorted(v) for i,v in enumerate(DOCK)},
      'start':START,'required_dependencies':list(checks),'shortest_solution':path,
      'reset':'Return player, water, boats, moorings and maintenance release to START; trainer victories and crest retained outside this model.'
    }
    root=Path(__file__).resolve().parents[2]
    (root/'docs/havora/fixed-transfer-design.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['reachable_states','naturally_recoverable_states','shortest_decision_count','transfers_on_shortest_route','required_dependencies']},indent=2))
if __name__=='__main__':main()
