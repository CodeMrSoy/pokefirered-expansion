#include "global.h"
#include "adventure_mode.h"
#include "adventure_progression.h"
#include "wild_encounter.h"
#include "constants/opponents.h"
#include "data/adventure_levels.h"

u8 AdventureMode_TrainerLevel(u16 trainerId, u32 slot, u8 quantumLevel)
{
    const struct ClassicTrainerLevels *row;
    if (AdventureMode_IsQuantum() || trainerId >= TRAINERS_COUNT || slot >= PARTY_SIZE)
        return quantumLevel;
    row = &sClassicTrainerLevels[trainerId];
    // A custom facility/difficulty party must not be mistaken for this baseline.
    if (row->before[slot] && row->quantum[slot] == quantumLevel)
        return row->before[slot];
    return quantumLevel;
}

void AdventureMode_WildRange(const struct WildPokemon *table, u32 slot, u8 *min, u8 *max)
{
    u32 i;
    if (AdventureMode_IsQuantum())
        return;
    for (i = 0; i < ARRAY_COUNT(sClassicWildLevels); i++)
        if (sClassicWildLevels[i].table == table && slot < sClassicWildLevels[i].count)
        {
            *min = sClassicWildLevels[i].levels[slot][0];
            *max = sClassicWildLevels[i].levels[slot][1];
            return;
        }
}

u8 AdventureMode_ScriptedLevelForMap(u16 map, u16 species, u8 quantumLevel)
{
    if (AdventureMode_IsQuantum())
        return quantumLevel;
    // Relocated Kanto Articuno/Moltres already use level 50 in both modes.
    switch (map)
    {
    case MAP_ROUTE12:
    case MAP_ROUTE16:
        if (species == SPECIES_SNORLAX && quantumLevel == 22) return 30;
        break;
    case MAP_POWER_PLANT:
        if (species == SPECIES_ZAPDOS && quantumLevel == 57) return 50;
        if (species == SPECIES_ELECTRODE && quantumLevel == 41) return 34;
        break;
    }
    return quantumLevel;
}

u8 AdventureMode_ScriptedLevel(u16 species, u8 quantumLevel)
{
    u16 map = (u8)gSaveBlock1Ptr->location.mapNum | ((u8)gSaveBlock1Ptr->location.mapGroup << 8);
    return AdventureMode_ScriptedLevelForMap(map, species, quantumLevel);
}
