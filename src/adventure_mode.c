#include "global.h"
#include "adventure_mode.h"
#include "constants/region_map_sections.h"
#include <stddef.h>

// ARM ABI measured on the unmodified V2 2742860df baseline. These assertions
// guard the actual save layout rather than the stale offset comments in global.h.
STATIC_ASSERT(sizeof(struct SaveBlock1) == 15780, AdventureSaveBlock1Size);
STATIC_ASSERT(sizeof(struct SaveBlock2) == 3968, AdventureSaveBlock2Size);
STATIC_ASSERT(offsetof(struct SaveBlock2, randomizerSeed) == 3756, AdventureSeedOffset);
STATIC_ASSERT(offsetof(struct SaveBlock2, gameModesVersion) == 3761, AdventureGameModesOffset);
STATIC_ASSERT(offsetof(struct SaveBlock2, nuzlockeAreas) == 3763, AdventureNuzlockeOffset);
STATIC_ASSERT(offsetof(struct SaveBlock2, adventureModeRecord) == 3795, AdventureReservedOffset);
STATIC_ASSERT(sizeof(((struct SaveBlock2 *)0)->adventureModeRecord)
    + sizeof(((struct SaveBlock2 *)0)->filler_90) == 173, AdventureReservedCapacity);

static EWRAM_DATA bool8 sPendingClassic = FALSE;
static const u8 sRecordTag[] = {'Q', 'A', 'D', 'V', 1};
static const u8 sClassicName[] = _("Classic Adventure");
static const u8 sQuantumName[] = _("Quantum Adventure");

static bool32 HasValidRecord(void)
{
    const u8 *record = gSaveBlock2Ptr->adventureModeRecord;
    return memcmp(record, sRecordTag, sizeof(sRecordTag)) == 0
        && record[5] < ADVENTURE_MODE_COUNT
        && record[6] == (u8)(record[5] ^ 0xFF)
        && record[7] == 0xA7;
}

static void WriteRecord(u8 mode)
{
    u8 *record = gSaveBlock2Ptr->adventureModeRecord;
    memcpy(record, sRecordTag, sizeof(sRecordTag));
    record[5] = mode;
    record[6] = mode ^ 0xFF;
    record[7] = 0xA7;
}

u8 AdventureMode_Get(void)
{
    // Reading a V2 save does not modify it. Checksummed loading owns migration.
    return HasValidRecord() ? gSaveBlock2Ptr->adventureModeRecord[5] : ADVENTURE_MODE_QUANTUM;
}

bool32 AdventureMode_IsQuantum(void)
{
    return AdventureMode_Get() == ADVENTURE_MODE_QUANTUM;
}

const u8 *AdventureMode_Name(u8 mode)
{
    return mode == ADVENTURE_MODE_CLASSIC ? sClassicName : sQuantumName;
}

void AdventureMode_ResetPending(void)
{
    sPendingClassic = FALSE;
}

bool32 AdventureMode_SelectNewGame(u8 mode)
{
    if (mode >= ADVENTURE_MODE_COUNT)
        return FALSE;
    sPendingClassic = mode == ADVENTURE_MODE_CLASSIC;
    return TRUE;
}

u8 AdventureMode_GetPending(void)
{
    return sPendingClassic ? ADVENTURE_MODE_CLASSIC : ADVENTURE_MODE_QUANTUM;
}

void AdventureMode_NewGame(void)
{
    WriteRecord(AdventureMode_GetPending());
}

void AdventureMode_MigrateLoadedSave(void)
{
    if (!HasValidRecord())
        WriteRecord(ADVENTURE_MODE_QUANTUM);
}

bool32 AdventureMode_IsVidraMap(s8 group, s8 number)
{
    // Dedicated Vidra groups, including their interiors and draft routes. No
    // header dereference: malformed/stale warp indices cannot overrun a table.
    return group >= MAP_GROUP(MAP_HAVORA_HARBOR)
        && group <= MAP_GROUP(MAP_VIDRA_DRAFT_CORVALA);
}

bool32 AdventureMode_AllowsMap(s8 group, s8 number)
{
    return AdventureMode_IsQuantum() || !AdventureMode_IsVidraMap(group, number);
}
