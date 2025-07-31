#include "global.h"
#include "pokemon.h"
#include "constants/species.h"
#include "data/pokemon/species_info.h"

#define MAX_VALID_SPECIES 1600 // Set higher than your max species ID
static u16 sValidSpecies[MAX_VALID_SPECIES];
static u16 sNumValidSpecies = 0;
static bool8 sSpeciesListInitialized = FALSE;

// List of allowed species for randomization.
// You can customize this to include or exclude anything you want.
static void InitValidSpeciesList(void)
{
    if (sSpeciesListInitialized)
        return;

    // You can skip fakes or forms by excluding their ranges here

    for (u16 i = SPECIES_BULBASAUR; i <= SPECIES_ENAMORUS_INCARNATE; i++)
        sValidSpecies[sNumValidSpecies++] = i;

    for (u16 i = SPECIES_RATTATA_ALOLA; i <= SPECIES_DECIDUEYE_HISUI; i++)
        sValidSpecies[sNumValidSpecies++] = i;

    for (u16 i = SPECIES_SPRIGATITO; i <= SPECIES_PECHARUNT; i++)
        sValidSpecies[sNumValidSpecies++] = i;

    // Manually include additional mons if needed
    //sValidSpecies[sNumValidSpecies++] = SPECIES_MIRAIDON;

    sSpeciesListInitialized = TRUE;
}

// This function takes the saved seed, map location, and encounter slot,
// and returns a randomized (but deterministic) Pokémon species.
u16 GetRandomisedSpecies(u32 seed, u16 mapGroup, u16 mapNum, u8 slot)
{
    InitValidSpeciesList();

    u32 x = seed ^ ((mapGroup << 16) | mapNum) ^ slot;
    x = (x * 0x41C64E6D + 0x6073) >> 16;

    return sValidSpecies[x % sNumValidSpecies];
}


