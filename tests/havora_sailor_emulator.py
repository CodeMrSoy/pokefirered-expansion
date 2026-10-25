"""Walking into either ticket trigger turns the sailor before the Stellar prompt."""
import os,pathlib,struct,subprocess,json
import havora_emulator_support as m
source=(m.root/'tests/avatar_wardrobe_emulator.py').read_text();exec(source[source.index('native_dir ='):source.index('avatar_var = native')])
groups=json.loads((m.root/'data/maps/map_groups.json').read_text());ids={n:(g,i) for g,k in enumerate(groups['group_order']) for i,n in enumerate(groups[k])}
item=next(int(l.split()[2]) for l in (m.root/'include/constants/items.h').read_text().splitlines() if l.startswith('#define ITEM_STELLAR_TICKET '))
assert native('AddBagItem',item,1)==1
for x in [22,23]:
 g,n=ids['VermilionCity'];m.inject(b'\x39'+struct.pack('<BBBHH',g,n,255,x,31)+b'\x6b\x02');m.run(180)
 m.keys.add(5);m.run(40);m.keys.clear();m.run(120)
 sailor=None
 for i in range(16):
  b=m.read(m.symbols['gObjectEvents']+36*i,36)
  if b[0]&1 and struct.unpack('<hh',b[16:20])==(31,40):sailor=b
 assert sailor is not None
 # ObjectEvent facingDirection is the low nibble of byte24.
 assert sailor[24]&15==3,('Sailor not facing left at prompt',sailor.hex())
 assert m.read(m.symbols['sLockFieldControls'],1)!=b'\0'
 m.snap('stellar-sailor-'+str(x));m.press(0,90)
 for _ in range(8):m.press(8,40)
print('PASS both walking ticket triggers face the sailor toward the player before the Stellar Ticket question',flush=True)
