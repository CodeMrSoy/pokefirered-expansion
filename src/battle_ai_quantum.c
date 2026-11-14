#include "global.h"
#include "battle.h"
#include "battle_ai_main.h"
#include "battle_ai_util.h"
#include "battle_ai_quantum.h"
#include "pokemon.h"
#include "constants/abilities.h"
#include "constants/battle_ai.h"
#include "constants/battle_move_effects.h"
#include "constants/moves.h"
#include "move.h"

enum QuantumAITier QuantumAI_GetTier(u32 battler)
{
    u64 flags = gAiThinkingStruct->aiFlags[GetThinkingBattler(battler)];
    u32 tier;

    // Highest tier wins if a debug battle accidentally selects several.
    for (tier = QUANTUM_AI_CHAMPION; tier > QUANTUM_AI_NONE; tier--)
    {
        if (flags & ((u64)1 << (27 + tier)))
            return tier;
    }
    return QUANTUM_AI_NONE;
}

bool32 QuantumAI_UsesFairKnowledge(void)
{
    return ((gAiThinkingStruct->aiFlags[B_POSITION_OPPONENT_LEFT]
           | gAiThinkingStruct->aiFlags[B_POSITION_OPPONENT_RIGHT]) & AI_FLAG_QUANTUM_TIERS) != 0;
}

static bool32 IsReliableKO(u32 battler, u32 target, u32 slot)
{
    u32 move = gBattleMons[battler].moves[slot];

    return !IsMoveUnusable(slot, move, gAiLogicData->moveLimitations[battler])
        && !IsBattleMoveStatus(move)
        && GetMoveEffect(move) != EFFECT_EXPLOSION
        && GetMoveEffect(move) != EFFECT_MISTY_EXPLOSION
        && gAiLogicData->moveAccuracy[battler][target][slot] >= 100
        && CanIndexMoveGuaranteeFaintTarget(battler, target, slot)
        && (AI_IsFaster(battler, target, move) || !CanTargetFaintAi(target, battler));
}

bool32 QuantumAI_HasReliableKO(u32 battler, u32 target)
{
    u32 slot;

    for (slot = 0; slot < MAX_MON_MOVES; slot++)
    {
        if (IsReliableKO(battler, target, slot))
            return TRUE;
    }
    return FALSE;
}

// Only damage simulations for revealed moves are considered. In doubles,
// both foes may attack the user; this is a conservative focus-fire estimate.
static u32 GetKnownIncomingDamage(u32 battler)
{
    u32 foe, slot, total = 0;

    for (foe = 0; foe < gBattlersCount; foe++)
    {
        u32 highest = 0;
        u16 *moves;

        if (!IsBattlerAlive(foe) || IsBattlerAlly(battler, foe))
            continue;
        moves = GetMovesArray(foe);
        for (slot = 0; slot < MAX_MON_MOVES; slot++)
        {
            u32 damage;
            if (moves[slot] == MOVE_NONE || IsBattleMoveStatus(moves[slot]))
                continue;
            damage = AI_GetDamage(foe, battler, slot, AI_DEFENDING, gAiLogicData);
            if (damage > highest)
                highest = damage;
        }
        total += highest;
    }
    return total;
}

static bool32 IsImmediateRecovery(enum BattleMoveEffects effect)
{
    return effect == EFFECT_RESTORE_HP || effect == EFFECT_ROOST || effect == EFFECT_MORNING_SUN;
}

s32 QuantumAI_ScoreMove(u32 battlerAtk, u32 battlerDef, u32 move, s32 score)
{
    enum QuantumAITier tier = QuantumAI_GetTier(battlerAtk);
    enum BattleMoveEffects effect = GetMoveEffect(move);
    u32 slot = gAiThinkingStruct->movesetIndex;
    u32 incoming, hp = gBattleMons[battlerAtk].hp;
    bool32 status = IsBattleMoveStatus(move);

    // Run once even if several tier markers were selected in the debug menu.
    if (gAiThinkingStruct->aiLogicId != 27 + tier
        || IsBattlerAlly(battlerAtk, battlerDef) || score < AI_BAD_SCORE_THRESHOLD)
        return score;

    if (!status && IsReliableKO(battlerAtk, battlerDef, slot))
        ADJUST_SCORE(8);

    // Don't spend a free winning turn boosting/healing. Leave doubles support
    // decisions to the existing partner-aware evaluator.
    if (!IsDoubleBattle() && status && QuantumAI_HasReliableKO(battlerAtk, battlerDef))
        ADJUST_SCORE(-8);

    if (tier < QUANTUM_AI_GYM_TRAINER)
        return score;

    incoming = GetKnownIncomingDamage(battlerAtk);
    if (status && IsStatRaisingEffect(effect))
    {
        // Boosting while being knocked out this turn achieves nothing.
        if (incoming >= hp)
            ADJUST_SCORE(-14);
        else if (tier >= QUANTUM_AI_GYM_LEADER && incoming * 2 >= hp)
            ADJUST_SCORE(-4);
        else if (tier >= QUANTUM_AI_GYM_LEADER && score >= AI_SCORE_DEFAULT)
            ADJUST_SCORE(1);
    }

    if (tier >= QUANTUM_AI_GYM_LEADER && status && IsImmediateRecovery(effect))
    {
        // Existing effect scoring handles weather, Heal Block and missing HP.
        // Add the tempo check: healing must outpace known incoming damage.
        if (incoming >= hp && !AI_IsFaster(battlerAtk, battlerDef, move))
            ADJUST_SCORE(-12);
        else if (incoming >= gBattleMons[battlerAtk].maxHP / 2)
            ADJUST_SCORE(-6);
        else if (gAiLogicData->hpPercents[battlerAtk] <= 50 && score >= AI_SCORE_DEFAULT)
            ADJUST_SCORE(2);
    }

    if (tier >= QUANTUM_AI_GYM_LEADER && !status && effect == EFFECT_RECOIL
        && gAiLogicData->abilities[battlerAtk] != ABILITY_ROCK_HEAD
        && gAiLogicData->abilities[battlerAtk] != ABILITY_MAGIC_GUARD)
    {
        u32 damage = AI_GetDamage(battlerAtk, battlerDef, slot, AI_ATTACKING, gAiLogicData);
        u32 recoil;
        if (damage > gBattleMons[battlerDef].hp)
            damage = gBattleMons[battlerDef].hp;
        recoil = damage * GetMoveRecoil(move) / 100;
        if (recoil >= hp && CountUsablePartyMons(battlerAtk) > 0)
            ADJUST_SCORE(-5);
    }

    // Rival and above exploit *revealed* disruption, without predicting the
    // player's selected action or reading unrevealed party members.
    if (tier >= QUANTUM_AI_RIVAL && status && IsStatRaisingEffect(effect)
        && (HasMove(battlerDef, MOVE_HAZE) || HasMove(battlerDef, MOVE_CLEAR_SMOG)))
        ADJUST_SCORE(-6);

    // High tiers recognize a short attacking race. This is bounded arithmetic
    // over cached damage, not a recursive battle simulator.
    if (tier >= QUANTUM_AI_ELITE_FOUR && !IsDoubleBattle() && !status)
    {
        u32 damage = AI_GetDamage(battlerAtk, battlerDef, slot, AI_ATTACKING, gAiLogicData);
        if (damage > 0 && damage * 2 >= gBattleMons[battlerDef].hp
            && incoming > 0 && incoming * 2 < hp
            && gAiLogicData->moveAccuracy[battlerAtk][battlerDef][slot] >= 100)
            ADJUST_SCORE(tier == QUANTUM_AI_CHAMPION ? 3 : 1);
    }

    return score;
}
