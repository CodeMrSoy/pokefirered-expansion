"""Audit the current directional gym, its compiled map data and physical access.

This is a source/map test. Emulator suites remain necessary for rendering,
frame timing, battle execution and save/load behavior.
"""
from pathlib import Path
from collections import deque
from functools import lru_cache
from itertools import product
import json, re, struct, sys

R = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(R / 'tools/havora'))
import overhead_lock_geometry as geo
from tidal_color_rules import apply_switch
from boat_routes import route, water_map

spec = json.loads((R / 'tools/havora/tidal_trial.json').read_text())
P, L = spec['platforms'], spec['links']
ALL = sum(p['victory'] for p in P)
SCRIPTS = (R / 'data/maps/Havora_Gym/scripts.inc').read_text()
MAP = json.loads((R / 'data/maps/Havora_Gym/map.json').read_text())

@lru_cache(None)
def tiles(w):
    return tuple(geo.draw((w, 0, 0, 4, 0, False)))

@lru_cache(None)
def walking(w, start):
    b = tiles(w)
    solid = {tuple(p['npc']) for i, p in enumerate(P) if i != 6 or w[1] != 2}
    solid.add((5, 24))
    if w[2] == 0:
        solid.add((65, 20))
    if b[start[1] * 80 + start[0]] & 0xc00:
        return frozenset()
    q = deque([start]); seen = {start}
    while q:
        x, y = q.popleft(); z = b[y * 80 + x] >> 12
        for xx, yy in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
            if not (0 <= xx < 80 and 0 <= yy < 27) or (xx, yy) in seen or (xx, yy) in solid:
                continue
            t = b[yy * 80 + xx]; nz = t >> 12
            if t & 0xc00 or z not in (0,15) and nz not in (0,15) and z != nz:
                continue
            seen.add((xx, yy)); q.append((xx, yy))
    return frozenset(seen)

@lru_cache(None)
def sailing(w, i):
    l = L[i]
    b = water_map(w)
    if any(b[y*80+x] & 0xc00 for x,y in (l['pad_from'], l['pad_to'])):
        return False
    return route(w, l['pad_from'], l['pad_to']) is not None

def edges(s):
    w,n,v,b = s; p = P[n]
    if not v & p['victory']:
        yield ('battle', n), (w,n,v | p['victory'],b)
    else:
        for k, color in enumerate(p['switch_colors']):
            nw = apply_switch(w, color.lower())
            if n == 6 and nw[1] == 2:
                continue
            yield ('switch',n,k), (nw,n,v,b | 1<<n)
    for i,l in enumerate(L):
        if n != l['from'] or v & l['clearance'] != l['clearance'] or not b & 1<<n:
            continue
        if any(a >= 0 and a != z for a,z in zip(l['water'],w)) or not sailing(w,i):
            continue
        yield ('travel',i), (w,l['to'],v,b)
    if n in (4,5) and w[2] == 0:
        yield ('walk',9-n), (w,9-n,v,b)

def goal(s):
    w,n,v,b = s
    return v == ALL and b == 127 and w[2] == 0 and n in (4,5)

start = ((0,0,0),0,0,0)
q = deque([start]); prev = {start:None}; actions = {}; adj = {}
while q:
    s = q.popleft(); adj[s] = list(edges(s))
    for a,t in adj[s]:
        if t not in prev:
            prev[t] = s; actions[t] = a; q.append(t)
goals = {s for s in prev if goal(s)}
assert goals, 'gym has no solution'
reverse = {s:[] for s in prev}
for s,es in adj.items():
    for a,t in es:
        reverse[t].append(s)
safe = set(goals); q = deque(goals)
while q:
    for s in reverse[q.popleft()]:
        if s not in safe:
            safe.add(s); q.append(s)
assert safe == set(prev), ('stranded states without reset',len(set(prev)-safe))
print(f'PASS exhaustive graph: {len(prev)} reachable states, {len(goals)} captain-ready states; every state can finish without reset')

# Every route onto a platform must allow the trainer, switches and all exposed
# outgoing pads to be reached through the actual collision/elevation grid.
physical = 0
for n,p in enumerate(P):
    for w in product(range(3),repeat=3):
        if n == 6 and w[1] == 2:
            continue
        b = tiles(w)
        x,y = p['switches'][0]
        anchors = [(xx,yy) for xx,yy in ((x+1,y),(x-1,y),(x,y+1),(x,y-1))
                   if not b[yy*80+xx]&0xc00 and (xx,yy) != tuple(p['npc'])]
        assert anchors, ('no usable control face',n,w)
        seen = walking(w,anchors[0])
        for target in [p['npc']] + p['switches']:
            assert any(abs(xx-target[0])+abs(yy-target[1]) == 1 for xx,yy in seen), ('unreachable control/trainer',n,w,target)
        for i,l in enumerate(L):
            if any(a >= 0 and a != z for a,z in zip(l['water'],w)) or not sailing(w,i):
                continue
            if l['from'] == n and not b[l['pad_from'][1]*80+l['pad_from'][0]]&0xc00:
                assert tuple(l['pad_from']) in seen, ('outbound pad unreachable',n,w,l['source_label'])
            if l['to'] == n and not b[l['pad_to'][1]*80+l['pad_to'][0]]&0xc00:
                assert tuple(l['pad_to']) in seen, ('arrival disconnected',n,w,l['destination_label'])
        physical += 1
for w in product(range(3),repeat=3):
    seen = walking(w,(56,6))
    assert ((77,6) in seen) == (w[2] == 0), ('C foot crossing',w)
    if w[2] == 0:
        assert any(abs(x-65)+abs(y-20)==1 for x,y in seen), ('captain unreachable',w)
print(f'PASS physical access: {physical} platform/water profiles; every exposed pad, trainer and switch; C crossing and captain at LOW')

# All map event coordinates, including removed lever spots, are checked against
# the generated native platform/link tables and original authored artwork.
for n,p in enumerate(P):
    assert len(p['switches']) == len(set(p['switch_colors'])) == 2
    for k,(x,y) in enumerate(p['switches']):
        assert sum(e['x']==x and e['y']==y and e['script']==f'HavoraTide_Switch{n}_{k}' for e in MAP['bg_events']) == 1
    for x,y in p.get('removed_switches',[]):
        assert not any(e['x']==x and e['y']==y and e['script'].startswith('HavoraTide_Switch') for e in MAP['bg_events'])
    obj = next(o for o in MAP['object_events'] if o['script']=='HavoraTrial_'+p['trainer'])
    assert [obj['x'],obj['y']] == p['npc']
    won = SCRIPTS.split('HavoraTrial_'+p['trainer']+'Won::',1)[1].split('\nHavora',1)[0]
    assert f'setvar VAR_0x8005, {p["victory"]}\n' in won
header = (R/'src/data/havora_tidal_trial.h').read_text()
platform_text = header.split('sPlatforms[] = {',1)[1].split('\n};',1)[0]
for line,p in zip(platform_text.strip().splitlines(),P,strict=True):
    values = list(map(int,re.findall(r'-?\d+',line)))
    expected = [p['section'],p['remote'],p['victory'],p['prerequisite']] + p['water'] + sum(p['switches'],[]) + [0,0]
    assert values == expected, ('native platform table mismatch',p['name'])
link_text = header.split('sLinks[] = {',1)[1].split('\n};',1)[0]
for line,l in zip(link_text.strip().splitlines(),L,strict=True):
    assert list(map(int,re.findall(r'-?\d+',line))) == [l['from'],l['to']] + l['pad_from'] + l['pad_to'] + l['water'] + [l['clearance']]
header = (R/'src/data/havora_lock_geometry.h').read_text()
offsets = list(map(int,re.search(r'sLockMapOffsets\[\] = \{([^}]+)',header).group(1).split(',')))
runs = [(int(n),int(t,16)) for n,t in re.findall(r'\{(\d+),0x([0-9a-f]+)\}',header)]
assert len(offsets) == 27
for value,offset in enumerate(offsets):
    end = offsets[value+1] if value+1<len(offsets) else len(runs)
    decoded = tuple(tile for count,tile in runs[offset:end] for _ in range(count))
    w = (value%3,value//3%3,value//9)
    assert decoded == tiles(w), ('native map profile differs',w)
print('PASS 14 live lever events, 7 removed lever events, 7 victory scripts, 9 native route bindings and all 27 native RLE maps')

# Gate predicates from the production C are also reviewed by the emulator
# suite; the independent model cannot reach its goal with a station omitted.
for n in range(7):
    restricted = {start}; q = deque([start])
    while q:
        for a,t in adj[q.popleft()]:
            if a[0] in ('battle','switch') and a[1] == n:
                continue
            if t not in restricted:
                restricted.add(t); q.append(t)
    assert not (restricted & goals), ('station bypass',n)
print('PASS removing any station battle/switch makes the captain unreachable')

trainer_source=(R/'src/data/trainers.party').read_text()
trainer_generated=(R/'src/data/trainers.h').read_text()
expected_counts={'HARBORMASTER':2,'DOCK_CREW':2,'DIVER':4,'LOCKKEEPER':3,'ENGINEER':3,'FIRST_MATE':4,'NAVIGATOR':3,'CAPTAIN':6}
for key,count in expected_counts.items():
    name='TRAINER_HAVORA_'+key
    body=trainer_source.split('=== '+name+' ===',1)[1].split('=== ',1)[0]
    assert 'Double Battle: Yes' in body and 'AI: Check Bad Move / Try To Faint / Check Viability / HP Aware' in body
    assert len(re.findall(r'^Level: ',body,re.M))==count,(name,'source party count')
    generated=trainer_generated.split('[DIFFICULTY_NORMAL]['+name+']',1)[1].split('[DIFFICULTY_NORMAL]',1)[0]
    assert '.battleType = TRAINER_BATTLE_TYPE_DOUBLES' in generated
    assert re.search(r'\.partySize = '+str(count)+r',',generated)
    assert 'trainerbattle_double '+name+',' in SCRIPTS
print('PASS all 8 doubles encounter scripts and source/generated party counts; captain has 6 Pokemon')
