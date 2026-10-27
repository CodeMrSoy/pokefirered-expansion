# Quantum V2 campaign scope

V2 inherits the current QOL branch through `f3a842cdf`: the tablet and PC-style storage, Party rendering and exit fixes, glass-only night lighting, National Pokédex, save compatibility, and ROM cleanup. Kanto, its first Elite Four/Champion teams, Hall of Fame, credits, and normal exploration remain.

The authoritative cleanup manifest is `data/quantum/retired_content.json`. It retires the same 189 legacy maps as QOL, including the old Sevii trips, caves and multiplayer rooms. Numeric map/species IDs and save structures remain stable. Mewtwo, Articuno and Moltres use QOL's Kanto replacement encounters. `docs/quantum-retired-maps.json` records the earlier 127-map V2 cleanup; it is a historical subset, not the current full retirement list.

All 20 V2 island maps remain, including the 40×32 Havora harbor, 80×80 city layout, five towns and their Centers, and four connecting routes. The Stellar Ticket quest, original Seagallop sailing/return interaction, healing, visit flags and native Fly eligibility remain. Painted island layouts and the original regional artwork are preserved. This is still an island foundation under active map development.

The tablet Map app previews Kanto and Vidra using L/R; A opens the native travel guide. Visiting a preview does not unlock travel. The existing native island map, region picker, location names and Fly behavior remain available.

V2 campaign sanitation delegates map/warp recovery to QOL's expanded predicate and safe Pallet destination (10,9), then clears its obsolete story/travel flags. Early Oak starter states are preserved. The campaign retains its removal of the separate post-League Oak ceremony and upgraded rematch introductions.

The QOL Center layout seals obsolete multiplayer stairs. The island's upstairs layout is retained because V2 maps and older V2 saves still reference it; upstairs return stairs remain available for those saves. Entrances to the retired Union/Trade rooms are disabled without renumbering warp slots. A coordinate trigger makes the harbor's existing city exit work with the in-progress painted tile while preserving the tilemap.

See `qol-branch-integration.md` for merge parents, checks and current ROM usage. An uninterrupted campaign playthrough is still outside this automated validation.
