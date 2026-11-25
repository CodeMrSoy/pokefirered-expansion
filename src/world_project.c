#include "global.h"
#include "adventure_mode.h"
#include "battle.h"
#include "caps.h"
#include "event_data.h"
#include "difficulty.h"
#include "random.h"
#include "game_modes.h"
#include "main.h"
#include "pokemon.h"
#include "quantum_cleanup.h"
#include "randomizer.h"
#include "wild_encounter.h"
#include "world_project.h"
#include "world_export.h"
#include "constants/maps.h"
#include "constants/opponents.h"

#define PROJECT_MAGIC 0x3132574C // LW21
#define PROJECT_VERSION 1
#define PROJECT_FRESH_FRAMES 120
#define PROJECT_TRAINER 1
#define PROJECT_LAND 2
#define PROJECT_LIMIT 6
#define SAMMY_LEVEL_LIMIT 9
#define SAMMY_PARTY_LIMIT 2
#define LAND_OVERLAY_PERCENT 20

struct ProjectMon
{
    u32 identity;
    u16 species, ability;
    u16 moves[MAX_MON_MOVES];
    u8 level, abilitySlot, weight, reserved;
};

struct WorldProjectPort
{
    u32 magic, version, generation, counter, frame, seed, mode, modes, player;
    u32 keyA, keyB, revision, kind, map, variant, count, checksum;
    struct ProjectMon mons[PROJECT_LIMIT];
};

STATIC_ASSERT(sizeof(struct ProjectMon) == 20, ProjectMonAbi);
STATIC_ASSERT(sizeof(struct WorldProjectPort) == 188, ProjectPortAbi);
EWRAM_DATA volatile struct
{
    struct WorldProjectPort offer;
    u32 nativeSeal;
} gWorldProjectPort = {0};
static EWRAM_DATA u32 sGeneration = 0;
static EWRAM_DATA u32 sKind = 0;
static EWRAM_DATA u32 sRevision = 0;
static EWRAM_DATA u32 sSelection = 0;
static EWRAM_DATA u32 sConsumedRareTag = 0;
static EWRAM_DATA u8 sConsumedRareNonce = 0;
static EWRAM_DATA u32 sRejectKind = 0;
static EWRAM_DATA u32 sRejectRevision = 0;
static EWRAM_DATA u32 sRejectReason = 0;
extern u32 gSaveCounter;

static u32 CurrentMap(void)
{
    return ((u8)gSaveBlock1Ptr->location.mapGroup << 8) | (u8)gSaveBlock1Ptr->location.mapNum;
}

void WorldProject_Reset(u32 generation)
{
    gWorldProjectPort.offer.magic = 0;
    gWorldProjectPort.nativeSeal = 0x215EA1AB ^ (u32)&gWorldProjectPort;
    sGeneration = generation;
    sKind = 0;
    sConsumedRareTag = 0;
    sRejectKind = 0;
}

static bool32 Reject(u32 kind, u32 reason)
{
    sRejectKind = kind;
    sRejectRevision = gWorldProjectPort.offer.revision;
    sRejectReason = reason;
    return FALSE;
}

static bool32 Read(struct WorldProjectPort *packet, u32 kind, u32 limit)
{
    u32 i, player, check = 2166136261u;
    const u8 *bytes = (const u8 *)packet;

    if (gWorldProjectPort.offer.magic != PROJECT_MAGIC || gWorldProjectPort.offer.kind != kind)
        return FALSE;
    *packet = gWorldProjectPort.offer;
    memcpy(&player, gSaveBlock2Ptr->playerTrainerId, sizeof(player));
    u32 mode = AdventureMode_Get() | (GetRandomizerOption(RANDOMIZER_OPTION_SPECIES_MODE) << 8)
             | (GetCurrentDifficultyLevel() << 16);
    if (packet->version != PROJECT_VERSION || !sGeneration || packet->generation != sGeneration
     || packet->counter != gSaveCounter || packet->player != player || packet->mode != mode
     || packet->seed != GetRandomizerSeed()
     || packet->modes != (gSaveBlock2Ptr->gameModes | WorldExport_Features() << 8)
     || packet->map != CurrentMap())
        return Reject(kind, 1);
    if (gMain.vblankCounter1 - packet->frame > PROJECT_FRESH_FRAMES)
        return Reject(kind, 2);
    if (!packet->keyA || !packet->keyB || !packet->revision || !packet->count || packet->count > limit)
        return Reject(kind, 3);
    for (i = sizeof(packet->magic); i < sizeof(*packet); i++)
    {
        if (i < offsetof(struct WorldProjectPort, checksum) || i >= offsetof(struct WorldProjectPort, mons))
            check = (check ^ bytes[i]) * 16777619u;
    }
    return check == packet->checksum || Reject(kind, 4);
}

static bool32 AllowedSpecies(u16 species)
{
    if (!species || species == SPECIES_UNOWN || species >= NUM_SPECIES || !IsSpeciesEnabled(species)
     || QuantumCanonicalSpecies(species) != species)
        return FALSE;
    const struct SpeciesInfo *info = &gSpeciesInfo[species];
    return !(info->isLegendary || info->isMythical || info->isUltraBeast || info->isParadox
             || info->isMegaEvolution || info->isPrimalReversion || info->isUltraBurst
             || info->isGigantamax || info->isTeraForm);
}

static bool32 ValidTrainerMon(const struct ProjectMon *mon)
{
    u32 i, j, count = 0, cap = GetCurrentLevelCap();
    if (!mon->identity || mon->weight || mon->reserved || !AllowedSpecies(mon->species)
     || !mon->level || mon->level > SAMMY_LEVEL_LIMIT || (cap && mon->level > cap)
     || mon->abilitySlot >= NUM_ABILITY_SLOTS || !gSpeciesInfo[mon->species].abilities[mon->abilitySlot]
     || GetEffectiveAbilityBySpecies(mon->species, mon->abilitySlot, FALSE) != mon->ability)
        return FALSE;
    const struct LevelUpMove *learnset = GetSpeciesLevelUpLearnset(mon->species);
    for (i = 0; i < MAX_MON_MOVES; i++)
    {
        u16 move = mon->moves[i];
        if (!move)
            continue;
        if (i != count || move >= MOVES_COUNT)
            return FALSE;
        for (j = 0; j < i; j++)
            if (mon->moves[j] == move)
                return FALSE;
        for (j = 0; j < 256 && learnset[j].move != LEVEL_UP_MOVE_END; j++)
            if (learnset[j].move == move && learnset[j].level <= mon->level)
                break;
        if (j == 256 || learnset[j].move == LEVEL_UP_MOVE_END)
            return FALSE;
        count++;
    }
    return count != 0;
}

bool32 WorldProject_Trainer(struct Pokemon *party, u16 trainer, bool32 first)
{
    struct WorldProjectPort packet;
    u32 i, j;
    if (!first || party != gEnemyParty || trainer != TRAINER_BUG_CATCHER_SAMMY
     || CurrentMap() != MAP_VIRIDIAN_FOREST
     || (gBattleTypeFlags & ~BATTLE_TYPE_IS_MASTER) != BATTLE_TYPE_TRAINER
     || !Read(&packet, PROJECT_TRAINER, SAMMY_PARTY_LIMIT) || packet.variant != trainer)
        return FALSE;
    for (i = 0; i < packet.count; i++)
    {
        if (!ValidTrainerMon(&packet.mons[i]))
            return Reject(PROJECT_TRAINER, 5);
        for (j = 0; j < i; j++)
            if (packet.mons[j].identity == packet.mons[i].identity)
                return Reject(PROJECT_TRAINER, 5);
    }

    ZeroEnemyPartyMons();
    for (i = 0; i < packet.count; i++)
    {
        const struct ProjectMon *mon = &packet.mons[i];
        u32 ot = mon->identity ^ 0x5A000000u;
        CreateMon(&party[i], mon->species, mon->level, 0, TRUE, mon->identity, OT_ID_PRESET, ot);
        SetMonData(&party[i], MON_DATA_ABILITY_NUM, &mon->abilitySlot);
        for (j = 0; j < MAX_MON_MOVES; j++)
            SetMonMoveSlot(&party[i], mon->moves[j], j);
    }
    sKind = PROJECT_TRAINER;
    sRevision = packet.revision;
    sSelection = packet.count;
    return TRUE;
}

static bool32 RareUnavailable(const struct ProjectMon *mon, u8 level)
{
    return mon->level != level || (mon->identity == sConsumedRareTag && mon->reserved == sConsumedRareNonce);
}

u16 WorldProject_Land(u32 variant, u16 species, u8 level, u8 slot, u32 *identity)
{
    struct WorldProjectPort packet;
    u32 i, total = 0, roll, rare = 0;
    if ((CurrentMap() != MAP_ROUTE24 && CurrentMap() != MAP_ROUTE25) || variant >= 32
     || !Read(&packet, PROJECT_LAND, PROJECT_LIMIT) || !(packet.variant & (1u << variant)))
        return species;
    for (i = 0; i < packet.count; i++)
    {
        const struct ProjectMon *mon = &packet.mons[i];
        if (!AllowedSpecies(mon->species) || !mon->weight || mon->weight > 25
         || mon->ability || mon->abilitySlot
         || mon->moves[0] || mon->moves[1] || mon->moves[2] || mon->moves[3])
        {
            Reject(PROJECT_LAND, 5);
            return species;
        }
        if (mon->identity)
        {
            if (++rare > 1 || mon->weight > 4 || !mon->reserved || !mon->level || mon->level > 15)
                return species;
            if (RareUnavailable(mon, level))
                continue;
        }
        else if (mon->level || mon->reserved)
            return species;
        total += mon->weight;
    }
    if (!total)
        return species;
    // Keep the native RNG cursor unchanged. The already drawn encounter
    // slot and RNG state select a small overlay share of ordinary spawns.
    rng_value_t entropy = gRngValue;
    roll = LocalRandom32(&entropy) ^ (slot * 0x9E3779B9u);
    roll ^= roll >> 16;
    roll *= 0x7FEB352Du;
    roll ^= roll >> 15;
    if (roll % 100 >= LAND_OVERLAY_PERCENT)
        return species;
    roll = (roll / 100) % total;
    for (i = 0; i < packet.count; i++)
    {
        const struct ProjectMon *mon = &packet.mons[i];
        if (mon->identity && RareUnavailable(mon, level))
            continue;
        if (roll < mon->weight)
        {
            if (mon->identity)
            {
                *identity = mon->identity;
                sConsumedRareTag = mon->identity;
                sConsumedRareNonce = mon->reserved;
            }
            sKind = PROJECT_LAND;
            sRevision = packet.revision;
            sSelection = i;
            return mon->species;
        }
        roll -= mon->weight;
    }
    return species;
}

void WorldProject_BattleStart(u32 flags, u16 trainer, u32 *kind, u32 *revision, u32 *selection)
{
    if ((sKind == PROJECT_TRAINER && trainer == TRAINER_BUG_CATCHER_SAMMY
        && (flags & ~BATTLE_TYPE_IS_MASTER) == BATTLE_TYPE_TRAINER)
     || (sKind == PROJECT_LAND && (flags & ~BATTLE_TYPE_IS_MASTER) == 0))
    {
        *kind = sKind;
        *revision = sRevision;
        *selection = sSelection;
    }
    else if ((sRejectKind == PROJECT_TRAINER && trainer == TRAINER_BUG_CATCHER_SAMMY
              && (flags & ~BATTLE_TYPE_IS_MASTER) == BATTLE_TYPE_TRAINER)
          || (sRejectKind == PROJECT_LAND && (flags & ~BATTLE_TYPE_IS_MASTER) == 0))
    {
        *kind = sRejectKind | 0x100;
        *revision = sRejectRevision;
        *selection = sRejectReason;
    }
    sKind = 0;
    sRejectKind = 0;
}
