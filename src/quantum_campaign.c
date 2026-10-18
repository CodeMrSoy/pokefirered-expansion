#include "global.h"
#include "quantum_campaign.h"
#include "quantum_cleanup.h"
#include "event_data.h"
#include "overworld.h"
#include "load_save.h"
#include "roamer.h"
#include "constants/maps.h"
#include "constants/layouts.h"
#include "constants/flags.h"
#include "constants/vars.h"
#include "data/quantum_retired_maps.h"

void SanitizeQuantumCampaignSave(void)
{
    u32 i;
    QuantumMigrateLoadedWorld();
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
