# QOL ROM-space cleanup

Implemented against `bf62bd5256f516290850e728f353514c3ba7e855` on QOL. V1, V2, Sprites and Havora-Development are unchanged. The preceding audit and decisions remain in `rom-space-audit.md` and `.json`.

## Measured result

| Measurement | Bytes |
| --- | ---: |
| Baseline linked ROM (`__rom_end`) | 23,811,700 |
| Cleaned release linked ROM | 21,408,464 |
| Reclaimed | **2,403,236 (2.292 MiB)** |
| Space remaining within 32 MiB | **12,145,968 (11.583 MiB)** |
| Development build linked ROM | 21,461,868 |

The distributed `.gba` remains padded to 32 MiB. Savings are the linked-ROM difference, not the padded file size or source-file sizes. Release EWRAM is 258,124 bytes; IWRAM is 27,573 bytes.

## Changes

- Shared the verified empty trainer slide data, identical Latin/Japanese font payloads, seasonal tile/metatile payloads and Arceus follower pixels. Separate palettes remain separate. Easy/Hard share an empty metadata row and retain their existing fallback to Normal difficulty.
- Enabled per-function/per-data linker collection. Debug menus/scripts are excluded by default; `make DEVELOPMENT=1 FILE_NAME=pokefirered-development` uses a separate object directory and keeps development tools.
- Retired 189 map headers and 194 layouts through the map generator. Numeric map/layout IDs stay stable; source files remain available for Porymap/future work. Removed original Sevii/multiplayer/selected cave event payloads and exclusive shared trainer scripts/text. Retired 106 exclusive trainer parties without renumbering trainer IDs.
- Removed forced Bill/Sevii detours and the League's Celio completion gate. League replays select the original teams. Original completion, Hall of Fame and credits remain.
- Replaced the Seafoam crossing with two-way Route 20 entrance warps. Disabled retired Fly destinations and added a runtime warp fallback for old destination references. Sealed Cerulean Cave; removed storage-PC art and upstairs multiplayer stairs from retained interiors. Bill's story computer remains.
- Added SELECT options to PokéGlass storage for release and inline box renaming. Release defaults to No and protects Eggs, the final usable party member, Mail and the final owner of each field move. Held items must fit in the Bag before a Pokémon is released.
- Retired 216 forms and mapped their IDs to retained species. Gigantamax, Z-Moves, Ultra Burst, Dynamax and Tera activation/trigger callbacks are unregistered; Mega and Primal remain. Fusion items and retired gadget items cannot open their old interfaces.
- Removed original movie/external-payload entry paths, Help, Teachy TV, Mail/phrase interfaces, diploma display, physical-PC menus, VS Seeker activation/rematches and roaming encounters. Retired special IDs share a no-op pointer rather than shifting the special table.
- Removed footprint data and guarded the retained native renderer. Unrooted decoration-catalogue/legacy sections are collected after retiring their metadata/shop roots.

## Replacement sources

| Content | Replacement |
| --- | --- |
| Mewtwo, level 70 | Pokémon Mansion B1F, after clearing the League |
| Articuno, level 50 | Route 20 island |
| Moltres, level 50 | Route 23, beyond the final badge gate |
| Rock Smash / Waterfall HMs | Celadon Department Store 4F |
| Solo trade-evolution items | Celadon Department Store 4F: Linking Cord, Metal Coat, Dragon Scale, Upgrade, Dubious Disc, Protector, Electirizer, Magmarizer, Reaper Cloth, Deep Sea Tooth/Scale, Prism Scale, Sachet and Whipped Dream |
| Jynx NPC-trade held Mail | Oran Berry |

The three relocated encounters preserve their original caught/fought/hide flags. The breeding/reminder engines and boat infrastructure remain for future Vidra locations. Other retired event-island legendary encounter locations remain reserved for future Vidra design; this change does not add those future maps or alter V2.

## Save compatibility

Species, item, trainer, map and layout IDs and save structures are unchanged. Migration runs after a valid save is loaded and before screens/maps read it:

- Converts party, boxes, daycare and hidden fusion partners to retained forms; recalculates party stats when species changes.
- Converts old follower/recap graphics IDs at graphics/palette lookup, including shiny/female cases.
- Recovers hidden fusion partners to free box slots; retains them when storage is full and retries when storage opens or a Pokémon is released.
- Transfers old PC items to the Bag only when they fit. Repeated recovery does not duplicate items.
- Removes retired held-Mail attachments while preserving the reserved Mail save arrays. Existing Bag/PC Mail can remain identifiable; it is excluded from random generation/new sources and cannot launch composition or be given from the Bag.
- Relocates saves from retired maps to Pallet Town (10,9), repairs return/heal/escape warps and forces a fresh field load rather than restoring retired NPC snapshots.
- Skips recap scenes recorded on retired maps and compacts retained scenes in order. The recap feature remains active.
- Clears the obsolete PC-service lock and hides the retired Cinnabar Bill detour.

## Protected data and conditional findings

All 1,201 linked direct-sound/cry samples compare byte-for-byte with baseline. All 347 song/SFX entries remain. The first stat/type fields of all 1,309 non-retired species entries match baseline. Ordinary species/moves/abilities/learnsets, natural/regional/gender forms, Mega/Primal, NPC trades, randomizer, Safari story rewards, Power Plant/Zapdos, followers, wardrobe, seasons, tablet UI and glass lighting remain.

Japanese glyphs/international string routines are retained for existing nicknames and retained internal text. Identical payloads are shared. Shared battle, NPC-trade, catch-Dex, transport and save helpers are retained even when their source module also supported retired features. A name containing `Unused` was not treated as proof of safe removal. Unreferenced sections are omitted by the linker; reusable source/assets stay in the repository. No audio reduction is counted.

## Validation

Release and development builds pass. Development-only debug symbols/scripts are present in the development ELF and absent from release. `git diff --check` passes.

The emulator checks cover actual pre-cleanup Flash-save loading, retired forms/followers and map relocation, fusion recovery with full storage, PC-item recovery idempotence, real Flash save/reset/Continue, tablet release/rename, 36 storage icons and drag/drop/cancel, Party rendering and repeated exits, Pokédex filters/habitats/save reload, single/double battles, Route 20 crossings and glass-only night lighting. Replacement encounter map screens were visually inspected. Logs are under `build/rom-cleanup-validation`.

This is a test build. An uninterrupted eight-badge/League/credits playthrough, every NPC trade/evolution and every randomizer seed have not been exhaustively played.

For reproduction, retain the baseline ELF/ROM in `build/cleanup-baseline`; use the checked-in encrypted form fixture and create its Flash fixture using `tests/rom_cleanup_old_save_emulator.py --create`. New tests use `ARM_NM` and `MGBA_CORE` environment overrides like the existing emulator tests.
