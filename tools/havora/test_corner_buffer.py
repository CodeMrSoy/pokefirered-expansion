from pathlib import Path
import os,subprocess
ROOT=Path(__file__).resolve().parents[2]
os.chdir(ROOT)
Path("build/havora-corners").mkdir(parents=True,exist_ok=True)
source=Path('src/fieldmap.c').read_text();start=source.index('static bool32 GetConnectionOrigin(');end=source.index('\nstatic void FillConnection(',start);functions=source[start:end]
pre=r'''
#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
#include <assert.h>
#include <string.h>
typedef uint16_t u16;typedef int32_t s32;typedef int bool32;
#define TRUE 1
#define FALSE 0
#define MAP_OFFSET 7
#define MAPGRID_UNDEFINED 0x03ff
#define CONNECTION_NORTH 1
#define CONNECTION_SOUTH 2
#define CONNECTION_WEST 3
#define CONNECTION_EAST 4
struct Tileset{int id;};
const struct Tileset gTileset_HavoraCityPrimary={1}, other={2};
struct MapLayout{int width,height;const struct Tileset *primaryTileset,*secondaryTileset;u16 *map;};
struct MapConnection{int direction,offset,mapNum;};
struct MapConnections{int count;struct MapConnection *connections;};
struct MapHeader{struct MapLayout *mapLayout;struct MapConnections *connections;};
struct {int Xsize,Ysize;u16*map;} VMap;
static struct MapHeader headers[4];
static const struct MapHeader *GetMapHeaderFromConnection(const struct MapConnection*c){return &headers[c->mapNum];}
'''
post=r'''
int main(void){
 static struct MapConnection c0[]={{4,-1,1},{2,49,2}},c1[]={{3,1,0},{2,0,3}},c2[]={{1,-49,0},{4,0,3}},c3[]={{1,0,1},{3,0,2}};
 static struct MapConnections connections[]={{2,c0},{2,c1},{2,c2},{2,c3}};
 int widths[]={90,37,41,20},heights[]={28,29,62,20};static struct MapLayout layouts[4];
 int origins[4][2]={{0,0},{90,-1},{49,28},{90,28}};
 for(int i=0;i<4;i++){layouts[i]=(struct MapLayout){widths[i],heights[i],&gTileset_HavoraCityPrimary,&gTileset_HavoraCityPrimary,malloc(widths[i]*heights[i]*2)};for(int j=0;j<widths[i]*heights[i];j++)layouts[i].map[j]=100+i;headers[i]=(struct MapHeader){&layouts[i],&connections[i]};}
 for(int active=0;active<4;active++){
  VMap.Xsize=widths[active]+15;VMap.Ysize=heights[active]+14;int size=VMap.Xsize*VMap.Ysize;
  u16 *guard=malloc((size+2)*2);guard[0]=12345;guard[size+1]=54321;VMap.map=guard+1;
  for(int j=0;j<size;j++)VMap.map[j]=MAPGRID_UNDEFINED;
  // Simulate the unchanged core map and cardinal-neighbor strips.
  for(int y=0;y<VMap.Ysize;y++)for(int x=0;x<VMap.Xsize;x++){
   int gx=x-7+origins[active][0],gy=y-7+origins[active][1];
   for(int k=0;k<4;k++){
    int direct=k==active;for(int t=0;t<2;t++)direct|=connections[active].connections[t].mapNum==k;
    if(direct&&gx>=origins[k][0]&&gy>=origins[k][1]&&gx<origins[k][0]+widths[k]&&gy<origins[k][1]+heights[k])VMap.map[y*VMap.Xsize+x]=100+k;
   }
  }
  u16 *before=malloc(size*2);memcpy(before,VMap.map,size*2);FillHavoraDiagonalConnections(&headers[active]);int filled=0;
  for(int y=0;y<VMap.Ysize;y++)for(int x=0;x<VMap.Xsize;x++){
   int p=y*VMap.Xsize+x;if(before[p]!=MAPGRID_UNDEFINED)assert(VMap.map[p]==before[p]);
   if(before[p]==MAPGRID_UNDEFINED&&VMap.map[p]!=MAPGRID_UNDEFINED){
    int k=VMap.map[p]-100;int gx=x-7+origins[active][0],gy=y-7+origins[active][1];assert(gx>=origins[k][0]&&gx<origins[k][0]+widths[k]);assert(gy>=origins[k][1]&&gy<origins[k][1]+heights[k]);filled++;
   }
  }
  assert(filled>0);assert(guard[0]==12345&&guard[size+1]==54321);
  // The guard must leave other regions alone.
  memcpy(VMap.map,before,size*2);layouts[active].primaryTileset=&other;FillHavoraDiagonalConnections(&headers[active]);assert(memcmp(VMap.map,before,size*2)==0);layouts[active].primaryTileset=&gTileset_HavoraCityPrimary;
  printf("view %d: %d diagonal cells filled, cardinal/main cells preserved, other-region guard passed\n",active,filled);free(before);free(guard);
 }
 for(int i=0;i<4;i++)free(layouts[i].map);
 return 0;
}
'''
Path('build/havora-corners/corner_test.c').write_text(pre+functions+post)

subprocess.run(["cc","-Wall","-Wextra","-Werror","-O2","build/havora-corners/corner_test.c","-o","build/havora-corners/corner_test"],check=True)
subprocess.run(["build/havora-corners/corner_test"],check=True)
