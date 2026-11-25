#ifndef GUARD_WORLD_PROJECT_H
#define GUARD_WORLD_PROJECT_H

struct Pokemon;

void WorldProject_Reset(u32 generation);
bool32 WorldProject_Trainer(struct Pokemon *party, u16 trainer, bool32 first);
u16 WorldProject_Land(u32 variant, u16 species, u8 level, u8 slot, u32 *identity);
void WorldProject_BattleStart(u32 flags, u16 trainer, u32 *kind, u32 *revision, u32 *selection);

#endif
