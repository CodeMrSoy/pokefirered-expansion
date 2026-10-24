#include "global.h"
#include "field_tools.h"
#include "sprite.h"
#include "event_data.h"
#include "constants/flags.h"
#include "field_effect.h"
#include "item.h"
#include "item_menu.h"
#include "string_util.h"
#include "strings.h"
#include "constants/items.h"

const u32 gFieldItemCaseIcon[] = INCBIN_U32("graphics/items/field_item_case.4bpp.lz");
const u16 gFieldItemCasePalette[] = INCBIN_U16("graphics/items/field_item_case.gbapal");

// Shared by field cut-ins and the selected field item in the Bag.
static const u32 sCutinShears[] = INCBIN_U32("graphics/field_effects/field_tools/shears.4bpp");
static const u16 sCutinShearsPalette[] = INCBIN_U16("graphics/field_effects/field_tools/shears.gbapal");
static const u32 sCutinWhistle[] = INCBIN_U32("graphics/field_effects/field_tools/whistle.4bpp");
static const u16 sCutinWhistlePalette[] = INCBIN_U16("graphics/field_effects/field_tools/whistle.gbapal");
static const u32 sCutinWailmerWailer[] = INCBIN_U32("graphics/field_effects/field_tools/wailmer_wailer.4bpp");
static const u16 sCutinWailmerWailerPalette[] = INCBIN_U16("graphics/field_effects/field_tools/wailmer_wailer.gbapal");
static const u32 sCutinGloves[] = INCBIN_U32("graphics/field_effects/field_tools/gloves.4bpp");
static const u16 sCutinGlovesPalette[] = INCBIN_U16("graphics/field_effects/field_tools/gloves.gbapal");
static const u32 sCutinLantern[] = INCBIN_U32("graphics/field_effects/field_tools/lantern.4bpp");
static const u16 sCutinLanternPalette[] = INCBIN_U16("graphics/field_effects/field_tools/lantern.gbapal");
static const u32 sCutinHammer[] = INCBIN_U32("graphics/field_effects/field_tools/hammer.4bpp");
static const u16 sCutinHammerPalette[] = INCBIN_U16("graphics/field_effects/field_tools/hammer.gbapal");
static const u32 sCutinBait[] = INCBIN_U32("graphics/field_effects/field_tools/bait.4bpp");
static const u16 sCutinBaitPalette[] = INCBIN_U16("graphics/field_effects/field_tools/bait.gbapal");

static const struct OamData sFieldToolLargeOam = {
    .shape = SPRITE_SHAPE(64x64),
    .size = SPRITE_SIZE(64x64),
};
static const struct SpriteTemplate sFieldToolLargeBase = {
    .oam = &sFieldToolLargeOam,
    .anims = gDummySpriteAnimTable,
    .affineAnims = gDummySpriteAffineAnimTable,
    .callback = SpriteCallbackDummy,
};
static EWRAM_DATA struct SpriteTemplate sFieldToolLargeTemplate = {0};

u8 FieldTool_CreateLargeSprite(u16 item, u16 tag, s16 x, s16 y)
{
    struct SpriteSheet sheet = { .size = 64 * 64 / 2 };
    struct SpritePalette palette;
    u8 spriteId;
    switch (item)
    {
    case ITEM_PRUNING_SHEARS:
        sheet.data = sCutinShears;
        palette.data = sCutinShearsPalette;
        break;
    case ITEM_SKY_WHISTLE:
        sheet.data = sCutinWhistle;
        palette.data = sCutinWhistlePalette;
        break;
    case ITEM_WAILMER_WAILER:
        sheet.data = sCutinWailmerWailer;
        palette.data = sCutinWailmerWailerPalette;
        break;
    case ITEM_POWER_GLOVES:
        sheet.data = sCutinGloves;
        palette.data = sCutinGlovesPalette;
        break;
    case ITEM_LANTERN:
        sheet.data = sCutinLantern;
        palette.data = sCutinLanternPalette;
        break;
    case ITEM_ROCK_HAMMER:
        sheet.data = sCutinHammer;
        palette.data = sCutinHammerPalette;
        break;
    case ITEM_BASCULEGION_BAIT:
        sheet.data = sCutinBait;
        palette.data = sCutinBaitPalette;
        break;
    default: return MAX_SPRITES;
    }
    sFieldToolLargeTemplate = sFieldToolLargeBase;
    sheet.tag = palette.tag = tag;
    sFieldToolLargeTemplate.tileTag = sFieldToolLargeTemplate.paletteTag = tag;
    LoadSpriteSheet(&sheet);
    if (GetSpriteTileStartByTag(tag) == TAG_NONE)
        return MAX_SPRITES;
    if (LoadSpritePalette(&palette) == 0xFF)
    {
        FreeSpriteTilesByTag(tag);
        return MAX_SPRITES;
    }
    spriteId = CreateSprite(&sFieldToolLargeTemplate, x, y, 0);
    if (spriteId == MAX_SPRITES)
    {
        FreeSpriteTilesByTag(tag);
        FreeSpritePaletteByTag(tag);
    }
    return spriteId;
}

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

bool32 FieldTool_HasFlag(u16 item)
{
    enum FieldMove move = FieldTool_GetMove(item);
    return move < 7 && FlagGet(FLAG_FIELD_TOOL_FIRST + move);
}

bool32 FieldTool_Collect(u16 item)
{
    enum FieldMove move = FieldTool_GetMove(item);
    if (move >= 7 || !AddBagItem(ITEM_FIELD_ITEM_CASE, 1))
        return FALSE;
    FlagSet(FLAG_FIELD_TOOL_FIRST + move);
    return TRUE;
}

bool32 FieldTool_Remove(u16 item)
{
    enum FieldMove move = FieldTool_GetMove(item);
    if (move >= 7 || !FieldTool_HasFlag(item))
        return FALSE;
    FlagClear(FLAG_FIELD_TOOL_FIRST + move);
    return TRUE;
}

void FieldTools_MigrateInventory(void)
{
    u32 pocket, i;
    bool32 any = FALSE, registeredCase = FALSE;
    // Replacing an existing tool frees the slot required for its case even
    // when the Key Items pocket is full. Restore the slot on any failure.
    for (pocket = 0; pocket < POCKETS_COUNT; pocket++)
        for (i = 0; i < gBagPockets[pocket].capacity; i++)
        {
            struct ItemSlot *slot = &gBagPockets[pocket].itemSlots[i];
            struct ItemSlot old = *slot;
            if (!old.quantity || FieldTool_GetMove(old.itemId) == FIELD_MOVE_COUNT)
                continue;
            slot->itemId = ITEM_NONE;
            slot->quantity = 0;
            if (!FieldTool_Collect(old.itemId))
                *slot = old;
        }
    for (i = 0; i < 7; i++)
        any |= FlagGet(FLAG_FIELD_TOOL_FIRST + i);
    if (any)
        AddBagItem(ITEM_FIELD_ITEM_CASE, 1);
    for (pocket = 0; pocket < POCKETS_COUNT; pocket++)
        CompactItemsInBagPocket(pocket);
    // A deferred old tool must not appear among teachable TMs.
    {
        u32 write = 0;
        struct ItemSlot *slots = gSaveBlock1Ptr->bag.TMsHMs;
        for (i = 0; i < BAG_TMHM_COUNT && slots[i].itemId != ITEM_NONE; i++)
            if (FieldTool_GetMove(slots[i].itemId) == FIELD_MOVE_COUNT)
            {
                struct ItemSlot pending = slots[write];
                slots[write++] = slots[i];
                slots[i] = pending;
            }
    }
    // Preserve the first old tool shortcut, remove duplicate case shortcuts.
    for (i = 0; i < 4; i++)
    {
        u16 *registered = RegisteredItemAt(i);
        if (FieldTool_GetMove(*registered) != FIELD_MOVE_COUNT && CheckBagHasItem(ITEM_FIELD_ITEM_CASE, 1))
            *registered = ITEM_FIELD_ITEM_CASE;
        if (*registered == ITEM_FIELD_ITEM_CASE)
        {
            if (registeredCase)
                *registered = ITEM_NONE;
            registeredCase = TRUE;
        }
    }
}
