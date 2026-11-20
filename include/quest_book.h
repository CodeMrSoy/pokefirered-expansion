#ifndef GUARD_QUEST_BOOK_H
#define GUARD_QUEST_BOOK_H
#include "global.h"
#include "constants/quest_book.h"
struct QuantumQuestDefinition {
    const u8 *title;
    const u8 *description;
    const u8 *location;
    const u8 *const *objectives;
    u16 rewardItem;
    u8 rewardQuantity;
    u8 objectiveCount;
    bool8 optional;
    bool8 quantumOnly;
};
const struct QuantumQuestDefinition *QuestBook_GetDefinition(u16 id);
bool8 QuestBook_IsReady(void);
void QuestBook_NewGame(void);
void QuestBook_Load(void);
void QuestBook_Update(void);
void QuestBook_Tick(void);
u8 QuestBook_GetState(u16 id);
u8 QuestBook_GetObjective(u16 id);
u16 QuestBook_GetCompletedObjectives(u16 id);
bool8 QuestBook_IsVisible(u16 id);
bool8 QuestBook_Discover(u16 id);
bool8 QuestBook_Accept(u16 id);
bool8 QuestBook_Decline(u16 id);
bool8 QuestBook_ClaimReward(u16 id);
bool8 QuestBook_Track(u16 id);
u8 QuestBook_GetTracked(void);
void QuestBook_NotifyNpc(u16 id);
struct ScriptContext;
bool8 QuestBook_OfferFromScript(struct ScriptContext *ctx);
#endif
