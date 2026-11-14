#include "global.h"
#include "test/test.h"
#include "game_modes.h"
#include "randomizer.h"
#include "caps.h"
#include "event_data.h"
#include "battle.h"
#include "battle_main.h"
#include "malloc.h"
#include "constants/battle.h"
#include "constants/region_map_sections.h"
#include "constants/opponents.h"

static void ResetModes(void)
{
    gSaveBlock2Ptr->randomizerSeed = 0;
    gCachedRandomizerSeed = 0;
    gSaveBlock2Ptr->gameModesVersion = 0;
    GameModes_EnsureInitialized();
    GameModes_Apply();
}

TEST("Game modes: legacy defaults preserve normal and randomized saves")
{
    ResetModes();
    EXPECT(GameModes_Enabled(GAME_MODE_LEVEL_CAPS));
    EXPECT(!GameModes_Enabled(GAME_MODE_RANDOM | GAME_MODE_NUZLOCKE));
    gSaveBlock2Ptr->gameModesVersion = 0;
    gSaveBlock2Ptr->randomizerSeed = 12345;
    GameModes_Apply();
    EXPECT_EQ(gSaveBlock2Ptr->gameModes, GAME_MODE_RANDOM | GAME_MODE_LEVEL_CAPS);
    EXPECT(RandomizerFeatureEnabled(RANDOMIZE_TRAINER_MON));
    EXPECT(RandomizerFeatureEnabled(RANDOMIZE_ABILITIES));
    EXPECT(RandomizerFeatureEnabled(RANDOMIZE_LEARNSET));
    ResetModes();
}

TEST("Game modes: each random category is independent and seed stays stable")
{
    u32 i;
    const u8 bits[] = {GAME_MODE_POKEMON,GAME_MODE_MOVES,GAME_MODE_ABILITIES,GAME_MODE_ITEMS};
    ResetModes();
    for (i=0;i<ARRAY_COUNT(bits);i++) {
        GameModes_Set(bits[i],TRUE);
        EXPECT_EQ(RandomizerFeatureEnabled(RANDOMIZE_WILD_MON), i==0);
        EXPECT_EQ(RandomizerFeatureEnabled(RANDOMIZE_TRAINER_MON), i==0);
        EXPECT_EQ(RandomizerFeatureEnabled(RANDOMIZE_STARTER_AND_GIFT_MON), i==0);
        EXPECT_EQ(RandomizerFeatureEnabled(RANDOMIZE_FIXED_MON), i==0);
        EXPECT_EQ(RandomizerFeatureEnabled(RANDOMIZE_EGG_MON), i==0);
        EXPECT_EQ(RandomizerFeatureEnabled(RANDOMIZE_LEARNSET), i==1);
        EXPECT_EQ(RandomizerFeatureEnabled(RANDOMIZE_ABILITIES), i==2);
        EXPECT_EQ(RandomizerFeatureEnabled(RANDOMIZE_FIELD_ITEMS), i==3);
        gSaveBlock2Ptr->randomizerSeed=12345;
        GameModes_Set(bits[i],FALSE);
        EXPECT_EQ(gSaveBlock2Ptr->randomizerSeed,12345);
        EXPECT(!gRandomizerEnabled);
        GameModes_Set(bits[i],TRUE);
        EXPECT_EQ(GetRandomizerSeed(),12345);
        GameModes_Set(bits[i],FALSE);
    }
    ResetModes();
}

TEST("Game modes: caps switch affects level limit and experience scaling")
{
    ResetModes(); FlagClear(FLAG_BADGE01_GET); FlagClear(FLAG_SYS_GAME_CLEAR);
    EXPECT_EQ(GetCurrentLevelCap(),14);
    EXPECT_EQ(GetSoftLevelCapExpValue(14,100),0);
    GameModes_Set(GAME_MODE_LEVEL_CAPS,FALSE);
    EXPECT_EQ(GetCurrentLevelCap(),MAX_LEVEL);
    EXPECT_EQ(GetSoftLevelCapExpValue(14,100),100);
    EXPECT_EQ(GetSoftLevelCapExpValue(5,100),100);
    GameModes_Set(GAME_MODE_LEVEL_CAPS,TRUE);
    EXPECT_EQ(GetCurrentLevelCap(),14);
    ResetModes();
}

TEST("Game modes: Nuzlocke shares one encounter across land surf and fishing")
{
    ResetModes(); GameModes_Set(GAME_MODE_NUZLOCKE,TRUE);
    Nuzlocke_BeginEncounter(MAPSEC_ROUTE_1,0);
    EXPECT(Nuzlocke_CanCatch());
    EXPECT(Nuzlocke_CanCatch()); // Failed balls do not end the first encounter.
    Nuzlocke_BeginEncounter(MAPSEC_ROUTE_1,0); // Same route, different method.
    EXPECT(!Nuzlocke_CanCatch()); // Also covers a previous escape or KO.
    Nuzlocke_BeginEncounter(MAPSEC_ROUTE_2,0);
    EXPECT(Nuzlocke_CanCatch());
    Nuzlocke_RecordCatch();
    EXPECT(!Nuzlocke_CanCatch());
    Nuzlocke_BeginEncounter(MAPSEC_ROUTE_2,0);
    EXPECT(!Nuzlocke_CanCatch());
    ResetModes();
}

TEST("Game modes: toggles preserve encounter history and New Game clears it")
{
    ResetModes(); GameModes_Set(GAME_MODE_NUZLOCKE,TRUE);
    Nuzlocke_BeginEncounter(MAPSEC_ROUTE_1,0);
    GameModes_Set(GAME_MODE_NUZLOCKE,FALSE);
    EXPECT(Nuzlocke_CanCatch());
    GameModes_Set(GAME_MODE_NUZLOCKE,TRUE);
    Nuzlocke_BeginEncounter(MAPSEC_ROUTE_1,0);
    EXPECT(!Nuzlocke_CanCatch());
    GameModes_NewGame();
    EXPECT(GameModes_Enabled(GAME_MODE_NUZLOCKE));
    Nuzlocke_BeginEncounter(MAPSEC_ROUTE_1,0);
    EXPECT(Nuzlocke_CanCatch());
    ResetModes();
}

TEST("Game modes: tutorials trainers ghosts and invalid areas cannot consume a route")
{
    u32 i;
    const u32 flags[] = {BATTLE_TYPE_TRAINER,BATTLE_TYPE_LINK,BATTLE_TYPE_RECORDED,
        BATTLE_TYPE_POKEDUDE,BATTLE_TYPE_OLD_MAN_TUTORIAL,BATTLE_TYPE_GHOST};
    for(i=0;i<ARRAY_COUNT(flags);i++) {
        ResetModes(); GameModes_Set(GAME_MODE_NUZLOCKE,TRUE);
        Nuzlocke_BeginEncounter(MAPSEC_ROUTE_1,flags[i]);
        Nuzlocke_BeginEncounter(MAPSEC_ROUTE_1,0);
        EXPECT(Nuzlocke_CanCatch());
    }
    Nuzlocke_BeginEncounter(MAPSEC_NONE,0); EXPECT(!Nuzlocke_CanCatch());
    Nuzlocke_BeginEncounter(0xffff,0); EXPECT(!Nuzlocke_CanCatch());
    ResetModes();
}

TEST("Game modes: all Havora weather teams keep species custom moves and abilities")
{
    u32 id,i,j;
    ResetModes(); RandomizerSetEnabled(TRUE);
    gBattleStruct=AllocZeroed(sizeof(*gBattleStruct));
    for(id=TRAINER_HAVORA_DOCK_CREW;id<=TRAINER_HAVORA_LOCKKEEPER;id++) {
        const struct Trainer *trainer=GetTrainerStructFromId(id);
        CreateNPCTrainerPartyFromTrainer(gEnemyParty,trainer,TRUE,BATTLE_TYPE_TRAINER|BATTLE_TYPE_DOUBLE,id);
        for(i=0;i<trainer->partySize;i++) {
            EXPECT_EQ(GetMonData(&gEnemyParty[i],MON_DATA_SPECIES),trainer->party[i].species);
            EXPECT(GetMonData(&gEnemyParty[i],MON_DATA_CANT_RANDOMIZE_ABILITY));
            for(j=0;j<4;j++) EXPECT_EQ(GetMonData(&gEnemyParty[i],MON_DATA_MOVE1+j),trainer->party[i].moves[j]);
            EXPECT_EQ(GetMonAbility(&gEnemyParty[i]),trainer->party[i].ability);
        }
    }
    FREE_AND_SET_NULL(gBattleStruct); ResetModes();
}

#include "item_use.h"
#include "battle_script_commands.h"
#include "battle_scripts.h"
#include "constants/items.h"

TEST("Game modes: Nuzlocke blocks bag shortcuts and direct Safari ball commands")
{
    u32 flags;
    static const u8 handleBall[] = {0xef};
    PARAMETRIZE { flags=0; }
    PARAMETRIZE { flags=BATTLE_TYPE_SAFARI; }
    ResetModes(); GameModes_Set(GAME_MODE_NUZLOCKE,TRUE);
    gBattleTypeFlags=flags;
    gBattlersCount=2;
    gBattlerPositions[0]=B_POSITION_PLAYER_LEFT;
    gBattlerPositions[1]=B_POSITION_OPPONENT_LEFT;
    gBattleMons[1].hp=10;
    gAbsentBattlerFlags=0;
    gStatuses3[1]=0;
    gBattlerAttacker=0;
    gBattleControllerExecFlags=0;
    Nuzlocke_BeginEncounter(MAPSEC_ROUTE_1,flags);
    EXPECT(CanThrowBall());
    Nuzlocke_BeginEncounter(MAPSEC_ROUTE_1,flags);
    EXPECT(!CanThrowBall());
    gBattlescriptCurrInstr=handleBall;
    gBattleScriptingCommandsTable[0xef]();
    EXPECT_EQ(gBattlescriptCurrInstr,BattleScript_NuzlockeBallBlock);
    Nuzlocke_BeginEncounter(MAPSEC_ROUTE_2,flags);
    EXPECT(CanThrowBall());
    ResetModes();
}

TEST("Game modes: trainer species and move switches produce matching level-up moves")
{
    u32 mode,i,j;
    const struct Trainer *trainer=GetTrainerStructFromId(TRAINER_CAMPER_LIAM);
    PARAMETRIZE { mode=GAME_MODE_POKEMON; }
    PARAMETRIZE { mode=GAME_MODE_MOVES; }
    PARAMETRIZE { mode=GAME_MODE_ABILITIES; }
    ResetModes();
    gSaveBlock2Ptr->randomizerSeed=12345;
    GameModes_Set(mode,TRUE);
    gBattleStruct=AllocZeroed(sizeof(*gBattleStruct));
    CreateNPCTrainerPartyFromTrainer(gEnemyParty,trainer,TRUE,BATTLE_TYPE_TRAINER,TRAINER_CAMPER_LIAM);
    for(i=0;i<trainer->partySize;i++) {
        u16 species=GetMonData(&gEnemyParty[i],MON_DATA_SPECIES);
        struct Pokemon reference;
        if(mode==GAME_MODE_POKEMON)
            EXPECT_EQ(species,RandomizeTrainerMon(TRAINER_CAMPER_LIAM,i,trainer->partySize,trainer->party[i].species));
        else
            EXPECT_EQ(species,trainer->party[i].species);
        CreateMon(&reference,species,trainer->party[i].lvl,0,TRUE,0,OT_ID_PRESET,0);
        for(j=0;j<4;j++)
            EXPECT_EQ(GetMonData(&gEnemyParty[i],MON_DATA_MOVE1+j),mode==GAME_MODE_ABILITIES
                ? trainer->party[i].moves[j] : GetMonData(&reference,MON_DATA_MOVE1+j));
    }
    FREE_AND_SET_NULL(gBattleStruct);ResetModes();
}
