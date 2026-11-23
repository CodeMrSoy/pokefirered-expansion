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
