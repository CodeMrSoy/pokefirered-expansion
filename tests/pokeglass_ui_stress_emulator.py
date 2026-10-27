#!/usr/bin/env python3
"""Stress complete Pokédex records and inspect embedded text against the glass."""
import pathlib,subprocess,struct
setup=pathlib.Path(__file__).with_name('pokeglass_benchmark_emulator.py')
exec(compile(setup.read_text().split('field=save()')[0],str(setup),'exec'))
# Fill seen/caught through the real save API in one native call.
native=m.symbols['gDecompressionBuffer']+0x3000
asm=['.syntax unified','.thumb','.thumb_func','_start:','push {r4,r5,lr}',
     'movs r4,#1','ldr r5,limit','loop:','movs r0,r4','movs r1,#2',
     'ldr r3,function','bl invoke','movs r0,r4','movs r1,#3','ldr r3,function','bl invoke',
     'adds r4,#1','cmp r4,r5','ble loop','movs r0,#1','pop {r4,r5,pc}',
     'invoke:','bx r3','.align 2',f'function: .word {m.symbols["GetSetPokedexFlag"]|1}',
     'limit: .word 1025']
(out/'fill.s').write_text('\n'.join(asm)+'\n')
prefix=__import__('os').environ.get('ARM_NM','arm-none-eabi-nm').removesuffix('nm')
subprocess.run([prefix+'as','-mthumb','-mcpu=arm7tdmi','-o',str(out/'fill.o'),str(out/'fill.s')],check=True)
subprocess.run([prefix+'objcopy','-O','binary','-j','.text',str(out/'fill.o'),str(out/'fill.bin')],check=True)
m.write(native,(out/'fill.bin').read_bytes());m.inject(b'\x23'+struct.pack('<I',native|1)+b'\x02')
def within_glass(label):
 wid=byte('sHubWindow');p=struct.unpack('<I',m.read(m.symbols['gWindows']+wid*12+8,4))[0]
 raw=np.frombuffer(m.read(p,28*18*32),dtype=np.uint8)
 yy,xx=np.mgrid[:144,:224];offset=((yy//8)*28+xx//8)*32+(yy%8)*4+(xx%8)//2
 pixels=(raw[offset]>>((xx%2)*4))&15
 outside=(xx<13)|(xx>=212)|(yy<15)|(yy>=128)
 bad=np.argwhere((pixels==8)&outside)
 m.snap('ui-stress-'+label)
 if len(bad):print('BORDER',label,bad[:12].tolist(),len(bad),flush=True)
 return len(bad)
trace('full-dex-tablet-open',3,hub)
ref=np.asarray(m.screen).copy()
trace('full-dex-open',8,lambda:ready('Task_PokeGlassPokedex'),True,ref)
issues=within_glass('full-dex-list')
# Sorting/filtering must produce a new visible header, not just change RAM flags.
for label,key,region in [('full-dex-sort',2,(16,29,44,39)),('full-dex-filter',3,(70,29,115,39))]:
 x0,y0,x1,y1=region;before=m.screen.crop((x0+8,y0+8,x1+8,y1+8)).tobytes()
 trace(label,key,lambda: m.screen.crop((x0+8,y0+8,x1+8,y1+8)).tobytes()!=before)
 issues+=within_glass(label)
 m.run(15)
before=m.screen.crop((25,40,100,100)).tobytes()
trace('full-dex-entry',8,lambda: m.screen.crop((25,40,100,100)).tobytes()!=before)
m.run(120);issues+=within_glass('full-dex-entry')
m.press(8,120);issues+=within_glass('full-dex-habitat')
m.press(0);m.press(0);m.press(0)
assert hub()
# Capture all party members and repeated Stats visits with their actual labels.
m.press(5,30);m.press(7,30);assert byte('sHubCursor')==3
trace('stats-stress-open',8,lambda:ready('Task_PokeGlassStats'),True,ref)
for i in range(12):
 issues+=within_glass('stats-'+str(i))
 m.press(7,30)
m.press(0);assert hub();m.press(0)
assert byte('sGlobalScriptContextStatus')==2 and byte('sLockFieldControls')==0
print('TEXT BORDER PIXELS',issues,flush=True)
assert issues == 0, ('Text extends beyond glass', issues)
(out/'stress-timings.json').write_text(json.dumps(results,indent=2)+'\n')
print('PASS full seen/caught records, sorting/filtering, entry/habitat, Stats cycling, field exit',flush=True)
