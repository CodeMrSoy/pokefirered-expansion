#include "global.h"
#include "game_modes.h"
#include "randomizer.h"
#include "constants/battle.h"
#include "constants/region_map_sections.h"
#include "constants/opponents.h"

STATIC_ASSERT(MAPSEC_COUNT <= NUZLOCKE_AREA_BYTES * 8, NuzlockeAreaCapacity);
STATIC_ASSERT(sizeof(((struct SaveBlock2 *)0)->filler_90) + 2 + NUZLOCKE_AREA_BYTES == 207, GameModesReservedSize);

static EWRAM_DATA bool8 sNuzlockeEncounterAllowed = FALSE;

void GameModes_EnsureInitialized(void)
{
    if (gSaveBlock2Ptr->gameModesVersion == GAME_MODE_VERSION)
        return;
    // These bytes were reserved padding. Legacy games keep their old behavior.
    gSaveBlock2Ptr->gameModesVersion = GAME_MODE_VERSION;
    gSaveBlock2Ptr->gameModes = GAME_MODE_LEVEL_CAPS;
    if (gSaveBlock2Ptr->randomizerSeed != 0)
        gSaveBlock2Ptr->gameModes |= GAME_MODE_RANDOM;
    memset(gSaveBlock2Ptr->nuzlockeAreas, 0, sizeof(gSaveBlock2Ptr->nuzlockeAreas));
}

bool32 GameModes_Enabled(u8 mode)
{
    GameModes_EnsureInitialized();
    return (gSaveBlock2Ptr->gameModes & mode) != 0;
}

void GameModes_Apply(void)
{
    GameModes_EnsureInitialized();
    gRandomizerEnabled = GameModes_Enabled(GAME_MODE_RANDOM);
    if (gRandomizerEnabled && gSaveBlock2Ptr->randomizerSeed == 0)
        gSaveBlock2Ptr->randomizerSeed = GenerateSeedForRandomizer();
    gCachedRandomizerSeed = gSaveBlock2Ptr->randomizerSeed;
    RandomizerApplyFeatureFlags();
}

void GameModes_Set(u8 mode, bool32 enabled)
{
    GameModes_EnsureInitialized();
    if (enabled)
        gSaveBlock2Ptr->gameModes |= mode;
    else
        gSaveBlock2Ptr->gameModes &= ~mode;
    GameModes_Apply();
}

void GameModes_NewGame(void)
{
    GameModes_EnsureInitialized();
    memset(gSaveBlock2Ptr->nuzlockeAreas, 0, sizeof(gSaveBlock2Ptr->nuzlockeAreas));
    sNuzlockeEncounterAllowed = TRUE;
    GameModes_Apply();
}

bool32 GameModes_PreserveGymTeam(u16 trainerId)
{
    // Current Vidra gym battles are the eight Havora trial/leader encounters.
    return trainerId >= TRAINER_HAVORA_DOCK_CREW && trainerId <= TRAINER_HAVORA_LOCKKEEPER
        && !GameModes_Enabled(GAME_MODE_VIDRA_GYMS);
}

void Nuzlocke_BeginEncounter(u16 area, u32 battleFlags)
{
    u8 mask;
    sNuzlockeEncounterAllowed = TRUE;
    if (!GameModes_Enabled(GAME_MODE_NUZLOCKE)
        || (battleFlags & (BATTLE_TYPE_TRAINER | BATTLE_TYPE_LINK | BATTLE_TYPE_RECORDED
            | BATTLE_TYPE_POKEDUDE | BATTLE_TYPE_OLD_MAN_TUTORIAL | BATTLE_TYPE_GHOST
            | BATTLE_TYPE_FRONTIER | BATTLE_TYPE_TRAINER_HILL | BATTLE_TYPE_EREADER_TRAINER)))
        return;
    if (area >= MAPSEC_COUNT || area == MAPSEC_NONE || area == MAPSEC_DYNAMIC)
    {
        sNuzlockeEncounterAllowed = FALSE;
        return;
    }
    mask = 1 << (area % 8);
    sNuzlockeEncounterAllowed = !(gSaveBlock2Ptr->nuzlockeAreas[area / 8] & mask);
    // Reserve on entry: fleeing, a KO or a failed capture still uses this area.
    gSaveBlock2Ptr->nuzlockeAreas[area / 8] |= mask;
}

bool32 Nuzlocke_CanCatch(void)
{
    return !GameModes_Enabled(GAME_MODE_NUZLOCKE) || sNuzlockeEncounterAllowed;
}

void Nuzlocke_RecordCatch(void)
{
    sNuzlockeEncounterAllowed = FALSE;
}
