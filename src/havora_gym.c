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
#include "malloc.h"
#include "sound.h"
#include "string_util.h"
#include "pokemon.h"
#include "script_pokemon_util.h"
#include "constants/songs.h"
#include "constants/maps.h"
#include "constants/vars.h"
#include "constants/flags.h"
#include "data/havora_lock_geometry.h"
#include "data/havora_tidal_trial.h"

static void MoveBoat(u8 id);
static void LaunchPassenger(struct Sprite *sprite)
{
 struct ObjectEvent *player=&gObjectEvents[gPlayerAvatar.objectEventId];
 struct Sprite *passenger=&gSprites[player->spriteId];
 sprite->invisible=FALSE;
 if(!sprite->data[0])
 {
  SetSpritePosToMapCoords(sprite->data[1]+MAP_OFFSET,sprite->data[2]+MAP_OFFSET,&sprite->x,&sprite->y);
  sprite->x+=8;sprite->y+=12;sprite->x2=0;sprite->y2=0;
  sprite->coordOffsetEnabled=TRUE;sprite->oam.priority=passenger->oam.priority;
  sprite->subpriority=passenger->subpriority+1;return;
 }
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
// The old conserved-water / cargo-boat state is deliberately not reused.
#define VERSION 0x8000
#define ALL_CREWS 251
#define ALL_SWITCHES 127
static const u16 sLockBase[]=INCBIN_U16("data/layouts/Havora_Gym/map.bin");
static void AnimateTide(u8 id);
static bool8 Here(void)
{
 return gSaveBlock1Ptr->location.mapGroup==MAP_GROUP(MAP_HAVORA_GYM)
     &&gSaveBlock1Ptr->location.mapNum==MAP_NUM(MAP_HAVORA_GYM);
}
static bool8 Valid(void)
{
 u16 s=VarGet(VAR_HAVORA_GYM_STATE);
 return (s&~31)==VERSION&&(s&31)<27;
}
static u8 Water(u8 section)
{
 u16 n=VarGet(VAR_HAVORA_GYM_STATE)&31;
 while(section--)n/=3;
 return n%3;
}
static u8 CountBits(u16 n)
{
 u8 count=0;
 while(n){count+=n&1;n>>=1;}
 return count;
}
static void SetVisibility(u8 localId,u16 flag,bool8 hidden,bool8 objectsReady)
{
 if(hidden)
 {
  FlagSet(flag);
  RemoveObjectEventByLocalIdAndMap(localId,MAP_NUM(MAP_HAVORA_GYM),MAP_GROUP(MAP_HAVORA_GYM));
 }
 else
 {
  FlagClear(flag);
  if(objectsReady&&GetObjectEventIdByLocalIdAndMap(localId,MAP_NUM(MAP_HAVORA_GYM),MAP_GROUP(MAP_HAVORA_GYM))==OBJECT_EVENTS_COUNT)
   TrySpawnObjectEvent(localId,MAP_NUM(MAP_HAVORA_GYM),MAP_GROUP(MAP_HAVORA_GYM));
 }
}
// Hide people before their floor floods; spawn them after it is exposed.
static void UpdateWaterOcclusion(u8 taskId,bool8 ready)
{
 bool8 captain=Water(2)!=0,island=Water(1)==2,steward=Water(0)!=0;
 if(taskId!=TASK_NONE&&gTasks[taskId].data[3]>0)
 {
  u8 next=gTasks[taskId].data[1];
  if(next/9)captain=TRUE;
  if(next%3)steward=TRUE;
  if(next/3%3==2)island=TRUE;
 }
 SetVisibility(TIDAL_STEWARD_LOCAL_ID,FLAG_TEMP_1D,steward,ready);
 SetVisibility(LOCK_CAPTAIN_LOCAL_ID,FLAG_TEMP_1F,captain,ready);
 SetVisibility(TIDAL_ISLAND_LOCAL_ID,FLAG_TEMP_1E,island,ready);
}
static void Draw(bool8 redraw)
{
 u8 tid=FindTaskIdByFunc(AnimateTide);
 u16 state=VarGet(VAR_HAVORA_GYM_STATE)&31;
 u16 oldIndex=sLockMapOffsets[state],newIndex=oldIndex,baseIndex=sLockMapOffsets[0];
 u16 left=0,nextLeft=0,baseLeft=0,tile=0,nextTile=0,baseTile=0,i;
 if(tid!=TASK_NONE)newIndex=sLockMapOffsets[gTasks[tid].data[1]];
 for(i=0;i<LOCK_WIDTH*LOCK_HEIGHT;i++)
 {
  u16 oldArt,newArt;u8 x=i%LOCK_WIDTH,y=i/LOCK_WIDTH;
  if(!left){left=sLockMapRuns[oldIndex].count;tile=sLockMapRuns[oldIndex++].tile;}left--;
  if(!nextLeft){nextLeft=sLockMapRuns[newIndex].count;nextTile=sLockMapRuns[newIndex++].tile;}nextLeft--;
  if(!baseLeft){baseLeft=sLockMapRuns[baseIndex].count;baseTile=sLockMapRuns[baseIndex++].tile;}baseLeft--;
  oldArt=tile==baseTile?sLockBase[i]:tile;
  newArt=nextTile==baseTile?sLockBase[i]:nextTile;
  if(FindTaskIdByFunc(MoveBoat)!=TASK_NONE)
  {
   u16 a=oldArt&1023,b=newArt&1023;
   if((a>=0x2bc&&a<=0x2c4)||(a>=0x390&&a<=0x398))oldArt=0x1682;
   if((b>=0x2bc&&b<=0x2c4)||(b>=0x390&&b<=0x398))newArt=0x1682;
  }
  MapGridSetMetatileEntryAt(x+MAP_OFFSET,y+MAP_OFFSET,tid!=TASK_NONE&&gTasks[tid].data[3]>=1+x%7?newArt:oldArt);
 }
 UpdateWaterOcclusion(tid,redraw);
 if(redraw)
 {
  u8 objectId;
  // Tide profiles change floor elevation under stationary island occupants.
  // Refresh cached elevations before movement collision is checked again.
  for(objectId=0;objectId<OBJECT_EVENTS_COUNT;objectId++)
   if(gObjectEvents[objectId].active)
    ObjectEventUpdateElevation(&gObjectEvents[objectId],&gSprites[gObjectEvents[objectId].spriteId]);
  DrawWholeMapView();
 }
}
void HavoraGym_OnLoad(void)
{
 if(!Here())return;
 if(VarGet(VAR_HAVORA_GYM_PROGRESS)&4)
 {
  VarSet(VAR_HAVORA_GYM_PROGRESS,255);
  VarSet(VAR_HAVORA_GYM_SWITCHES,ALL_SWITCHES);
 }
 if(!Valid())
 {
  VarSet(VAR_HAVORA_GYM_STATE,VERSION);
  gSaveBlock1Ptr->pos.x=LOCK_ENTRY_X;gSaveBlock1Ptr->pos.y=LOCK_ENTRY_Y;
 }
 if(gSaveBlock1Ptr->pos.x>=LOCK_WIDTH||gSaveBlock1Ptr->pos.y>=LOCK_HEIGHT)
 {
  gSaveBlock1Ptr->pos.x=LOCK_ENTRY_X;gSaveBlock1Ptr->pos.y=LOCK_ENTRY_Y;
 }
 Draw(FALSE);
}
void HavoraGym_OnResume(void)
{
 if(Here()){if(!Valid())VarSet(VAR_HAVORA_GYM_STATE,VERSION);Draw(TRUE);}
}
static void AnimateTide(u8 id)
{
 struct Task *t=&gTasks[id];
 if(++t->data[5]<12)return;
 t->data[5]=0;
 if(++t->data[3]==8)
 {
  VarSet(VAR_HAVORA_GYM_STATE,VERSION|t->data[1]);
  gPlayerAvatar.preventStep=FALSE;
  UnfreezeObjectEvents();UnlockPlayerFieldControls();DestroyTask(id);
  Draw(TRUE);ScriptContext_Enable();
 }
 else Draw(TRUE);
}
static bool8 StartTide(u8 next)
{
 u8 id=CreateTask(AnimateTide,80);
 if(id==TASK_NONE)return FALSE;
 gTasks[id].data[1]=next;
 PlaySE(SE_SWITCH);LockPlayerFieldControls();FreezeObjectEvents();gPlayerAvatar.preventStep=TRUE;
 Draw(TRUE);return TRUE;
}
static bool8 BoatWater(s16 x,s16 y)
{
 // A's submerged face can be invisible while B remains at a different level.
 // Visual coverage does not permit sailing across an unequal-level dam.
 if(x==27&&!(Water(0)==Water(1)&&Water(0)>0))return FALSE;
 if(x==54&&!(Water(1)==2&&Water(2)==2))return FALSE;
 u16 tile=MapGridGetMetatileIdAt(x+MAP_OFFSET,y+MAP_OFFSET);
 return tile==0x282||(tile>=0x2bc&&tile<=0x2c4)||(tile>=0x390&&tile<=0x398);
}
static bool8 BoatClear(s16 x,s16 y)
{
 s16 xx,yy;
 if(x<1||y<1||x>=LOCK_WIDTH-1||y>=LOCK_HEIGHT-1)return FALSE;
 for(yy=y-1;yy<=y+1;yy++)for(xx=x-1;xx<=x+1;xx++)if(!BoatWater(xx,yy))return FALSE;
 return TRUE;
}
static void EndBoat(u8 id)
{
 struct ObjectEvent *p=&gObjectEvents[gPlayerAvatar.objectEventId];
 Free((void *)GetWordTaskArg(id,11));
 DestroySpriteAndFreeResources(&gSprites[gTasks[id].data[8]]);
 gSprites[p->spriteId].animPaused=FALSE;
 ObjectEventUpdateElevation(p,&gSprites[p->spriteId]);
 gPlayerAvatar.preventStep=FALSE;UnfreezeObjectEvents();UnlockPlayerFieldControls();
 DestroyTask(id);Draw(TRUE);ScriptContext_Enable();
}
static void MoveBoat(u8 id)
{
 struct Task *t=&gTasks[id];struct ObjectEvent *p=&gObjectEvents[gPlayerAvatar.objectEventId];
 s16 x,y,tx,ty;u8 direction;
 if(t->data[7])
 {
  if(!ObjectEventCheckHeldMovementStatus(p))return;
  ObjectEventClearHeldMovementIfFinished(p);t->data[7]=0;
 }
 for(;;)
 {
  x=p->currentCoords.x-MAP_OFFSET;y=p->currentCoords.y-MAP_OFFSET;
  if(t->data[0]==0){tx=t->data[3];ty=t->data[4];}
  else if(t->data[0]==1)
  {
   u16 cell=((u16 *)GetWordTaskArg(id,11))[t->data[1]];
   tx=cell%LOCK_WIDTH;ty=cell/LOCK_WIDTH;
  }
  else {tx=t->data[5];ty=t->data[6];}
  if(x==tx&&y==ty)
  {
   if(t->data[0]==0){t->data[0]=1;gSprites[t->data[8]].data[0]=1;continue;}
   if(t->data[0]==1)
   {
    if(++t->data[1]<t->data[2])continue;
    t->data[0]=2;gSprites[t->data[8]].data[1]=x;gSprites[t->data[8]].data[2]=y;gSprites[t->data[8]].data[0]=0;gSprites[p->spriteId].animPaused=FALSE;continue;
   }
   EndBoat(id);return;
  }
  direction=x<tx?DIR_EAST:x>tx?DIR_WEST:y<ty?DIR_SOUTH:DIR_NORTH;
  if(t->data[0]==1)
  {
   u8 matrix=gSprites[t->data[8]].oam.matrixNum;
   if(direction==DIR_NORTH)SetOamMatrix(matrix,0,256,-256,0);
   else if(direction==DIR_SOUTH)SetOamMatrix(matrix,0,-256,256,0);
   else if(direction==DIR_WEST)SetOamMatrix(matrix,-256,0,0,-256);
   else SetOamMatrix(matrix,256,0,0,256);
  }
  ObjectEventSetHeldMovement(p,GetWalkNormalMovementAction(direction));t->data[7]=1;return;
 }
}
static bool8 StartBoat(const u8 *source,const u8 *destination)
{
 const u16 cells=LOCK_WIDTH*LOCK_HEIGHT;
 u8 *previous=AllocZeroed(cells);u16 *queue=Alloc(cells*sizeof(u16)),*path=NULL;
 u16 head=0,tail=0,start,goal,at,count=0,i;u8 id=TASK_NONE,sid=MAX_SPRITES,matrix=0xFF;
 s16 sx=source[0],sy=source[1],dx=destination[0],dy=destination[1];
 static const s8 ox[]={0,-1,1,0,0},oy[]={0,0,0,-1,1};
 if(!previous||!queue)goto failed;
 sx+=MapGridGetMetatileIdAt(sx+MAP_OFFSET,sy+MAP_OFFSET)==0x370?4:-4;
 dx+=MapGridGetMetatileIdAt(dx+MAP_OFFSET,dy+MAP_OFFSET)==0x370?4:-4;
 start=sy*LOCK_WIDTH+sx;goal=dy*LOCK_WIDTH+dx;
 if(!BoatClear(sx,sy)||!BoatClear(dx,dy))goto failed;
 queue[tail++]=start;previous[start]=255;
 while(head<tail&&!previous[goal])
 {
  at=queue[head++];
  for(i=1;i<=4;i++)
  {
   s16 x=at%LOCK_WIDTH+ox[i],y=at/LOCK_WIDTH+oy[i];u16 next=y*LOCK_WIDTH+x;
   if(x<1||y<1||x>=LOCK_WIDTH-1||y>=LOCK_HEIGHT-1||previous[next]||!BoatClear(x,y))continue;
   previous[next]=i;queue[tail++]=next;
  }
 }
 if(!previous[goal])goto failed;
 for(at=goal;at!=start;at-=oy[previous[at]]*LOCK_WIDTH+ox[previous[at]])count++;
 count++;path=Alloc(count*sizeof(u16));if(!path)goto failed;
 at=goal;
 for(i=count;i;i--){path[i-1]=at;if(at!=start)at-=oy[previous[at]]*LOCK_WIDTH+ox[previous[at]];}
 Free(previous);previous=NULL;Free(queue);queue=NULL;
 id=CreateTask(MoveBoat,80);if(id==TASK_NONE)goto failed;
 if(LoadSpriteSheet(&sLaunchSheet[0])==0xFFFF||LoadSpritePalette(&sLaunchPalette)==0xFF)goto failed;
 sid=CreateSprite(&sLaunchTemplate,0,0,0);if(sid==MAX_SPRITES)goto failed;
 matrix=AllocOamMatrix();if(matrix==0xFF)goto failed;
 gSprites[sid].oam.affineMode=ST_OAM_AFFINE_NORMAL;gSprites[sid].oam.matrixNum=matrix;
 SetOamMatrix(matrix,256,0,0,256);gSprites[sid].data[1]=sx;gSprites[sid].data[2]=sy;
 gTasks[id].data[2]=count;gTasks[id].data[3]=sx;gTasks[id].data[4]=sy;
 gTasks[id].data[5]=destination[0];gTasks[id].data[6]=destination[1];gTasks[id].data[8]=sid;
 SetWordTaskArg(id,11,(u32)path);
 LockPlayerFieldControls();FreezeObjectEvents();gPlayerAvatar.preventStep=TRUE;PlaySE(SE_SELECT);Draw(TRUE);return TRUE;
failed:
 Free(previous);Free(queue);Free(path);
 if(sid!=MAX_SPRITES)DestroySprite(&gSprites[sid]);
 if(id!=TASK_NONE)DestroyTask(id);
 FreeSpriteTilesByTag(LAUNCH_TAG);FreeSpritePaletteByTag(LAUNCH_TAG);return FALSE;
}

static bool8 AtControl(u8 platform,u8 control,s16 x,s16 y)
{
 const u8 *p=sPlatforms[platform].controls[control];
 u16 tile=MapGridGetMetatileIdAt(p[0]+MAP_OFFSET,p[1]+MAP_OFFSET);
 return abs(x-p[0])+abs(y-p[1])==1&&tile>=0x300&&tile<=0x303;
}
static u8 Operate(u8 platform,u8 control,s16 x,s16 y)
{
 u8 w[3]={Water(0),Water(1),Water(2)},i,color;
 u16 tile;
 static const s8 effects[][3]={{-1,0,1},{1,1,-1},{0,1,0},{1,-1,-1}};
 if(platform>=ARRAY_COUNT(sPlatforms)||control>=3||!AtControl(platform,control,x,y))return 3;
 if(!(VarGet(VAR_HAVORA_GYM_PROGRESS)&sPlatforms[platform].victory))return 2;
 tile=MapGridGetMetatileIdAt(sPlatforms[platform].controls[control][0]+MAP_OFFSET,sPlatforms[platform].controls[control][1]+MAP_OFFSET);
 color=tile-0x300;
 for(i=0;i<3;i++)w[i]=(w[i]+effects[color][i]+3)%3;
 // Do not flood the player's island floor. Its LOW/MID floor remains safe.
 if(platform==6&&w[1]==2)return 7;
 if(!StartTide(w[0]+3*w[1]+9*w[2]))return 4;
 VarSet(VAR_HAVORA_GYM_SWITCHES,VarGet(VAR_HAVORA_GYM_SWITCHES)|(1<<platform));
 return 1;
}
static u8 Travel(s16 x,s16 y)
{
 u8 i,j;u16 progress=VarGet(VAR_HAVORA_GYM_PROGRESS);
 for(i=0;i<ARRAY_COUNT(sLinks);i++)
 {
  const struct TidalLink *link=&sLinks[i];
  bool8 forward=abs(x-link->source[0])+abs(y-link->source[1])<=1;

  const u8 *dest;
  if(!forward)continue;
  if((progress&link->clearance)!=link->clearance||!(VarGet(VAR_HAVORA_GYM_SWITCHES)&(1<<link->from)))return 2;
  for(j=0;j<3;j++)if(link->water[j]>=0&&Water(j)!=link->water[j])return 7;
  dest=link->destination;
  // The authored pad must actually be exposed, even if a script is invoked directly.
  if(MapGridGetCollisionAt(dest[0]+MAP_OFFSET,dest[1]+MAP_OFFSET))return 7;
  gSpecialVar_0x8008=dest[0];gSpecialVar_0x8009=dest[1];
  return StartBoat(link->source,dest)?1:7;
 }
 return 3;
}
static u8 CheckTrainer(u8 platform)
{
 if(platform>=ARRAY_COUNT(sPlatforms))return 3;
 return 1;
}
static const u8 sLow[] = _("LOW"),sMid[] = _("MID"),sHigh[] = _("HIGH");
static const u8 *const sLevels[]={sLow,sMid,sHigh};
static const u8 sA[] = _("A "),sB[] = _("  B "),sC[] = _("\nC ");
void HavoraGym_Control(void)
{
 u8 cmd=gSpecialVar_0x8004,a=gSpecialVar_0x8005,b=gSpecialVar_0x8006;
 u16 progress=VarGet(VAR_HAVORA_GYM_PROGRESS);
 struct ObjectEvent *player=&gObjectEvents[gPlayerAvatar.objectEventId];
 s16 x=player->currentCoords.x-MAP_OFFSET,y=player->currentCoords.y-MAP_OFFSET;
 gSpecialVar_Result=0;
 if(!Here())return;
 if(!Valid())VarSet(VAR_HAVORA_GYM_STATE,VERSION);
 if(FindTaskIdByFunc(AnimateTide)!=TASK_NONE||FindTaskIdByFunc(MoveBoat)!=TASK_NONE){gSpecialVar_Result=4;return;}
 if(cmd==30){gSpecialVar_Result=Operate(a,b,x,y);return;}
 if(cmd==31){gSpecialVar_Result=Travel(x,y);return;}
 if(cmd==32){gSpecialVar_Result=CheckTrainer(a);return;}
 if(cmd==22){VarSet(VAR_HAVORA_GYM_PROGRESS,progress|a);gSpecialVar_Result=1;return;}
 if(cmd==23){gSpecialVar_Result=(progress&a)==a;return;}
 if(cmd==24)
 {
  u8 i,count=0;
  if(progress&4){gSpecialVar_Result=1;return;}
  if((progress&ALL_CREWS)!=ALL_CREWS||(VarGet(VAR_HAVORA_GYM_SWITCHES)&ALL_SWITCHES)!=ALL_SWITCHES||Water(2)!=0){gSpecialVar_Result=2;return;}
  for(i=0;i<PARTY_SIZE;i++)if(GetMonData(&gPlayerParty[i],MON_DATA_SPECIES)&&!GetMonData(&gPlayerParty[i],MON_DATA_IS_EGG)&&GetMonData(&gPlayerParty[i],MON_DATA_HP))count++;
  gSpecialVar_Result=count==6?1:3;return;
 }
 if(cmd==25){HealPlayerParty();gSpecialVar_Result=1;return;}
 if(cmd==6){if(progress&4)VarSet(VAR_VIDRA_CRESTS,VarGet(VAR_VIDRA_CRESTS)|1);return;}
 if(cmd==21)
 {
  StringCopy(gStringVar1,sA);StringAppend(gStringVar1,sLevels[Water(0)]);
  StringAppend(gStringVar1,sB);StringAppend(gStringVar1,sLevels[Water(1)]);
  StringAppend(gStringVar1,sC);StringAppend(gStringVar1,sLevels[Water(2)]);
  ConvertIntToDecimalStringN(gStringVar2,CountBits(progress&ALL_CREWS),STR_CONV_MODE_LEFT_ALIGN,1);
  ConvertIntToDecimalStringN(gStringVar3,CountBits(VarGet(VAR_HAVORA_GYM_SWITCHES)&ALL_SWITCHES),STR_CONV_MODE_LEFT_ALIGN,1);return;
 }
 if(cmd==15){gSpecialVar_Result=StartTide(0)?1:4;return;}
 // Kept for artwork/emulator review only; no map event invokes command 26.
 if(cmd==26)
 {
  static const u8 weight[]={1,3,9};
  if(a>=3||b>=3){gSpecialVar_Result=3;return;}
  gSpecialVar_Result=StartTide((VarGet(VAR_HAVORA_GYM_STATE)&31)+weight[a]*(b-Water(a)))?1:4;return;
 }
 gSpecialVar_Result=3;
}
