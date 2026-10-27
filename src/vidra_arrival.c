#include "global.h"
#include "gflib.h"
#include "vidra_arrival.h"
#include "decompress.h"
#include "event_object_movement.h"
#include "field_fadetransition.h"
#include "field_weather.h"
#include "overworld.h"
#include "scanline_effect.h"
#include "script.h"
#include "script_movement.h"
#include "task.h"
#include "constants/event_object_movement.h"
#include "constants/event_objects.h"

static const u32 sArrivalTiles[] = INCBIN_U32("graphics/vidra_arrival/vidra.8bpp.lz");
static const u16 sArrivalPalette[] = INCBIN_U16("graphics/vidra_arrival/vidra.gbapal");
static const u16 sArrivalMap[] = INCBIN_U16("graphics/vidra_arrival/vidra.bin");
static const struct BgTemplate sArrivalBg = {
    .bg = 0, .charBaseIndex = 0, .mapBaseIndex = 31,
    .screenSize = 0, .paletteMode = 1, .priority = 0,
};
static EWRAM_DATA MainCallback sArrivalCallback = NULL;
static EWRAM_DATA u16 sArrivalFrames = 0;
static EWRAM_DATA u8 sArrivalState = 0;

static void VBlankCB_VidraArrival(void)
{
    LoadOam();
    TransferPlttBuffer();
}

static void CB2_VidraArrival(void)
{
    switch (sArrivalState)
    {
    case 0:
        SetVBlankCallback(NULL);
        SetGpuReg(REG_OFFSET_DISPCNT, 0);
        ScanlineEffect_Stop();
        ResetTasks();
        ResetSpriteData();
        FreeAllSpritePalettes();
        ResetPaletteFade();
        ResetBgsAndClearDma3BusyFlags(0);
        DmaClearLarge16(3, (void *)VRAM, VRAM_SIZE, 0x1000);
        InitBgsFromTemplates(0, &sArrivalBg, 1);
        SetGpuReg(REG_OFFSET_BLDCNT, 0);
        SetGpuReg(REG_OFFSET_BLDALPHA, 0);
        SetGpuReg(REG_OFFSET_BLDY, 0);
        ChangeBgX(0, 0, BG_COORD_SET);
        ChangeBgY(0, 0, BG_COORD_SET);
        sArrivalState++;
        break;
    case 1:
        LZ77UnCompVram(sArrivalTiles, (void *)VRAM);
        CpuCopy16(sArrivalMap, (void *)(VRAM + 31 * 0x800), sizeof(sArrivalMap));
        LoadPalette(sArrivalPalette, 0, sizeof(sArrivalPalette));
        BeginNormalPaletteFade(PALETTES_ALL, 0, 16, 0, RGB_BLACK);
        BuildOamBuffer();
        SetVBlankCallback(VBlankCB_VidraArrival);
        ShowBg(0);
        sArrivalState++;
        break;
    case 2:
        if (!gPaletteFade.active)
        {
            sArrivalFrames++;
            // Show the complete artwork for three seconds; a deliberate new
            // button press can continue after its first second.
            if (sArrivalFrames >= 180 || (sArrivalFrames >= 60 && JOY_NEW(A_BUTTON | B_BUTTON)))
            {
                BeginNormalPaletteFade(PALETTES_ALL, 0, 0, 16, RGB_BLACK);
                sArrivalState++;
            }
        }
        break;
    case 3:
        if (!gPaletteFade.active)
        {
            MainCallback callback = sArrivalCallback;
            SetVBlankCallback(NULL);
            sArrivalCallback = NULL;
            callback();
            return;
        }
        break;
    }
    UpdatePaletteFade();
}

void ShowVidraArrival(MainCallback callback)
{
    sArrivalCallback = callback;
    sArrivalFrames = 0;
    sArrivalState = 0;
    SetMainCallback2(CB2_VidraArrival);
}

// Script/debug preview, also available on QOL before its Vidra maps are merged.
void ShowVidraArrivalArt(void)
{
    ShowVidraArrival(CB2_ReturnToFieldContinueScript);
}

static const u8 sDisembarkMovement[] = {
    MOVEMENT_ACTION_FACE_DOWN,
    MOVEMENT_ACTION_WALK_NORMAL_DOWN,
    MOVEMENT_ACTION_WALK_NORMAL_DOWN,
    MOVEMENT_ACTION_WALK_NORMAL_DOWN,
    MOVEMENT_ACTION_STEP_END,
};

static void Task_VidraDisembark(u8 taskId)
{
    if (gTasks[taskId].data[0] == 0)
    {
        if (!FieldFadeTransitionBackgroundEffectIsFinished())
            return;
        ScriptMovement_StartObjectMovementScript(LOCALID_PLAYER,
            gSaveBlock1Ptr->location.mapNum, gSaveBlock1Ptr->location.mapGroup, sDisembarkMovement);
        gTasks[taskId].data[0]++;
    }
    else if (ScriptMovement_IsObjectMovementFinished(LOCALID_PLAYER,
        gSaveBlock1Ptr->location.mapNum, gSaveBlock1Ptr->location.mapGroup))
    {
        ScriptMovement_UnfreezeObjectEvents();
        UnfreezeObjectEvents();
        UnlockPlayerFieldControls();
        DestroyTask(taskId);
    }
}

void FieldCB_VidraDisembark(void)
{
    Overworld_PlaySpecialMapMusic();
    FreezeObjectEvents();
    LockPlayerFieldControls();
    FadeInFromBlack();
    if (CreateTask(Task_VidraDisembark, 10) == TASK_NONE)
    {
        UnfreezeObjectEvents();
        UnlockPlayerFieldControls();
    }
}
