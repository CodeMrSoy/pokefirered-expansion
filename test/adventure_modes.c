#include "global.h"
#include "test/test.h"
#include "adventure_mode.h"
#include "game_modes.h"
#include "quantum_cleanup.h"

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
    u8 original[sizeof(struct SaveBlock2)];
    u32 i;
    memset(gSaveBlock2Ptr, 0x5A, sizeof(struct SaveBlock2));
    memcpy(original, gSaveBlock2Ptr, sizeof(original));
    AdventureMode_MigrateLoadedSave();
    EXPECT_EQ(AdventureMode_Get(), ADVENTURE_MODE_QUANTUM);
    for (i = 0; i < sizeof(original); i++)
        if (i < 3795 || i >= 3803)
            EXPECT_EQ(((u8 *)gSaveBlock2Ptr)[i], original[i]);
    memcpy(original, gSaveBlock2Ptr, sizeof(original));
    AdventureMode_MigrateLoadedSave();
    EXPECT_EQ(memcmp(original, gSaveBlock2Ptr, sizeof(original)), 0);
    memset(gSaveBlock2Ptr, 0, sizeof(struct SaveBlock2));
    AdventureMode_ResetPending();
    AdventureMode_NewGame();
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
}
