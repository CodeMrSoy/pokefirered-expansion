#!/usr/bin/env python3
"""Derive a cropped retracting OBJ sheet from the user's native gate tile.

The open tile keeps the log end-grain visible at ground level. One previously
blank, unreferenced tile in the ocean animation tail stores the static caps.
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
 # A flattened end-grain face has no vertical trunk edge: it reads as flush
 # with the grass rather than as two short stumps. Use existing wood colors.
 cap=Image.new('P',(8,8))
 rows=[[0,0,13,13,13,13,0,0],[0,13,12,10,10,12,13,0],
       [0,13,10,11,11,10,13,0],[0,0,13,13,13,13,0,0]]
 for y,row in enumerate(rows,4):
  for x,value in enumerate(row):cap.putpixel((x,y),value)
 resting=Image.new('P',(16,16));resting.paste(cap,(0,8));resting.paste(cap,(8,8))
 sheet=Image.new('P',(16,80))
 for frame,shift in enumerate([0,4,8,10,None]):
  if shift is None:sheet.paste(resting,(0,frame*16))
  else:sheet.paste(overlay.crop((0,0,16,16-shift)),(0,frame*16+shift))
 lines=(R/'data/tilesets/primary/havora_city/palettes/01.pal').read_text().splitlines()[3:19]
 pal=sum((list(map(int,line.split())) for line in lines),[])
 sheet.putpalette(pal+[0]*(768-len(pal)));sheet.save(R/'graphics/havora/gate.png',bits=4)
 # Preserve the user's no-crossbar design, with plain grass beneath the posts.
 meta[0x231*8:0x232*8]=ground[:4]+gate[4:]
 meta[0x232*8:0x233*8]=ground[:4]+[0,0,0x13f8,0x13f8]
 secondary=R/'data/tilesets/secondary/havora_city/tiles.png'
 im=Image.open(secondary);im.paste(cap,((1016-640)%16*8,(1016-640)//16*8));im.save(secondary,bits=4)
 p.write_bytes(struct.pack('<'+'H'*len(meta),*meta))
 base=json.loads((R/'tools/havora/gate-animation.json').read_text())['base_commit'] if (R/'tools/havora/gate-animation.json').exists() else subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip()
 manifest={'base_commit':base,'source_gate_metatile':90,'closed_metatile':561,'open_metatile':562,'frame_shifts':[0,4,8,10,None],'bg_cap_graphic':1016,'water_animated_tiles':120,'ticks_per_frame':6,'frames':5,'obj_tiles':20,'background_palette':1,'sheet':'graphics/havora/gate.png','maps_changed':False}
 (R/'tools/havora/gate-animation.json').write_text(json.dumps(manifest,indent=2)+'\n')
if __name__=='__main__':main()
