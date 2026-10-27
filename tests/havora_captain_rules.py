"""Check Eirik's actual Bag predicate and Yes/No encounter script flow."""
from pathlib import Path
import re, subprocess
R=Path(__file__).resolve().parents[1]
source=(R/'src/battle_main.c').read_text()
start=source.index('if (FlagGet(B_FLAG_NO_BAG_USE)',source.index('case B_ACTION_USE_ITEM:',source.index('case B_ACTION_USE_MOVE:')))
condition=source[start+3:source.index('\n                    {',start)].strip()
# Compile the exact production condition, using the real numeric constants.
ids=(R/'include/constants/opponents.h').read_text()
captain=int(re.search(r'#define TRAINER_HAVORA_CAPTAIN\s+(\d+)',ids)[1])
flags=(R/'include/constants/battle.h').read_text()
def flag(name):
    return re.search(r'^#define '+name+r'\s+(\(1 << \d+\))',flags,re.M)[1]
code='#include <assert.h>\n#include <stdio.h>\n'
for name in ['BATTLE_TYPE_TRAINER','BATTLE_TYPE_LINK','BATTLE_TYPE_RECORDED_LINK']:
    code+='#define '+name+' '+flag(name)+'\n'
code+=f'#define TRAINER_HAVORA_CAPTAIN {captain}\n#define B_FLAG_NO_BAG_USE 0\n'
code+='''unsigned gBattleTypeFlags; int globalBan;
struct {unsigned opponentA;} trainer;
#define TRAINER_BATTLE_PARAM trainer
int FlagGet(int flag){(void)flag;return globalBan;}
int blocked(void){return '''+condition+''';}
int main(void){
 globalBan=0;gBattleTypeFlags=BATTLE_TYPE_TRAINER;trainer.opponentA=TRAINER_HAVORA_CAPTAIN;
 assert(blocked());
 trainer.opponentA=TRAINER_HAVORA_CAPTAIN+1;assert(!blocked());
 trainer.opponentA=TRAINER_HAVORA_CAPTAIN;gBattleTypeFlags=0;assert(!blocked());
 gBattleTypeFlags=BATTLE_TYPE_TRAINER|BATTLE_TYPE_LINK;assert(!blocked());
 gBattleTypeFlags=BATTLE_TYPE_TRAINER|BATTLE_TYPE_RECORDED_LINK;assert(!blocked());
 globalBan=1;trainer.opponentA=1;assert(blocked());
 puts("PASS actual compiled Bag condition: Eirik blocked, other/wild/link battles unaffected, existing global ban retained");
}
'''
d=R/'build/havora-tests';d.mkdir(parents=True,exist_ok=True)
p=d/'captain-bag-host.c';p.write_text(code);binary=d/'captain-bag-host'
subprocess.run(['gcc','-Wall','-Wextra','-Werror',str(p),'-o',str(binary)],check=True)
subprocess.run([str(binary)],check=True)
scripts=(R/'data/maps/Havora_Gym/scripts.inc').read_text()
blocks={}
for name,body in re.findall(r'^(\w+)::\n(.*?)(?=^\w+::|\Z)',scripts,re.M|re.S):
    blocks[name]=body.strip().splitlines()
def trace(ready=True,defeated=False,clearance=1):
    label='HavoraTrial_Captain';result=None;events=[]
    for _ in range(20):
        jumped=False
        for raw in blocks[label]:
            line=raw.strip()
            if line.startswith('goto_if_defeated ') and defeated:
                label=line.split(', ')[1];jumped=True;break
            if line=='special HavoraGym_Control':result=clearance
            if line=='msgbox HavoraTrial_CaptainReadyText, MSGBOX_YESNO':
                events.append('prompt');result=1 if ready else 0
            if line.startswith('goto_if_eq VAR_RESULT, '):
                _,value,target=line.split(', ')
                value=0 if value=='NO' else int(value)
                if result==value:label=target;jumped=True;break
            if line.startswith('trainerbattle_double '):events.append('battle');return events
            if line=='releaseall':events.append('release')
            if line=='end':return events
            if line.startswith('goto '):
                label=line[5:];jumped=True
                if label=='HavoraTide_Recovery':events.append('postbattle');return events
                break
        if not jumped:raise AssertionError(('unexpected script flow',label))
    raise AssertionError('script loop')
assert trace(ready=True)==['prompt','battle']
assert trace(ready=False)==['prompt','release']
assert trace(defeated=True)==['postbattle']
for status in [2,3]:assert trace(clearance=status)==['release']
assert 'Your BAG is off limits.' in '\n'.join(blocks['HavoraTrial_CaptainReadyText'])
assert 'Held items are allowed.' in '\n'.join(blocks['HavoraTrial_CaptainReadyText'])
print('PASS actual script flow: Yes starts battle; No releases/exits; completed encounter skips prompt; existing readiness gates retained')
