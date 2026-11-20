#include "global.h"
#include "event_data.h"
#include "event_object_movement.h"
#include "field_player_avatar.h"
#include "living_world_bridge.h"
#include "quest_log.h"
#include "script.h"
#include "text.h"
#include "constants/characters.h"
#include "constants/event_objects.h"
#include "constants/flags.h"
#include "constants/living_world.h"
#include "constants/maps.h"
#include "constants/species.h"
#include "constants/vars.h"

#define LIVING_WORLD_REQUEST_V1 0x3157514C // Bytes "LQW1"
#define LIVING_WORLD_TIMEOUT_FRAMES 30
#define LIVING_WORLD_DEFERRED_FRAMES 600
#define LIVING_WORLD_REPLY_PENDING 255
#define LIVING_WORLD_LINE_LENGTH 28
#define LIVING_WORLD_TEXT_CAPACITY (LIVING_WORLD_LINE_LENGTH * 4 + 3)

struct LivingWorldMailbox
{
    u32 request;
    u32 sequence;
    u16 npc;
    u16 visibleSpecies;
    u32 responseSequence;
    u8 length;
    u8 text[LIVING_WORLD_TEXT_CAPACITY];
};

STATIC_ASSERT(offsetof(struct LivingWorldMailbox, responseSequence) == 12, LivingWorldReplyOffset);
STATIC_ASSERT(sizeof(struct LivingWorldMailbox) == 132, LivingWorldMailboxSize);

// The reference host finds this symbol in the ELF from the same build.
EWRAM_DATA volatile struct LivingWorldMailbox gLivingWorldMailbox = {0};
EWRAM_DATA u8 gLivingWorldDialogue[LIVING_WORLD_TEXT_CAPACITY + 1] = {0};
static EWRAM_DATA u16 sFramesRemaining = 0;
static EWRAM_DATA bool8 sDeferred = FALSE;

struct LivingWorldFieldHint
{
    u32 magic;
    u16 frame;
    u16 species;
    u8 area;
    u8 story;
    u8 npc;
    u8 distance;
};

STATIC_ASSERT(sizeof(struct LivingWorldFieldHint) == 12, LivingWorldFieldHintSize);
EWRAM_DATA volatile struct LivingWorldFieldHint gLivingWorldFieldHint = {0};

static u16 VisibleSpecies(void)
{
    struct ObjectEvent *follower = GetFollowerObject();
    return follower != NULL && !follower->invisible && !follower->offScreen
         ? OW_SPECIES(follower) : SPECIES_NONE;
}

static void ConsiderNearby(struct LivingWorldFieldHint *hint, u8 localId, u8 npc)
{
    const struct ObjectEvent *player = &gObjectEvents[gPlayerAvatar.objectEventId];
    u8 object = GetObjectEventIdByLocalIdAndMap(localId, gSaveBlock1Ptr->location.mapNum,
                                              gSaveBlock1Ptr->location.mapGroup);
    if (object >= OBJECT_EVENTS_COUNT || !player->active)
        return;
    const struct ObjectEvent *resident = &gObjectEvents[object];
    if (resident->invisible || resident->offScreen)
        return;
    s32 dx = player->currentCoords.x - resident->currentCoords.x;
    s32 dy = player->currentCoords.y - resident->currentCoords.y;
    s32 distance = abs(dx) + abs(dy);
    if (distance < hint->distance)
    {
        hint->npc = npc;
        hint->distance = distance;
    }
}

void LivingWorld_UpdateFieldHint(void)
{
    struct LivingWorldFieldHint hint = {
        .magic = 0x3150514C, // Bytes "LQP1"
        .frame = gLivingWorldFieldHint.frame + 1,
        .distance = 8,
    };
    if (FlagGet(FLAG_SYS_POKEDEX_GET) && gQuestLogState != QL_STATE_PLAYBACK)
    {
        bool8 idle = !ScriptContext_IsEnabled();
        switch ((gSaveBlock1Ptr->location.mapGroup << 8) | gSaveBlock1Ptr->location.mapNum)
        {
        case MAP_PALLET_TOWN:
            hint.area = 1;
            hint.story = VarGet(VAR_MAP_SCENE_PALLET_TOWN_SIGN_LADY);
            if (idle)
            {
                ConsiderNearby(&hint, 2, LIVING_WORLD_PC_RESIDENT);
                if (hint.story == 2)
                    ConsiderNearby(&hint, 1, LIVING_WORLD_SIGN_GUIDE);
            }
            break;
        case MAP_PALLET_TOWN_RIVALS_HOUSE:
            hint.area = 2;
            hint.story = VarGet(VAR_MAP_SCENE_PALLET_TOWN_RIVALS_HOUSE) | (FlagGet(FLAG_SYS_GAME_CLEAR) << 7);
            if (idle && (hint.story == 2
                     || (hint.story == 0 && VarGet(VAR_MAP_SCENE_PALLET_TOWN_PROFESSOR_OAKS_LAB) >= 1)))
                ConsiderNearby(&hint, 1, LIVING_WORLD_DAISY);
            break;
        case MAP_PALLET_TOWN_PROFESSOR_OAKS_LAB:
            hint.area = 3;
            hint.story = VarGet(VAR_MAP_SCENE_PALLET_TOWN_PROFESSOR_OAKS_LAB)
                       | (FlagGet(FLAG_OAK_SAW_DEX_COMPLETION) << 6)
                       | ((VarGet(VAR_MAP_SCENE_CERULEAN_CITY_RIVAL) == 1) << 7);
            if (idle && (hint.story & 0x3F) >= 6)
                ConsiderNearby(&hint, 4, LIVING_WORLD_OAK);
            break;
        }
        if (hint.area)
        {
            hint.species = VisibleSpecies();
            if (!idle)
                hint.distance = 255;
        }
    }
    gLivingWorldFieldHint = hint;
}

static bool8 EncodeCharacter(u8 ascii, u8 *encoded)
{
    if (ascii >= 'A' && ascii <= 'Z')
        *encoded = CHAR_A + ascii - 'A';
    else if (ascii >= 'a' && ascii <= 'z')
        *encoded = CHAR_a + ascii - 'a';
    else if (ascii >= '0' && ascii <= '9')
        *encoded = CHAR_0 + ascii - '0';
    else
    {
        switch (ascii)
        {
        case ' ': *encoded = CHAR_SPACE; break;
        case '!': *encoded = CHAR_EXCL_MARK; break;
        case '?': *encoded = CHAR_QUESTION_MARK; break;
        case '.': *encoded = CHAR_PERIOD; break;
        case ',': *encoded = CHAR_COMMA; break;
        case '-': *encoded = CHAR_HYPHEN; break;
        case ':': *encoded = CHAR_COLON; break;
        case '\'': *encoded = CHAR_SGL_QUOTE_RIGHT; break;
        default: return FALSE;
        }
    }
    return TRUE;
}

static bool8 ReceiveDialogue(void)
{
    u8 length = gLivingWorldMailbox.length;
    u8 lineStart = 0;
    u8 page = 0;
    bool8 secondLine = FALSE;

    if (length == 0 || length > LIVING_WORLD_TEXT_CAPACITY)
        return FALSE;

    for (u8 i = 0; i < length; i++)
    {
        u8 ascii = gLivingWorldMailbox.text[i];

        if (ascii == '\n' || ascii == '\f')
        {
            if (i == lineStart || i + 1 == length
             || (ascii == '\n' && secondLine) || (ascii == '\f' && page != 0))
                return FALSE;
            gLivingWorldDialogue[i] = EOS;
            if (GetStringWidth(FONT_NORMAL, gLivingWorldDialogue + lineStart, -1) > 198)
                return FALSE;
            gLivingWorldDialogue[i] = ascii == '\n' ? CHAR_NEWLINE : CHAR_PROMPT_CLEAR;
            secondLine = ascii == '\n';
            if (ascii == '\f')
                page++;
            lineStart = i + 1;
        }
        else if (i - lineStart >= LIVING_WORLD_LINE_LENGTH
              || !EncodeCharacter(ascii, &gLivingWorldDialogue[i]))
        {
            return FALSE;
        }
    }
    gLivingWorldDialogue[length] = EOS;
    return GetStringWidth(FONT_NORMAL, gLivingWorldDialogue + lineStart, -1) <= 198;
}

static void BeginConversation(u8 npc)
{
    u32 sequence = gLivingWorldMailbox.sequence + 1;

    gSpecialVar_Result = FALSE;
    gLivingWorldMailbox.request = 0;
    sFramesRemaining = 0;
    sDeferred = FALSE;
    if (npc < LIVING_WORLD_PC_RESIDENT || npc > LIVING_WORLD_GUIDE_FOLLOW_UP
     || !FlagGet(FLAG_SYS_POKEDEX_GET) || gQuestLogState == QL_STATE_PLAYBACK)
        return;

    gLivingWorldMailbox.sequence = sequence != 0 ? sequence : 1;
    gLivingWorldMailbox.npc = npc;
    gLivingWorldMailbox.visibleSpecies = npc < LIVING_WORLD_PALLET_EXCHANGE ? VisibleSpecies() : SPECIES_NONE;
    gLivingWorldMailbox.responseSequence = 0;
    gLivingWorldMailbox.length = 0;
    sFramesRemaining = LIVING_WORLD_TIMEOUT_FRAMES;
    gLivingWorldMailbox.request = LIVING_WORLD_REQUEST_V1;
}

void LivingWorld_BeginPalletConversation(struct ScriptContext *ctx)
{
    BeginConversation(LIVING_WORLD_PC_RESIDENT);
}

void LivingWorld_BeginPalletOptional(struct ScriptContext *ctx)
{
    BeginConversation(ScriptReadByte(ctx));
}

bool8 LivingWorld_WaitForDialogue(void)
{
    if (sFramesRemaining == 0)
        return TRUE;

    if (gLivingWorldMailbox.responseSequence == gLivingWorldMailbox.sequence)
    {
        if (gLivingWorldMailbox.length == LIVING_WORLD_REPLY_PENDING && !sDeferred)
        {
            // Acknowledge the one-shot host deferral. Continue rendering frames.
            gLivingWorldMailbox.responseSequence = 0;
            sFramesRemaining = LIVING_WORLD_DEFERRED_FRAMES;
            sDeferred = TRUE;
            return FALSE;
        }
        gSpecialVar_Result = ReceiveDialogue();
    }
    else if (--sFramesRemaining != 0)
        return FALSE;

    gLivingWorldMailbox.request = 0;
    sFramesRemaining = 0;
    return TRUE;
}
