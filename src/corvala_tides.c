#include "global.h"
#include "corvala_tides.h"
#include "field_camera.h"
#include "field_player_avatar.h"
#include "field_message_box.h"
#include "fieldmap.h"
#include "link.h"
#include "palette.h"
#include "quest_log.h"
#include "rtc.h"
#include "script.h"
#include "constants/maps.h"

struct CorvalaTideTile
{
    u8 x, y;
    u16 low, high;
};

#include "data/corvala_tides.h"

// All geometry stays in ROM; reuse the engine's existing virtual map buffer.
static EWRAM_DATA u8 sCorvalaTide = 0;
static EWRAM_DATA u8 sCorvalaTideTimer = 0;
extern const u8 Corvala_TideRisingWarning[];
extern const u8 Corvala_TideRecedingWarning[];

static bool32 IsCorvala(void)
{
    return gSaveBlock1Ptr->location.mapGroup == MAP_GROUP(MAP_CORVALA_TOWN)
        && gSaveBlock1Ptr->location.mapNum == MAP_NUM(MAP_CORVALA_TOWN);
}

static bool32 IsSafePosition(s16 x, s16 y)
{
    u32 index;
    if (x < 0 || y < 0 || x >= 64 || y >= 64)
        return FALSE;
    index = y * 64 + x;
    return (sCorvalaTideSafe[index / 8] >> (index % 8)) & 1;
}

static void ApplyTide(u8 high)
{
    u32 i;
    for (i = 0; i < ARRAY_COUNT(sCorvalaTideTiles); i++)
    {
        const struct CorvalaTideTile *tile = &sCorvalaTideTiles[i];
        MapGridSetMetatileEntryAt(tile->x + MAP_OFFSET, tile->y + MAP_OFFSET, high ? tile->high : tile->low);
    }
    sCorvalaTide = high;
}

void CorvalaTide_OnLoad(void)
{
    u8 high = GetCurrentHour() & 1;
    u32 i;
    if (!IsCorvala())
        return;
    if (!IsSafePosition(gSaveBlock1Ptr->pos.x, gSaveBlock1Ptr->pos.y))
    {
        // Loading a save after an hour boundary must not flood a walking
        // player or remove water beneath a surfer. Recover the saved phase
        // from the restored view, then warn and rescue on the next update.
        high = FALSE;
        for (i = 0; i < ARRAY_COUNT(sCorvalaTideTiles); i++)
        {
            const struct CorvalaTideTile *tile = &sCorvalaTideTiles[i];
            u32 offset = (tile->y + MAP_OFFSET) * VMap.Xsize + tile->x + MAP_OFFSET;
            if (VMap.map[offset] == tile->high)
            {
                high = TRUE;
                break;
            }
        }
    }
    ApplyTide(high);
    sCorvalaTideTimer = 0;
}

void CorvalaTide_Update(void)
{
    s16 x, y;
    u8 high;
    if (!IsCorvala() || QL_IS_PLAYBACK_STATE || gReceivedRemoteLinkPlayers)
        return;
    if (++sCorvalaTideTimer < 60)
        return;
    sCorvalaTideTimer = 0;
    if (gPaletteFade.active || ScriptContext_IsEnabled() || !IsFieldMessageBoxHidden()
        || gPlayerAvatar.tileTransitionState != T_NOT_MOVING)
        return;
    high = GetCurrentHour() & 1;
    if (high == sCorvalaTide)
        return;
    PlayerGetDestCoords(&x, &y);
    if (!IsSafePosition(x - MAP_OFFSET, y - MAP_OFFSET))
    {
        // Keep the current ground intact until the warning is acknowledged.
        // The script warps onto permanent dock ground; OnLoad applies the RTC
        // phase there and the normal warp resets Surf to walking.
        ScriptContext_SetupScript(high ? Corvala_TideRisingWarning : Corvala_TideRecedingWarning);
        return;
    }
    ApplyTide(high);
    DrawWholeMapView();
}
