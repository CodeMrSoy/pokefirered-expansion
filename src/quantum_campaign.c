#include "global.h"
#include "quantum_campaign.h"
#include "event_data.h"
#include "overworld.h"
#include "load_save.h"
#include "roamer.h"
#include "constants/maps.h"
#include "constants/layouts.h"
#include "constants/flags.h"
#include "constants/vars.h"
#include "data/quantum_retired_maps.h"

bool8 IsQuantumRetiredMap(s8 mapGroup, s8 mapNum)
{
    u32 i;
    for (i = 0; i < ARRAY_COUNT(sQuantumRetiredMaps); i++)
        if (MAP_GROUP(sQuantumRetiredMaps[i]) == mapGroup
            && MAP_NUM(sQuantumRetiredMaps[i]) == mapNum)
            return TRUE;
    return FALSE;
}

static bool8 RepairRetiredWarp(struct WarpData *warp)
{
    if (!IsQuantumRetiredMap(warp->mapGroup, warp->mapNum))
        return FALSE;
    warp->mapGroup = MAP_GROUP(MAP_PALLET_TOWN);
    warp->mapNum = MAP_NUM(MAP_PALLET_TOWN);
    warp->warpId = -1;
    warp->x = 6;
    warp->y = 8;
    return TRUE;
}

void SanitizeQuantumCampaignSave(void)
{
    u32 i;
    if (RepairRetiredWarp(&gSaveBlock1Ptr->location))
    {
        gSaveBlock1Ptr->pos.x = 6;
        gSaveBlock1Ptr->pos.y = 8;
        gSaveBlock1Ptr->mapLayoutId = LAYOUT_PALLET_TOWN;
        gSaveBlock1Ptr->weather = 0;
        gSaveBlock1Ptr->flashLevel = 0;
        ResetInitialPlayerAvatarState();
        // Reload through a real warp rather than old saved object templates.
        gSaveBlock1Ptr->continueGameWarp = gSaveBlock1Ptr->location;
        SetContinueGameWarpStatus();
    }
    RepairRetiredWarp(&gSaveBlock1Ptr->continueGameWarp);
    RepairRetiredWarp(&gSaveBlock1Ptr->dynamicWarp);
    RepairRetiredWarp(&gSaveBlock1Ptr->lastHealLocation);
    RepairRetiredWarp(&gSaveBlock1Ptr->escapeWarp);
    for (i = 0; i < ARRAY_COUNT(sQuantumRetiredWorldMapFlags); i++)
        FlagClear(sQuantumRetiredWorldMapFlags[i]);
    FlagClear(FLAG_SYS_CAN_LINK_WITH_RS);
    FlagClear(FLAG_SYS_SEVII_MAP_4567);
    FlagClear(FLAG_ENABLE_SHIP_NAVEL_ROCK);
    FlagClear(FLAG_ENABLE_SHIP_BIRTH_ISLAND);
    FlagClear(FLAG_HIDE_CERULEAN_CAVE_GUARD);
    FlagSet(FLAG_HIDE_POSTGAME_GOSSIPERS);
    // Values 0/1 belong to the starter sequence; only retire the post-League scene.
    if (VarGet(VAR_MAP_SCENE_PALLET_TOWN_OAK) >= 2)
        VarSet(VAR_MAP_SCENE_PALLET_TOWN_OAK, 3);
    if (VarGet(VAR_MAP_SCENE_PALLET_TOWN_PROFESSOR_OAKS_LAB) >= 7)
        VarSet(VAR_MAP_SCENE_PALLET_TOWN_PROFESSOR_OAKS_LAB, 9);
    if (VarGet(VAR_MAP_SCENE_ONE_ISLAND_POKEMON_CENTER_1F) >= 4)
        VarSet(VAR_MAP_SCENE_ONE_ISLAND_POKEMON_CENTER_1F, 3);
    DeactivateAllRoamers();
}
