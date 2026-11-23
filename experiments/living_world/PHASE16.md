# Phase 16 world simulation

## Phase 15 audit

Baseline `dd2b637623b41e6688eff6a5a72a26b5ade818c0` (15.0.1) added measured
goal predicates, persistent unfinished commitments, a revision turn and
stimulus-driven retries. `4655c1a3` added real inference evidence, and
`84bf15d3` records native timeouts. GitHub Actions run [45023720406](https://github.com/CodeMrSoy/pokefirered-expansion/actions/runs/45023720406)
completed successfully on Linux and Windows parity, the candidate build and
the native Windows package job.

| Existing component | Reuse and boundary |
| --- | --- |
| Kanto identities, profiles and catalog | Use stable identity keys and native map names for the experimental region. Census and authored scripts continue to define playable hooks. |
| WorldMemory, social knowledge and routines | Checkpoint-scoped SQLite and attributed knowledge inform the new schema. Keep native checkpoint storage and existing memory schemas in place. |
| Population, Society and World Director | Existing emulator-clock schedulers execute bounded regional routines and authored opportunities. Phase 16 advances its own clock and creates only circumstances and generic consequences. |
| Regional events and Phase 15 agency | Reuse observation, intent, steps, and measured follow-through as concepts. The original choices and shop skills remain part of their shipped pilot. |
| Phase 14 WorldRules and native cap checks | Reuse real service registries and preserve native validators. Extend the copied-candidate and atomic-commit policy to the host simulation. |
| Offline worker | Reuse the bounded isolated transport and local weights. Distinguish recorded inference from maintenance and idle behavior. |
| ROM mailbox and Windows package | Preserve protocol, host loop, native progression, release build, and save profile. |

## Design before implementation

The experimental world uses its own versioned SQLite database. A single
transaction commits a validated candidate and its journal entry. The journal
records the seed and initial state, commands, observations, model decisions,
effects and failures. Replaying the same commands re-applies validation and
compares outcomes and state digests without invoking a model. Writes take a
database lock and plans carry an observed revision. The inspector opens the
database read-only.

Use opaque stable IDs and typed entity tables in the world snapshot. Native
locations and catalog keys identify projections. The host owns simulation
occupation, holdings, leases, relationships, knowledge, events, travel and
ambitions. Endpoint and ownership references, stock and money accounting,
essential service accessibility and mandatory route reachability are host
invariants. The ROM owns badges, story flags, battles, team legality, field
abilities, player inventory and checkpoint state. Presentation derives from
a validated host revision and contains no protected writes.

Action primitives have typed arguments and explicit preconditions. Resource,
currency and access changes are atomic per action. Plans are durable
commitments with an observable success condition. A subsequent failure
preserves actions already committed to the world and wakes the actor for
revision. Travel and work take simulation time. Updates run in stable order
and use seeded events, bounded ticks and a decision budget. A second NPC can
learn about a request or vacancy and act of its own accord. Public facilities,
local observations and attributed reports inform each actor. Private
holdings, motives and relationships belong to the relevant participants.

The runner seeds an isolated three-town region and advances hourly ticks.
Test cases set only conditions and measure effects. The offline model
interface receives an observation and proposes ambitions, observable goals
and sequences assembled from current primitives. A stopped or unavailable
model leaves pending decisions visible. Maintenance still advances, and the
journal distinguishes it from inferences and manually supplied commands.

Future ROM consumers can map validated relocation and occupations to safe
local object slots, dynamic shopkeepers to native shops, buildings to
whitelisted variants, conversations and events to existing text projection,
and environmental changes to vetted map variants. Any Gym challenge would
need a separate, native pre-battle check against the actual reachable
progression, team and supported content. Phase 16 exposes a read projection
for integration work while keeping it outside the live mailbox.

## Running the simulation

From the repository root, run Python 3.11 or newer. The simulator uses the
standard library and can run with a fresh SQLite file and no inference runtime.

```sh
python -B experiments/living_world/simulate.py run Trial.sqlite3 --days 15 --case cooperation
python -B experiments/living_world/simulate.py run Trial.sqlite3 --days 15
python -B experiments/living_world/simulate.py inspect Trial.sqlite3 --actor brock_attendant
python -B experiments/living_world/simulate.py trace Trial.sqlite3 > Trial.jsonl
python -B experiments/living_world/simulate.py replay Trial.jsonl --trace
python -B tests/living_world_simulation.py
```

Add `--runtime PATH` to use the existing isolated offline worker and its
`model.gguf`, or supply `--model FILE --style qwen3` or `--style gemma`.
`--decisions` limits model decisions, including failed requests. By default
the trial enables inference for the two focus residents.
`--all-npcs` makes the entire 24-resident roster eligible. A new database
uses the selected case and seed. Subsequent runs resume the same world.
A call advances up to 31 in-game days. The clock advances only when requested,
so a long real-world pause does not spend game resources.

The inspector outputs JSON suitable for filtering or viewing in an editor.
The whole-world view includes pending schedules, routes, entities, and
knowledge. The actor view includes personal state and that actor's timeline.
The journal includes full observation and inference evidence, action effects,
explicit rejections and snapshot hashes. It can be shared and replayed
without a battery save, ROM, emulator, model, or worker.

```sh
python -B experiments/living_world/benchmark_simulation.py RUNTIME MODEL.gguf qwen3 --decisions 6 --trace Traces
```

The benchmark uses the same starting state for each model. It permits six
decisions in the first 36 hours and three after reload over the next 36 hours
when run with `--decisions 6`. Initial conditions include funds, stock,
skills, housing access and an optional route closure. The only interventions
are at setup. Each case reports a measurable endpoint and preserves the raw
goals, actions, forecasts and model timing. The engine's unit tests exercise
controlled operations independently from the model trials.

## Supported mechanics and limits

| Area | Phase 16 behavior |
| --- | --- |
| Region | Viridian, Pewter and Cerulean, with abstract travel links, native facility identifiers, 24 residents, guest houses, three Marts and a Museum workplace. Census identities are reused where present. Synthetic residents and the trial economy are isolated. |
| Actions | Travel, report known facts, request or decline teaching, give goods, buy or sell, accept a job, release an employee, work, lease a room, establish or join organizations, practice with an owned Pokémon, rest and propose an optional route repair. Company wages are reserved and paid after a shift. |
| Knowledge | Public town names, neighboring sites, local shop and lease listings, actor-owned possessions, own memory and attributed reports. Other residents' skills and wallets are private. Teaching, trade and rent recheck current access at execution. |
| Scheduling | Hourly ticks, travel and shift completion, expiring requests, rest, local events, event wakeups and persistent plan queues. Model calls are budgeted. World updates and idle results are distinguishable in replay. |
| Authority | Experimental profile protection, required service floors, connected route checks, isolated player actions, native cap policy references and read-only projections. The ROM remains the sole authority for badge and story flags, mandatory teams, player party and inventory. |
| Remaining mechanics | Broader goods production and logistics, richer social contracts, property purchase, negotiated hiring, staffed service relocation, individual Pokémon stat changes, and live native presentation. The bundled planner exposes a subset of engine actions. Its short prompt and small model limit goal quality. |

Phase 15 launchers, battery saves, native mailbox code, shop interactions,
Gym gates and team validation have the same implementation as the audited
baseline. The Windows player ZIP remains the 15.0.1 playable preview. Run
Phase 16 headlessly from this branch. The read-only adapter reports host state
for future native sprite, shopkeeper, building, dialogue and event projections.

## Observed behavior and regressions

The [benchmark report](benchmarks/simulation/README.md) compares the three
local models. The [evidence archive](benchmarks/simulation/phase16-evidence.zip)
contains the raw Linux benchmark output, per-model and per-case replay
journals, longer traces, and the local native emulator logs. Unpack the
archive and pass any trial journal to `simulate.py replay PATH --trace`.
The SHA-256 manifest identifies every archived member.

| Trace | Observed result |
| --- | --- |
| `traces/thirty.jsonl` | The world reached hour 720. The run reopened the database at hour 360, recorded six seeded events, and replayed all 732 revisions to the same state. The two focus residents received 12 model decisions. |
| `traces/daily.jsonl` | With two model decisions per 24-hour window, the unhoused Brock attendant traveled to a guest house at hour 2, arrived at hour 3, then chose to lease it in a new planning turn. The lease committed at hour 26. The actor paid rent and retained the home after reload. The fixture supplied homelessness, available rooms and the decision budget. |
| `traces/thirty.jsonl`, hours 13–15 | The Brock attendant requested training from the society assistant. The assistant chose to teach, changing skill and trust. The attendant then chose to fill a vacancy that required the newly acquired skill. |
| `traces/roster.jsonl` | Each of the 24 residents across all three towns received one actual model decision. Sixteen decisions contained actions. The two-day history replayed all 72 revisions. |
| `traces/neighborhood.jsonl` | Four local residents were eligible for model turns. The assistant and researcher independently filled the two Mart vacancies. Their decisions removed that opportunity for the Brock attendant. The requested lesson never resolved in this trial. |

The 30-day and daily trials use the same primitives as ordinary runs. Daily
decision windows can be reproduced with repeated invocations of
`simulate.py run Trial.sqlite3 --days 1 --case relocation --decisions 2 --runtime RUNTIME`.
Other trace initial conditions, seeds and inputs are included in the journals.

Local Linux QA rebuilt the ROM with the ARM GNU toolchain and exercised
the Phase 15 host suites, checkpoint parity, Kanto dialogue and badge
continuation, Museum inquiries after reload, both native shop counters,
player endorsement, and capped Gym practice. The native emulator checks
ran in Classic and Quantum. The native shop and dialogue checks also ran
against the real isolated Qwen3 0.6B worker in both modes. The 11 headless
tests cover rollback, concurrent claims, provenance, state authority,
bounded catch-up, production-profile isolation and replay.

The new validator has no battle-authoring access. Universal preflight checks
for existing authored mandatory teams and an audit of all reachable player
parties, evolutions, items and field abilities remain outside this build.

The Phase 16 [platform run](https://github.com/CodeMrSoy/pokefirered-expansion/actions/runs/45154275224)
tested implementation commit `d8c6a1c8ff4d145b0a189c16c1716523ca5c1481`.
Linux and Windows parity passed. CI built the candidate, checked its checksum
and commit manifest, and passed the native Windows package smoke test on the
extracted ZIP. The platform run also records the Windows inference benchmark,
which exercises the packaged worker with the same local model families.
