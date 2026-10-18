#include "graphics/gimmicks.h"

// Gimmick data

const struct GimmickInfo gGimmicksInfo[GIMMICKS_COUNT] =
{
    [GIMMICK_NONE] = {0},
    [GIMMICK_MEGA] =
    {
        .triggerSheet = &sSpriteSheet_MegaTrigger,
        .triggerPal = &sSpritePalette_MegaTrigger,
        .triggerTemplate = &sSpriteTemplate_GimmickTrigger,
        .indicatorData = sMegaIndicatorGfx,
        .indicatorPalTag = TAG_MEGA_INDICATOR_PAL,
        .CanActivate = CanMegaEvolve,
        .ActivateGimmick = ActivateMegaEvolution,
    },
    [GIMMICK_Z_MOVE] = {0},
    [GIMMICK_ULTRA_BURST] = {0},
    [GIMMICK_DYNAMAX] = {0},
    [GIMMICK_TERA] = {0}
};
