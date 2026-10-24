#include "global.h"
#include "event_data.h"
#include "event_object_movement.h"
#include "field_camera.h"
#include "field_player_avatar.h"
#include "fieldmap.h"
#include "havora_puzzle.h"
#include "main.h"
#include "script.h"
#include "sound.h"
#include "constants/event_objects.h"
#include "constants/flags.h"
#include "constants/havora_puzzle.h"
#include "constants/maps.h"
#include "constants/songs.h"
#include "constants/vars.h"

#define STATE_MAGIC 0x5A00
#define STATE_MAGIC_MASK 0xFF00
#define CUT_MASK 7
#define HOLE_SHIFT 3
#define GONE 0xFFFF
#define PACK(x, y) ((u16)((x) | ((y) << 8)))
#define ROCK_FLAG(i) (FLAG_TEMP_11 + (i))
#define TREE_FLAG(i) (FLAG_TEMP_17 + (i))

static const u16 sInitialRocks[] = {
    PACK(15, 24), PACK(22, 18), PACK(19, 16),
    PACK(24, 17), PACK(16, 23), PACK(19, 23),
};
static const u16 sPits[] = {PACK(18, 24), PACK(22, 16), PACK(16, 20)};
// A, B, C, D. A is temporary; B/C/D hold the final gate open.
static const u16 sPlates[] = {PACK(16, 22), PACK(21, 21), PACK(13, 27), PACK(18, 14)};
static const u16 sGates[] = {PACK(19, 22), PACK(16, 21), PACK(10, 13)};
extern const u8 HavoraNorthQuadrant_PuzzleReset[];

static bool8 IsPuzzleMap(u8 mapNum, u8 mapGroup)
{
    return mapNum == MAP_NUM(MAP_HAVORA_NORTH_QUADRANT)
        && mapGroup == MAP_GROUP(MAP_HAVORA_NORTH_QUADRANT);
}

static bool8 IsCurrentPuzzleMap(void)
{
    return IsPuzzleMap(gSaveBlock1Ptr->location.mapNum, gSaveBlock1Ptr->location.mapGroup);
}

static bool8 IsPuzzleRock(const struct ObjectEvent *object)
{
    return IsCurrentPuzzleMap() && IsPuzzleMap(object->mapNum, object->mapGroup)
        && object->graphicsId == OBJ_EVENT_GFX_PUSHABLE_BOULDER
        && object->localId >= HAVORA_PUZZLE_BOULDER_FIRST
        && object->localId < HAVORA_PUZZLE_BOULDER_FIRST + HAVORA_PUZZLE_BOULDER_COUNT;
}

static u16 RockPosition(u8 i)
{
    return VarGet(VAR_HAVORA_PUZZLE_ROCK_1 + i);
}

static u16 State(void)
{
    return VarGet(VAR_HAVORA_PUZZLE_STATE);
}

static u8 FilledPits(void)
{
    return (State() >> HOLE_SHIFT) & 7;
}

static bool8 Occupied(const u16 *rocks, u16 position)
{
    u8 i;
    for (i = 0; i < HAVORA_PUZZLE_BOULDER_COUNT; i++)
        if (rocks[i] == position)
            return TRUE;
    return FALSE;
}

static u8 OpenGates(const u16 *rocks, u8 holes)
{
    u8 result = 0;
    if (Occupied(rocks, sPlates[0]))
        result |= 1;
    if (Occupied(rocks, sPlates[1]))
        result |= 2;
    if (holes == 7 && Occupied(rocks, sPlates[1])
        && Occupied(rocks, sPlates[2]) && Occupied(rocks, sPlates[3]))
        result |= 4;
    return result;
}

static void ReadRocks(u16 *rocks)
{
    u8 i;
    for (i = 0; i < HAVORA_PUZZLE_BOULDER_COUNT; i++)
        rocks[i] = RockPosition(i);
}

static void PutTile(u16 position, u16 tile, bool8 blocked, bool8 redraw)
{
    s16 x = (position & 0xFF) + MAP_OFFSET;
    s16 y = (position >> 8) + MAP_OFFSET;
    MapGridSetMetatileEntryAt(x, y, tile | (blocked ? 0x400 : 0)
        | (HAVORA_PUZZLE_ELEVATION << 12));
    if (redraw)
        CurrentMapDrawMetatileAt(x, y);
}

static void RefreshWorld(bool8 redraw, bool8 sound)
{
    u16 rocks[HAVORA_PUZZLE_BOULDER_COUNT];
    u8 i, open, holes = FilledPits();
    bool8 gateChanged = FALSE;
    ReadRocks(rocks);
    open = OpenGates(rocks, holes);
    for (i = 0; i < 3; i++)
        PutTile(sPits[i], holes & (1 << i) ? HAVORA_PUZZLE_GROUND : HAVORA_PUZZLE_PIT,
            !(holes & (1 << i)), redraw);
    for (i = 0; i < 4; i++)
        PutTile(sPlates[i], Occupied(rocks, sPlates[i]) ? HAVORA_PUZZLE_PLATE_DOWN : HAVORA_PUZZLE_PLATE_UP, FALSE, redraw);
    for (i = 0; i < 3; i++)
    {
        u16 tile = open & (1 << i) ? HAVORA_PUZZLE_GATE_OPEN : HAVORA_PUZZLE_GATE_CLOSED;
        if (MapGridGetMetatileIdAt((sGates[i] & 0xFF) + MAP_OFFSET, (sGates[i] >> 8) + MAP_OFFSET) != tile)
            gateChanged = TRUE;
        PutTile(sGates[i], tile, !(open & (1 << i)), redraw);
    }
    if (sound && gateChanged)
        PlaySE(SE_SWITCH);
}

void HavoraPuzzle_ResetState(void)
{
    u8 i;
    if (!IsCurrentPuzzleMap())
        return;
    for (i = 0; i < HAVORA_PUZZLE_BOULDER_COUNT; i++)
        VarSet(VAR_HAVORA_PUZZLE_ROCK_1 + i, sInitialRocks[i]);
    VarSet(VAR_HAVORA_PUZZLE_STATE, STATE_MAGIC);
}

static void RestoreTemplates(void)
{
    u8 i;
    u16 state = State();
    for (i = 0; i < HAVORA_PUZZLE_BOULDER_COUNT; i++)
    {
        if (RockPosition(i) == GONE)
            FlagSet(ROCK_FLAG(i));
        else
            FlagClear(ROCK_FLAG(i));
    }
    for (i = 0; i < HAVORA_PUZZLE_TREE_COUNT; i++)
    {
        if (state & (1 << i))
            FlagSet(TREE_FLAG(i));
        else
            FlagClear(TREE_FLAG(i));
    }
    for (i = 0; i < gMapHeader.events->objectEventCount; i++)
    {
        struct ObjectEventTemplate *template = &gSaveBlock1Ptr->objectEventTemplates[i];
        if (template->localId >= HAVORA_PUZZLE_BOULDER_FIRST
            && template->localId < HAVORA_PUZZLE_BOULDER_FIRST + HAVORA_PUZZLE_BOULDER_COUNT)
        {
            u16 p = RockPosition(template->localId - HAVORA_PUZZLE_BOULDER_FIRST);
            if (p != GONE)
            {
                template->x = p & 0xFF;
                template->y = p >> 8;
            }
        }
    }
}

void HavoraPuzzle_OnLoad(void)
{
    if (!IsCurrentPuzzleMap())
        return;
    if ((State() & STATE_MAGIC_MASK) != STATE_MAGIC)
        HavoraPuzzle_ResetState();
    RestoreTemplates();
    RefreshWorld(FALSE, FALSE);
}

void HavoraPuzzle_OnResume(void)
{
    u8 i;
    if (!IsCurrentPuzzleMap())
        return;
    HavoraPuzzle_OnLoad();
    // Continuing a saved game may already have active object states. Bring
    // those into agreement with the persistent puzzle coordinates as well.
    for (i = 0; i < OBJECT_EVENTS_COUNT; i++)
    {
        struct ObjectEvent *object = &gObjectEvents[i];
        if (!object->active || !IsPuzzleMap(object->mapNum, object->mapGroup))
            continue;
        if (IsPuzzleRock(object))
        {
            u16 p = RockPosition(object->localId - HAVORA_PUZZLE_BOULDER_FIRST);
            if (p == GONE)
                RemoveObjectEventByLocalIdAndMap(object->localId, object->mapNum, object->mapGroup);
            else if (object->currentCoords.x != (p & 0xFF) + MAP_OFFSET || object->currentCoords.y != (p >> 8) + MAP_OFFSET)
                MoveObjectEventToMapCoords(object, (p & 0xFF) + MAP_OFFSET, (p >> 8) + MAP_OFFSET);
        }
        else if (object->localId >= HAVORA_PUZZLE_TREE_FIRST
            && object->localId < HAVORA_PUZZLE_TREE_FIRST + HAVORA_PUZZLE_TREE_COUNT
            && (State() & (1 << (object->localId - HAVORA_PUZZLE_TREE_FIRST))))
            RemoveObjectEventByLocalIdAndMap(object->localId, object->mapNum, object->mapGroup);
    }
}

static bool8 IsOpenPit(s16 x, s16 y)
{
    u8 i;
    u16 p;
    if (!IsCurrentPuzzleMap() || x < MAP_OFFSET || y < MAP_OFFSET)
        return FALSE;
    p = PACK(x - MAP_OFFSET, y - MAP_OFFSET);
    for (i = 0; i < 3; i++)
        if (sPits[i] == p && !(FilledPits() & (1 << i)))
            return TRUE;
    return FALSE;
}

bool8 HavoraPuzzle_CanEnterPit(const struct ObjectEvent *object, s16 x, s16 y)
{
    return IsPuzzleRock(object) && IsOpenPit(x, y);
}

bool8 HavoraPuzzle_CanPushBoulder(const struct ObjectEvent *object, s16 x, s16 y)
{
    u16 rocks[HAVORA_PUZZLE_BOULDER_COUNT];
    u16 destination;
    u8 i, j, open, holes = FilledPits();
    if (!IsPuzzleRock(object))
        return TRUE;
    if (IsOpenPit(x, y) && GetObjectEventIdByPosition(x, y, HAVORA_PUZZLE_ELEVATION) != OBJECT_EVENTS_COUNT)
        return FALSE;
    destination = PACK(x - MAP_OFFSET, y - MAP_OFFSET);
    ReadRocks(rocks);
    rocks[object->localId - HAVORA_PUZZLE_BOULDER_FIRST] = destination;
    for (i = 0; i < 3; i++)
        if (sPits[i] == destination && !(holes & (1 << i)))
        {
            holes |= 1 << i;
            rocks[object->localId - HAVORA_PUZZLE_BOULDER_FIRST] = GONE;
        }
    open = OpenGates(rocks, holes);
    // A plate may be released only if none of the gates it closes contain
    // a boulder, the player, a follower or an NPC. Never crush or trap an actor.
    for (i = 0; i < 3; i++)
    {
        if (open & (1 << i))
            continue;
        if (Occupied(rocks, sGates[i]))
            return FALSE;
        for (j = 0; j < OBJECT_EVENTS_COUNT; j++)
        {
            const struct ObjectEvent *other = &gObjectEvents[j];
            if (other == object || !other->active || !IsPuzzleMap(other->mapNum, other->mapGroup))
                continue;
            if (other->currentCoords.x == (sGates[i] & 0xFF) + MAP_OFFSET
                && other->currentCoords.y == (sGates[i] >> 8) + MAP_OFFSET)
                return FALSE;
        }
    }
    return TRUE;
}

bool8 HavoraPuzzle_OnBoulderMoved(struct ObjectEvent *object)
{
    u8 i, index;
    u16 p;
    bool8 fell = FALSE;
    if (!IsPuzzleRock(object))
        return FALSE;
    index = object->localId - HAVORA_PUZZLE_BOULDER_FIRST;
    if (!object->active || RockPosition(index) == GONE)
        return TRUE;
    p = PACK(object->currentCoords.x - MAP_OFFSET, object->currentCoords.y - MAP_OFFSET);
    if (p == RockPosition(index))
        return TRUE;
    VarSet(VAR_HAVORA_PUZZLE_ROCK_1 + index, p);
    OverrideTemplateCoordsForObjectEvent(object);
    for (i = 0; i < 3; i++)
        if (p == sPits[i] && !(FilledPits() & (1 << i)))
        {
            VarSet(VAR_HAVORA_PUZZLE_STATE, State() | (1 << (i + HOLE_SHIFT)));
            VarSet(VAR_HAVORA_PUZZLE_ROCK_1 + index, GONE);
            RemoveObjectEventByLocalIdAndMap(object->localId, object->mapNum, object->mapGroup);
            PlaySE(SE_FALL);
            fell = TRUE;
            break;
        }
    RefreshWorld(TRUE, !fell);
    return TRUE;
}

void HavoraPuzzle_RecordCut(u16 localId, u8 mapNum, u8 mapGroup)
{
    if (IsPuzzleMap(mapNum, mapGroup) && IsCurrentPuzzleMap()
        && localId >= HAVORA_PUZZLE_TREE_FIRST
        && localId < HAVORA_PUZZLE_TREE_FIRST + HAVORA_PUZZLE_TREE_COUNT)
        VarSet(VAR_HAVORA_PUZZLE_STATE, State() | (1 << (localId - HAVORA_PUZZLE_TREE_FIRST)));
}

bool8 HavoraPuzzle_TryResetShortcut(void)
{
    s16 x, y;
    if (!IsCurrentPuzzleMap() || !(gMain.newKeys & SELECT_BUTTON)
        || (gMain.heldKeys & (L_BUTTON | R_BUTTON)) != (L_BUTTON | R_BUTTON))
        return FALSE;
    PlayerGetDestCoords(&x, &y);
    x -= MAP_OFFSET;
    y -= MAP_OFFSET;
    if (x < 10 || x > 30 || y < 11 || y > 27)
        return FALSE;
    ScriptContext_SetupScript(HavoraNorthQuadrant_PuzzleReset);
    return TRUE;
}
