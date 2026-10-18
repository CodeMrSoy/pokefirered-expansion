#include "global.h"
#include "avatar.h"
#include "event_data.h"
#include "event_object_movement.h"
#include "field_player_avatar.h"
#include "constants/event_objects.h"
#include "constants/trainers.h"
#include "constants/vars.h"

static const u8 sNames[AVATAR_LOOK_COUNT][12] = {
    _("Red"), _("Leaf"), _("Brendan"), _("May")
};
static const u8 sStyles[AVATAR_LOOK_COUNT][20] = {
    _("FireRed"), _("LeafGreen"), _("Emerald"), _("Emerald")
};
static const u16 sFrontPics[AVATAR_LOOK_COUNT] = {
    TRAINER_PIC_RED, TRAINER_PIC_LEAF, TRAINER_PIC_QUANTUM_BRENDAN,
    TRAINER_PIC_QUANTUM_MAY
};
static const u16 sBackPics[AVATAR_LOOK_COUNT] = {
    TRAINER_BACK_PIC_RED, TRAINER_BACK_PIC_LEAF, TRAINER_BACK_PIC_QUANTUM_BRENDAN,
    TRAINER_BACK_PIC_QUANTUM_MAY
};

u8 GetCurrentAvatarLook(void)
{
    u16 saved = VarGet(VAR_PLAYER_AVATAR);
    // Values 5 and 6 were Ruby/Sapphire looks; migrate to Emerald counterparts.
    if (saved == 5 || saved == 6)
    {
        saved -= 2;
        VarSet(VAR_PLAYER_AVATAR, saved);
    }
    // Zero is the legacy-save default. Gender and OT data stay independent.
    if (saved == 0 || saved > AVATAR_LOOK_COUNT)
        return gSaveBlock2Ptr->playerGender == FEMALE ? AVATAR_LEAF : AVATAR_RED;
    return saved - 1;
}

void SetCurrentAvatarLook(u8 look)
{
    if (look < AVATAR_LOOK_COUNT)
        VarSet(VAR_PLAYER_AVATAR, look + 1);
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
    return OBJ_EVENT_GFX_AVATAR_BRENDAN_NORMAL + (look - AVATAR_BRENDAN) * 7 + slot;
}

u8 GetAvatarBikeVsSeekerGraphicsId(u8 look)
{
    if (look >= AVATAR_LOOK_COUNT)
        look = AVATAR_RED;
    if (look <= AVATAR_LEAF)
        return look * 7 + 6;
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

void ApplyAvatarLookToField(u8 look)
{
    SetCurrentAvatarLook(look);
    ObjectEventSetGraphicsId(&gObjectEvents[gPlayerAvatar.objectEventId], GetPlayerAvatarGraphicsIdByCurrentState());
}
