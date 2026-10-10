#include "global.h"
#include "gflib.h"
#include "menu.h"
#include "poke_glass.h"
#include "event_data.h"
#include "script.h"
#include "sound.h"
#include "task.h"
#include "constants/menu.h"
#include "constants/songs.h"

// Both screens share the bezel palette and nine reusable tiles. Reserving only
// nine tiles avoids overwriting the field menu's standard window-border art.
static const u16 sPalette[16] = {
    RGB(0,0,0), RGB(4,8,12), RGB(11,17,22), RGB(24,29,31),
    RGB(3,11,18), RGB(7,19,27), RGB(18,26,30), RGB(12,22,28),
    0, 0, 0, 0, 0, 0, 0, RGB(31,31,31)
};
static const u8 sFrameTiles[] = {
    0x22, 0x22, 0x22, 0x22, 0x22, 0x22, 0x22, 0x22, 0x22, 0x22, 0x22, 0x22, 0x22, 0x22, 0x22, 0x22,
    0x22, 0x22, 0x33, 0x33, 0x22, 0x22, 0x33, 0x33, 0x22, 0x22, 0x33, 0x33, 0x22, 0x22, 0x33, 0x33,
    0x22, 0x22, 0x22, 0x22, 0x22, 0x22, 0x22, 0x22, 0x22, 0x22, 0x22, 0x22, 0x22, 0x22, 0x22, 0x22,
    0x33, 0x33, 0x33, 0x33, 0x33, 0x33, 0x33, 0x33, 0x33, 0x33, 0x33, 0x33, 0x33, 0x33, 0x33, 0x33,
    0x22, 0x22, 0x22, 0x22, 0x22, 0x22, 0x22, 0x22, 0x22, 0x22, 0x22, 0x22, 0x22, 0x22, 0x22, 0x22,
    0x33, 0x33, 0x22, 0x22, 0x33, 0x33, 0x22, 0x22, 0x33, 0x33, 0x22, 0x22, 0x33, 0x33, 0x22, 0x22,
    0x22, 0x22, 0x33, 0x33, 0x22, 0x22, 0x33, 0x33, 0x22, 0x22, 0x33, 0x33, 0x22, 0x22, 0x33, 0x33,
    0x22, 0x22, 0x33, 0x33, 0x22, 0x22, 0x33, 0x33, 0x22, 0x22, 0x33, 0x33, 0x22, 0x22, 0x33, 0x33,
    0x44, 0x44, 0x44, 0x44, 0x44, 0x44, 0x44, 0x44, 0x44, 0x44, 0x44, 0x44, 0x44, 0x44, 0x44, 0x44,
    0x44, 0x44, 0x44, 0x44, 0x44, 0x44, 0x44, 0x44, 0x44, 0x44, 0x44, 0x44, 0x44, 0x44, 0x44, 0x44,
    0x33, 0x33, 0x22, 0x22, 0x33, 0x33, 0x22, 0x22, 0x33, 0x33, 0x22, 0x22, 0x33, 0x33, 0x22, 0x22,
    0x33, 0x33, 0x22, 0x22, 0x33, 0x33, 0x22, 0x22, 0x33, 0x33, 0x22, 0x22, 0x33, 0x33, 0x22, 0x22,
    0x22, 0x22, 0x33, 0x33, 0x22, 0x22, 0x33, 0x33, 0x22, 0x22, 0x33, 0x33, 0x22, 0x22, 0x33, 0x33,
    0x22, 0x22, 0x22, 0x22, 0x22, 0x22, 0x22, 0x22, 0x22, 0x22, 0x22, 0x22, 0x22, 0x22, 0x22, 0x22,
    0x33, 0x33, 0x33, 0x33, 0x33, 0x33, 0x33, 0x33, 0x33, 0x33, 0x33, 0x33, 0x33, 0x33, 0x33, 0x33,
    0x22, 0x22, 0x22, 0x22, 0x22, 0x22, 0x22, 0x22, 0x22, 0x22, 0x22, 0x22, 0x22, 0x22, 0x22, 0x22,
    0x33, 0x33, 0x22, 0x22, 0x33, 0x33, 0x22, 0x22, 0x33, 0x33, 0x22, 0x22, 0x33, 0x33, 0x22, 0x22,
    0x22, 0x22, 0x22, 0x22, 0x22, 0x22, 0x22, 0x22, 0x22, 0x22, 0x22, 0x22, 0x22, 0x22, 0x22, 0x22,
};

void DrawPokeGlassFrame(u8 bg)
{
    u8 x, y, tx, ty;
    // Field BG0 starts at char block 2; tile 0x300 would overwrite map
    // screen blocks. Party BG1 instead has free space above its menu windows.
    u16 tileBase = bg == 0 ? 0x280 : 0x3E0;
    LoadPalette(sPalette, BG_PLTT_ID(11), sizeof(sPalette));
    LoadBgTiles(bg, sFrameTiles, sizeof(sFrameTiles), tileBase);
    for (y = 0; y < 20; y++)
    {
        ty = y == 0 ? 0 : y == 19 ? 2 : 1;
        for (x = 0; x < 30; x++)
        {
            tx = x == 0 ? 0 : x == 29 ? 2 : 1;
            FillBgTilemapBufferRect(bg, tileBase + ty * 3 + tx, x, y, 1, 1, 11);
        }
    }
    ScheduleBgCopyTilemapToVram(bg);
}

// The field hub owns one BG0 window. Hardware alpha blending keeps the map and
// player visible through the glass; restore field/weather registers on every exit.

static EWRAM_DATA u8 sHubWindow = 0;
static EWRAM_DATA u8 sHubCursor = 0;
static EWRAM_DATA u16 sHubBlend[5] = {0};
static EWRAM_DATA u16 sHubPalette[32] = {0};
static const u16 sHubColors[16] = {
    RGB(0,0,0), RGB(2,6,12), RGB(9,18,24), RGB(2,5,9),
    RGB(4,11,18), RGB(8,21,27), RGB(14,25,29), RGB(23,30,31),
    RGB(9,27,23), RGB(27,20,9), RGB(20,16,29), RGB(13,22,31),
    RGB(10,15,20), RGB(17,22,25), RGB(25,29,30), RGB(31,31,31)
};
static const u8 sHubTitle[] = _("POKéGLASS");
static const u8 sHubHint[] = _("A Open   B Close");
static const u8 sHubHome[] = _("HOME");
static const u8 sHubLabels[][16] = {
    _("Pokédex"), _("Party"), _("Storage"), _("Stats"), _("Map")
};
static const struct WindowTemplate sHubTemplate = {
    .bg = 0, .tilemapLeft = 1, .tilemapTop = 1,
    .width = 28, .height = 18, .paletteNum = 11, .baseBlock = 0x038,
};

static void HubRect(u8 color, u16 x, u16 y, u16 width, u16 height)
{
    FillWindowPixelRect(sHubWindow, PIXEL_FILL(color), x, y, width, height);
}

static void DrawHubIcon(u8 app, u16 x, u16 y)
{
    u8 color = 7;
    switch (app)
    {
    case 0: // Hinged Pokédex with a lens and lower display.
        HubRect(color, x + 1, y, 13, 18);
        HubRect(4, x + 3, y + 2, 9, 14);
        HubRect(11, x + 4, y + 3, 4, 4);
        HubRect(color, x + 4, y + 10, 7, 1);
        HubRect(color, x + 4, y + 13, 5, 1);
        break;
    case 1: // Poké Ball.
        HubRect(color, x + 3, y + 1, 10, 16);
        HubRect(color, x, y + 4, 16, 10);
        HubRect(4, x, y + 8, 16, 2);
        HubRect(4, x + 5, y + 6, 6, 6);
        HubRect(15, x + 7, y + 8, 2, 2);
        break;
    case 2: // Storage drawers.
        HubRect(color, x, y + 1, 16, 16);
        HubRect(4, x + 2, y + 3, 12, 5);
        HubRect(4, x + 2, y + 10, 12, 5);
        HubRect(8, x + 6, y + 5, 4, 1);
        HubRect(8, x + 6, y + 12, 4, 1);
        break;
    case 3: // Stat bars.
        HubRect(color, x, y + 16, 17, 1);
        HubRect(8, x + 1, y + 10, 3, 5);
        HubRect(11, x + 7, y + 6, 3, 9);
        HubRect(9, x + 13, y + 1, 3, 14);
        break;
    case 4: // Folded route map.
        HubRect(color, x, y + 2, 17, 14);
        HubRect(4, x + 5, y + 2, 1, 14);
        HubRect(4, x + 11, y + 2, 1, 14);
        HubRect(8, x + 2, y + 10, 12, 2);
        HubRect(8, x + 12, y + 5, 2, 7);
        HubRect(9, x + 11, y + 3, 4, 4);
        break;
    }
}

static void DrawHubApp(u8 i, bool8 upload)
{
    static const u8 textColors[] = {0, 15, 3};
    u16 x = 12 + (i % 2) * 104;
    u16 y = 32 + (i / 2) * 31;
    u16 width = i == 4 ? 200 : 96;
    bool8 selected = i == sHubCursor;
    HubRect(selected ? 7 : 2, x, y, width, 27);
    HubRect(selected ? 5 : 4, x + 1, y + 1, width - 2, 25);
    if (selected)
        HubRect(15, x + 2, y + 5, 2, 17);
    DrawHubIcon(i, x + 8, y + 5);
    AddTextPrinterParameterized3(sHubWindow, FONT_SMALL, x + 30, y + 7, textColors, TEXT_SKIP_DRAW, sHubLabels[i]);
    if (upload)
        CopyWindowRectToVram(sHubWindow, COPYWIN_GFX, x / 8, y / 8, (x + width + 7) / 8 - x / 8, (y + 27 + 7) / 8 - y / 8);
}

static void DrawHub(void)
{
    static const u8 textColors[] = {0, 15, 3};
    static const u8 mutedColors[] = {0, 14, 3};
    u8 i;
    FillWindowPixelBuffer(sHubWindow, PIXEL_FILL(0));
    // Inset corners, double rim, and a narrow reflection along the top edge.
    HubRect(2, 4, 0, 216, 144);
    HubRect(2, 0, 4, 224, 136);
    HubRect(7, 5, 2, 214, 1);
    HubRect(6, 2, 5, 1, 134);
    HubRect(1, 5, 5, 214, 134);
    HubRect(6, 12, 25, 200, 1);
    AddTextPrinterParameterized3(sHubWindow, FONT_SMALL, 13, 7, textColors, TEXT_SKIP_DRAW, sHubTitle);
    AddTextPrinterParameterized3(sHubWindow, FONT_SMALL, 156, 8, mutedColors, TEXT_SKIP_DRAW, sHubHome);
    HubRect(6, 197, 10, 13, 7);
    HubRect(8, 199, 12, 9, 3);
    HubRect(6, 210, 12, 2, 3);
    for (i = 0; i < 5; i++)
        DrawHubApp(i, FALSE);
    AddTextPrinterParameterized3(sHubWindow, FONT_SMALL, 66, 126, mutedColors, TEXT_SKIP_DRAW, sHubHint);
    PutWindowTilemap(sHubWindow);
    // Upload once after drawing all labels; per-label copies stall rapid input.
    CopyWindowToVram(sHubWindow, COPYWIN_FULL);
}

static void CloseHub(void)
{
    ClearWindowTilemap(sHubWindow);
    RemoveWindow(sHubWindow);
    sHubWindow = WINDOW_NONE;
    CpuCopy16(sHubPalette, &gPlttBufferUnfaded[BG_PLTT_ID(11)], 32);
    CpuCopy16(sHubPalette + 16, &gPlttBufferFaded[BG_PLTT_ID(11)], 32);
    SetGpuReg(REG_OFFSET_BLDCNT, sHubBlend[0]);
    SetGpuReg(REG_OFFSET_BLDALPHA, sHubBlend[1]);
    SetGpuReg(REG_OFFSET_BLDY, sHubBlend[2]);
    SetGpuReg(REG_OFFSET_WININ, sHubBlend[3]);
    SetGpuReg(REG_OFFSET_WINOUT, sHubBlend[4]);
    ScheduleBgCopyTilemapToVram(0);
}

static void Task_PokeGlassHub(u8 taskId)
{
    u8 oldCursor = sHubCursor;
    if (gPaletteFade.active)
        return;
    if (gTasks[taskId].data[1] < 8)
    {
        gTasks[taskId].data[1]++;
        return;
    }
    if (JOY_NEW(B_BUTTON) && !gTasks[taskId].data[0])
        gSpecialVar_Result = SCR_MENU_CANCEL;
    else if (JOY_NEW(A_BUTTON))
        gSpecialVar_Result = sHubCursor;
    else
    {
        if (JOY_NEW(DPAD_UP) && sHubCursor >= 2)
            sHubCursor -= 2;
        else if (JOY_NEW(DPAD_DOWN) && sHubCursor < 4)
            sHubCursor = sHubCursor >= 2 ? 4 : sHubCursor + 2;
        else if (JOY_NEW(DPAD_LEFT) && sHubCursor < 4)
            sHubCursor &= ~1;
        else if (JOY_NEW(DPAD_RIGHT) && sHubCursor < 4)
            sHubCursor |= 1;
        if (oldCursor != sHubCursor)
        {
            PlaySE(SE_SELECT);
            DrawHubApp(oldCursor, TRUE);
            DrawHubApp(sHubCursor, TRUE);
        }
        return;
    }
    PlaySE(SE_SELECT);
    CloseHub();
    DestroyTask(taskId);
    ScriptContext_Enable();
}

void ShowPokeGlassHub(bool8 ignoreBPress)
{
    u8 taskId;
    sHubWindow = AddWindow(&sHubTemplate);
    if (sHubWindow == WINDOW_NONE)
    {
        gSpecialVar_Result = SCR_MENU_CANCEL;
        ScriptContext_Enable();
        return;
    }
    sHubBlend[0] = GetGpuReg(REG_OFFSET_BLDCNT);
    sHubBlend[1] = GetGpuReg(REG_OFFSET_BLDALPHA);
    sHubBlend[2] = GetGpuReg(REG_OFFSET_BLDY);
    sHubBlend[3] = GetGpuReg(REG_OFFSET_WININ);
    sHubBlend[4] = GetGpuReg(REG_OFFSET_WINOUT);
    SetGpuRegBits(REG_OFFSET_WININ, WININ_WIN0_CLR | WININ_WIN1_CLR);
    SetGpuRegBits(REG_OFFSET_WINOUT, WINOUT_WIN01_CLR | WINOUT_WINOBJ_CLR);
    CpuCopy16(&gPlttBufferUnfaded[BG_PLTT_ID(11)], sHubPalette, 32);
    CpuCopy16(&gPlttBufferFaded[BG_PLTT_ID(11)], sHubPalette + 16, 32);
    LoadPalette(sHubColors, BG_PLTT_ID(11), sizeof(sHubColors));
    SetGpuReg(REG_OFFSET_BLDCNT, BLDCNT_TGT1_BG0 | BLDCNT_EFFECT_BLEND
        | BLDCNT_TGT2_BG1 | BLDCNT_TGT2_BG2 | BLDCNT_TGT2_BG3 | BLDCNT_TGT2_OBJ | BLDCNT_TGT2_BD);
    SetGpuReg(REG_OFFSET_BLDALPHA, BLDALPHA_BLEND(12, 6));
    DrawHub();
    taskId = CreateTask(Task_PokeGlassHub, 80);
    gTasks[taskId].data[0] = ignoreBPress;
}
