"""Construct all six real NPC parties and verify exact sets, including randomizer.

An isolated native probe reads engine Pokemon data; no production hooks are added.
"""
import os,pathlib,struct,subprocess,re
import havora_emulator_support as m
s=(m.root/'tests/avatar_wardrobe_emulator.py').read_text();exec(s[s.index('native_dir ='):s.index('avatar_var = native')])
source=(m.root/'src/data/trainers.party').read_text()
def token(s):return s.upper().replace('-','_').replace(' ','_')
def stats(s):return {b:int(a) for a,b in re.findall(r'(\d+) (HP|Atk|Def|SpA|SpD|Spe)',s)}
records=[];teams=[]
for section in source.split('=== ')[1:]:
 name,body=section.split(' ===',1)
 if not name.startswith('TRAINER_HAVORA_'):continue
 mons=[]
 for block in body.strip().split('\n\n')[1:]:
  lines=block.splitlines()
  if not lines:continue
  species,item=lines[0].split(' @ ');attributes=dict(line.split(': ',1) for line in lines[1:] if ': ' in line)
  ev=stats(attributes['EVs']);iv=stats(attributes['IVs'])
  values=['SPECIES_'+token(species),attributes['Level'],'ITEM_'+token(item),'ABILITY_'+token(attributes['Ability']),'NATURE_'+token(attributes['Nature'])]
  order=['HP','Atk','Def','SpA','SpD','Spe']
  values += [str(ev.get(k,0)) for k in order]+[str(iv[k]) for k in order]
  values += ['MOVE_'+token(line[2:]) for line in lines if line.startswith('- ')]
  mons.append(values)
 teams.append((name,len(records),len(mons)));records+=mons
assert [t[2] for t in teams]==[2,3,3,4,4,6]
fields=['SPECIES','LEVEL','HELD_ITEM']+['HP_EV','ATK_EV','DEF_EV','SPATK_EV','SPDEF_EV','SPEED_EV']+['HP_IV','ATK_IV','DEF_IV','SPATK_IV','SPDEF_IV','SPEED_IV']+['MOVE1','MOVE2','MOVE3','MOVE4']
code=m.symbols['gDecompressionBuffer']+0x3000;output=m.symbols['gDecompressionBuffer']+0x2000
get=m.symbols['GetMonData2']|1;ability=m.symbols['GetMonAbility']|1;nature=m.symbols['GetNature']|1;create=m.symbols['CreateNPCTrainerPartyFromTrainer']|1
text='''#include "global.h"
#include "data.h"
#include "pokemon.h"
#include "constants/abilities.h"
#include "constants/items.h"
#include "constants/opponents.h"
#include "constants/species.h"
'''
text+='static const u16 expected[][21] = {\n'+''.join('{'+','.join(v)+'},\n' for v in records)+'};\n'
text+='static const u16 fields[] = {'+','.join('MON_DATA_'+v for v in fields)+'};\n'
text+='static const u16 ids[] = {'+','.join(t[0] for t in teams)+'};\n'
text+='static const u8 offsets[] = {'+','.join(str(t[1]) for t in teams)+'};\n'
text+=f'''u32 __attribute__((section(".text.entry"))) Probe(u32 which)
{{
 struct Pokemon *party=(void *){m.symbols['gEnemyParty']};
 const struct Trainer *trainer=((const struct Trainer **){m.symbols['gTrainers']})[DIFFICULTY_NORMAL]+ids[which];
 u32 (*get)(struct Pokemon*,s32)=(void *){get};
 u16 (*ability)(struct Pokemon*)=(void *){ability};
 u8 (*nature)(struct Pokemon*)=(void *){nature};
 u8 (*create)(struct Pokemon*,const struct Trainer*,bool32,u32,u16)=(void *){create};
 u32 *out=(void *){output},*diag=out+2,errors=0,i,j,count;
 count=create(party,trainer,TRUE,BATTLE_TYPE_TRAINER|BATTLE_TYPE_DOUBLE,ids[which]);
 *out++=count;
 for(i=0;i<count;i++)
 {{
  const u16 *e=expected[offsets[which]+i];
  for(j=0;j<3;j++){{*diag++=get(party+i,fields[j]);if(get(party+i,fields[j])!=e[j])errors++;}}
  *diag++=ability(party+i);*diag++=nature(party+i);
  if(ability(party+i)!=e[3]||nature(party+i)!=e[4])errors++;
  for(j=3;j<19;j++){{*diag++=get(party+i,fields[j]);if(get(party+i,fields[j])!=e[j+2])errors++;}}
  *diag++=get(party+i,MON_DATA_CANT_RANDOMIZE_ABILITY);
  if(get(party+i,MON_DATA_CANT_RANDOMIZE_ABILITY)!=TRUE)errors++;
 }}
 *out=errors;return errors;
}}
'''
# A party entry has 5 identity fields, 12 stat values, and 4 moves.
probe=m.d/'team-data-probe.c';probe.write_text(text)
obj=probe.with_suffix('.o');elf=probe.with_suffix('.elf');binary=probe.with_suffix('.bin');ld=probe.with_suffix('.ld')
ld.write_text('SECTIONS { . = '+hex(code)+'; .text : { *(.text.entry) *(.text*) *(.rodata*) } /DISCARD/ : { *(.ARM.exidx*) *(.ARM.extab*) *(.comment*) } }')
subprocess.run([tool_prefix+'gcc','-mthumb','-mcpu=arm7tdmi','-mabi=apcs-gnu','-Os','-fno-builtin','-iquote',str(m.root/'include'),'-iquote',str(m.root/'gflib'),'-DFIRERED','-c',str(probe),'-o',str(obj)],check=True)
subprocess.run([tool_prefix+'ld','-T',str(ld),'-o',str(elf),str(obj)],check=True)
subprocess.run([tool_prefix+'objcopy','-O','binary',str(elf),str(binary)],check=True)
data=binary.read_bytes();assert len(data)<0xF00,len(data)
# The ordinary native-call shim lives at +0x3000, so put this helper at +0x1000.
# Its linked address must agree; retain the shim and invoke Probe through it.
new_code=m.symbols['gDecompressionBuffer']+0x1000
ld.write_text(ld.read_text().replace(hex(code),hex(new_code)))
subprocess.run([tool_prefix+'ld','-T',str(ld),'-o',str(elf),str(obj)],check=True)
subprocess.run([tool_prefix+'objcopy','-O','binary',str(elf),str(binary)],check=True)
m.write(new_code,binary.read_bytes());m.symbols['HavoraPartyProbe']=new_code
for i,(name,_,count) in enumerate(teams):
 result=native('HavoraPartyProbe',i)
 if result:print('PARTY DIAGNOSTIC',name,result,struct.unpack('<'+'I'*(count*22),m.read(output+8,count*88)),flush=True)
 assert result==0,name
 assert struct.unpack('<II',m.read(output,8))==(count,0)
 print('PASS exact native party:',name,count,'mons; species, level, item, ability, nature, EVs, IVs, moves',flush=True)
native('FlagSet',0xB1);native('FlagSet',0xB5)
m.write(m.symbols['gRandomizerEnabled'],b'\x01')
m.write(m.symbols['gCachedRandomizerSeed'],struct.pack('<I',1234567))
assert native('RandomizerFeatureEnabled',1)==1,'trainer randomization not enabled'
assert native('RandomizerFeatureEnabled',9)==1,'ability randomization not enabled'
for i,(name,_,count) in enumerate(teams):
 assert native('HavoraPartyProbe',i)==0,('randomizer changed curated party',name)
 print('PASS curated species and abilities with randomization enabled:',name,flush=True)
print('PASS all 22 native sets; ability randomization is explicitly disabled on every member',flush=True)
