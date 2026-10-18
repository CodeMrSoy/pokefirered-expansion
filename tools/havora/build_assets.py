#!/usr/bin/env python3
"""Pack Havora art across a dedicated primary/secondary pair without tile loss.

Keep General pavement, water, shrubs and all General animation destinations at
identical tile IDs. Other primary slots are available for the harbor artwork;
this avoids shrinking buildings just to fit a single 384-tile secondary bank.
"""
from pathlib import Path
from PIL import Image
from firered_buildings import exteriors
from firered_waterfront import waterfront_assets
import numpy as np,struct,json,shutil
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'data/tilesets/secondary/havora_harbor';PRIMARY=ROOT/'data/tilesets/primary/havora_harbor'
SPECS=[
 ('warehouse','harbor-assets.png',(6,55,345,424),(80,96),2),
 ('fish_store','harbor-assets.png',(345,55,669,424),(80,96),3),
 ('office','harbor-assets.png',(669,120,1000,424),(64,64),5),
 ('lighthouse','harbor-assets.png',(1000,10,1238,427),(48,96),4),
 ('crane','harbor-assets.png',(35,435,330,699),(48,64),7),
 ('cargo','harbor-assets.png',(395,510,615,699),(32,32),7),
 ('crate','harbor-assets.png',(720,555,872,699),(16,16),7),
 ('barrel','harbor-assets.png',(1010,550,1175,699),(16,16),7),
 ('lamp','harbor-assets.png',(125,719,241,970),(16,32),8),
 ('bollard','harbor-assets.png',(405,815,570,970),(16,16),8),
 ('rope','harbor-assets.png',(710,825,880,970),(16,16),11),
 ('net','harbor-assets.png',(980,726,1225,970),(16,32),11),
 ('wood','harbor-assets.png',(475,1035,650,1218),(16,16),12),
 ('gate','harbor-assets.png',(1035,965,1175,1218),(16,32),11),
 ('wall','harbor-terrain.png',(65,195,590,482),(32,32),9),
 ('wall_side','harbor-terrain.png',(707,82,905,495),(16,32),9),
 ('rock','harbor-terrain.png',(1070,145,1505,485),(32,32),9),
 ('pile','harbor-terrain.png',(238,563,381,962),(16,32),11),
 ('dock_face','harbor-terrain.png',(578,664,1028,934),(32,16),11),
 ('planter','harbor-terrain.png',(1208,678,1430,925),(16,16),10)]
def unpack(p):
 b=p.read_bytes();return list(struct.unpack('<'+'H'*(len(b)//2),b))
def main():
 for p in [OUT,PRIMARY]:p.mkdir(parents=True,exist_ok=True);(p/'palettes').mkdir(exist_ok=True)
 originals=ROOT/'data/tilesets/primary/general';raw_meta=unpack(originals/'metatiles.bin');raw_attrs=(originals/'metatile_attributes.bin').read_bytes();general=Image.open(originals/'tiles.png')
 assets={}
 for name,file,box,size,bank in SPECS:
  a=Image.open(ROOT/'tools/havora/source_art'/file).convert('RGBA').crop(box)
  alpha=a.getchannel('A').point(lambda v:255 if v>=220 else 0);a.putalpha(alpha);a=a.crop(alpha.getbbox());a=a.resize(size,Image.Resampling.NEAREST)
  if name in ['pile','lamp']:
   narrow=a.resize((10,size[1]),Image.Resampling.NEAREST);a=Image.new('RGBA',size);a.paste(narrow,((size[0]-10)//2,0))
  assets[name]=(a,bank)
 # Native FireRed architecture overrides the earlier resampled concept exteriors.
 for name,a in exteriors().items():assets[name]=(a,assets[name][1])
 assets.update(waterfront_assets(assets))
 palettes={}
 for bank in range(13):
  if bank in [0,1,6]:
   palettes[bank]=[tuple(map(int,s.split())) for s in (originals/'palettes'/f'{bank:02}.pal').read_text().splitlines()[3:19]];continue
  rgb=[]
  for name,(a,b) in assets.items():
   # New coping variants must not shift the approved rock/masonry palette.
   if bank==9 and name not in ['wall','wall_side','rock']:continue
   if b==bank:rgb.extend([tuple(p[:3]) for p in np.array(a).reshape(-1,4) if p[3]])
  train=Image.new('RGB',(len(rgb),1));train.putdata(rgb);q=train.quantize(15,method=Image.Quantize.MEDIANCUT)
  # Native-style assets can use fewer than 15 colors; pad the fixed GBA bank.
  qp=(q.getpalette()+[0]*45)[:45]
  colors=[tuple((v>>3)<<3 for v in qp[i:i+3]) for i in range(0,45,3)];palettes[bank]=[(0,0,0)]+colors
 for bank in range(16):
  colors=palettes.get(bank,[(0,0,0)]*16);content='JASC-PAL\n0100\n16\n'+'\n'.join(' '.join(map(str,c)) for c in colors)+'\n'
  for p in [PRIMARY,OUT]:(p/'palettes'/f'{bank:02}.pal').write_text(content)
 keep_metas=[5,0x1c1,0x1d9];reserved={0}|set(range(416,482))|set(range(508,512))
 for mid in keep_metas:
  for v in raw_meta[mid*8:mid*8+8]:reserved.add(v&1023)
 assert all(v<640 for v in reserved)
 tiles={};lookup={}
 for tid in sorted(reserved):
  ar=np.array(general.crop(((tid%16)*8,(tid//16)*8,(tid%16)*8+8,(tid//16)*8+8)),dtype=np.uint8)
  tiles[tid]=ar
  if tid not in set(range(416,482))|set(range(508,512)):lookup.setdefault(ar.tobytes(),tid)
 # A guaranteed transparent tile, independent of the original tile zero contents.
 blank=next(i for i in range(640) if i not in reserved);tiles[blank]=np.zeros((8,8),dtype=np.uint8);lookup[tiles[blank].tobytes()]=blank
 free=iter([i for i in range(1024) if i not in tiles]);custom_count=0
 def pack(t):
  nonlocal custom_count
  for arr,flip in [(t,0),(t[:,::-1],1024),(t[::-1,:],2048),(t[::-1,::-1],3072)]:
   if arr.tobytes() in lookup:return lookup[arr.tobytes()]|flip
  try:idx=next(free)
  except StopIteration:raise AssertionError('Havora graphics exceed 1024 tiles')
  tiles[idx]=t.copy();lookup[t.tobytes()]=idx;custom_count+=1;return idx
 def quantize(a,bank):
  ar=np.array(a);colors=np.array(palettes[bank][1:],dtype=np.int32);delta=ar[:,:,:3].astype(np.int32)[:,:,None,:]-colors
  ix=np.argmin((delta*delta).sum(3),2).astype(np.uint8)+1;ix[ar[:,:,3]<128]=0;return ix
 quant={name:quantize(a,bank) for name,(a,bank) in assets.items()};metas=[];attrs=[];info={};floors={}
 def pixels4(ar,bank):return [pack(ar[y:y+8,x:x+8])|(bank<<12) for y in [0,8] for x in [0,8]]
 floors['stone']=640;metas.append(raw_meta[0x1c1*8:0x1c1*8+8]);attrs.append(0)
 floors['wood']=641;metas.append(pixels4(quant['wood'],12)+[blank]*4);attrs.append(0)
 water=raw_meta[0x1d9*8:0x1d9*8+4]
 for name,(a,bank) in assets.items():
  if name=='wood':continue
  ar=quant[name];w,h=a.size;ids=[]
  for y in range(0,h,16):
   row=[]
   for x in range(0,w,16):
    water_backed=name in ['wall','wall_side','rock','dock_face','wall_corner_left','wall_corner_right','dock_tip_left','dock_tip_right','boarding_ramp'] or (name=='pile' and y>0)
    wood_backed=name in ['pile','bollard','rope','net','dock_rail_left','dock_rail_right','dock_head','dock_post_left','dock_post_right','dock_boarding_gate']
    base=water if water_backed else metas[floors['wood' if wood_backed else 'stone']-640][:4]
    row.append(640+len(metas));metas.append(list(base)+pixels4(ar[y:y+16,x:x+16],bank));attrs.append(0)
   ids.append(row)
  info[name]={'metatiles':ids,'size':[w//16,h//16],'bank':bank}
 assert len(metas)<=384
 pm=[blank]*5120;pa=bytearray(640*4)
 for mid in keep_metas:pm[mid*8:mid*8+8]=raw_meta[mid*8:mid*8+8];pa[mid*4:mid*4+4]=raw_attrs[mid*4:mid*4+4]
 (PRIMARY/'metatiles.bin').write_bytes(struct.pack('<5120H',*pm));(PRIMARY/'metatile_attributes.bin').write_bytes(pa)
 secondary_count=max(1,max(tiles)-639)
 for p,start,count in [(PRIMARY,0,640),(OUT,640,secondary_count)]:
  im=Image.new('P',(128,((count+15)//16)*8),0);im.putpalette(sum((list(c) for c in palettes[2]),[])+[0]*720)
  for tid in range(start,start+count):
   if tid in tiles:im.paste(Image.fromarray(tiles[tid],'P'),(((tid-start)%16)*8,((tid-start)//16)*8))
  im.save(p/'tiles.png')
 (OUT/'metatiles.bin').write_bytes(struct.pack('<'+'H'*(8*len(metas)),*sum(metas,[])));(OUT/'metatile_attributes.bin').write_bytes(struct.pack('<'+'I'*len(attrs),*attrs))
 data={'floors':floors,'assets':info,'tiles':max(tiles)+1,'custom_tiles':custom_count,'reserved_primary_tiles':sorted(reserved),'blank_tile':blank,'secondary_tiles':secondary_count,'metatiles':len(metas),'palette_banks':list(range(13))}
 (ROOT/'tools/havora/assets.json').write_text(json.dumps(data,indent=2)+'\n')
 sheet=Image.new('RGB',(480,((len(SPECS)+4)//5)*112),'#87959e')
 for i,(name,_,_,_,bank) in enumerate(SPECS):
  ar=quant[name];rgba=np.array([(*c,255) for c in palettes[bank]],dtype=np.uint8)[ar];rgba[ar==0,3]=0;a=Image.fromarray(rgba,'RGBA');sheet.paste(a,((i%5)*96,(i//5)*112),a)
 sheet.resize((960,sheet.height*2),Image.Resampling.NEAREST).save(ROOT/'build/havora-assets-native.png')
 print(json.dumps({'custom_tiles':custom_count,'reserved_primary_tiles':len(reserved),'highest_tile':max(tiles),'metatiles':len(metas)}))
if __name__=='__main__':main()
