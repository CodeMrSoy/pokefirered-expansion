#include "global.h"
#include "gflib.h"
#include "main.h"
#include "task.h"
#include "menu.h"
#include "menu_helpers.h"
#include "constants/songs.h"
#include "item.h"
#include "field_tools.h"
#include "field_move.h"
#include "constants/sound.h"
#include "palette.h"

#define CASE_PREVIEW_TAG 0xD131
static EWRAM_DATA u8 sCaseWindow = 0;
static EWRAM_DATA u8 sCaseSelection = 0;
static EWRAM_DATA u8 sCasePreview = 0;
static const u8 sColors[] = {1, 2, 3};
static const u8 sDisabledColors[] = {1, 3, 1};
static const u16 sPalette[] = {RGB(5,10,15), RGB(29,30,28), RGB(3,7,10), RGB(18,21,20)};
static const struct BgTemplate sBackground = {.bg = 0, .charBaseIndex = 0, .mapBaseIndex = 31, .priority = 1};
static const struct WindowTemplate sWindow = {.bg = 0, .tilemapLeft = 1, .tilemapTop = 1, .width = 28, .height = 18, .paletteNum = 15, .baseBlock = 1};
static const u8 *const sDescriptions[] = {
    COMPOUND_STRING("Trim a tree or tall grass."),
    COMPOUND_STRING("Call a flying ride to a visited town."),
    COMPOUND_STRING("Call a sea ride at the water's edge."),
    COMPOUND_STRING("Move heavy boulders out of the way."),
    COMPOUND_STRING("Light the darkness around you."),
    COMPOUND_STRING("Break cracked rocks in your path."),
    COMPOUND_STRING("Call a ride up a waterfall."),
};
static void CaseText(const u8 *text, u8 x, u8 y, u8 font)
{
    AddTextPrinterParameterized3(sCaseWindow, font, x, y, sColors, TEXT_SKIP_DRAW, text);
}
static void CaseDestroyPreview(void)
{
    if (sCasePreview != MAX_SPRITES)
        DestroySpriteAndFreeResources(&gSprites[sCasePreview]);
    sCasePreview = MAX_SPRITES;
}
static void CaseDraw(bool32 missingBadge)
{
    u32 i;
    u16 item = FieldTool_GetItem(sCaseSelection);
    bool32 owned = FieldTool_IsOwned(sCaseSelection);
    FillWindowPixelBuffer(sCaseWindow, PIXEL_FILL(1));
    CaseText(COMPOUND_STRING("FIELD ITEM CASE"), 5, 0, FONT_NORMAL);
    for (i = 0; i < 7; i++)
    {
        AddTextPrinterParameterized3(sCaseWindow, FONT_SMALL, 91, 24 + i * 12,
            FieldTool_IsOwned(i) ? sColors : sDisabledColors, TEXT_SKIP_DRAW,
            GetItemName(FieldTool_GetItem(i)));
        if (i == sCaseSelection)
            CaseText(COMPOUND_STRING(">"), 80, 24 + i * 12, FONT_SMALL);
    }
    CaseText(sDescriptions[sCaseSelection], 4, 111, FONT_SMALL);
    CaseText(missingBadge ? COMPOUND_STRING("A GYM BADGE is needed.   B: Back") :
        owned ? COMPOUND_STRING("A: Use tool                 B: Back") : COMPOUND_STRING("Tool not collected.         B: Back"), 4, 127, FONT_SMALL);
    CaseDestroyPreview();
    sCasePreview = FieldTool_CreateLargeSprite(item, CASE_PREVIEW_TAG, 49, 72);
    if (!owned && sCasePreview != MAX_SPRITES)
    {
        u16 colors[16];
        u16 offset = 0x100 + gSprites[sCasePreview].oam.paletteNum * 16;
        for (i = 0; i < 16; i++)
        {
            u16 c = gPlttBufferUnfaded[offset + i];
            u16 gray = (((c & 31) * 3 + ((c >> 5) & 31) * 6 + ((c >> 10) & 31)) / 10 + 21) / 2;
            colors[i] = RGB(gray, gray, gray);
        }
        LoadPalette(colors, offset, sizeof(colors));
    }
    CopyWindowToVram(sCaseWindow, COPYWIN_FULL);
}
static void CaseClose(bool32 use)
{
    u16 item = FieldTool_GetItem(sCaseSelection);
    SetVBlankCallback(NULL);
    CaseDestroyPreview();
    FreeAllWindowBuffers();
    FieldItemCase_Return(use, item);
}
static void Task_FieldItemCase(u8 taskId)
{
    if (gPaletteFade.active)
        return;
    if (JOY_NEW(B_BUTTON))
    {
        PlaySE(SE_SELECT);
        DestroyTask(taskId);
        CaseClose(FALSE);
    }
    else if (JOY_NEW(A_BUTTON))
    {
        if (!FieldTool_IsOwned(sCaseSelection))
            return;
        PlaySE(SE_SELECT);
        if (!FieldMove_IsUnlocked(sCaseSelection))
            CaseDraw(TRUE);
        else
        {
            DestroyTask(taskId);
            CaseClose(TRUE);
        }
    }
    else if (JOY_REPEAT(DPAD_UP | DPAD_DOWN))
    {
        sCaseSelection = (sCaseSelection + (JOY_REPEAT(DPAD_UP) ? 6 : 1)) % 7;
        PlaySE(SE_SELECT);
        CaseDraw(FALSE);
    }
}
static void VBlank_FieldItemCase(void)
{
    LoadOam();
    ProcessSpriteCopyRequests();
    TransferPlttBuffer();
}
static void CB2_FieldItemCase(void)
{
    RunTasks();
    AnimateSprites();
    BuildOamBuffer();
    UpdatePaletteFade();
    DoScheduledBgTilemapCopiesToVram();
}
static void CB2_InitFieldItemCase(void)
{
    SetVBlankCallback(NULL);
    SetGpuReg(REG_OFFSET_DISPCNT, 0);
    DmaFill16(3, 0, (void *)VRAM, VRAM_SIZE);
    ResetBgsAndClearDma3BusyFlags(0);
    InitBgsFromTemplates(0, &sBackground, 1);
    ResetAllBgsCoordinates();
    ResetPaletteFade();
    ResetSpriteData();
    FreeAllSpritePalettes();
    ResetTasks();
    sCasePreview = MAX_SPRITES;
    InitWindows((const struct WindowTemplate[]){sWindow, DUMMY_WIN_TEMPLATE});
    DeactivateAllTextPrinters();
    sCaseWindow = 0;
    LoadPalette(sPalette, 0, sizeof(sPalette));
    LoadPalette(sPalette, 15 * 16, sizeof(sPalette));
    PutWindowTilemap(sCaseWindow);
    SetGpuReg(REG_OFFSET_WININ, 0);
    SetGpuReg(REG_OFFSET_WINOUT, 0);
    SetGpuReg(REG_OFFSET_BLDCNT, 0);
    SetGpuReg(REG_OFFSET_BLDY, 0);
    SetGpuReg(REG_OFFSET_DISPCNT, DISPCNT_MODE_0 | DISPCNT_OBJ_ON | DISPCNT_OBJ_1D_MAP);
    ShowBg(0);
    CaseDraw(FALSE);
    CreateTask(Task_FieldItemCase, 0);
    SetVBlankCallback(VBlank_FieldItemCase);
    SetMainCallback2(CB2_FieldItemCase);
}
void FieldItemCase_OpenUI(void)
{
    FieldTools_MigrateInventory();
    for (sCaseSelection = 0; sCaseSelection < FIELD_MOVE_COUNT; sCaseSelection++)
        if (FieldTool_IsOwned(sCaseSelection))
            break;
    if (sCaseSelection == FIELD_MOVE_COUNT)
        sCaseSelection = 0;
    SetMainCallback2(CB2_InitFieldItemCase);
}
