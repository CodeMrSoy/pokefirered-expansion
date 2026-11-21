#include "global.h"
#include "quest_book.h"
#include "adventure_mode.h"
#include "event_data.h"
#include "item.h"
#include "quest_log.h"
#include "constants/flags.h"
#include "constants/vars.h"
#include "constants/items.h"
#include "constants/maps.h"
#include <stddef.h>

STATIC_ASSERT(sizeof(struct SaveBlock2) == 3968, QuestSaveBlock2Size);
STATIC_ASSERT(offsetof(struct SaveBlock2, questBookRecord) == 3803, QuestSaveOffset);
STATIC_ASSERT(sizeof(((struct SaveBlock2 *)0)->questBookRecord) == QUEST_SAVE_BYTES, QuestRecordSize);
STATIC_ASSERT(8 + QUEST_CAPACITY * 4 <= QUEST_SAVE_BYTES, QuestCapacityFits);

static const u8 *const sParcelObjectives[] = {COMPOUND_STRING("Collect Oak's Parcel at the Viridian Mart."), COMPOUND_STRING("Deliver the parcel to Professor Oak in Pallet Town.")};
static const u8 *const sBadgeObjectives[] = {COMPOUND_STRING("Win Brock's Boulder Badge in Pewter."), COMPOUND_STRING("Win Misty's Cascade Badge in Cerulean."), COMPOUND_STRING("Win Lt. Surge's Thunder Badge in Vermilion."), COMPOUND_STRING("Win Erika's Rainbow Badge in Celadon."), COMPOUND_STRING("Win Koga's Soul Badge in Fuchsia."), COMPOUND_STRING("Win Sabrina's Marsh Badge in Saffron."), COMPOUND_STRING("Win Blaine's Volcano Badge on Cinnabar."), COMPOUND_STRING("Win Giovanni's Earth Badge in Viridian.")};
static const u8 *const sSafariObjectives[] = {COMPOUND_STRING("Find HM03 Surf in the Safari Zone's Secret House."), COMPOUND_STRING("Recover the Warden's Gold Teeth in the Safari Zone."), COMPOUND_STRING("Return the teeth to the Warden in Fuchsia for HM04 Strength.")};
static const u8 *const sPassageObjectives[] = {COMPOUND_STRING("Speak with the traveler at the Safari Secret House for a Stellar Ticket."), COMPOUND_STRING("Use the Quantum boat service to visit Vidra."), COMPOUND_STRING("Speak with Koga in Havora so he returns to Fuchsia.")};
static const u8 *const sHarborObjectives[] = {COMPOUND_STRING("Complete Captain Eirik's Havora Gym challenge and earn his crest.")};
static const u8 *const sNotesObjectives[] = {COMPOUND_STRING("Visit Route 1 after accepting the aide's field assignment."), COMPOUND_STRING("Return to the same aide in Oak's Lab to report your field notes.")};
static const u8 *const sIndigoObjectives[] = {COMPOUND_STRING("Challenge the Elite Four and Champion at Indigo Plateau.")};
#define DEF(title_, desc_, loc_, obj_, item_, qty_, optional_, quantum_) {COMPOUND_STRING(title_), COMPOUND_STRING(desc_), COMPOUND_STRING(loc_), obj_, item_, qty_, ARRAY_COUNT(obj_), optional_, quantum_}
static const struct QuantumQuestDefinition sQuests[QUEST_DEFINITION_COUNT] = {
    [QUEST_OAKS_PARCEL] = DEF("Oak's Parcel", "The Viridian Mart has a parcel for Professor Oak. Help deliver it to begin your research journey.", "Viridian Mart / Oak's Lab", sParcelObjectives, ITEM_NONE, 0, FALSE, FALSE),
    [QUEST_KANTO_BADGES] = DEF("Kanto Badges", "Earn all eight Kanto badges. Each Gym victory brings you closer to the Pokemon League.", "Kanto Gyms", sBadgeObjectives, ITEM_NONE, 0, FALSE, FALSE),
    [QUEST_SAFARI_TOOLS] = DEF("Safari Expedition", "Explore the Safari Zone for Surf and the Warden's missing teeth. Return the teeth to their owner for Strength.", "Safari Zone / Fuchsia", sSafariObjectives, ITEM_NONE, 0, FALSE, FALSE),
    [QUEST_VIDRA_PASSAGE] = DEF("The Vidra Passage", "A traveler in the Safari Zone can help you reach Vidra. Follow Koga's trail to Havora.", "Safari Secret House / Havora", sPassageObjectives, ITEM_NONE, 0, FALSE, TRUE),
    [QUEST_HAVORA_TRIAL] = DEF("The Harbor Trial", "Captain Eirik's Gym tests your command of double battles. Earn the captain's recognition.", "Havora Gym", sHarborObjectives, ITEM_NONE, 0, FALSE, TRUE),
    [QUEST_FIELD_NOTES] = DEF("Field Notes", "An Oak aide offers a small field assignment. Visit Route 1, then return to report what you observed.", "Oak's Lab / Route 1", sNotesObjectives, ITEM_POKE_BALL, 3, TRUE, FALSE),
    [QUEST_INDIGO_CHALLENGE] = DEF("Indigo Challenge", "With all eight Kanto badges, face the Pokemon League. Quest Book adds no extra access requirements.", "Indigo Plateau", sIndigoObjectives, ITEM_NONE, 0, FALSE, FALSE),
};
#undef DEF

static u8 *Record(u16 id) { return &gSaveBlock2Ptr->questBookRecord[8 + id * 4]; }
const struct QuantumQuestDefinition *QuestBook_GetDefinition(u16 id)
{
    if (id >= QUEST_DEFINITION_COUNT || (sQuests[id].quantumOnly && !AdventureMode_IsQuantum())) return NULL;
    return &sQuests[id];
}
bool8 QuestBook_IsReady(void)
{
    const u8 *p = gSaveBlock2Ptr->questBookRecord;
    return p[0] == 'Q' && p[1] == 'S' && p[2] == 'T' && p[3] == '3' && p[4] == 1 && p[7] == 0xA5;
}
void QuestBook_NewGame(void)
{
    u8 *p = gSaveBlock2Ptr->questBookRecord;
    memset(p, 0, QUEST_SAVE_BYTES);
    memcpy(p, "QST3", 4); p[4] = 1; p[5] = QUEST_NONE; p[7] = 0xA5;
}
void QuestBook_Load(void)
{
    u32 i;
    if (QuestBook_IsReady()) return;
    // Older Quantum saves never used this padding. Unknown nonzero data is
    // deliberately preserved rather than guessed at or silently overwritten.
    for (i = 0; i < QUEST_SAVE_BYTES; i++) if (gSaveBlock2Ptr->questBookRecord[i]) return;
    QuestBook_NewGame();
    QuestBook_Update();
}
u8 QuestBook_GetState(u16 id)
{
    if (!QuestBook_IsReady() || !QuestBook_GetDefinition(id)) return QUEST_UNDISCOVERED;
    return Record(id)[0] <= QUEST_FAILED ? Record(id)[0] : QUEST_UNDISCOVERED;
}
u16 QuestBook_GetCompletedObjectives(u16 id)
{
    if (!QuestBook_IsReady() || !QuestBook_GetDefinition(id)) return 0;
    return Record(id)[2] | (Record(id)[3] << 8);
}
u8 QuestBook_GetObjective(u16 id)
{
    const struct QuantumQuestDefinition *q = QuestBook_GetDefinition(id);
    u8 i; u16 done = QuestBook_GetCompletedObjectives(id);
    if (!q) return 0;
    for (i = 0; i < q->objectiveCount; i++) if (!(done & (1 << i))) return i;
    return q->objectiveCount;
}
bool8 QuestBook_IsVisible(u16 id) { return QuestBook_GetDefinition(id) && QuestBook_GetState(id) != QUEST_UNDISCOVERED; }
bool8 QuestBook_Discover(u16 id)
{
    const struct QuantumQuestDefinition *q = QuestBook_GetDefinition(id);
    if (!q || !QuestBook_IsReady()) return FALSE;
    if (id == QUEST_FIELD_NOTES && !FlagGet(FLAG_SYS_POKEDEX_GET)) return FALSE;
    if (QuestBook_GetState(id) == QUEST_UNDISCOVERED) Record(id)[0] = q->optional ? QUEST_AVAILABLE : QUEST_ACTIVE;
    return TRUE;
}
bool8 QuestBook_Accept(u16 id)
{
    u8 state = QuestBook_GetState(id);
    if (!QuestBook_GetDefinition(id) || (state != QUEST_AVAILABLE && state != QUEST_DECLINED)) return FALSE;
    Record(id)[0] = QUEST_ACTIVE;
    QuestBook_Update();
    return TRUE;
}
bool8 QuestBook_Decline(u16 id)
{
    const struct QuantumQuestDefinition *q = QuestBook_GetDefinition(id);
    u8 state = QuestBook_GetState(id);
    if (!q || !q->optional || (state != QUEST_AVAILABLE && state != QUEST_DECLINED)) return FALSE;
    Record(id)[0] = QUEST_DECLINED;
    return TRUE;
}
static bool8 Condition(u16 id, u8 objective)
{
    switch (id)
    {
    case QUEST_OAKS_PARCEL:
        return FlagGet(FLAG_SYS_POKEDEX_GET) || (!objective && CheckBagHasItem(ITEM_OAKS_PARCEL, 1));
    case QUEST_KANTO_BADGES: return FlagGet(FLAG_BADGE01_GET + objective);
    case QUEST_SAFARI_TOOLS:
        if (!objective) return FlagGet(FLAG_GOT_HM03);
        if (objective == 1) return CheckBagHasItem(ITEM_GOLD_TEETH, 1) || FlagGet(FLAG_GOT_HM04);
        return FlagGet(FLAG_GOT_HM04);
    case QUEST_VIDRA_PASSAGE:
        if (!objective) return FlagGet(FLAG_RECEIVED_SAFARI_STELLAR_TICKET) || CheckBagHasItem(ITEM_STELLAR_TICKET, 1);
        if (objective == 1) return AdventureMode_IsVidraMap(gSaveBlock1Ptr->location.mapGroup, gSaveBlock1Ptr->location.mapNum) || FlagGet(FLAG_KOGA_RETURNED_FROM_HAVORA);
        return FlagGet(FLAG_KOGA_RETURNED_FROM_HAVORA);
    case QUEST_HAVORA_TRIAL: return (VarGet(VAR_HAVORA_GYM_PROGRESS) & 4) || (VarGet(VAR_VIDRA_CRESTS) & 1);
    case QUEST_FIELD_NOTES: return !objective && gSaveBlock1Ptr->location.mapGroup == MAP_GROUP(MAP_ROUTE1) && gSaveBlock1Ptr->location.mapNum == MAP_NUM(MAP_ROUTE1);
    case QUEST_INDIGO_CHALLENGE: return FlagGet(FLAG_SYS_GAME_CLEAR);
    }
    return FALSE;
}
void QuestBook_Update(void)
{
    u16 id;
    if (!QuestBook_IsReady() || QL_IS_PLAYBACK_STATE) return;
    if (FlagGet(FLAG_SYS_POKEMON_GET) || FlagGet(FLAG_SYS_POKEDEX_GET)) QuestBook_Discover(QUEST_OAKS_PARCEL);
    if (FlagGet(FLAG_SYS_POKEDEX_GET)) QuestBook_Discover(QUEST_KANTO_BADGES);
    if (FlagGet(FLAG_WORLD_MAP_FUCHSIA_CITY) || FlagGet(FLAG_GOT_HM03) || FlagGet(FLAG_GOT_HM04)) QuestBook_Discover(QUEST_SAFARI_TOOLS);
    if (FlagGet(FLAG_GOT_HM03) || FlagGet(FLAG_RECEIVED_SAFARI_STELLAR_TICKET)) QuestBook_Discover(QUEST_VIDRA_PASSAGE);
    if (FlagGet(FLAG_KOGA_RETURNED_FROM_HAVORA) || VarGet(VAR_HAVORA_GYM_PROGRESS)) QuestBook_Discover(QUEST_HAVORA_TRIAL);
    if (FlagGet(FLAG_BADGE08_GET)) QuestBook_Discover(QUEST_INDIGO_CHALLENGE);
    for (id = 0; id < QUEST_DEFINITION_COUNT; id++)
    {
        const struct QuantumQuestDefinition *q = QuestBook_GetDefinition(id);
        u8 i, objective;
        u16 done;
        if (!q || QuestBook_GetState(id) != QUEST_ACTIVE) continue;
        done = QuestBook_GetCompletedObjectives(id);
        for (i = 0; i < q->objectiveCount; i++) if (Condition(id, i)) done |= 1 << i;
        Record(id)[2] = done; Record(id)[3] = done >> 8;
        objective = QuestBook_GetObjective(id);
        Record(id)[1] = objective;
        if (objective == q->objectiveCount) Record(id)[0] = QUEST_COMPLETED;
    }
    if (gSaveBlock2Ptr->questBookRecord[5] != QUEST_NONE && QuestBook_GetState(gSaveBlock2Ptr->questBookRecord[5]) != QUEST_ACTIVE) gSaveBlock2Ptr->questBookRecord[5] = QUEST_NONE;
}
void QuestBook_Tick(void)
{
    static u8 tick;
    if (++tick >= 30) { tick = 0; QuestBook_Update(); }
}
void QuestBook_NotifyNpc(u16 id)
{
    if (id == QUEST_FIELD_NOTES && QuestBook_GetState(id) == QUEST_ACTIVE && (QuestBook_GetCompletedObjectives(id) & 1))
    { Record(id)[2] |= 2; QuestBook_Update(); }
}
bool8 QuestBook_ClaimReward(u16 id)
{
    const struct QuantumQuestDefinition *q = QuestBook_GetDefinition(id);
    if (!q || QuestBook_GetState(id) != QUEST_COMPLETED || QuestBook_GetObjective(id) != q->objectiveCount) return FALSE;
    if (q->rewardItem != ITEM_NONE && !AddBagItem(q->rewardItem, q->rewardQuantity)) return FALSE;
    Record(id)[0] = QUEST_CLAIMED;
    return TRUE;
}
bool8 QuestBook_Track(u16 id)
{
    if (id != QUEST_NONE && QuestBook_GetState(id) != QUEST_ACTIVE) return FALSE;
    if (!QuestBook_IsReady()) return FALSE;
    gSaveBlock2Ptr->questBookRecord[5] = id;
    return TRUE;
}
u8 QuestBook_GetTracked(void)
{
    u8 id;
    if (!QuestBook_IsReady()) return QUEST_NONE;
    id = gSaveBlock2Ptr->questBookRecord[5];
    return QuestBook_GetDefinition(id) && QuestBook_GetState(id) == QUEST_ACTIVE ? id : QUEST_NONE;
}
