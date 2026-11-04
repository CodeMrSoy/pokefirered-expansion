#!/usr/bin/env python3
"""Exercise real Gym TM scripts and generated leader parties in an mGBA ROM."""
import pathlib, re, struct
setup = pathlib.Path(__file__).with_name('avatar_wardrobe_emulator.py')
exec(compile(setup.read_text().split("fixture = b'\\x23'")[0], str(setup), 'exec'))

# Native assertions do not need the UI harness's fixed 180-frame settling wait.
# Run until the injected script actually finishes instead.
base_native=native
def native(name,*args):
    original_inject=m.inject
    def inject_until_done(blob):
        address=m.symbols['gDecompressionBuffer']
        m.write(address,blob)
        context=m.symbols['sGlobalScriptContext']
        m.write(context,b'\x00\x01\x00\x00')
        m.write(context+8,struct.pack('<I',address))
        m.write(m.symbols['sGlobalScriptContextStatus'],b'\x00')
        for _ in range(180):
            m.run(1)
            if m.read(m.symbols['sGlobalScriptContextStatus'],1)==b'\x02': return
        raise AssertionError('Native helper script did not finish: '+name)
    m.inject=inject_until_done
    try: return base_native(name,*args)
    finally: m.inject=original_inject

def constant(name, header):
    value = subprocess.check_output([tool_prefix+'cpp','-P','-I',str(m.root/'include'),'-'],
        input=f'#include "constants/{header}"\n{name}\n',text=True)
    expression=value.strip().splitlines()[-1]
    if expression==name:
        # A C enum is not expanded by cpp (Pocket uses one).
        cfile=native_dir/'constant.c'; binary=native_dir/'constant'
        cfile.write_text(f'#include <stdio.h>\n#include "constants/{header}"\nint main(void){{printf("%u",(unsigned){name});}}\n')
        subprocess.run(['cc','-I',str(m.root/'include'),str(cfile),'-o',str(binary)],check=True)
        return int(subprocess.check_output([str(binary)],text=True))
    return eval(expression, {'__builtins__':{}}, {})

rows=[('PewterCity',39,'BROCK'),('CeruleanCity',3,'MISTY'),
      ('VermilionCity',34,'LT_SURGE'),('CeladonCity',19,'ERIKA'),
      ('FuchsiaCity',6,'KOGA'),('SaffronCity',4,'SABRINA'),
      ('CinnabarIsland',38,'BLAINE'),('ViridianCity',26,'GIOVANNI')]
rows=[(town,constant(f'ITEM_TM{tm:02}','items.h'),constant('TRAINER_LEADER_'+leader,'opponents.h')) for town,tm,leader in rows]

def set_seed(seed):
    native('RandomizerSetEnabled',0)
    m.write(m.symbols['gCachedRandomizerSeed'],struct.pack('<I',seed))
    native('RandomizerSetEnabled',1)

def reward(item,leader):
    m.write(m.symbols['gSpecialVar_0x8008'],struct.pack('<H',item))
    m.write(m.symbols['gSpecialVar_0x8009'],struct.pack('<H',leader))
    native('RandomizeGymTM_NativeCall',0)
    return struct.unpack('<H',m.read(m.symbols['gSpecialVar_0x8008'],2))[0]

def finish_dialogue():
    for _ in range(50):
        if m.read(m.symbols['sGlobalScriptContextStatus'],1)==b'\x02':
            return
        m.press(8,30)
    raise AssertionError('Gym reward script did not finish')

def run_script(label):
    m.inject(b'\x04'+struct.pack('<I',m.symbols[label])+b'\x02')
    finish_dialogue()

# Stable, different TM-only rewards for every leader over several seeds.
minimum=constant('ITEM_TM01','items.h'); maximum=constant('ITEM_TM50','items.h')
for seed in (12345,7654321,0x12345678):
    set_seed(seed)
    for town,item,leader in rows:
        actual=reward(item,leader)
        assert minimum<=actual<=maximum and actual!=item,(town,item,actual)
        assert reward(item,leader)==actual
        native('FlagClear',0x0b0)
        assert reward(item,leader)==item
        native('FlagSet',0x0b0)
print('PASS all eight Gym rewards: deterministic TM-only substitutions, original excluded, feature off',flush=True)

set_seed(12345)
native('AddBagItem',constant('ITEM_TM_CASE','items.h'),1)
# Restore the same bag and story flags before each real reward script.
size=m.lib.retro_serialize_size(); baseline=m.c.create_string_buffer(size)
assert m.lib.retro_serialize(baseline,size)
for town,item,leader in rows:
    assert m.lib.retro_unserialize(baseline,size)
    number=item-minimum+1
    label=f'{town}_Gym_EventScript_GiveTM{number:02}'
    expected=reward(item,leader)
    run_script(label)
    assert native('CheckBagHasItem',expected,1),(town,expected)
    leadername=next(name for name in ['BROCK','MISTY','LT_SURGE','ERIKA','KOGA','SABRINA','BLAINE','GIOVANNI'] if constant('TRAINER_LEADER_'+name,'opponents.h')==leader)
    flagname='SURGE' if leadername=='LT_SURGE' else leadername
    flag=constant(f'FLAG_GOT_TM{number:02}_FROM_{flagname}','flags.h')
    assert native('FlagGet',flag),(town,'reward flag missing')
    # Talk again through the leader's actual defeated-trainer path.
    native('SetTrainerFlag',leader)
    quantity=native('CountTotalItemQuantityInBag',expected)
    objectname={'LT_SURGE':'LtSurge','GIOVANNI':'Giovanni'}.get(leadername,leadername.title())
    run_script(f'{town}_Gym_EventScript_{objectname}')
    assert native('CountTotalItemQuantityInBag',expected)==quantity,'Duplicate reward'
    print('PASS real gift script:',town,'TM',expected-minimum+1,flush=True)

# Full TM pocket must leave Brock's reward flag clear, then retry the same TM.
assert m.lib.retro_unserialize(baseline,size)
flag=constant('FLAG_GOT_TM39_FROM_BROCK','flags.h')
expected=reward(rows[0][1],rows[0][2])
pocket=constant('POCKET_TM_HM','item.h')
capacity_addr=m.symbols['gBagPockets']+pocket*8+4
capacity=m.read(capacity_addr,1)
m.write(capacity_addr,b'\0')
run_script('PewterCity_Gym_EventScript_GiveTM39')
assert not native('FlagGet',flag)
assert not native('CheckBagHasItem',expected,1)
m.write(capacity_addr,capacity)
assert reward(rows[0][1],rows[0][2])==expected
run_script('PewterCity_Gym_EventScript_GiveTM39')
assert native('FlagGet',flag) and native('CheckBagHasItem',expected,1)
print('PASS full-Bag retry preserves the randomized TM and reward flag',flush=True)

# Read the real MON_DATA enum rather than hard-coding an old engine layout.
enum=(m.root/'include/pokemon.h').read_text().split('enum {',1)[1].split('};',1)[0]
fields={name:i for i,name in enumerate(re.findall(r'\bMON_DATA_\w+',enum))}
def mon_data(mon,name): return native('GetMonData3',mon,fields[name],0)

# The convenience script wrapper is link-time stripped in release builds.
# Call the retained production party constructor with its fifth stack argument.
trainer_count=constant('TRAINERS_COUNT','opponents.h')
table0,table1=struct.unpack('<II',m.read(m.symbols['gTrainers'],8))
trainer_size=(table1-table0)//trainer_count
assert trainer_size>0 and (table1-table0)%trainer_count==0
def create_party(leader):
    difficulty=native('GetTrainerDifficultyLevel',leader)
    table=struct.unpack('<I',m.read(m.symbols['gTrainers']+difficulty*4,4))[0]
    m.write(m.symbols['gPlayerParty'],bytes(600))
    flags=constant('BATTLE_TYPE_TRAINER','battle.h')
    assembly=['.syntax unified','.thumb','.thumb_func','_start:',
        'push {r4, lr}','sub sp, #8','ldr r4, trainerid','str r4, [sp]',
        'ldr r0, party','ldr r1, trainer','movs r2, #1','ldr r3, flags',
        'ldr r4, function','bl invoke','ldr r3, result','str r0, [r3]',
        'movs r0, #1','add sp, #8','pop {r4, pc}','invoke:','bx r4','.align 2',
        f'trainerid: .word {leader}',f'party: .word {m.symbols["gPlayerParty"]}',
        f'trainer: .word {table+leader*trainer_size}',f'flags: .word {flags}',
        f'function: .word {m.symbols["CreateNPCTrainerPartyFromTrainer"]|1}',
        f'result: .word {result_addr}']
    (native_dir/'party.s').write_text('\n'.join(assembly)+'\n')
    subprocess.run([tool_prefix+'as','-mthumb','-mcpu=arm7tdmi','-o',str(native_dir/'party.o'),str(native_dir/'party.s')],check=True)
    subprocess.run([tool_prefix+'objcopy','-O','binary','-j','.text',str(native_dir/'party.o'),str(native_dir/'party.bin')],check=True)
    m.write(native_addr,(native_dir/'party.bin').read_bytes())
    m.inject(b'\x23'+struct.pack('<I',native_addr|1)+b'\x6b\x02')

# Test species+learnsets, species-only and learnsets-only. Initial moves must
# survive the custom trainer party path in all three combinations.
for trainer_flag,learnset_flag in ((True,True),(True,False),(False,True)):
    assert m.lib.retro_unserialize(baseline,size)
    native('FlagSet' if trainer_flag else 'FlagClear',0x0b1)
    native('FlagSet' if learnset_flag else 'FlagClear',0x0b6)
    battle=native('AllocZeroed_',16384,0)
    assert battle
    m.write(m.symbols['gBattleStruct'],struct.pack('<I',battle))
    leaders=[row[2] for row in rows]+[constant('TRAINER_HAVORA_HARBORMASTER','opponents.h')]
    for leader in leaders:
        m.write(m.symbols['gSpecialVar_0x8004'],struct.pack('<H',leader))
        create_party(leader)
        count=0
        for slot in range(6):
            mon=m.symbols['gPlayerParty']+slot*100
            if not mon_data(mon,'MON_DATA_SPECIES'): break
            before=m.read(mon,100)
            native('GiveBoxMonInitialMoveset',mon)
            assert m.read(mon,100)==before,(leader,slot,'authored moves overwrote current learnset')
            count+=1
        assert count
    print('PASS all nine leaders use current species learnsets:',trainer_flag,learnset_flag,flush=True)

# Fixed Havora crews keep their authored strategies under all feature states.
for leader in range(constant('TRAINER_HAVORA_DOCK_CREW','opponents.h'),constant('TRAINER_HAVORA_FIRST_MATE','opponents.h')+1):
    assert not native('RandomizerTrainerUsesLearnset',leader)
native('FlagClear',0x0b1);native('FlagClear',0x0b6)
assert not native('RandomizerTrainerUsesLearnset',rows[0][2])
print('PASS fixed Havora crews and non-randomized trainer policy',flush=True)
