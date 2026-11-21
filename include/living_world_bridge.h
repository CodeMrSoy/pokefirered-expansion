#ifndef GUARD_LIVING_WORLD_BRIDGE_H
#define GUARD_LIVING_WORLD_BRIDGE_H

void LivingWorld_UpdateFieldHint(void);
bool8 LivingWorld_AllowsObject(u8 localId, u8 mapNum, u8 mapGroup);
void LivingWorld_ReconcileBrock(void);
struct ObjectEvent;
bool8 LivingWorld_AllowsScheduledWalk(const struct ObjectEvent *objectEvent);

#endif
