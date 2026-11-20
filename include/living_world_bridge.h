#ifndef GUARD_LIVING_WORLD_BRIDGE_H
#define GUARD_LIVING_WORLD_BRIDGE_H

void LivingWorld_UpdateFieldHint(void);
struct ObjectEvent;
bool8 LivingWorld_AllowsScheduledWalk(const struct ObjectEvent *objectEvent);

#endif
