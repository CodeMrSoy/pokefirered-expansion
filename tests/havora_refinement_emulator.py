"""In-game checks for the visible quay boundary and Minior story marker."""
import json,struct
import havora_emulator_support as m
groups=json.loads((m.root/'data/maps/map_groups.json').read_text())['gMapGroup_QuantumIsland']
def warp(name,x,y):
 m.inject(b'\x39'+struct.pack('<BBBHH',43,groups.index(name),255,x,y)+b'\x6b\x02');m.run(240)
def loc():
 p=struct.unpack('<I',m.read(m.symbols['gSaveBlock1Ptr'],4))[0]
 return tuple(m.read(p+4,2)),struct.unpack('<hh',m.read(p,4))
def walk(key,frames):
 m.keys.add(key);m.run(frames);m.keys.clear();m.run(90)
# Regression: the old invisible western boundary is now a visible railing.
warp('QuantumPortCity',46,75);before=loc();walk(7,40);assert loc()==before
m.snap('refined-west-railing')
# Exercise the Minior story sign through normal facing + A interaction.
warp('QuantumHavoraNorthWalk',5,21);walk(6,1);m.press(8);m.run(180)
import re
charmap={a:int(b,16) for a,b in re.findall(r"^'(.)'\s*=\s*(?:0x)?([0-9A-Fa-f]{2})",(m.root/'charmap.txt').read_text(),re.M)}
assert bytes(charmap[c] for c in 'MINIOR') in m.read(m.symbols['gStringVar4'],256),'Minior sign text did not open'
m.snap('refined-minior-marker');m.press(0);m.press(0)
print('PASS: visible western railing blocks crossing and Minior sign opens its actual dialogue',flush=True)
# Camera connections must refresh the primary graphics bank, not just the
# secondary bank. Otherwise coordinate-only tests pass over scrambled terrain.
from PIL import Image
reserved=set(json.loads((m.root/'tools/havora/assets.json').read_text())['reserved_primary_tiles'])
def primary_pixels(folder):
 im=Image.open(m.root/'data/tilesets/primary'/folder/'tiles.png');out=bytearray()
 for ty in range(0,320,8):
  for tx in range(0,128,8):
   for yy in range(8):
    for xx in range(0,8,2):out.append(im.getpixel((tx+xx,ty+yy)) | (im.getpixel((tx+xx+1,ty+yy))<<4))
 return out
for source,x,y,key,target,folder in [
 ('QuantumHarborRoad',22,9,7,'QuantumPortCity','havora_city'),
 ('QuantumPortCity',1,69,6,'QuantumHarborRoad','general'),
 ('QuantumHarbor',5,1,4,'QuantumHavoraNorthQuay','havora_city'),
 ('QuantumHavoraNorthQuay',5,62,5,'QuantumHarbor','havora_harbor')]:
 warp(source,x,y);walk(key,35);assert loc()[0]==(43,groups.index(target))
 if folder=='general':
  active=struct.unpack('<I',m.read(m.symbols['gCurrentPrimaryTileset'],4))[0]
  for season in ['Autumn','Summer','Winter']:
   if active==m.symbols['gTileset_General'+season]:folder='general_'+season.lower()
 expected=primary_pixels(folder)
 for tid in range(640):
  if tid not in reserved:assert m.read(0x06000000+tid*32,32)==expected[tid*32:(tid+1)*32],('stale primary VRAM',source,target,tid)
 m.snap('refined-primary-'+source+'-'+target)
print('PASS: four different-primary crossings load the destination static graphics into real VRAM',flush=True)
