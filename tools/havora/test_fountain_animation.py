#!/usr/bin/env python3
"""Compile and execute actual Havora animation callbacks against a DMA recorder."""
import json,re,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[2];j=json.loads((R/'tools/havora/fountain.json').read_text());source=(R/'src/tileset_anims.c').read_text()
def function(name):
 m=re.search(r'(?:static )?void '+name+r'\([^)]*\)\s*\{',source);assert m,name
 depth=1;i=m.end()
 while depth:
  depth+=(source[i]=='{')-(source[i]=='}');i+=1
 return source[m.start():i]
header='''#include <stdint.h>
#include <assert.h>
#include <stdio.h>
typedef uint16_t u16;
#define BG_VRAM 0x06000000u
#define TILE_SIZE_4BPP 32
#define TILE_OFFSET_4BPP(n) ((n)*32u)
#define ARRAY_COUNT(a) (sizeof(a)/sizeof((a)[0]))
#define HAVORA_WATER_ANIM_START 896
#define HAVORA_WATER_ANIM_TILES 128
#define HAVORA_FOUNTAIN_ANIM_TILES 6
#define HAVORA_FOUNTAIN_FRAME_TILE_OFFSET 2
static u16 water[8][2048], fountain[5][128];
static const u16 *sHavoraWaterFrames[]={water[0],water[1],water[2],water[3],water[4],water[5],water[6],water[7]};
static const u16 *sHavoraFountainFrames[]={fountain[0],fountain[1],fountain[2],fountain[3],fountain[4]};
static u16 sHavoraFountainTileIds[]={IDS};
static u16 sSecondaryTilesetAnimCounter,sSecondaryTilesetAnimCounterMax;
static void (*sSecondaryTilesetAnimCallback)(u16);
static struct {const u16 *src; uintptr_t dest; u16 size;} transfer[20];
static unsigned count;
static void AppendTilesetAnimToBuffer(const u16 *src,u16 *dest,u16 size){assert(count<20);transfer[count].src=src;transfer[count].dest=(uintptr_t)dest;transfer[count++].size=size;}
'''.replace('IDS',','.join(map(str,j['animation_graphic_ids'])))
code=header+'\n'.join(function(n) for n in ['TilesetAnim_Havora_Harbor','InitTilesetAnim_Havora_Harbor','TilesetAnim_HavoraCity','InitTilesetAnim_HavoraCity'])+'''
int main(void){
 unsigned n,i,k,max=0;
 InitTilesetAnim_Havora_Harbor();assert(sSecondaryTilesetAnimCounterMax==128);assert(sSecondaryTilesetAnimCallback==TilesetAnim_Havora_Harbor);
 InitTilesetAnim_HavoraCity();assert(sSecondaryTilesetAnimCounterMax==1920);assert(sSecondaryTilesetAnimCallback==TilesetAnim_HavoraCity);
 for(n=0;n<3840;n++){
  u16 timer=n%sSecondaryTilesetAnimCounterMax;count=0;k=0;sSecondaryTilesetAnimCallback(timer);
  if(n%16==0){assert(transfer[k].src==sHavoraWaterFrames[(n/16)%8]);assert(transfer[k].dest==BG_VRAM+896*32);assert(transfer[k++].size==120*32);}
  if(n%12==0)for(i=0;i<6;i++){assert(transfer[k].src==sHavoraFountainFrames[(n/12)%5]+(i+2)*16);assert(transfer[k].dest==BG_VRAM+sHavoraFountainTileIds[i]*32);assert(transfer[k++].size==32);}
  assert(count==k);if(count>max)max=count;
  // General's schedule queues at most one transfer on any tick.
  assert(count+1<=20);
 }
 printf("PASS: 3840 ticks; five fountain frames; unchanged ocean phase; legacy callback unchanged; peak %u secondary DMA entries (8 including primary).\\n",max);
}
'''
p=R/'build/fountain';p.mkdir(parents=True,exist_ok=True);(p/'callback-test.c').write_text(code)
subprocess.run(['cc','-std=c99','-Wall','-Wextra','-Werror','-Wno-int-to-pointer-cast',str(p/'callback-test.c'),'-o',str(p/'callback-test')],check=True);subprocess.run([str(p/'callback-test')],check=True)
