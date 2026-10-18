#!/usr/bin/env python3
"""Convert authored harbor art into GBA palettes, 8px tiles and 16px metatiles.

No runtime art approximation: transparent pixel silhouettes are quantized to
15 opaque RGB555 colors per bank; deduplication only reuses exact tile flips.
"""
from pathlib import Path
from PIL import Image
import numpy as np,struct,json
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'data/tilesets/secondary/havora_harbor'
# Source atlas regions and intended native pixel dimensions. Six palette banks.
SPECS=[
 ('warehouse',(6,55,345,424),(64,64),7),('fish_store',(345,55,669,424),(64,64),7),
 ('office',(669,120,1000,424),(48,48),7),('lighthouse',(1000,10,1238,427),(32,64),8),
 ('crane',(35,435,330,699),(32,48),9),('cargo',(395,510,615,699),(32,32),9),
 ('crate',(720,555,872,699),(16,16),9),('barrel',(1010,550,1175,699),(16,16),9),
 ('lamp',(125,719,241,970),(16,32),10),('bollard',(405,815,570,970),(16,16),10),
 ('rope',(710,825,880,970),(16,16),9),('net',(980,726,1225,970),(16,32),9),
 ('wall',(25,1020,385,1210),(32,16),11),('wood',(475,1035,650,1218),(16,16),12),
 ('stone',(735,1035,915,1218),(16,16),11),('gate',(1035,965,1175,1218),(16,32),9)]
def main():
 OUT.mkdir(parents=True,exist_ok=True);(OUT/'palettes').mkdir(exist_ok=True)
 src=Image.open(ROOT/'tools/havora/source_art/harbor-assets.png').convert('RGBA');assets={}
 for name,box,size,bank in SPECS:
  a=src.crop(box);alpha=a.getchannel('A').point(lambda v:255 if v>=128 else 0);a.putalpha(alpha);bb=alpha.getbbox();a=a.crop(bb)
  a=a.resize(size,Image.Resampling.NEAREST);assets[name]=(a,bank)
 palettes={}
 for bank in range(7,13):
  rgb=[]
  for a,b in assets.values():
   if b==bank:rgb.extend([p[:3] for p in a.getdata() if p[3]])
  train=Image.new('RGB',(len(rgb),1));train.putdata(rgb);q=train.quantize(15,method=Image.Quantize.MEDIANCUT)
  colors=[tuple((v>>3)<<3 for v in q.getpalette()[i:i+3]) for i in range(0,45,3)]
  palettes[bank]=[(0,0,0)]+colors
 for bank in range(16):
  colors=palettes.get(bank,[(0,0,0)]*16)
  (OUT/'palettes'/f'{bank:02}.pal').write_text('JASC-PAL\n0100\n16\n'+'\n'.join(' '.join(map(str,c)) for c in colors)+'\n')
 tiles=[np.zeros((8,8),dtype=np.uint8)];lookup={tiles[0].tobytes():640};metas=[];attrs=[];info={};quant={}
 def pack(t):
  for arr,flip in [(t,0),(t[:,::-1],1024),(t[::-1,:],2048),(t[::-1,::-1],3072)]:
   if arr.tobytes() in lookup:return lookup[arr.tobytes()]|flip
  idx=640+len(tiles);tiles.append(t.copy());lookup[t.tobytes()]=idx;return idx
 def quantize(a,bank):
  ar=np.array(a);colors=np.array(palettes[bank][1:],dtype=np.int32);delta=ar[:,:,:3].astype(np.int32)[:,:,None,:]-colors
  ix=np.argmin((delta*delta).sum(3),2).astype(np.uint8)+1;ix[ar[:,:,3]<128]=0;return ix
 for name,(a,b) in assets.items():quant[name]=quantize(a,b)
 def lower(name):
  a=quant[name];bank=assets[name][1];return [pack(a[y:y+8,x:x+8])|(bank<<12) for y in [0,8] for x in [0,8]]
 floors={}
 for name in ['stone','wood']:
  floors[name]=640+len(metas)
  if name=='stone':
   primary=struct.unpack('<5120H',(ROOT/'data/tilesets/primary/general/metatiles.bin').read_bytes())
   metas.append(list(primary[0x1c1*8:0x1c1*8+8]))
  else:metas.append(lower(name)+[640]*4)
  attrs.append(0)
 # Native water metatile is used directly, leaving General's water animation intact.
 water=struct.unpack('<5120H',(ROOT/'data/tilesets/primary/general/metatiles.bin').read_bytes())[0x1d9*8:0x1d9*8+4]
 for name,(a,bank) in assets.items():
  if name in floors:continue
  ar=quant[name];w,h=a.size;ids=[]
  base=water if name=='wall' else metas[floors['wood' if name in ['bollard','rope','net'] else 'stone']-640][:4]
  for y in range(0,h,16):
   row=[]
   for x in range(0,w,16):
    row.append(640+len(metas));meta=list(base)
    meta += [pack(ar[y+dy:y+dy+8,x+dx:x+dx+8])|(bank<<12) for dy in [0,8] for dx in [0,8]]
    metas.append(meta);attrs.append(0)
   ids.append(row)
  info[name]={'metatiles':ids,'size':[w//16,h//16],'bank':bank}
 assert len(tiles)<=384,('secondary tile overflow',len(tiles))
 assert len(metas)<=384
 im=Image.new('P',(128,((len(tiles)+15)//16)*8),0);im.putpalette(sum((list(c) for c in palettes[7]),[])+[0]*720)
 for i,t in enumerate(tiles):im.paste(Image.fromarray(t,'P'),((i%16)*8,(i//16)*8))
 im.save(OUT/'tiles.png');(OUT/'metatiles.bin').write_bytes(struct.pack('<'+'H'*(8*len(metas)),*sum(metas,[])))
 (OUT/'metatile_attributes.bin').write_bytes(struct.pack('<'+'I'*len(attrs),*attrs))
 data={'floors':floors,'assets':info,'tiles':len(tiles),'metatiles':len(metas),'palette_banks':[7,8,9,10,11,12]}
 (ROOT/'tools/havora/assets.json').write_text(json.dumps(data,indent=2)+'\n')
 # Review sheet uses the exact indexed RGB555 asset pixels, not the original art.
 sheet=Image.new('RGB',(256,256),'#87959e')
 for i,(name,_,_,bank) in enumerate(SPECS):
  ar=quant[name];rgba=np.array([(*c,255) for c in palettes[bank]],dtype=np.uint8)[ar];rgba[ar==0,3]=0
  a=Image.fromarray(rgba,'RGBA');sheet.paste(a,((i%4)*64,(i//4)*64),a)
 sheet.resize((768,768),Image.Resampling.NEAREST).save(ROOT/'build/havora-assets-native.png')
 print(json.dumps({k:data[k] for k in ['tiles','metatiles','palette_banks']}))
if __name__=='__main__':main()
