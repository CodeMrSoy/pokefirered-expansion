#include "global.h"
#include "gflib.h"
#include "main.h"
#include "field_screen_effect.h"

#define LANTERN_GLOW_TAG 0xD132
#define GLOW_TILE_BYTES 0x2000

static const u32 sGlowFrame0[] = INCBIN_U32("graphics/field_effects/lantern_glow/frame_0.4bpp.lz");
static const u32 sGlowFrame1[] = INCBIN_U32("graphics/field_effects/lantern_glow/frame_1.4bpp.lz");
static const u32 sGlowFrame2[] = INCBIN_U32("graphics/field_effects/lantern_glow/frame_2.4bpp.lz");
static const u32 sGlowFrame3[] = INCBIN_U32("graphics/field_effects/lantern_glow/frame_3.4bpp.lz");
static const u32 sGlowFrame4[] = INCBIN_U32("graphics/field_effects/lantern_glow/frame_4.4bpp.lz");
static const u32 sGlowFrame5[] = INCBIN_U32("graphics/field_effects/lantern_glow/frame_5.4bpp.lz");
static const u32 sGlowFrame6[] = INCBIN_U32("graphics/field_effects/lantern_glow/frame_6.4bpp.lz");
static const u32 sGlowFrame7[] = INCBIN_U32("graphics/field_effects/lantern_glow/frame_7.4bpp.lz");
static const u32 *const sGlowFrames[] = {sGlowFrame0, sGlowFrame1, sGlowFrame2, sGlowFrame3, sGlowFrame4, sGlowFrame5, sGlowFrame6, sGlowFrame7};
static const union AnimCmd sGlowAnim0[] = {ANIMCMD_FRAME(0, 1), ANIMCMD_END};
static const union AnimCmd sGlowAnim1[] = {ANIMCMD_FRAME(64, 1), ANIMCMD_END};
static const union AnimCmd sGlowAnim2[] = {ANIMCMD_FRAME(128, 1), ANIMCMD_END};
static const union AnimCmd sGlowAnim3[] = {ANIMCMD_FRAME(192, 1), ANIMCMD_END};
static const union AnimCmd *const sGlowAnims[] = {sGlowAnim0, sGlowAnim1, sGlowAnim2, sGlowAnim3};
static const struct OamData sGlowOam = {
    .shape = SPRITE_SHAPE(64x64), .size = SPRITE_SIZE(64x64), .priority = 1,
};
static const struct SpriteTemplate sGlowTemplate = {
    .tileTag = LANTERN_GLOW_TAG, .paletteTag = LANTERN_GLOW_TAG,
    .oam = &sGlowOam, .anims = sGlowAnims,
    .affineAnims = gDummySpriteAffineAnimTable, .callback = SpriteCallbackDummy,
};
static const u16 sGlowPalette[16] = {0};
static EWRAM_DATA u8 sGlowSprites[4] = {0};
static EWRAM_DATA u8 sGlowPhase = 0;

void LanternGlow_SetVisible(bool32 visible)
{
    u32 i;
    if (GetSpriteTileStartByTag(LANTERN_GLOW_TAG) == TAG_NONE)
        return;
    for (i = 0; i < 4; i++)
        if (sGlowSprites[i] < MAX_SPRITES && gSprites[sGlowSprites[i]].template == &sGlowTemplate)
            gSprites[sGlowSprites[i]].invisible = !visible;
}

void LanternGlow_Clear(void)
{
    u32 i;
    if (GetSpriteTileStartByTag(LANTERN_GLOW_TAG) != TAG_NONE)
    {
        for (i = 0; i < 4; i++)
            if (sGlowSprites[i] < MAX_SPRITES && gSprites[sGlowSprites[i]].template == &sGlowTemplate)
                DestroySprite(&gSprites[sGlowSprites[i]]);
        FreeSpriteTilesByTag(LANTERN_GLOW_TAG);
        FreeSpritePaletteByTag(LANTERN_GLOW_TAG);
    }
    for (i = 0; i < 4; i++)
        sGlowSprites[i] = MAX_SPRITES;
    sGlowPhase = 0xFF;
}

bool32 LanternGlow_Update(s16 x, s16 y)
{
    u32 i;
    u16 tiles = GetSpriteTileStartByTag(LANTERN_GLOW_TAG);
    u8 phase = (gMain.vblankCounter1 / 12) % ARRAY_COUNT(sGlowFrames);
    if (tiles == TAG_NONE)
    {
        struct SpriteSheet sheet;
        void *blank = AllocZeroed(GLOW_TILE_BYTES);
        if (blank == NULL)
            return FALSE;
        sheet.data = blank;
        sheet.size = GLOW_TILE_BYTES;
        sheet.tag = LANTERN_GLOW_TAG;
        LoadSpriteSheet(&sheet);
        Free(blank);
        tiles = GetSpriteTileStartByTag(LANTERN_GLOW_TAG);
        if (tiles == TAG_NONE)
            return FALSE;
        for (i = 0; i < 4; i++)
            sGlowSprites[i] = MAX_SPRITES;
        if (LoadSpritePaletteWithTag(sGlowPalette, LANTERN_GLOW_TAG) == 0xFF)
        {
            LanternGlow_Clear();
            return FALSE;
        }
        for (i = 0; i < 4; i++)
        {
            sGlowSprites[i] = CreateSprite(&sGlowTemplate, x, y, 0);
            if (sGlowSprites[i] == MAX_SPRITES)
            {
                LanternGlow_Clear();
                return FALSE;
            }
            StartSpriteAnim(&gSprites[sGlowSprites[i]], i);
        }
        sGlowPhase = 0xFF;
    }
    if (phase != sGlowPhase)
    {
        LZ77UnCompVram(sGlowFrames[phase], (void *)(OBJ_VRAM0 + tiles * TILE_SIZE_4BPP));
        sGlowPhase = phase;
    }
    for (i = 0; i < 4; i++)
    {
        struct Sprite *sprite = &gSprites[sGlowSprites[i]];
        sprite->x = x + ((i & 1) ? 32 : -32);
        sprite->y = y + ((i & 2) ? 32 : -32);
        sprite->invisible = FALSE;
    }
    return TRUE;
}
