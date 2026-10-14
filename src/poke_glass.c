#include "global.h"
#include "avatar.h"
#include "data.h"
#include "gflib.h"
#include "menu.h"
#include "poke_glass.h"
#include "pokemon.h"
#include "event_data.h"
#include "script.h"
#include "sound.h"
#include "task.h"
#include "string_util.h"
#include "trainer_pokemon_sprites.h"
#include "decompress.h"
#include "pokedex.h"
#include "pokedex_screen.h"
#include "battle_main.h"
#include "wild_encounter.h"
#include "overworld.h"
#include "region_map.h"
#include "constants/characters.h"
#include "constants/pokedex.h"
#include "constants/region_map_sections.h"

static EWRAM_DATA u8 *sFieldBackdrop = NULL;
static EWRAM_DATA u16 sFieldBackdropPalette[16] = {0};

void ReleasePokeGlassBackdrop(void)
{
    if (sFieldBackdrop != NULL)
        Free(sFieldBackdrop);
    sFieldBackdrop = NULL;
}

// Capture only for screens that replace the field's VRAM. Walk tile rows,
// rather than resolving three tilemaps independently for every screen pixel.
static u8 ClosestBackdropColor(u16 color)
{
    u32 j, best = 1, distance = 0xFFFFFFFF;
    for (j = 1; j < 16; j++)
    {
        u16 target = sFieldBackdropPalette[j];
        s32 r = (color & 31) - (target & 31);
        s32 g = ((color >> 5) & 31) - ((target >> 5) & 31);
        s32 b = ((color >> 10) & 31) - ((target >> 10) & 31);
        u32 d = r * r + g * g + b * b;
        if (d < distance) { distance = d; best = j; }
    }
    return best;
}

// First pass counts visible character colors; second pass draws them using
// the selected palette. Offscreen sprites never incur palette matching work.
static void CaptureBackdropSprites(u32 *counts)
{
    static const u8 widths[3][4] = {{8,16,32,64}, {16,32,32,64}, {8,8,16,32}};
    static const u8 heights[3][4] = {{8,16,32,64}, {8,8,16,32}, {16,32,32,64}};
    const u8 *vram = (const u8 *)VRAM;
    u32 i, x, y, j;
    bool8 oneDimensional = GetGpuReg(REG_OFFSET_DISPCNT) & DISPCNT_OBJ_1D_MAP ? TRUE : FALSE;
    for (i = MAX_SPRITES; i-- > 0;)
    {
        const struct Sprite *sprite = &gSprites[i];
        u8 colors[16];
        u32 width, height, palette;
        s32 left, top;
        if (!sprite->inUse || sprite->invisible || sprite->oam.affineMode != 0
            || sprite->oam.objMode != 0 || sprite->oam.bpp || sprite->oam.shape >= 3)
            continue;
        width = widths[sprite->oam.shape][sprite->oam.size];
        height = heights[sprite->oam.shape][sprite->oam.size];
        left = sprite->x + sprite->x2 + sprite->centerToCornerVecX;
        top = sprite->y + sprite->y2 + sprite->centerToCornerVecY;
        if (sprite->coordOffsetEnabled) { left += gSpriteCoordOffsetX; top += gSpriteCoordOffsetY; }
        if (left >= 240 || top >= 160 || left + (s32)width <= 0 || top + (s32)height <= 0)
            continue;
        palette = OBJ_PLTT_ID(sprite->oam.paletteNum);
        if (counts == NULL)
            for (j = 1; j < 16; j++)
                colors[j] = ClosestBackdropColor(gPlttBufferFaded[palette + j]);
        for (y = 0; y < height; y++)
        {
            s32 dy = top + y;
            u32 py = sprite->vFlip ? height - 1 - y : y;
            if (dy < 0 || dy >= 160) continue;
            for (x = 0; x < width; x++)
            {
                s32 dx = left + x;
                u32 px = sprite->hFlip ? width - 1 - x : x;
                u32 tile = sprite->oam.tileNum + (py / 8) * (oneDimensional ? width / 8 : 32) + px / 8;
                u32 offset, shift;
                u8 color;
                if (dx < 0 || dx >= 240) continue;
                color = (vram[0x10000 + tile * 32 + (py & 7) * 4 + (px & 7) / 2] >> ((px & 1) * 4)) & 15;
                if (!color) continue;
                if (counts != NULL)
                    counts[palette + color]++;
                else
                {
                    offset = ((dy / 8) * 30 + dx / 8) * 32 + (dy & 7) * 4 + (dx & 7) / 2;
                    shift = (dx & 1) * 4;
                    sFieldBackdrop[offset] = (sFieldBackdrop[offset] & ~(15 << shift)) | (colors[color] << shift);
                }
            }
        }
    }
}

void CapturePokeGlassBackdrop(void)
{
    u8 *pixels = AllocZeroed(240 * 160);
    u32 counts[512] = {0};
    u8 remap[256];
    u32 x, y, i, j;
    s32 priority, bg;
    u16 display = GetGpuReg(REG_OFFSET_DISPCNT);
    const u8 *vram = (const u8 *)VRAM;
    if (pixels == NULL) return;
    if (sFieldBackdrop == NULL) sFieldBackdrop = Alloc(240 * 160 / 2);
    if (sFieldBackdrop == NULL) { Free(pixels); return; }
    // Lower priority layers first; lower BG numbers win ties.
    for (priority = 3; priority >= 0; priority--)
        for (bg = 3; bg >= 1; bg--)
        {
            u16 control = GetGpuReg(REG_OFFSET_BG0CNT + bg * 2);
            u32 scrollX, scrollY, widthMask, heightMask, blockStride;
            const u16 *map;
            const u8 *tiles;
            if (!(display & (0x100 << bg)) || (control & 3) != priority) continue;
            scrollX = GetGpuReg(REG_OFFSET_BG0HOFS + bg * 4);
            scrollY = GetGpuReg(REG_OFFSET_BG0VOFS + bg * 4);
            widthMask = control & 0x4000 ? 511 : 255;
            heightMask = control & 0x8000 ? 511 : 255;
            blockStride = control & 0x4000 ? 2048 : 1024;
            map = (const u16 *)(vram + ((control >> 8) & 31) * 0x800);
            tiles = vram + ((control >> 2) & 3) * 0x4000;
            for (y = 0; y < 160; y++)
            {
                u32 sy = (y + scrollY) & heightMask;
                u32 row = (sy >> 8) * blockStride + ((sy & 248) << 2);
                u8 *dest = pixels + y * 240;
                for (x = 0; x < 240;)
                {
                    u32 sx = (x + scrollX) & widthMask;
                    u16 tile = map[row + (sx >> 8) * 1024 + ((sx & 255) >> 3)];
                    u32 py = tile & 0x800 ? 7 - (sy & 7) : sy & 7;
                    u32 count = 8 - (sx & 7), px = sx & 7;
                    const u8 *gfx = tiles + (tile & 1023) * 32 + py * 4;
                    u8 palette = (tile >> 12) * 16;
                    if (count > 240 - x) count = 240 - x;
                    for (j = 0; j < count; j++, px++, x++)
                    {
                        u32 tx = tile & 0x400 ? 7 - px : px;
                        u8 color = (gfx[tx >> 1] >> ((tx & 1) * 4)) & 15;
                        if (color) dest[x] = palette + color;
                    }
                }
            }
        }
    for (i = 0; i < 240 * 160; i++) counts[pixels[i]]++;
    CaptureBackdropSprites(counts);
    sFieldBackdropPalette[0] = gPlttBufferFaded[0] & 0x7FFF;
    counts[0] = 0;
    for (i = 1; i < 16; i++)
    {
        u32 best = 1;
        for (j = 2; j < 512; j++)
            if (counts[j] > counts[best]) best = j;
        sFieldBackdropPalette[i] = gPlttBufferFaded[best] & 0x7FFF;
        counts[best] = 0;
    }
    for (i = 0; i < 256; i++) remap[i] = ClosestBackdropColor(gPlttBufferFaded[i]);
    for (y = 0; y < 160; y++)
        for (x = 0; x < 240; x += 2)
        {
            u32 offset = ((y / 8) * 30 + x / 8) * 32 + (y & 7) * 4 + (x & 7) / 2;
            sFieldBackdrop[offset] = remap[pixels[y * 240 + x]] | (remap[pixels[y * 240 + x + 1]] << 4);
        }
    CaptureBackdropSprites(NULL);
    Free(pixels);
}

void LoadPokeGlassBackdrop(void)
{
    u16 map[32 * 32] = {0};
    u32 x, y;
    if (sFieldBackdrop == NULL)
        return;
    CpuCopy16(sFieldBackdrop, (void *)(VRAM + 0x8000), 240 * 160 / 2);
    LoadPalette(sFieldBackdropPalette, BG_PLTT_ID(10), sizeof(sFieldBackdropPalette));
    for (y = 0; y < 20; y++)
        for (x = 0; x < 30; x++)
            map[y * 32 + x] = (10 << 12) | (y * 30 + x);
    CpuCopy16(map, (void *)(VRAM + 27 * 0x800), sizeof(map));
    SetGpuReg(REG_OFFSET_BG3CNT, (2 << 2) | (27 << 8) | 3);
    SetGpuReg(REG_OFFSET_BG3HOFS, 0);
    SetGpuReg(REG_OFFSET_BG3VOFS, 0);
    SetGpuRegBits(REG_OFFSET_DISPCNT, DISPCNT_BG3_ON);
    SetPokeGlassBlend(FALSE);
}
#include "constants/menu.h"
#include "constants/songs.h"

static const u16 sPalette[16] = {
    RGB(0,0,0), RGB(2,2,3), RGB(5,5,7), RGB(11,12,14), RGB(0,6,11), RGB(0,16,24), RGB(8,25,29), RGB(15,29,31), RGB(26,31,31), RGB(22,2,5), RGB(31,5,7), RGB(31,14,15), RGB(20,21,24), RGB(28,29,30), RGB(14,16,19), RGB(31,31,31)
};

// The field hub owns one BG0 window. Hardware alpha blending keeps the map and
// player visible through the glass; restore field/weather registers on every exit.

static EWRAM_DATA u8 sHubWindow = 0;
static EWRAM_DATA u8 sHubCursor = 0;
static EWRAM_DATA u16 sHubBlend[8] = {0};
static EWRAM_DATA u16 sHubPalette[32] = {0};
static const u8 sHubTitle[] = _("POKéGLASS");
static const u8 sHubHint[] = _("A Open   B Close");
static const u8 sHubLabels[][16] = {
    _("Pokédex"), _("Party"), _("Storage"), _("Stats"), _("Map"), _("Wardrobe")
};
static const struct WindowTemplate sHubTemplate = {
    .bg = 0, .tilemapLeft = 1, .tilemapTop = 1,
    .width = 28, .height = 18, .paletteNum = 11, .baseBlock = 0x038,
};

static void TabletRect(u8 *pixels, u8 color, u16 x, u16 y, u16 width, u16 height)
{
    u32 py, px, fill = 0x11111111 * color;
    // The hub redraws large rectangles. Fill each aligned eight-pixel tile
    // row in one write, handling only its edges a pixel at a time.
    for (py = y; py < y + height; py++)
        for (px = x; px < x + width;)
        {
            u32 offset = ((py / 8) * 28 + px / 8) * 32 + (py & 7) * 4 + (px & 7) / 2;
            if (!(px & 7) && px + 8 <= x + width)
            {
                *(u32 *)(pixels + offset) = fill;
                px += 8;
            }
            else
            {
                u32 shift = (px & 1) * 4;
                pixels[offset] = (pixels[offset] & ~(15 << shift)) | (color << shift);
                px++;
            }
        }
}

static void HubRect(u8 color, u16 x, u16 y, u16 width, u16 height)
{
    TabletRect((u8 *)GetWindowAttribute(sHubWindow, WINDOW_TILE_DATA), color, x, y, width, height);
}

// Only the glass blends. The shell and corner grips remain solid, and party
// cards/sprites are clipped to the display during switching animations.
void SetPokeGlassBlend(bool8 field)
{
    SetGpuReg(REG_OFFSET_WIN1H, WIN_RANGE(20, 220));
    SetGpuReg(REG_OFFSET_WIN1V, WIN_RANGE(23, 136));
    SetGpuReg(REG_OFFSET_WININ, WININ_WIN1_BG_ALL | WININ_WIN1_OBJ | WININ_WIN1_CLR);
    SetGpuReg(REG_OFFSET_WINOUT, field ? WINOUT_WIN01_BG_ALL | WINOUT_WIN01_OBJ
        : WINOUT_WIN01_BG1 | WINOUT_WIN01_BG3);
    ClearGpuRegBits(REG_OFFSET_DISPCNT, DISPCNT_WIN0_ON | DISPCNT_OBJWIN_ON);
    SetGpuRegBits(REG_OFFSET_DISPCNT, DISPCNT_WIN1_ON);
    SetGpuReg(REG_OFFSET_BLDCNT, BLDCNT_TGT1_BG0 | (field ? 0 : BLDCNT_TGT1_BG1)
        | BLDCNT_EFFECT_BLEND | (field ? BLDCNT_TGT2_BG1 | BLDCNT_TGT2_BG2
        | BLDCNT_TGT2_BG3 | BLDCNT_TGT2_OBJ | BLDCNT_TGT2_BD : BLDCNT_TGT2_BG3));
    SetGpuReg(REG_OFFSET_BLDALPHA, BLDALPHA_BLEND(12, 6));
}

// Cyan pictograms echo the reference tablet at native GBA pixel resolution.
static void DrawHubIcon(u8 app, u16 x, u16 y)
{
    switch (app)
    {
    case 0: // Pokédex: a Poké Ball.
        HubRect(8, x + 8, y, 8, 2);
        HubRect(8, x + 5, y + 2, 14, 3);
        HubRect(8, x + 2, y + 5, 20, 4);
        HubRect(8, x, y + 9, 24, 6);
        HubRect(8, x + 2, y + 15, 20, 4);
        HubRect(8, x + 5, y + 19, 14, 3);
        HubRect(8, x + 8, y + 22, 8, 2);
        HubRect(5, x, y + 11, 24, 2);
        HubRect(5, x + 8, y + 8, 8, 8);
        HubRect(8, x + 10, y + 10, 4, 4);
        break;
    case 1: // Party: pointed ears and a rounded Pokémon head.
        HubRect(8, x + 2, y + 1, 3, 9);
        HubRect(8, x + 19, y + 1, 3, 9);
        HubRect(8, x + 4, y + 5, 3, 8);
        HubRect(8, x + 17, y + 5, 3, 8);
        HubRect(8, x + 3, y + 9, 18, 10);
        HubRect(8, x + 6, y + 19, 12, 3);
        break;
    case 2: // PC storage: a box with a handle and inset drawer.
        HubRect(8, x + 7, y + 1, 10, 3);
        HubRect(8, x + 5, y + 3, 3, 5);
        HubRect(8, x + 16, y + 3, 3, 5);
        HubRect(8, x + 3, y + 7, 18, 16);
        HubRect(5, x + 7, y + 11, 10, 9);
        HubRect(8, x + 10, y + 13, 4, 2);
        break;
    case 3: // Existing stats shortcut remains available in the dock.
        HubRect(8, x + 2, y + 16, 20, 2);
        HubRect(8, x + 3, y + 10, 4, 6);
        HubRect(8, x + 10, y + 6, 4, 10);
        HubRect(8, x + 17, y + 1, 4, 15);
        break;
    case 4: // Map: a location pin on a folded map.
        HubRect(8, x + 1, y + 17, 7, 5);
        HubRect(8, x + 16, y + 17, 7, 5);
        HubRect(8, x + 3, y + 22, 18, 2);
        HubRect(8, x + 8, y + 1, 8, 12);
        HubRect(8, x + 6, y + 4, 12, 6);
        HubRect(5, x + 10, y + 4, 4, 4);
        HubRect(8, x + 9, y + 13, 6, 3);
        HubRect(8, x + 11, y + 16, 2, 3);
        break;
    }
}

static void DrawHubApp(u8 i, bool8 upload)
{
    static const u8 textColors[] = {0, 8, 4};
    static const u8 positions[6][2] = {{25,34}, {127,34}, {25,78}, {112,116}, {127,78}, {152,116}};
    u16 x = positions[i][0], y = positions[i][1];
    bool8 selected = i == sHubCursor;
    u8 dockWidth = i == 5 ? 54 : 36;
    if (i == 3 || i == 5)
    {
        HubRect(selected ? 8 : 6, x, y, dockWidth, 10);
        HubRect(4, x + 1, y + 1, dockWidth - 2, 8);
        AddTextPrinterParameterized3(sHubWindow, FONT_SMALL, x + 4, y - 1, textColors, TEXT_SKIP_DRAW, sHubLabels[i]);
    }
    else
    {
        HubRect(selected ? 8 : 6, x, y, 72, 38);
        HubRect(selected ? 5 : 4, x + 2, y + 2, 68, 34);
        DrawHubIcon(i, x + 8, y + 7);
        AddTextPrinterParameterized3(sHubWindow, FONT_SMALL, x + 35, y + 13, textColors, TEXT_SKIP_DRAW, sHubLabels[i]);
    }
    if (upload)
        CopyWindowRectToVram(sHubWindow, COPYWIN_GFX, x / 8, y / 8, (x + ((i == 3 || i == 5) ? dockWidth : 72) + 7) / 8 - x / 8, (y + (i == 3 ? 10 : 38) + 7) / 8 - y / 8);
}

static void DrawTabletShell(u8 *pixels)
{
    u8 i;
    CpuFill16(0, pixels, 28 * 18 * 32);
    // Ivory shell, red corner grips, graphite bezel, and transparent blue glass.
    TabletRect(pixels, 1, 4, 0, 216, 144);
    TabletRect(pixels, 1, 0, 4, 224, 136);
    TabletRect(pixels, 12, 4, 2, 216, 140);
    TabletRect(pixels, 13, 3, 4, 218, 136);
    TabletRect(pixels, 15, 24, 3, 176, 1);
    for (i = 0; i < 4; i++)
    {
        u16 x = (i & 1) ? 200 : 1;
        u16 y = (i & 2) ? 121 : 1;
        TabletRect(pixels, 9, x, y, 23, 22);
        TabletRect(pixels, 10, x + 2, y + 2, 19, 18);
        TabletRect(pixels, 11, x + 4, y + 3, 15, 2);
    }
    TabletRect(pixels, 2, 8, 11, 208, 120);
    TabletRect(pixels, 3, 10, 12, 204, 1);
    TabletRect(pixels, 4, 12, 15, 200, 113);
    TabletRect(pixels, 6, 13, 16, 20, 1);
    TabletRect(pixels, 7, 13, 17, 12, 1);
    // Camera and home button match the bag and startup tablet.
    TabletRect(pixels, 1, 104, 4, 16, 4);
    TabletRect(pixels, 7, 111, 5, 2, 2);
    TabletRect(pixels, 1, 103, 132, 18, 10);
    TabletRect(pixels, 10, 106, 133, 12, 4);
    TabletRect(pixels, 15, 106, 138, 12, 3);
    TabletRect(pixels, 1, 103, 137, 18, 1);
    TabletRect(pixels, 15, 110, 136, 4, 3);
}

void DrawPokeGlassFrame(u8 bg)
{
    u8 x, y;
    u16 count = 1, tile;
    u8 *pixels = AllocZeroed(28 * 18 * 32);
    u8 *tiles = AllocZeroed(128 * 32);
    if (pixels == NULL || tiles == NULL)
    {
        Free(pixels);
        Free(tiles);
        return;
    }
    DrawTabletShell(pixels);
    // Cards blend directly with the captured field instead of an opaque
    // second copy of the glass on BG1. Their pixels supply its blue tint.
    TabletRect(pixels, 0, 16, 16, 192, 96);
    FillBgTilemapBufferRect(bg, 0x180, 0, 0, 32, 32, 11);
    for (y = 0; y < 18; y++)
        for (x = 0; x < 28; x++)
        {
            const u8 *source = pixels + (y * 28 + x) * 32;
            for (tile = 0; tile < count; tile++)
                if (memcmp(source, tiles + tile * 32, 32) == 0)
                    break;
            if (tile == count)
            {
                if (count == 128)
                {
                    Free(pixels);
                    Free(tiles);
                    return;
                }
                CpuCopy16(source, tiles + count * 32, 32);
                count++;
            }
            FillBgTilemapBufferRect(bg, 0x180 + tile, x + 1, y + 1, 1, 1, 11);
        }
    // Deduplicate the shared shell into the reserved final 4 KiB of char
    // block 1. Party windows use the space below; the backdrop starts at 0x8000.
    LoadPalette(sPalette, BG_PLTT_ID(11), sizeof(sPalette));
    CpuCopy16(tiles, (void *)(VRAM + 0x7000), count * 32);
    Free(pixels);
    Free(tiles);
    ScheduleBgCopyTilemapToVram(bg);
}

static void DrawHub(void)
{
    static const u8 textColors[] = {0, 8, 4};
    u8 i;
    DrawTabletShell((u8 *)GetWindowAttribute(sHubWindow, WINDOW_TILE_DATA));
    AddTextPrinterParameterized3(sHubWindow, FONT_SMALL, 75, 18, textColors, TEXT_SKIP_DRAW, sHubTitle);
    // Signal and battery indicators on the glass.
    for (i = 0; i < 3; i++) HubRect(8, 176 + i * 4, 26 - i * 2, 2, 2 + i * 2);
    HubRect(8, 191, 20, 16, 7);
    HubRect(4, 192, 21, 14, 5);
    HubRect(6, 193, 22, 10, 3);
    for (i = 0; i < 6; i++) DrawHubApp(i, FALSE);
    AddTextPrinterParameterized3(sHubWindow, FONT_SMALL, 24, 114, textColors, TEXT_SKIP_DRAW, sHubHint);
    PutWindowTilemap(sHubWindow);
    CopyWindowToVram(sHubWindow, COPYWIN_FULL);
}

static void CloseHub(void)
{
    ClearWindowTilemap(sHubWindow);
    RemoveWindow(sHubWindow);
    sHubWindow = WINDOW_NONE;
    ScheduleBgCopyTilemapToVram(0);
}

static void RestoreTabletAppearance(void)
{
    CpuCopy16(sHubPalette, &gPlttBufferUnfaded[BG_PLTT_ID(11)], 32);
    CpuCopy16(sHubPalette + 16, &gPlttBufferFaded[BG_PLTT_ID(11)], 32);
    SetGpuReg(REG_OFFSET_BLDCNT, sHubBlend[0]);
    SetGpuReg(REG_OFFSET_BLDALPHA, sHubBlend[1]);
    SetGpuReg(REG_OFFSET_BLDY, sHubBlend[2]);
    SetGpuReg(REG_OFFSET_WININ, sHubBlend[3]);
    SetGpuReg(REG_OFFSET_WINOUT, sHubBlend[4]);
    SetGpuReg(REG_OFFSET_WIN1H, sHubBlend[5]);
    SetGpuReg(REG_OFFSET_WIN1V, sHubBlend[6]);
    ClearGpuRegBits(REG_OFFSET_DISPCNT, DISPCNT_WIN0_ON | DISPCNT_WIN1_ON | DISPCNT_OBJWIN_ON);
    SetGpuRegBits(REG_OFFSET_DISPCNT, sHubBlend[7]);
}

static void Task_CloseTablet(u8 taskId)
{
    // Let the cleared tilemap reach VRAM before restoring its old palette.
    // Capture on the following frame, after both changes have reached VBlank.
    if (gTasks[taskId].data[2] == 0)
    {
        RestoreTabletAppearance();
        gTasks[taskId].data[2] = 1;
        return;
    }
    if (gTasks[taskId].data[3])
        CapturePokeGlassBackdrop();
    DestroyTask(taskId);
    ScriptContext_Enable();
}

static void Task_PokeGlassHub(u8 taskId)
{
    u8 oldCursor = sHubCursor;
    if (gPaletteFade.active)
        return;
    if (gTasks[taskId].data[1] < 2)
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
        if (JOY_NEW(DPAD_UP))
            sHubCursor = sHubCursor == 2 ? 0 : sHubCursor == 4 ? 1 : (sHubCursor == 3 || sHubCursor == 5) ? 4 : sHubCursor;
        else if (JOY_NEW(DPAD_DOWN))
            sHubCursor = sHubCursor == 0 ? 2 : sHubCursor == 1 ? 4 : (sHubCursor == 3 || sHubCursor == 5) ? 5 : 3;
        else if (JOY_NEW(DPAD_LEFT))
            sHubCursor = sHubCursor == 1 ? 0 : sHubCursor == 4 ? 2 : sHubCursor == 5 ? 3 : sHubCursor;
        else if (JOY_NEW(DPAD_RIGHT))
            sHubCursor = sHubCursor == 0 ? 1 : sHubCursor == 2 ? 4 : sHubCursor == 3 ? 5 : sHubCursor;
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
    gTasks[taskId].data[2] = 0;
    gTasks[taskId].data[3] = gSpecialVar_Result == 1 && gPlayerPartyCount != 0;
    gTasks[taskId].func = Task_CloseTablet;
    if (gSpecialVar_Result == SCR_MENU_CANCEL)
        ReleasePokeGlassBackdrop();
}

static bool8 OpenTabletWindow(void)
{
    sHubWindow = AddWindow(&sHubTemplate);
    if (sHubWindow == WINDOW_NONE)
    {
        gSpecialVar_Result = SCR_MENU_CANCEL;
        ScriptContext_Enable();
        return FALSE;
    }
    sHubBlend[0] = GetGpuReg(REG_OFFSET_BLDCNT);
    sHubBlend[1] = GetGpuReg(REG_OFFSET_BLDALPHA);
    sHubBlend[2] = GetGpuReg(REG_OFFSET_BLDY);
    sHubBlend[3] = GetGpuReg(REG_OFFSET_WININ);
    sHubBlend[4] = GetGpuReg(REG_OFFSET_WINOUT);
    sHubBlend[5] = GetGpuReg(REG_OFFSET_WIN1H);
    sHubBlend[6] = GetGpuReg(REG_OFFSET_WIN1V);
    sHubBlend[7] = GetGpuReg(REG_OFFSET_DISPCNT) & (DISPCNT_WIN0_ON | DISPCNT_WIN1_ON | DISPCNT_OBJWIN_ON);
    CpuCopy16(&gPlttBufferUnfaded[BG_PLTT_ID(11)], sHubPalette, 32);
    CpuCopy16(&gPlttBufferFaded[BG_PLTT_ID(11)], sHubPalette + 16, 32);
    LoadPalette(sPalette, BG_PLTT_ID(11), sizeof(sPalette));
    SetPokeGlassBlend(TRUE);
    // Storage's field menu can leave a frame outside our inset window.
    // BG0 belongs to menus here; clear it before drawing the tablet again.
    FillBgTilemapBufferRect(0, 0, 0, 0, 32, 32, 0);
    return TRUE;
}

void ShowPokeGlassHub(bool8 ignoreBPress)
{
    u8 taskId;
    if (!OpenTabletWindow())
        return;
    DrawHub();
    taskId = CreateTask(Task_PokeGlassHub, 80);
    if (taskId == TASK_NONE)
    {
        CloseHub();
        RestoreTabletAppearance();
        gSpecialVar_Result = SCR_MENU_CANCEL;
        ScriptContext_Enable();
        return;
    }
    gTasks[taskId].data[0] = ignoreBPress;
}


#define TAG_POKEGLASS_STATS_MON 0xD10F
static EWRAM_DATA u8 sStatsPartySlot = 0;
static EWRAM_DATA u16 sStatsMonSprite = 0;
static const u8 sStatsLabels[6][12] = {
    _("HP"), _("Attack"), _("Defense"), _("Sp. Atk"), _("Sp. Def"), _("Speed")
};
static const u8 sStatsFields[6][3] = {
    {MON_DATA_MAX_HP, MON_DATA_HP_EV, MON_DATA_HP_IV},
    {MON_DATA_ATK, MON_DATA_ATK_EV, MON_DATA_ATK_IV},
    {MON_DATA_DEF, MON_DATA_DEF_EV, MON_DATA_DEF_IV},
    {MON_DATA_SPATK, MON_DATA_SPATK_EV, MON_DATA_SPATK_IV},
    {MON_DATA_SPDEF, MON_DATA_SPDEF_EV, MON_DATA_SPDEF_IV},
    {MON_DATA_SPEED, MON_DATA_SPEED_EV, MON_DATA_SPEED_IV},
};
static const u8 sStatsValueHeader[] = _("Stat");
static const u8 sStatsEVHeader[] = _("EV");
static const u8 sStatsIVHeader[] = _("IV");
static const u8 sStatsAbility[] = _("Ability:");
static const u8 sStatsHint[] = _("Left/Right: Pokémon   B Back");
static const u8 sStatsEggAbility[] = _("Unknown");
static const u8 sStatsDash[] = _("-");
static const u8 sStatsLevel[] = _("Lv.");

static void StatsText(u16 x, u16 y, const u8 *text)
{
    static const u8 colors[] = {0, 8, 4};
    AddTextPrinterParameterized3(sHubWindow, FONT_SMALL, x, y, colors, TEXT_SKIP_DRAW, text);
}

static void StatsNumber(u16 right, u16 y, u16 value)
{
    u8 text[6];
    ConvertIntToDecimalStringN(text, value, STR_CONV_MODE_LEFT_ALIGN, 5);
    StatsText(right - GetStringWidth(FONT_SMALL, text, 0), y, text);
}

static void DestroyStatsMonSprite(void)
{
    if (sStatsMonSprite != 0xFFFF)
        FreeAndDestroyMonPicSpriteNoPalette(sStatsMonSprite);
    FreeSpritePaletteByTag(TAG_POKEGLASS_STATS_MON);
    sStatsMonSprite = 0xFFFF;
}

static void DrawStatsPage(void)
{
    struct Pokemon *mon = &gPlayerParty[sStatsPartySlot];
    u8 nickname[POKEMON_NAME_LENGTH + 1];
    u8 row, column;
    u8 paletteSlot;
    bool8 isEgg = GetMonData(mon, MON_DATA_IS_EGG);
    static const u8 rightEdges[] = {160, 185, 207};
    DrawTabletShell((u8 *)GetWindowAttribute(sHubWindow, WINDOW_TILE_DATA));
    GetMonData(mon, MON_DATA_NICKNAME, nickname);
    StringGet_Nickname(nickname);
    StatsText(17, 18, nickname);
    if (!isEgg)
    {
        StatsText(17, 29, sStatsLevel);
        StatsNumber(52, 29, GetMonData(mon, MON_DATA_LEVEL));
    }
    StatsNumber(76, 29, sStatsPartySlot + 1);
    // Clear column headings and thin rules keep all six rows on one page.
    HubRect(6, 90, 16, 120, 84);
    HubRect(4, 91, 17, 118, 82);
    StatsText(137, 18, sStatsValueHeader);
    StatsText(173, 18, sStatsEVHeader);
    StatsText(195, 18, sStatsIVHeader);
    HubRect(6, 92, 31, 116, 1);
    for (row = 0; row < 6; row++)
    {
        u16 y = 33 + row * 11;
        HubRect((row & 1) ? 4 : 5, 92, y, 116, 11);
        StatsText(94, y, sStatsLabels[row]);
        for (column = 0; column < 3; column++)
        {
            if (isEgg)
                StatsText(rightEdges[column] - 4, y, sStatsDash);
            else
                StatsNumber(rightEdges[column], y, GetMonData(mon, sStatsFields[row][column]));
        }
    }
    HubRect(6, 17, 101, 190, 1);
    StatsText(18, 102, sStatsAbility);
    StatsText(64, 102, isEgg ? sStatsEggAbility : gAbilitiesInfo[GetMonAbility(mon)].name);
    StatsText(28, 114, sStatsHint);
    PutWindowTilemap(sHubWindow);
    CopyWindowToVram(sHubWindow, COPYWIN_FULL);
    // Reuse the portrait buffer and OBJ tiles when changing party members.
    // This keeps allocation and sprite creation out of repeated navigation.
    if (sStatsMonSprite != 0xFFFF)
    {
        paletteSlot = IndexOfSpritePaletteTag(TAG_POKEGLASS_STATS_MON);
        LoadPalette(GetMonSpritePalFromSpeciesAndPersonality(GetMonData(mon, MON_DATA_SPECIES_OR_EGG),
            GetMonData(mon, MON_DATA_IS_SHINY), GetMonData(mon, MON_DATA_PERSONALITY)),
            OBJ_PLTT_ID(paletteSlot), PLTT_SIZE_4BPP);
        LoadSpecialPokePic((void *)gSprites[sStatsMonSprite].images[0].data,
            GetMonData(mon, MON_DATA_SPECIES_OR_EGG), GetMonData(mon, MON_DATA_PERSONALITY), TRUE);
        StartSpriteAnim(&gSprites[sStatsMonSprite], 0);
        return;
    }
    // Reserve a private OBJ slot. The generic portrait helper's tagged path
    // loads a species tag, so use its explicit-slot path for this overlay.
    paletteSlot = LoadSpritePaletteWithTag(GetMonSpritePalFromSpeciesAndPersonality(
        GetMonData(mon, MON_DATA_SPECIES_OR_EGG), GetMonData(mon, MON_DATA_IS_SHINY),
        GetMonData(mon, MON_DATA_PERSONALITY)), TAG_POKEGLASS_STATS_MON);
    if (paletteSlot == 0xFF)
        return;
    sStatsMonSprite = CreateMonPicSprite(GetMonData(mon, MON_DATA_SPECIES_OR_EGG),
        GetMonData(mon, MON_DATA_IS_SHINY), GetMonData(mon, MON_DATA_PERSONALITY),
        TRUE, 60, 76, paletteSlot, TAG_NONE);
    if (sStatsMonSprite < MAX_SPRITES)
        gSprites[sStatsMonSprite].oam.priority = 0;
    else
    {
        sStatsMonSprite = 0xFFFF;
        FreeSpritePaletteByTag(TAG_POKEGLASS_STATS_MON);
    }
}

static void Task_PokeGlassStats(u8 taskId)
{
    u8 previous = sStatsPartySlot;
    if (gPaletteFade.active)
        return;
    if (gTasks[taskId].data[0] < 2)
    {
        gTasks[taskId].data[0]++;
        return;
    }
    if (JOY_NEW(B_BUTTON))
    {
        PlaySE(SE_SELECT);
        DestroyStatsMonSprite();
        CloseHub();
        gTasks[taskId].data[2] = 0;
        gTasks[taskId].data[3] = FALSE;
        gTasks[taskId].func = Task_CloseTablet;
        return;
    }
    if (JOY_NEW(DPAD_LEFT))
        sStatsPartySlot = sStatsPartySlot == 0 ? gPlayerPartyCount - 1 : sStatsPartySlot - 1;
    else if (JOY_NEW(DPAD_RIGHT))
        sStatsPartySlot = (sStatsPartySlot + 1) % gPlayerPartyCount;
    if (previous != sStatsPartySlot)
    {
        PlaySE(SE_SELECT);
        DrawStatsPage();
    }
}

void ShowPokeGlassStats(void)
{
    u8 taskId;
    if (gPlayerPartyCount == 0)
    {
        ScriptContext_Enable();
        return;
    }
    if (!OpenTabletWindow())
        return;
    if (sStatsPartySlot >= gPlayerPartyCount)
        sStatsPartySlot = 0;
    sStatsMonSprite = 0xFFFF;
    DrawStatsPage();
    taskId = CreateTask(Task_PokeGlassStats, 80);
    if (taskId == TASK_NONE)
    {
        DestroyStatsMonSprite();
        CloseHub();
        RestoreTabletAppearance();
        ScriptContext_Enable();
    }
}

#define TAG_POKEGLASS_WARDROBE 0xD110
static EWRAM_DATA u8 sWardrobeLook = 0;
static EWRAM_DATA u16 sWardrobePortrait = 0;

static void DestroyWardrobePortrait(void)
{
    if (sWardrobePortrait != 0xFFFF)
        FreeAndDestroyTrainerPicSprite(sWardrobePortrait);
    FreeSpritePaletteByTag(TAG_POKEGLASS_WARDROBE);
    sWardrobePortrait = 0xFFFF;
}

static void DrawWardrobePage(void)
{
    u8 i, palette;
    u16 pic = GetAvatarFrontPic(sWardrobeLook);
    DrawTabletShell((u8 *)GetWindowAttribute(sHubWindow, WINDOW_TILE_DATA));
    StatsText(17, 18, COMPOUND_STRING("WARDROBE"));
    StatsText(107, 35, GetAvatarLookName(sWardrobeLook));
    StatsText(107, 49, GetAvatarLookStyle(sWardrobeLook));
    StatsText(107, 72, sWardrobeLook == GetCurrentAvatarLook() ? COMPOUND_STRING("Currently worn") : COMPOUND_STRING("Preview"));
    StatsText(107, 88, COMPOUND_STRING("Look"));
    StatsNumber(148, 88, sWardrobeLook + 1);
    StatsText(153, 88, COMPOUND_STRING("/ 4"));
    for (i = 0; i < AVATAR_LOOK_COUNT; i++)
        HubRect(i == sWardrobeLook ? 8 : 6, 107 + i * 14, 103, 6, 3);
    StatsText(30, 114, COMPOUND_STRING("Left/Right: Look   A Wear   B Back"));
    PutWindowTilemap(sHubWindow);
    CopyWindowToVram(sHubWindow, COPYWIN_FULL);
    DestroyWardrobePortrait();
    palette = LoadSpritePaletteWithTag(gTrainerSprites[pic].palette.data, TAG_POKEGLASS_WARDROBE);
    if (palette == 0xFF)
        return;
    sWardrobePortrait = CreateTrainerPicSprite(pic, TRUE, 65, 78, palette, TAG_NONE);
    if (sWardrobePortrait < MAX_SPRITES)
        gSprites[sWardrobePortrait].oam.priority = 0;
    else
    {
        sWardrobePortrait = 0xFFFF;
        FreeSpritePaletteByTag(TAG_POKEGLASS_WARDROBE);
    }
}

static void Task_PokeGlassWardrobe(u8 taskId)
{
    u8 previous = sWardrobeLook;
    if (gPaletteFade.active)
        return;
    if (gTasks[taskId].data[0] < 2)
    {
        gTasks[taskId].data[0]++;
        return;
    }
    if (JOY_NEW(A_BUTTON | B_BUTTON))
    {
        PlaySE(SE_SELECT);
        if (JOY_NEW(A_BUTTON))
            ApplyAvatarLookToField(sWardrobeLook);
        DestroyWardrobePortrait();
        CloseHub();
        gTasks[taskId].data[2] = 0;
        gTasks[taskId].data[3] = FALSE;
        gTasks[taskId].func = Task_CloseTablet;
        return;
    }
    if (JOY_NEW(DPAD_LEFT))
        sWardrobeLook = sWardrobeLook == 0 ? AVATAR_LOOK_COUNT - 1 : sWardrobeLook - 1;
    else if (JOY_NEW(DPAD_RIGHT))
        sWardrobeLook = (sWardrobeLook + 1) % AVATAR_LOOK_COUNT;
    if (previous != sWardrobeLook)
    {
        PlaySE(SE_SELECT);
        DrawWardrobePage();
    }
}

void ShowPokeGlassWardrobe(void)
{
    u8 taskId;
    if (!OpenTabletWindow())
        return;
    sWardrobeLook = GetCurrentAvatarLook();
    sWardrobePortrait = 0xFFFF;
    DrawWardrobePage();
    taskId = CreateTask(Task_PokeGlassWardrobe, 80);
    if (taskId == TASK_NONE)
    {
        DestroyWardrobePortrait();
        CloseHub();
        RestoreTabletAppearance();
        ScriptContext_Enable();
    }
}

#define TAG_POKEGLASS_DEX_MON 0xD111
#define GLASS_DEX_ROWS 6
#define GLASS_DEX_TEXT_LINES 16

struct GlassDex
{
    u16 species[NATIONAL_DEX_COUNT];
    u16 areas[MAPSEC_COUNT];
    u16 count;
    u16 cursor;
    u16 seen;
    u16 caught;
    u16 sprite;
    u16 areaCount;
    u8 areaPage;
    u8 view; // List, entry, or habitat.
    u8 filter; // Seen or caught.
    u8 alphabetical;
    u8 textPage;
    u8 textLines;
    u8 text[GLASS_DEX_TEXT_LINES][64];
};

static EWRAM_DATA struct GlassDex *sGlassDex = NULL;

static void DestroyGlassDexPortrait(void)
{
    if (sGlassDex->sprite != 0xFFFF)
        FreeAndDestroyMonPicSpriteNoPalette(sGlassDex->sprite);
    FreeSpritePaletteByTag(TAG_POKEGLASS_DEX_MON);
    sGlassDex->sprite = 0xFFFF;
}

static void BuildGlassDexList(void)
{
    u16 dex, species, i, j;
    sGlassDex->count = sGlassDex->seen = sGlassDex->caught = 0;
    sGlassDex->cursor = 0;
    for (dex = 1; dex <= NATIONAL_DEX_COUNT; dex++)
    {
        bool8 caught = GetSetPokedexFlag(dex, FLAG_GET_CAUGHT);
        bool8 seen = caught || GetSetPokedexFlag(dex, FLAG_GET_SEEN);
        sGlassDex->seen += seen;
        sGlassDex->caught += caught;
        if (!(sGlassDex->filter ? caught : seen))
            continue;
        species = NationalPokedexNumToSpecies(dex);
        if (species != SPECIES_NONE)
            sGlassDex->species[sGlassDex->count++] = species;
    }
    if (sGlassDex->alphabetical)
        for (i = 1; i < sGlassDex->count; i++)
        {
            species = sGlassDex->species[i];
            for (j = i; j > 0 && StringCompare(gSpeciesInfo[species].speciesName,
                gSpeciesInfo[sGlassDex->species[j - 1]].speciesName) < 0; j--)
                sGlassDex->species[j] = sGlassDex->species[j - 1];
            sGlassDex->species[j] = species;
        }
}

static bool8 GlassDexEncounterHasSpecies(const struct WildPokemonInfo *info, u8 count, u16 species)
{
    u8 i;
    if (info == NULL)
        return FALSE;
    for (i = 0; i < count; i++)
        if (SpeciesToNationalPokedexNum(info->wildPokemon[i].species) == SpeciesToNationalPokedexNum(species))
            return TRUE;
    return FALSE;
}

static void BuildGlassDexAreas(u16 species)
{
    u16 i, area, j;
    u8 season, time;
    sGlassDex->areaCount = sGlassDex->areaPage = 0;
    for (i = 0; gWildMonHeaders[i].mapGroup != 0xFF; i++)
    {
        const struct WildPokemonHeader *header = &gWildMonHeaders[i];
        bool8 found = FALSE;
        for (season = 0; season < NELEMS(header->encounterTypes); season++)
            for (time = 0; time < NELEMS(header->encounterTypes[0]); time++)
            {
                const struct WildEncounterTypes *encounters = &header->encounterTypes[season][time];
                if (GlassDexEncounterHasSpecies(encounters->landMonsInfo, LAND_WILD_COUNT, species)
                 || GlassDexEncounterHasSpecies(encounters->waterMonsInfo, WATER_WILD_COUNT, species)
                 || GlassDexEncounterHasSpecies(encounters->rockSmashMonsInfo, ROCK_WILD_COUNT, species)
                 || GlassDexEncounterHasSpecies(encounters->fishingMonsInfo, FISH_WILD_COUNT, species)
                 || GlassDexEncounterHasSpecies(encounters->hiddenMonsInfo, HIDDEN_WILD_COUNT, species))
                    found = TRUE;
            }
        if (!found)
            continue;
        area = Overworld_GetMapHeaderByGroupAndId(header->mapGroup, header->mapNum)->regionMapSectionId;
        if (area >= MAPSEC_COUNT)
            continue;
        for (j = 0; j < sGlassDex->areaCount && sGlassDex->areas[j] != area; j++);
        if (j == sGlassDex->areaCount && j < MAPSEC_COUNT)
            sGlassDex->areas[sGlassDex->areaCount++] = area;
    }
}

static void BuildGlassDexText(u16 species)
{
    const u8 *source = gSpeciesInfo[species].description;
    u8 word[64], candidate[128];
    u8 line = 0, length;
    sGlassDex->textPage = 0;
    sGlassDex->textLines = 1;
    memset(sGlassDex->text, EOS, sizeof(sGlassDex->text));
    if (!GetSetPokedexFlag(SpeciesToNationalPokedexNum(species), FLAG_GET_CAUGHT))
    {
        StringCopy(sGlassDex->text[0], COMPOUND_STRING("Catch this Pokémon to unlock"));
        StringCopy(sGlassDex->text[1], COMPOUND_STRING("its full Pokédex entry."));
        sGlassDex->textLines = 2;
        return;
    }
    if (source == NULL || source[0] == EOS)
    {
        StringCopy(sGlassDex->text[0], COMPOUND_STRING("No entry text available."));
        return;
    }
    while (*source != EOS && line < GLASS_DEX_TEXT_LINES)
    {
        while (*source == CHAR_SPACE || *source == CHAR_NEWLINE || *source == CHAR_PROMPT_SCROLL || *source == CHAR_PROMPT_CLEAR)
            source++;
        if (*source == EOS)
            break;
        length = 0;
        while (*source != EOS && *source != CHAR_SPACE && *source != CHAR_NEWLINE
            && *source != CHAR_PROMPT_SCROLL && *source != CHAR_PROMPT_CLEAR)
        {
            if (length < sizeof(word) - 1)
                word[length++] = *source;
            source++;
        }
        word[length] = EOS;
        StringCopy(candidate, sGlassDex->text[line]);
        if (candidate[0] != EOS)
            StringAppend(candidate, COMPOUND_STRING(" "));
        StringAppend(candidate, word);
        if (StringLength(candidate) >= 64 || GetStringWidth(FONT_SMALL, candidate, 0) > 188)
        {
            if (++line == GLASS_DEX_TEXT_LINES)
                break;
            StringCopy(sGlassDex->text[line], word);
        }
        else
            StringCopy(sGlassDex->text[line], candidate);
    }
    sGlassDex->textLines = line < GLASS_DEX_TEXT_LINES ? line + 1 : GLASS_DEX_TEXT_LINES;
}

static void DrawGlassDexPortrait(u16 species, s16 x, s16 y)
{
    u8 palette;
    if (sGlassDex->sprite != 0xFFFF)
    {
        palette = IndexOfSpritePaletteTag(TAG_POKEGLASS_DEX_MON);
        LoadPalette(GetMonSpritePalFromSpecies(species, FALSE, FALSE), OBJ_PLTT_ID(palette), PLTT_SIZE_4BPP);
        LoadSpecialPokePic((void *)gSprites[sGlassDex->sprite].images[0].data, species, 0, TRUE);
        gSprites[sGlassDex->sprite].x = x;
        gSprites[sGlassDex->sprite].y = y;
        StartSpriteAnim(&gSprites[sGlassDex->sprite], 0);
        return;
    }
    palette = LoadSpritePaletteWithTag(GetMonSpritePalFromSpecies(species, FALSE, FALSE), TAG_POKEGLASS_DEX_MON);
    if (palette == 0xFF)
        return;
    sGlassDex->sprite = CreateMonPicSprite(species, FALSE, 0, TRUE, x, y, palette, TAG_NONE);
    if (sGlassDex->sprite < MAX_SPRITES)
        gSprites[sGlassDex->sprite].oam.priority = 0;
    else
    {
        sGlassDex->sprite = 0xFFFF;
        FreeSpritePaletteByTag(TAG_POKEGLASS_DEX_MON);
    }
}

static void GlassDexMeasurement(u16 x, u16 y, const u8 *label, u16 value, const u8 *unit)
{
    u8 number[8], text[32];
    StringCopy(text, label);
    ConvertIntToDecimalStringN(number, value / 10, STR_CONV_MODE_LEFT_ALIGN, 4);
    StringAppend(text, number);
    StringAppend(text, COMPOUND_STRING("."));
    ConvertIntToDecimalStringN(number, value % 10, STR_CONV_MODE_LEFT_ALIGN, 1);
    StringAppend(text, number);
    StringAppend(text, unit);
    StatsText(x, y, text);
}

static void DrawGlassDexPage(void)
{
    u16 species = sGlassDex->count ? sGlassDex->species[sGlassDex->cursor] : SPECIES_NONE;
    u16 i, first = sGlassDex->cursor / GLASS_DEX_ROWS * GLASS_DEX_ROWS;
    bool8 caught = species != SPECIES_NONE && GetSetPokedexFlag(SpeciesToNationalPokedexNum(species), FLAG_GET_CAUGHT);
    DrawTabletShell((u8 *)GetWindowAttribute(sHubWindow, WINDOW_TILE_DATA));
    if (sGlassDex->view == 0)
    {
        StatsText(17, 18, COMPOUND_STRING("POKéDEX"));
        StatsText(88, 18, COMPOUND_STRING("Seen"));
        StatsNumber(141, 18, sGlassDex->seen);
        StatsText(151, 18, COMPOUND_STRING("Own"));
        StatsNumber(207, 18, sGlassDex->caught);
        StatsText(18, 31, sGlassDex->filter ? COMPOUND_STRING("Caught") : COMPOUND_STRING("Seen"));
        StatsText(72, 31, sGlassDex->alphabetical ? COMPOUND_STRING("A-Z") : COMPOUND_STRING("No."));
        HubRect(6, 17, 41, 103, 66);
        for (i = 0; i < GLASS_DEX_ROWS; i++)
        {
            u16 entry = first + i, y = 42 + i * 11;
            HubRect(entry == sGlassDex->cursor ? 5 : 4, 18, y, 101, 11);
            if (entry < sGlassDex->count)
            {
                u16 mon = sGlassDex->species[entry];
                StatsNumber(39, y, SpeciesToNationalPokedexNum(mon));
                StatsText(46, y, gSpeciesInfo[mon].speciesName);
                if (GetSetPokedexFlag(SpeciesToNationalPokedexNum(mon), FLAG_GET_CAUGHT))
                    HubRect(8, 113, y + 4, 3, 3);
            }
        }
        if (species != SPECIES_NONE)
        {
            StatsText(129, 31, gSpeciesInfo[species].speciesName);
            StatsText(144, 102, caught ? COMPOUND_STRING("Caught") : COMPOUND_STRING("Seen"));
            DrawGlassDexPortrait(species, 173, 81);
        }
        else
        {
            DestroyGlassDexPortrait();
            StatsText(129, 57, COMPOUND_STRING("No entries yet."));
            StatsText(129, 70, COMPOUND_STRING("Keep exploring!"));
        }
        StatsText(19, 106, COMPOUND_STRING("A Info  L/R Page  B Back"));
        StatsText(19, 116, COMPOUND_STRING("START Filter   SELECT Sort"));
    }
    else if (sGlassDex->view == 1)
    {
        StatsText(18, 18, gSpeciesInfo[species].speciesName);
        StatsText(142, 18, COMPOUND_STRING("No."));
        StatsNumber(187, 18, SpeciesToNationalPokedexNum(species));
        DrawGlassDexPortrait(species, 66, 69);
        StatsText(98, 34, caught ? gSpeciesInfo[species].categoryName : COMPOUND_STRING("Seen only"));
        if (caught)
        {
            StatsText(98, 46, gTypesInfo[gSpeciesInfo[species].types[0]].name);
            if (gSpeciesInfo[species].types[1] != gSpeciesInfo[species].types[0])
                StatsText(152, 46, gTypesInfo[gSpeciesInfo[species].types[1]].name);
            GlassDexMeasurement(98, 60, COMPOUND_STRING("Height "), gSpeciesInfo[species].height, COMPOUND_STRING(" m"));
            GlassDexMeasurement(98, 73, COMPOUND_STRING("Weight "), gSpeciesInfo[species].weight, COMPOUND_STRING(" kg"));
        }
        else
            StatsText(98, 52, COMPOUND_STRING("Data incomplete"));
        HubRect(6, 18, 92, 189, 1);
        for (i = 0; i < 2 && sGlassDex->textPage * 2 + i < sGlassDex->textLines; i++)
            StatsText(18, 94 + i * 10, sGlassDex->text[sGlassDex->textPage * 2 + i]);
        StatsText(18, 114, COMPOUND_STRING("A Text  R Habitat  SELECT Cry  B List"));
    }
    else
    {
        u8 name[64];
        DestroyGlassDexPortrait();
        StatsText(18, 18, gSpeciesInfo[species].speciesName);
        StatsText(133, 18, COMPOUND_STRING("HABITAT"));
        for (i = 0; i < GLASS_DEX_ROWS && sGlassDex->areaPage * GLASS_DEX_ROWS + i < sGlassDex->areaCount; i++)
        {
            GetMapName(name, sGlassDex->areas[sGlassDex->areaPage * GLASS_DEX_ROWS + i], 0);
            StatsText(25, 35 + i * 12, name);
        }
        if (sGlassDex->areaCount == 0)
        {
            StatsText(25, 54, COMPOUND_STRING("No wild habitat recorded."));
            StatsText(25, 69, COMPOUND_STRING("May be evolved, traded, or gifted."));
        }
        StatsText(25, 114, COMPOUND_STRING("L/R Page   B Entry"));
    }
    PutWindowTilemap(sHubWindow);
    CopyWindowToVram(sHubWindow, COPYWIN_FULL);
}

static void Task_PokeGlassPokedex(u8 taskId)
{
    u16 oldCursor = sGlassDex->cursor;
    if (gPaletteFade.active)
        return;
    if (gTasks[taskId].data[0]++ < 2)
        return;
    gTasks[taskId].data[0] = 2;
    if (JOY_NEW(B_BUTTON))
    {
        if (sGlassDex->view != 0)
        {
            sGlassDex->view--;
            DrawGlassDexPage();
        }
        else
        {
            DestroyGlassDexPortrait();
            Free(sGlassDex);
            sGlassDex = NULL;
            CloseHub();
            gTasks[taskId].data[2] = 0;
            gTasks[taskId].data[3] = FALSE;
            gTasks[taskId].func = Task_CloseTablet;
        }
        PlaySE(SE_SELECT);
        return;
    }
    if (JOY_NEW(SELECT_BUTTON) && sGlassDex->view == 1)
    {
        PlayCry_Normal(sGlassDex->species[sGlassDex->cursor], 0);
        return;
    }
    if (sGlassDex->view == 2)
    {
        u8 pages = (sGlassDex->areaCount + GLASS_DEX_ROWS - 1) / GLASS_DEX_ROWS;
        if (pages > 1 && JOY_NEW(L_BUTTON | R_BUTTON | DPAD_LEFT | DPAD_RIGHT))
        {
            sGlassDex->areaPage = JOY_NEW(L_BUTTON | DPAD_LEFT)
                ? (sGlassDex->areaPage + pages - 1) % pages : (sGlassDex->areaPage + 1) % pages;
            DrawGlassDexPage();
        }
        return;
    }
    if (sGlassDex->view == 1)
    {
        if (JOY_NEW(A_BUTTON))
        {
            sGlassDex->textPage = (sGlassDex->textPage + 1) % ((sGlassDex->textLines + 1) / 2);
            DrawGlassDexPage();
        }
        else if (JOY_NEW(R_BUTTON))
        {
            BuildGlassDexAreas(sGlassDex->species[sGlassDex->cursor]);
            sGlassDex->view = 2;
            DrawGlassDexPage();
        }
        return;
    }
    if (JOY_NEW(START_BUTTON | SELECT_BUTTON))
    {
        if (JOY_NEW(START_BUTTON))
            sGlassDex->filter ^= 1;
        else
            sGlassDex->alphabetical ^= 1;
        BuildGlassDexList();
        DrawGlassDexPage();
    }
    else if (sGlassDex->count != 0)
    {
        if (JOY_NEW(A_BUTTON))
        {
            BuildGlassDexText(sGlassDex->species[sGlassDex->cursor]);
            sGlassDex->view = 1;
            DrawGlassDexPage();
        }
        else if (JOY_REPEAT(DPAD_UP))
            sGlassDex->cursor = (sGlassDex->cursor + sGlassDex->count - 1) % sGlassDex->count;
        else if (JOY_REPEAT(DPAD_DOWN))
            sGlassDex->cursor = (sGlassDex->cursor + 1) % sGlassDex->count;
        else if (JOY_NEW(L_BUTTON | DPAD_LEFT))
            sGlassDex->cursor = sGlassDex->cursor > GLASS_DEX_ROWS ? sGlassDex->cursor - GLASS_DEX_ROWS : 0;
        else if (JOY_NEW(R_BUTTON | DPAD_RIGHT))
            sGlassDex->cursor = min(sGlassDex->cursor + GLASS_DEX_ROWS, sGlassDex->count - 1);
        if (oldCursor != sGlassDex->cursor)
        {
            PlaySE(SE_SELECT);
            DrawGlassDexPage();
        }
    }
}

void ShowPokeGlassPokedex(void)
{
    u8 taskId;
    // Upgrade old saves without altering their actual seen/caught records.
    EnableNationalPokedex();
    sGlassDex = AllocZeroed(sizeof(*sGlassDex));
    if (sGlassDex == NULL)
    {
        ScriptContext_Enable();
        return;
    }
    sGlassDex->sprite = 0xFFFF;
    if (!OpenTabletWindow())
    {
        Free(sGlassDex);
        sGlassDex = NULL;
        return;
    }
    BuildGlassDexList();
    DrawGlassDexPage();
    taskId = CreateTask(Task_PokeGlassPokedex, 80);
    if (taskId == TASK_NONE)
    {
        DestroyGlassDexPortrait();
        Free(sGlassDex);
        sGlassDex = NULL;
        CloseHub();
        RestoreTabletAppearance();
        ScriptContext_Enable();
    }
}
