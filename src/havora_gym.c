#include "global.h"
#include "event_data.h"
#include "event_object_movement.h"
#include "field_camera.h"
#include "field_player_avatar.h"
#include "fieldmap.h"
#include "overworld.h"
#include "script.h"
#include "task.h"
#include "constants/maps.h"
#include "constants/vars.h"

#define EAST 1
#define HIGH 2
#define GANGWAY 4
#define UPPER 8
static bool8 Here(void)
{
 return gSaveBlock1Ptr->location.mapGroup == MAP_GROUP(MAP_QUANTUM_HAVORA_GYM)
     && gSaveBlock1Ptr->location.mapNum == MAP_NUM(MAP_QUANTUM_HAVORA_GYM);
}
static void Tile(s16 x, s16 y, u16 id, bool8 block, u8 height)
{
 MapGridSetMetatileEntryAt(x + MAP_OFFSET, y + MAP_OFFSET, id | (block ? 0x400 : 0) | (height << 12));
}
static void Rect(u8 x, u8 y, u8 w, u8 h, u16 id, bool8 block, u8 height)
{
 u8 xx, yy;
 for (yy=y; yy<y+h; yy++) for (xx=x; xx<x+w; xx++) Tile(xx,yy,id,block,height);
}
static void Draw(s16 boatX, s16 boatY, bool8 redraw)
{
 u16 s=VarGet(VAR_HAVORA_GYM_STATE), p=VarGet(VAR_HAVORA_GYM_PROGRESS);
 u8 x,y;
 Rect(10,12,19,17,0x282,TRUE,1);
 // A timber divider separates the lower basin from the upper berth.
 Rect(10,19,16,1,0x304,TRUE,3);
 Rect(4,29,3,1,s&GANGWAY?0x281:0x282,!(s&GANGWAY),s&GANGWAY?3:1);
 Rect(4,9,3,3,s&UPPER?0x281:0x304,!(s&UPPER),3);
 Rect(33,9,3,3,p&4?0x281:0x304,!(p&4),3);
 Rect(33,29,3,1,p&4?0x281:0x304,!(p&4),3);
 // Native sailboat pixels; the boat sits below the passenger in this private pair.
 for(y=0;y<3;y++)for(x=0;x<3;x++)Tile(boatX+x-1,boatY+y-1,0x2bc+y*3+x,TRUE,3);
 if(redraw)DrawWholeMapView();
}
void HavoraGym_OnLoad(void)
{
 u16 s=VarGet(VAR_HAVORA_GYM_STATE);
 Draw(s&EAST?27:11,s&HIGH?14:26,FALSE);
}
void HavoraGym_OnResume(void)
{
 HavoraGym_OnLoad();DrawWholeMapView();
}
static void Finish(u8 id)
{
 gPlayerAvatar.preventStep=FALSE;
 UnfreezeObjectEvents();
 UnlockPlayerFieldControls();
 DestroyTask(id);
 ScriptContext_Enable();
}
static void MoveBoat(u8 id)
{
 struct Task *t=&gTasks[id];
 struct ObjectEvent *player=&gObjectEvents[gPlayerAvatar.objectEventId];
 if(!Here()){Finish(id);return;}
 if(t->data[0]==1)
 {
  s16 x=player->currentCoords.x-MAP_OFFSET;
  if(t->data[6])
  {
   if(!ObjectEventCheckHeldMovementStatus(player))return;
   ObjectEventClearHeldMovementIfFinished(player);
   t->data[6]=0;
   x=player->currentCoords.x-MAP_OFFSET;
   Draw(x<11?11:x>27?27:x,t->data[3],TRUE);
  }
  if(x==t->data[4]){Finish(id);return;}
  ObjectEventSetHeldMovement(player,GetWalkNormalMovementAction(x<t->data[4]?DIR_EAST:DIR_WEST));
  t->data[6]=1;
 }
 else
 {
  if(++t->data[7]<8)return;
  t->data[7]=0;
  if(t->data[0]==2)t->data[3]+=t->data[3]<t->data[5]?1:-1;
  else t->data[2]+=t->data[2]<t->data[4]?1:-1;
  Draw(t->data[2],t->data[3],TRUE);
  if((t->data[0]==2&&t->data[3]==t->data[5])||(t->data[0]==0&&t->data[2]==t->data[4]))Finish(id);
 }
}
static bool8 Start(u8 mode,s16 x,s16 y,s16 targetX,s16 targetY)
{
 u8 id=CreateTask(MoveBoat,80);
 if(id==TASK_NONE)return FALSE;
 gTasks[id].data[0]=mode;gTasks[id].data[2]=x;gTasks[id].data[3]=y;
 gTasks[id].data[4]=targetX;gTasks[id].data[5]=targetY;
 LockPlayerFieldControls();FreezeObjectEvents();gPlayerAvatar.preventStep=TRUE;
 return TRUE;
}
void HavoraGym_Control(void)
{
 u16 s=VarGet(VAR_HAVORA_GYM_STATE),p=VarGet(VAR_HAVORA_GYM_PROGRESS);
 struct ObjectEvent *player=&gObjectEvents[gPlayerAvatar.objectEventId];
 s16 x=player->currentCoords.x-MAP_OFFSET,y=player->currentCoords.y-MAP_OFFSET;
 s16 bx=s&EAST?27:11,by=s&HIGH?14:26;
 u8 command=gSpecialVar_0x8004;
 gSpecialVar_Result=0;
 if(!Here())return;
 if(command==7){gSpecialVar_Result=!!(s&HIGH);return;}
 if(command==1)s^=GANGWAY;
 else if(command==2)
 {
  if(!(p&1)){gSpecialVar_Result=2;return;}
  if(!(s&EAST)){gSpecialVar_Result=3;return;}
  if(!Start(2,bx,by,bx,s&HIGH?26:14)){gSpecialVar_Result=4;return;}
  s^=HIGH;VarSet(VAR_HAVORA_GYM_STATE,s);gSpecialVar_Result=1;return;
 }
 else if(command==3)
 {
  if(y!=by||(x!=9&&x!=29)){gSpecialVar_Result=5;return;}
  if((x==29)!=(bool8)(s&EAST))
  {
   if(!Start(0,bx,by,x==29?27:11,by)){gSpecialVar_Result=4;return;}
   s^=EAST;
  }
  else
  {
   if(!Start(1,bx,by,x==29?9:29,by)){gSpecialVar_Result=4;return;}
   s^=EAST;
  }
  VarSet(VAR_HAVORA_GYM_STATE,s);gSpecialVar_Result=1;return;
 }
 else if(command==4)
 {
  if(!(p&2)){gSpecialVar_Result=6;return;}
  s|=UPPER;
 }
 else if(command==5)
 {
  VarSet(VAR_HAVORA_GYM_STATE,0);HavoraGym_OnLoad();DrawWholeMapView();return;
 }
 else if(command==6){Draw(bx,by,TRUE);return;}
 VarSet(VAR_HAVORA_GYM_STATE,s);Draw(bx,by,TRUE);
}
