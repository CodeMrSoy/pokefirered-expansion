#include "global.h"
#include "event_data.h"
#include "event_object_movement.h"
#include "field_camera.h"
#include "field_player_avatar.h"
#include "fieldmap.h"
#include "overworld.h"
#include "script.h"
#include "task.h"
#include "sprite.h"
#include "script_menu.h"
#include "strings.h"
#include "sound.h"
#include "constants/songs.h"
#include "string_util.h"
#include "data/havora_lock_geometry.h"
#include "constants/maps.h"
#include "constants/vars.h"

static void MoveBoat(u8 id);
static void LaunchPassenger(struct Sprite *sprite)
{
 struct ObjectEvent *player=&gObjectEvents[gPlayerAvatar.objectEventId];
 struct Sprite *passenger=&gSprites[player->spriteId];
 sprite->invisible=!sprite->data[0];
 if(sprite->invisible)return;
 sprite->x=passenger->x;sprite->y=passenger->y+12;
 sprite->x2=passenger->x2;sprite->y2=passenger->y2;
 sprite->coordOffsetEnabled=passenger->coordOffsetEnabled;
 sprite->oam.priority=passenger->oam.priority;
 sprite->subpriority=passenger->subpriority+1;
 // Movement still advances coordinates/camera, but the passenger stands still.
 StartSpriteAnim(passenger,GetFaceDirectionAnimNum(player->facingDirection));
 passenger->animPaused=TRUE;
}
static const u32 sLaunchGfx[]=INCBIN_U32("graphics/havora_gym/launch.4bpp");
static const u16 sLaunchPal[]=INCBIN_U16("graphics/havora_gym/launch.gbapal");
#define LAUNCH_TAG 0x15F0
static const u32 sCargoGfx[]=INCBIN_U32("graphics/havora_gym/cargo.4bpp");
static const struct SpriteSheet sLaunchSheet[]={ {sLaunchGfx,sizeof(sLaunchGfx),LAUNCH_TAG}, {sCargoGfx,sizeof(sCargoGfx),LAUNCH_TAG} };
static const struct SpritePalette sLaunchPalette={sLaunchPal,LAUNCH_TAG};
static const struct OamData sLaunchOam={.shape=SPRITE_SHAPE(64x64),.size=SPRITE_SIZE(64x64),.priority=2};
static const struct SpriteTemplate sLaunchTemplate={
 .tileTag=LAUNCH_TAG,.paletteTag=LAUNCH_TAG,.oam=&sLaunchOam,
 .anims=gDummySpriteAnimTable,.images=NULL,.affineAnims=gDummySpriteAffineAnimTable,.callback=LaunchPassenger
};
// State is versioned; existing victories and crest flags are independent.
#define VERSION 0x8000
static const u16 sLockBase[]=INCBIN_U16("data/layouts/HavoraCaptainsTrial/base.bin");
static bool8 Here(void)
{
 return gSaveBlock1Ptr->location.mapGroup==MAP_GROUP(MAP_QUANTUM_HAVORA_GYM)&&gSaveBlock1Ptr->location.mapNum==MAP_NUM(MAP_QUANTUM_HAVORA_GYM);
}
static u8 Water(u8 ch){u16 n=VarGet(VAR_HAVORA_GYM_STATE)&31;while(ch--)n/=3;return n%3;}
static u8 Boat(u8 b){return (VarGet(VAR_HAVORA_GYM_STATE)>>(b?8:5))&7;}
static u8 Moor(void){return (VarGet(VAR_HAVORA_GYM_STATE)>>11)&3;}
static bool8 Released(void){return !!(VarGet(VAR_HAVORA_GYM_STATE)&0x2000);}
static void SetBoat(u8 b,u8 n)
{
 u16 s=VarGet(VAR_HAVORA_GYM_STATE),shift=b?8:5;s=(s&~(7<<shift))|(n<<shift);VarSet(VAR_HAVORA_GYM_STATE,s);
}
static void SetWater(u8 src,u8 dst)
{
 u8 w[3]={Water(0),Water(1),Water(2)};u16 s=VarGet(VAR_HAVORA_GYM_STATE);w[src]--;w[dst]++;
 VarSet(VAR_HAVORA_GYM_STATE,(s&~31)|(w[0]+3*w[1]+9*w[2]));
}
static void SetMoor(u8 m){VarSet(VAR_HAVORA_GYM_STATE,(VarGet(VAR_HAVORA_GYM_STATE)&~0x1800)|(m<<11));}
static void ResetLock(void){VarSet(VAR_HAVORA_GYM_STATE,VERSION|8|(4<<8));}
static bool8 Valid(void)
{
 u16 s=VarGet(VAR_HAVORA_GYM_STATE);
 return (s&VERSION)&&(s&31)<27&&Water(0)+Water(1)+Water(2)==4&&Boat(0)<6&&Boat(1)<6&&Moor()<3;
}
static u8 Node(s16 x,s16 y)
{
 u8 n;
 if(x>=40&&x<=43&&y>=21&&y<=25)return 6;
 if(x>=65&&x<=69&&y>=22&&y<=25)return 7;
 for(n=0;n<6;n++)if(x>=sBank[n]&&x<sBank[n]+5&&y>=11&&y<=40)return n;
 if(x>=1&&x<=5&&y>=41&&y<=50)return 0;
 return 255;
}
static void Tile(s16 x,s16 y,u16 tile,bool8 blocked,u8 z){MapGridSetMetatileEntryAt(x+MAP_OFFSET,y+MAP_OFFSET,tile|(blocked?0x400:0)|(z<<12));}
static void Rect(u8 x,u8 y,u8 w,u8 h,u16 t,bool8 b,u8 z){u8 xx,yy;for(yy=y;yy<y+h;yy++)for(xx=x;xx<x+w;xx++)Tile(xx,yy,t,b,z);}
static void Line(u8 x,u8 y,u8 xx,u8 yy,u16 t,u8 z)
{
 s8 dx=x<xx?1:x>xx?-1:0,dy=y<yy?1:y>yy?-1:0;
 while(TRUE){Tile(x,y,t,FALSE,z);if(x==xx&&y==yy)break;x+=dx;y+=dy;}
}
static void Draw(bool8 redraw)
{
 u8 x,y,n,b,ch,tid=FindTaskIdByFunc(MoveBoat),m=Moor();
 bool8 transfer=tid!=TASK_NONE&&gTasks[tid].data[0]==2;
 bool8 occupied=tid!=TASK_NONE&&gTasks[tid].data[0]==1&&gTasks[tid].data[7];
 s16 surface[3], deckCut[3];
 for(y=0;y<LOCK_HEIGHT;y++)for(x=0;x<LOCK_WIDTH;x++)MapGridSetMetatileEntryAt(x+7,y+7,sLockBase[y*LOCK_WIDTH+x]);
 for(ch=0;ch<3;ch++)
 {
  u8 w=Water(ch);surface[ch]=33-8*w;
  if(transfer){if(ch==gTasks[tid].data[1])surface[ch]+=gTasks[tid].data[3];if(ch==gTasks[tid].data[2])surface[ch]-=gTasks[tid].data[3];}
  // Deck flooding follows the same transfer phase as the moving waterline.
  deckCut[ch]=w==0?41:w==1?32:24;
  if(transfer&&(ch==gTasks[tid].data[1]||ch==gTasks[tid].data[2]))
  {
   s16 target=w+(ch==gTasks[tid].data[1]?-1:1);
   target=target==0?41:target==1?32:24;
   deckCut[ch]+=(target-deckCut[ch])*gTasks[tid].data[3]/8;
  }
  Rect(sPoolX[ch],17,sPoolWidth[ch],27,0x282,TRUE,3+2*w);
  // Fixed basin: expose only a shallow rear retaining face.
  if(surface[ch]>17)Rect(sPoolX[ch],17,sPoolWidth[ch],(surface[ch]-17)/8,0x380,TRUE,1);
  Rect(sPoolX[ch],17+(surface[ch]-17)/8,sPoolWidth[ch],1,0x381,TRUE,1);
 }
 for(y=21;y<26;y++)for(x=39;x<45;x++)MapGridSetMetatileEntryAt(x+7,y+7,sLockBase[y*LOCK_WIDTH+x]);
 for(y=21;y<26;y++)for(x=64;x<71;x++)MapGridSetMetatileEntryAt(x+7,y+7,sLockBase[y*LOCK_WIDTH+x]);
 Tile(41,25,0x302,TRUE,5);
 for(y=24;y<26;y++)if(y>=deckCut[1])Rect(40,y,3,1,0x282,TRUE,1);
 // Lower decks and the submerged ladder sections vanish beneath the tide.
 for(n=0;n<6;n++)
 {
  u8 w=Water(n/2),cut=deckCut[n/2];
  if(cut<41)Rect(sBank[n],cut,5,41-cut,0x282,TRUE,1);
  Rect(sStair[n],15,1,n==0?35:24,0x281,FALSE,0);
  for(y=16;y<=32;y+=8)Tile(sStair[n],y,0x386,FALSE,0);
  Tile(sBank[n]+((n==0||n==1||n==2||n==5)?4:1),14,w==0?0x376:w==1?0x387:0x377,TRUE,9);
  for(ch=0;ch<3;ch++)for(b=0;b<2;b++)
  {
   y=sWaterRow[ch]+3*b;
   if(y>=cut)Tile(sShore[n],y,0x282,TRUE,1);
   else Tile(sShore[n],y,(sDockMask[n]&(1<<ch))?(sBankDirection[n]>0?0x370:0x372):0x385,!(sDockMask[n]&(1<<ch)),3+ch*2);
  }
 }
 // Canal gates are shut while the paired chambers transfer water.
 Rect(22,42,11,1,!transfer&&Water(0)==Water(1)?0x282:0x385,TRUE,3+2*Water(0));
 Rect(49,42,11,1,!transfer&&Water(1)==Water(2)?0x282:0x385,TRUE,3+2*Water(1));
 if(Water(0)==0&&!transfer)Line(5,32,22,32,0x280,3);
 if(Water(2)==0&&!transfer)Line(59,32,74,32,0x280,3);
 if(Water(0)==1&&Water(1)==1&&!transfer)Line(26,28,28,28,0x318,5);
 if(Water(1)==1&&Water(2)==1&&!transfer)
 {
  Line(30,13,30,10,0x318,9);Line(30,10,76,10,0x318,9);Line(76,10,76,13,0x318,9);
 }
 for(b=0;b<2;b++)
 {
  u8 berth=Boat(b);s16 bx=sShore[berth]+2*sBankDirection[berth],by=surface[berth/2]+2+3*b;
  if(occupied&&gTasks[tid].data[1]==b)continue;
  for(y=0;y<3;y++)for(x=0;x<3;x++)Tile(bx+x-1,by+y-1,(b?0x390:0x2bc)+y*3+x,TRUE,3+2*Water(berth/2));
 }
 // These overlays make the secured cargo deck walkable rather than colliding.
 if(m==1&&Boat(1)==3&&Water(1)==2&&!transfer){Line(49,22,43,22,0x318,7);Tile(43,22,0x386,FALSE,0);}
 if(m==2&&Boat(1)==5&&Water(1)==2&&Water(2)==2&&!transfer){Line(53,22,64,22,0x318,7);Tile(64,22,0x386,FALSE,0);}
 // Finish the deck edges after landing/bridge overlays, without blocking them.
 for(n=0;n<6;n++)for(y=17;y<41;y++)
 {
  x=sShore[n];
  if(MapGridGetMetatileIdAt(x+MAP_OFFSET,y+MAP_OFFSET)==0x281)
   Tile(x,y,sBankDirection[n]>0?0x3b2:0x3b3,FALSE,MapGridGetElevationAt(x+MAP_OFFSET,y+MAP_OFFSET));
 }
 // Animate only the lever the player used, preserving its collision/elevation.
 if(tid!=TASK_NONE&&gTasks[tid].data[10])
 {
  struct Task *t=&gTasks[tid];
  static const u8 frames[]={1,0,0,1,2,2,1,1};
  u8 frame=frames[t->data[3]&7];
  u8 elevation=MapGridGetElevationAt(t->data[8]+MAP_OFFSET,t->data[9]+MAP_OFFSET);
  Tile(t->data[8],t->data[9],0x3a0+(t->data[10]-0x300)*3+frame,TRUE,elevation);
 }
 if(redraw)DrawWholeMapView();
}
void HavoraGym_OnLoad(void)
{
 if(!Here())return;
 if(!Valid()){ResetLock();gSaveBlock1Ptr->pos.x=3;gSaveBlock1Ptr->pos.y=48;}
 Draw(FALSE);
}
void HavoraGym_OnResume(void){if(Here()){if(!Valid())ResetLock();Draw(TRUE);}}
static void Finish(u8 id)
{
 if(gTasks[id].data[6])DestroySpriteAndFreeResources(&gSprites[gTasks[id].data[6]-1]);
 gSprites[gObjectEvents[gPlayerAvatar.objectEventId].spriteId].animPaused=FALSE;
 gPlayerAvatar.preventStep=FALSE;UnfreezeObjectEvents();UnlockPlayerFieldControls();DestroyTask(id);Draw(TRUE);ScriptContext_Enable();
}
static void Waypoint(struct Task *t,s16 *x,s16 *y)
{
 u8 boat=t->data[1],src=t->data[2],dst=t->data[3],phase=t->data[4];
 u8 sr=sWaterRow[Water(src/2)]+boat*3,dr=sWaterRow[Water(dst/2)]+boat*3;
 s16 sx=sShore[src]+2*sBankDirection[src],dx=sShore[dst]+2*sBankDirection[dst];
 bool8 ss=boat&&Water(src/2)==2&&(src==3||src==5),ds=boat&&Water(dst/2)==2&&(dst==3||dst==5);
 *x=sx;*y=sr;
 if(phase==0)return;
 if(phase==1){*x=ss?sx:sCoreX[src/2];*y=ss?29:sr;return;}
 if(phase==2){*x=sCoreX[src/2];*y=ss?29:sr;return;}
 if(phase==3){*x=sCoreX[src/2];*y=42;return;}
 if(phase==4){*x=sCoreX[dst/2];*y=42;return;}
 if(phase==5){*x=sCoreX[dst/2];*y=ds?29:dr;return;}
 if(phase==6){*x=dx;*y=ds?29:dr;return;}
 if(phase==7){*x=dx;*y=dr;return;}
 *x=sShore[dst];*y=dr;
}
static void MoveBoat(u8 id)
{
 struct Task *t=&gTasks[id];struct ObjectEvent *p=&gObjectEvents[gPlayerAvatar.objectEventId];
 if(!Here()){Finish(id);return;}
 if(t->data[0]==3)
 {
  if(++t->data[5]<8)return;
  t->data[5]=0;
  if(++t->data[3]==8)Finish(id);else Draw(TRUE);
  return;
 }
 if(t->data[0]==2)
 {
  if(++t->data[5]<12)return;t->data[5]=0;t->data[3]++;
  if(t->data[3]==8){SetWater(t->data[1],t->data[2]);Finish(id);}else Draw(TRUE);
  return;
 }
 if(t->data[5])
 {
  if(!ObjectEventCheckHeldMovementStatus(p))return;
  ObjectEventClearHeldMovementIfFinished(p);t->data[5]=0;
 }
 while(t->data[4]<=8)
 {
  s16 x=p->currentCoords.x-7,y=p->currentCoords.y-7,tx,ty;u8 direction;
  Waypoint(t,&tx,&ty);
  if(x==tx&&y==ty)
  {
   if(t->data[4]==0){t->data[7]=1;gSprites[t->data[6]-1].data[0]=1;Draw(TRUE);}
   if(t->data[4]==7){t->data[7]=0;gSprites[t->data[6]-1].data[0]=0;SetBoat(t->data[1],t->data[3]);Draw(TRUE);}
   t->data[4]++;continue;
  }
  direction=x<tx?DIR_EAST:x>tx?DIR_WEST:y<ty?DIR_SOUTH:DIR_NORTH;
  ObjectEventSetHeldMovement(p,GetWalkNormalMovementAction(direction));t->data[5]=1;return;
 }
 Finish(id);
}
static bool8 Start(u8 mode,u8 a,u8 b,u8 c)
{
 u8 id=CreateTask(MoveBoat,80),sid;
 if(id==TASK_NONE)return FALSE;
 gTasks[id].data[0]=mode;gTasks[id].data[1]=a;gTasks[id].data[2]=b;gTasks[id].data[3]=c;
 if(mode==1)
 {
  if(LoadSpriteSheet(&sLaunchSheet[a])==0xFFFF||LoadSpritePalette(&sLaunchPalette)==0xFF)goto failed;
  sid=CreateSprite(&sLaunchTemplate,0,0,0);if(sid==MAX_SPRITES)goto failed;
  gTasks[id].data[6]=sid+1;gSprites[sid].invisible=TRUE;
 }
 if(mode!=1)
 {
  struct ObjectEvent *p=&gObjectEvents[gPlayerAvatar.objectEventId];
  s16 px=p->currentCoords.x-MAP_OFFSET,py=p->currentCoords.y-MAP_OFFSET;
  u8 i; s16 best=3;
  for(i=0;i<ARRAY_COUNT(sLockControls);i++)
  {
   const u8 *control=sLockControls[i];
   s16 distance=abs(control[0]-px)+abs(control[1]-py);
   bool8 matches=mode==2 ? control[2]==10&&control[3]==a&&control[4]==b : control[2]==a;
   if(matches&&distance<best)
   {
    best=distance;gTasks[id].data[8]=control[0];gTasks[id].data[9]=control[1];
    gTasks[id].data[10]=MapGridGetMetatileIdAt(control[0]+MAP_OFFSET,control[1]+MAP_OFFSET);
   }
  }
  PlaySE(SE_SWITCH);
 }
 LockPlayerFieldControls();FreezeObjectEvents();gPlayerAvatar.preventStep=TRUE;Draw(TRUE);return TRUE;
failed:
 FreeSpriteTilesByTag(LAUNCH_TAG);FreeSpritePaletteByTag(LAUNCH_TAG);DestroyTask(id);return FALSE;
}
static bool8 CanReach(u8 src,u8 dst)
{
 u8 a=src/2,b=dst/2,i;
 if(!(sDockMask[dst]&(1<<Water(b))))return FALSE;
 for(i=a<b?a:b;i<(a>b?a:b);i++)if(Water(i)!=Water(i+1))return FALSE;
 return TRUE;
}
static bool8 AtDock(u8 boat,u8 node,s16 x,s16 y)
{
 return node<6&&boat<2&&Boat(boat)==node&&x==sShore[node]&&y==sWaterRow[Water(node/2)]+boat*3&&(sDockMask[node]&(1<<Water(node/2)))&&!(boat&&Moor());
}
static const u8 sADock[] = _("A WEST QUAY");static const u8 sAInner[] = _("A INNER LANDING");
static const u8 sBDock[] = _("B WEST QUAY");static const u8 sBUpper[] = _("B SERVICE BERTH");
static const u8 sCDock[] = _("C CONTROL QUAY");static const u8 sCOuter[] = _("C OUTER MOORING");
static const struct MenuAction sBerths[]={{sADock},{sAInner},{sBDock},{sBUpper},{sCDock},{sCOuter}};
static const u8 sLow[] = _("LOW");static const u8 sMid[] = _("MID");static const u8 sHigh[] = _("HIGH");
static const u8 *const sLevels[]={sLow,sMid,sHigh};
static const u8 sA[] = _("A ");static const u8 sB[] = _("  B ");static const u8 sC[] = _("\nC ");
void HavoraGym_Control(void)
{
 struct ObjectEvent *p=&gObjectEvents[gPlayerAvatar.objectEventId];s16 x=p->currentCoords.x-7,y=p->currentCoords.y-7;
 u8 node=Node(x,y),cmd=gSpecialVar_0x8004,a=gSpecialVar_0x8005,b=gSpecialVar_0x8006;
 u16 progress=VarGet(VAR_HAVORA_GYM_PROGRESS),s=VarGet(VAR_HAVORA_GYM_STATE);
 gSpecialVar_Result=0;if(!Here())return;if(!Valid())ResetLock();
 if(FindTaskIdByFunc(MoveBoat)!=TASK_NONE){gSpecialVar_Result=4;return;}
 if(cmd==6){if(progress&4)VarSet(VAR_VIDRA_CRESTS,VarGet(VAR_VIDRA_CRESTS)|1);Draw(TRUE);return;}
 if(cmd==21)
 {
  StringCopy(gStringVar1,sA);StringAppend(gStringVar1,sLevels[Water(0)]);StringAppend(gStringVar1,sB);StringAppend(gStringVar1,sLevels[Water(1)]);StringAppend(gStringVar1,sC);StringAppend(gStringVar1,sLevels[Water(2)]);return;
 }
 if(cmd==10)
 {
  bool8 ab=(a==0&&b==1)||(a==1&&b==0),bc=(a==1&&b==2)||(a==2&&b==1);
  if(node==2&&!(progress&1)){gSpecialVar_Result=2;return;}
  if(node==4&&!(progress&2)){gSpecialVar_Result=6;return;}
  if(!((ab&&(node==0||node==1||node==4))||(bc&&(node==2||node==4||node==5||node==6)))){gSpecialVar_Result=3;return;}
  if(!Water(a)||Water(b)==2){gSpecialVar_Result=7;return;}
  gSpecialVar_Result=Start(2,a,b,0)?1:4;return;
 }
 if(cmd==20||cmd==11)
 {
  if(!AtDock(a,node,x,y)){gSpecialVar_Result=5;return;}
  if(cmd==20){DrawMultichoiceMenuInternal(0,0,0,FALSE,0,sBerths,6);gSpecialVar_Result=1;return;}
  if(b>=6||b==node||!CanReach(node,b)){gSpecialVar_Result=3;return;}
  gSpecialVar_Result=Start(1,a,node,b)?1:4;return;
 }
 if(cmd==12)
 {
  if(node!=3||Boat(1)!=3||Water(1)!=2||Moor()==2){gSpecialVar_Result=8;return;}
  if(!Start(3,cmd,0,0)){gSpecialVar_Result=4;return;}
  SetMoor(Moor()==1?0:1);Draw(TRUE);gSpecialVar_Result=1;return;
 }
 if(cmd==13)
 {
  if(node!=6||Water(1)==2){gSpecialVar_Result=8;return;}
  if(!Start(3,cmd,0,0)){gSpecialVar_Result=4;return;}
  VarSet(VAR_HAVORA_GYM_STATE,s|0x2000);Draw(TRUE);gSpecialVar_Result=1;return;
 }
 if(cmd==14)
 {
  if(node!=4||Boat(1)!=5||Water(1)!=2||Water(2)!=2||!Released()||Moor()!=0){gSpecialVar_Result=8;return;}
  if(!Start(3,cmd,0,0)){gSpecialVar_Result=4;return;}
  SetMoor(2);Draw(TRUE);gSpecialVar_Result=1;return;
 }
 if(cmd==15)
 {
  if(!Start(3,cmd,0,0)){gSpecialVar_Result=4;return;}
  ResetLock();Draw(TRUE);gSpecialVar_Result=1;return;
 }
 gSpecialVar_Result=3;
}
