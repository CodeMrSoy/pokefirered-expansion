#include "global.h"
#include "test/battle.h"
#include "battle_ai_quantum.h"
#include "battle_ai_util.h"

AI_SINGLE_BATTLE_TEST("Quantum AI: all six tiers take an accurate KO over setup")
{
    u64 flags;
    PARAMETRIZE { flags = AI_FLAG_QUANTUM_REGULAR; }
    PARAMETRIZE { flags = AI_FLAG_QUANTUM_GYM_TRAINER; }
    PARAMETRIZE { flags = AI_FLAG_QUANTUM_GYM_LEADER; }
    PARAMETRIZE { flags = AI_FLAG_QUANTUM_RIVAL; }
    PARAMETRIZE { flags = AI_FLAG_QUANTUM_ELITE_FOUR; }
    PARAMETRIZE { flags = AI_FLAG_QUANTUM_CHAMPION; }

    GIVEN {
        AI_FLAGS(flags);
        PLAYER(SPECIES_WOBBUFFET) { HP(1); Speed(10); }
        PLAYER(SPECIES_WOBBUFFET) { Speed(10); }
        OPPONENT(SPECIES_SCIZOR) { Speed(100); Moves(MOVE_SWORDS_DANCE, MOVE_SLAM, MOVE_STRENGTH); }
    } WHEN {
        TURN { EXPECT_MOVE(opponent, MOVE_STRENGTH); SEND_OUT(player, 1); }
    } THEN {
        EXPECT_NE(QuantumAI_GetTier(B_POSITION_OPPONENT_LEFT), QUANTUM_AI_NONE);
        EXPECT_EQ(gAiThinkingStruct->aiFlags[B_POSITION_OPPONENT_LEFT], flags);
    }
}

AI_SINGLE_BATTLE_TEST("Quantum AI: reject setup when a revealed attack will KO this turn")
{
    GIVEN {
        AI_FLAGS(AI_FLAG_QUANTUM_GYM_TRAINER);
        PLAYER(SPECIES_WOBBUFFET) { Level(50); MaxHP(1000); HP(1000); Speed(100); Moves(MOVE_NIGHT_SHADE); }
        OPPONENT(SPECIES_SCIZOR) { MaxHP(150); HP(150); Speed(10); Moves(MOVE_SWORDS_DANCE, MOVE_BULLET_PUNCH); }
    } WHEN {
        TURN { MOVE(player, MOVE_NIGHT_SHADE); }
        TURN { MOVE(player, MOVE_NIGHT_SHADE); }
        TURN { MOVE(player, MOVE_NIGHT_SHADE); EXPECT_MOVE(opponent, MOVE_BULLET_PUNCH); }
    }
}

AI_SINGLE_BATTLE_TEST("Quantum AI: reject recovery that a slower user cannot execute before a known KO")
{
    GIVEN {
        AI_FLAGS(AI_FLAG_QUANTUM_GYM_LEADER);
        PLAYER(SPECIES_WOBBUFFET) { Level(100); MaxHP(1000); HP(1000); Speed(100); Moves(MOVE_NIGHT_SHADE); }
        OPPONENT(SPECIES_SCIZOR) { MaxHP(150); HP(150); Speed(10); Moves(MOVE_RECOVER, MOVE_BULLET_PUNCH); }
    } WHEN {
        TURN { MOVE(player, MOVE_NIGHT_SHADE); }
        TURN { MOVE(player, MOVE_NIGHT_SHADE); EXPECT_MOVE(opponent, MOVE_BULLET_PUNCH); }
    }
}

AI_SINGLE_BATTLE_TEST("Quantum AI: use priority to secure a KO against a faster foe")
{
    GIVEN {
        AI_FLAGS(AI_FLAG_QUANTUM_CHAMPION);
        PLAYER(SPECIES_WOBBUFFET) { HP(1); Speed(100); }
        PLAYER(SPECIES_WOBBUFFET) { Speed(100); }
        OPPONENT(SPECIES_SCIZOR) { Speed(10); Moves(MOVE_SWORDS_DANCE, MOVE_QUICK_ATTACK, MOVE_STRENGTH); }
    } WHEN {
        TURN { EXPECT_MOVE(opponent, MOVE_QUICK_ATTACK); SEND_OUT(player, 1); }
    }
}

AI_SINGLE_BATTLE_TEST("Quantum AI: unrevealed player moves and items stay hidden and live moves are restored")
{
    u16 hiddenMove, hiddenItem;
    PARAMETRIZE { hiddenMove = MOVE_FLAMETHROWER; hiddenItem = ITEM_CHOICE_SPECS; }
    PARAMETRIZE { hiddenMove = MOVE_SURF; hiddenItem = ITEM_LIFE_ORB; }

    GIVEN {
        AI_FLAGS(AI_FLAG_QUANTUM_CHAMPION);
        PLAYER(SPECIES_ALAKAZAM) { Moves(MOVE_SPLASH, hiddenMove); Item(hiddenItem); Speed(100); }
        OPPONENT(SPECIES_SCIZOR) { Moves(MOVE_TACKLE); Speed(10); }
    } WHEN {
        TURN { MOVE(player, MOVE_SPLASH); EXPECT_MOVE(opponent, MOVE_TACKLE); }
    } THEN {
        EXPECT_EQ(gAiLogicData->items[B_POSITION_PLAYER_LEFT], ITEM_NONE);
        EXPECT_EQ(gAiLogicData->holdEffects[B_POSITION_PLAYER_LEFT], HOLD_EFFECT_NONE);
        EXPECT_EQ(gAiLogicData->simulatedDmg[B_POSITION_PLAYER_LEFT][B_POSITION_OPPONENT_LEFT][1].maximum, 0);
        EXPECT_EQ(gBattleMons[B_POSITION_PLAYER_LEFT].moves[1], hiddenMove);
        EXPECT_EQ(gBattleMons[B_POSITION_PLAYER_LEFT].item, hiddenItem);
        EXPECT_EQ(GetMovesArray(B_POSITION_PLAYER_LEFT)[1], MOVE_NONE);
    }
}

AI_SINGLE_BATTLE_TEST("Quantum AI: an immune target is rejected by every tier")
{
    u64 flags;
    PARAMETRIZE { flags = AI_FLAG_QUANTUM_REGULAR; }
    PARAMETRIZE { flags = AI_FLAG_QUANTUM_GYM_TRAINER; }
    PARAMETRIZE { flags = AI_FLAG_QUANTUM_GYM_LEADER; }
    PARAMETRIZE { flags = AI_FLAG_QUANTUM_RIVAL; }
    PARAMETRIZE { flags = AI_FLAG_QUANTUM_ELITE_FOUR; }
    PARAMETRIZE { flags = AI_FLAG_QUANTUM_CHAMPION; }

    GIVEN {
        AI_FLAGS(flags);
        PLAYER(SPECIES_GENGAR);
        OPPONENT(SPECIES_ALAKAZAM) { Moves(MOVE_STRENGTH, MOVE_PSYCHIC); }
    } WHEN {
        TURN { EXPECT_MOVE(opponent, MOVE_PSYCHIC); }
    }
}

AI_SINGLE_BATTLE_TEST("Quantum AI: unusable Choice-locked moves retain a zero score")
{
    GIVEN {
        AI_FLAGS(AI_FLAG_QUANTUM_REGULAR);
        PLAYER(SPECIES_BLISSEY) { Moves(MOVE_SPLASH); }
        OPPONENT(SPECIES_WOBBUFFET) { Moves(MOVE_WATER_GUN, MOVE_HYDRO_PUMP); Item(ITEM_CHOICE_SPECS); }
    } WHEN {
        TURN { MOVE(player, MOVE_SPLASH); }
        TURN { MOVE(player, MOVE_SPLASH); }
    } THEN {
        u32 chosen = gAiBattleData->chosenMoveIndex[B_POSITION_OPPONENT_LEFT];
        EXPECT_EQ(gAiBattleData->finalScore[B_POSITION_OPPONENT_LEFT][B_POSITION_PLAYER_LEFT][chosen ^ 1], 0);
    }
}

AI_SINGLE_BATTLE_TEST("Quantum AI: do not voluntarily switch a one-HP Charizard into Stealth Rock")
{
    GIVEN {
        AI_FLAGS(AI_FLAG_QUANTUM_GYM_LEADER);
        PLAYER(SPECIES_WOBBUFFET) { Moves(MOVE_SPLASH); }
        OPPONENT(SPECIES_WOBBUFFET) { Moves(MOVE_TACKLE); }
        OPPONENT(SPECIES_CHARIZARD) { HP(1); Moves(MOVE_FLAMETHROWER); }
    } WHEN {
        TURN { MOVE(player, MOVE_SPLASH); }
    } THEN {
        gSideStatuses[B_SIDE_OPPONENT] |= SIDE_STATUS_STEALTH_ROCK;
        gBattleStruct->AI_monToSwitchIntoId[B_POSITION_OPPONENT_LEFT] = 1;
        gAiLogicData->shouldSwitch |= 1u << B_POSITION_OPPONENT_LEFT;
        QuantumAI_FinalizeSwitch(B_POSITION_OPPONENT_LEFT);
        EXPECT_EQ(gAiLogicData->shouldSwitch & (1u << B_POSITION_OPPONENT_LEFT), 0);
    }
}

AI_SINGLE_BATTLE_TEST("Quantum AI: Heavy-Duty Boots make a one-HP hazard entry possible")
{
    GIVEN {
        AI_FLAGS(AI_FLAG_QUANTUM_GYM_LEADER);
        PLAYER(SPECIES_WOBBUFFET) { Moves(MOVE_SPLASH); }
        OPPONENT(SPECIES_WOBBUFFET) { Moves(MOVE_TACKLE); }
        OPPONENT(SPECIES_CHARIZARD) { HP(1); Item(ITEM_HEAVY_DUTY_BOOTS); Moves(MOVE_FLAMETHROWER); }
    } WHEN {
        TURN { MOVE(player, MOVE_SPLASH); }
    } THEN {
        gSideStatuses[B_SIDE_OPPONENT] |= SIDE_STATUS_STEALTH_ROCK;
        gBattleStruct->AI_monToSwitchIntoId[B_POSITION_OPPONENT_LEFT] = 1;
        gAiLogicData->shouldSwitch |= 1u << B_POSITION_OPPONENT_LEFT;
        QuantumAI_FinalizeSwitch(B_POSITION_OPPONENT_LEFT);
        EXPECT_NE(gAiLogicData->shouldSwitch & (1u << B_POSITION_OPPONENT_LEFT), 0);
    }
}

AI_DOUBLE_BATTLE_TEST("Quantum AI: gym leader doubles retain partner support and restore both human movesets")
{
    GIVEN {
        AI_FLAGS(AI_FLAG_QUANTUM_GYM_LEADER);
        PLAYER(SPECIES_WOBBUFFET) { Moves(MOVE_SPLASH, MOVE_FLAMETHROWER); }
        PLAYER(SPECIES_WOBBUFFET) { Moves(MOVE_SPLASH, MOVE_SURF); }
        OPPONENT(SPECIES_WOBBUFFET) { Moves(MOVE_HELPING_HAND, MOVE_SCRATCH); }
        OPPONENT(SPECIES_WOBBUFFET) { Moves(MOVE_SPLASH); }
    } WHEN {
        TURN {
            MOVE(playerLeft, MOVE_SPLASH);
            MOVE(playerRight, MOVE_SPLASH);
            NOT_EXPECT_MOVE(opponentLeft, MOVE_HELPING_HAND);
        }
    } THEN {
        EXPECT_EQ(gBattleMons[B_POSITION_PLAYER_LEFT].moves[1], MOVE_FLAMETHROWER);
        EXPECT_EQ(gBattleMons[B_POSITION_PLAYER_RIGHT].moves[1], MOVE_SURF);
        EXPECT_EQ(gAiLogicData->simulatedDmg[B_POSITION_PLAYER_LEFT][B_POSITION_OPPONENT_LEFT][1].maximum, 0);
        EXPECT_EQ(gAiLogicData->simulatedDmg[B_POSITION_PLAYER_RIGHT][B_POSITION_OPPONENT_RIGHT][1].maximum, 0);
    }
}

AI_SINGLE_BATTLE_TEST("Quantum AI: voluntary switch cooldown still allows escaping Perish Song")
{
    GIVEN {
        AI_FLAGS(AI_FLAG_QUANTUM_RIVAL);
        PLAYER(SPECIES_WOBBUFFET) { Moves(MOVE_SPLASH); Ability(ABILITY_TELEPATHY); }
        OPPONENT(SPECIES_WOBBUFFET) { Moves(MOVE_TACKLE); }
        OPPONENT(SPECIES_CHARIZARD) { Moves(MOVE_FLAMETHROWER); }
    } WHEN {
        TURN { MOVE(player, MOVE_SPLASH); }
    } THEN {
        gAiBattleData->quantumLastSwitchTurn[B_POSITION_OPPONENT_LEFT] = gBattleResults.battleTurnCounter + 1;
        gBattleStruct->AI_monToSwitchIntoId[B_POSITION_OPPONENT_LEFT] = 1;
        gAiLogicData->shouldSwitch |= 1u << B_POSITION_OPPONENT_LEFT;
        QuantumAI_FinalizeSwitch(B_POSITION_OPPONENT_LEFT);
        EXPECT_EQ(gAiLogicData->shouldSwitch & (1u << B_POSITION_OPPONENT_LEFT), 0);
        gStatuses3[B_POSITION_OPPONENT_LEFT] |= STATUS3_PERISH_SONG;
        gDisableStructs[B_POSITION_OPPONENT_LEFT].perishSongTimer = 0;
        gBattleStruct->AI_monToSwitchIntoId[B_POSITION_OPPONENT_LEFT] = 1;
        gAiLogicData->shouldSwitch |= 1u << B_POSITION_OPPONENT_LEFT;
        QuantumAI_FinalizeSwitch(B_POSITION_OPPONENT_LEFT);
        EXPECT_NE(gAiLogicData->shouldSwitch & (1u << B_POSITION_OPPONENT_LEFT), 0);
    }
}
