# QOL cleanup regression validation — 2026-10-17

Tested commit: `8f34d2cbfe1b444322108aaa4396c7cd0b52d50e` plus regression-test updates only.

Release ROM SHA-256: `d03f0439288592be1edf48cb5625f59f681f4f8170319b8f98aff564bc72c9de`.
The existing Space Cleanup Test download has this same hash. Release and development builds both completed. No gameplay code changed during this validation.

**Result: 24/24 release regression checks passed.** Both builds completed; no reproducible gameplay defect was found in the tested paths. The separate upstream battle suite remains blocked as described below.

## Release-ROM coverage

The emulator tests use an mGBA libretro core. They drive actual button input and, where appropriate, use controlled RAM/script fixtures to reach specific conditions. These are targeted regressions, not an uninterrupted playthrough.

| Area | Checks |
| --- | --- |
| Party | One through six members; selection and swapping; summary/actions return; every exit frame and 12 repeated returns; field input restored after close |
| Party text and HP | Level digit growth, 9→10 and 99→100 boundaries, HP thresholds/healing/fainting, long nicknames, actual Rare Candy level-up, stat gain/total pages |
| Tablet | Six-app cursor navigation and clamped edges, app IDs and launch tasks, shell/backdrop, transitions, Stats and Pokédex, selected-app return |
| Storage | Box/party dragging and full-box cases; release confirmation defaults to No; party/box releases; last usable member; rename confirmation/cancellation |
| Additional release safety | Eggs cannot be released; sole Surf user protected; replacement in another box allows release; an Egg does not count as a replacement; held Oran Berry returned once; empty-slot no-op |
| Existing saves | Real old Flash save reset/Continue; encrypted retired forms in party/box/fusion; personality/OT preservation; idempotence; full boxes retain a hidden fusion partner; PC item recovery; stale follower graphics; retired current/return warps |
| World data | All 236 retained map layout byte sizes; 845 warp entries including intentionally disabled stairs; 84 connections; reachable static exits cannot lead to retired maps |
| World behavior | Removed Center stairs; Route 20 crossing in both directions; retired runtime warp recovery; relocated encounter maps |
| Story checkpoints | Complete Surf reward dialogue; Warden gives Strength and consumes Gold Teeth; physical League doorway works before and after game clear while Celio's link flag is unset |
| Replacement encounters | Mewtwo hidden before game clear; all three original fought flags respected; actual placed-object interactions enter Mewtwo Lv70, Articuno Lv50 and Moltres Lv50 battles |
| Trades and access | All nine NPC trade species requests and encrypted offered-Pokémon builders; Jynx holds Oran Berry; linked Celadon 4F shop includes HM06/HM07/Linking Cord |
| Avatars and intro | All four choices; Wardrobe confirm/cancel; identity unchanged; field/running animation mappings; four battle backs; tablet map; Fly landing; Flash save/reset/Continue; candy gift once; all three lab rival battle variants |
| Lighting | Asset and emulator day/night checks; paths darken and building glass warms |
| Data preservation | 1,201 audio samples byte-identical to pre-cleanup baseline; all 347 song/SFX entries retained; 1,309 non-retired species stat/type headers unchanged; 216 retired forms and stable numeric IDs/difficulty fallback |
| Randomizer | Existing host-side randomizer regression cases |

Three old test expectations were corrected: an extra Start press skipped the title after intro removal; the Storage app still expected the old PC task; the avatar test navigated to the former map location and inspected the former map icon. The updated checks assert the current tablet map task and saved avatar instead.

## Reproduction

Build the release first, then run:

```sh
python tests/run_qol_regressions.py
```

Requirements: ARM binutils (`ARM_NM` may specify the full nm path), an mGBA libretro core (`MGBA_CORE`), Pillow and NumPy. Baseline comparison and old-save tests also require the pre-cleanup assets in `build/cleanup-baseline/`. The runner saves individual logs and a machine-readable result file to `build/thorough-validation/` and continues after failures.

## Limits and blocked checks

The separate upstream `make check` battle suite did not run successfully. Its trainer tests call `CreateNPCTrainerPartyFromTrainer` without the current seed argument, and its linker script omits the function/data subsections used by this repository. A diagnostic attempt also exposed a reference to removed `gFallbackPokedexText`. These are test-suite compatibility problems; they are not counted as passing battle coverage. Temporary diagnostic edits to that suite were reverted.

This validation does not establish that every interaction is correct. An uninterrupted eight-badge/League/credits playthrough, every catch/defeat/flee result of each relocated encounter, complete NPC-trade animations, every evolution, Mega/Primal mechanics, hardware behavior, and all randomizer seeds still need broader playtesting. The initial/replay League doorway and targeted battle entry checks do not substitute for finishing the League.
