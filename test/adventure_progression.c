#include "global.h"
#include "test/test.h"
#include "adventure_mode.h"
#include "adventure_progression.h"
#include "game_modes.h"
#include "caps.h"
#include "event_data.h"
#include "battle.h"
#include "battle_main.h"
#include "malloc.h"
#include "pokemon.h"
#include "wild_encounter.h"
#include "constants/opponents.h"

static void BeginAdventure(u8 mode)
{
    AdventureMode_SelectNewGame(mode);
    AdventureMode_NewGame();
    gSaveBlock2Ptr->gameModesVersion = GAME_MODE_VERSION;
    gSaveBlock2Ptr->gameModes = GAME_MODE_LEVEL_CAPS;
    gSaveBlock2Ptr->randomizerSeed = 0;
    GameModes_Apply();
}

TEST("Adventure progression: Classic gym teams and caps use the recorded Kanto baseline")
{
    u32 i, j;
    const u16 trainers[] = {TRAINER_LEADER_BROCK, TRAINER_LEADER_MISTY,
        TRAINER_LEADER_LT_SURGE, TRAINER_LEADER_ERIKA, TRAINER_LEADER_KOGA,
        TRAINER_LEADER_SABRINA, TRAINER_LEADER_BLAINE, TRAINER_LEADER_GIOVANNI};
    const u8 caps[] = {14,21,24,29,43,43,47,50};
    BeginAdventure(ADVENTURE_MODE_CLASSIC);
    FlagClear(FLAG_SYS_GAME_CLEAR);
    for (i = 0; i < 8; i++) FlagClear(FLAG_BADGE01_GET + i);
    VarSet(VAR_VIDRA_CRESTS, 0xFFFF); // Classic must not inspect Vidra milestones.
    gBattleStruct = AllocZeroed(sizeof(*gBattleStruct));
    for (i = 0; i < ARRAY_COUNT(trainers); i++)
    {
        const struct Trainer *trainer = GetTrainerStructFromId(trainers[i]);
        u8 ace = 0;
        EXPECT_EQ(GetCurrentLevelCap(), caps[i]);
        CreateNPCTrainerPartyFromTrainer(gEnemyParty, trainer, TRUE, BATTLE_TYPE_TRAINER, trainers[i]);
        for (j = 0; j < trainer->partySize; j++)
        {
            u8 level = GetMonData(&gEnemyParty[j], MON_DATA_LEVEL);
            if (level > ace) ace = level;
            EXPECT_EQ(GetMonData(&gEnemyParty[j], MON_DATA_SPECIES), trainer->party[j].species);
        }
        EXPECT_EQ(ace, caps[i]);
        FlagSet(FLAG_BADGE01_GET + i);
    }
    EXPECT_EQ(GetCurrentLevelCap(), 63);
    CreateNPCTrainerPartyFromTrainer(gEnemyParty, GetTrainerStructFromId(TRAINER_CHAMPION_FIRST_SQUIRTLE),
        TRUE, BATTLE_TYPE_TRAINER, TRAINER_CHAMPION_FIRST_SQUIRTLE);
    for (j = 0; j < 6; j++) EXPECT_LE(GetMonData(&gEnemyParty[j], MON_DATA_LEVEL), 63);
    GameModes_Set(GAME_MODE_LEVEL_CAPS, FALSE);
    EXPECT_EQ(GetCurrentLevelCap(), 100);
    GameModes_Set(GAME_MODE_LEVEL_CAPS, TRUE);
    FlagSet(FLAG_SYS_GAME_CLEAR);
    EXPECT_EQ(GetCurrentLevelCap(), 100);
    FREE_AND_SET_NULL(gBattleStruct);
    for (i = 0; i < 8; i++) FlagClear(FLAG_BADGE01_GET + i);
    FlagClear(FLAG_SYS_GAME_CLEAR); VarSet(VAR_VIDRA_CRESTS, 0);
    BeginAdventure(ADVENTURE_MODE_QUANTUM);
}

TEST("Adventure progression: Quantum preserves Koga Eirik Sabrina and Champion levels")
{
    BeginAdventure(ADVENTURE_MODE_QUANTUM);
    EXPECT_EQ(AdventureMode_TrainerLevel(TRAINER_LEADER_KOGA, 0, 29), 29);
    EXPECT_EQ(AdventureMode_TrainerLevel(TRAINER_LEADER_BLAINE, 0, 58), 58);
    EXPECT_EQ(AdventureMode_TrainerLevel(TRAINER_LEADER_GIOVANNI, 0, 77), 77);
    EXPECT_EQ(AdventureMode_TrainerLevel(TRAINER_CHAMPION_FIRST_SQUIRTLE, 0, 88), 88);
    EXPECT_EQ(AdventureMode_TrainerLevel(TRAINER_HAVORA_CAPTAIN, 0, 46), 46);
    BeginAdventure(ADVENTURE_MODE_CLASSIC);
    EXPECT_EQ(AdventureMode_TrainerLevel(TRAINER_LEADER_GIOVANNI, PARTY_SIZE, 77), 77);
    EXPECT_EQ(AdventureMode_TrainerLevel(TRAINERS_COUNT, 0, 77), 77);
    BeginAdventure(ADVENTURE_MODE_QUANTUM);
}

TEST("Adventure progression: Classic restores exact grass Surf and clamped Old Rod ranges")
{
#ifdef FIRERED
    extern const struct WildPokemon sPowerPlant_FireRed_LandMons[];
    extern const struct WildPokemon sRoute12_FireRed_WaterMons[];
    extern const struct WildPokemon sRoute12_FireRed_FishingMons[];
    u8 min, max;
    BeginAdventure(ADVENTURE_MODE_CLASSIC);
    min = 29; max = 29;
    AdventureMode_WildRange(sPowerPlant_FireRed_LandMons, 0, &min, &max);
    EXPECT_EQ(min, 22); EXPECT_EQ(max, 22);
    min = 1; max = 2;
    AdventureMode_WildRange(sRoute12_FireRed_WaterMons, 0, &min, &max);
    EXPECT_EQ(min, 5); EXPECT_EQ(max, 10);
    min = 1; max = 1;
    AdventureMode_WildRange(sRoute12_FireRed_FishingMons, 0, &min, &max);
    EXPECT_EQ(min, 5); EXPECT_EQ(max, 5);
    BeginAdventure(ADVENTURE_MODE_QUANTUM);
    min = 1; max = 1;
    AdventureMode_WildRange(sRoute12_FireRed_FishingMons, 0, &min, &max);
    EXPECT_EQ(min, 1); EXPECT_EQ(max, 1);
#endif
}

TEST("Adventure progression: scripted levels are selected before species randomization")
{
    s8 group = gSaveBlock1Ptr->location.mapGroup, number = gSaveBlock1Ptr->location.mapNum;
    BeginAdventure(ADVENTURE_MODE_CLASSIC);
    gSaveBlock1Ptr->location.mapGroup = MAP_GROUP(MAP_ROUTE12);
    gSaveBlock1Ptr->location.mapNum = MAP_NUM(MAP_ROUTE12);
    EXPECT_EQ(AdventureMode_ScriptedLevel(SPECIES_SNORLAX,22),30);
    gSaveBlock1Ptr->location.mapGroup = MAP_GROUP(MAP_POWER_PLANT);
    gSaveBlock1Ptr->location.mapNum = MAP_NUM(MAP_POWER_PLANT);
    EXPECT_EQ(AdventureMode_ScriptedLevel(SPECIES_ZAPDOS,57),50);
    EXPECT_EQ(AdventureMode_ScriptedLevel(SPECIES_ELECTRODE,41),34);
    BeginAdventure(ADVENTURE_MODE_QUANTUM);
    EXPECT_EQ(AdventureMode_ScriptedLevel(SPECIES_ZAPDOS,57),57);
    gSaveBlock1Ptr->location.mapGroup = group; gSaveBlock1Ptr->location.mapNum = number;
}
