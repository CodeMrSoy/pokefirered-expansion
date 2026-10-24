#ifndef GUARD_FIELD_TOOLS_H
#define GUARD_FIELD_TOOLS_H

#include "constants/field_move.h"

// Fits the signed 16-bit task arguments used by Surf, Fly and Waterfall.
#define FIELD_TOOL_ARGUMENT (1 << 13)
#define FIELD_TOOL_ICON_TAG 0xD130

u16 FieldTool_GetItem(enum FieldMove fieldMove);
enum FieldMove FieldTool_GetMove(u16 item);
bool32 FieldTool_IsOwned(enum FieldMove fieldMove);
void FieldTool_Prepare(enum FieldMove fieldMove);
void FieldTools_MigrateInventory(void);

extern const u32 gFieldToolIcon_Shears[];
extern const u32 gFieldToolIcon_Whistle[];
extern const u32 gFieldToolIcon_WailmerWailer[];
extern const u32 gFieldToolIcon_Gloves[];
extern const u32 gFieldToolIcon_Lantern[];
extern const u32 gFieldToolIcon_Hammer[];
extern const u32 gFieldToolIcon_Bait[];
extern const u16 gFieldToolIconPalette_Shears[];
extern const u16 gFieldToolIconPalette_Whistle[];
extern const u16 gFieldToolIconPalette_WailmerWailer[];
extern const u16 gFieldToolIconPalette_Gloves[];
extern const u16 gFieldToolIconPalette_Lantern[];
extern const u16 gFieldToolIconPalette_Hammer[];
extern const u16 gFieldToolIconPalette_Bait[];

#endif
