#ifndef GUARD_FIELD_TOOLS_H
#define GUARD_FIELD_TOOLS_H

#include "constants/field_move.h"

// Fits the signed 16-bit task arguments used by Surf, Fly and Waterfall.
#define FIELD_TOOL_ARGUMENT (1 << 13)
#define FIELD_TOOL_ICON_TAG 0xD130

u8 FieldTool_CreateLargeSprite(u16 item, u16 tag, s16 x, s16 y);
u16 FieldTool_GetItem(enum FieldMove fieldMove);
enum FieldMove FieldTool_GetMove(u16 item);
bool32 FieldTool_IsOwned(enum FieldMove fieldMove);
void FieldTool_Prepare(enum FieldMove fieldMove);
void FieldTools_MigrateInventory(void);
bool32 FieldTool_HasFlag(u16 item);
bool32 FieldTool_Collect(u16 item);
bool32 FieldTool_Remove(u16 item);
extern const u32 gFieldItemCaseIcon[];
extern const u16 gFieldItemCasePalette[];
void FieldItemCase_OpenUI(void);
void FieldItemCase_Return(bool32 use, u16 item);


#endif
