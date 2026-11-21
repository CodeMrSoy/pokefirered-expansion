# Phase 11 · Regional NPC society

Phase 10 baseline: `cbacf9e60bd38eaecaf3560714041a44a1e93e28`.
This includes the controller and keyboard-remapping update. Development and
delivery are isolated on `Living-World-Phase11`.

## 11A

The configurable roster contains 24 host-side residents with distinct names,
six occupations, assigned workplaces, weekly days off, and shift times.
A deadline heap drives their schedules. The new table uses the existing
battery checkpoint transaction. No new native NPC slots are allocated.

## 11B

Goals survive daily shifts and battery branches. Profiles establish a work
motive and priority. Work units advance an explicit target over multiple
working days. Expired work ends against a game-clock deadline. Missed shifts
cannot create retroactive work, and a later goal gets its own identity.

## 11C

Occupations supply different work dependencies. A resident can ask an
eligible peer, prefer previous collaborators, and attempt independent work
after two failed requests. The recipient answers from their shift capacity
and existing relationship. A successful exchange records its actual
source, updates both relationships, and unlocks dependent work. Pending
requests expire and are capped at 24.

## 11D

Validated requests now create regional cooperation or survey events. Work
that reaches its goal yields a research, training, or ordinary work result.
Requests can complete, expire, or be withdrawn without a player action.
The capped ledger preserves the active entries and their true origin.
Only researchers' outstanding survey requests are published at the Museum
desk. Other resident memories and internal events remain private.

## 11E

An outstanding, published survey request can produce one Survey Notes
objective after an accepted Museum desk dialogue. Player delivery completes
the objective and NPC resolution can independently complete, expire, or
withdraw it. The dedicated projection has a fixed size and source code.
Classic and Quantum mGBA validated all four display states, rollback,
and preservation of the 144-byte native quest record.

## 11F

The model queue handles only survey-assistance decisions where the volunteer
can spare the time. Other shift and relationship choices use deterministic
rules. It allows three eligible requests per regional day and one per actor
per day, with a cap of four pending and 32 processed transitions per tick.
Old decisions become invalid on deadline, save change or response. If the
worker times out, the scheduler retains the already permissible default.
Current foreground actions take priority over queued plans. A resident's
in-flight request can still occupy the one offline worker. Logs record
ready-to-dispatch wait separately from Qwen and executor timings.

Forty-day synthetic measurements under Python allocation tracing on Linux:

| Residents | Transitions | p95 tick | Traced peak | SQLite |
| --- | ---: | ---: | ---: | ---: |
| 20 | 1370 | 4.534 ms | 140 KiB | 128 KiB |
| 50 | 3436 | 6.062 ms | 270 KiB | 160 KiB |
| 100 | 6878 | 11.574 ms | 492 KiB | 208 KiB |
| 250 | 17155 | 27.299 ms | 1089 KiB | 336 KiB |

These workloads made zero model calls. The 250-resident burst exceeded a
60 FPS frame budget with tracing active, and the package uses 24 people.
The size is for one battery history. Separate checkpoint snapshots retain
their own state, so the file can grow as the player makes additional saves.
The roster keeps eight memories and twelve relationships per resident,
24 open requests and 48 events. A simultaneous burst admitted three
distinct volunteers to the real Qwen worker. All three chose to continue
their work in that fixture. Cooperation and refusal were both exercised
by the deterministic simulations. No larger model was adopted.

## 11G · Demo, regression and merge readiness

Extract the Phase 11 archive into its own folder and run **Play Phase 11
Society Demo.cmd**. Choose **Continue**. The fixture starts in Pewter with
PokéGlass. The population runs two prior days through the normal simulation
rules to establish working history. Then one ROM-clock second advances one
population minute. This acceleration applies to the Phase 11 society only.
The ROM clock and existing Phase 10 travel stay at their normal speed.
The Phase 11 package uses the separate local profile
`%LOCALAPPDATA%\LivingQuantumWorldPhase11`.

Give the society some field time, then ask the assistant at the public
Pewter Museum desk about outstanding survey work. Museum admission still
uses the existing game script. You can carry a disclosed notice to the
volunteer or let the region resolve it first. Return later to see the
objective update. The route traveler, Museum volunteer, and Brock still
use the Phase 10 projection system. The 24 new identities live in the host
simulation and use existing Museum representatives for player interaction.

The Classic and Quantum Linux mGBA suite passed 18 mode-specific runs plus
three shared checks, including the native story paths, Brock battle launch
and separate award continuation, travel geometry and exclusive presence,
controllers, Bag, the seven static quests and all three dynamic categories.
The Linux probe denied unrelated file access, child process execution and
socket creation. These fixtures did not play an entire Brock fight. Native
Windows execution and AppContainer behavior are still unverified.

To reproduce, build the ROM with `make -j8`, set `ARM_NM` and `MGBA_CORE`
to the ARM symbols tool and Linux mGBA core, and run:

- `python -B tests/living_world_population.py`
- `python -B tests/living_world_population_bench.py` for deterministic scaling.
- Set `LIVING_WORLD_PHASE5_RUNTIME` to the bundled offline runtime and run
  the benchmark again for the real-Qwen contention test.
- `QUEST_QC_ADVENTURE=0 python -B tests/living_world_regional_quest_emulator.py`,
  then repeat with mode 1.
- Run the existing regional, Museum, PokéGlass, Bag, Gym and story suites
  against the same ROM. Generate the Pewter save fixtures with
  `LIVING_WORLD_PEWTER_FIXTURE=1` on the Brock emulator test.
- Build the separate Windows package with
  `experiments/living_world/package-windows.py`, the two Pewter fixtures
  and the existing pinned Windows inputs.

### Merge-readiness decision

The current `Living-Quantum-World` tip matched the recorded Phase 10 baseline
at review. Phase 11 already includes its controller and remapping fix. There
were no newer Phase 10 commits to bring over. The branch comparison is additive.
The new SQLite table and isolated package profile avoid changing Phase 10
demo state. Native ROM quest storage retains the same layout and seven
compiled quests. Phase 11 is suitable for isolated integration testing.
Before promoting it to the primary Windows playtest, validate the native
launcher, controller, AppContainer and save/restart flow. Keep the Phase 10
branch and release usable in parallel. No merge was performed.
