#ifndef GUARD_ADVENTURE_PROGRESSION_H
#define GUARD_ADVENTURE_PROGRESSION_H
#include "global.h"
struct WildPokemon;
u8 AdventureMode_TrainerLevel(u16 trainerId, u32 slot, u8 quantumLevel);
void AdventureMode_WildRange(const struct WildPokemon *table, u32 slot, u8 *min, u8 *max);
u8 AdventureMode_ScriptedLevel(u16 species, u8 quantumLevel);
#endif
