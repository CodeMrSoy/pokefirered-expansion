"""Actual ROM priority and visual overlap on Havora's walkable canopy/roof caps."""
import struct,json
from pathlib import Path
import havora_emulator_support as m
from PIL import Image,ImageDraw
G=json.loads((m.root/'data/maps/map_groups.json').read_text());ids={n:(g,i) for g,k in enumerate(G['group_order']) for i,n in enumerate(G[k])}
def warp(n,x,y):
 g,k=ids[n];m.inject(b'\x39'+struct.pack('<BBBHH',g,k,255,x,y)+b'\x6b\x02');m.run(180)
def player():return m.symbols['gObjectEvents']+m.read(m.symbols['gPlayerAvatar']+5,1)[0]*36
def sprite():return m.symbols['gSprites']+m.read(player()+35,1)[0]*68
def priority():return (struct.unpack('<H',m.read(sprite()+4,2))[0]>>10)&3
frames=[]
for name,n,x,y in [('tree','Havora_WestQuadrant',7,1),('roof4','Havora_WestQuadrant',23,31),('roof6','Havora_NorthQuadrant',34,16)]:
 warp(n,x,y);o=player();s=sprite();height=m.read(o+11,1)[0]
 assert priority()==2 and m.read(s+66,1)[0]&63==1,(name,'not below canopy',priority(),height)
 m.snap('occlusion-'+name);after=m.screen.copy()
 # Reproduce the former bridge priority at the same position for a direct
 # comparison. FixedPriority is fixture-only; no terrain/graphics are edited.
 flags=m.read(o+3,1)[0];m.write(o+3,bytes([flags|4]))
 attr=struct.unpack('<H',m.read(s+4,2))[0];m.write(s+4,struct.pack('<H',(attr&~0xc00)|0x400));sub=m.read(s+66,1)[0];m.write(s+66,bytes([(sub&0xc0)|2]));m.run(3);before=m.screen.copy()
 from PIL import ImageChops
 assert ImageChops.difference(before,after).getbbox(),(name,'no visual overlap exercised')
 frames.append((name,before,after))
 assert m.read(o+11,1)[0]==height,'Changed physical elevation'
 m.write(o+3,bytes([flags]))
# Dock decks at native elevation 2 and stock Kanto retain their ordering.
warp('Havora_Harbor',12,5);assert priority()==2
warp('PalletTown',10,9);assert priority()==2
out=Image.new('RGB',(960,len(frames)*348),'#183139');d=ImageDraw.Draw(out)
for i,(name,before,after) in enumerate(frames):
 y=i*348;d.text((10,y+5),name+' — previous ordering / corrected ordering',fill='white');out.paste(before.resize((480,320),Image.Resampling.NEAREST),(0,y+25));out.paste(after.resize((480,320),Image.Resampling.NEAREST),(480,y+25))
p=m.root/'docs/havora/review/occlusion-comparison.png';out.save(p)
print('PASS actual canopy and roof overlap on elevations 4/6, ground sprite priorities, unchanged physical elevation, and stock Kanto ordering',flush=True)
