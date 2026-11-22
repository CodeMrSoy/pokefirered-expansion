#include "global.h"
#include "event_data.h"
#include "event_object_movement.h"
#include "field_player_avatar.h"
#include "fieldmap.h"
#include "living_world_bridge.h"
#include "quest_log.h"
#include "rtc.h"
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
    u32 localSecond;
};

STATIC_ASSERT(sizeof(struct LivingWorldFieldHint) == 16, LivingWorldFieldHintSize);
EWRAM_DATA volatile struct LivingWorldFieldHint gLivingWorldFieldHint = {0};

enum
{
    BROCK_AT_GYM,
    BROCK_TRAVELING,
    BROCK_AT_FORECOURT
};

struct LivingWorldBrockPresence
{
    u32 magic;
    u16 frame;
    u8 location;
    u8 inverse;
};

STATIC_ASSERT(sizeof(struct LivingWorldBrockPresence) == 8, LivingWorldBrockPresenceSize);
EWRAM_DATA volatile struct LivingWorldBrockPresence gLivingWorldBrockPresence = {0};
EWRAM_DATA volatile struct LivingWorldBrockPresence gLivingWorldTrainerPresence = {0};
EWRAM_DATA volatile struct LivingWorldBrockPresence gLivingWorldResearcherPresence = {0};

struct LivingWorldQuestView
{
    u32 magic;
    u32 plan;
    u8 state;
    u8 source;
    u16 reserved;
};

STATIC_ASSERT(sizeof(struct LivingWorldQuestView) == 12, LivingWorldQuestViewSize);
EWRAM_DATA volatile struct LivingWorldQuestView gLivingWorldQuestView = {0};

u8 LivingWorld_BrockQuestView(void)
{
    struct LivingWorldQuestView view = gLivingWorldQuestView;
    if (view.magic != 0x3951574C || !view.plan || !view.state || view.state > 4
     || !view.source || view.source > 3 || view.reserved
     || !FlagGet(FLAG_SYS_POKEDEX_GET) || gQuestLogState == QL_STATE_PLAYBACK)
        return 0;
    if ((view.state == 1 && view.source != 1) || (view.state == 3 && view.source != 3))
        return 0;
    return view.state;
}

EWRAM_DATA volatile struct LivingWorldQuestView gLivingWorldMuseumQuestView = {0};

u8 LivingWorld_MuseumQuestView(void)
{
    struct LivingWorldQuestView view = gLivingWorldMuseumQuestView;
    if (view.magic != 0x314D514C || !view.plan || view.reserved
     || !FlagGet(FLAG_SYS_POKEDEX_GET) || gQuestLogState == QL_STATE_PLAYBACK)
        return 0;
    if ((view.state == 1 || view.state == 4) && view.source == 1)
        return view.state;
    return view.state == 3 && view.source == 3 ? 3 : 0;
}

EWRAM_DATA volatile struct LivingWorldQuestView gLivingWorldRegionalQuestView = {0};

u8 LivingWorld_RegionalQuestView(void)
{
    struct LivingWorldQuestView view = gLivingWorldRegionalQuestView;
    if (view.magic != 0x3131574C || !view.plan || view.reserved || view.source != 1
     || !FlagGet(FLAG_SYS_POKEDEX_GET) || gQuestLogState == QL_STATE_PLAYBACK)
        return 0;
    return view.state == 1 || (view.state >= 3 && view.state <= 5) ? view.state : 0;
}

static bool8 BrockProtected(void)
{
    return !FlagGet(FLAG_SYS_POKEDEX_GET) || FlagGet(FLAG_BADGE01_GET)
        || FlagGet(FLAG_DEFEATED_BROCK) || gQuestLogState == QL_STATE_PLAYBACK;
}

static u8 ProjectedLocation(volatile const struct LivingWorldBrockPresence *presence, u32 magic, u8 maxLocation)
{
    struct LivingWorldBrockPresence view = *presence;
    if (view.magic != magic || (u16)(gLivingWorldFieldHint.frame - view.frame) >= 90
     || view.location > maxLocation || (view.location ^ view.inverse) != 255)
        return 0;
    return view.location;
}

static u8 BrockLocation(void)
{
    return BrockProtected() ? BROCK_AT_GYM : ProjectedLocation(&gLivingWorldBrockPresence, 0x3142574C, 2);
}

static u8 TrainerLocation(void)
{
    if (!FlagGet(FLAG_SYS_POKEDEX_GET) || gQuestLogState == QL_STATE_PLAYBACK)
        return 0;
    return ProjectedLocation(&gLivingWorldTrainerPresence, 0x3153574C, 2); // LWS1
}

enum { AGENT_BROCK, AGENT_TRAINER, AGENT_RESEARCHER };

static u8 ResearcherLocation(void)
{
    if (!FlagGet(FLAG_SYS_POKEDEX_GET) || gQuestLogState == QL_STATE_PLAYBACK)
        return 0;
    return ProjectedLocation(&gLivingWorldResearcherPresence, 0x3152574C, 3); // LWR1
}

struct LivingWorldSlot
{
    u16 map;
    u8 id, x, y, location;
    u8 actor;
};

static const struct LivingWorldSlot sSlots[] = {
    {MAP_PEWTER_CITY_GYM, 1, 6, 5, BROCK_AT_GYM, AGENT_BROCK},
    {MAP_PEWTER_CITY, 7, 19, 9, BROCK_AT_FORECOURT, AGENT_BROCK},
    {MAP_PEWTER_CITY, 4, 33, 27, 0, AGENT_TRAINER},
    {MAP_ROUTE2, 8, 7, 6, 2, AGENT_TRAINER},
    {MAP_PEWTER_CITY_MUSEUM_1F, 2, 2, 4, 0, AGENT_RESEARCHER},
    {MAP_PEWTER_CITY, 8, 18, 9, 2, AGENT_RESEARCHER},
    {MAP_ROUTE2, 9, 9, 6, 3, AGENT_RESEARCHER},
};

static bool8 WantsSlot(const struct LivingWorldSlot *slot)
{
    u8 current = slot->actor == AGENT_RESEARCHER ? ResearcherLocation()
               : slot->actor == AGENT_TRAINER ? TrainerLocation() : BrockLocation();
    return current == slot->location;
}

bool8 LivingWorld_AllowsObject(u8 localId, u8 mapNum, u8 mapGroup)
{
    u16 map = (mapGroup << 8) | mapNum;
    for (u8 slotId = 0; slotId < ARRAY_COUNT(sSlots); slotId++)
    {
        const struct LivingWorldSlot *slot = &sSlots[slotId];
        if (slot->map != map || slot->id != localId)
            continue;
        if (!WantsSlot(slot))
            return FALSE;
        const s16 x = slot->x + MAP_OFFSET;
        const s16 y = slot->y + MAP_OFFSET;
        for (u8 i = 0; i < OBJECT_EVENTS_COUNT; i++)
        {
            const struct ObjectEvent *object = &gObjectEvents[i];
            if (object->active && ((object->currentCoords.x == x && object->currentCoords.y == y)
                               || (object->previousCoords.x == x && object->previousCoords.y == y)))
                return FALSE;
        }
        break;
    }
    return TRUE;
}

void LivingWorld_ReconcileAgents(void)
{
    u8 group = gSaveBlock1Ptr->location.mapGroup;
    u8 number = gSaveBlock1Ptr->location.mapNum;
    u16 map = (group << 8) | number;
    if ((map != MAP_PEWTER_CITY && map != MAP_PEWTER_CITY_GYM && map != MAP_ROUTE2
      && map != MAP_PEWTER_CITY_MUSEUM_1F)
     || gLivingWorldFieldHint.frame % 8 != 0
     || ScriptContext_IsEnabled() || ArePlayerFieldControlsLocked())
        return;

    const struct ObjectEvent *player = &gObjectEvents[gPlayerAvatar.objectEventId];
    for (u8 i = 0; i < ARRAY_COUNT(sSlots); i++)
    {
        const struct LivingWorldSlot *slot = &sSlots[i];
        if (slot->map != map)
            continue;
        u8 object = GetObjectEventIdByLocalIdAndMap(slot->id, number, group);
        if (!WantsSlot(slot))
        {
            // Let the Route 2 volunteer leave the camera before retiring his slot.
            if (object < OBJECT_EVENTS_COUNT
             && (map != MAP_ROUTE2 || slot->actor != AGENT_RESEARCHER || gObjectEvents[object].offScreen))
                RemoveObjectEventByLocalIdAndMap(slot->id, number, group);
        }
        else if (object >= OBJECT_EVENTS_COUNT && player->active
              && abs(player->currentCoords.x - (slot->x + MAP_OFFSET)) <= 8
              && abs(player->currentCoords.y - (slot->y + MAP_OFFSET)) <= 6)
            TrySpawnObjectEvent(slot->id, number, group);
    }
}

void LivingWorld_BrockHome(struct ScriptContext *ctx)
{
    gSpecialVar_Result = BrockLocation() == BROCK_AT_GYM;
}

bool8 LivingWorld_AllowsScheduledWalk(const struct ObjectEvent *objectEvent)
{
    u16 map = (objectEvent->mapGroup << 8) | objectEvent->mapNum;
    // Only these two ordinary wanderers get schedules. Existing engine
    // direction, range, collision, freeze and held movements remain in force.
    if (!FlagGet(FLAG_SYS_POKEDEX_GET) || gQuestLogState == QL_STATE_PLAYBACK)
        return TRUE;
    if (map == MAP_ROUTE1 && objectEvent->localId == 2)
        return gLocalTime.hours >= LIVING_WORLD_SCOUT_START && gLocalTime.hours < LIVING_WORLD_SCOUT_END;
    if (map == MAP_VIRIDIAN_CITY && objectEvent->localId == 6)
        return gLocalTime.hours >= LIVING_WORLD_STUDENT_START && gLocalTime.hours < LIVING_WORLD_STUDENT_END;
    return TRUE;
}

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
        .localSecond = (u32)-1,
    };
    if (FlagGet(FLAG_SYS_POKEDEX_GET) && gQuestLogState != QL_STATE_PLAYBACK)
    {
        bool8 idle = !ScriptContext_IsEnabled();
        if (hint.frame % 60 == 1)
            RtcCalcLocalTime();
        if (gLocalTime.days >= 0 && gLocalTime.hours >= 0 && gLocalTime.hours < 24
         && gLocalTime.minutes >= 0 && gLocalTime.minutes < 60
         && gLocalTime.seconds >= 0 && gLocalTime.seconds < 60)
            hint.localSecond = (u32)gLocalTime.days * 86400 + gLocalTime.hours * 3600
                             + gLocalTime.minutes * 60 + gLocalTime.seconds;
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
        case MAP_PEWTER_CITY:
            hint.area = 6;
            hint.story = BrockProtected();
            break;
        case MAP_PEWTER_CITY_GYM:
            hint.area = 7;
            hint.story = BrockProtected();
            break;
        case MAP_ROUTE2:
            hint.area = 8;
            hint.story = BrockProtected();
            break;
        case MAP_ROUTE1:
            hint.area = 4;
            if (idle)
                ConsiderNearby(&hint, 2, LIVING_WORLD_ROUTE_SCOUT);
            break;
        case MAP_VIRIDIAN_CITY:
            hint.area = 5;
            hint.story = VarGet(VAR_MAP_SCENE_VIRIDIAN_CITY_OLD_MAN);
            if (idle)
                ConsiderNearby(&hint, 6, LIVING_WORLD_VIRIDIAN_STUDENT);
            break;
        case MAP_VIRIDIAN_FOREST:
            hint.area = 9;
            break;
        case MAP_ROUTE3:
            hint.area = 10;
            break;
        case MAP_MT_MOON_1F:
        case MAP_MT_MOON_B1F:
        case MAP_MT_MOON_B2F:
            hint.area = 11;
            break;
        case MAP_ROUTE4:
            hint.area = 12;
            break;
        case MAP_CERULEAN_CITY:
            hint.area = 13;
            break;
        case MAP_ROUTE24:
            hint.area = 14;
            break;
        case MAP_ROUTE25:
            hint.area = 15;
            break;
        case MAP_CERULEAN_CITY_GYM:
            hint.area = 16;
            break;
        case MAP_ROUTE25_SEA_COTTAGE:
            hint.area = 17;
            break;
        case MAP_PALLET_TOWN_PLAYERS_HOUSE_1F:
        case MAP_PALLET_TOWN_PLAYERS_HOUSE_2F:
            hint.area = 18;
            break;
        case MAP_VIRIDIAN_CITY_GYM:
        case MAP_VIRIDIAN_CITY_HOUSE:
        case MAP_VIRIDIAN_CITY_MART:
        case MAP_VIRIDIAN_CITY_POKEMON_CENTER_1F:
        case MAP_VIRIDIAN_CITY_POKEMON_CENTER_2F:
        case MAP_VIRIDIAN_CITY_SCHOOL:
            hint.area = 19;
            break;
        case MAP_DIGLETTS_CAVE_NORTH_ENTRANCE:
        case MAP_ROUTE2_EAST_BUILDING:
        case MAP_ROUTE2_HOUSE:
        case MAP_ROUTE2_VIRIDIAN_FOREST_NORTH_ENTRANCE:
        case MAP_ROUTE2_VIRIDIAN_FOREST_SOUTH_ENTRANCE:
            hint.area = 20;
            break;
        case MAP_PEWTER_CITY_HOUSE1:
        case MAP_PEWTER_CITY_HOUSE2:
        case MAP_PEWTER_CITY_MART:
        case MAP_PEWTER_CITY_MUSEUM_1F:
        case MAP_PEWTER_CITY_MUSEUM_2F:
        case MAP_PEWTER_CITY_POKEMON_CENTER_1F:
        case MAP_PEWTER_CITY_POKEMON_CENTER_2F:
            hint.area = 21;
            break;
        case MAP_ROUTE4_POKEMON_CENTER_1F:
        case MAP_ROUTE4_POKEMON_CENTER_2F:
            hint.area = 22;
            break;
        case MAP_CERULEAN_CITY_BIKE_SHOP:
        case MAP_CERULEAN_CITY_HOUSE1:
        case MAP_CERULEAN_CITY_HOUSE2:
        case MAP_CERULEAN_CITY_HOUSE3:
        case MAP_CERULEAN_CITY_HOUSE4:
        case MAP_CERULEAN_CITY_HOUSE5:
        case MAP_CERULEAN_CITY_MART:
        case MAP_CERULEAN_CITY_POKEMON_CENTER_1F:
        case MAP_CERULEAN_CITY_POKEMON_CENTER_2F:
            hint.area = 23;
            break;
        case MAP_CERULEAN_CAVE_1F:
        case MAP_CERULEAN_CAVE_2F:
        case MAP_CERULEAN_CAVE_B1F:
            hint.area = 24;
            break;
        case MAP_TRADE_CENTER:
        case MAP_UNION_ROOM:
            hint.area = 25;
            break;
        }
        if (!hint.area || hint.area >= 9)
            hint.story = BrockProtected();
        if (hint.area)
            hint.species = VisibleSpecies();
        if (!idle)
            hint.distance = 255;
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
    if (npc < LIVING_WORLD_PC_RESIDENT || npc > LIVING_WORLD_ROUTE25_RESIDENT
     || !FlagGet(FLAG_SYS_POKEDEX_GET) || gQuestLogState == QL_STATE_PLAYBACK)
        return;

    if (npc == LIVING_WORLD_BROCK_CONTACT && BrockLocation() != BROCK_AT_FORECOURT)
        return;
    gLivingWorldMailbox.sequence = sequence != 0 ? sequence : 1;
    gLivingWorldMailbox.npc = npc;
    gLivingWorldMailbox.visibleSpecies = npc == LIVING_WORLD_PALLET_EXCHANGE || npc == LIVING_WORLD_GUIDE_FOLLOW_UP
                                       ? SPECIES_NONE : VisibleSpecies();
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
