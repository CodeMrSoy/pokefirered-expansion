#include "global.h"
#include "test/test.h"
#include "adventure_mode.h"
#include "game_modes.h"
#include "randomizer.h"
#include "malloc.h"
#include "quantum_cleanup.h"
#include "constants/region_map_sections.h"

TEST("Adventure: legacy padding reads Quantum without being modified")
{
    u8 original[8];
    memset(gSaveBlock2Ptr->adventureModeRecord, 0xCC, 8);
    memcpy(original, gSaveBlock2Ptr->adventureModeRecord, 8);
    EXPECT_EQ(AdventureMode_Get(), ADVENTURE_MODE_QUANTUM);
    EXPECT_EQ(memcmp(original, gSaveBlock2Ptr->adventureModeRecord, 8), 0);
}

TEST("Adventure: pending New Game choice cannot change the loaded adventure")
{
    AdventureMode_ResetPending();
    AdventureMode_NewGame();
    EXPECT_EQ(AdventureMode_GetPending(), ADVENTURE_MODE_QUANTUM);
    EXPECT(AdventureMode_SelectNewGame(ADVENTURE_MODE_CLASSIC));
    EXPECT_EQ(AdventureMode_Get(), ADVENTURE_MODE_QUANTUM);
    EXPECT(!AdventureMode_SelectNewGame(ADVENTURE_MODE_COUNT));
    EXPECT_EQ(AdventureMode_GetPending(), ADVENTURE_MODE_CLASSIC);
    AdventureMode_NewGame();
    EXPECT_EQ(AdventureMode_Get(), ADVENTURE_MODE_CLASSIC);
    AdventureMode_ResetPending();
    EXPECT_EQ(AdventureMode_Get(), ADVENTURE_MODE_CLASSIC);
    AdventureMode_MigrateLoadedSave();
    EXPECT_EQ(AdventureMode_Get(), ADVENTURE_MODE_CLASSIC);
    AdventureMode_NewGame();
}

TEST("Adventure: legacy migration changes only its eight reserved bytes")
{
    u8 *original = Alloc(sizeof(struct SaveBlock2));
    struct SaveBlock2 *backup = Alloc(sizeof(struct SaveBlock2));
    EXPECT(original != NULL && backup != NULL);
    memcpy(backup, gSaveBlock2Ptr, sizeof(*backup));
    u32 i;
    memset(gSaveBlock2Ptr, 0x5A, sizeof(struct SaveBlock2));
    memcpy(original, gSaveBlock2Ptr, sizeof(struct SaveBlock2));
    AdventureMode_MigrateLoadedSave();
    EXPECT_EQ(AdventureMode_Get(), ADVENTURE_MODE_QUANTUM);
    for (i = 0; i < sizeof(struct SaveBlock2); i++)
        if (i < 3795 || i >= 3803)
            EXPECT_EQ(((u8 *)gSaveBlock2Ptr)[i], original[i]);
    memcpy(original, gSaveBlock2Ptr, sizeof(struct SaveBlock2));
    AdventureMode_MigrateLoadedSave();
    EXPECT_EQ(memcmp(original, gSaveBlock2Ptr, sizeof(struct SaveBlock2)), 0);
    memcpy(gSaveBlock2Ptr, backup, sizeof(*backup));
    Free(original);
    Free(backup);
    AdventureMode_ResetPending();
}

TEST("Adventure: record signature protects against arbitrary V2 reserved data")
{
    u32 i;
    AdventureMode_SelectNewGame(ADVENTURE_MODE_CLASSIC);
    AdventureMode_NewGame();
    for (i = 0; i < 8; i++)
    {
        gSaveBlock2Ptr->adventureModeRecord[i] ^= 0x40;
        EXPECT_EQ(AdventureMode_Get(), ADVENTURE_MODE_QUANTUM);
        gSaveBlock2Ptr->adventureModeRecord[i] ^= 0x40;
        EXPECT_EQ(AdventureMode_Get(), ADVENTURE_MODE_CLASSIC);
    }
    AdventureMode_ResetPending();
    AdventureMode_NewGame();
}

TEST("Adventure: every independent gameplay setting survives mode initialization")
{
    u32 mode, bits;
    for (mode = 0; mode < ADVENTURE_MODE_COUNT; mode++)
    {
        for (bits = 0; bits < 128; bits++)
        {
            gSaveBlock2Ptr->gameModesVersion = GAME_MODE_VERSION;
            gSaveBlock2Ptr->gameModes = bits;
            gSaveBlock2Ptr->randomizerSeed = 0x12345678;
            AdventureMode_SelectNewGame(mode);
            AdventureMode_NewGame();
            EXPECT_EQ(AdventureMode_Get(), mode);
            EXPECT_EQ(gSaveBlock2Ptr->gameModes, bits);
            EXPECT_EQ(gSaveBlock2Ptr->randomizerSeed, 0x12345678);
        }
    }
    AdventureMode_ResetPending();
    AdventureMode_NewGame();
    gSaveBlock2Ptr->gameModes = GAME_MODE_LEVEL_CAPS;
    gSaveBlock2Ptr->randomizerSeed = 0;
    gCachedRandomizerSeed = 0;
    GameModes_Apply();
}

TEST("Adventure: all Sevii ferry IDs are disabled and Vidra requires Quantum and a ticket")
{
    u32 mode, origin, dest, ticket;
    for (mode = 0; mode < ADVENTURE_MODE_COUNT; mode++)
    {
        AdventureMode_SelectNewGame(mode); AdventureMode_NewGame();
        for (origin = 0; origin < 13; origin++)
            for (dest = 0; dest < 14; dest++)
                for (ticket = 0; ticket < 2; ticket++)
                    EXPECT_EQ(AdventureMode_FerryDestination(origin, dest, ticket),
                        mode == ADVENTURE_MODE_QUANTUM && origin == 0 && dest == 11 && ticket ? 11 : 0);
    }
    AdventureMode_ResetPending(); AdventureMode_NewGame();
}

TEST("Adventure: Classic blocks every Vidra group but retains shared shop interiors")
{
    u32 group;
    s8 oldGroup = gSaveBlock1Ptr->location.mapGroup, oldNum = gSaveBlock1Ptr->location.mapNum;
    struct WarpData warp;
    struct MapHeader header = {0};
    AdventureMode_SelectNewGame(ADVENTURE_MODE_CLASSIC); AdventureMode_NewGame();
    for (group = MAP_GROUP(MAP_HAVORA_HARBOR); group <= MAP_GROUP(MAP_VIDRA_DRAFT_CORVALA); group++)
    {
        EXPECT(!AdventureMode_AllowsMap(group, 0));
        EXPECT(QuantumIsRetiredMap(group, 0));
    }
    EXPECT(AdventureMode_AllowsMap(MAP_GROUP(MAP_CELADON_CITY_DEPARTMENT_STORE_1F), MAP_NUM(MAP_CELADON_CITY_DEPARTMENT_STORE_1F)));
    gSaveBlock1Ptr->location.mapGroup = MAP_GROUP(MAP_CELADON_CITY_DEPARTMENT_STORE_1F);
    gSaveBlock1Ptr->location.mapNum = MAP_NUM(MAP_CELADON_CITY_DEPARTMENT_STORE_1F);
    warp.mapGroup = MAP_GROUP(MAP_HAVORA_MARKET); warp.mapNum = MAP_NUM(MAP_HAVORA_MARKET);
    AdventureMode_AdjustWarp(&warp);
    EXPECT_EQ(warp.mapGroup, MAP_GROUP(MAP_CELADON_CITY)); EXPECT_EQ(warp.mapNum, MAP_NUM(MAP_CELADON_CITY));
    EXPECT_EQ(warp.x, 12); EXPECT_EQ(warp.y, 14);
    header.regionMapSectionId = MAPSEC_HAVORA_CITY;
    AdventureMode_AdjustMapHeader(&header);
    EXPECT_EQ(header.regionMapSectionId, MAPSEC_CELADON_CITY);
    AdventureMode_ResetPending(); AdventureMode_NewGame();
    EXPECT(AdventureMode_AllowsMap(MAP_GROUP(MAP_HAVORA_HARBOR), MAP_NUM(MAP_HAVORA_HARBOR)));
    gSaveBlock1Ptr->location.mapGroup = oldGroup; gSaveBlock1Ptr->location.mapNum = oldNum;
}
