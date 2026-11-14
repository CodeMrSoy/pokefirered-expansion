#ifndef GUARD_BATTLE_AI_QUANTUM_H
#define GUARD_BATTLE_AI_QUANTUM_H

enum QuantumAITier
{
    QUANTUM_AI_NONE,
    QUANTUM_AI_REGULAR,
    QUANTUM_AI_GYM_TRAINER,
    QUANTUM_AI_GYM_LEADER,
    QUANTUM_AI_RIVAL,
    QUANTUM_AI_ELITE_FOUR,
    QUANTUM_AI_CHAMPION,
};

enum QuantumAITier QuantumAI_GetTier(u32 battler);
bool32 QuantumAI_UsesFairKnowledge(void);
bool32 QuantumAI_HasReliableKO(u32 battler, u32 target);
void QuantumAI_FinalizeSwitch(u32 battler);
s32 QuantumAI_ScoreMove(u32 battlerAtk, u32 battlerDef, u32 move, s32 score);

#endif
