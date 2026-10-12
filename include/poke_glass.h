#ifndef GUARD_POKE_GLASS_H
#define GUARD_POKE_GLASS_H

void DrawPokeGlassFrame(u8 bg);
void SetPokeGlassBlend(bool8 field);
void CapturePokeGlassBackdrop(void);
void LoadPokeGlassBackdrop(void);
void ReleasePokeGlassBackdrop(void);
void ShowPokeGlassHub(bool8 ignoreBPress);
void ShowPokeGlassStats(void);

#endif
