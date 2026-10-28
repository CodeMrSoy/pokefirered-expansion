#!/usr/bin/env python3
"""Walk and sail the current complete gym route with no Surf tool or move.

Crew victories are fixtures; this verifies navigation and captain readiness,
not combat. Every walking step and boat trip runs in the compiled game.
"""
from pathlib import Path
source=Path(__file__).with_name('eirik_surf_progression_emulator.py').read_text()
exec(compile(source[:source.index('wailer=constant')],str(Path(__file__)),'exec'))
m.d=m.d/'gym-no-surf';m.d.mkdir(exist_ok=True)
P=json.loads((m.root/'tools/havora/tidal_trial.json').read_text())['platforms']
L=json.loads((m.root/'tools/havora/tidal_trial.json').read_text())['links']
plan=json.loads((m.root/'build/havora-tests/directional-solution.json').read_text())
fixture=b''
for species in (1,4,7,25,133,143):
    fixture+=b'\x23'+struct.pack('<I',(m.symbols['ScrCmd_createmon']|1)+0x2000000)+struct.pack('<BBHHI',0,6,species,100,0)
m.inject(fixture+b'\x02')
for tid in (743,744,746,747,748,749,750):native('SetTrainerFlag',tid)
for v,n in ((0x40d7,0x8000),(0x40d8,0),(0x40da,0)):native('VarSet',v,n)
warp('Havora_Gym',3,25)

def walking(target,exact=False):
    w,h,address=struct.unpack('<iiI',m.read(m.symbols['VMap'],12))
    raw=struct.unpack('<'+'H'*(w*h),m.read(address,w*h*2))
    layout=ptr('gMapHeader')
    primary,secondary=struct.unpack('<II',m.read(layout+16,8))
    attributes=[]
    for tileset,count in ((primary,640),(secondary,384)):
        pointer=struct.unpack('<I',m.read(tileset+20,4))[0]
        attributes.extend(struct.unpack('<'+'I'*count,m.read(pointer,count*4)))
    solid=set()
    player=m.read(m.symbols['gPlayerAvatar']+5,1)[0]
    for i in range(16):
        obj=m.read(m.symbols['gObjectEvents']+i*36,36)
        if i!=player and obj[0]&1 and obj[8]!=254:
            x,y=struct.unpack_from('<hh',obj,16);solid.add((x-7,y-7))
    def good(p):return p==tuple(target) if exact else abs(p[0]-target[0])+abs(p[1]-target[1])==1
    start=pos();queue=collections.deque([start]);prev={start:None};end=None
    while queue:
        x,y=queue.popleft()
        if good((x,y)):end=x,y;break
        old=raw[(y+7)*w+x+7];z=old>>12
        for xx,yy in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
            if not(0<=xx<80 and 0<=yy<27) or (xx,yy) in prev or (xx,yy) in solid:continue
            tile=raw[(yy+7)*w+xx+7];nz=tile>>12
            if tile&0xc00 or attributes[tile&1023]&511 in (0x10,0x11,0x12,0x13,0x15) or z not in (0,15) and nz not in (0,15) and z!=nz:continue
            prev[xx,yy]=(x,y);queue.append((xx,yy))
    if end is None:
        m.snap('no-dry-route')
        print('LOCAL GRID',[[hex(raw[(y+7)*w+x+7]) for x in range(5)] for y in range(3,8)],'solids',solid,flush=True)
    assert end is not None,('No dry route',start,target,value(0x40d7))
    path=[]
    while prev[end] is not None:path.append(end);end=prev[end]
    for x,y in reversed(path):
        px,py=pos();key=7 if x>px else 6 if x<px else 5 if y>py else 4
        m.keys.add(key)
        try:until(lambda:pos()==(x,y),100)
        finally:m.keys.clear()
        m.run(20)
        assert pos()==(x,y),('Walk drift',x,y,pos())

def command(cmd,a=0,b=0):
    for v,n in ((0x8004,cmd),(0x8005,a),(0x8006,b)):native('VarSet',v,n)
    native('HavoraGym_Control')
    until(lambda:not task('MoveBoat') and not task('AnimateTide'),5000)
    return value(0x800d)

for action,state in plan:
    kind=action[0]
    if kind=='battle':
        walking(P[action[1]]['npc']);assert command(22,P[action[1]]['victory'])==1
    elif kind=='switch':
        n,k=action[1:3];walking(P[n]['switches'][k]);assert command(30,n,k)==1,(action,pos())
    elif kind=='travel':
        l=L[action[1]];walking(l['pad_from'],True);assert command(31)==1,(action,pos())
        assert list(pos())==l['pad_to'],('Boat destination',action,pos())
    elif kind=='walk':walking(P[action[1]]['npc'])
    else:raise AssertionError(action)
    assert value(0x40d7)==0x8000+state[0][0]+3*state[0][1]+9*state[0][2]
    assert not owns(constant('ITEM_WAILMER_WAILER','items.h'))
    assert not m.read(m.symbols['gPlayerAvatar'],1)[0]&8
    print('PASS navigation:',action,'position',pos(),flush=True)
walking((65,20))
assert command(24)==1
m.snap('captain-reached-without-surf')
print('PASS complete current gym: dry walking, real boats, all seven crew/switch stations and captain readiness without Surf (crew-win fixtures)',flush=True)
