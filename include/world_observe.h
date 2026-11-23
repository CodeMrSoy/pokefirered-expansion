#ifndef GUARD_WORLD_OBSERVE_H
#define GUARD_WORLD_OBSERVE_H

struct Pokemon;

void WorldObserve_Start(u32 generation);
void WorldObserve_Frame(void);
void WorldObserve_Field(void);
void WorldObserve_BattleStart(u32 flags, u16 trainerA, u16 trainerB);
void WorldObserve_BattleEnd(u8 outcome);
void WorldObserve_BallFailed(struct Pokemon *mon, u8 slot, u16 item);
void WorldObserve_Capture(struct Pokemon *mon, u8 slot, u8 destination);
void WorldObserve_Evolution(struct Pokemon *mon, u16 formerSpecies);
void WorldObserve_Save(u32 counter);

#endif
