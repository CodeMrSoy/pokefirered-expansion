#!/usr/bin/env python3
"""Compare the release against the pre-cleanup ELF/ROM, including protected audio."""
from pathlib import Path
import os,re,struct,subprocess,json
root=Path(__file__).resolve().parents[1];os.chdir(root)
nm=os.environ.get('ARM_NM','arm-none-eabi-nm')
def symbols(p):
 result={}
 for l in subprocess.check_output([nm,str(p)],text=True).splitlines():
  a=l.split()
  if len(a)==3:result[a[2]]=int(a[0],16)
 return result
oldsy=symbols(root/'build/cleanup-baseline/pokefirered.elf');newsy=symbols(root/'pokefirered.elf')
old=(root/'build/cleanup-baseline/pokefirered.gba').read_bytes();new=(root/'pokefirered.gba').read_bytes()
def data(rom,sy,name,n):return rom[sy[name]-0x8000000:sy[name]-0x8000000+n]
count=0
for name,path in re.findall(r'^(\w+)::\s*\n\s*\.incbin "([^"]+)"',Path('sound/direct_sound_data.inc').read_text(),re.M):
 if name not in oldsy:continue
 assert name in newsy,('Missing audio',name)
 size=Path(path).stat().st_size
 assert data(old,oldsy,name,size)==data(new,newsy,name,size),('Changed audio',name)
 count+=1
songs=re.findall(r'^\s*song (\w+),',Path('sound/song_table.inc').read_text(),re.M)
assert all(n in newsy for n in songs if n in oldsy)
# All species retain numeric IDs. Check unchanged stat/type headers outside retired forms.
defs=dict(re.findall(r'^#define\s+(SPECIES_\w+)\s+(\w+)',Path('include/constants/species.h').read_text(),re.M))
def number(n):
 while not n.isdigit():n=defs[n]
 return int(n)
retired={number(n) for n in json.loads(Path('docs/rom-retired-forms.json').read_text())}
old_size=260;size=256;checked=0
for i in range(1525):
 a=data(old,oldsy,'gSpeciesInfo',(i+1)*old_size)[i*old_size:i*old_size+8]
 b=data(new,newsy,'gSpeciesInfo',(i+1)*size)[i*size:i*size+8]
 if i in retired:assert not any(b),(i,'Retired form still has stats')
 else:assert a==b,(i,'Protected species stats changed');checked+=1
rows=struct.unpack('<III',data(new,newsy,'gTrainers',12));assert rows[0]==rows[2] and rows[1]!=rows[0]
for f in ['include/constants/species.h','include/constants/items.h','include/constants/opponents.h','data/maps/map_groups.json','data/layouts/layouts.json']:
 assert not subprocess.check_output(['git','diff','HEAD','--',f]),('Renumbered IDs',f)
print(f'{count} audio samples byte-identical; {len(songs)} song/SFX entries retained; {checked} protected species stat/type headers unchanged; {len(retired)} forms retired; IDs and difficulty fallback stable')
