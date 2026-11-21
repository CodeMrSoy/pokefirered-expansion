// The linear ListMenu remains authoritative for every native item action.
// Its printed rows are replaced with a paged 3x3 view only inside PokéGlass.
#define GLASS_GRID_TAG 0xD300
static const u8 sGlassGridEmpty[] = _("");
static EWRAM_DATA u8 sGlassGridSprites[9];
static EWRAM_DATA u16 sGlassGridItems[9];
static EWRAM_DATA u16 sGlassGridPage;
static EWRAM_DATA u8 sGlassGridPocket;
static EWRAM_DATA u8 sGlassInfoPage;
static EWRAM_DATA u8 sGlassInfoPages;
static EWRAM_DATA s32 sGlassGridSelection;

static bool8 GlassBagGrid(void)
{
    return IsPokeGlassSessionActive() && gBagPosition.location != ITEMMENULOCATION_ITEMPC && !IsTutorialBag();
}

static void GlassGridReset(void)
{
    memset(sGlassGridSprites, MAX_SPRITES, sizeof(sGlassGridSprites));
    memset(sGlassGridItems, 0, sizeof(sGlassGridItems));
    sGlassGridPocket = 0xFF;
    sGlassGridPage = 0xFFFF;
    sGlassGridSelection = -2;
    sGlassInfoPage = 0;
}

static void GlassGridDestroy(void)
{
    u32 i;
    for (i = 0; i < 9; i++)
        if (sGlassGridSprites[i] < MAX_SPRITES)
        {
            DestroySpriteAndFreeResources(&gSprites[sGlassGridSprites[i]]);
            sGlassGridSprites[i] = MAX_SPRITES;
        }
    sGlassGridPocket = 0xFF;
}

static void GlassGridDescription(s32 selected)
{
    static const u8 colors[] = {0, 8, 4};
    u8 name[ITEM_NAME_LENGTH + 1];
    const u8 *description;
    u32 i;
    FillWindowPixelBuffer(WIN_DESCRIPTION, PIXEL_FILL(0));
    FillWindowPixelBuffer(WIN_GLASS_ITEM_NAME, PIXEL_FILL(0));
    if (selected == LIST_CANCEL)
    {
        StringCopy(name, COMPOUND_STRING("Back"));
        description = COMPOUND_STRING("Return to PokéGlass.");
    }
    else
    {
        u16 item = GetBagItemId(gBagPosition.pocket, selected);
        CopyItemName(item, name);
        description = GetItemDescription(item);
    }
    FitPokeGlassText(name, FONT_SMALL, 84);
    AddTextPrinterParameterized3(WIN_GLASS_ITEM_NAME, FONT_SMALL, 2, 0, colors, TEXT_SKIP_DRAW, name);
    // Own the border with the text so native popup cleanup cannot obscure it.
    FillWindowPixelRect(WIN_DESCRIPTION, 6, 0, 0, 88, 40);
    FillWindowPixelRect(WIN_DESCRIPTION, 0, 1, 1, 86, 38);
    sGlassInfoPages = PokeGlassPrintTextPage(WIN_DESCRIPTION, 2, 0, 84, 3, sGlassInfoPage, description);
    for (i = 0; i < sGlassInfoPages && i < 20; i++)
        FillWindowPixelRect(WIN_GLASS_ITEM_NAME, i == sGlassInfoPage ? 8 : 6, i * 4, 13, 3, 2);
    PutWindowTilemap(WIN_GLASS_ITEM_NAME);
    CopyWindowToVram(WIN_GLASS_ITEM_NAME, COPYWIN_FULL);
    CopyWindowToVram(WIN_DESCRIPTION, COPYWIN_FULL);
}

static void GlassGridDraw(s32 selected, struct ListMenu *list)
{
    static const u8 colors[] = {0, 8, 4};
    u32 i, index = list->scrollOffset + list->selectedRow, page = index / 9;
    bool8 rebuild = page != sGlassGridPage || gBagPosition.pocket != sGlassGridPocket;
    u16 items[9];
    for (i = 0; i < 9; i++)
    {
        u32 slot = page * 9 + i;
        items[i] = slot < gBagMenu->numItemStacks[gBagPosition.pocket] - 1 ? GetBagItemId(gBagPosition.pocket, slot) : ITEM_NONE;
        if (items[i] != sGlassGridItems[i]) rebuild = TRUE;
    }
    if (rebuild)
    {
        if (gBagPosition.pocket != sGlassGridPocket)
        {
            sGlassInfoPage = 0;
            sGlassGridSelection = -2;
        }
        GlassGridDestroy();
        for (i = 0; i < 9; i++)
            if (items[i])
            {
                u8 sprite = AddItemIconSprite(GLASS_GRID_TAG + i, GLASS_GRID_TAG + i, items[i]);
                sGlassGridSprites[i] = sprite;
                if (sprite < MAX_SPRITES)
                {
                    // Item art occupies the top-left 24x24 of a 32x32 sprite.
                    // Offset its canvas so the art is centered above the quantity.
                    gSprites[sprite].x = 134 + (i % 3) * 36;
                    gSprites[sprite].y = 50 + (i / 3) * 36;
                    gSprites[sprite].oam.priority = 1;
                }
            }
        memcpy(sGlassGridItems, items, sizeof(items));
        sGlassGridPage = page;
        sGlassGridPocket = gBagPosition.pocket;
    }
    FillWindowPixelBuffer(WIN_ITEM_LIST, PIXEL_FILL(0));
    for (i = 0; i < 9; i++)
    {
        u32 slot = page * 9 + i, x = i % 3 * 36, y = i / 3 * 36;
        u8 quantity[8];
        if (slot >= gBagMenu->numItemStacks[gBagPosition.pocket]) break;
        FillWindowPixelRect(WIN_ITEM_LIST, slot == index ? 8 : 6, x, y, 35, 35);
        FillWindowPixelRect(WIN_ITEM_LIST, 0, x + 1, y + 1, 33, 33);
        if (items[i])
        {
            if (gBagPosition.pocket != POCKET_KEY_ITEMS)
            {
                ConvertIntToDecimalStringN(quantity, GetBagItemQuantity(gBagPosition.pocket, slot), STR_CONV_MODE_LEFT_ALIGN, MAX_ITEM_DIGITS);
                AddTextPrinterParameterized3(WIN_ITEM_LIST, FONT_SMALL, x + 34 - GetStringWidth(FONT_SMALL, quantity, 0), y + 23, colors, TEXT_SKIP_DRAW, quantity);
            }
            else if (RegisteredItemSlot(items[i]) >= 0)
                AddTextPrinterParameterized3(WIN_ITEM_LIST, FONT_SMALL, x + 26, y + 23, colors, TEXT_SKIP_DRAW, COMPOUND_STRING("R"));
        }
        else AddTextPrinterParameterized3(WIN_ITEM_LIST, FONT_SMALL, x + 4, y + 10, colors, TEXT_SKIP_DRAW, COMPOUND_STRING("Back"));
    }
    if (selected != sGlassGridSelection)
    {
        sGlassInfoPage = 0;
        sGlassGridSelection = selected;
    }
    if (gBagMenu->toSwapPos == NOT_SWAPPING) GlassGridDescription(selected);
    CopyWindowToVram(WIN_ITEM_LIST, COPYWIN_FULL);
    PrintPocketName();
}

static s32 GlassGridInput(u8 listTaskId)
{
    struct ListMenu *list = (void *)gTasks[listTaskId].data;
    u16 index = list->scrollOffset + list->selectedRow, target = index;
    if (JOY_NEW(A_BUTTON)) return list->template.items[index].id;
    if (JOY_NEW(B_BUTTON)) return LIST_CANCEL;
    if (JOY_REPEAT(DPAD_UP) && index >= 3) target -= 3;
    else if (JOY_REPEAT(DPAD_DOWN) && index + 3 < list->template.totalItems) target += 3;
    else if (JOY_REPEAT(DPAD_LEFT) && index) target--;
    else if (JOY_REPEAT(DPAD_RIGHT) && index + 1 < list->template.totalItems) target++;
    if (target != index)
    {
        // Suppress the hidden linear renderer; keep native action indices intact.
        list->scrollOffset = target;
        list->selectedRow = 0;
        PlaySE(SE_BAG_CURSOR);
        GlassGridDraw(list->template.items[target].id, list);
    }
    return LIST_NOTHING_CHOSEN;
}
