"""Verify actual prior-ROM Flash images without publishing save fixtures.

QUEST_LEGACY_SAVES is an os.pathsep-separated list of private local .sav files.
"""
import ctypes as c, os, pathlib, struct, types
root=pathlib.Path(__file__).resolve().parents[1]
p=root/'tests/quantum_qol_emulator.py'
m=types.ModuleType('quest_legacy_harness');m.__file__=str(p)
exec(compile(p.read_text().split("run(360);press(3);press(8);snap('boot')")[0],str(p),'exec'),m.__dict__)
m.lib.retro_get_memory_data.argtypes=[c.c_uint];m.lib.retro_get_memory_data.restype=c.c_void_p
m.lib.retro_get_memory_size.argtypes=[c.c_uint];m.lib.retro_get_memory_size.restype=c.c_size_t
paths=os.environ.get('QUEST_LEGACY_SAVES','').split(os.pathsep)
assert paths and paths[0], 'Provide genuine prior-ROM Flash saves via QUEST_LEGACY_SAVES'
for index,path in enumerate(paths):
 flash=pathlib.Path(path).read_bytes()
 assert len(flash)==m.lib.retro_get_memory_size(0)
 sectors=[flash[i:i+4096] for i in range(0,len(flash),4096)]
 old=max((b for b in sectors if struct.unpack_from('<H',b,4084)[0]==0 and struct.unpack_from('<I',b,4088)[0]==0x08012025),key=lambda b:struct.unpack_from('<I',b,4092)[0])
 assert old[3803:3947]==bytes(144), 'Fixture must predate Quest Book'
 c.memmove(m.lib.retro_get_memory_data(0),flash,len(flash));m.lib.retro_reset();m.run(360);m.press(3)
 save=struct.unpack('<I',m.read(m.symbols['gSaveBlock2Ptr'],4))[0]
 assert m.read(save+3803,5)==b'QST3\x01'
 assert m.read(save,14)==old[:14], 'Name, character or trainer ID changed'
 expected_settings=bytearray(old[3756:3795])
 if not expected_settings[5]:
  # Existing pre-V3 migration enables caps on the original reserved bytes.
  expected_settings[5]=0x71;expected_settings[6]=8 | (0x27 if struct.unpack_from('<I',old,3756)[0] else 0)
  expected_settings[7:]=bytes(32)
 assert m.read(save+3756,39)==expected_settings, 'Quest migration changed existing gameplay settings'
 expected=old[3795:3803] if old[3795:3800]==b'QADV\x01' else b'QADV\x01\x01\xfe\xa7'
 assert m.read(save+3795,8)==expected
 assert m.read(save+3947,21)==old[3947:3968]
 m.press(8);m.run(240);m.snap('quest-legacy-continue-'+str(index))
 assert m.read(m.symbols['sLockFieldControls'],1)==b'\0'
 print('PASS prior-ROM Flash save',index,'preserves identity, adventure, existing settings migration and remaining padding',flush=True)
