#ifndef GUARD_POKE_GLASS_H
#define GUARD_POKE_GLASS_H
u16 PokeGlassPrintTextPage(u8 window, u16 x, u16 y, u16 width, u16 rows, u16 page, const u8 *text);

void FitPokeGlassText(u8 *text, u8 font, u16 width);
bool8 IsPokeGlassActive(void);
bool8 IsPokeGlassSessionActive(void);
bool8 CanUsePokeGlass(void);
void PreparePokeGlassReturn(void);
void BeginPokeGlassReturn(void);
void BeginPokeGlassAppLoad(void);
void FinishPokeGlassAppLoad(void);
void BeginPokeGlassNativeTransition(void);
void FinishPokeGlassNativeTransition(void);
bool8 IsPokeGlassNativeTransitionActive(void);
void SetPokeGlassNativeViewport(u8 layer);
bool8 IsPokeGlassReturnActive(void);
void VBlankCB_PokeGlassReturn(void);
void PreservePokeGlassCoverPalette(void);
void EndPokeGlassSession(void);
void DrawPokeGlassFrame(u8 bg);
void DrawPokeGlassBagFrame(void);
void DrawPokeGlassTMFrame(void);
void LoadPokeGlassWindowBorder(u16 baseTile);
void LoadPokeGlassMenuPalette(u8 slot);
void DrawPokeGlassNativeOverlay(bool8 bag);
void DrawPokeGlassCaseOverlay(void);
void SetPokeGlassBlend(bool8 field);
void CapturePokeGlassBackdrop(void);
void LoadPokeGlassBackdrop(void);
void ReleasePokeGlassBackdrop(void);
void InvalidatePokeGlassBackdropForHeapReset(void);
void ShowPokeGlassHub(bool8 ignoreBPress);
void ShowPokeGlassStats(void);
void ShowPokeGlassStorage(void);
void ShowPokeGlassMap(void);
void OpenPokeGlassMapNative(void);
void ShowPokeGlassPokedex(void);
void ShowPokeGlassWardrobe(void);

#endif
