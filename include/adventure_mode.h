#ifndef GUARD_ADVENTURE_MODE_H
#define GUARD_ADVENTURE_MODE_H

#include "global.h"
#include "constants/adventure_mode.h"

u8 AdventureMode_Get(void);
bool32 AdventureMode_IsQuantum(void);
const u8 *AdventureMode_Name(u8 mode);
void AdventureMode_ResetPending(void);
bool32 AdventureMode_SelectNewGame(u8 mode);
u8 AdventureMode_GetPending(void);
void AdventureMode_NewGame(void);
void AdventureMode_MigrateLoadedSave(void);
bool32 AdventureMode_IsVidraMap(s8 group, s8 number);
bool32 AdventureMode_AllowsMap(s8 group, s8 number);
u16 AdventureMode_FerryDestination(u16 origin, u16 destination, bool32 hasTicket);
void AdventureMode_AdjustWarp(struct WarpData *warp);
void AdventureMode_AdjustMapHeader(struct MapHeader *header);

#endif
