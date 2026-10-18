# QOL → V1 → V2 integration — 2026-10-18

V1 advances from `2f008a1035b41902abdd57d6a268de83dd5a07e2` to the already-tested QOL commit `f3a842cdfa978f0db70056bf9d22ad6de56c9272`. This is a fast-forward, retaining the complete QOL history.

V2 merges that V1 commit into `563419b86419cf1e2e6de3d457cc66ace8f06e23`, retaining both histories. QOL and Havora-Development are not changed by this integration.

## Conflict resolution and integration

- The current tablet, storage, Party, night lighting, Pokédex, avatar and ROM-cleanup implementation comes from QOL.
- V2 keeps its island maps, Stellar Ticket quest, Seagallop sailing/return interactions, regional atlas, healing/visit flags, Fly checks, and removal of the separate post-League Oak ceremony. Replays use the original League teams.
- The map-recovery predicate is shared between QOL and V2 campaign sanitation. All saved/current/return warps use QOL's complete retirement set and safe Pallet location (10,9); species, item, fusion and recap migration remains intact.
- The ticket quest keeps flags 0x4E0–0x4E7. The independent candy gift uses 0x4E8. A release-ROM regression checks that completing the candy gift leaves the ticket quest flag intact.
- QOL's retired-layout list is adjusted to retain `PokemonCenter_2F_Layout`, which the new island maps and older V2 saves still use. The shared downstairs layout retains QOL's sealed multiplayer stairs. Older upstairs saves can use their return stairs; entrances into retired Union/Trade rooms are disabled without renumbering warp slots.
- The tablet Map app can preview the existing island artwork with L/R and defaults to the island page while there. A opens the retained native guide. Previewing does not unlock travel.
- A coordinate trigger makes the harbor's already-declared exit respond on its current painted tile. No island tilemap is repainted. The harbor return door and connecting routes are checked in both directions.

All 27 existing island layout/art files and the complete V2 map-group table were compared by Git blob hash with the original V2 head and preserved. Island Center event metadata changes only retire links into unavailable multiplayer rooms. The new harbor exit is event metadata/script behavior. The separate Havora development branch is untouched.

## Validation

V1 was rebuilt independently and produced SHA-256 `96ffe0d715a2c409d6455d5e5467adfe951d7fd69ca03f5cfb5842ebd27f3f33`, identical to the tested QOL ROM. Its title, storage visuals/resource cleanup, Party text, tablet transitions and night-lighting checks passed.

V2 release and development builds pass. Release linked usage is 21,426,844 bytes ROM, 258,352 bytes EWRAM and 27,573 bytes IWRAM. Development ROM usage is 21,480,252 bytes. ROM padding remains 32 MiB.

The combined runner includes the 25 shared QOL checks plus four V2 checks: campaign migration and credits, native region map, ticket/ferry/Center/route/Fly/save behavior, and QOL/island UI/flag coexistence. World integrity covers 256 retained maps, 887 warp entries and 100 connections, including a new assertion that a live map cannot use a layout marked retired.

The old upstream `make check` battle-suite compatibility limitation remains as documented in `qol-regression-validation.md`. This validation is targeted emulator coverage, not an uninterrupted full-story playthrough or a finished-island claim. The island layouts remain under active development.
