"""Real seeded encounters, assigned abilities, type badges and arrival-gated maps."""
import pathlib, struct, re, subprocess
import numpy as np
setup = pathlib.Path(__file__).with_name('avatar_wardrobe_emulator.py')
exec(compile(setup.read_text().split("fixture = b'\\x23'")[0], str(setup), 'exec'))
m.d = m.d / 'dex-randomized-habitat'
m.d.mkdir(exist_ok=True)
native('FlagSet', 0x829)
native('AddBagItem', 717, 1)

def ptr(name): return struct.unpack('<I', m.read(m.symbols[name], 4))[0]
def enum_count(file, prefix, last):
    source=(m.root/file).read_text(encoding='utf-8').split('enum',1)[1].split('}',1)[0]
    return re.findall(r'\b'+prefix+r'[A-Z0-9_]+\b',source).index(last)
count=enum_count('include/constants/pokedex.h','NATIONAL_DEX_','NATIONAL_DEX_PECHARUNT')
areas=enum_count('include/constants/region_map_sections.h','MAPSEC_','MAPSEC_COUNT')
class Dex(c.Structure):
    _fields_=[('species',c.c_uint16*count),('areas',c.c_uint16*areas),
              ('count',c.c_uint16),('cursor',c.c_uint16),('seen',c.c_uint16),('caught',c.c_uint16),
              ('sprite',c.c_uint16),('areaCount',c.c_uint16),('areaPage',c.c_uint8),
              ('view',c.c_uint8),('filter',c.c_uint8),('alphabetical',c.c_uint8),
              ('speciesByDex',c.c_uint16*(count+1)),('typeWindows',c.c_uint8*2),
              ('areaSpecies',c.c_uint16),('areaHeader',c.c_uint16),('areaLoading',c.c_uint8)]
def dex(): return Dex.from_buffer_copy(m.read(ptr('sGlassDex'),c.sizeof(Dex)))

# A tiny ABI adapter supplies the fifth argument on the stack, just as gameplay
# does, while the existing native helper supplies species/map/method in r0-r3.
adapter=m.symbols['gDecompressionBuffer']+0x2000
assembly=['.syntax unified','.thumb','.thumb_func','entry:','push {r4,lr}',
          'sub sp,#8','movs r4,#0','str r4,[sp]','ldr r4,function','bl invoke',
          'add sp,#8','pop {r4,pc}','invoke:','bx r4','.align 2',
          f"function: .word {m.symbols['RandomizeWildEncounter']|1}"]
(native_dir/'wild.s').write_text('\n'.join(assembly)+'\n')
subprocess.run([tool_prefix+'as','-mthumb','-mcpu=arm7tdmi','-o',str(native_dir/'wild.o'),str(native_dir/'wild.s')],check=True)
subprocess.run([tool_prefix+'objcopy','-O','binary','-j','.text',str(native_dir/'wild.o'),str(native_dir/'wild.bin')],check=True)
m.write(adapter,(native_dir/'wild.bin').read_bytes())
m.symbols['TestWildSlotZero']=adapter

# One actual table per encounter method, using the compiled header layout.
samples={}
for index in range(1000):
    h=m.symbols['gWildMonHeaders']+index*84
    group,num=m.read(h,2)
    if group==255: break
    for time in range(4):
        for method in range(5):
            info=struct.unpack('<I',m.read(h+4+time*20+method*4,4))[0]
            if not info or method in samples: continue
            mons=struct.unpack('<I',m.read(info+4,4))[0]
            species=struct.unpack('<H',m.read(mons+2,2))[0]
            samples[method]=(species,num,group)
assert set(range(4)).issubset(samples),samples
n=m.lib.retro_serialize_size();baseline=c.create_string_buffer(n);assert m.lib.retro_serialize(baseline,n)
text_adapter=adapter+0x100
params=adapter+0x200
colors=params+0x20
assembly=['.syntax unified','.thumb','.thumb_func','entry:','push {r4-r6,lr}',
          'sub sp,#16','ldr r4,params','ldr r5,[r4]','str r5,[sp]',
          'ldr r5,[r4,#4]','str r5,[sp,#4]','ldr r5,[r4,#8]','str r5,[sp,#8]',
          'ldr r4,function','bl invoke','add sp,#16','pop {r4-r6,pc}',
          'invoke:','bx r4','.align 2',f'params: .word {params}',
          f"function: .word {m.symbols['AddTextPrinterParameterized3']|1}"]
(native_dir/'text.s').write_text('\n'.join(assembly)+'\n')
subprocess.run([tool_prefix+'as','-mthumb','-mcpu=arm7tdmi','-o',str(native_dir/'text.o'),str(native_dir/'text.s')],check=True)
subprocess.run([tool_prefix+'objcopy','-O','binary','-j','.text',str(native_dir/'text.o'),str(native_dir/'text.bin')],check=True)
text_code=(native_dir/'text.bin').read_bytes()
m.symbols['TestPrintText']=text_adapter

for seed in (0x12345678,0x5eed1234):
    assert m.lib.retro_unserialize(baseline,n)
    m.write(text_adapter,text_code);m.write(colors,bytes([0,8,4]))
    m.write(m.symbols['gCachedRandomizerSeed'],struct.pack('<I',seed));native('RandomizerSetEnabled',1)
    expected={}
    for method,(original,num,group) in samples.items():
        species=native('TestWildSlotZero',original,num,group,method)
        national=native('SpeciesToNationalPokedexNum',species)
        header=native('Overworld_GetMapHeaderByGroupAndId',group,num)
        expected.setdefault(national,set()).add(m.read(header+20,1)[0])
        native('GetSetPokedexFlag',national,3)
    species_to_dex={}
    reference={}
    for national in expected:
        species=native('NationalPokedexNumToSpecies',national)
        species_to_dex[species]=national
        ability=native('GetSpeciesAbilityWithRandomizerCheck',species,0,0)
        template=params+0x40
        m.write(template,struct.pack('<6BH',0,0,0,22,2,13,0x300))
        temp=native('AddWindow',template)
        assert temp<32
        native('FillWindowPixelBuffer',temp,0)
        m.write(params,struct.pack('<III',colors,255,m.symbols['gAbilitiesInfo']+ability*28))
        native('TestPrintText',temp,0,0,0)
        w=m.read(m.symbols['gWindows']+temp*12,12)
        raw=m.read(struct.unpack_from('<I',w,8)[0],22*2*32)
        reference[national]=np.array([[((raw[(y//8*22+x//8)*32+y%8*4+x%8//2]>>((x&1)*4))&15)==8
                                      for x in range(166)] for y in range(12)])
        assert reference[national].sum()>5
        native('RemoveWindow',temp)
    m.press(3);wait_task('Task_PokeGlassHub');m.press(8);wait_task('Task_PokeGlassPokedex')
    m.press(7,20);assert dex().filter==1
    m.press(6,20);assert dex().filter==0
    for entry in range(dex().count):
        state=dex();species=state.species[state.cursor]
        national=species_to_dex[species]
        m.press(8,10);assert dex().view==1
        rendered=np.asarray(m.screen)[102:114,58:224]
        foreground=(rendered[:,:,0]>130)&(rendered[:,:,1]>170)&(rendered[:,:,2]>170)
        assert np.array_equal(foreground,reference[national]),('Assigned ability glyphs differ',hex(seed),species)
        badges=[]
        for w in range(32):
            data=m.read(m.symbols['gWindows']+w*12,12)
            if data[0]==0 and data[5]==14 and struct.unpack_from('<I',data,8)[0]:badges.append(data)
        assert len(badges) in (1,2) and all(b[3:5]==b'\x04\x02' for b in badges)
        native_palette=m.read(m.symbols['gMenuInfoElements2_Pal'],32)
        palette=m.read(m.symbols['gPlttBufferUnfaded']+14*32,32)
        assert palette[:20]==native_palette[:20] and palette[22:]==native_palette[22:]
        assert palette[20:22]==struct.pack('<H',(6<<5)|(11<<10))
        for badge in badges:
            raw=m.read(struct.unpack_from('<I',badge,8)[0],4*2*32)
            assert all((pixel&15) and (pixel>>4) for pixel in raw),'Badge exposes raw overworld pixels'
        if entry==0:m.snap('assigned-ability-types-'+hex(seed))
        if entry==0:
            progress=dex().areaHeader
            m.press(0,10);assert dex().view==0,'Background scan blocked B'
            m.press(8,10);assert dex().view==1 and dex().areaHeader>=progress
        m.press(8,10);assert dex().view==2,'Background scan blocked A'
        for wait in range(1500):
            if not dex().areaLoading:break
            m.run(1)
        else:raise AssertionError('Habitat scan did not complete')
        # areaLoading changes before the final page's text and DMA finish.
        m.run(20)
        assert expected[national].issubset(set(dex().areas[:dex().areaCount])),(seed,national,list(dex().areas[:dex().areaCount]),expected[national])
        if entry==0:m.snap('actual-randomized-habitats-'+hex(seed))
        m.press(8);assert dex().view==1
        m.press(0);assert dex().view==0
        m.press(5,20)
    m.press(0);m.press(0)
    assert ptr('sGlassDex')==0
    print('PASS',len(samples),'actual encounter methods, assigned ability pixels, native type palettes, A page toggle and cleanup for seed',hex(seed),flush=True)

# Arrival locking applies to both Town Map and the native Fly picker.
type_offset=19*2+5*600*2+3*0x800*2
native('FlagClear',0x4e1)
for kind in (0,2):
    if kind==0:native('InitRegionMapWithExitCB',0,m.symbols['CB2_ReturnToField']|1)
    else:native('CB2_OpenFlyMapWithExitCB',m.symbols['CB2_ReturnToField']|1)
    m.run(240)
    assert m.read(ptr('sRegionMap')+type_offset+1,1)==b'\0','Vidra visible before arrival'
    m.press(0,300)
native('FlagSet',0x4e1)
for kind in (0,2):
    if kind==0:native('InitRegionMapWithExitCB',0,m.symbols['CB2_ReturnToField']|1)
    else:native('CB2_OpenFlyMapWithExitCB',m.symbols['CB2_ReturnToField']|1)
    m.run(240)
    assert m.read(ptr('sRegionMap')+type_offset+1,1)==b'\x01','Visited Vidra still locked'
    m.press(0,300)
print('PASS Town Map and Fly: Vidra hidden before arrival, available after arrival',flush=True)
