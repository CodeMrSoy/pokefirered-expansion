#ifndef GUARD_QUANTUM_CLEANUP_H
#define GUARD_QUANTUM_CLEANUP_H
#include "global.h"
u16 QuantumCanonicalSpecies(u16 species);
void QuantumMigrateLoadedPokemon(void);
void QuantumMigrateLoadedWorld(void);
void QuantumRecoverWarpDestination(struct WarpData *warp);
void QuantumRecoverStoredItemsAndPokemon(void);
#endif
