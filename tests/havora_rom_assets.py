"""Verify that the compiled ROM embeds the current Porymap blocks and native art."""
from pathlib import Path
import subprocess,os,struct
from PIL import Image
R=Path(__file__).resolve().parents[1]
sy={}
for line in subprocess.check_output([os.environ.get('ARM_NM','arm-none-eabi-nm'),str(R/'pokefirered.elf')],text=True).splitlines():
 p=line.split()
 if len(p)==3:sy[p[2]]=int(p[0],16)
rom=(R/'pokefirered.gba').read_bytes()
def check(symbol,path):
 data=(R/path).read_bytes();off=sy[symbol]-0x8000000;assert rom[off:off+len(data)]==data,('Stale ROM data',symbol,path)
for symbol,name in [('Quantum_Havora_Harbor_Layout','Quantum_Havora_Harbor_Layout'),('QuantumHavoraWestQuay_Layout','QuantumHavoraWestQuay'),('QuantumHavoraNorthQuay_Layout','QuantumHavoraNorthQuay'),('QuantumPortCity_Layout','QuantumPortCity')]+[(n+'_Layout',n) for n in ['QuantumHavoraNorthDistrict','QuantumHavoraCoastalDaycare','QuantumHavoraNorthWalk','QuantumHarborRoad']]:
 for suffix,file in [('Blockdata','map.bin'),('Border','border.bin')]:check(symbol+'_'+suffix,'data/layouts/'+name+'/'+file)
for suffix,directory,folder in [('HavoraPrimary','primary','havora_harbor'),('HavoraHarbor','secondary','havora_harbor'),('HavoraCityPrimary','primary','havora_city'),('HavoraCity','secondary','havora_city')]:
 root='data/tilesets/'+directory+'/'+folder+'/'
 check('gMetatiles_'+suffix,root+'metatiles.bin');check('gMetatileAttributes_'+suffix,root+'metatile_attributes.bin');check('gTilesetTiles_'+suffix,root+'tiles.4bpp.lz')
 # Decode the actual ROM compression, then compare indices with the source PNG.
 off=sy['gTilesetTiles_'+suffix]-0x8000000;b=rom[off:];assert b[0]==0x10;size=int.from_bytes(b[1:4],'little');out=bytearray();pos=4
 while len(out)<size:
  flags=b[pos];pos+=1
  for bit in range(7,-1,-1):
   if len(out)>=size:break
   if flags&(1<<bit):
    a,c=b[pos:pos+2];pos+=2;length=(a>>4)+3;distance=((a&15)<<8|c)+1
    for _ in range(length):out.append(out[-distance])
   else:out.append(b[pos]);pos+=1
 im=Image.open(R/root/'tiles.png');expected=bytearray()
 for ty in range(0,im.height,8):
  for tx in range(0,im.width,8):
   for y in range(8):
    for x in range(0,8,2):expected.append(im.getpixel((tx+x,ty+y))|(im.getpixel((tx+x+1,ty+y))<<4))
 assert out==expected[:len(out)],('PNG/ROM graphics mismatch',suffix)
print('PASS: ROM blocks/borders, metatile tables, attributes and decompressed native graphics match the current source')
for frame in range(8):
 check('sHavoraWaterFrame'+str(frame),'data/tilesets/secondary/havora_harbor/anim/water/'+str(frame)+'.4bpp')
print('PASS: all eight current water DMA frames are embedded in the ROM')
