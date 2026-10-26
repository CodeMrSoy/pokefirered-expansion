"""Native Trainer Card page navigation and legacy/new crest rewards in mGBA."""
import os,pathlib,struct,subprocess
import havora_emulator_support as m
source=(m.root/'tests/avatar_wardrobe_emulator.py').read_text()
exec(source[source.index('native_dir ='):source.index('avatar_var = native')])
def setvar(v,n):native('VarSet',v,n)
def state():
    ptr=struct.unpack('<I',m.read(m.symbols['sTrainerCardDataPtr'],4))[0]
    return m.read(ptr,1)[0] if ptr else None
def open_card():
    native('ShowPlayerTrainerCard',m.symbols['CB2_ReturnToFieldContinueScriptPlayMapMusic']|1)
    m.run(180);assert state()==10,('open',state())
setvar(0x40d7,0);setvar(0x40d8,0);setvar(0x40d9,0)
assert native('TrainerCard_GetVidraCrests')==0
setvar(0x40d8,4)
assert native('TrainerCard_GetVidraCrests')==1,'legacy captain victory lost'
setvar(0x40d8,0);setvar(0x40d9,0xfffe)
assert native('TrainerCard_GetVidraCrests')==30,'mask escaped its five bits'
setvar(0x40d9,0)
open_card();m.snap('vidra-card-kanto');front=m.screen.copy()
palette_addr=m.symbols['gPlttBufferUnfaded']+15*32
front_palette=m.read(palette_addr,32)
m.press(8);assert state()==17;m.snap('vidra-card-locked')
locked=m.screen.copy()
m.press(6);assert state()==10,'left did not restore Kanto'
assert m.read(palette_addr,32)==front_palette,'crest palette leaked onto Kanto card'
assert front.crop((144,32,230,152)).tobytes()==m.screen.crop((144,32,230,152)).tobytes(),'portrait/badge region changed on restore'
m.press(7);assert state()==17,'right did not open Vidra'
m.press(8);assert state()==11,('original statistics inaccessible',state())
assert m.read(palette_addr,32)==front_palette,'crest palette leaked onto statistics'
m.snap('vidra-card-stats')
m.press(0);assert state()==10,'stats B did not return to front'
m.press(0);m.run(120);assert state() is None,'card did not free its allocation'
setvar(0x40d8,7);setvar(0x40d9,0)
open_card();m.press(8);assert state()==17;m.snap('vidra-card-earned')
assert locked.crop((24,60,52,84)).tobytes()!=m.screen.crop((24,60,52,84)).tobytes(),'earned crest did not change color'
m.press(0);assert state()==10;m.press(0);m.run(120)
assert state() is None
print('PASS empty and legacy Harbor reward, five-bit masking, Kanto/Vidra/stats navigation, earned icon, close and reopen')
