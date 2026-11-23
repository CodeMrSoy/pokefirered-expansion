#ifndef GUARD_WORLD_EXPORT_H
#define GUARD_WORLD_EXPORT_H

// A passive context record on the player core and a query port for a replica.
void WorldExport_SetContext(u32 origin);
void WorldExport_Poll(void);

extern const u8 gWorldEncounterWeights[5][12];

#endif
