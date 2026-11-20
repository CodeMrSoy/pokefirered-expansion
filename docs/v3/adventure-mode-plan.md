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

The prior completed AI fix efe35fbdd was absent from the remote V2 baseline.
V3 carries it forward in its own AI commit; V2 and the earlier feature branch
remain unchanged.

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

At that checkpoint only the framework was verified. Classic progression/story
integrations and their later checks are recorded below.

## Phase 3 executed checks

Classic party levels are selected at mon construction, before learnset/species
randomization, using the original party slot. Current species, items, abilities,
moves and AI are shared. An explicit quantum-level match prevents applying
normal campaign overrides to a mismatching custom facility/difficulty party.
Wild ranges are selected before RNG, including Lure's maximum-species scan;
this restores Old Rod slots that cannot be recovered by reversing a clamped
level shift. Scripted Snorlax/Power Plant levels are selected before species
randomization. Retired encounter payloads are not referenced. Relocated Kanto
legendaries already use their retained levels.

The generated data validates the current Quantum party/table slots against the
recorded manifest; new balance edits require an intentional mapping update.
Run tools/progression/generate_adventure_levels.py --check. The normal ROM
build and all 19 native framework/progression/game-mode groups passed. Actual
created Classic Gym parties match caps 14,21,24,29,43,43,47,50; Classic League
cap is 63, completed games and disabled caps return 100. Quantum level lookup
is unchanged. The native checks do not claim a whole campaign playthrough.

## Phase 4 integration and executed checks

Classic keeps Koga in Fuchsia without setting his Havora-return flag. Safari's
attendant gives the Surf tool at the traditional location; the Warden still
gives Strength/Power Gloves for Gold Teeth. The shared field-tool engine
retains the traditional Soul/Rainbow badge requirements. Gold Teeth use the
recorded pre-rebalance position (28,14) in Classic and V2's water-gated (11,17)
in Quantum. Classic visitors have Kanto-only dialogue and no Stellar rewards.

The native ferry uses an allowlist: only ticketed Quantum departures from
Vermilion reach Vidra; every Sevii/invalid ID resolves to the mainland. Classic
classifies Vidra maps from bounded map headers at the shared warp/load/recap boundary
and cannot unlock them through arrival or Fly flags. Quantum retains its
ferry/artwork/ticket/return path. The classic map app offers only Kanto.

Blaine's victory now keeps both Bill objects hidden and retires the invitation
scene. Transition/load sanitation also clears stale invitation state. Existing
retired maps/layouts, Kanto legendary replacements, National Dex initialization,
first-League teams, Hall of Fame and Celio-gate removal remain shared. Original
Sevii assets and IDs are retained; no new pass or gemstone gates are introduced.

V2 moved Celadon's department store to Havora. Classic can enter the same shop
interiors through Celadon's existing storefront attendants; the shared shop
exit and map header resolve back to Celadon in Classic. Quantum retains its
Havora entrances/exits. This preserves evolution/trade-evolution items and
other shop features without duplicating interiors. Receptionist/sign dialogue
is mode-specific. The current closed storefront art is preserved.

The normal ROM build and all 53 native framework/progression/game-mode/Quantum
AI/scoring groups passed. Separate emulator runs executed Koga's map state,
the mode-specific Gold Teeth position and actual Safari reward scripts; Classic
received Surf and Strength and entered/returned from the shared shop. Both
modes rejected legacy ferry IDs and stale Bill invitation state; Classic's
forged Vidra warp recovered safely. These are scripted integration scenarios,
not an uninterrupted campaign completion claim.

## Phase 5 final regression status

The final combined native test ROM passed **138 groups**, with zero failures
and no known-failing markers. It includes all adventure/framework/progression
groups, existing game-mode groups, Quantum AI tiers, doubles, switching and
move-scoring suites. A temporary migration-test fixture originally cleared live
options and stalled an unrelated switching test; restoring its prior save state
and using heap buffers resolved that cross-test interference. Assertions were
retained. All six host AI checks and the assignment audit pass.

Thirteen emulator regression scripts passed: fresh Classic/Quantum New Game
selection and persistence, real V2 save migration, both story scenarios, gameplay
options, avatar creation/movement/battle backs/save, PokéGlass launcher/apps and
backdrops, Quantum Koga, Eirik/Surf/Strength, Gym randomizer controls and legacy
Vidra map migration. Final story reruns also executed Blaine's real victory/reward
script, Classic's League guard without Celio flags, and both modes' scripted
Hall of Fame/credits paths. Those are end-state integration fixtures, not a
continuous playthrough through all eight Gym battles or the Elite Four battles.

The world audit initially found three existing V2 houses referencing retired
House3_Layout (which aliased Pallet Town). V3 restores that one registry entry;
no map geometry/art is redrawn. Actual entry, correct 11x9 layout and normal
exits were verified for Havora Weaver House, Fisher House and Cliff House 3.
The final audit passes all 295 retained maps, 977 warps and 138 connections.

Randomizer host checks pass for grass/water/rocks/all rods/rival milestones,
200 seeds of item/TM restrictions and 2,772,000 early-encounter selections.
The final ARM ABI probe matches V2 sizes and existing offsets exactly; actual
V2 Flash loading and both fresh-save reset/Continue paths pass. Real save files
stay local and are not published in the repository or ROM download.

## Remaining release checks and existing content limits

- Run uninterrupted Classic and Quantum campaign playtests on actual emulator
  saves, including every Gym/League battle and story route. The scripted
  integration checks above do not substitute for that playtest.
- Corvala, Brandon, Ben and Cody's Gym battles remain unbuilt V2 milestones.
  Their planned Quantum caps/crests are retained without fake completions.
- Future trainer/encounter edits must regenerate the Classic baseline mapping;
  missing active tables now fail generation rather than silently using Quantum
  levels. Shared normal campaign party overrides intentionally do not rewrite
  unrelated custom facility/difficulty parties whose authored levels differ.
- Device timing and long-session performance benchmarking remain unperformed.
  V3 adds no recursive battle search or second engine; final linker memory use
  stays within the GBA EWRAM/IWRAM/32 MiB ROM limits.
- Keep V3 isolated. It is a development build for continuing this work, not a
  claim that all planned Vidra content or campaign release QA is complete.

Final linked build: ROM payload 21,910,544 bytes (65.30% of 32 MiB), EWRAM
238,824 bytes and IWRAM 27,573 bytes. Both adventures run in that single ROM.
The baseline EWRAM was 238,820 bytes; save block sizes and pre-existing settings
offsets are identical. The eight-byte mode record consumes reserved save bytes.
