#include "global.h"
#include "event_data.h"
#include "event_object_movement.h"
#include "field_camera.h"
#include "field_player_avatar.h"
#include "fieldmap.h"
#include "havora_puzzle.h"
#include "main.h"
#include "palette.h"
#include "sprite.h"
#include "task.h"
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
static const u16 sPlateTiles[][2] = {{0x233, 0x234}, {0x235, 0x236}, {0x237, 0x238}, {0x23c, 0x23d}};
static const u16 sGateClosedTiles[] = {0x239, 0x23a, 0x23b};
extern const u8 Havora_NorthQuadrant_PuzzleReset[];

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

// Temporary OBJ graphics animate the barrier above its static grass/cap tile.
// Three marked barriers share one 1,920-byte sheet and one existing palette.
#define GATE_ANIM_TAG 0xFA50
#define GATE_FRAME_TICKS 6
#define GATE_ANIM_TICKS (5 * GATE_FRAME_TICKS)
static const u32 sGateAnimationTiles[] = INCBIN_U32("graphics/havora/gate_marked.4bpp");
static const struct SpriteSheet sGateSheet = {sGateAnimationTiles, sizeof(sGateAnimationTiles), GATE_ANIM_TAG};
static const struct OamData sGateOam = {
    .shape = SPRITE_SHAPE(16x16),
    .size = SPRITE_SIZE(16x16),
    .priority = 2,
};
static const union AnimCmd sGateOpenAnim[] = {
    ANIMCMD_FRAME(0, GATE_FRAME_TICKS),
    ANIMCMD_FRAME(4, GATE_FRAME_TICKS),
    ANIMCMD_FRAME(8, GATE_FRAME_TICKS),
    ANIMCMD_FRAME(12, GATE_FRAME_TICKS),
    ANIMCMD_FRAME(16, GATE_FRAME_TICKS),
    ANIMCMD_END,
};
static const union AnimCmd sGateCloseAnim[] = {
    ANIMCMD_FRAME(16, GATE_FRAME_TICKS),
    ANIMCMD_FRAME(12, GATE_FRAME_TICKS),
    ANIMCMD_FRAME(8, GATE_FRAME_TICKS),
    ANIMCMD_FRAME(4, GATE_FRAME_TICKS),
    ANIMCMD_FRAME(0, GATE_FRAME_TICKS),
    ANIMCMD_END,
};
static const union AnimCmd *const sGateAnims[] = {sGateOpenAnim, sGateCloseAnim};
static const struct SpriteTemplate sGateTemplate = {
    .tileTag = GATE_ANIM_TAG,
    .paletteTag = GATE_ANIM_TAG,
    .oam = &sGateOam,
    .anims = sGateAnims,
    .affineAnims = gDummySpriteAffineAnimTable,
    .callback = SpriteCallbackDummy,
};
static void Task_AnimateHavoraGates(u8 taskId);

static void CopyGatePalette(u8 paletteNum)
{
    // Copy the marker/wood palette, including weather/night/fade tint. The
    // barrier must not flash to a brighter object palette while retracting.
    u16 offset = 0x100 + paletteNum * 16;
    CpuCopy16(gPlttBufferUnfaded + 12 * 16, gPlttBufferUnfaded + offset, 32);
    CpuCopy16(gPlttBufferFaded + 12 * 16, gPlttBufferFaded + offset, 32);
}

static void FinishGateAnimation(u8 taskId, bool8 redraw)
{
    u8 i;
    struct Task *task = &gTasks[taskId];
    for (i = 0; i < 3; i++)
    {
        u8 spriteId = task->data[4 + i];
        if (spriteId < MAX_SPRITES && gSprites[spriteId].inUse
            && gSprites[spriteId].template == &sGateTemplate)
            DestroySprite(&gSprites[spriteId]);
        if (redraw && (task->data[0] & (1 << i)))
        {
            bool8 open = task->data[1] & (1 << i);
            PutTile(sGates[i], open ? HAVORA_PUZZLE_GATE_OPEN : sGateClosedTiles[i], !open, TRUE);
        }
    }
    FreeSpriteTilesByTag(GATE_ANIM_TAG);
    FreeSpritePaletteByTag(GATE_ANIM_TAG);
    DestroyTask(taskId);
}

static void Task_AnimateHavoraGates(u8 taskId)
{
    if (!IsCurrentPuzzleMap())
    {
        FinishGateAnimation(taskId, FALSE);
        return;
    }
    CopyGatePalette(gTasks[taskId].data[3]);
    if (++gTasks[taskId].data[2] >= GATE_ANIM_TICKS)
        FinishGateAnimation(taskId, TRUE);
}

static bool8 StartGateAnimation(u8 open)
{
    u8 i, changed = 0, taskId, paletteNum;
    for (i = 0; i < 3; i++)
    {
        u16 tile = open & (1 << i) ? HAVORA_PUZZLE_GATE_OPEN : sGateClosedTiles[i];
        if (MapGridGetMetatileIdAt((sGates[i] & 0xFF) + MAP_OFFSET, (sGates[i] >> 8) + MAP_OFFSET) != tile)
            changed |= 1 << i;
    }
    if (!changed)
        return FALSE;
    // Resource exhaustion safely falls back to the final tiles. No gameplay
    // state or control lock depends on a sprite allocation succeeding.
    if (GetTaskCount() >= NUM_TASKS || GetSpriteTileStartByTag(TAG_NONE) == 0xFFFF)
        goto fallback;
    LoadSpriteSheet(&sGateSheet);
    // This engine's loader returns zero on allocation failure (also a valid
    // tile start), so inspect the registered tag instead of its return value.
    if (GetSpriteTileStartByTag(GATE_ANIM_TAG) == 0xFFFF)
        goto fallback;
    paletteNum = AllocSpritePalette(GATE_ANIM_TAG);
    if (paletteNum == 0xFF)
    {
        FreeSpriteTilesByTag(GATE_ANIM_TAG);
        goto fallback;
    }
    CopyGatePalette(paletteNum);
    taskId = CreateTask(Task_AnimateHavoraGates, 80);
    gTasks[taskId].data[0] = changed;
    gTasks[taskId].data[1] = open;
    gTasks[taskId].data[3] = paletteNum;
    for (i = 0; i < 3; i++)
        gTasks[taskId].data[4 + i] = MAX_SPRITES;
    for (i = 0; i < 3; i++)
    {
        s16 x = (sGates[i] & 0xFF) + MAP_OFFSET;
        s16 y = (sGates[i] >> 8) + MAP_OFFSET;
        u8 spriteId;
        if (!(changed & (1 << i)))
            continue;
        SetSpritePosToOffsetMapCoords(&x, &y, 8, 8);
        spriteId = CreateSpriteAtEnd(&sGateTemplate, x, y, 0);
        if (spriteId == MAX_SPRITES)
        {
            FinishGateAnimation(taskId, TRUE);
            return TRUE;
        }
        gTasks[taskId].data[4 + i] = spriteId;
        gSprites[spriteId].sheetTileStart += i * 20;
        gSprites[spriteId].coordOffsetEnabled = TRUE;
        StartSpriteAnim(&gSprites[spriteId], open & (1 << i) ? 0 : 1);
        // Opening remains blocked until the barrier is flush with the grass;
        // closing blocks immediately, so actors cannot enter a rising gate.
        PutTile(sGates[i], HAVORA_PUZZLE_GROUND, TRUE, TRUE);
    }
    return TRUE;
fallback:
    for (i = 0; i < 3; i++)
        PutTile(sGates[i], open & (1 << i) ? HAVORA_PUZZLE_GATE_OPEN : sGateClosedTiles[i], !(open & (1 << i)), TRUE);
    return TRUE;
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
        PutTile(sPlates[i], sPlateTiles[i][Occupied(rocks, sPlates[i]) ? 1 : 0], FALSE, redraw);
    if (redraw)
        gateChanged = StartGateAnimation(open);
    else
        for (i = 0; i < 3; i++)
            PutTile(sGates[i], open & (1 << i) ? HAVORA_PUZZLE_GATE_OPEN : sGateClosedTiles[i], !(open & (1 << i)), FALSE);
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
    // Resume/warp may interrupt an animation. Restore the saved target state,
    // rather than retaining temporary collision or painting another map.
    if (FuncIsActiveTask(Task_AnimateHavoraGates))
        FinishGateAnimation(FindTaskIdByFunc(Task_AnimateHavoraGates), FALSE);
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
    if (FuncIsActiveTask(Task_AnimateHavoraGates))
        return FALSE;
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
    ScriptContext_SetupScript(Havora_NorthQuadrant_PuzzleReset);
    return TRUE;
}
