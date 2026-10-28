#include "global.h"
#include "battle.h"
#include "event_data.h"
#include "caps.h"
#include "pokemon.h"
#include "constants/opponents.h"
#include "constants/vars.h"



u32 GetCurrentLevelCap(void)
{
    // Vidra uses the same five crest bits shown on the Trainer Card.
    static const struct
    {
        u16 flag;
        u8 crest;
        u8 cap;
    } sLevelCapMilestones[] =
    {
        {FLAG_BADGE01_GET, 0, 14},
        {FLAG_BADGE02_GET, 0, 21},
        {FLAG_BADGE03_GET, 0, 24},
        {FLAG_BADGE04_GET, 0, 29},
        {FLAG_BADGE05_GET, 0, 35},
        {TRAINER_FLAGS_START + TRAINER_HAVORA_CAPTAIN, 1 << 0, 46},
        {FLAG_BADGE06_GET, 0, 50},
        {0, 1 << 1, 57}, // Corvala
        {FLAG_BADGE07_GET, 0, 63},
        {0, 1 << 2, 68}, // Eldervale: Brandon
        {0, 1 << 3, 73}, // Myrdal: Ben
        {0, 1 << 4, 79}, // Iskora: Cody
        {FLAG_BADGE08_GET, 0, 82},
        {FLAG_SYS_GAME_CLEAR, 0, 90},
    };

    u32 i;
    u16 crests;

    if (B_LEVEL_CAP_TYPE == LEVEL_CAP_FLAG_LIST)
    {
        // Completed saves remain uncapped, including saves from before the
        // additional Vidra Gym milestones existed.
        if (FlagGet(FLAG_SYS_GAME_CLEAR))
            return MAX_LEVEL;

        crests = VarGet(VAR_VIDRA_CRESTS);

        // Older Havora saves recorded the crest in the Gym progress variable.
        if (VarGet(VAR_HAVORA_GYM_PROGRESS) & 4)
            crests |= 1;

        for (i = 0; i < ARRAY_COUNT(sLevelCapMilestones); i++)
        {
            bool32 completed = sLevelCapMilestones[i].flag != 0
                && FlagGet(sLevelCapMilestones[i].flag);
            if (!completed && !(crests & sLevelCapMilestones[i].crest))
                return sLevelCapMilestones[i].cap;
        }
    }
    else if (B_LEVEL_CAP_TYPE == LEVEL_CAP_VARIABLE)
    {
        return VarGet(B_LEVEL_CAP_VARIABLE);
    }

    return MAX_LEVEL;
}

u32 GetSoftLevelCapExpValue(u32 level, u32 expValue)
{
    static const u32 sExpScalingDown[5] = { 4, 8, 16, 32, 64 };
    static const u32 sExpScalingUp[5]   = { 16, 8, 4, 2, 1 };

    u32 levelDifference;
    u32 currentLevelCap = GetCurrentLevelCap();

    if (B_EXP_CAP_TYPE == EXP_CAP_NONE)
        return expValue;

    if (level < currentLevelCap)
    {
        if (B_LEVEL_CAP_EXP_UP)
        {
            levelDifference = currentLevelCap - level;
            if (levelDifference > ARRAY_COUNT(sExpScalingUp) - 1)
                return expValue + (expValue / sExpScalingUp[ARRAY_COUNT(sExpScalingUp) - 1]);
            else
                return expValue + (expValue / sExpScalingUp[levelDifference]);
        }
        else
        {
            return expValue;
        }
    }
    else if (B_EXP_CAP_TYPE == EXP_CAP_HARD)
    {
        return 0;
    }
    else if (B_EXP_CAP_TYPE == EXP_CAP_SOFT)
    {
        levelDifference = level - currentLevelCap;
        if (levelDifference > ARRAY_COUNT(sExpScalingDown) - 1)
            return expValue / sExpScalingDown[ARRAY_COUNT(sExpScalingDown) - 1];
        else
            return expValue / sExpScalingDown[levelDifference];
    }
    else
    {
       return expValue;
    }
}

u32 GetCurrentEVCap(void)
{

    static const u16 sEvCapFlagMap[][2] = {
        // Define EV caps for each milestone
        {FLAG_BADGE01_GET, 30},
        {FLAG_BADGE02_GET, 90},
        {FLAG_BADGE03_GET, 150},
        {FLAG_BADGE04_GET, 210},
        {FLAG_BADGE05_GET, 270},
        {FLAG_BADGE06_GET, 330},
        {FLAG_BADGE07_GET, 390},
        {FLAG_BADGE08_GET, 450},
        {FLAG_SYS_GAME_CLEAR, MAX_TOTAL_EVS},
    };

    if (B_EV_CAP_TYPE == EV_CAP_FLAG_LIST)
    {
        for (u32 evCap = 0; evCap < ARRAY_COUNT(sEvCapFlagMap); evCap++)
        {
            if (!FlagGet(sEvCapFlagMap[evCap][0]))
                return sEvCapFlagMap[evCap][1];
        }
    }
    else if (B_EV_CAP_TYPE == EV_CAP_VARIABLE)
    {
        return VarGet(B_EV_CAP_VARIABLE);
    }
    else if (B_EV_CAP_TYPE == EV_CAP_NO_GAIN)
    {
        return 0;
    }

    return MAX_TOTAL_EVS;
}
