#!/usr/bin/env python3
"""Generate an actual pre-cleanup Flash save, then load it in the cleaned ROM.
Run once with --create using the baseline ELF/ROM, then normally for the release.
"""
from pathlib import Path
import sys,types,struct,ctypes as c,re
h=Path(__file__).with_name('quantum_qol_emulator.py').resolve();source=h.read_text()
create='--create' in sys.argv
if create:
 source=source.replace("rom=(root/'pokefirered.gba').read_bytes()","rom=(root/'build/cleanup-baseline/pokefirered.gba').read_bytes()").replace("str(root/'pokefirered.elf')","str(root/'build/cleanup-baseline/pokefirered.elf')")
else:source=source.split('run(360);press(3)')[0]
m=types.ModuleType('oldsave_harness');m.__file__=str(h);exec(compile(source,str(h),'exec'),m.__dict__)
helpers=Path(__file__).with_name('rom_cleanup_migration_emulator.py').read_text().split('old=(m.root')[0]
helpers=helpers.replace('import quantum_qol_emulator as m','')
exec(compile(helpers,'migration_helpers','exec'))
fixture=m.root/'build/cleanup-baseline/old-world-save.sav'
m.lib.retro_get_memory_data.argtypes=[c.c_uint];m.lib.retro_get_memory_data.restype=c.c_void_p
m.lib.retro_get_memory_size.argtypes=[c.c_uint];m.lib.retro_get_memory_size.restype=c.c_size_t
if create:
 party=(m.root/'tests/fixtures/rom_cleanup_old_form_party.bin').read_bytes();m.write(m.symbols['gPlayerParty'],party);m.write(m.symbols['gPlayerPartyCount'],b'\x06')
 box=ptr('gPokemonStoragePtr');m.write(box+4,party[:80]);fusion=(box+4+14*30*80+14*9+14+3)&~3;m.write(fusion,party[100:200])
 native('AddPCItem',13,3)
 save=ptr('gSaveBlock1Ptr')
 for offset in (4,12,20,28,36):m.write(save+offset,struct.pack('<bbb x hh',3,12,-1,10,9))
 m.write(save,struct.pack('<hh',10,9))
 layout=int(re.search(r'#define LAYOUT_ONE_ISLAND\s+(\d+)',(m.root/'include/constants/layouts.h').read_text())[1]);m.write(save+0x32,struct.pack('<H',layout))
 assert native('TrySavingData',0)==1
 fixture.write_bytes(c.string_at(m.lib.retro_get_memory_data(0),m.lib.retro_get_memory_size(0)))
 print('Baseline Flash fixture saved with retired forms, fusion partner, PC items and One Island location')
else:
 raw=fixture.read_bytes();assert len(raw)==m.lib.retro_get_memory_size(0);c.memmove(m.lib.retro_get_memory_data(0),raw,len(raw))
 m.run(360);m.press(3);m.press(8);m.press(8);m.run(300)
 save=ptr('gSaveBlock1Ptr');assert m.read(save+4,2)==bytes((3,0)),'Old save did not relocate to Pallet'
 assert struct.unpack('<hh',m.read(save,4))==(10,9)
 assert m.read(m.symbols['gPlayerPartyCount'],1)==b'\x06'
 for i,n in enumerate(('CHARIZARD','NECROZMA','CALYREX','PIKACHU','FURFROU_NATURAL','UNOWN')):
  assert native('GetMonData3',m.symbols['gPlayerParty']+i*100,18,0)==species('SPECIES_'+n)
 m.snap('cleanup-actual-old-save-continue')
 native('QuantumRecoverStoredItemsAndPokemon');box=ptr('gPokemonStoragePtr')
 assert native('GetBoxMonData3',box+4+80,18,0)==species('SPECIES_NECROZMA')
 assert native('CountTotalItemQuantityInBag',13)==3
 m.press(3);m.snap('cleanup-actual-old-save-controls');m.press(0)
 print('Actual pre-cleanup Flash save loaded: Pallet relocation, canonical forms, hidden partner/items recovery and field menu controls passed')
