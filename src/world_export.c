#include "global.h"
#include "world_observe.h"
#include "adventure_mode.h"
#include "adventure_progression.h"
#include "caps.h"
#include "constants/region_map_sections.h"
#include "constants/abilities.h"
#include "data.h"
#include "event_data.h"
#include "game_modes.h"
#include "randomizer.h"
#include "wild_encounter.h"
#include "world_export.h"
#include <stddef.h>
#define MAP_GROUP_COUNT gWorldMapCounts
#include "data/map_group_count.h"

#define EXPORT_MAGIC 0x3731574C // LW17
#define EXPORT_PAGE 32
#define EXPORT_WORDS (MAX_LEVEL_UP_MOVES + 1)

enum { QUERY_LAYOUT = 1, QUERY_WILD, QUERY_ABILITY, QUERY_LEARNSET, QUERY_TRAINER, QUERY_STATIC };
enum { QUERY_INVALID, QUERY_RESOLVED, QUERY_DEFERRED };

struct WorldExportContext
{
    u32 magic, version, generation, origin, seed, mode, modes, features, speciesMode, buildTrainer;
    u32 cap, playerTrainerId, starterChosen, starterSlot, nativeMap;
};

struct WorldExportQuery
{
    u32 a, b;
};

struct WorldExportResult
{
    u32 status;
    u32 data[EXPORT_WORDS];
};

struct WorldExportPort
{
    u32 magic, generation, request, command, count, reply;
    struct WorldExportQuery queries[EXPORT_PAGE];
    struct WorldExportResult results[EXPORT_PAGE];
};

EWRAM_DATA struct WorldExportContext gWorldExportContext = {0};
EWRAM_DATA volatile struct WorldExportPort gWorldExportPort = {0};

const u32 gWorldCatalogLayout[] = {
#define WORLD_LAYOUT(name, value) value,
#include "world_catalog_layout.inc"
#undef WORLD_LAYOUT
};

void WorldExport_SetContext(u32 origin)
{
    u32 i, features = 0;
    static const enum RandomizerFeature options[] = {
        RANDOMIZE_WILD_MON, RANDOMIZE_FIELD_ITEMS, RANDOMIZE_TRAINER_MON, RANDOMIZE_FIXED_MON,
        RANDOMIZE_STARTER_AND_GIFT_MON, RANDOMIZE_EGG_MON, RANDOMIZE_ABILITIES, RANDOMIZE_LEARNSET,
    };

    for (i = 0; i < ARRAY_COUNT(options); i++)
        if (RandomizerFeatureEnabled(options[i]))
            features |= 1u << i;
    gWorldExportContext.magic = EXPORT_MAGIC;
    gWorldExportContext.version = 1;
    if (++gWorldExportContext.generation == 0)
        gWorldExportContext.generation = 1;
    gWorldExportContext.origin = origin;
    gWorldExportContext.seed = GetRandomizerSeed();
    gWorldExportContext.mode = AdventureMode_Get();
    gWorldExportContext.modes = gSaveBlock2Ptr->gameModes;
    gWorldExportContext.features = features;
    gWorldExportContext.speciesMode = GetRandomizerOption(RANDOMIZER_OPTION_SPECIES_MODE);
    gWorldExportContext.buildTrainer = GetCurrentDifficultyLevel();
    gWorldExportContext.cap = GetCurrentLevelCap();
    memcpy(&gWorldExportContext.playerTrainerId, gSaveBlock2Ptr->playerTrainerId, sizeof(u32));
    gWorldExportContext.starterChosen = FlagGet(FLAG_SYS_POKEMON_GET);
    gWorldExportContext.starterSlot = VarGet(VAR_STARTER_MON);
    gWorldExportContext.nativeMap = (u8)gSaveBlock1Ptr->location.mapNum
                                | ((u32)(u8)gSaveBlock1Ptr->location.mapGroup << 8);
    gWorldExportPort.magic = 0;
    gWorldExportPort.reply = 0;
    WorldObserve_Start(gWorldExportContext.generation);
}

static void ResolveWild(u32 headerIndex, u32 selector, struct WorldExportResult *out)
{
    static const u8 count[] = { LAND_WILD_COUNT, WATER_WILD_COUNT, ROCK_WILD_COUNT, FISH_WILD_COUNT, HIDDEN_WILD_COUNT };
    u32 variant = selector >> 16;
    u32 area = (selector >> 8) & 0xFF;
    u32 slot = selector & 0xFF;
    u32 i;
    const struct WildPokemonHeader *header;
    const struct WildEncounterTypes *types;
    const struct WildPokemonInfo *methods[5], *info;
    u8 minimum, maximum;
    u16 species;

    if (area >= ARRAY_COUNT(count) || slot >= count[area] || headerIndex >= 2048)
        return;
    for (i = 0; i <= headerIndex; i++)
        if (gWildMonHeaders[i].mapGroup == 0xFF)
            return;
    header = &gWildMonHeaders[headerIndex];
    if (variant >= ARRAY_COUNT(header->encounterTypes) * ARRAY_COUNT(header->encounterTypes[0]))
        return;
    types = &header->encounterTypes[variant / ARRAY_COUNT(header->encounterTypes[0])]
                                   [variant % ARRAY_COUNT(header->encounterTypes[0])];
    methods[0] = types->landMonsInfo;
    methods[1] = types->waterMonsInfo;
    methods[2] = types->rockSmashMonsInfo;
    methods[3] = types->fishingMonsInfo;
    methods[4] = types->hiddenMonsInfo;
    info = methods[area];
    if (info == NULL)
        return;
    if (area == WILD_AREA_HIDDEN)
    {
        out->status = QUERY_DEFERRED;
        return;
    }
    minimum = info->wildPokemon[slot].minLevel;
    maximum = info->wildPokemon[slot].maxLevel;
    AdventureMode_WildRange(info->wildPokemon, slot, &minimum, &maximum);
    species = info->wildPokemon[slot].species;
    out->data[0] = RandomizeWildEncounter(species, header->mapNum, header->mapGroup, area, slot);
    out->data[1] = min(minimum, maximum);
    out->data[2] = max(minimum, maximum);
    out->data[3] = gWorldEncounterWeights[area][slot];
    out->status = QUERY_RESOLVED;
}

static bool32 UsesLearnset(const struct TrainerMon *entry, u16 id)
{
    u32 i;
    if (RandomizerTrainerUsesLearnset(id))
        return TRUE;
    for (i = 0; i < MAX_MON_MOVES; i++)
        if (entry->moves[i] != MOVE_NONE)
            return FALSE;
    return TRUE;
}

static void ResolveTrainer(u32 id, u32 slot, struct WorldExportResult *out)
{
    const struct Trainer *trainer;
    const struct TrainerMon *entry;
    u32 i;
    u16 species, rawAbility, level;
    u8 abilitySlot = 0;
    bool32 protected;

    if (id >= TRAINERS_COUNT || id == TRAINER_NONE)
        return;
    trainer = GetTrainerStructFromId(id);
    if (trainer->party == NULL || slot >= trainer->partySize)
        return;
    protected = GameModes_PreserveGymTeam(id);
    out->data[3] = protected;
    if (trainer->poolSize != 0 || (!protected && RandomizerFeatureEnabled(RANDOMIZE_TRAINER_MON)
        && (trainer->trainerClass == TRAINER_CLASS_RIVAL_EARLY
         || trainer->trainerClass == TRAINER_CLASS_RIVAL_LATE
         || trainer->trainerClass == TRAINER_CLASS_CHAMPION)))
    {
        out->status = QUERY_DEFERRED;
        return;
    }
    entry = &trainer->party[slot];
    species = protected ? entry->species : RandomizeTrainerMon(id, slot, trainer->partySize, entry->species);
    if (species >= NUM_SPECIES)
        return;
    level = AdventureMode_TrainerLevel(id, slot, entry->lvl);
    if (entry->ability != ABILITY_NONE)
        for (i = 0; i < NUM_ABILITY_SLOTS; i++)
            if (gSpeciesInfo[species].abilities[i] == entry->ability)
            {
                abilitySlot = i;
                break;
            }
    rawAbility = gSpeciesInfo[species].abilities[abilitySlot];
    if (rawAbility == ABILITY_NONE)
        for (i = 0; i < NUM_ABILITY_SLOTS; i++)
            if (gSpeciesInfo[species].abilities[i] != ABILITY_NONE)
            {
                rawAbility = gSpeciesInfo[species].abilities[i];
                break;
            }
    out->data[0] = species;
    out->data[1] = level;
    out->data[2] = entry->heldItem;
    out->data[4] = protected ? rawAbility : RandomizeAbility(species, rawAbility);
    out->data[5] = abilitySlot;
    out->data[6] = UsesLearnset(entry, id);
    if (out->data[6])
    {
        u16 moves[MAX_MON_MOVES];
        GetInitialLevelUpMoves(species, level, moves);
        for (i = 0; i < MAX_MON_MOVES; i++)
            out->data[7 + i] = moves[i];
    }
    else
        for (i = 0; i < MAX_MON_MOVES; i++)
            out->data[7 + i] = entry->moves[i];
    out->status = QUERY_RESOLVED;
}

static void Resolve(u32 command, u32 a, u32 b, struct WorldExportResult *out)
{
    u32 i;
    switch (command)
    {
    case QUERY_LAYOUT:
        if (b == 0 && a < ARRAY_COUNT(gWorldCatalogLayout))
        {
            out->data[0] = gWorldCatalogLayout[a];
            out->status = QUERY_RESOLVED;
        }
        else if (b == 1 && a < ARRAY_COUNT(MAP_GROUP_COUNT))
        {
            out->data[0] = MAP_GROUP_COUNT[a];
            out->status = QUERY_RESOLVED;
        }
        break;
    case QUERY_WILD:
        ResolveWild(a, b, out);
        break;
    case QUERY_ABILITY:
        if (a == SPECIES_NONE || a >= NUM_SPECIES || gSpeciesInfo[a].baseHP == 0)
            break;
        for (i = 0; i < NUM_ABILITY_SLOTS; i++)
            out->data[i] = RandomizeAbility(a, gSpeciesInfo[a].abilities[i]);
        out->status = QUERY_RESOLVED;
        break;
    case QUERY_LEARNSET:
        if (a == SPECIES_NONE || a >= NUM_SPECIES || gSpeciesInfo[a].baseHP == 0)
            break;
        {
            const struct LevelUpMove *set = GetSpeciesLevelUpLearnset(a);
            u32 first;
            if (b > 12)
                break;
            first = b * MAX_LEVEL_UP_MOVES;
            for (i = 0; i < first && set->move != LEVEL_UP_MOVE_END; i++)
                set++;
            for (i = 0; i < MAX_LEVEL_UP_MOVES && set[i].move != LEVEL_UP_MOVE_END; i++)
                out->data[i + 1] = set[i].move | ((u32)set[i].level << 16);
            out->data[0] = i;
            out->status = QUERY_RESOLVED;
        }
        break;
    case QUERY_TRAINER:
        ResolveTrainer(a, b, out);
        break;
    case QUERY_STATIC:
        if ((u16)b == SPECIES_NONE || (u16)b >= NUM_SPECIES || b >> 16 > MAX_LEVEL
         || (a >> 24) != 0 || (a >> 16) >= ARRAY_COUNT(MAP_GROUP_COUNT)
         || ((a >> 8) & 0xFF) >= MAP_GROUP_COUNT[a >> 16])
            break;
        out->data[0] = RandomizeFixedEncounterMon((u16)b, (a >> 8) & 0xFF, a >> 16, a & 0xFF);
        out->data[1] = AdventureMode_ScriptedLevelForMap(a >> 8, (u16)b, b >> 16);
        out->status = QUERY_RESOLVED;
        break;
    }
}

void WorldExport_Poll(void)
{
    u32 i, j, command, count, request;
    if (gWorldExportPort.magic != EXPORT_MAGIC
     || gWorldExportPort.generation != gWorldExportContext.generation)
        return;
    request = gWorldExportPort.request;
    if (request == 0 || request == gWorldExportPort.reply)
        return;
    command = gWorldExportPort.command;
    count = gWorldExportPort.count;
    if (count == 0 || count > EXPORT_PAGE)
        return;
    for (i = 0; i < count; i++)
    {
        struct WorldExportResult row = {0};
        Resolve(command, gWorldExportPort.queries[i].a, gWorldExportPort.queries[i].b, &row);
        gWorldExportPort.results[i].status = row.status;
        for (j = 0; j < EXPORT_WORDS; j++)
            gWorldExportPort.results[i].data[j] = row.data[j];
    }
    gWorldExportPort.reply = request;
}
