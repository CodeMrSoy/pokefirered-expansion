# Quantum QOL ROM-space audit

Historical baseline audit. The subsequently authorized implementation and validation are recorded in `rom-space-cleanup.md`.

Audit baseline: `bf62bd5256f516290850e728f353514c3ba7e855` on **QOL**. This records Cody’s decisions from the audit conversation. No game code, map, asset, save layout or build option was changed; nothing was removed. V1, V2 and Sprites were not edited. The cleanup is a later implementation stage.

## Actual space baseline

- Linked ROM payload: **23,811,700 bytes (22.71 MiB)**.
- GBA ROM capacity: **33,554,432 bytes (32 MiB)**.
- Remaining address space: **9,742,732 bytes (9.29 MiB)**.
- ROM file: 32 MiB because it is padded. A smaller payload may still produce a 32 MiB download.
- Baseline ROM SHA-256: `8670e60ced1b7eb7d3672c9ef651ffcc3afe8a3972a11d61eb91f732a0c83e4d`.
- Review/index scope: **425 map headers, 365 layouts, 701 linked object entries and 50,629 size-bearing ROM symbols**.

The broad code/data pass identifies feature-level removal candidates. It is not a proof that every dead byte has been found: runtime script dispatch, pointer tables, saved IDs and metadata roots require dependency validation during each implementation chunk. “Unused” in a name and “not in a map header” are leads, not deletion instructions.

The largest gross linked input contributions are sound (`data/sound_data.o`, 9,061,928 bytes), Pokémon code/data (`src/pokemon.o`, 6,843,127 bytes), general graphics (1,044,008 bytes), tilesets (669,388 bytes), object movement/graphics (566,146 bytes), maps (515,992 bytes), fonts (514,888 bytes) and event scripts (452,419 bytes). These are **not free-space estimates**. Linked cry sample payload alone is 8,398,152 bytes, across 1,113 sample entries, and is protected by the roster/audio decisions.

## Decisions: remove or reduce

- Remove original multiplayer: link trading/battling, Union Room/chat, record mixing, wireless minigames, obsolete external-device services and their exclusive access paths. Keep NPC trades and their shared presentation.
- Remove original Sevii content, Trainer Tower, event islands and prototypes. Keep the boat system and reusable shared assets needed for Vidra.
- Remove Fame Checker, Teachy TV/skipped tutorials, contextual Help, Mail/mailbox, VS Seeker and the diploma display.
- Remove physical storage PCs. First put Pokémon **release and box renaming into PokéGlass**. Keep story-essential computers, storage/save logic and caught-Pokémon transfer behavior. Existing PC items/held Mail need safe handling.
- Remove Cerulean Cave and relocate Mewtwo. Remove Seafoam caves, relocate Articuno and preserve a Route 20 crossing. Keep Power Plant/Zapdos.
- Remove roaming beasts, keeping their species. Remove stronger League rematch teams; keep original-team League replays, completion, credits and Hall of Fame recording.
- Remove Gigantamax, special Tera forms, fusion forms, Ultra Burst, costume/cap Pikachu, Z-Moves, Dynamax and Terastallization. Keep base species and selected retained forms.
- Keep one Vivillon pattern, natural Furfrou, one Alcremie appearance and one Unown form. Choose canonical pattern/appearance/letter and old-save mappings during implementation.
- Remove the original Gengar/Nidorino movie; preserve Quantum’s space/Minior title and required boot behavior.
- Target footprints and Japanese-only assets conditionally, after retained screen/text/old-save dependencies are resolved.
- Include verified unused legacy/prototype data and the unused Hoenn decoration catalogue. Ordinary furniture/map tiles stay wherever used.
- Exclude debug menus from release builds; preserve them for development.

## Decisions: protected

- All Generation 1–9 base species; ordinary moves, abilities, learnsets, cries, gender differences and required species data.
- Regional forms/evolutions, Mega Evolutions and Primal Reversions.
- Natural color/seasonal variants, including Shellos/Gastrodon, flower colors, Deerling/Sawsbuck and Minior colors.
- Randomizer; save recap; Celadon Game Corner, coin/prize logic and Rocket Hideout story; NPC trades; Power Plant/Zapdos.
- Area-entry artwork for retained areas; current PokéGlass apps, battle HUD, follower Pokémon, wardrobe, time/seasons and window lighting.
- **Audio for Vidra**, including removed-content music/SFX. Audio must not silently vanish as a side effect of form/config changes. Do not count audio savings under this plan.
- Breeding/daycare and move-relearning engines, reserved for Vidra/Havora. Their original Sevii locations go; no new Kanto service location was requested.
- Standard Kanto services: fossil revival, move tutors/deleter, Name Rater, fishing, cycling and Itemfinder. Ordinary NPC dialogue, signs and occupied houses remain, except content exclusive to selected removals.
- Existing QOL save compatibility. Do not shrink save structures or renumber map/species/item/trainer IDs without a working migration strategy.
- Solo trade-evolution alternatives. Linking Cord and held-item alternatives already exist in species definitions; item availability still needs checking.

## Safe-storage optimization candidates

1. **175,224 bytes of empty trainer-dialogue arrays**, verified all-zero in the linked ROM: `sTrainerSlides` (124,824) and `sFrontierTrainerSlides` (50,400). Preserve future dialogue support with compact empty lookup behavior.
2. **435,301 raw duplicate bytes (425.1 KiB) across 139 identical read-only groups**. Four identical 32,768-byte Latin glyph arrays alone duplicate 98,304 bytes. Other groups include identical seasonal tile/metatile arrays and follower images with distinct palettes. Validate pointer identity/alignment; share identical payloads, not distinct palettes.
3. The non-LTO build does not currently enable per-function/per-data section collection. Evaluate that build optimization after the removal inventory is approved, keeping required linker/header/script roots. No trial build or savings measurement was performed here.
4. Inspect the empty Easy/Hard trainer metadata rows and difficulty fallback before considering compact representation. No difficulty feature removal was selected.

These candidates overlap other removals; **do not add their headline numbers together**.

## Candidate measurements

Byte counts below are current footprints or raw observations, not guaranteed reclaimed bytes. The JSON contains exact paths and per-candidate dependencies.

| ID | Candidate | Decision | Current measurement (bytes unless noted) |
|---|---|---|---|
| R01 | Original multiplayer and upper floors | remove | gross_object_bucket_bytes: 396,650 |
| R02 | Original Sevii maps, quests, trainers and tower | remove | map_headers: 164; exclusive_header_layouts: 124; raw_layout_payload_bytes: 153,272; trainer_tower_gross_objects_bytes: 36,276 |
| R03 | External-device multiboot payloads | remove | colosseum_payload_bytes: 163,840; ereader_payload_bytes: 14,176; berry_fix_payload_bytes: 15,348 |
| R04 | Fame Checker | remove | gross_module_bytes: 22,527 |
| R05 | Teachy TV and skipped tutorials | remove | gross_name_bucket_bytes: 8,437 |
| R06 | Help overlay/pages | remove | gross_module_bucket_bytes: 14,233 |
| R07 | Mail, mailbox and exclusive phrase UI | remove | gross_mail_easy_chat_bucket_bytes: 46,885 |
| R08 | Physical PC access and old PC UI | remove after replacement | gross_storage_module_bytes: 67,139 |
| R09 | Cerulean Cave maps | remove after relocation | Not yet measured |
| R10 | Seafoam cave maps | remove after replacement | Not yet measured |
| R11 | Roaming beasts | remove | gross_module_bytes: 1,690 |
| R12 | Stronger League rematch teams | remove | Not yet measured |
| R13 | VS Seeker | remove | gross_module_bytes: 7,380 |
| R14 | Pokédex diploma display | remove | gross_module_bytes: 5,754 |
| R15 | Original opening movie | remove | intro_object_gross_bytes: 49,345; old_title_wrapper_bytes: 12 |
| R16 | Development/debug menus and print helpers | release build exclusion | gross_debug_named_bucket_bytes: 46,833 |
| R17 | Selected battle form groups and mechanics | remove | gmax_named_readonly_bucket_bytes: 108,438 |
| R18 | Cosplay/cap Pikachu | remove | Not yet measured |
| R19 | Vivillon patterns | reduce to one | all_vivillon_named_readonly_bytes_including_kept_base: 110,006 |
| R20 | Furfrou trims | natural form only | all_furfrou_named_readonly_bytes_including_kept_base: 47,014 |
| R21 | Alcremie appearances | reduce to one | all_alcremie_named_readonly_bytes_including_kept_base: 20,732 |
| R22 | Unown letters/punctuation | reduce to one | all_unown_named_readonly_bytes_including_kept_base: 71,400 |
| R23 | Pokémon footprints | conditional remove | linked_footprint_bytes: 32,992 |
| R24 | Japanese-only font/text data | conditional remove | linked_japanese_glyph_bytes: 172,032 |
| R25 | Empty trainer slide tables | compact preserve behavior | verified_all_zero_bytes: 175,224; trainer_table_bytes: 124,824; frontier_table_bytes: 50,400 |
| R26 | Identical read-only arrays | deduplicate preserve behavior | groups: 139; raw_duplicate_bytes: 435,301 |
| R27 | Unused/prototype layouts and assets | conditional remove | layouts_without_located_runtime_reference: 36; their_raw_layout_bytes: 31,850; unused_named_rom_symbols: 139; unused_named_rom_symbol_bytes: 37,737; decoration_object_bytes: 10,090 |
| R28 | Dormant DexNav and imported facility support | conditional remove | dexnav_object_bytes: 7,169; imported_battle_tower_object_bytes: 16,524 |
| R29 | Obsolete native Dex/retired UI resources | conditional remove | native_dex_object_gross_bytes: 46,922 |
| R30 | Linker collection granularity | evaluate build optimization | Not yet measured |
| R31 | Empty difficulty metadata rows | evaluate compaction | trainer_metadata_table_bytes: 98,076 |

## Dependencies that must be resolved before deleting anything used

| Dependency | Required handling |
|---|---|
| Kanto League/Bill/Celio story coupling | `IndigoPlateau_PokemonCenter_1F` closes the League when National Dex is enabled but Celio’s quest is incomplete; Champion scripts choose stronger teams using the same flag. Replace the gate and team choice before removing Sevii. Preserve original League replay and the original ending. |
| Vidra transport | Keep Seagallop/boat animation and transport infrastructure; remove old destinations/quests without deleting the future Vidra route engine. Do not edit V2 here. |
| Lost useful sources | One Island gives HM06/Rock Smash; Icefall Cave supplies Waterfall; removed areas contain Articuno, Mewtwo, Moltres and event legends. Preserve moves/species/items and plan replacement sources in Kanto/Vidra. |
| Daycare and reminder | Four Island hosts breeding; Two Island hosts the Move Reminder. User chose to preserve engines for Vidra, not to delete these capabilities or add Kanto replacements now. |
| Physical PCs | Release and box renaming are still available through the old PC, not the tablet. Transfer those actions before cutting access/UI. Recover old saved PC items; keep storage data, box names, catch transfer and full-party/full-box handling. Current storage is 14 boxes × 30 slots; expanding capacity is outside this cleanup. |
| Mail and NPC trades | Jynx’s trade explicitly gives `ITEM_FAB_MAIL`. Replace the reward and safely handle existing held/stored Mail while preserving that NPC trade. Do not delete all of `trade.c`/`trade_scene.c` as multiplayer-only. |
| Single-player evolution | Many trade evolutions already have Linking Cord or evolution-item alternatives. Keep these rules and verify usable item sources without randomizer/link trades. |
| Old saves and disabled forms | Keep numeric IDs stable or migrate before sprite, summary, party, storage and battle code reads removed forms. Also handle saved positions in removed maps, PC items, Mail and accumulated story flags. A removed form must not become a corrupt/null Pokémon. |
| Randomizer | Current `IsSpeciesPermitted` rejects zero-HP/invalid species; verify all wild/trainer/starter/gift/egg/item/learnset paths after exclusions. Keep items/moves/forms selected for removal out of generated results. |
| Japanese glyphs | Retained internal Japanese strings and existing Japanese nicknames may still require glyph support. English-only scope permits review, not blind removal of international string routines. |
| Footprints and legacy Dex | The current tablet Dex does not show footprints, but native Dex code does. Resolve entry-point/table roots and retain shared Dex queries before removing assets. |
| Layouts absent from map headers | 56 layouts are outside map-header membership; 20 have located runtime references, including Seafoam current-stopped variants and Trainer Tower layouts. Only 36 have no located runtime reference (31,850 raw map/border bytes); verify indirect use and table slots. |
| Names containing “Unused” | 139 linked size-bearing symbols contain “unused” (37,737 bytes, including some functions). Some are still table-referenced. Check each before cutting. This is not a guaranteed savings total. |
| Metadata roots | `gDecorations` is retained through `src/rom_header_gf.c`; generic decoration shop commands also exist. Preserve mandatory cartridge header structure and used map furniture; retire unused catalogue roots deliberately. |
| Audio | Keep all selected audio. Feature/form flags may otherwise conditionally omit sounds; verify voice/song/cry tables and do not assume feature removal authorizes audio removal. |
| Shared graphics | Preserve retained area artwork, normal battles, NPC trades, followers, seasons, gender differences and tablet UI. A folder named after a removed feature may still contain shared data. |
| Safari Zone | Protected: its Secret House gives Surf and the Warden/Gold Teeth path gives Strength. It is not safe optional-map cleanup while keeping the original story progression. |

## Implementation order for the later cleanup

1. Preserve baseline/test saves and map/item/species IDs; implement necessary save migrations and replacement access paths first.
2. Compact verified empty/identical data and evaluate finer linker collection. Rebuild and measure the actual `__rom_end` delta.
3. Exclude release debug tools and verify their development-build availability.
4. Remove complete multiplayer/external-device paths while retaining NPC trades, shared interrupts, battle/save logic and protected audio.
5. Transfer PC actions to PokéGlass, recover old PC/Mail items, then remove physical terminal interactions and exclusive old UI.
6. Repair story gates/transport/rewards, then remove Sevii/selected Kanto maps and exclusive scripts/encounters/trainers/artwork. Preserve route connectivity and ending progression.
7. Remove selected mechanics/forms/cosmetic variants with old-save mappings, evolution/form-change fixes and randomizer filtering.
8. Remove the selected gadgets/help/diploma/movie, then any proven exclusive Japanese/footprint/legacy assets. Keep all shared data.
9. For each chunk, record real ROM-byte changes and relevant regressions. Validate opening/loading old saves, all eight badges/HMs/League/ending, original-team League replay, tablet apps, storage/release/rename/catching, NPC trades, solo evolutions, randomizer modes, title/audio, followers, seasons and lighting.

Do not count deleted source comments, PNG references, test files, unused headers, padding, save-RAM switches or already-discarded sections as reclaimed game ROM. Source-only assets can stay available for future Vidra work without being linked into a release ROM. Final savings can only be reported after rebuilt comparisons; no additive “total saved” is claimed here.

## Inventory files

`docs/rom-space-audit.json` contains every recorded decision, candidate source paths/dependencies, all 425 map statuses, the 56 alternate/orphan layout candidates, 139 duplicate-array groups, unused-name leads and the gross linked object attribution. These records make the removal pass reviewable and repeatable. The audit files are uncommitted; this audit did not create a new test ROM.
