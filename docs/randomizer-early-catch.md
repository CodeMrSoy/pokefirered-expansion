# Opening-route randomized encounters

Randomized wild encounters on Route 1, Route 2, Route 22, Viridian Forest,
Pallet Town, Viridian City and Pewter City must have a natural catch rate of
at least 120. Legendary, Mythical and Ultra Beast species are excluded.

The threshold is configured by RANDOMIZER_EARLY_MIN_CATCH_RATE in
include/config/randomizer.h. Species catch rates, balls, encounter levels,
abilities and Nuzlocke rules are unchanged. Captures are not guaranteed.

The filter covers every wild encounter area on these maps, including fishing
and Surf encounters on later visits. It is geographic, not badge-dependent;
the same seed/map/area/slot remains deterministic. Existing save files may
therefore see new species in opening slots whose previous results were excluded.
Other maps, trainers, starters and gifts retain their existing randomization.

An existing eligible random result is retained. Otherwise, selection uses the
eligible pool compatible with the selected species mode. If that mode has no
eligible candidates, the full catch-friendly pool takes priority. Rattata is a
defensive fallback only for a custom configuration with no eligible candidates;
the standard species data has catch-friendly candidates, including Rattata.

Validation: python3 tests/randomizer_early_catch.py compiles production filter
and encounter functions with controlled species, mode and PRNG stubs. It checks
200 seeds / 2,772,000 selections, all protected maps, encounter areas and slots,
the 119/120 boundary, Legendary/Mythical/Ultra Beast exclusions, invalid species,
determinism, mode-compatible and empty-mode fallback, later maps and disabled
behavior. Map IDs come from the real map_groups.json. This host regression is
not a ROM build or an emulator test.
