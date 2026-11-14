#ifndef GUARD_GAME_MODES_H
#define GUARD_GAME_MODES_H
#include "global.h"

#define GAME_MODE_POKEMON    (1 << 0)
#define GAME_MODE_MOVES      (1 << 1)
#define GAME_MODE_ABILITIES  (1 << 2)
#define GAME_MODE_LEVEL_CAPS (1 << 3)
#define GAME_MODE_NUZLOCKE   (1 << 4)
#define GAME_MODE_ITEMS      (1 << 5)
#define GAME_MODE_RANDOM     (GAME_MODE_POKEMON | GAME_MODE_MOVES | GAME_MODE_ABILITIES | GAME_MODE_ITEMS)
#define GAME_MODE_VERSION    0x71
#define NUZLOCKE_AREA_BYTES   32

void GameModes_EnsureInitialized(void);
bool32 GameModes_Enabled(u8 mode);
void GameModes_Set(u8 mode, bool32 enabled);
void GameModes_Apply(void);
void GameModes_NewGame(void);
void Nuzlocke_BeginEncounter(u16 area, u32 battleFlags);
bool32 Nuzlocke_CanCatch(void);
void Nuzlocke_RecordCatch(void);

#endif
