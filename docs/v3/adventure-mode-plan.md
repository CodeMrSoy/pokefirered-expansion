# V3 adventure modes: implementation and audit

Base: remote Pokemon-Quantum-V2, 2742860dfeff96a24e0dfda9680bd4232ef76ff1.
V3 is a separate development branch. V2 is never updated by this work.
The unchanged baseline compiled successfully before source changes.

## Architecture and phases

1. Baseline/audit: record compiled save offsets, preserve a baseline ROM/ELF,
   inspect existing retirement, story, party, encounters and mode-menu systems.
2. Mode framework: centralized adventure_mode API, versioned eight-byte record
   within reserved SaveBlock2 padding, pending New Game selection, confirmation,
   gameplay settings then existing Oak/avatar introduction. Loaded games cannot
   change adventure. Continue shows the mode; Classic hides Vidra gym settings.
3. Classic progression: generated per-party/per-slot baseline levels; exact
   baseline wild ranges before RNG; separate caps; restore Koga/Safari/Surf
   seams while keeping shared field-tool QoL. No blanket global level scaling.
4. Region/story boundaries: central Vidra access predicate and warp protection,
   ferry/Fly/map visibility, Classic-specific Kanto dialogue. Preserve Quantum
   story/crests/caps. Confirm existing Sevii retirement and close native ferry
   fallbacks; never delete Vidra's Stellar Ticket route.
5. QA: ARM save-layout checks, native test ROM, menu/character/Flash emulator
   checks using fresh games in both modes, actual baseline V2 Flash load into V3,
   independent randomizer/Nuzlocke/caps, story/travel regressions and release build.
   Publish completed commits only to Pokemon-Quantum-V3.

## Save audit

Compiled with the project's ARM ABI, V2 SaveBlock1 is 15780 bytes and SaveBlock2
is 3968 bytes. SaveBlock2 randomizerSeed is at 3756, gameModesVersion at 3761,
nuzlockeAreas at 3763 and unused filler_90 starts at 3795 (173 bytes).
V3 reserves the first eight filler bytes, leaving 165. Static assertions and
an ARM layout probe must enforce these exact boundaries. No sector sizes,
checksums, storage, party, flag or map IDs change.

A getter treats an untagged record as Quantum without writing. Only a successful
checksummed save load may install the legacy Quantum tag, after byte-layout
and cross-version tests. New Game writes its pending choice when the playthrough
is initialized. Merely opening/canceling New Game cannot relabel a loaded save.
Game-mode version 0x71, independent randomizer bits, seed and Nuzlocke history
remain unchanged. Save compatibility with arbitrary other expansion forks is
not claimed. Forward-loading V3 saves into V2 is not a supported mode-preserving
operation: V2 cannot interpret Classic progression.

## Systems requiring separation

- main_menu/new_game/save: pending selection, confirmation, commit, migration.
- game_modes/randomizer: independent toggles, Quantum-only Vidra gym control.
- caps: Classic 14,21,24,29,43,43,47,50,63; Quantum's existing 14 milestones.
- battle_main party construction: select baseline levels before mon creation.
- wild_encounter/scripted encounters: restore baseline ranges/levels before RNG.
- Fuchsia gym/city, Safari secret house/Gold Teeth: Koga and field-tool access.
- Vermilion ferry, seagallop, region_map, poke_glass: access and visibility.
- quantum_cleanup/campaign: load recovery must respect the active mode.

## Existing limitations and risks

V2 already retires 189 maps including Sevii, disables Bill's mandatory detour,
removes Celio's League gate, starts with the National Dex, and relocates useful
legendary encounters into Kanto. Verify these protections; do not delete assets
or restore old Sevii dependencies. Legacy native ferry destinations still need
an explicit allowlist so stale parameters cannot attempt a retired island.

Four Quantum Gym milestones (Corvala, Brandon, Ben, Cody) remain unbuilt in V2.
Preserve their reserved caps/crests; do not award fake victories or claim the
expanded campaign is complete. Their absence limits an end-to-end Quantum
campaign completion claim independently of V3 mode work.

The recorded pre-rebalance source is tools/progression/story-levels.json's
0a2b5758da3daab772144b412117cab0edab8df7. Its exact before-level arrays are a
verified baseline for Classic; current species, moves, abilities, AI and shared
QoL remain shared. Active rematch/difficulty data needs explicit coverage.

The prior local AI fix efe35fbdd is not in remote V2. It is preserved on its
separate feature branch and is not silently included in this V3 baseline.

A native test is evidence for its asserted path, not an uninterrupted campaign
playthrough. Release-readiness and unfinished checks must be reported explicitly.

## Phase 2 executed checks

The unchanged baseline and framework ROM builds passed. All 15 native groups
(adventure save invariants plus existing gameplay modes) passed. Separate mGBA
runs started fresh Classic and Quantum games through the real mode/confirmation/
settings/Oak/avatar flow, saved to Flash, reset and continued. A real baseline V2
Flash save migrated to Quantum without changing the seed, gameplay settings or
Nuzlocke history. Canceling pending Classic selection did not relabel that save.
Screenshots of selection, confirmation, character selection and Continue were
inspected. The real V2 Flash fixture remains local and is not published. Set
ADVENTURE_LEGACY_SAVE to a local V2 .sav path to replay the migration check.

These checks establish the framework, not completion of Classic balance/story.
Those integrations are the next phase.
