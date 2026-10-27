"""Native replay of revised color rules and actual trainer sight approach."""
from pathlib import Path
src=Path(__file__).with_name('havora_tidal_trial_emulator.py').read_text()
exec(compile(src[:src.index('# Migrate legacy')],'directional-setup','exec'))
plan=json.loads((m.root/'build/havora-tests/directional-solution.json').read_text())
native('VarSet',0x40d7,encode((0,0,0)));native('VarSet',0x40d8,0);native('VarSet',0x40da,0);warp()
# Battle-win fixtures prevent incidental sight fights during the state replay.
for tid in range(743,751):native('SetTrainerFlag',tid)
w=(0,0,0)
for action,state in plan:
 kind=action[0]
 if kind=='battle':assert command(22,P[action[1]]['victory'])==1
 elif kind=='switch':
  n,k=action[1:3];x,y=P[n]['switches'][k];b=geo.draw((w,0,0,4,0,False))
  adjacent=next((xx,yy) for xx,yy in [(x+1,y),(x-1,y),(x,y+1),(x,y-1)] if 0<=xx<80 and 0<=yy<27 and not b[yy*80+xx]&0xc00 and (xx,yy) not in {tuple(p['npc']) for p in P})
  stage(*adjacent);assert command(30,n,k)==1,(action,w,pos())
 elif kind=='travel':
  link=L[action[1]];stage(*link['pad_from']);assert command(31)==1,(action,w)
  assert [value(0x8008),value(0x8009)]==link['pad_to'];stage(*link['pad_to'])
 elif kind=='walk':walk_to(P[action[1]]['npc'],w)
 w=tuple(state[0]);assert value(0x40d7)==encode(w);assert_map(w)
print('PASS native revised solution: wraparound colors, seven victories/switch stations, fixed directional routes and MID AR3/BL3',flush=True)
# Inbound-only pads cannot call the reverse transport.
stage(75,11);assert command(31)==3
# Every color and both wraps, from actual authored levers.
for n,k,color in [(0,0,'green'),(0,1,'red'),(0,2,'yellow'),(6,0,'blue')]:
 for levels in [(0,0,0),(2,2,2)]:
  if n==6:levels=(levels[0],0,levels[2])
  setwater(levels);x,y=P[n]['switches'][k];stage(x+1,y) if n!=6 else stage(39,10)
  assert command(30,n,k)==1
  from tidal_color_rules import apply_switch
  assert value(0x40d7)==encode(apply_switch(levels,color))
print('PASS all four native switch effects, upward and downward wrapping; inbound pad rejects reverse travel',flush=True)
# Real approach: walk into horizontal sight at range 3; observe approach and doubles battle.
fixture=b''
for species in [131,68]:fixture+=b'\x23'+struct.pack('<I',(m.symbols['ScrCmd_createmon']|1)+0x2000000)+struct.pack('<BBHHI',0,6,species,60,0)
m.inject(fixture+b'\x02')
size=m.lib.retro_serialize_size();snapshot=m.c.create_string_buffer(size);assert m.lib.retro_serialize(snapshot,size)
native('ClearTrainerFlag',749);setwater((0,0,0));stage(4,7)
g,n=ids['Havora_Gym'];obj=native('GetObjectEventIdByLocalIdAndMap',8,n,g)&255
before=struct.unpack('<hh',m.read(m.symbols['gObjectEvents']+obj*36+16,4))
m.press(4,30);m.press(4,120)
for _ in range(20):
 m.press(8,80)
 if m.read(m.symbols['gBattlersCount'],1)==b'\x04':break
assert m.read(m.symbols['gBattlersCount'],1)==b'\x04','sight did not start doubles battle'
after=struct.unpack('<hh',m.read(m.symbols['gObjectEvents']+obj*36+16,4))
assert after!=before,('trainer did not approach',before,after)
print('PASS actual horizontal sight -> trainer walks toward player -> doubles battle',flush=True)

assert m.lib.retro_unserialize(snapshot,size)
setwater((0,1,0));stage(41,10)
assert command(30,6,2)==1
walk_to((39,9),(1,0,2))
assert command(30,6,0)==1
assert value(0x40d7)==encode((2,1,1))
walk_to((41,9),(2,1,1))
print('PASS actual island walking after MID -> LOW -> MID floor elevation changes',flush=True)
