#include "randomizer.h"

#if RANDOMIZER_AVAILABLE == TRUE
#include "main.h"
#include "new_game.h"
#include "item.h"
#include "event_data.h"
#include "field_control_avatar.h"
#include "pokemon.h"
#include "script.h"
#include "data.h"
#include "data/randomizer/special_form_tables.h"
#include "constants/abilities.h"
#include "constants/moves.h"
#include "constants/opponents.h"
#include "data/randomizer/ability_whitelist.h"
#include "constants/abilities.h"

bool8 gRandomizerEnabled = FALSE;
u32 gCachedRandomizerSeed = 0;

void RandomizerApplyFeatureFlags(void)
{
    // A brand-new title-screen session may not have SaveBlock1 mapped yet.
    // NewGameInitData calls this again after the save blocks are initialized.
    if (gSaveBlock1Ptr == NULL)
        return;

    #ifndef FORCE_RANDOMIZE_WILD_MON
        if (gRandomizerEnabled) FlagSet(RANDOMIZER_FLAG_WILD_MON);
        else FlagClear(RANDOMIZER_FLAG_WILD_MON);
    #endif
    #ifndef FORCE_RANDOMIZE_FIELD_ITEMS
        if (gRandomizerEnabled) FlagSet(RANDOMIZER_FLAG_FIELD_ITEMS);
        else FlagClear(RANDOMIZER_FLAG_FIELD_ITEMS);
    #endif
    #ifndef FORCE_RANDOMIZE_TRAINER_MON
        if (gRandomizerEnabled) FlagSet(RANDOMIZER_FLAG_TRAINER_MON);
        else FlagClear(RANDOMIZER_FLAG_TRAINER_MON);
    #endif
    #ifndef FORCE_RANDOMIZE_FIXED_MON
        if (gRandomizerEnabled) FlagSet(RANDOMIZER_FLAG_FIXED_MON);
        else FlagClear(RANDOMIZER_FLAG_FIXED_MON);
    #endif
    #ifndef FORCE_RANDOMIZE_STARTER_AND_GIFT_MON
        if (gRandomizerEnabled) FlagSet(RANDOMIZER_FLAG_STARTER_AND_GIFT_MON);
        else FlagClear(RANDOMIZER_FLAG_STARTER_AND_GIFT_MON);
    #endif
    #ifndef FORCE_RANDOMIZE_EGG_MON
        if (gRandomizerEnabled) FlagSet(RANDOMIZER_FLAG_EGG_MON);
        else FlagClear(RANDOMIZER_FLAG_EGG_MON);
    #endif
    #ifndef FORCE_RANDOMIZE_ABILITIES
        if (gRandomizerEnabled) FlagSet(RANDOMIZER_FLAG_ABILITIES);
        else FlagClear(RANDOMIZER_FLAG_ABILITIES);
    #endif
    #ifndef FORCE_RANDOMIZE_LEARNSET
        if (gRandomizerEnabled) FlagSet(RANDOMIZER_FLAG_LEARNSET);
        else FlagClear(RANDOMIZER_FLAG_LEARNSET);
    #endif
}

void RandomizerSetEnabled(bool8 enabled)
{
    gRandomizerEnabled = enabled;
    if (enabled)
    {
        if (gCachedRandomizerSeed == 0)
        {
            if (gSaveBlock2Ptr != NULL && gSaveBlock2Ptr->randomizerSeed != 0)
                gCachedRandomizerSeed = gSaveBlock2Ptr->randomizerSeed;
            else
                gCachedRandomizerSeed = GenerateSeedForRandomizer();
        }
        if (gSaveBlock2Ptr != NULL)
            gSaveBlock2Ptr->randomizerSeed = gCachedRandomizerSeed;
    }
    else
    {
        gCachedRandomizerSeed = 0;
        if (gSaveBlock2Ptr != NULL)
            gSaveBlock2Ptr->randomizerSeed = 0;
    }
    RandomizerApplyFeatureFlags();
}


// Add the mons you wish to be randomized when given as starter/gift mon to this list
const u16 gStarterAndGiftMonTable[STARTER_AND_GIFT_MON_COUNT] =
{
    SPECIES_BULBASAUR,
    SPECIES_CHARMANDER,
    SPECIES_SQUIRTLE,
    SPECIES_MAGIKARP,
    SPECIES_EEVEE,
    SPECIES_HITMONLEE,
    SPECIES_HITMONCHAN,
    SPECIES_LAPRAS,
    SPECIES_OMANYTE,
    SPECIES_KABUTO,
    SPECIES_AERODACTYL,
};

// Add the mons you wish to be randomized when given as egg mon to this list
const u16 gEggMonTable[EGG_MON_COUNT] =
{
    SPECIES_TOGEPI, 
};

static const u16 sPlayerStarterSpecies[] =
{
    SPECIES_BULBASAUR,
    SPECIES_SQUIRTLE,
    SPECIES_CHARMANDER,
};

// These are the stable roster roles used by the rival's parties throughout
// the game.  The actual species assigned to each role is generated once from
// the randomizer seed and reused in every later rival battle.
static const u16 sRivalRosterOriginalSpecies[] =
{
    SPECIES_BULBASAUR, // starter
    SPECIES_PIDGEY,    // Pidgey line
    SPECIES_ABRA,      // Abra line
    SPECIES_RATTATA,   // Rattata line
    SPECIES_RHYHORN,   // Rhyhorn line
    SPECIES_GROWLITHE, // Growlithe line
    SPECIES_EXEGGCUTE, // Exeggcute line
    SPECIES_GYARADOS,  // Gyarados line
};

EWRAM_DATA static u32 sLastRivalRosterSeed = 0;
EWRAM_DATA static u16 sRivalRosterSpecies[ARRAY_COUNT(sRivalRosterOriginalSpecies)] = {0};

// This is a list of baby Pokémon that should not cause their evolution
// to count as an evolved pokemon.
// XXX: put this somewhere else?
static const u16 sPreevolutionBabyMons[] =
{
    SPECIES_PICHU,
    SPECIES_CLEFFA,
    SPECIES_IGGLYBUFF,
    SPECIES_TYROGUE,
    SPECIES_SMOOCHUM,
    SPECIES_ELEKID,
    SPECIES_MAGBY,
    SPECIES_AZURILL,
    SPECIES_WYNAUT,
    SPECIES_BUDEW,
    SPECIES_CHINGLING,
    SPECIES_BONSLY,
    SPECIES_MIME_JR,
    SPECIES_HAPPINY,
    SPECIES_MUNCHLAX,
    SPECIES_MANTYKE,
};

bool32 RandomizerFeatureEnabled(enum RandomizerFeature feature)
{
    if (!gRandomizerEnabled || GetRandomizerSeed() == 0)
        return FALSE;

    switch(feature)
    {
        case RANDOMIZE_WILD_MON:
            #ifdef FORCE_RANDOMIZE_WILD_MON
                return FORCE_RANDOMIZE_WILD_MON;
            #else
                return FlagGet(RANDOMIZER_FLAG_WILD_MON);
            #endif
        case RANDOMIZE_FIELD_ITEMS:
            #ifdef FORCE_RANDOMIZE_FIELD_ITEMS
                return FORCE_RANDOMIZE_FIELD_ITEMS;
            #else
                return FlagGet(RANDOMIZER_FLAG_FIELD_ITEMS);
            #endif
        case RANDOMIZE_TRAINER_MON:
            #ifdef FORCE_RANDOMIZE_TRAINER_MON
                return FORCE_RANDOMIZE_TRAINER_MON;
            #else
                return FlagGet(RANDOMIZER_FLAG_TRAINER_MON);
            #endif
        case RANDOMIZE_FIXED_MON:
            #ifdef FORCE_RANDOMIZE_FIXED_MON
                return FORCE_RANDOMIZE_FIXED_MON;
            #else
                return FlagGet(RANDOMIZER_FLAG_FIXED_MON);
            #endif
        case RANDOMIZE_STARTER_AND_GIFT_MON:
            #ifdef FORCE_RANDOMIZE_STARTER_AND_GIFT_MON
                return FORCE_RANDOMIZE_STARTER_AND_GIFT_MON;
            #else
                return FlagGet(RANDOMIZER_FLAG_STARTER_AND_GIFT_MON);
            #endif
        case RANDOMIZE_EGG_MON:
            #ifdef FORCE_RANDOMIZE_EGG_MON
                return FORCE_RANDOMIZE_EGG_MON;
            #else
                return FlagGet(RANDOMIZER_FLAG_EGG_MON);
            #endif
        case RANDOMIZE_ABILITIES:
            #ifdef FORCE_RANDOMIZE_ABILITIES
                return FORCE_RANDOMIZE_ABILITIES;
            #else
                return FlagGet(RANDOMIZER_FLAG_ABILITIES);
            #endif
        case RANDOMIZE_LEARNSET:
            #ifdef FORCE_RANDOMIZE_LEARNSET
                return FORCE_RANDOMIZE_LEARNSET;
            #else
                return FlagGet(RANDOMIZER_FLAG_LEARNSET);
            #endif
        default:
            return FALSE;
    }
}

u32 GetRandomizerSeed(void)
{
    /* return cached seed when saveblock is cleared or uninitialised */
    if (gSaveBlock2Ptr == NULL || gSaveBlock2Ptr->randomizerSeed == 0)
        return gCachedRandomizerSeed;
    return gSaveBlock2Ptr->randomizerSeed;
}

bool8 RandomizerEnabled(void)
{
    return GetRandomizerSeed() != 0;
}

static bool32 IsSpeciesPermitted(u16 species)
{
    // SPECIES_NONE is never valid.
    if (species == SPECIES_NONE)
        return FALSE;
    // This is used to indicate a disabled species.
    if (gSpeciesInfo[species].baseHP == 0)
        return FALSE;
    if (gSpeciesInfo[species].randomizerMode == MON_RANDOMIZER_INVALID)
        return FALSE;

    return TRUE;
};

u32 GenerateSeedForRandomizer(void)
{
    u32 data;
    const u32 vblankCounter = gMain.vblankCounter1;
    #if HQ_RANDOM == TRUE
        data = Random32();
    #else
        data = gRngValue;
        Random();
    #endif
    return data ^ vblankCounter;
}

u16 GetRandomizerOption(enum RandomizerOption option)
{
    switch(option) {
        case RANDOMIZER_OPTION_SPECIES_MODE:
            return VarGet(RANDOMIZER_VAR_SPECIES_MODE);
        default: // Unknown option.
            return 0;
    }
}

/* Seeds an SFC32 random number generator state for the randomizer.
SFC32 can be seeded with up to 96 bits of data.
32 are used for the randomizer reason, which is mixed with the seed.
data1 and data2 are 64 bits of data that a caller can use for
any purpose they wish. Certain groups of functions will assign a purpose to
these: for example, RandomizeMon uses data2 for the original species number.
data2 is also mixed with the seed.
*/
struct Sfc32State RandomizerRandSeed(enum RandomizerReason reason, u32 data1, u32 data2)
{
    struct Sfc32State state;
    u32 i;
    const u32 randomizerSeed = GetRandomizerSeed();

    state.a = randomizerSeed + (u32)reason;
    state.b = randomizerSeed ^ data2;
    state.c = data1;
    state.ctr = RANDOMIZER_STREAM;

    for (i = 0; i < 10; i++)
    {
        _SFC32_Next_Stream(&state, RANDOMIZER_STREAM);
    }

    return state;
}


// This uses a slightly accelerated bitmasking method.
u32 RandomizerNextRange(struct Sfc32State* state, u32 range)
{
    u32 next_power_of_two, mask, result;
    if (range < 2)
        return 0;
    else if (range == UINT32_MAX)
        return _SFC32_Next_Stream(state, RANDOMIZER_STREAM);

    next_power_of_two = range;
    --next_power_of_two;
    next_power_of_two |= next_power_of_two >> 1;
    next_power_of_two |= next_power_of_two >> 2;
    next_power_of_two |= next_power_of_two >> 4;
    next_power_of_two |= next_power_of_two >> 8;
    ++next_power_of_two;

    mask = next_power_of_two - 1;

    do
    {
        result = _SFC32_Next_Stream(state, RANDOMIZER_STREAM) & mask;
    } while (result >= range);

    return result;
}

// Functions for producing single seeded random numbers.
u16 RandomizerRand(enum RandomizerReason reason, u32 data1, u32 data2)
{
    struct Sfc32State state;
    state = RandomizerRandSeed(reason, data1, data2);
    return RandomizerNext(&state);
}

u16 RandomizerRandRange(enum RandomizerReason reason, u32 data1, u32 data2, u16 range)
{
    struct Sfc32State state;
    state = RandomizerRandSeed(reason, data1, data2);
    return RandomizerNextRange(&state, range);
}

// Utility functions for the field item randomizer.
//static inline bool32 IsItemTMHM(u16 itemId)
//{
//  return ItemId_GetPocket(itemId) == POCKET_TM_HM;
//}

//static inline bool32 IsItemHM(u16 itemId)
//{
//    return itemId >= ITEM_HM01 && IsItemTMHM(itemId);
//}

static inline bool32 IsKeyItem(u16 itemId)
{
    return GetPocketByItemId(itemId) == POCKET_KEY_ITEMS;
}

// Don't randomize HMs or key items, that can make the game unwinnable.
// ITEM_NONE also should not be randomized as it is invalid.
static inline bool32 ShouldRandomizeItem(u16 itemId)
{
    return !(IsItemHM(itemId) || IsKeyItem(itemId) || itemId == ITEM_NONE);
}

#include "data/randomizer/item_whitelist.h"

// Given a found item and its location in the game, returns a replacement for that item.
u16 RandomizeFoundItem(u16 itemId, u8 mapNum, u8 mapGroup, u8 localId)
{
    struct Sfc32State state;
    u16 result;
    u32 mapSeed;

    if (!ShouldRandomizeItem(itemId))
        return itemId;

    // Seed the generator using the original item and the object event that led up
    // to this call.
    mapSeed = ((u32)mapGroup) << 16;
    mapSeed |= ((u32)mapNum) << 8;
    mapSeed |= localId;

    state = RandomizerRandSeed(RANDOMIZER_REASON_FIELD_ITEM, mapSeed, itemId);

    // Randomize TMs to TMs. Because HMs shouldn't be randomized, we can assume
    // this is a TM.
    if (IsItemTMHM(itemId))
        return RandomizerNextRange(&state, RANDOMIZER_MAX_TM - ITEM_TM01 + 1) + ITEM_TM01;

    // Randomize everything else to everything else.
    do {
        result = sRandomizerItemWhitelist[RandomizerNextRange(&state, ITEM_WHITELIST_SIZE)];
    } while(!ShouldRandomizeItem(result) || IsItemTMHM(result));

    return result;

}

// Takes a SpecialVar as an argument to simplify handling separate scripts.
static inline void RandomizeFoundItemScript(u16 *scriptVar)
{
    if (RandomizerFeatureEnabled(RANDOMIZE_FIELD_ITEMS))
    {
        // Pull the object event information from the current object event.
        u8 objEvent = gSelectedObjectEvent;
        *scriptVar = RandomizeFoundItem(
            *scriptVar,
            gObjectEvents[objEvent].mapGroup,
            gObjectEvents[objEvent].mapNum,
            gObjectEvents[objEvent].localId);
    }
}

// These functions are invoked by the scripts that handle found items and
// write the results of the randomization to the correct script variable.
void FindItemRandomize_NativeCall(struct ScriptContext *ctx)
{
    RandomizeFoundItemScript(&gSpecialVar_0x8000);
}

void FindHiddenItemRandomize_NativeCall(struct ScriptContext *ctx)
{
    RandomizeFoundItemScript(&gSpecialVar_0x8005);
}

// Both legendary and mythical Pokémon are included in this category.
static inline bool32 IsRandomizerLegendary(u16 species)
{
    return gSpeciesInfo[species].isLegendary
        || gSpeciesInfo[species].isMythical
        || gSpeciesInfo[species].isUltraBeast;
}

struct SpeciesTable
{
    // Stores the group records for each species.
    u16 groupData[RANDOMIZER_SPECIES_COUNT];
    u16 speciesToGroupIndex[RANDOMIZER_SPECIES_COUNT];
    // Maps a group data index to a species.
    u16 groupIndexToSpecies[RANDOMIZER_SPECIES_COUNT];
};

#define GROUP_INVALID   0xFFFF

static inline u16 GetSpeciesGroup(const struct SpeciesTable* table, u16 species)
{
    u16 groupEntry = table->groupData[table->speciesToGroupIndex[species]];

    #ifndef NDEBUG
        u16 index = table->speciesToGroupIndex[species];
        u16 mappedSpecies = table->groupIndexToSpecies[index];
        MgbaPrintf(MGBA_LOG_INFO, "GetSpeciesGroup: species=%u, mappedSpecies=%u, group=%u",
        species + 1, mappedSpecies + 1, groupEntry);
    #endif

    return groupEntry;

}

static void GetGroupRange(u16 group, enum RandomizerSpeciesMode mode, u16 *resultMin, u16 *resultMax)
{
    // This should never be called on a GROUP_INVALID mon, but if it happens,
    // GROUP_INVALID should be the only valid group.
    if (group == GROUP_INVALID)
    {
        *resultMax = *resultMin = group;
        return;
    }

    // BST mode: species can randomize to species with similar BST.
    if (mode == MON_RANDOM_BST)
    {
        // Choose a 10.24% range around the base BST.
        s32 base, minScaled, maxScaled;
        base = group * 1024;
        minScaled = (base - group * 100) / 1024;
        maxScaled = (base + group * 100) / 1024;
        *resultMin = (u16)max(minScaled, 0);
        *resultMax =(u16)min(maxScaled, GROUP_INVALID-1);
    }
    // Species in the same category can randomize to each other.
    else
    {
        *resultMax = *resultMin = group;
    }
}

//
static void GetIndicesFromGroupRange(const struct SpeciesTable *table, u16 minGroup, u16 maxGroup, u16 *start, u16 *end)
{
    u16 index, leftBound, rightBound, maxRightBound;
    maxRightBound = RANDOMIZER_SPECIES_COUNT-1;
    maxGroup = min(0xFFFEu, maxGroup);
    minGroup = min(0xFFFEu, minGroup);
    leftBound = 0;
    rightBound = RANDOMIZER_SPECIES_COUNT-1;
    // Do leftmost binary search to find the lower limit.
    while (leftBound < rightBound)
    {
        u16 leftFoundGroup;
        index = (leftBound + rightBound) / 2;
        leftFoundGroup = table->groupData[index];
        if (leftFoundGroup < minGroup)
            leftBound = index + 1;
        else
        {
            if (leftFoundGroup > maxGroup)
                maxRightBound = index;
            rightBound = index;
        }
    }
    *start = leftBound;

    rightBound = maxRightBound;

    // Do rightmost binary search to find the upper limit.
    while (leftBound < rightBound)
    {
        index = (leftBound + rightBound) / 2;
        if (table->groupData[index] > maxGroup)
            rightBound = index;
        else
            leftBound = index + 1;
    }
    *end = rightBound - 1;
}

#if RANDOMIZER_DYNAMIC_SPECIES == TRUE

struct RamSpeciesTable
{
    enum RandomizerSpeciesMode mode;
    bool16 tableInitialized;
    struct SpeciesTable speciesTable;
};

EWRAM_DATA static struct RamSpeciesTable sRamSpeciesTable = {0};

static void FillSpeciesGroupsRandom(struct SpeciesTable* entries)
{
    u16 i;
    for (i = 0; i < RANDOMIZER_SPECIES_COUNT; i++)
    {
        entries->groupIndexToSpecies[i] = i;
        if (IsSpeciesPermitted(i))
            entries->groupData[i] = 0;
        else
            entries->groupData[i] = GROUP_INVALID;
    }
}

static void FillSpeciesGroupsBST(struct SpeciesTable* entries)
{
    u16 i;
    for(i = 0; i < RANDOMIZER_SPECIES_COUNT; i++)
    {
        const struct SpeciesInfo *curSpeciesInfo;
        u16 group;

        entries->groupIndexToSpecies[i] = i;

        if (IsSpeciesPermitted(i))
        {
            curSpeciesInfo = &gSpeciesInfo[i];

            group = curSpeciesInfo->baseAttack;
            group += curSpeciesInfo->baseDefense;
            group += curSpeciesInfo->baseSpAttack;
            group += curSpeciesInfo->baseSpDefense;
            group += curSpeciesInfo->baseHP;
            group += curSpeciesInfo->baseSpeed;

        }
        else
            group = GROUP_INVALID;

        entries->groupData[i] = group;
    }
}

static void FillSpeciesGroupsLegendary(struct SpeciesTable* entries)
{
    u16 i;
    for(i = 0; i < RANDOMIZER_SPECIES_COUNT; i++)
    {
        entries->groupIndexToSpecies[i] = i;
        if (!IsSpeciesPermitted(i))
            entries->groupData[i] = GROUP_INVALID;
        else
            entries->groupData[i] = IsRandomizerLegendary(i);
    }
}

static void MarkEvolutions(struct SpeciesTable *entries, u16 species, u16 stage)
{
    const struct Evolution *evos;
    if (stage == RANDOMIZER_MAX_EVO_STAGES)
        return;

    evos = GetSpeciesEvolutions(species);
    if (evos != NULL)
    {
        u32 i;
        for (i = 0; evos[i].method != 0xFFFF; i++)
        {
            if(entries->groupData[species-1] <= stage)
                MarkEvolutions(entries, evos[i].targetSpecies, stage+1);
        }
    }
    entries->groupIndexToSpecies[species] = species;
    entries->groupData[species] = stage;
}

static void FillSpeciesGroupsEvolution(struct SpeciesTable* entries)
{
    u16 i;
    static const u8 EVO_GROUP_LEGENDARY = 0x81;
    static const u8 EVO_GROUP_NO_EVO = RANDOMIZER_MAX_EVO_STAGES+1;

    // Step 0: zero everything
    memset(entries, 0, sizeof(sRamSpeciesTable.speciesTable));

    // Step 1: pre-visit the special babies, and mark them as basic mons.
    for (i = 0; i < ARRAY_COUNT(sPreevolutionBabyMons); i++)
    {
        u16 babyMonIndex = sPreevolutionBabyMons[i];
        entries->groupIndexToSpecies[babyMonIndex] = babyMonIndex;
        if(IsSpeciesPermitted(babyMonIndex))
            entries->groupData[babyMonIndex] = 0;
        else
            entries->groupData[babyMonIndex] = GROUP_INVALID;
    }

    for(i = 0; i < RANDOMIZER_SPECIES_COUNT; i++)
    {
        if (entries->groupIndexToSpecies[i] == 0)
        {
            // This entry hasn't been visited yet, so we don't know if it evolves.
            const struct Evolution *evos = GetSpeciesEvolutions(i);
            entries->groupIndexToSpecies[i] = i;
            if (!IsSpeciesPermitted(i)) // This shouldn't show up in randomization.
                entries->groupData[i] = GROUP_INVALID;
            else if (IsRandomizerLegendary(i)) // Legendaries get their own group.
                entries->groupData[i] = EVO_GROUP_LEGENDARY;
            else if (evos == NULL || evos->method == 0xFFFF)
                entries->groupData[i] = EVO_GROUP_NO_EVO;
            else // There are evolutions! Let's check it out.
                MarkEvolutions(entries, i, 0);
        }
    }
}

static inline u16 LeftChildIndex(u16 index)
{
    return 2*index + 1;
}

static inline void SwapSpeciesAndGroup(struct SpeciesTable* table, u16 indexA, u16 indexB)
{
    u16 temp;
    SWAP(table->groupData[indexA], table->groupData[indexB], temp);
    SWAP(table->groupIndexToSpecies[indexA], table->groupIndexToSpecies[indexB], temp);
}

static void BuildRandomizerSpeciesTable(enum RandomizerSpeciesMode mode)
{
    u16 i, start, end;
    struct SpeciesTable* speciesTable;

    sRamSpeciesTable.tableInitialized = TRUE;
    sRamSpeciesTable.mode = mode;
    speciesTable = &sRamSpeciesTable.speciesTable;

    switch(mode)
    {
        case MON_RANDOM_LEGEND_AWARE:
            FillSpeciesGroupsLegendary(speciesTable);
            break;
        case MON_RANDOM_BST:
            FillSpeciesGroupsBST(speciesTable);
            break;
        case MON_EVOLUTION:
            FillSpeciesGroupsEvolution(speciesTable);
            break;
        case MON_RANDOM:
        default:
            FillSpeciesGroupsRandom(speciesTable);
    }

    // Heap sort the table.
    start = RANDOMIZER_SPECIES_COUNT/2;
    end = RANDOMIZER_SPECIES_COUNT-1;

    while (end > 1)
    {
        u16 root;
        if (start > 0)
            start = start - 1;
        else
        {
            end = end - 1;
            SwapSpeciesAndGroup(speciesTable, end, 0);
        }
        root = start;
        while(LeftChildIndex(root) < end)
        {
            u16 child;
            child = LeftChildIndex(root);

            if (child+1 < end
                && speciesTable->groupData[child] < speciesTable->groupData[child+1])
            {
                child = child + 1;
            }

            if (speciesTable->groupData[root] < speciesTable->groupData[child])
            {
                SwapSpeciesAndGroup(speciesTable, root, child);
                root = child;
            }
            else
                break;
        }
    }


    // Build the species index. This is needed for getting a group from a species.
    for (i = 0; i < RANDOMIZER_SPECIES_COUNT; i++)
    {
        u16 targetIndex = speciesTable->groupIndexToSpecies[i];
        speciesTable->speciesToGroupIndex[targetIndex] = i;
    }
}

static const struct SpeciesTable* GetSpeciesTable(enum RandomizerSpeciesMode mode)
{
    if (!sRamSpeciesTable.tableInitialized || mode != sRamSpeciesTable.mode )
        BuildRandomizerSpeciesTable(mode);

    return &sRamSpeciesTable.speciesTable;
}

void PreloadRandomizationTables(void)
{
    GetSpeciesTable(GetRandomizerOption(RANDOMIZER_OPTION_SPECIES_MODE));
}

#endif

static u16 RandomizeMonTableLookup(struct Sfc32State* state, enum RandomizerSpeciesMode mode, u16 species)
{
    u16 minGroup, maxGroup, originalGroup, resultIndex;
    u16 minIndex, maxIndex;
    const struct SpeciesTable *table;

    table = GetSpeciesTable(mode);
    originalGroup = GetSpeciesGroup(table, species);

    if (originalGroup == GROUP_INVALID)
        return species;

    GetGroupRange(originalGroup, mode, &minGroup, &maxGroup);
    GetIndicesFromGroupRange(table, minGroup, maxGroup, &minIndex, &maxIndex);
    resultIndex = RandomizerNextRange(state, maxIndex - minIndex + 1) + minIndex;
    return table->groupIndexToSpecies[resultIndex];
}

static u16 RandomizeMonFromSeed(struct Sfc32State *state, enum RandomizerSpeciesMode mode, u16 species)
{
    if (!IsSpeciesPermitted(species))
        return species;

    if (mode >= MAX_MON_MODE)
        mode = MON_RANDOM;

    MgbaPrintf(MGBA_LOG_DEBUG, "RWEnc: Seed %08X Species %d", GetRandomizerSeed(), species);
    return RandomizeMonTableLookup(state, mode, species);

}

// Fills an array with count Pokémon, with no repeats.
void GetUniqueMonList(enum RandomizerReason reason, enum RandomizerSpeciesMode mode, u32 seed1, u16 seed2, u8 count, const u16 *originalSpecies, u16 *resultSpecies)
{
    u32 i, curMon;
    u32 seenMonBitVector[(RANDOMIZER_SPECIES_COUNT-1)/32+1] = {};
    struct Sfc32State state = RandomizerRandSeed(reason, seed1, seed2);

    for (i = 0; i < count; i++)
    {
        u16 curOriginal = originalSpecies[i];
        bool32 foundNextMon = FALSE;
        if (!IsSpeciesPermitted(curOriginal))
        {
            // If there's non-permitted Pokémon in here, something is wrong.
            // Just pass them through without marking.
            curMon = curOriginal;
            continue;
        }

        // Find the next mon.
        while (!foundNextMon)
        {
            u16 wordIndex, adjustedCurMon;
            u32 bitVectorWord;
            u8 bitIndex;

            // Generate a Pokémon. If it has already been generated, keep generating new ones
            // until one that hasn't been seen is picked.

            curMon = RandomizeMonFromSeed(&state, mode, curOriginal);

            // Compute the bit address of this mon.
            adjustedCurMon = curMon - 1;
            wordIndex = adjustedCurMon / 32;
            bitIndex = adjustedCurMon & 31;
            bitVectorWord = seenMonBitVector[wordIndex];

            // If set, this mon has been seen already.
            if (bitVectorWord & (1 << bitIndex))
                continue;

            bitVectorWord |= 1 << bitIndex;
            seenMonBitVector[wordIndex] = bitVectorWord;
            foundNextMon = TRUE;
        }
        resultSpecies[i] = curMon;
    }
}

u16 RandomizeMonBaseForm(enum RandomizerReason reason, enum RandomizerSpeciesMode mode, u32 seed, u16 species)
{
    struct Sfc32State state;
    state = RandomizerRandSeed(reason, seed, species);
    return RandomizeMonFromSeed(&state, mode, species);
}

static u16 ChooseRandomForm(struct Sfc32State *state, const u16 baseSpecies)
{
    const u16 *formsTable = gSpeciesInfo[baseSpecies].formSpeciesIdTable;
    if (formsTable)
    {
        u32 formCount = 0;
        while (formsTable[formCount] != FORM_SPECIES_END)
        {
            formCount++;
        }
        return formsTable[RandomizerNextRange(state, formCount)];
    }

    return baseSpecies;
}

static u16 GetFormFromRareFormInfo(struct Sfc32State *state, const struct RandomizerRareFormInfo *info)
{
    if (RandomizerNextRange(state, info->inverseRareFormChance) > 0)
        return info->commonForm;
    else
        return info->rareForm;
}

#define RANDOM_FROM_ARRAY(arr)  (arr[RandomizerNextRange(state, ARRAY_COUNT(arr))])
#define RARE_FORM(infoStruct)   (GetFormFromRareFormInfo(state, &infoStruct))
static u16 ChooseFormSpecial(struct Sfc32State *state, const u16 baseSpecies)
{
    switch (baseSpecies) {
        // These species do almost ordinary ordinary random form selection processes.
        // However, their form tables include forms that shouldn't normally be
        // selected, so they need to have special hard-coded form tables.
        case SPECIES_FLOETTE:
            return RANDOM_FROM_ARRAY(sFloetteFormChoices);
        case SPECIES_TAUROS_PALDEA_COMBAT:
            return RANDOM_FROM_ARRAY(sPaldeanTaurosFormChoices);
        case SPECIES_MINIOR:
            return RANDOM_FROM_ARRAY(sMiniorFormChoices);
        // These are species, first appearing in Gen 8, that have one common
        // form and one rare form.
        // Note that as Maushold can only appear in raid battles in Gen 9, it
        // normally does not behave this way in the wild, but for a randomizer
        // this seems like a reasonable choice.
        case SPECIES_MAUSHOLD:
            return RARE_FORM(sMausholdRareFormInfo);
        case SPECIES_SINISTEA:
            return RARE_FORM(sSinisteaRareFormInfo);
        case SPECIES_SINISTCHA:
            return RARE_FORM(sSinistchaRareFormInfo);
        case SPECIES_POLTEAGEIST:
            return RARE_FORM(sPolteageistRareFormInfo);
        case SPECIES_DUDUNSPARCE:
            return RARE_FORM(sDudunsparceRareFormInfo);
        default:
            return baseSpecies;
    }

}
#undef RANDOM_FROM_ARRAY
#undef RARE_FORM

u16 RandomizeMon(enum RandomizerReason reason, enum RandomizerSpeciesMode mode, u32 seed, u16 species)
{
    u32 speciesMode;
    u16 resultSpecies;
    struct Sfc32State state;

    if (!IsSpeciesPermitted(species))
        return species;

    state = RandomizerRandSeed(reason, seed, species);

    resultSpecies = RandomizeMonFromSeed(&state, mode, species);
    speciesMode = gSpeciesInfo[resultSpecies].randomizerMode;
    MgbaPrintf(MGBA_LOG_DEBUG, "RWEnc: Seed %08X Species %d", GetRandomizerSeed(), species);
    switch (speciesMode)
    {
        case MON_RANDOMIZER_RANDOM_FORM:
            return ChooseRandomForm(&state, resultSpecies);
        case MON_RANDOMIZER_SPECIAL_FORM:
            return ChooseFormSpecial(&state, resultSpecies);
        case MON_RANDOMIZER_NORMAL:
        default:
            return resultSpecies;
    }
}

u16 RandomizeWildEncounter(u16 species, u8 mapNum, u8 mapGroup, enum WildPokemonArea area, u8 slot)
{
    if (RandomizerFeatureEnabled(RANDOMIZE_WILD_MON))
    {
        // Randomization is done based on the map number, the WildArea, and the encounter slot.
        // This means a distinct species can appear in each encounter slot.
        MgbaPrintf(MGBA_LOG_DEBUG, "RWEnc: Randomizing!");
        u32 seed;
        seed = ((u32)mapGroup) << 24;
        seed |= ((u32)mapNum) << 16;
        seed |= ((u32)area) << 8;
        seed |= slot;

        return RandomizeMon(RANDOMIZER_REASON_WILD_ENCOUNTER, GetRandomizerOption(RANDOMIZER_OPTION_SPECIES_MODE), seed, species);
    }
    
    MgbaPrintf(MGBA_LOG_DEBUG, "RWEnc: Seed 0x%08X Species %d", GetRandomizerSeed(), species);
    return species;
}


// This is used in the Pokédex area map code.
bool32 IsRandomizationPossible(u16 originalSpecies, u16 targetSpecies)
{
    const enum RandomizerSpeciesMode mode = GetRandomizerOption(RANDOMIZER_OPTION_SPECIES_MODE);
    if (!IsSpeciesPermitted(targetSpecies) || !IsSpeciesPermitted(originalSpecies))
    {
        // For a species that is not permitted, randomization is disabled.
        // Therefore, if the species are the same, they will "randomize".
        return originalSpecies == targetSpecies;
    }

    if (mode != MON_RANDOM && mode < MAX_MON_MODE)
    {
        u16 minGroupOriginal, maxGroupOriginal, minGroupTarget, maxGroupTarget,
            originalGroup, targetGroup;
        const struct SpeciesTable* table;
        table = GetSpeciesTable(mode);
        originalGroup = GetSpeciesGroup(table, originalSpecies);
        targetGroup = GetSpeciesGroup(table, targetSpecies);
        GetGroupRange(originalGroup, mode, &minGroupOriginal, &maxGroupOriginal);
        GetGroupRange(targetGroup, mode, &minGroupTarget, &maxGroupTarget);

        // If the group ranges intersect, randomization is possible.
        return maxGroupOriginal >= minGroupTarget && minGroupOriginal <= maxGroupTarget;
    }

    return TRUE;
}

u16 RandomizeTrainerMon(u16 trainerId, u8 slot, u8 totalMons, u16 species)
{
    if (RandomizerFeatureEnabled(RANDOMIZE_TRAINER_MON))
    {
        // The seed is based on the internal trainer number, the number of
        // Pokémon in that trainer's party, and which party position it is in.
        u32 seed;
        seed = (u32)trainerId << 16;
        seed |= (u32)totalMons << 8;
        seed |= slot;

        return RandomizeMon(RANDOMIZER_REASON_TRAINER_PARTY, GetRandomizerOption(RANDOMIZER_OPTION_SPECIES_MODE), seed, species);
    }

    return species;
}

u16 RandomizeFixedEncounterMon(u16 species, u8 mapNum, u8 mapGroup, u8 localId)
{
    if (RandomizerFeatureEnabled(RANDOMIZE_FIXED_MON))
    {
        // The seed is based on the location of the object event.
        u32 seed;
        seed = (u32)mapNum << 16;
        seed |= (u32)mapGroup << 8;
        seed |= localId;

        return RandomizeMon(RANDOMIZER_REASON_FIXED_ENCOUNTER, GetRandomizerOption(RANDOMIZER_OPTION_SPECIES_MODE), seed, species);
    }

    return species;
}

EWRAM_DATA static u32 sLastMonRandomizerSeed = 0;
EWRAM_DATA static u32 sLastMonRandomizerHash = 0;
EWRAM_DATA static u8 sLastMonRandomizerCount = 0;
EWRAM_DATA static u16 sRandomizedMons[STARTER_AND_GIFT_MON_COUNT] = {0};

u16 RandomizeStarterAndGiftMon(u16 originalSlot, const u16* originalStarterAndGiftMons, u8 count)
{
    /* Randomize the Pokémon given as a starter or gift … */

    MgbaPrintf(MGBA_LOG_DEBUG, "StarterRand: Called for slot %d", originalSlot);

    // Prevent out-of-range access
    if (count == 0 || originalSlot >= count || count > STARTER_AND_GIFT_MON_COUNT)
    {
        MgbaPrintf(MGBA_LOG_DEBUG,
                   "StarterRand: Slot %d out of range (max %d), returning original",
                   originalSlot, count - 1);
        return SPECIES_NONE;
    }

    if (RandomizerFeatureEnabled(RANDOMIZE_STARTER_AND_GIFT_MON))
    {
        MgbaPrintf(MGBA_LOG_DEBUG, "StarterRand: Feature enabled");

        u32 starterHash = 5381;
        for (u32 i = 0; i < count; i++)
        {
            u16 originalStarter = originalStarterAndGiftMons[i];
            starterHash = ((starterHash << 5) + starterHash) ^ (u8)originalStarter;
            starterHash = ((starterHash << 5) + starterHash) ^ (u8)(originalStarter >> 8);
        }

        // Rebuild the list if the seed, source pool, or pool size changed.
        if (sLastMonRandomizerSeed != GetRandomizerSeed()
            || sLastMonRandomizerHash != starterHash
            || sLastMonRandomizerCount != count
            || sRandomizedMons[0] == SPECIES_NONE)
        {
            GetUniqueMonList(RANDOMIZER_REASON_STARTER_AND_GIFT_MON,
                              MON_RANDOM,
                              starterHash, 0,
                              count,
                              originalStarterAndGiftMons,
                              sRandomizedMons);

            // Cache the seed used to build the table
            sLastMonRandomizerSeed = GetRandomizerSeed();
            sLastMonRandomizerHash = starterHash;
            sLastMonRandomizerCount = count;
        }

        MgbaPrintf(MGBA_LOG_DEBUG, "StarterRand: Returning %d",
                   sRandomizedMons[originalSlot]);
        return sRandomizedMons[originalSlot];
    }

    // Randomizer disabled; return original starter
    return originalStarterAndGiftMons[originalSlot];
}

u16 GetRandomizedStarterSpecies(u16 starterSlot)
{
    // Use the same table and slot order as showmonpic and givemonrandom.
    static const u8 giftSlots[] = {0, 2, 1};

    if (starterSlot >= ARRAY_COUNT(sPlayerStarterSpecies))
        starterSlot = 0;
    return RandomizeStarterAndGiftMon(giftSlots[starterSlot], gStarterAndGiftMonTable, STARTER_AND_GIFT_MON_COUNT);
}

static u16 GetSpeciesBaseStatTotal(u16 species)
{
    const struct SpeciesInfo *info = &gSpeciesInfo[species];
    return info->baseHP + info->baseAttack + info->baseDefense
        + info->baseSpeed + info->baseSpAttack + info->baseSpDefense;
}

u16 GetRivalStarterSlot(u16 playerStarterSlot)
{
    u16 bestSpecies;
    u16 bestSlot;
    u16 candidateSpecies;
    u16 candidateSlot;

    if (playerStarterSlot >= ARRAY_COUNT(sPlayerStarterSpecies))
        playerStarterSlot = 0;

    // Preserve the original game when the starter randomizer is off.
    if (!RandomizerFeatureEnabled(RANDOMIZE_STARTER_AND_GIFT_MON))
        return (playerStarterSlot == 0) ? 2 : (playerStarterSlot == 1 ? 0 : 1);

    bestSpecies = SPECIES_NONE;
    bestSlot = 0;
    for (candidateSlot = 0; candidateSlot < ARRAY_COUNT(sPlayerStarterSpecies); candidateSlot++)
    {
        if (candidateSlot == playerStarterSlot)
            continue;

        candidateSpecies = GetRandomizedStarterSpecies(candidateSlot);
        if (bestSpecies == SPECIES_NONE
            || GetSpeciesBaseStatTotal(candidateSpecies) > GetSpeciesBaseStatTotal(bestSpecies))
        {
            bestSpecies = candidateSpecies;
            bestSlot = candidateSlot;
        }
    }

    return bestSlot;
}

u16 GetRivalStarterSpecies(u16 playerStarterSlot)
{
    if (!RandomizerFeatureEnabled(RANDOMIZE_STARTER_AND_GIFT_MON))
    {
        static const u16 sOriginalRivalSpecies[] =
        {
            SPECIES_CHARMANDER,
            SPECIES_BULBASAUR,
            SPECIES_SQUIRTLE,
        };
        if (playerStarterSlot >= ARRAY_COUNT(sOriginalRivalSpecies))
            playerStarterSlot = 0;
        return sOriginalRivalSpecies[playerStarterSlot];
    }
    return GetRandomizedStarterSpecies(GetRivalStarterSlot(playerStarterSlot));
}

enum
{
    RIVAL_ROLE_STARTER,
    RIVAL_ROLE_BIRD,
    RIVAL_ROLE_PSYCHIC,
    RIVAL_ROLE_RAT,
    RIVAL_ROLE_RHYHORN,
    RIVAL_ROLE_GROWLITHE,
    RIVAL_ROLE_EXEGGCUTE,
    RIVAL_ROLE_GYARADOS,
    RIVAL_ROLE_INVALID = 0xFF,
};

static u8 GetRivalRosterRole(u16 species)
{
    switch (species)
    {
    case SPECIES_BULBASAUR:
    case SPECIES_IVYSAUR:
    case SPECIES_VENUSAUR:
    case SPECIES_SQUIRTLE:
    case SPECIES_WARTORTLE:
    case SPECIES_BLASTOISE:
    case SPECIES_CHARMANDER:
    case SPECIES_CHARMELEON:
    case SPECIES_CHARIZARD:
        return RIVAL_ROLE_STARTER;
    case SPECIES_PIDGEY:
    case SPECIES_PIDGEOTTO:
    case SPECIES_PIDGEOT:
        return RIVAL_ROLE_BIRD;
    case SPECIES_ABRA:
    case SPECIES_KADABRA:
    case SPECIES_ALAKAZAM:
        return RIVAL_ROLE_PSYCHIC;
    case SPECIES_RATTATA:
    case SPECIES_RATICATE:
        return RIVAL_ROLE_RAT;
    case SPECIES_RHYHORN:
    case SPECIES_RHYDON:
        return RIVAL_ROLE_RHYHORN;
    case SPECIES_GROWLITHE:
    case SPECIES_ARCANINE:
        return RIVAL_ROLE_GROWLITHE;
    case SPECIES_EXEGGCUTE:
    case SPECIES_EXEGGUTOR:
        return RIVAL_ROLE_EXEGGCUTE;
    case SPECIES_GYARADOS:
        return RIVAL_ROLE_GYARADOS;
    default:
        return RIVAL_ROLE_INVALID;
    }
}

static u16 GetRivalNonLevelEvolution(u16 species, u8 role)
{
    const struct Evolution *evolutions = GetSpeciesEvolutions(species);
    u16 candidates[8];
    u8 count = 0;
    u8 i;
    struct Sfc32State state;

    for (i = 0; evolutions[i].method != EVOLUTIONS_END && count < ARRAY_COUNT(candidates); i++)
    {
        if (evolutions[i].method == EVO_ITEM || evolutions[i].method == EVO_TRADE)
            candidates[count++] = evolutions[i].targetSpecies;
    }

    if (count == 0)
        return SPECIES_NONE;

    state = RandomizerRandSeed(RANDOMIZER_REASON_TRAINER_PARTY, 0x45564F00 | role, species);
    return candidates[RandomizerNextRange(&state, count)];
}

static u8 GetRivalEncounterStage(u16 trainerId)
{
    if (trainerId >= TRAINER_RIVAL_OAKS_LAB_SQUIRTLE && trainerId <= TRAINER_RIVAL_OAKS_LAB_CHARMANDER)
        return 0;
    if (trainerId >= TRAINER_RIVAL_ROUTE22_EARLY_SQUIRTLE && trainerId <= TRAINER_RIVAL_ROUTE22_EARLY_CHARMANDER)
        return 1;
    if (trainerId >= TRAINER_RIVAL_CERULEAN_SQUIRTLE && trainerId <= TRAINER_RIVAL_CERULEAN_CHARMANDER)
        return 2;
    if (trainerId >= TRAINER_RIVAL_SS_ANNE_SQUIRTLE && trainerId <= TRAINER_RIVAL_SS_ANNE_CHARMANDER)
        return 3;
    if (trainerId >= TRAINER_RIVAL_POKEMON_TOWER_SQUIRTLE && trainerId <= TRAINER_RIVAL_POKEMON_TOWER_CHARMANDER)
        return 4;
    if (trainerId >= TRAINER_RIVAL_SILPH_SQUIRTLE && trainerId <= TRAINER_RIVAL_SILPH_CHARMANDER)
        return 5;
    if (trainerId >= TRAINER_RIVAL_ROUTE22_LATE_SQUIRTLE && trainerId <= TRAINER_RIVAL_ROUTE22_LATE_CHARMANDER)
        return 6;
    if (trainerId >= TRAINER_CHAMPION_FIRST_SQUIRTLE && trainerId <= TRAINER_CHAMPION_FIRST_CHARMANDER)
        return 7;
    return 0xFF;
}

static bool8 HasRivalReachedSecondOccurrence(u8 role, u16 trainerId)
{
    u8 stage = GetRivalEncounterStage(trainerId);

    if (stage == 0xFF)
        return FALSE;

    switch (role)
    {
    case RIVAL_ROLE_STARTER:
        return stage >= 1;
    case RIVAL_ROLE_BIRD:
    case RIVAL_ROLE_PSYCHIC:
    case RIVAL_ROLE_RAT:
        return stage >= (role == RIVAL_ROLE_BIRD ? 2 : 3);
    case RIVAL_ROLE_RHYHORN:
        return stage >= 7;
    case RIVAL_ROLE_GROWLITHE:
    case RIVAL_ROLE_EXEGGCUTE:
    case RIVAL_ROLE_GYARADOS:
        return stage >= 5;
    default:
        return FALSE;
    }
}

static u16 GetRivalSpeciesAtLevel(u16 species, u8 level, bool8 forceNonLevelEvolution, u8 role)
{
    struct Pokemon mon;
    u16 evolvedSpecies;
    u8 evolutionCount = 0;

    // Reuse the game's evolution rules for level-based evolutions. Trainer
    // Pokémon do not have an inventory or a trade partner, so item/trade
    // evolutions are applied separately when this roster role appears again.
    CreateMon(&mon, species, level, 0, TRUE, 0, OT_ID_RANDOM_NO_SHINY, 0);
    while (evolutionCount++ < 10)
    {
        evolvedSpecies = GetEvolutionTargetSpecies(&mon, EVO_MODE_NORMAL, ITEM_NONE, NULL, NULL, CHECK_EVO);
        if (evolvedSpecies == SPECIES_NONE || evolvedSpecies == species)
            break;
        species = evolvedSpecies;
        CreateMon(&mon, species, level, 0, TRUE, 0, OT_ID_RANDOM_NO_SHINY, 0);
    }
    if (forceNonLevelEvolution)
    {
        evolvedSpecies = GetRivalNonLevelEvolution(species, role);
        if (evolvedSpecies != SPECIES_NONE)
            species = evolvedSpecies;
    }

    return species;
}

u16 GetRivalTrainerSpecies(u16 originalSpecies, u8 level, u16 playerStarterSlot, u16 trainerId)
{
    u8 role;
    u16 species;

    if (!RandomizerFeatureEnabled(RANDOMIZE_TRAINER_MON))
        return originalSpecies;

    role = GetRivalRosterRole(originalSpecies);
    if (role == RIVAL_ROLE_INVALID)
        return originalSpecies;

    if (role == RIVAL_ROLE_STARTER)
    {
        if (!RandomizerFeatureEnabled(RANDOMIZE_STARTER_AND_GIFT_MON))
            return originalSpecies;
        species = GetRivalStarterSpecies(playerStarterSlot);
    }
    else
    {
        if (sLastRivalRosterSeed != GetRandomizerSeed() || sRivalRosterSpecies[1] == SPECIES_NONE)
        {
            GetUniqueMonList(RANDOMIZER_REASON_TRAINER_PARTY,
                             MON_RANDOM,
                             0x5249564C, // "RIVL"
                             0,
                             ARRAY_COUNT(sRivalRosterOriginalSpecies),
                             sRivalRosterOriginalSpecies,
                             sRivalRosterSpecies);
            sLastRivalRosterSeed = GetRandomizerSeed();
        }
        species = sRivalRosterSpecies[role];
    }

    return GetRivalSpeciesAtLevel(species, level, HasRivalReachedSecondOccurrence(role, trainerId), role);
}

EWRAM_DATA static u32 sLastEggMonRandomizerSeed = 0;
EWRAM_DATA static u16 sRandomizedEggMons[EGG_MON_COUNT] = {0};

u16 RandomizeEggMon(u16 originalSlot, const u16* originalEggMons)
{
    /* Validate the slot index */
    if (originalSlot >= EGG_MON_COUNT)
    {
        MgbaPrintf(MGBA_LOG_DEBUG,
                   "EggRand: Slot %d out of range (max %d), returning original",
                   originalSlot, EGG_MON_COUNT - 1);
        return originalEggMons[originalSlot];
    }

    if (RandomizerFeatureEnabled(RANDOMIZE_EGG_MON))
    {
        if (sLastEggMonRandomizerSeed != GetRandomizerSeed()
            || sRandomizedEggMons[0] == SPECIES_NONE)
        {
            u32 eggHash = 5381;
            for (u32 i = 0; i < EGG_MON_COUNT; i++)
            {
                u16 originalEgg = originalEggMons[i];
                eggHash = ((eggHash << 5) + eggHash) ^ (u8)originalEgg;
                eggHash = ((eggHash << 5) + eggHash) ^ (u8)(originalEgg >> 8);
            }

            GetUniqueMonList(RANDOMIZER_REASON_EGG,
                              GetRandomizerOption(RANDOMIZER_OPTION_SPECIES_MODE),
                              eggHash, 0,
                              EGG_MON_COUNT,
                              originalEggMons,
                              sRandomizedEggMons);

            // Cache the seed used for this table
            sLastEggMonRandomizerSeed = GetRandomizerSeed();
        }
        return sRandomizedEggMons[originalSlot];
    }

    return originalEggMons[originalSlot];
}

// Ability assignment is keyed only by species and seed, so every instance of a
// species gets the same result regardless of its normal ability slot.
u16 RandomizeAbility(u16 species, u16 originalAbility)
{
    if (RandomizerFeatureEnabled(RANDOMIZE_ABILITIES) && originalAbility != ABILITY_NONE)
    {
        struct Sfc32State state;

        // The randomizer seed and species form a stable per-species assignment.
        state = RandomizerRandSeed(RANDOMIZER_REASON_ABILITIES, species, 0);
        // Keep all defined abilities eligible, including Wonder Guard.
        return sRandomizerAbilityWhitelist[RandomizerNextRange(&state, ABILITY_WHITELIST_SIZE)];
    }

    return originalAbility;
}

// A single small cache keeps consumers that expect a pointer-based learnset API
// compatible with seeded randomization while avoiding a large per-species RAM table.
EWRAM_DATA static struct LevelUpMove sRandomizedLevelUpLearnset[MAX_LEVEL_UP_MOVES + 1];
EWRAM_DATA static u16 sRandomizedLevelUpLearnsetSpecies = SPECIES_NONE;
EWRAM_DATA static u32 sRandomizedLevelUpLearnsetSeed = 0;

const struct LevelUpMove *RandomizeLearnset(u16 species, const struct LevelUpMove *originalLearnset)
{
    struct Sfc32State state;
    u32 seed = GetRandomizerSeed();
    u32 i, j;

    if (!RandomizerFeatureEnabled(RANDOMIZE_LEARNSET) || originalLearnset == NULL)
        return originalLearnset;

    if (sRandomizedLevelUpLearnsetSpecies == species
        && sRandomizedLevelUpLearnsetSeed == seed)
        return sRandomizedLevelUpLearnset;

    // Preserve the species' move-learning levels and replace only the move IDs.
    // Rejected duplicates ensure no species learns a generated move twice.
    state = RandomizerRandSeed(RANDOMIZER_REASON_LEARNSET, species, 0);
    for (i = 0; i < MAX_LEVEL_UP_MOVES && originalLearnset[i].move != LEVEL_UP_MOVE_END; i++)
    {
        u16 move;
        bool32 duplicate;

        do
        {
            move = RandomizerNextRange(&state, MOVES_COUNT);
            duplicate = (move == MOVE_NONE || move == MOVE_STRUGGLE);
            for (j = 0; !duplicate && j < i; j++)
            {
                if (sRandomizedLevelUpLearnset[j].move == move)
                    duplicate = TRUE;
            }
        } while (duplicate);

        sRandomizedLevelUpLearnset[i].move = move;
        sRandomizedLevelUpLearnset[i].level = originalLearnset[i].level;
    }
    sRandomizedLevelUpLearnset[i].move = LEVEL_UP_MOVE_END;
    sRandomizedLevelUpLearnset[i].level = LEVEL_UP_MOVE_END;
    sRandomizedLevelUpLearnsetSpecies = species;
    sRandomizedLevelUpLearnsetSeed = seed;
    return sRandomizedLevelUpLearnset;
}

#endif // RANDOMIZER_AVAILABLE
