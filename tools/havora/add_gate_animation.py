#!/usr/bin/env python3
"""Derive a cropped retracting OBJ sheet from the user's native gate tile.

No shared BG graphics/palettes are reclaimed: the full tileset remains intact.
The temporary OBJ sheet has five 16x16 frames and uses one shared palette.
"""
import json, struct, subprocess
from pathlib import Path
from PIL import Image
R=Path(__file__).resolve().parents[2]
def words(p):
 b=p.read_bytes();return list(struct.unpack('<'+'H'*(len(b)//2),b))
def main():
 p=R/'data/tilesets/primary/havora_city/metatiles.bin';meta=words(p)
 ground=meta[:8];gate=meta[0x5a*8:0x5b*8]
 tiles=[]
 for gr in ['primary','secondary']:
  im=Image.open(R/f'data/tilesets/{gr}/havora_city/tiles.png')
  tiles.extend(im.crop((x,y,x+8,y+8)) for y in range(0,im.height,8) for x in range(0,128,8))
 assert all(w>>12==1 for w in gate[4:]),'Gate overlay needs a single palette'
 overlay=Image.new('P',(16,16))
 for k,w in enumerate(gate[4:]):
  im=tiles[w&1023]
  if w&1024:im=im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
  if w&2048:im=im.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
  overlay.paste(im,(k%2*8,k//2*8))
 sheet=Image.new('P',(16,80))
 for frame,shift in enumerate([0,4,8,12,16]):
  if shift<16:sheet.paste(overlay.crop((0,0,16,16-shift)),(0,frame*16+shift))
 lines=(R/'data/tilesets/primary/havora_city/palettes/01.pal').read_text().splitlines()[3:19]
 pal=sum((list(map(int,line.split())) for line in lines),[])
 sheet.putpalette(pal+[0]*(768-len(pal)));sheet.save(R/'graphics/havora/gate.png',bits=4)
 # Preserve the user's no-crossbar design, with plain grass beneath the posts.
 meta[0x231*8:0x232*8]=ground[:4]+gate[4:]
 p.write_bytes(struct.pack('<'+'H'*len(meta),*meta))
 base=json.loads((R/'tools/havora/gate-animation.json').read_text())['base_commit'] if (R/'tools/havora/gate-animation.json').exists() else subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip()
 manifest={'base_commit':base,'source_gate_metatile':90,'closed_metatile':561,'open_metatile':562,'frame_shifts':[0,4,8,12,16],'ticks_per_frame':6,'frames':5,'obj_tiles':20,'background_palette':1,'sheet':'graphics/havora/gate.png','maps_changed':False}
 (R/'tools/havora/gate-animation.json').write_text(json.dumps(manifest,indent=2)+'\n')
if __name__=='__main__':main()
