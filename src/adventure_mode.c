#include "global.h"
#include "adventure_mode.h"
#include "constants/region_map_sections.h"
#include "constants/seagallop.h"
#include <stddef.h>
#include "data/map_group_count.h"

// ARM ABI measured on the unmodified V2 2742860df baseline. These assertions
// guard the actual save layout rather than the stale offset comments in global.h.
STATIC_ASSERT(sizeof(struct SaveBlock1) == 15780, AdventureSaveBlock1Size);
STATIC_ASSERT(sizeof(struct SaveBlock2) == 3968, AdventureSaveBlock2Size);
STATIC_ASSERT(offsetof(struct SaveBlock2, randomizerSeed) == 3756, AdventureSeedOffset);
STATIC_ASSERT(offsetof(struct SaveBlock2, gameModesVersion) == 3761, AdventureGameModesOffset);
STATIC_ASSERT(offsetof(struct SaveBlock2, nuzlockeAreas) == 3763, AdventureNuzlockeOffset);
STATIC_ASSERT(offsetof(struct SaveBlock2, adventureModeRecord) == 3795, AdventureReservedOffset);
STATIC_ASSERT(sizeof(((struct SaveBlock2 *)0)->adventureModeRecord)
    + sizeof(((struct SaveBlock2 *)0)->questBookRecord)
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
    extern const struct MapHeader *const *gMapGroups[];
    u16 section;
    if (group < 0 || group >= MAP_GROUPS_COUNT || number < 0
        || number >= MAP_GROUP_COUNT[(u8)group])
        return FALSE;
    // These interiors are shared: Celadon in Classic, Havora in Quantum.
    if (group == MAP_GROUP(MAP_CELADON_CITY_DEPARTMENT_STORE_1F)
        && number <= MAP_NUM(MAP_CELADON_CITY_DEPARTMENT_STORE_ELEVATOR))
        return FALSE;
    section = gMapGroups[(u8)group][(u8)number]->regionMapSectionId;
    // Includes draft and future Vidra sections after the original map-page end.
    return section >= QUANTUM_MAPSEC_START && section < MAPSEC_COUNT;
}

bool32 AdventureMode_AllowsMap(s8 group, s8 number)
{
    return AdventureMode_IsQuantum() || !AdventureMode_IsVidraMap(group, number);
}

// All legacy Sevii ferry IDs resolve to the retained mainland port. The only
// island destination is Vidra, with both mode and ticket authorization.
u16 AdventureMode_FerryDestination(u16 origin, u16 destination, bool32 hasTicket)
{
    if (destination == SEAGALLOP_QUANTUM_PORT && origin == SEAGALLOP_VERMILION_CITY
        && AdventureMode_IsQuantum() && hasTicket)
        return SEAGALLOP_QUANTUM_PORT;
    return SEAGALLOP_VERMILION_CITY;
}

void AdventureMode_AdjustWarp(struct WarpData *warp)
{
    if (!AdventureMode_IsQuantum()
        && gSaveBlock1Ptr->location.mapGroup == MAP_GROUP(MAP_CELADON_CITY_DEPARTMENT_STORE_1F)
        && gSaveBlock1Ptr->location.mapNum == MAP_NUM(MAP_CELADON_CITY_DEPARTMENT_STORE_1F)
        && warp->mapGroup == MAP_GROUP(MAP_HAVORA_MARKET)
        && warp->mapNum == MAP_NUM(MAP_HAVORA_MARKET))
    {
        warp->mapGroup = MAP_GROUP(MAP_CELADON_CITY);
        warp->mapNum = MAP_NUM(MAP_CELADON_CITY);
        warp->warpId = -1;
        warp->x = 12;
        warp->y = 14;
    }
}

void AdventureMode_AdjustMapHeader(struct MapHeader *header)
{
    // The department-store interiors are shared by both adventures. Classic
    // reaches them from Celadon; Quantum reaches them from Havora Market.
    if (!AdventureMode_IsQuantum() && header->regionMapSectionId == MAPSEC_HAVORA_CITY
        && gSaveBlock1Ptr->location.mapGroup == MAP_GROUP(MAP_CELADON_CITY_DEPARTMENT_STORE_1F))
        header->regionMapSectionId = MAPSEC_CELADON_CITY;
}
