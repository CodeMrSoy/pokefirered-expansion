#include "global.h"
#include "quantum_cleanup.h"
#include "avatar.h"
#include "data.h"
#include "gflib.h"
#include "menu.h"
#include "poke_glass.h"
#include "pokemon.h"
#include "item.h"
#include "mail.h"
#include "pokemon_icon.h"
#include "pokemon_storage_system.h"
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
#include "constants/flags.h"
#include "constants/pokedex.h"
#include "constants/region_map_sections.h"
#include "constants/moves.h"

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
    static const struct BgTemplate backdropBg = {
        .bg = 3, .charBaseIndex = 2, .mapBaseIndex = 27,
        .screenSize = 0, .paletteMode = 0, .priority = 3, .baseTile = 0,
    };
    u16 map[32 * 32] = {0};
    u32 x, y;
    if (sFieldBackdrop == NULL)
        return;
    CpuCopy16(sFieldBackdrop, (void *)(VRAM + 0x8000), 240 * 160 / 2);
    LoadPalette(sFieldBackdropPalette, BG_PLTT_ID(10), sizeof(sFieldBackdropPalette));
    // Native app initialization temporarily disables palette transfers. Publish
    // the captured field colors before its BG is shown, rather than exposing the
    // old overworld palette in this reserved slot for several loading frames.
    CpuCopy16(sFieldBackdropPalette, (void *)(PLTT + BG_PLTT_ID(10) * 2), sizeof(sFieldBackdropPalette));
    for (y = 0; y < 20; y++)
        for (x = 0; x < 30; x++)
            map[y * 32 + x] = (10 << 12) | (y * 30 + x);
    CpuCopy16(map, (void *)(VRAM + 27 * 0x800), sizeof(map));
    // Register this BG with the manager as well as the hardware. Otherwise
    // showing party windows silently hides it and exposes the backdrop color.
    InitBgFromTemplate(&backdropBg);
    SetGpuReg(REG_OFFSET_BG3HOFS, 0);
    SetGpuReg(REG_OFFSET_BG3VOFS, 0);
    ShowBg(3);
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
static EWRAM_DATA bool8 sTabletActive = FALSE;
static EWRAM_DATA bool8 sTabletNative = FALSE;

bool8 IsPokeGlassActive(void) { return sTabletActive; }
static EWRAM_DATA u8 sHubCursor = 0;
static EWRAM_DATA u16 sHubBlend[8] = {0};
static EWRAM_DATA u16 sHubPalette[32] = {0};
static const u8 sHubTitle[] = _("POKéGLASS");
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
    case 3: // Stats: a rising bar chart.
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
    case 5: // Wardrobe: a shirt with sleeves and an inset collar.
        HubRect(8, x + 6, y + 2, 12, 4);
        HubRect(8, x + 2, y + 5, 20, 7);
        HubRect(8, x, y + 7, 24, 4);
        HubRect(8, x + 6, y + 11, 12, 12);
        HubRect(5, x + 9, y + 2, 6, 4);
        break;
    }
}

static void DrawHubApp(u8 i, bool8 upload)
{
    static const u8 textColors[] = {0, 8, 4};
    // Preserve script app IDs: Pokédex, Party, Storage / Map, Stats, Wardrobe.
    static const u8 positions[6][2] = {{18,34}, {82,34}, {146,34}, {82,80}, {18,80}, {146,80}};
    u16 x = positions[i][0], y = positions[i][1];
    bool8 selected = i == sHubCursor;
    HubRect(selected ? 8 : 6, x, y, 60, 44);
    HubRect(selected ? 5 : 4, x + 2, y + 2, 56, 40);
    DrawHubIcon(i, x + 18, y + 3);
    AddTextPrinterParameterized3(sHubWindow, FONT_SMALL,
        x + (60 - GetStringWidth(FONT_SMALL, sHubLabels[i], 0)) / 2,
        y + 28, textColors, TEXT_SKIP_DRAW, sHubLabels[i]);
    if (upload)
        CopyWindowRectToVram(sHubWindow, COPYWIN_GFX, x / 8, y / 8,
            (x + 60 + 7) / 8 - x / 8, (y + 44 + 7) / 8 - y / 8);
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

// A compact, opaque tablet cover survives the field's VRAM/heap reset. Its
// tiles live above map graphics and below the field tilemaps. Only the glass
// changes during the handoff; the captured scenery around the bezel stays put.
// c000-c5ff belongs to field dialogue / the hub window. c600-d7ff holds
// 144 cover tiles: 46 unique shell tiles plus at most 96 surrounding tiles.
// d800-dfff holds its map; the field's three maps start at e000.
#define RETURN_COVER_FIRST_TILE 48
#define RETURN_COVER_TILES (192 - RETURN_COVER_FIRST_TILE)
static EWRAM_DATA bool8 sReturnCoverActive = FALSE;
static EWRAM_DATA bool8 sReturnCoverReady = FALSE;
static EWRAM_DATA u16 sReturnCoverPalette[32] = {0};

bool8 IsPokeGlassReturnActive(void)
{
    return sReturnCoverActive;
}

void BeginPokeGlassReturn(void)
{
    u8 *pixels, *tiles;
    u16 map[32 * 32] = {0};
    u32 x, y, tile, count = 0;
    if (!sTabletActive || !sTabletNative || sFieldBackdrop == NULL)
        return;
    pixels = AllocZeroed(28 * 18 * 32);
    tiles = AllocZeroed(RETURN_COVER_TILES * 32);
    if (pixels == NULL || tiles == NULL)
    {
        Free(pixels);
        Free(tiles);
        return;
    }
    DrawTabletShell(pixels);
    for (y = 0; y < 20; y++)
        for (x = 0; x < 30; x++)
        {
            bool8 shell = x > 0 && x < 29 && y > 0 && y < 19;
            const u8 *source = shell ? pixels + ((y - 1) * 28 + x - 1) * 32
                : sFieldBackdrop + (y * 30 + x) * 32;
            for (tile = 0; tile < count; tile++)
                if (memcmp(source, tiles + tile * 32, 32) == 0)
                    break;
            if (tile == count)
            {
                if (count == RETURN_COVER_TILES)
                {
                    Free(pixels);
                    Free(tiles);
                    return;
                }
                CpuCopy16(source, tiles + count++ * 32, 32);
            }
            map[y * 32 + x] = (RETURN_COVER_FIRST_TILE + tile) | ((shell ? 14 : 13) << 12);
        }
    CpuCopy16(sFieldBackdropPalette, sReturnCoverPalette, 32);
    CpuCopy16(sPalette, sReturnCoverPalette + 16, 32);
    VBlankIntrWait();
    CpuCopy16(tiles, (void *)(VRAM + 0xC000 + RETURN_COVER_FIRST_TILE * 32), count * 32);
    CpuCopy16(map, (void *)(VRAM + 0xD800), sizeof(map));
    sReturnCoverReady = FALSE;
    sReturnCoverActive = TRUE;
    VBlankCB_PokeGlassReturn();
    Free(pixels);
    Free(tiles);
}

// Run after buffered registers and DMA, so field loading can update its normal
// state without exposing half-loaded graphics. Release only after the tablet
// window's tile graphics and tilemap have both arrived in VRAM.
void VBlankCB_PokeGlassReturn(void)
{
    if (!sReturnCoverActive)
        return;
    if (sReturnCoverReady && WaitDma3Request(-1) == 0)
    {
        REG_BG0CNT = GetGpuReg(REG_OFFSET_BG0CNT);
        REG_BG0HOFS = GetGpuReg(REG_OFFSET_BG0HOFS);
        REG_BG0VOFS = GetGpuReg(REG_OFFSET_BG0VOFS);
        REG_BLDCNT = GetGpuReg(REG_OFFSET_BLDCNT);
        REG_DISPCNT = GetGpuReg(REG_OFFSET_DISPCNT);
        *(vu16 *)PLTT = gPlttBufferFaded[0];
        CpuCopy16(&gPlttBufferFaded[BG_PLTT_ID(13)], (void *)(PLTT + 13 * 32), 64);
        sReturnCoverActive = FALSE;
        return;
    }
    *(vu16 *)PLTT = RGB_BLACK;
    CpuCopy16(sReturnCoverPalette, (void *)(PLTT + 13 * 32), 64);
    REG_BG0CNT = BGCNT_CHARBASE(3) | BGCNT_SCREENBASE(27);
    REG_BG0HOFS = 0;
    REG_BG0VOFS = 0;
    REG_BLDCNT = 0;
    REG_DISPCNT = DISPCNT_BG0_ON;
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
    PutWindowTilemap(sHubWindow);
    CopyWindowToVram(sHubWindow, COPYWIN_FULL);
    if (sReturnCoverActive)
        sReturnCoverReady = TRUE;
}

static void CloseHub(void)
{
    if (sTabletActive)
        return; // Task_CloseTablet animates only the screen before the handoff.
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
    if (sTabletActive)
    {
        u8 step = gTasks[taskId].data[2]++;
        if (step < 6)
        {
            u16 x = 12 + step * 34;
            HubRect(4, x, 15, step == 5 ? 30 : 34, 113);
            CopyWindowToVram(sHubWindow, COPYWIN_GFX);
            return;
        }
        if (sTabletNative) sHubWindow = WINDOW_NONE;
        DestroyTask(taskId);
        ScriptContext_Enable();
        return;
    }
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
            sHubCursor = sHubCursor == 4 ? 0 : sHubCursor == 3 ? 1 : sHubCursor == 5 ? 2 : sHubCursor;
        else if (JOY_NEW(DPAD_DOWN))
            sHubCursor = sHubCursor == 0 ? 4 : sHubCursor == 1 ? 3 : sHubCursor == 2 ? 5 : sHubCursor;
        else if (JOY_NEW(DPAD_LEFT))
            sHubCursor = sHubCursor == 1 ? 0 : sHubCursor == 2 ? 1 : sHubCursor == 3 ? 4 : sHubCursor == 5 ? 3 : sHubCursor;
        else if (JOY_NEW(DPAD_RIGHT))
            sHubCursor = sHubCursor == 0 ? 1 : sHubCursor == 1 ? 2 : sHubCursor == 4 ? 3 : sHubCursor == 3 ? 5 : sHubCursor;
        if (oldCursor != sHubCursor)
        {
            PlaySE(SE_SELECT);
            DrawHubApp(oldCursor, TRUE);
            DrawHubApp(sHubCursor, TRUE);
        }
        return;
    }
    PlaySE(SE_SELECT);
    sTabletNative = gSpecialVar_Result == 1;
    if (gSpecialVar_Result == SCR_MENU_CANCEL) sTabletActive = FALSE;
    CloseHub();
    gTasks[taskId].data[2] = 0;
    gTasks[taskId].data[3] = FALSE;
    gTasks[taskId].func = Task_CloseTablet;
    if (gSpecialVar_Result == SCR_MENU_CANCEL)
        ReleasePokeGlassBackdrop();
}

static bool8 OpenTabletWindow(void)
{
    if (sHubWindow != WINDOW_NONE && sTabletActive && !sTabletNative)
        return TRUE;
    sTabletNative = FALSE;
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
    if (!sTabletActive) CapturePokeGlassBackdrop();
    if (!OpenTabletWindow())
        return;
    sTabletActive = TRUE;
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
    StatsText(17, 16, nickname);
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
    StatsText(17, 16, COMPOUND_STRING("WARDROBE"));
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
        StatsText(17, 16, COMPOUND_STRING("POKéDEX"));
        StatsText(88, 16, COMPOUND_STRING("Seen"));
        StatsNumber(141, 16, sGlassDex->seen);
        StatsText(151, 16, COMPOUND_STRING("Own"));
        StatsNumber(207, 16, sGlassDex->caught);
        StatsText(72, 29, sGlassDex->filter ? COMPOUND_STRING("Caught") : COMPOUND_STRING("Seen"));
        StatsText(18, 29, sGlassDex->alphabetical ? COMPOUND_STRING("A-Z") : COMPOUND_STRING("No."));
        HubRect(6, 17, 39, 103, 66);
        for (i = 0; i < GLASS_DEX_ROWS; i++)
        {
            u16 entry = first + i, y = 40 + i * 11;
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
            StatsText(129, 29, gSpeciesInfo[species].speciesName);
            StatsText(144, 100, caught ? COMPOUND_STRING("Caught") : COMPOUND_STRING("Seen"));
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
        StatsText(18, 16, gSpeciesInfo[species].speciesName);
        StatsText(142, 16, COMPOUND_STRING("No."));
        StatsNumber(187, 16, SpeciesToNationalPokedexNum(species));
        DrawGlassDexPortrait(species, 66, 65);
        StatsText(98, 32, caught ? gSpeciesInfo[species].categoryName : COMPOUND_STRING("Seen only"));
        if (caught)
        {
            StatsText(98, 44, gTypesInfo[gSpeciesInfo[species].types[0]].name);
            if (gSpeciesInfo[species].types[1] != gSpeciesInfo[species].types[0])
                StatsText(152, 44, gTypesInfo[gSpeciesInfo[species].types[1]].name);
            GlassDexMeasurement(98, 58, COMPOUND_STRING("Height "), gSpeciesInfo[species].height, COMPOUND_STRING(" m"));
            GlassDexMeasurement(98, 71, COMPOUND_STRING("Weight "), gSpeciesInfo[species].weight, COMPOUND_STRING(" kg"));
        }
        else
            StatsText(98, 50, COMPOUND_STRING("Data incomplete"));
        StatsText(98, 83, COMPOUND_STRING("Habitat"));
        HubRect(6, 18, 94, 189, 1);
        if (sGlassDex->areaCount != 0)
        {
            u8 name[64];
            GetMapName(name, sGlassDex->areas[sGlassDex->areaPage], 0);
            StatsText(18, 96, name);
            StatsNumber(177, 83, sGlassDex->areaPage + 1);
            StatsText(181, 83, COMPOUND_STRING("/"));
            StatsNumber(207, 83, sGlassDex->areaCount);
        }
        else
            StatsText(18, 96, COMPOUND_STRING("No wild habitat recorded."));
        StatsText(18, 114, COMPOUND_STRING("A All  L/R Place  SELECT Cry  B"));
    }
    else
    {
        u8 name[64];
        DestroyGlassDexPortrait();
        StatsText(18, 16, gSpeciesInfo[species].speciesName);
        StatsText(133, 16, COMPOUND_STRING("HABITAT"));
        for (i = 0; i < GLASS_DEX_ROWS && sGlassDex->areaPage * GLASS_DEX_ROWS + i < sGlassDex->areaCount; i++)
        {
            GetMapName(name, sGlassDex->areas[sGlassDex->areaPage * GLASS_DEX_ROWS + i], 0);
            StatsText(25, 33 + i * 12, name);
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
            sGlassDex->areaPage = 0;
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
            sGlassDex->areaPage = 0;
            sGlassDex->view = 2;
            DrawGlassDexPage();
        }
        else if (sGlassDex->areaCount > 1 && JOY_NEW(L_BUTTON | R_BUTTON | DPAD_LEFT | DPAD_RIGHT))
        {
            sGlassDex->areaPage = JOY_NEW(L_BUTTON | DPAD_LEFT)
                ? (sGlassDex->areaPage + sGlassDex->areaCount - 1) % sGlassDex->areaCount
                : (sGlassDex->areaPage + 1) % sGlassDex->areaCount;
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
            BuildGlassDexAreas(sGlassDex->species[sGlassDex->cursor]);
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


// Selection keeps its source intact until a validated placement is committed.
static EWRAM_DATA struct {
    u8 box, cursor, sourceBox, sourceSlot;
    bool8 panel, holding, sourceParty;
    u8 icons[37];
    u8 actionMode, actionChoice, nameCursor;
    u8 editedName[BOX_NAME_LENGTH + 1];
    const u8 *notice;
    u16 iconSpecies[37];
    u32 iconPersonality[37];
} sGlassStorage = {0};

static void StorageClearIcons(void)
{
    u8 i;
    for (i = 0; i < ARRAY_COUNT(sGlassStorage.icons); i++)
        if (sGlassStorage.icons[i] < MAX_SPRITES)
            FreeAndDestroyMonIconSprite(&gSprites[sGlassStorage.icons[i]]);
    memset(sGlassStorage.icons, MAX_SPRITES, sizeof(sGlassStorage.icons));
}

// Keep the PC background quiet so species colors carry the visual weight.
static const u16 sStoragePalette[16] = {
    RGB(0,0,0), RGB(2,2,3), RGB(5,5,7), RGB(11,12,14),
    RGB(0,6,11), RGB(3,13,20), RGB(15,23,26), RGB(15,29,31),
    RGB(26,31,31), RGB(22,2,5), RGB(31,5,7), RGB(31,14,15),
    RGB(20,21,24), RGB(28,29,30), RGB(17,25,28), RGB(31,31,31)
};
#define TAG_POKEGLASS_STORAGE_MON 0xD112
static EWRAM_DATA u16 sStoragePortrait = 0;

static void StorageDestroyPortrait(void)
{
    if (sStoragePortrait != 0xFFFF)
        FreeAndDestroyMonPicSpriteNoPalette(sStoragePortrait);
    sStoragePortrait = 0xFFFF;
    FreeSpritePaletteByTag(TAG_POKEGLASS_STORAGE_MON);
}

static void StoragePosition(u8 slot, s16 *x, s16 *y)
{
    if (slot < 30)
    {
        // The box never moves when the party panel opens.
        *x = 86 + slot % 6 * 22;
        *y = 35 + slot / 6 * 19;
    }
    else if (slot < 36)
    {
        *x = 29 + (slot - 30) % 2 * 29;
        *y = 47 + (slot - 30) / 2 * 25;
    }
    else { *x = 43; *y = 119; }
}

static void StorageRead(u8 box, u8 slot, bool8 party, struct Pokemon *mon)
{
    if (party) *mon = gPlayerParty[slot];
    else
    {
        ZeroMonData(mon);
        mon->box = *GetBoxedMonPtr(box, slot);
    }
}

static void StorageRemoveIcon(u8 index)
{
    if (sGlassStorage.icons[index] < MAX_SPRITES)
        FreeAndDestroyMonIconSprite(&gSprites[sGlassStorage.icons[index]]);
    sGlassStorage.icons[index] = MAX_SPRITES;
}

static void StorageIcon(u8 index, struct Pokemon *mon, s16 x, s16 y)
{
    u16 species = GetMonData(mon, MON_DATA_SPECIES_OR_EGG);
    u32 personality = GetMonData(mon, MON_DATA_PERSONALITY);
    u8 id = sGlassStorage.icons[index];
    if (!species)
    {
        StorageRemoveIcon(index);
        return;
    }
    if (id >= MAX_SPRITES || sGlassStorage.iconSpecies[index] != species
     || sGlassStorage.iconPersonality[index] != personality)
    {
        StorageRemoveIcon(index);
        LoadMonIconPalettePersonality(species, personality);
        id = CreateMonIcon(species, SpriteCallbackDummy, x + 8, y + 8, 0, personality);
        sGlassStorage.icons[index] = id;
        sGlassStorage.iconSpecies[index] = species;
        sGlassStorage.iconPersonality[index] = personality;
    }
    if (id < MAX_SPRITES)
    {
        gSprites[id].x = x + 8;
        gSprites[id].y = y + 8;
        gSprites[id].oam.priority = 0;
        gSprites[id].subpriority = index == 36 ? 0 : 1;
        gSprites[id].callback = index == sGlassStorage.cursor || index == 36 ? SpriteCB_MonIcon : SpriteCallbackDummy;
    }
}

static void StorageTextFit(u16 x, u16 y, u16 width, const u8 *text)
{
    u8 fitted[32];
    u32 len = 0;
    while (text[len] != EOS && len < sizeof(fitted) - 1)
    {
        fitted[len] = text[len];
        fitted[++len] = EOS;
        if (GetStringWidth(FONT_SMALL, fitted, 0) > width)
        {
            fitted[--len] = EOS;
            break;
        }
    }
    fitted[len] = EOS;
    StatsText(x, y, fitted);
}

static void StoragePreview(struct Pokemon *mon)
{
    u8 name[POKEMON_NAME_LENGTH + 1], palette;
    u16 species = GetMonData(mon, MON_DATA_SPECIES_OR_EGG);
    u32 personality = GetMonData(mon, MON_DATA_PERSONALITY);
    bool32 shiny = GetMonData(mon, MON_DATA_IS_SHINY);
    if (!species)
    {
        StorageDestroyPortrait();
        StatsText(19, 54, COMPOUND_STRING("Choose a"));
        StatsText(19, 66, COMPOUND_STRING("Pokémon"));
        return;
    }
    GetMonData(mon, MON_DATA_NICKNAME, name);
    StorageTextFit(15, 29, 61, name);
    HubRect(6, 15, 43, 61, 55);
    HubRect(14, 16, 44, 59, 53);
    if (sStoragePortrait == 0xFFFF)
    {
        palette = LoadSpritePaletteWithTag(GetMonSpritePalFromSpeciesAndPersonality(species, shiny, personality), TAG_POKEGLASS_STORAGE_MON);
        if (palette != 0xFF)
        {
            sStoragePortrait = CreateMonPicSprite(species, shiny, personality, TRUE, 52, 78, palette, TAG_NONE);
            if (sStoragePortrait < MAX_SPRITES) gSprites[sStoragePortrait].oam.priority = 0;
            else { sStoragePortrait = 0xFFFF; FreeSpritePaletteByTag(TAG_POKEGLASS_STORAGE_MON); }
        }
    }
    else
    {
        palette = IndexOfSpritePaletteTag(TAG_POKEGLASS_STORAGE_MON);
        LoadPalette(GetMonSpritePalFromSpeciesAndPersonality(species, shiny, personality), OBJ_PLTT_ID(palette), PLTT_SIZE_4BPP);
        LoadSpecialPokePic((void *)gSprites[sStoragePortrait].images[0].data, species, personality, TRUE);
        StartSpriteAnim(&gSprites[sStoragePortrait], 0);
    }
    if (GetMonData(mon, MON_DATA_IS_EGG)) StatsText(27, 100, COMPOUND_STRING("Egg"));
    else
    {
        StatsText(17, 100, COMPOUND_STRING("Lv."));
        StatsNumber(53, 100, GetLevelFromBoxMonExp(&mon->box));
        if (GetMonGender(mon) != MON_GENDERLESS)
            StatsText(61, 100, GetMonGender(mon) == MON_FEMALE ? COMPOUND_STRING("♀") : COMPOUND_STRING("♂"));
    }
}

static void StorageCursor(s16 x, s16 y)
{
    u8 color = sGlassStorage.holding ? 10 : 4;
    // Four brackets leave the icon unobscured and stay visible on occupied slots.
    HubRect(color, x - 10, y - 9, 5, 2);
    HubRect(color, x - 10, y - 9, 2, 5);
    HubRect(color, x + 5, y - 9, 5, 2);
    HubRect(color, x + 8, y - 9, 2, 5);
    HubRect(color, x - 10, y + 7, 5, 2);
    HubRect(color, x - 10, y + 4, 2, 5);
    HubRect(color, x + 5, y + 7, 5, 2);
    HubRect(color, x + 8, y + 4, 2, 5);
}

static void DrawGlassStorage(void)
{
    u8 i, count[8];
    s16 x, y;
    struct Pokemon mon, selected;
    ZeroMonData(&selected);
    // Storage needs the same contrast as a PC box. Keep the bezel but make
    // this app's screen opaque; the overworld cannot show through the grid.
    SetGpuReg(REG_OFFSET_BLDCNT, 0);
    LoadPalette(sStoragePalette, BG_PLTT_ID(11), sizeof(sStoragePalette));
    DrawTabletShell((u8 *)GetWindowAttribute(sHubWindow, WINDOW_TILE_DATA));
    HubRect(4, 12, 15, 200, 113);
    HubRect(5, 78, 15, 134, 12);
    StatsText(16, 15, sGlassStorage.holding ? COMPOUND_STRING("B Cancel") : COMPOUND_STRING("SELECT"));
    StatsText(81, 15, COMPOUND_STRING("L"));
    StorageTextFit(98, 15, 62, GetBoxNamePtr(sGlassStorage.box));
    ConvertIntToDecimalStringN(count, CountMonsInBox(sGlassStorage.box), STR_CONV_MODE_LEFT_ALIGN, 2);
    StringAppend(count, COMPOUND_STRING("/30"));
    StatsText(169, 15, count);
    StatsText(201, 15, COMPOUND_STRING("R"));
    HubRect(6, 76, 27, 136, 101);
    for (i = 0; i < 30; i++)
    {
        StoragePosition(i, &x, &y);
        // A quiet checkerboard reads as one box instead of thirty tiny cards.
        HubRect((i / 6 + i % 6) % 2 ? 14 : 6, x - 10, y - 8, 21, i >= 24 ? 25 : 18);
    }
    if (sGlassStorage.panel)
    {
        StorageDestroyPortrait();
        StatsText(25, 29, COMPOUND_STRING("PARTY"));
        for (i = 30; i < 36; i++)
        {
            StoragePosition(i, &x, &y);
            HubRect(5, x - 12, y - 9, 25, 20);
        }
    }
    for (i = 0; i < 36; i++)
    {
        bool8 source = sGlassStorage.holding && sGlassStorage.sourceParty == (i >= 30)
            && sGlassStorage.sourceSlot == (i < 30 ? i : i - 30)
            && (i >= 30 || sGlassStorage.sourceBox == sGlassStorage.box);
        if ((i >= 30 && !sGlassStorage.panel) || source || (sGlassStorage.holding && i == sGlassStorage.cursor))
        {
            StorageRemoveIcon(i);
            continue;
        }
        StoragePosition(i, &x, &y);
        StorageRead(sGlassStorage.box, i < 30 ? i : i - 30, i >= 30, &mon);
        StorageIcon(i, &mon, x, y);
    }
    HubRect(sGlassStorage.cursor == 36 ? 15 : 6, 15, 114, 61, 14);
    HubRect(5, 16, 115, 59, 12);
    StatsText(29, 114, COMPOUND_STRING("Party"));
    if (sGlassStorage.holding)
        StorageRead(sGlassStorage.sourceBox, sGlassStorage.sourceSlot, sGlassStorage.sourceParty, &selected);
    else if (sGlassStorage.cursor < 36)
        StorageRead(sGlassStorage.box, sGlassStorage.cursor < 30 ? sGlassStorage.cursor : sGlassStorage.cursor - 30, sGlassStorage.cursor >= 30, &selected);
    if (!sGlassStorage.panel) StoragePreview(&selected);
    StoragePosition(sGlassStorage.cursor, &x, &y);
    if (sGlassStorage.cursor < 36) StorageCursor(x, y);
    if (sGlassStorage.holding)
    {
        StorageIcon(36, &selected, x, y - (sGlassStorage.cursor == 36 ? 8 : 1));
    }
    else
    {
        StorageRemoveIcon(36);
    }
    PutWindowTilemap(sHubWindow);
    CopyWindowToVram(sHubWindow, COPYWIN_FULL);
}

static const u8 sStorageNameChars[] = _(" ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-.");

static u16 StorageFieldMoves(struct BoxPokemon *mon)
{
    static const u16 moves[] = {MOVE_CUT, MOVE_FLY, MOVE_SURF, MOVE_STRENGTH, MOVE_FLASH, MOVE_ROCK_SMASH, MOVE_WATERFALL, MOVE_DIVE};
    u16 mask = 0;
    u32 i, j;
    if (!GetBoxMonData(mon, MON_DATA_SPECIES) || GetBoxMonData(mon, MON_DATA_IS_EGG)) return 0;
    for (i = 0; i < MAX_MON_MOVES; i++)
        for (j = 0; j < ARRAY_COUNT(moves); j++)
            if (GetBoxMonData(mon, MON_DATA_MOVE1 + i) == moves[j]) mask |= 1 << j;
    return mask;
}

static const u8 *StorageReleaseSelected(void)
{
    u8 slot = sGlassStorage.cursor < 30 ? sGlassStorage.cursor : sGlassStorage.cursor - 30;
    bool8 party = sGlassStorage.cursor >= 30;
    struct Pokemon mon;
    u16 needed, item;
    u32 i, box;
    if (sGlassStorage.cursor >= 36) return COMPOUND_STRING("Choose a Pokemon first.");
    StorageRead(sGlassStorage.box, slot, party, &mon);
    if (!GetMonData(&mon, MON_DATA_SPECIES)) return COMPOUND_STRING("This slot is empty.");
    if (GetMonData(&mon, MON_DATA_IS_EGG)) return COMPOUND_STRING("An Egg cannot be released.");
    if (party && !CountPartyAliveNonEggMonsExcept(slot)) return COMPOUND_STRING("Keep a usable party Pokemon.");
    if ((party && GetMonData(&mon, MON_DATA_MAIL) != 255) || ItemIsMail(GetMonData(&mon, MON_DATA_HELD_ITEM))) return COMPOUND_STRING("Remove its Mail first.");
    needed = StorageFieldMoves(&mon.box);
    for (i = 0; needed && i < PARTY_SIZE; i++)
        if (!(party && i == slot)) needed &= ~StorageFieldMoves(&gPlayerParty[i].box);
    for (box = 0; needed && box < TOTAL_BOXES_COUNT; box++)
        for (i = 0; needed && i < IN_BOX_COUNT; i++)
            if (!(!party && box == sGlassStorage.box && i == slot))
                needed &= ~StorageFieldMoves(GetBoxedMonPtr(box, i));
    if (needed) return COMPOUND_STRING("Keep another field-move user.");
    item = GetMonData(&mon, MON_DATA_HELD_ITEM);
    if (item && !AddBagItem(item, 1)) return COMPOUND_STRING("Make room for its held item.");
    if (party)
    {
        ZeroMonData(&gPlayerParty[slot]);
        CompactPartySlots();
        CalculatePlayerPartyCount();
    }
    else ZeroBoxMonAt(sGlassStorage.box, slot);
    QuantumRecoverStoredItemsAndPokemon();
    return item ? COMPOUND_STRING("Released. Item sent to Bag.") : COMPOUND_STRING("Pokemon released.");
}

static void DrawStorageActions(void)
{
    u8 mark[] = _(">");
    StorageClearIcons();
    StorageDestroyPortrait();
    HubRect(2, 18, 32, 188, 77);
    HubRect(4, 19, 33, 186, 75);
    if (sGlassStorage.actionMode == 1)
    {
        StatsText(34, 44, COMPOUND_STRING("Release Pokemon"));
        StatsText(34, 64, COMPOUND_STRING("Rename box"));
        StatsText(22, 44 + sGlassStorage.actionChoice * 20, mark);
        StatsText(25, 89, COMPOUND_STRING("A Choose   B Back"));
    }
    else if (sGlassStorage.actionMode == 2)
    {
        StatsText(25, 42, COMPOUND_STRING("Release this Pokemon?"));
        StatsText(40, 65, sGlassStorage.actionChoice ? COMPOUND_STRING("No    >Yes") : COMPOUND_STRING(">No    Yes"));
        StatsText(25, 89, COMPOUND_STRING("A Confirm   B Cancel"));
    }
    else if (sGlassStorage.actionMode == 3)
    {
        StatsText(25, 40, COMPOUND_STRING("Rename box"));
        StatsText(45, 59, sGlassStorage.editedName);
        // Fixed-width character cells let the cursor track narrow glyphs too.
        HubRect(4, 43, 58, 140, 20);
        for (u32 i = 0; i < BOX_NAME_LENGTH; i++)
        {
            u8 letter[] = {sGlassStorage.editedName[i], EOS};
            StatsText(45 + i * 16, 59, letter);
        }
        HubRect(8, 45 + sGlassStorage.nameCursor * 16, 73, 10, 1);
        StatsText(25, 81, COMPOUND_STRING("Up/Down Letter  Left/Right"));
        StatsText(25, 94, COMPOUND_STRING("A Save   B Cancel"));
    }
    else StatsText(23, 60, sGlassStorage.notice);
    PutWindowTilemap(sHubWindow);
    CopyWindowToVram(sHubWindow, COPYWIN_FULL);
}

static bool8 HandleStorageActions(void)
{
    u8 mode = sGlassStorage.actionMode;
    if (!mode) return FALSE;
    if (!JOY_NEW(A_BUTTON | B_BUTTON | DPAD_LEFT | DPAD_RIGHT | DPAD_UP | DPAD_DOWN)
     && !(mode == 3 && JOY_REPEAT(DPAD_UP | DPAD_DOWN))) return TRUE;
    if (JOY_NEW(B_BUTTON)) sGlassStorage.actionMode = 0;
    else if (mode == 1)
    {
        if (JOY_NEW(DPAD_UP | DPAD_DOWN)) sGlassStorage.actionChoice ^= 1;
        if (JOY_NEW(A_BUTTON))
        {
            if (!sGlassStorage.actionChoice)
            {
                sGlassStorage.actionMode = 2;
                sGlassStorage.actionChoice = 0; // Never default to a destructive action.
            }
            else
            {
                u8 *name = GetBoxNamePtr(sGlassStorage.box);
                u32 i;
                bool8 ended = FALSE;
                for (i = 0; i < BOX_NAME_LENGTH; i++)
                {
                    if (name[i] == EOS) ended = TRUE;
                    sGlassStorage.editedName[i] = ended ? CHAR_SPACE : name[i];
                }
                sGlassStorage.editedName[BOX_NAME_LENGTH] = EOS;
                sGlassStorage.nameCursor = 0;
                sGlassStorage.actionMode = 3;
            }
        }
    }
    else if (mode == 2)
    {
        if (JOY_NEW(DPAD_LEFT | DPAD_RIGHT)) sGlassStorage.actionChoice ^= 1;
        if (JOY_NEW(A_BUTTON))
        {
            if (!sGlassStorage.actionChoice) sGlassStorage.actionMode = 0;
            else
            {
                sGlassStorage.notice = StorageReleaseSelected();
                sGlassStorage.actionMode = 4;
            }
        }
    }
    else if (mode == 3)
    {
        u8 *letter = &sGlassStorage.editedName[sGlassStorage.nameCursor];
        u32 i, len = ARRAY_COUNT(sStorageNameChars) - 1;
        if (JOY_NEW(DPAD_LEFT)) sGlassStorage.nameCursor = (sGlassStorage.nameCursor + BOX_NAME_LENGTH - 1) % BOX_NAME_LENGTH;
        else if (JOY_NEW(DPAD_RIGHT)) sGlassStorage.nameCursor = (sGlassStorage.nameCursor + 1) % BOX_NAME_LENGTH;
        else if (JOY_REPEAT(DPAD_UP | DPAD_DOWN))
        {
            for (i = 0; i < len && sStorageNameChars[i] != *letter; i++);
            if (i == len) i = 0;
            *letter = sStorageNameChars[(i + (JOY_REPEAT(DPAD_UP) ? 1 : len - 1)) % len];
        }
        else if (JOY_NEW(A_BUTTON))
        {
            u8 *name = GetBoxNamePtr(sGlassStorage.box);
            s32 end = BOX_NAME_LENGTH;
            while (end && sGlassStorage.editedName[end - 1] == CHAR_SPACE) end--;
            if (!end) { PlaySE(SE_FAILURE); return TRUE; }
            memcpy(name, sGlassStorage.editedName, end);
            name[end] = EOS;
            sGlassStorage.actionMode = 0;
        }
    }
    else if (JOY_NEW(A_BUTTON)) sGlassStorage.actionMode = 0;
    PlaySE(SE_SELECT);
    if (sGlassStorage.actionMode) DrawStorageActions();
    else DrawGlassStorage();
    return TRUE;
}

static bool8 StoragePlace(void)
{
    struct Pokemon source, target;
    bool8 party = sGlassStorage.cursor >= 30;
    u8 slot = party ? sGlassStorage.cursor - 30 : sGlassStorage.cursor;
    StorageRead(sGlassStorage.sourceBox, sGlassStorage.sourceSlot, sGlassStorage.sourceParty, &source);
    StorageRead(sGlassStorage.box, slot, party, &target);
    if (!sGlassStorage.sourceParty && GetMonData(&source, MON_DATA_SPECIES))
        BoxMonAtToMon(sGlassStorage.sourceBox, sGlassStorage.sourceSlot, &source);
    if (!party && GetMonData(&target, MON_DATA_SPECIES))
        BoxMonAtToMon(sGlassStorage.box, slot, &target);
    // A party member may only leave if a usable member remains or arrives.
    if (sGlassStorage.sourceParty != party)
    {
        u8 removed = party ? slot : sGlassStorage.sourceSlot;
        struct Pokemon *incoming = party ? &source : &target;
        struct Pokemon *outgoing = party ? &target : &source;
        if (GetMonData(outgoing, MON_DATA_SPECIES)
         && (!CountPartyAliveNonEggMonsExcept(removed)
          && (!GetMonData(incoming, MON_DATA_SPECIES) || GetMonData(incoming, MON_DATA_IS_EGG) || !GetMonData(incoming, MON_DATA_HP))))
            return FALSE;
        if (GetMonData(outgoing, MON_DATA_SPECIES) && GetMonData(outgoing, MON_DATA_MAIL) != 255)
            return FALSE;
    }
    if (sGlassStorage.sourceParty) gPlayerParty[sGlassStorage.sourceSlot] = target;
    else SetBoxMonAt(sGlassStorage.sourceBox, sGlassStorage.sourceSlot, &target.box);
    if (party) gPlayerParty[slot] = source;
    else SetBoxMonAt(sGlassStorage.box, slot, &source.box);
    CompactPartySlots();
    CalculatePlayerPartyCount();
    return TRUE;
}

static void Task_CloseGlassStorage(u8 taskId)
{
    // Restore the hub only after the app's opaque screen has been wiped.
    // OpenTabletWindow reuses the existing window on app-to-hub returns.
    if (sTabletActive && gTasks[taskId].data[2] == 6)
    {
        LoadPalette(sPalette, BG_PLTT_ID(11), sizeof(sPalette));
        SetPokeGlassBlend(TRUE);
    }
    Task_CloseTablet(taskId);
}

static void Task_GlassStorage(u8 taskId)
{
    u8 cursor = sGlassStorage.cursor;
    if (gTasks[taskId].data[0]++ < 2) return;
    gTasks[taskId].data[0] = 2;
    if (HandleStorageActions()) return;
    if (JOY_NEW(SELECT_BUTTON) && !sGlassStorage.holding)
    {
        sGlassStorage.actionMode = 1;
        sGlassStorage.actionChoice = 0;
        DrawStorageActions();
        return;
    }
    if (JOY_NEW(B_BUTTON))
    {
        if (sGlassStorage.holding) sGlassStorage.holding = FALSE;
        else if (sGlassStorage.panel) { sGlassStorage.panel = FALSE; sGlassStorage.cursor = 36; }
        else
        {
            StorageClearIcons();
            StorageDestroyPortrait();
            FreeMonIconPalettes();
            CloseHub();
            gTasks[taskId].data[2] = 0;
            gTasks[taskId].data[3] = FALSE;
            gTasks[taskId].func = Task_CloseGlassStorage;
            return;
        }
    }
    else if (JOY_NEW(L_BUTTON | R_BUTTON))
    {
        sGlassStorage.box = (sGlassStorage.box + (JOY_NEW(L_BUTTON) ? TOTAL_BOXES_COUNT - 1 : 1)) % TOTAL_BOXES_COUNT;
        gPokemonStoragePtr->currentBox = sGlassStorage.box;
    }
    else if (JOY_NEW(A_BUTTON))
    {
        if (cursor == 36) { sGlassStorage.panel = TRUE; sGlassStorage.cursor = 30; }
        else if (sGlassStorage.holding)
        {
            if (!StoragePlace()) { PlaySE(SE_FAILURE); return; }
            sGlassStorage.holding = FALSE;
        }
        else
        {
            struct Pokemon mon;
            StorageRead(sGlassStorage.box, cursor < 30 ? cursor : cursor - 30, cursor >= 30, &mon);
            if (!GetMonData(&mon, MON_DATA_SPECIES)) return;
            sGlassStorage.holding = TRUE;
            sGlassStorage.sourceParty = cursor >= 30;
            sGlassStorage.sourceSlot = cursor < 30 ? cursor : cursor - 30;
            sGlassStorage.sourceBox = sGlassStorage.box;
        }
    }
    else if (cursor == 36)
    {
        if (JOY_NEW(DPAD_UP | DPAD_RIGHT)) sGlassStorage.cursor = sGlassStorage.panel ? 34 : 24;
        else return;
    }
    else if (cursor >= 30)
    {
        if (JOY_NEW(DPAD_RIGHT)) sGlassStorage.cursor = cursor % 2 ? (cursor - 30) / 2 * 6 : cursor + 1;
        else if (JOY_NEW(DPAD_LEFT)) sGlassStorage.cursor = cursor % 2 ? cursor - 1 : 36;
        else if (JOY_NEW(DPAD_UP)) sGlassStorage.cursor = cursor >= 32 ? cursor - 2 : 36;
        else if (JOY_NEW(DPAD_DOWN)) sGlassStorage.cursor = cursor < 34 ? cursor + 2 : 36;
        else return;
    }
    else
    {
        if (JOY_NEW(DPAD_LEFT)) sGlassStorage.cursor = cursor % 6 ? cursor - 1 : (sGlassStorage.panel ? 30 + (cursor / 6 / 2) * 2 + 1 : 36);
        else if (JOY_NEW(DPAD_RIGHT)) sGlassStorage.cursor = cursor % 6 < 5 ? cursor + 1 : 36;
        else if (JOY_NEW(DPAD_UP)) sGlassStorage.cursor = cursor >= 6 ? cursor - 6 : 36;
        else if (JOY_NEW(DPAD_DOWN)) sGlassStorage.cursor = cursor < 24 ? cursor + 6 : 36;
        else return;
    }
    if (sGlassStorage.holding && sGlassStorage.cursor == 36 && !sGlassStorage.panel)
    {
        sGlassStorage.panel = TRUE;
        sGlassStorage.cursor = 30;
    }
    PlaySE(SE_SELECT);
    DrawGlassStorage();
}

void ShowPokeGlassStorage(void)
{
    u8 taskId;
    QuantumRecoverStoredItemsAndPokemon();
    if (!OpenTabletWindow()) return;
    sStoragePortrait = 0xFFFF;
    memset(&sGlassStorage, 0, sizeof(sGlassStorage));
    memset(sGlassStorage.icons, MAX_SPRITES, sizeof(sGlassStorage.icons));
    sGlassStorage.box = StorageGetCurrentBox();
    taskId = CreateTask(Task_GlassStorage, 80);
    if (taskId == TASK_NONE)
    {
        CloseHub(); RestoreTabletAppearance(); ScriptContext_Enable(); return;
    }
    DrawGlassStorage();
}


static const u8 sGlassMapKanto[] = INCBIN_U8("graphics/poke_glass_maps/kanto.bin");
static const u8 sGlassMap123[] = INCBIN_U8("graphics/poke_glass_maps/sevii_123.bin");
static const u8 sGlassMapQuantum[] = INCBIN_U8("graphics/poke_glass_maps/quantum.bin");
static const u8 sGlassMap67[] = INCBIN_U8("graphics/poke_glass_maps/sevii_67.bin");
static const u16 sGlassMapPalette[] = INCBIN_U16("graphics/poke_glass_maps/atlas_palette.bin");
static EWRAM_DATA struct {
    u8 region, x, y;
    u16 palette[16];
} sGlassMap = {0};

static void DrawGlassMap(void)
{
    static const u8 *const maps[] = {sGlassMapKanto, sGlassMap123, sGlassMapQuantum, sGlassMap67};
    u16 section = PokeGlassMapSection(sGlassMap.region, sGlassMap.x, sGlassMap.y);
    u8 name[64];
    u16 x = 16 + (sGlassMap.x * 8 + 36) * 192 / 240;
    u16 y = 32 + (sGlassMap.y * 8 + 36) * 80 / 160;
    DrawTabletShell((u8 *)GetWindowAttribute(sHubWindow, WINDOW_TILE_DATA));
    StatsText(18, 15, sGlassMap.region == 2 ? COMPOUND_STRING("QUANTUM") : COMPOUND_STRING("KANTO"));
    BlitBitmapToWindow(sHubWindow, maps[sGlassMap.region], 16, 32, 192, 80);
    // Map tiles use their own palette; the shell keeps its original colors.
    HubRect(15, x - 2, y - 2, 5, 1);
    HubRect(15, x - 2, y + 2, 5, 1);
    HubRect(15, x - 2, y - 1, 1, 3);
    HubRect(15, x + 2, y - 1, 1, 3);
    if (section != MAPSEC_NONE)
    {
        GetMapName(name, section, 0);
        StatsText(80, 114, name);
    }
    StatsText(18, 114, COMPOUND_STRING("A Guide"));
    StatsText(143, 15, COMPOUND_STRING("L/R Map"));
    PutWindowTilemap(sHubWindow);
    PutWindowRectTilemapOverridePalette(sHubWindow, 2, 4, 24, 10, 9);
    CopyWindowToVram(sHubWindow, COPYWIN_FULL);
}

static void Task_GlassMap(u8 taskId)
{
    if (gTasks[taskId].data[0]++ < 2) return;
    gTasks[taskId].data[0] = 2;
    if (JOY_NEW(B_BUTTON | A_BUTTON))
    {
        bool8 native = JOY_NEW(A_BUTTON) != 0;
        LoadPalette(sGlassMap.palette, BG_PLTT_ID(9), sizeof(sGlassMap.palette));
        if (native)
        {
            // Travel and dungeon guides retain the native eligibility checks.
            sTabletNative = TRUE;
            sHubWindow = WINDOW_NONE;
            DestroyTask(taskId);
            OpenPokeGlassMapNative();
            return;
        }
        CloseHub();
        gTasks[taskId].data[2] = 0;
        gTasks[taskId].data[3] = FALSE;
        gTasks[taskId].func = Task_CloseTablet;
        return;
    }
    if (JOY_NEW(L_BUTTON | R_BUTTON))
    {
        // Old Sevii pages are retired; the island remains previewable before travel.
        sGlassMap.region = sGlassMap.region == 2 ? 0 : 2;
    }
    else if (JOY_NEW(DPAD_LEFT) && sGlassMap.x) sGlassMap.x--;
    else if (JOY_NEW(DPAD_RIGHT) && sGlassMap.x < 21) sGlassMap.x++;
    else if (JOY_NEW(DPAD_UP) && sGlassMap.y) sGlassMap.y--;
    else if (JOY_NEW(DPAD_DOWN) && sGlassMap.y < 14) sGlassMap.y++;
    else return;
    PlaySE(SE_SELECT);
    DrawGlassMap();
}

void ShowPokeGlassMap(void)
{
    u8 taskId;
    if (!OpenTabletWindow()) return;
    taskId = CreateTask(Task_GlassMap, 80);
    if (taskId == TASK_NONE)
    {
        CloseHub(); ScriptContext_Enable(); return;
    }
    sGlassMap.region = PokeGlassPlayerRegion();
    sGlassMap.x = sGlassMap.region == 2 ? 15 : 4;
    sGlassMap.y = sGlassMap.region == 2 ? 12 : 9;
    CpuCopy16(&gPlttBufferUnfaded[BG_PLTT_ID(9)], sGlassMap.palette, sizeof(sGlassMap.palette));
    LoadPalette(sGlassMapPalette, BG_PLTT_ID(9), sizeof(sGlassMapPalette));
    DrawGlassMap();
}

void PreparePokeGlassReturn(void)
{
    if (!sTabletActive || !sTabletNative) return;
    CapturePokeGlassBackdrop();
    if (!OpenTabletWindow()) return;
    DrawTabletShell((u8 *)GetWindowAttribute(sHubWindow, WINDOW_TILE_DATA));
    PutWindowTilemap(sHubWindow);
    CopyWindowToVram(sHubWindow, COPYWIN_FULL);
}

void EndPokeGlassSession(void)
{
    sTabletActive = FALSE;
    sTabletNative = FALSE;
    sHubWindow = WINDOW_NONE;
    ReleasePokeGlassBackdrop();
}
