#ifndef GUARD_AVATAR_H
#define GUARD_AVATAR_H

enum AvatarLook
{
    AVATAR_RED,
    AVATAR_LEAF,
    AVATAR_BRENDAN,
    AVATAR_MAY,
    AVATAR_RS_BRENDAN,
    AVATAR_RS_MAY,
    AVATAR_LOOK_COUNT
};

u8 GetCurrentAvatarLook(void);
void SetCurrentAvatarLook(u8 look);
const u8 *GetAvatarLookName(u8 look);
const u8 *GetAvatarLookStyle(u8 look);
u8 GetAvatarGraphicsId(u8 look, u8 state);
u8 GetAvatarBikeVsSeekerGraphicsId(u8 look);
u16 GetAvatarFrontPic(u8 look);
u16 GetCurrentAvatarFrontPic(void);
u16 GetCurrentAvatarBackPic(void);
void ApplyAvatarLookToField(u8 look);

#endif
