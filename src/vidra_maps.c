#include "global.h"
#include "event_data.h"
#include "vidra_maps.h"
#include "constants/maps.h"
#include "constants/vars.h"

// Before Vidra was split into settlement groups, all its maps used group 43.
// Keep the legacy numeric order here: never sort or regenerate from new groups.
static const u16 sLegacyVidraMaps[] = {
    MAP_HAVORA_WEST_QUADRANT,
    MAP_HAVORA_POKEMON_CENTER_1_F,
    MAP_HAVORA_POKEMON_CENTER_2_F,
    MAP_CORVALA_TOWN,
    MAP_CORVALA_TOWN_POKEMON_CENTER_1_F,
    MAP_CORVALA_TOWN_POKEMON_CENTER_2_F,
    MAP_ELDERVALE_VILLAGE,
    MAP_ELDERVALE_VILLAGE_POKEMON_CENTER_1_F,
    MAP_ELDERVALE_VILLAGE_POKEMON_CENTER_2_F,
    MAP_MYRDAL_CITY,
    MAP_MYRDAL_CITY_POKEMON_CENTER_1_F,
    MAP_MYRDAL_CITY_POKEMON_CENTER_2_F,
    MAP_ISKORA_VILLAGE,
    MAP_ISKORA_VILLAGE_POKEMON_CENTER_1_F,
    MAP_ISKORA_VILLAGE_POKEMON_CENTER_2_F,
    MAP_VIDRA_HARBOR_ROAD,
    MAP_VIDRA_COASTAL_ROAD,
    MAP_ELDERVIK_WOODS,
    MAP_FROSTFELL_MOUNTAINS,
    MAP_HAVORA_HARBOR,
    MAP_HAVORA_RIVER,
    MAP_HAVORA_MARKET,
    MAP_HAVORA_SHIPWRIGHT_HOUSE,
    MAP_HAVORA_WEAVER_HOUSE,
    MAP_HAVORA_FISHER_HOUSE,
    MAP_HAVORA_TRADER_HOUSE,
    MAP_HAVORA_TRADE_HALL,
    MAP_HAVORA_OUTFITTERS,
    MAP_HAVORA_PROVISIONS,
    MAP_HAVORA_NORTH_QUADRANT,
    MAP_HAVORA_DAYCARE_EXTERIOR,
    MAP_HAVORA_LOOKOUT,
    MAP_HAVORA_GYM,
    MAP_HAVORA_MART,
    MAP_HAVORA_DAYCARE_INTERIOR,
    MAP_HAVORA_WEST_HOUSE_1,
    MAP_HAVORA_WEST_HOUSE_2,
    MAP_HAVORA_NORTH_HOUSE_1,
    MAP_HAVORA_NORTH_HOUSE_2,
    MAP_HAVORA_NORTH_HOUSE_3,
    MAP_HAVORA_CLIFF_HOUSE_1,
    MAP_HAVORA_CLIFF_HOUSE_2,
    MAP_HAVORA_CLIFF_HOUSE_3,
    MAP_HAVORA_CLIFF_HOUSE_4,
    MAP_HAVORA_CLIFF_HOUSE_5,
    MAP_HAVORA_HARBOR_INN,
    MAP_HAVORA_NORTH_HOUSE_4,
    MAP_HAVORA_NORTH_HOUSE_5,
    MAP_HAVORA_NORTH_LODGE,
    MAP_HAVORA_COASTAL_CLIFFS,
};

static void MigrateMapPair(s8 *group, s8 *number)
{
    if (*group == 43 && (u8)*number < ARRAY_COUNT(sLegacyVidraMaps))
    {
        u16 map = sLegacyVidraMaps[(u8)*number];
        *group = MAP_GROUP(map);
        *number = MAP_NUM(map);
    }
}

void VidraMigrateMapIds(void)
{
    u32 i;
    struct WarpData *warps[] = {
        &gSaveBlock1Ptr->location, &gSaveBlock1Ptr->continueGameWarp,
        &gSaveBlock1Ptr->dynamicWarp, &gSaveBlock1Ptr->lastHealLocation,
        &gSaveBlock1Ptr->escapeWarp,
    };
    if (VarGet(VAR_VIDRA_MAP_VERSION) >= 1)
        return;
    for (i = 0; i < ARRAY_COUNT(warps); i++)
        MigrateMapPair(&warps[i]->mapGroup, &warps[i]->mapNum);
    for (i = 0; i < OBJECT_EVENTS_COUNT; i++)
    {
        struct ObjectEvent *object = &gSaveBlock1Ptr->objectEvents[i];
        s8 group = object->mapGroup, number = object->mapNum;
        MigrateMapPair(&group, &number);
        object->mapGroup = group;
        object->mapNum = number;
    }
    // Old Vidra recap scripts may contain encoded map IDs; retire these scenes
    // rather than replaying a transition using the wrong group/number pair.
    for (i = 0; i < QUEST_LOG_SCENE_COUNT; i++)
        if (gSaveBlock1Ptr->questLog[i].mapGroup == 43)
            gSaveBlock1Ptr->questLog[i].startType = 0;
    if (gSaveBlock1Ptr->ramScript.data.mapGroup == 43)
        memset(&gSaveBlock1Ptr->ramScript, 0, sizeof(gSaveBlock1Ptr->ramScript));
    VarSet(VAR_VIDRA_MAP_VERSION, 1);
}
