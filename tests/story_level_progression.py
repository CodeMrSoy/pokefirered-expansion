"""Audit area deltas and execute the production cap/experience code on the host."""
import json
from pathlib import Path
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
plan = json.loads((ROOT / 'tools/progression/story-levels.json').read_text())
stages = {s['id']: s for s in plan['milestones']}

def original(path):
    return subprocess.check_output(['git', 'show', plan['baseline_commit'] + ':' + path], cwd=ROOT).decode()

def delta(stage):
    s = stages[stage]
    return s['cap'] - s['old_cap']

def parties(source):
    return dict(re.findall(r'=== (\w+) ===(.*?)(?==== |\Z)', source, re.S))

def levels(body):
    return list(map(int, re.findall(r'^Level: (\d+)$', body, re.M)))

source = (ROOT / 'src/data/trainers.party').read_text()
before = parties(original('src/data/trainers.party'))
after = parties(source)
assert before.keys() == after.keys()
for tid, body in after.items():
    if tid in plan['trainers']:
        row = plan['trainers'][tid]
        assert levels(before[tid]) == row['before'], tid
        assert levels(body) == row['after'] == [n + delta(row['stage']) for n in row['before']], tid
        assert re.sub(r'^Level: \d+$', 'Level: X', body, flags=re.M) == re.sub(r'^Level: \d+$', 'Level: X', before[tid], flags=re.M), tid
    else:
        assert body == before[tid], ('unintended trainer change', tid)
    assert all(1 <= n <= 100 for n in levels(body)), tid

# Gym aces and every starter variant of the Champion must hit their exact cap.
for tid, cap in {
    'TRAINER_LEADER_BROCK': 14, 'TRAINER_LEADER_MISTY': 21,
    'TRAINER_LEADER_LT_SURGE': 24, 'TRAINER_LEADER_ERIKA': 29,
    'TRAINER_LEADER_KOGA': 35, 'TRAINER_HAVORA_CAPTAIN': 46,
    'TRAINER_LEADER_SABRINA': 50, 'TRAINER_LEADER_BLAINE': 63,
    'TRAINER_LEADER_GIOVANNI': 82,
    **{'TRAINER_CHAMPION_FIRST_' + s: 90 for s in ('SQUIRTLE','BULBASAUR','CHARMANDER')},
}.items():
    assert max(levels(after[tid])) == cap, tid
for tid in ('LORELEI','BRUNO','AGATHA','LANCE'):
    tid = 'TRAINER_ELITE_FOUR_' + tid
    assert levels(after[tid]) == [n + 27 for n in levels(before[tid])]

# Coverage includes routes in the shared trainer scripts and active Vs. Seeker tiers.
header = (ROOT / 'src/data/trainers.h').read_text()
active = set(re.findall(r'\[DIFFICULTY_NORMAL\]\[(TRAINER_\w+)\]', header))
for path in (ROOT / 'data/maps').glob('*/scripts.inc'):
    mid = json.loads((path.parent / 'map.json').read_text())['id']
    stage = plan['map_stages'].get(mid)
    if stage and stages[stage]['old_cap'] is not None and delta(stage):
        for tid in set(re.findall(r'\bTRAINER_\w+', path.read_text())) & active:
            assert plan['trainers'][tid]['stage'] == stage, (path, tid)
shared = (ROOT / 'data/scripts/trainers.inc').read_text()
for label, body in re.findall(r'^(\w+)::(.*?)(?=^\w+::|\Z)', shared, re.M | re.S):
    match = re.match(r'Route(\d+)_', label)
    if not match:
        continue
    mid = 'MAP_ROUTE' + match[1]
    stage = plan['map_stages'].get(mid)
    if stage and delta(stage):
        for tid in set(re.findall(r'\bTRAINER_\w+', body)) & active:
            assert plan['trainers'][tid]['stage'] == stage, tid
rematches = (ROOT / 'src/vs_seeker.c').read_text().split('static const struct RematchData sRematches[] = {', 1)[1].split('\n};', 1)[0]
for ids, mid in re.findall(r'\{\s*\{([^}]+)\},\s*MAP\((MAP_\w+)\)\s*\}', rematches):
    stage = plan['map_stages'].get(mid)
    if stage and delta(stage):
        for tid in set(re.findall(r'\bTRAINER_\w+', ids)) & active:
            assert plan['trainers'][tid]['stage'] == stage, tid
# The checked-in generated header must change only numeric levels.
assert re.sub(r'\.lvl = \d+', '.lvl = X', header) == re.sub(r'\.lvl = \d+', '.lvl = X', original('src/data/trainers.h'))
for tid, row in plan['trainers'].items():
    body = header.split('[DIFFICULTY_NORMAL][' + tid + '] =', 1)[1].split('\n    [DIFFICULTY_NORMAL]', 1)[0]
    assert list(map(int, re.findall(r'\.lvl = (\d+)', body))) == row['after'], tid
print(f"PASS {len(plan['trainers'])} active trainer teams: exact deltas, route/Gym/rematch coverage, unchanged sets, generated header")

wild = json.loads((ROOT / 'src/data/wild_encounters.json').read_text())
old_wild = json.loads(original('src/data/wild_encounters.json'))
fields = ('land_mons', 'water_mons', 'rock_smash_mons', 'fishing_mons')
def strip_levels(value):
    value = json.loads(json.dumps(value))
    for g in value['wild_encounter_groups']:
        for e in g['encounters']:
            for kind in fields:
                for mon in e.get(kind, {}).get('mons', []):
                    mon.pop('min_level'); mon.pop('max_level')
    return value
# Havora is new in this batch; its species/access audit has its own test.
def without_havora(value):
    value = json.loads(json.dumps(value))
    for g in value['wild_encounter_groups']:
        g['encounters'] = [e for e in g['encounters'] if not e['map'].startswith('MAP_HAVORA_')]
    return value
assert strip_levels(without_havora(wild)) == strip_levels(without_havora(old_wild))
old_entries = {e['base_label']: e for g in old_wild['wild_encounter_groups'] for e in g['encounters']}
for g in wild['wild_encounter_groups']:
    for e in g['encounters']:
        label = e['base_label']
        stage = plan['map_stages'].get(e['map'])
        changed = stage and stages[stage]['old_cap'] is not None and delta(stage)
        assert bool(label in plan['wild_encounters']) == bool(changed), label
        if label not in plan['wild_encounters']:
            assert e == old_entries[label], ('unintended encounter change', label)
            continue
        row = plan['wild_encounters'][label]
        assert row['map'] == e['map'] and row['stage'] == stage
        for kind in fields:
            if kind not in e:
                assert kind not in row['after']
                continue
            actual = [[m['min_level'], m['max_level']] for m in e[kind]['mons']]
            expected = [[max(1, n + delta(stage)) for n in pair] for pair in row['before'][kind]]
            assert actual == row['after'][kind] == expected, (label, kind)
            if not e['map'].startswith('MAP_HAVORA_'):
                assert row['before'][kind] == [[m['min_level'],m['max_level']] for m in old_entries[label][kind]['mons']]
            assert all(1 <= a <= b <= 100 for a,b in actual)
for path, row in plan['scripted_wild'].items():
    old = original(path)
    expected = re.sub(r'(\bsetwildbattle\s+SPECIES_\w+,\s*)(\d+)', lambda m: m[1] + str(int(m[2]) + delta(row['stage'])), old)
    assert (ROOT / path).read_text() == expected, path
print(f"PASS {len(plan['wild_encounters'])} encounter tables and six scripted wild encounter maps; species, slots and odds retained")

# Compile the actual production functions, using only mocked save access.
caps = (ROOT / 'src/caps.c').read_text()
caps = caps[caps.index('u32 GetCurrentLevelCap'):caps.index('u32 GetCurrentEVCap')]
prefix = r'''
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include "constants/flags.h"
#include "constants/vars.h"
typedef uint32_t u32;
typedef uint16_t u16;
typedef uint8_t u8;
typedef uint32_t bool32;
#define ARRAY_COUNT(a) (sizeof(a)/sizeof((a)[0]))
#define MAX_LEVEL 100
#define TRUE 1
#define FALSE 0
#include "config/caps.h"
static u8 flags[0x1000];
static u16 vars[0x10000];
static u32 FlagGet(u32 id) { assert(id < sizeof(flags)); return flags[id]; }
static u32 VarGet(u32 id) { return vars[id]; }
'''
main = '\nint main(void) {\n'
main += 'const u16 milestones[] = {' + ','.join(m['completion_flag'] or '0' for m in plan['milestones']) + '};\n'
main += 'const u8 crests[] = {' + ','.join(str(m.get('crest_mask',0)) for m in plan['milestones']) + '};\n'
main += 'const u8 expected[] = {' + ','.join(str(m['cap']) for m in plan['milestones']) + '};\n'
main += r'''
 for (u32 i=0; i<ARRAY_COUNT(expected); i++) {
     assert(GetCurrentLevelCap() == expected[i]);
     assert(GetSoftLevelCapExpValue(expected[i], 100) == 0);
     assert(GetSoftLevelCapExpValue(expected[i]-1, 100) > 0);
     if(milestones[i]) flags[milestones[i]]=1;
     vars[VAR_VIDRA_CRESTS] |= crests[i];
 }
 assert(GetCurrentLevelCap() == 100);
 // Every subset of earned badges/crests must stop at the first unfinished Gym.
 for (u32 mask=0; mask<(1u<<14); mask++) {
     memset(flags,0,sizeof(flags)); memset(vars,0,sizeof(vars));
     u32 first=14;
     for(u32 i=0;i<14;i++) {
         if(mask & (1u<<i)) {
             if(milestones[i]) flags[milestones[i]]=1;
             vars[VAR_VIDRA_CRESTS] |= crests[i];
         } else if(first==14) first=i;
     }
     assert(GetCurrentLevelCap() == ((mask & (1u<<13)) || first==14 ? 100 : expected[first]));
 }
 // Old completed saves are uncapped, even without the newly introduced crests.
 memset(flags,0,sizeof(flags));memset(vars,0,sizeof(vars));
 flags[FLAG_SYS_GAME_CLEAR]=1; assert(GetCurrentLevelCap()==100);
 // Havora's saved trainer flag, crest bit and legacy progress bit all work.
 for(u32 legacy=0;legacy<3;legacy++) {
     memset(flags,0,sizeof(flags));memset(vars,0,sizeof(vars));
     for(u32 i=0;i<5;i++) flags[milestones[i]]=1;
     assert(GetCurrentLevelCap()==46);
     if(legacy==0) flags[TRAINER_FLAGS_START+TRAINER_HAVORA_CAPTAIN]=1;
     if(legacy==1) vars[VAR_VIDRA_CRESTS]=1;
     if(legacy==2) vars[VAR_HAVORA_GYM_PROGRESS]=4;
     assert(GetCurrentLevelCap()==50);
 }
 puts("PASS production C: all 14 caps, all 16,384 milestone combinations, hard EXP limits, Havora legacy saves and game-clear compatibility");
}
'''
with tempfile.TemporaryDirectory() as tmp:
    cfile = Path(tmp) / 'caps.c'
    binary = Path(tmp) / 'caps'
    cfile.write_text(prefix + caps + main)
    subprocess.run(['gcc','-std=gnu17','-Wall','-Wextra','-Werror','-iquote',str(ROOT/'include'),str(cfile),'-o',str(binary)],check=True)
    subprocess.run([str(binary)],check=True)
