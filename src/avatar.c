#include "global.h"
#include "avatar.h"
#include "event_data.h"
#include "event_object_movement.h"
#include "field_player_avatar.h"
#include "constants/event_objects.h"
#include "constants/trainers.h"
#include "constants/vars.h"

static const u8 sNames[AVATAR_LOOK_COUNT][12] = {
    _("Red"), _("Leaf"), _("Brendan"), _("May"), _("Cody"), _("Ben"), _("Brandon")
};
static const u8 sStyles[AVATAR_LOOK_COUNT][20] = {
    _("FireRed"), _("LeafGreen"), _("Emerald"), _("Emerald"), _("Quantum"), _("Quantum"), _("Quantum")
};
static const u16 sFrontPics[AVATAR_LOOK_COUNT] = {
    TRAINER_PIC_RED, TRAINER_PIC_LEAF, TRAINER_PIC_QUANTUM_BRENDAN,
    TRAINER_PIC_QUANTUM_MAY, TRAINER_PIC_QUANTUM_CODY, TRAINER_PIC_QUANTUM_BEN, TRAINER_PIC_QUANTUM_BRANDON
};
static const u16 sBackPics[AVATAR_LOOK_COUNT] = {
    TRAINER_BACK_PIC_RED, TRAINER_BACK_PIC_LEAF, TRAINER_BACK_PIC_QUANTUM_BRENDAN,
    TRAINER_BACK_PIC_QUANTUM_MAY, TRAINER_BACK_PIC_QUANTUM_CODY, TRAINER_BACK_PIC_QUANTUM_BEN, TRAINER_BACK_PIC_QUANTUM_BRANDON
};

u8 GetCurrentAvatarLook(void)
{
    u16 saved = VarGet(VAR_PLAYER_AVATAR);
    // Leave retired Ruby/Sapphire values 5 and 6 available for migration.
    if (saved == 9)
        return AVATAR_BRANDON;
    if (saved == 8)
        return AVATAR_BEN;
    if (saved == 7)
        return AVATAR_CODY;
    // Values 5 and 6 were Ruby/Sapphire looks; migrate to Emerald counterparts.
    if (saved == 5 || saved == 6)
    {
        saved -= 2;
        VarSet(VAR_PLAYER_AVATAR, saved);
    }
    // Zero is the legacy-save default. Gender and OT data stay independent.
    if (saved == 0 || saved > 4)
        return gSaveBlock2Ptr->playerGender == FEMALE ? AVATAR_LEAF : AVATAR_RED;
    return saved - 1;
}

void SetCurrentAvatarLook(u8 look)
{
    if (look < AVATAR_LOOK_COUNT)
        VarSet(VAR_PLAYER_AVATAR, look == AVATAR_BRANDON ? 9 : look == AVATAR_BEN ? 8 : look == AVATAR_CODY ? 7 : look + 1);
}

const u8 *GetAvatarLookName(u8 look)
{
    return sNames[look < AVATAR_LOOK_COUNT ? look : AVATAR_RED];
}

const u8 *GetAvatarLookStyle(u8 look)
{
    return sStyles[look < AVATAR_LOOK_COUNT ? look : AVATAR_RED];
}

u8 GetAvatarGraphicsId(u8 look, u8 state)
{
    u8 slot;
    switch (state)
    {
    case PLAYER_AVATAR_STATE_MACH_BIKE:
    case PLAYER_AVATAR_STATE_ACRO_BIKE: slot = 1; break;
    case PLAYER_AVATAR_STATE_SURFING: slot = 2; break;
    case PLAYER_AVATAR_STATE_FIELD_MOVE:
    case PLAYER_AVATAR_STATE_WATERING: slot = 3; break;
    case PLAYER_AVATAR_STATE_FISHING: slot = 4; break;
    case PLAYER_AVATAR_STATE_VSSEEKER: slot = 5; break;
    default: slot = 0; break;
    }
    if (look >= AVATAR_LOOK_COUNT)
        look = AVATAR_RED;
    if (look <= AVATAR_LEAF)
        return look * 7 + slot;
    if (look == AVATAR_BRANDON)
        return OBJ_EVENT_GFX_AVATAR_BRANDON_NORMAL + slot;
    if (look == AVATAR_BEN)
        return OBJ_EVENT_GFX_AVATAR_BEN_NORMAL + slot;
    if (look == AVATAR_CODY)
        return OBJ_EVENT_GFX_AVATAR_CODY_NORMAL + slot;
    return OBJ_EVENT_GFX_AVATAR_BRENDAN_NORMAL + (look - AVATAR_BRENDAN) * 7 + slot;
}

u8 GetAvatarBikeVsSeekerGraphicsId(u8 look)
{
    if (look >= AVATAR_LOOK_COUNT)
        look = AVATAR_RED;
    if (look <= AVATAR_LEAF)
        return look * 7 + 6;
    if (look == AVATAR_BRANDON)
        return OBJ_EVENT_GFX_AVATAR_BRANDON_VSSEEKERBIKE;
    if (look == AVATAR_BEN)
        return OBJ_EVENT_GFX_AVATAR_BEN_VSSEEKERBIKE;
    if (look == AVATAR_CODY)
        return OBJ_EVENT_GFX_AVATAR_CODY_VSSEEKERBIKE;
    return OBJ_EVENT_GFX_AVATAR_BRENDAN_NORMAL + (look - AVATAR_BRENDAN) * 7 + 6;
}

u16 GetAvatarFrontPic(u8 look)
{
    return sFrontPics[look < AVATAR_LOOK_COUNT ? look : AVATAR_RED];
}

u16 GetCurrentAvatarFrontPic(void)
{
    return GetAvatarFrontPic(GetCurrentAvatarLook());
}

u16 GetCurrentAvatarBackPic(void)
{
    return sBackPics[GetCurrentAvatarLook()];
}
