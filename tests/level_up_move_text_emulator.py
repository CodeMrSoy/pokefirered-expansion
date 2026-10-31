#!/usr/bin/env python3
"""Real Rare Candy learning, five-row text, long names and cancellation."""
import pathlib,sys,struct,os,subprocess,re
root=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(root/'tests'))
import quantum_qol_emulator as m
# Reuse the task-safe native caller used for the existing Rare Candy regression.
s=(root/'tests/pokeglass_party_text_emulator.py').read_text()
exec(compile(s[s.index('root=m.root;'):s.index('original_first=')],'level-up-helpers','exec'))
def task_active(name):
    expected=m.symbols[name]|1
    return any(m.read(m.symbols['gTasks']+i*40+4,1)!=b'\0' and struct.unpack('<I',m.read(m.symbols['gTasks']+i*40,4))[0]==expected for i in range(16))
def wait(name):
    for _ in range(1200):
        if task_active(name):return
        m.run(1)
    m.snap('level-up-description-debug')
    rev={v|1:k for k,v in m.symbols.items()}
    print([(i,rev.get(struct.unpack('<I',m.read(m.symbols['gTasks']+40*i,4))[0]),m.read(m.symbols['gTasks']+40*i+8,32).hex()) for i in range(16) if m.read(m.symbols['gTasks']+40*i+4,1)!=b'\0'],flush=True)
    raise AssertionError('Did not reach '+name)
fixture=b''
for species,level in [(54,14),(179,10)]:
 fixture+=b'\x23'+struct.pack('<I',(m.symbols['ScrCmd_createmon']|1)+0x2000000)+struct.pack('<BBHHI',0,6,species,level,0)
fixture+=b'\x29'+struct.pack('<H',0x820)+b'\x44'+struct.pack('<HH',102,5)
fixture+=b'\x29'+struct.pack('<H',0x829)+b'\x44'+struct.pack('<HH',717,1)+b'\x02'
m.inject(fixture)
size=m.lib.retro_serialize_size();state=m.c.create_string_buffer(size);assert m.lib.retro_serialize(state,size)
for slot,newmove in [(0,50),(1,178)]:
 assert m.lib.retro_unserialize(state,size)
 script=b''.join(b'\x7a'+struct.pack('<BBH',slot,i,move) for i,move in enumerate([63,344,751,867]))
 m.inject(script+b'\x02');m.press(3);m.press(7);m.press(8);wait('Task_HandleChooseMonInput')
 if slot:m.press(7)
 m.write(m.symbols['gSpecialVar_ItemId'],struct.pack('<H',102))
 tasks=m.read(m.symbols['gTasks'],640)
 task=next(i for i in range(16) if tasks[i*40+4] and struct.unpack_from('<I',tasks,i*40)[0]==(m.symbols['Task_HandleChooseMonInput']|1))
 native('ItemUseCB_RareCandy',task,m.symbols['Task_ClosePartyMenuAfterText']|1)
 for _ in range(35):
  if task_active('Task_InputHandler_SelectOrForgetMove'):break
  m.press(8,120)
 wait('Task_InputHandler_SelectOrForgetMove');m.run(90)
 assert struct.unpack('<H',m.read(m.symbols['sMoveSelectionCursorPos'],1)+b'\0')[0]==0
 summary=struct.unpack('<I',m.read(m.symbols['sMonSummaryScreen'],4))[0]
 expected_moves=struct.pack('<5H',63,344,751,867,newmove)
 assert expected_moves in m.read(summary,0x3800), 'Learning screen lost the existing or new move IDs'
 # The longest Z-move name must be bounded and explicitly abbreviated.
 nameptr=struct.unpack('<I',m.rom[m.symbols['gMovesInfo']-0x8000000+867*48:m.symbols['gMovesInfo']-0x8000000+867*48+4])[0]-0x8000000
 full=m.rom[nameptr:m.rom.index(b'\xff',nameptr)]
 display=full[:15]+b'\xb0\xff'
 assert display in m.read(summary,0x3800), 'Extra-long name was not safely bounded'
 for expected in range(5):
  assert m.read(m.symbols['sMoveSelectionCursorPos'],1)==bytes([expected])
  m.snap(f'level-up-{newmove}-slot-{expected}')
  if expected<4:m.press(5)
 m.press(0)
 assert not task_active('Task_InputHandler_SelectOrForgetMove'), 'Cancel stayed on the learning screen'
 for i,move in enumerate([63,344,751,867]):
  assert native('GetMonData3',m.symbols['gPlayerParty']+slot*100,fields['MON_DATA_MOVE'+str(i+1)],0)==move, 'Cancel changed an existing move'
 print('PASS real Rare Candy level-up to learn move',newmove,'all four existing descriptions and new fifth-row description rendered; cancel worked',flush=True)
