#include "global.h"
#include "bg.h"
#include "decompress.h"
#include "event_data.h"
#include "gpu_regs.h"
#include "help_system.h"
#include "intro.h"
#include "main_menu.h"
#include "malloc.h"
#include "menu.h"
#include "palette.h"
#include "reset_rtc_screen.h"
#include "scanline_effect.h"
#include "sound.h"
#include "sprite.h"
#include "task.h"
#include "title_screen.h"
#include "trig.h"
#include "clear_save_data_screen.h"
#include "berry_fix_program.h"
#include "constants/songs.h"

#define TAG_QUANTUM_MINIOR 0x7100
#define TAG_QUANTUM_TRAIL 0x7101
#define MINIOR_FLIGHT_FRAMES 400
#define MINIOR_FLIGHT_PAUSE 90

static EWRAM_DATA u16 sMiniorFlightFrame = 0;

static const u32 sSpaceTiles[] = INCBIN_U32("graphics/title_screen/quantum/space.8bpp.lz");
static const u16 sSpacePalette[] = INCBIN_U16("graphics/title_screen/quantum/space.gbapal");
static const u16 sSpaceMap[] = INCBIN_U16("graphics/title_screen/quantum/space.tilemap");
static const u32 sLogoTiles[] = INCBIN_U32("graphics/title_screen/quantum/pokemon_logo.4bpp.lz");
static const u16 sLogoPalette[] = INCBIN_U16("graphics/title_screen/quantum/pokemon_logo.gbapal");
static const u16 sLogoMap[] = INCBIN_U16("graphics/title_screen/quantum/logo.tilemap");
static const u32 sMiniorTiles[] = INCBIN_U32("graphics/pokemon/minior/front.4bpp.lz");
static const u16 sMiniorPalette[] = INCBIN_U16("graphics/pokemon/minior/normal.gbapal");
static const u8 sVersion[] = _("QUANTUM VERSION");
static const u8 sPressStart[] = _("PRESS START");
static const u16 sTextPalette[16] = {RGB_BLACK, RGB_WHITE, RGB(9, 15, 24)};
static const u8 sTextColors[] = {0, 1, 2};

static const struct BgTemplate sQuantumBgs[] = {
    {.bg = 0, .charBaseIndex = 3, .mapBaseIndex = 30, .paletteMode = 0, .priority = 0},
    {.bg = 1, .charBaseIndex = 0, .mapBaseIndex = 31, .paletteMode = 1, .priority = 3},
};
static const struct WindowTemplate sQuantumWindows[] = {
    {.bg = 0, .tilemapLeft = 4, .tilemapTop = 9, .width = 22, .height = 2, .paletteNum = 9, .baseBlock = 177},
    {.bg = 0, .tilemapLeft = 9, .tilemapTop = 17, .width = 12, .height = 2, .paletteNum = 9, .baseBlock = 221},
    DUMMY_WIN_TEMPLATE,
};

static void SpriteCB_QuantumMinior(struct Sprite *sprite);
static void SpriteCB_QuantumTrail(struct Sprite *sprite);
static void Task_QuantumTitle(u8 taskId);

static const struct OamData sMiniorOam = {
    .shape = SPRITE_SHAPE(64x64), .size = SPRITE_SIZE(64x64), .priority = 1,
};
static const struct OamData sTrailOam = {
    .shape = SPRITE_SHAPE(8x8), .size = SPRITE_SIZE(8x8), .priority = 2,
};
static const u32 sTrailTiles[8] = {
    0x00000000, 0x00011000, 0x00122100, 0x01233210,
    0x01233210, 0x00122100, 0x00011000, 0x00000000,
};
static const u16 sTrailPalette[16] = {RGB_BLACK, RGB(8, 12, 21), RGB(12, 20, 29), RGB(25, 29, 31)};
static const struct SpriteTemplate sMiniorTemplate = {
    .tileTag = TAG_QUANTUM_MINIOR, .paletteTag = TAG_QUANTUM_MINIOR,
    .oam = &sMiniorOam, .anims = gDummySpriteAnimTable,
    .affineAnims = gDummySpriteAffineAnimTable, .callback = SpriteCB_QuantumMinior,
};
static const struct SpriteTemplate sTrailTemplate = {
    .tileTag = TAG_QUANTUM_TRAIL, .paletteTag = TAG_QUANTUM_TRAIL,
    .oam = &sTrailOam, .anims = gDummySpriteAnimTable,
    .affineAnims = gDummySpriteAffineAnimTable, .callback = SpriteCB_QuantumTrail,
};

static void QuantumTitleVBlank(void)
{
    LoadOam();
    ProcessSpriteCopyRequests();
    TransferPlttBuffer();
}

static void QuantumTitleRun(void)
{
    if (++sMiniorFlightFrame >= MINIOR_FLIGHT_FRAMES + MINIOR_FLIGHT_PAUSE)
        sMiniorFlightFrame = 0;
    RunTasks();
    AnimateSprites();
    BuildOamBuffer();
    UpdatePaletteFade();
}

void CB2_InitQuantumTitleScreen(void)
{
    u8 spriteId, i, j;
    // The lead is down-right, with one follower on either wing of the V.
    static const s8 formationOffsets[3][2] = {{0, 0}, {-8, -40}, {-42, -6}};
    const struct CompressedSpriteSheet miniorSheet = {sMiniorTiles, 64 * 64 / 2, TAG_QUANTUM_MINIOR};
    const struct SpritePalette miniorPalette = {sMiniorPalette, TAG_QUANTUM_MINIOR};
    const struct SpriteSheet trailSheet = {sTrailTiles, sizeof(sTrailTiles), TAG_QUANTUM_TRAIL};
    const struct SpritePalette trailPalette = {sTrailPalette, TAG_QUANTUM_TRAIL};

    switch (gMain.state)
    {
    case 0:
        SetVBlankCallback(NULL);
        StartTimer1();
        InitHeap(gHeap, HEAP_SIZE);
        ResetTasks();
        ResetSpriteData();
        sMiniorFlightFrame = 0;
        FreeAllSpritePalettes();
        ResetPaletteFade();
        ScanlineEffect_Stop();
        SetGpuReg(REG_OFFSET_DISPCNT, 0);
        SetGpuReg(REG_OFFSET_BLDCNT, 0);
        SetGpuReg(REG_OFFSET_BLDY, 0);
        SetGpuReg(REG_OFFSET_BLDALPHA, 0);
        DmaFill16(3, 0, (void *)VRAM, VRAM_SIZE);
        DmaFill32(3, 0, (void *)OAM, OAM_SIZE);
        DmaFill16(3, 0, (void *)PLTT, PLTT_SIZE);
        ResetBgsAndClearDma3BusyFlags(FALSE);
        InitBgsFromTemplates(0, sQuantumBgs, ARRAY_COUNT(sQuantumBgs));
        SetGpuRegBits(REG_OFFSET_DISPCNT, DISPCNT_OBJ_1D_MAP | DISPCNT_OBJ_ON);
        LoadPalette(sSpacePalette, 0, 64 * sizeof(u16));
        LoadPalette(sLogoPalette, BG_PLTT_ID(8), PLTT_SIZE_4BPP);
        LoadPalette(sTextPalette, BG_PLTT_ID(9), sizeof(sTextPalette));
        DecompressAndCopyTileDataToVram(1, sSpaceTiles, 0, 0, 0);
        DecompressAndCopyTileDataToVram(0, sLogoTiles, 0, 1, 0);
        LoadBgTilemap(1, sSpaceMap, sizeof(sSpaceMap), 0);
        InitWindows(sQuantumWindows);
        CpuCopy16(sLogoMap, GetBgTilemapBuffer(0), sizeof(sLogoMap));
        DeactivateAllTextPrinters();
        FillWindowPixelBuffer(0, PIXEL_FILL(0));
        AddTextPrinterParameterized3(0, FONT_NORMAL, (176 - GetStringWidth(FONT_NORMAL, sVersion, 0)) / 2, 0, sTextColors, TEXT_SKIP_DRAW, sVersion);
        PutWindowTilemap(0);
        CopyWindowToVram(0, COPYWIN_GFX);
        FillWindowPixelBuffer(1, PIXEL_FILL(0));
        AddTextPrinterParameterized3(1, FONT_SMALL, (96 - GetStringWidth(FONT_SMALL, sPressStart, 0)) / 2, 0, sTextColors, TEXT_SKIP_DRAW, sPressStart);
        PutWindowTilemap(1);
        CopyWindowToVram(1, COPYWIN_GFX);
        CopyBgTilemapBufferToVram(0);
        LoadCompressedSpriteSheet(&miniorSheet);
        LoadSpritePalette(&miniorPalette);
        LoadSpriteSheet(&trailSheet);
        LoadSpritePalette(&trailPalette);
        for (i = 0; i < ARRAY_COUNT(formationOffsets); i++)
        {
            spriteId = CreateSprite(&sMiniorTemplate, -44 + formationOffsets[i][0], -28 + formationOffsets[i][1], i);
            if (spriteId >= MAX_SPRITES)
                continue;
            gSprites[spriteId].data[0] = formationOffsets[i][0];
            gSprites[spriteId].data[1] = formationOffsets[i][1];
            for (j = 0; j < 6; j++)
            {
                u8 trailId = CreateSprite(&sTrailTemplate, -64, -64, j + 3);
                if (trailId < MAX_SPRITES)
                {
                    gSprites[trailId].data[0] = spriteId;
                    gSprites[trailId].data[1] = j;
                }
            }
        }
        gMain.state++;
        break;
    case 1:
        if (FreeTempTileDataBuffersIfPossible())
            return;
        ShowBg(0);
        ShowBg(1);
        BeginNormalPaletteFade(PALETTES_ALL, 0, 16, 0, RGB_BLACK);
        SetHelpContext(HELPCONTEXT_TITLE_SCREEN);
        HelpSystem_Enable();
        CreateTask(Task_QuantumTitle, 0);
        SetVBlankCallback(QuantumTitleVBlank);
        SetMainCallback2(QuantumTitleRun);
        PlayBGM(MUS_TITLE);
        break;
    default:
        gMain.state = 0;
        break;
    }
}

static void SpriteCB_QuantumMinior(struct Sprite *sprite)
{
    // Every member uses the same clock, including the offscreen pause, so the
    // formation stays together as it crosses the screen and loops again.
    sprite->invisible = sMiniorFlightFrame >= MINIOR_FLIGHT_FRAMES;
    if (sprite->invisible)
        return;
    sprite->x = -44 + sMiniorFlightFrame + sprite->data[0];
    sprite->y = -28 + (sMiniorFlightFrame * 11) / 16 + sprite->data[1];
}

static void SpriteCB_QuantumTrail(struct Sprite *sprite)
{
    const struct Sprite *minior = &gSprites[sprite->data[0]];
    s16 distance = 20 + sprite->data[1] * 7;
    sprite->x = minior->x - distance;
    sprite->y = minior->y - (distance * 11) / 16
        + Sin((sMiniorFlightFrame * 3 + sprite->data[1] * 20) & 255, 2);
    sprite->invisible = minior->invisible;
}

static void Task_QuantumTitle(u8 taskId)
{
    s16 *data = gTasks[taskId].data;
    if (data[0] == 0)
    {
        if (!gPaletteFade.active)
            data[0] = 1;
        return;
    }
    if (data[0] == 1)
    {
        data[1]++;
        if ((data[1] % 48) == 0)
        {
            PutWindowTilemap(1);
            CopyBgTilemapBufferToVram(0);
        }
        else if ((data[1] % 48) == 32)
        {
            ClearWindowTilemap(1);
            CopyBgTilemapBufferToVram(0);
        }
        if (JOY_HELD(B_BUTTON | SELECT_BUTTON | DPAD_UP) == (B_BUTTON | SELECT_BUTTON | DPAD_UP))
            data[2] = 1;
        else if (JOY_HELD(B_BUTTON | SELECT_BUTTON | DPAD_LEFT) == (B_BUTTON | SELECT_BUTTON | DPAD_LEFT) && CanResetRTC())
            data[2] = 2;
        else if (JOY_HELD(B_BUTTON | SELECT_BUTTON) == (B_BUTTON | SELECT_BUTTON))
            data[2] = 3;
        else if (JOY_NEW(A_BUTTON | START_BUTTON))
        {
            PlayCry_Normal(SPECIES_MINIOR, 0);
            data[2] = 0;
        }
        else if (data[1] >= 2700)
            data[2] = 4;
        else
            return;
        HelpSystem_Disable();
        FadeOutBGM(4);
        BeginNormalPaletteFade(PALETTES_ALL, 0, 0, 16, RGB_BLACK);
        data[0] = 2;
    }
    else if (!gPaletteFade.active)
    {
        FreeAllWindowBuffers();
        SetBgTilemapBuffer(0, NULL);
        SetBgTilemapBuffer(1, NULL);
        switch (data[2])
        {
        case 1: SetMainCallback2(CB2_SaveClearScreen_Init); break;
        case 2: SetMainCallback2(CB2_InitResetRtcScreen); break;
        case 3: SetMainCallback2(CB2_InitMainMenu); break;
        case 4: SetMainCallback2(CB2_InitCopyrightScreenAfterTitleScreen); break;
        default: SetMainCallback2(CB2_InitMainMenu); break;
        }
        DestroyTask(taskId);
    }
}
