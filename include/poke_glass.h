#ifndef GUARD_POKE_GLASS_H
#define GUARD_POKE_GLASS_H

bool8 IsPokeGlassActive(void);
bool8 IsPokeGlassSessionActive(void);
bool8 CanUsePokeGlass(void);
void PreparePokeGlassReturn(void);
void BeginPokeGlassReturn(void);
void BeginPokeGlassAppLoad(void);
void FinishPokeGlassAppLoad(void);
bool8 IsPokeGlassReturnActive(void);
void VBlankCB_PokeGlassReturn(void);
void PreservePokeGlassCoverPalette(void);
void EndPokeGlassSession(void);
void DrawPokeGlassFrame(u8 bg);
void DrawPokeGlassNativeOverlay(bool8 bag);
void DrawPokeGlassCaseOverlay(void);
void SetPokeGlassBlend(bool8 field);
void CapturePokeGlassBackdrop(void);
void LoadPokeGlassBackdrop(void);
void ReleasePokeGlassBackdrop(void);
void ShowPokeGlassHub(bool8 ignoreBPress);
void ShowPokeGlassStats(void);
void ShowPokeGlassStorage(void);
void ShowPokeGlassMap(void);
void OpenPokeGlassMapNative(void);
void ShowPokeGlassPokedex(void);
void ShowPokeGlassWardrobe(void);

#endif
