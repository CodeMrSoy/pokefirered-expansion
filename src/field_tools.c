#include "global.h"
#include "field_tools.h"
#include "field_effect.h"
#include "item.h"
#include "string_util.h"
#include "strings.h"
#include "constants/items.h"

const u32 gFieldToolIcon_Shears[] = INCBIN_U32("graphics/items/field_tools/shears.4bpp.lz");
const u32 gFieldToolIcon_Whistle[] = INCBIN_U32("graphics/items/field_tools/whistle.4bpp.lz");
const u32 gFieldToolIcon_WailmerWailer[] = INCBIN_U32("graphics/items/field_tools/wailmer_wailer.4bpp.lz");
const u32 gFieldToolIcon_Gloves[] = INCBIN_U32("graphics/items/field_tools/gloves.4bpp.lz");
const u32 gFieldToolIcon_Lantern[] = INCBIN_U32("graphics/items/field_tools/lantern.4bpp.lz");
const u32 gFieldToolIcon_Hammer[] = INCBIN_U32("graphics/items/field_tools/hammer.4bpp.lz");
const u32 gFieldToolIcon_Bait[] = INCBIN_U32("graphics/items/field_tools/bait.4bpp.lz");
const u16 gFieldToolIconPalette_Shears[] = INCBIN_U16("graphics/items/field_tools/shears.gbapal");
const u16 gFieldToolIconPalette_Whistle[] = INCBIN_U16("graphics/items/field_tools/whistle.gbapal");
const u16 gFieldToolIconPalette_WailmerWailer[] = INCBIN_U16("graphics/items/field_tools/wailmer_wailer.gbapal");
const u16 gFieldToolIconPalette_Gloves[] = INCBIN_U16("graphics/items/field_tools/gloves.gbapal");
const u16 gFieldToolIconPalette_Lantern[] = INCBIN_U16("graphics/items/field_tools/lantern.gbapal");
const u16 gFieldToolIconPalette_Hammer[] = INCBIN_U16("graphics/items/field_tools/hammer.gbapal");
const u16 gFieldToolIconPalette_Bait[] = INCBIN_U16("graphics/items/field_tools/bait.gbapal");

u16 FieldTool_GetItem(enum FieldMove fieldMove)
{
    switch (fieldMove)
    {
    case FIELD_MOVE_CUT: return ITEM_PRUNING_SHEARS;
    case FIELD_MOVE_FLY: return ITEM_SKY_WHISTLE;
    case FIELD_MOVE_SURF: return ITEM_WAILMER_WAILER;
    case FIELD_MOVE_STRENGTH: return ITEM_POWER_GLOVES;
    case FIELD_MOVE_FLASH: return ITEM_LANTERN;
    case FIELD_MOVE_ROCK_SMASH: return ITEM_ROCK_HAMMER;
    case FIELD_MOVE_WATERFALL: return ITEM_BASCULEGION_BAIT;
    default: return ITEM_NONE;
    }
}

enum FieldMove FieldTool_GetMove(u16 item)
{
    u32 move;
    if (item != ITEM_NONE)
        for (move = 0; move < FIELD_MOVE_COUNT; move++)
            if (FieldTool_GetItem(move) == item)
                return move;
    return FIELD_MOVE_COUNT;
}

bool32 FieldTool_IsOwned(enum FieldMove fieldMove)
{
    u16 item = FieldTool_GetItem(fieldMove);
    u32 i;
    if (item == ITEM_NONE)
        return FALSE;
    if (CheckBagHasItem(item, 1))
        return TRUE;
    // A full Key Items pocket must never remove access on an old save.
    for (i = 0; i < BAG_TMHM_COUNT; i++)
        if (gSaveBlock1Ptr->bag.TMsHMs[i].itemId == item
            && gSaveBlock1Ptr->bag.TMsHMs[i].quantity)
            return TRUE;
    return FALSE;
}

void FieldTool_Prepare(enum FieldMove fieldMove)
{
    gFieldEffectArguments[0] = FIELD_TOOL_ARGUMENT | FieldTool_GetItem(fieldMove);
    // Tool users are never followers, even if a party member knows the move.
    gFieldEffectArguments[3] = TRUE;
    StringCopy(gStringVar1, gSaveBlock2Ptr->playerName);
    CopyItemName(FieldTool_GetItem(fieldMove), gStringVar2);
}

void FieldTools_MigrateInventory(void)
{
    u32 i, write = 0;
    for (i = 0; i < BAG_TMHM_COUNT; i++)
    {
        struct ItemSlot *slot = &gSaveBlock1Ptr->bag.TMsHMs[i];
        if (!slot->quantity || FieldTool_GetMove(slot->itemId) == FIELD_MOVE_COUNT)
            continue;
        // Keep the old slot until its replacement is safely in Key Items.
        if (CheckBagHasItem(slot->itemId, 1) || AddBagItem(slot->itemId, 1))
        {
            slot->itemId = ITEM_NONE;
            slot->quantity = 0;
        }
    }
    CompactItemsInBagPocket(POCKET_TM_HM);
    // Keep any deferred tools after the genuine TMs/HMs. The TM Case can
    // hide that tail without losing the old save's inventory or slot IDs.
    for (i = 0; i < BAG_TMHM_COUNT; i++)
    {
        struct ItemSlot *slots = gSaveBlock1Ptr->bag.TMsHMs;
        if (slots[i].itemId == ITEM_NONE)
            break;
        if (FieldTool_GetMove(slots[i].itemId) == FIELD_MOVE_COUNT)
        {
            struct ItemSlot pending = slots[write];
            slots[write++] = slots[i];
            slots[i] = pending;
        }
    }
}
