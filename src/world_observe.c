#include "global.h"
#include "battle.h"
#include "event_data.h"
#include "main.h"
#include "pokemon.h"
#include "world_observe.h"

#define OBSERVE_MAGIC 0x3831574C // LW18
#define OBSERVE_CAPACITY 48
#define NO_MAP 0xFFFF
#define OMITTED_BATTLES (BATTLE_TYPE_LINK | BATTLE_TYPE_RECORDED | BATTLE_TYPE_RECORDED_LINK \
                       | BATTLE_TYPE_POKEDUDE | BATTLE_TYPE_OLD_MAN_TUTORIAL)

enum ObservationKind
{
    OBS_MAP = 1, OBS_STORY, OBS_BATTLE_START, OBS_BATTLE_MON, OBS_BATTLE_END,
    OBS_BALL_FAILED, OBS_CAPTURE, OBS_PARTY, OBS_EVOLUTION, OBS_SAVE,
};

struct ObservedMon
{
    u32 personality, ot, ivs;
    u16 species, ability, item, moves[MAX_MON_MOVES];
    u8 level, nature, ball, slot, abilitySlot, egg;
};

struct WorldObservation
{
    u32 sequence, frame, kind, map, battle, actor, value, flags;
    struct ObservedMon mon;
};

struct WorldObservationPort
{
    u32 magic, version, capacity, recordSize, generation, sequence, frame, reserved;
    struct WorldObservation records[OBSERVE_CAPACITY];
};

STATIC_ASSERT(sizeof(struct WorldObservation) == 64, WorldObservationRecordSize);
STATIC_ASSERT(offsetof(struct WorldObservationPort, records) == 32, WorldObservationHeaderSize);

EWRAM_DATA volatile struct WorldObservationPort gWorldObservationPort = {0};
static EWRAM_DATA struct ObservedMon sParty[PARTY_SIZE] = {0};
static EWRAM_DATA struct Pokemon sPartySource[PARTY_SIZE] = {0};
static EWRAM_DATA u32 sMap = 0;
static EWRAM_DATA u32 sStory = 0;
static EWRAM_DATA u32 sBattle = 0;
static EWRAM_DATA u32 sBattleFlags = 0;
static EWRAM_DATA u32 sLastParty = 0;

static bool32 Active(void)
{
    return gWorldObservationPort.magic == OBSERVE_MAGIC;
}

static u32 Map(void)
{
    return ((u8)gSaveBlock1Ptr->location.mapGroup << 8) | (u8)gSaveBlock1Ptr->location.mapNum;
}

static u32 Emit(u8 kind, u32 battle, u32 actor, u32 value, u32 flags, const struct ObservedMon *mon)
{
    u32 sequence = gWorldObservationPort.sequence + 1;
    struct WorldObservation observation = {
        .sequence = sequence,
        .frame = gMain.vblankCounter1,
        .kind = kind,
        .map = Map(),
        .battle = battle,
        .actor = actor,
        .value = value,
        .flags = flags,
    };
    if (mon != NULL)
        observation.mon = *mon;
    gWorldObservationPort.records[(sequence - 1) % OBSERVE_CAPACITY] = observation;
    gWorldObservationPort.sequence = sequence;
    return sequence;
}

static struct ObservedMon ReadMon(const struct Pokemon *source, u8 slot)
{
    // GetMonData can mark damaged data as a Bad Egg. Inspect a copy.
    struct Pokemon mon = *source;
    struct ObservedMon observed = { .slot = slot };
    u32 i;

    observed.species = GetMonData(&mon, MON_DATA_SPECIES_OR_EGG);
    if (observed.species == SPECIES_NONE)
        return observed;
    observed.egg = GetMonData(&mon, MON_DATA_IS_EGG);
    observed.personality = GetMonData(&mon, MON_DATA_PERSONALITY);
    observed.ot = GetMonData(&mon, MON_DATA_OT_ID);
    observed.ivs = GetMonData(&mon, MON_DATA_IVS);
    if (observed.egg)
        return observed;
    observed.abilitySlot = GetMonData(&mon, MON_DATA_ABILITY_NUM);
    observed.ability = GetEffectiveAbilityBySpecies(observed.species, observed.abilitySlot,
                                                  GetMonData(&mon, MON_DATA_CANT_RANDOMIZE_ABILITY));
    observed.item = GetMonData(&mon, MON_DATA_HELD_ITEM);
    observed.level = GetMonData(&mon, MON_DATA_LEVEL);
    observed.nature = GetNature(&mon);
    observed.ball = GetMonData(&mon, MON_DATA_POKEBALL);
    for (i = 0; i < MAX_MON_MOVES; i++)
        observed.moves[i] = GetMonData(&mon, MON_DATA_MOVE1 + i);
    return observed;
}

static void ObserveParty(void)
{
    u32 slot;
    for (slot = 0; slot < PARTY_SIZE; slot++)
    {
        struct ObservedMon mon;
        if (memcmp(&sPartySource[slot], &gPlayerParty[slot], sizeof(struct Pokemon)) == 0)
            continue;
        sPartySource[slot] = gPlayerParty[slot];
        mon = ReadMon(&sPartySource[slot], slot);
        if (memcmp(&mon, &sParty[slot], sizeof(mon)) != 0)
        {
            Emit(OBS_PARTY, 0, 0, 0, 0, &mon);
            sParty[slot] = mon;
        }
    }
    sLastParty = gMain.vblankCounter1;
}

static void ObserveStory(void)
{
    static const u16 flags[] = {
        FLAG_BADGE01_GET, FLAG_BADGE02_GET, FLAG_BADGE03_GET, FLAG_BADGE04_GET,
        FLAG_BADGE05_GET, FLAG_BADGE06_GET, FLAG_BADGE07_GET, FLAG_BADGE08_GET,
        FLAG_SYS_POKEMON_GET, FLAG_SYS_GAME_CLEAR, FLAG_KOGA_RETURNED_FROM_HAVORA,
        FLAG_RECEIVED_SAFARI_STELLAR_TICKET,
    };
    u32 i, story = 0;
    for (i = 0; i < ARRAY_COUNT(flags); i++)
        if (FlagGet(flags[i]))
            story |= 1u << i;
    if (story != sStory)
    {
        Emit(OBS_STORY, 0, 0, story, 0, NULL);
        sStory = story;
    }
}

void WorldObserve_Start(u32 generation)
{
    gWorldObservationPort.magic = 0;
    gWorldObservationPort.version = 1;
    gWorldObservationPort.capacity = OBSERVE_CAPACITY;
    gWorldObservationPort.recordSize = sizeof(struct WorldObservation);
    gWorldObservationPort.generation = generation;
    gWorldObservationPort.sequence = 0;
    gWorldObservationPort.frame = gMain.vblankCounter1;
    sMap = NO_MAP;
    sStory = 0xFFFFFFFF;
    sBattle = 0;
    sLastParty = gMain.vblankCounter1 - 32;
    memset(sParty, 0, sizeof(sParty));
    memset(sPartySource, 0, sizeof(sPartySource));
    gWorldObservationPort.magic = OBSERVE_MAGIC;
}

void WorldObserve_Frame(void)
{
    gWorldObservationPort.frame = gMain.vblankCounter1;
}

void WorldObserve_Field(void)
{
    u32 map;
    if (!Active())
        return;
    map = Map();
    if (map != sMap)
    {
        Emit(OBS_MAP, 0, 0, sMap, 0, NULL);
        sMap = map;
        ObserveStory();
    }
    if (gMain.vblankCounter1 - sLastParty >= 32)
    {
        ObserveParty();
        ObserveStory();
    }
}

void WorldObserve_BattleStart(u32 flags, u16 trainerA, u16 trainerB)
{
    u32 slot;
    if (!Active() || (flags & OMITTED_BATTLES))
        return;
    if (!(flags & BATTLE_TYPE_TRAINER))
        trainerA = trainerB = 0;
    else if (!(flags & BATTLE_TYPE_TWO_OPPONENTS))
        trainerB = 0;

    sBattle = gWorldObservationPort.sequence + 1;
    sBattleFlags = flags;
    Emit(OBS_BATTLE_START, sBattle, trainerA, trainerB, flags, NULL);
    for (slot = 0; slot < PARTY_SIZE; slot++)
    {
        struct ObservedMon mon = ReadMon(&gEnemyParty[slot], slot);
        u32 actor = trainerB && slot >= PARTY_SIZE / 2 ? trainerB : trainerA;
        if (mon.species != SPECIES_NONE)
            Emit(OBS_BATTLE_MON, sBattle, actor, 0, flags, &mon);
    }
}

void WorldObserve_BattleEnd(u8 outcome)
{
    if (Active() && sBattle)
    {
        Emit(OBS_BATTLE_END, sBattle, 0, outcome, sBattleFlags, NULL);
        sBattle = 0;
    }
}

void WorldObserve_BallFailed(struct Pokemon *mon, u8 slot, u16 item)
{
    if (Active() && sBattle)
    {
        struct ObservedMon observed = ReadMon(mon, slot);
        Emit(OBS_BALL_FAILED, sBattle, 0, item, sBattleFlags, &observed);
    }
}

void WorldObserve_Capture(struct Pokemon *mon, u8 slot, u8 destination)
{
    if (Active() && sBattle)
    {
        struct ObservedMon observed = ReadMon(mon, slot);
        Emit(OBS_CAPTURE, sBattle, 0, destination, sBattleFlags, &observed);
    }
}

void WorldObserve_Evolution(struct Pokemon *mon, u16 formerSpecies)
{
    if (Active())
    {
        struct ObservedMon observed = ReadMon(mon, 0);
        Emit(OBS_EVOLUTION, 0, 0, formerSpecies, 0, &observed);
    }
}

void WorldObserve_Save(u32 counter)
{
    if (Active())
    {
        ObserveParty();
        ObserveStory();
        Emit(OBS_SAVE, 0, 0, counter, 0, NULL);
    }
}
