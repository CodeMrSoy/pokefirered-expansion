# Phase 20 · Autonomous Pokémon trainers

Phase 20 starts at Living World `8906c6e`. It shares the native observation
journal, ecology clock, knowledge retrieval, offline planning worker and
paired Flash checkpoints. No ROM code or native battle outcomes change.
Phase 19's five reviewed migration corridors and simulated ecology remain in
effect. Windows display frame pacing and the earlier recorder-free timing
diagnostic remain outside this phase's automated coverage.

## Participants and authority

The initial participants are the Route 1 scout, Viridian insect student and
Bug Catcher Sammy. Their profiles require exact compiled object script labels.
Sammy additionally requires the authored normal trainer 104 definition, a
plain single battle and an unprotected roster. The two early local asides
can verify the speaker and location for dialogue. Sammy has no dialogue hook.

The catalog now reads the trainer ID after the local-object byte emitted by
`asm/macros/event.inc`. The old offset can be reproduced exactly to prove the
digest of a prior catalog for the same ROM. A reviewed legacy Sammy binding
can be associated with trainer 104 while keeping the original manifest
immutable. Conditional native team templates appear beside independent
companion rosters. No native trainer party is transferred into companion
ownership. Opening companion inventory is journal policy (64 credits and
three ordinary Poké Balls per trainer). Purchases and fixed-price local
jobs debit or credit those balances, with no connection to player inventory
or payment rates in the ROM.

## Actions and information

An active session advances one ecology and trainer day per 24 existing
simulation hours. Travel occupies one to three days and requires a reviewed
outdoor corridor with reciprocal, direction- and offset-verified compiled
connections. The first two profiles use only Pallet–Route 1–Viridian.
Viridian Forest acts as Sammy's local training area. The routes through
gates, caves and interiors are unavailable. Current work, rest, practice
and travel consume the trainer's turn. Opening grants, local jobs,
travel, training, purchases, and shared reports are companion activities.

Trainers scout accessible land and see only a sampled result. They can act
on fresh, local sightings or lower-confidence reports from a known contact.
Reports keep original speaker, location, time and confidence. Existing
Phase 19 sightings can be used only when attributed to that trainer and
current on the trainer's map. Recent companion activity can enter the
existing validated NPC dialogue retrieval once the ROM verifies speaker and
area. Reports expire after 14 days and are rechecked at use.

A shared Qwen3 worker may choose a goal and one or two action steps from
the existing compositional planner. It sees the actor's own state, contact
opportunities, and available actions. A grammar built from feasible action
paths limits proposals. Accepted and rejected plans are journaled, and each
step is revalidated before execution. Inference is offered at most once
across the world every five days, with one background request in flight.
Busy, absent, stale or failed inference falls back to the seeded policy.
Different ambitions, preferences, opportunities and resources affect
action priorities. Routine decisions do not require language inference.

## Capture, teams and development

A capture attempt requires a recent local sighting, an eligible wild
cohort or exact simulated rare individual, a ball and a free destination.
The companion odds per thousand are capped at 925 and combine twice the
compiled catch rate, three times competence, up to 90 experience points,
a seeded condition penalty/bonus and sighting confidence. A witnessed
individual whose whereabouts cannot be verified produces an unconfirmed
sighting with no ball consumption. A real attempt uses a ball whether it
succeeds or fails. On success exactly one wild resident is transferred, an
aggregate capture gets a deterministic identity, and a simulated named
individual retains its identity. Protected species and native-observed
individuals are excluded. The first supported habitat layer is land.

Starting levels use the native resolved land ranges capped to this
companion tier, or level 1 for a supported migrant without any local
authored range. Species IDs retain form identity. Abilities follow the
resolved native ability slots. Known moves come from eligible entries of
the resolved level-up learnset. Party size is six, with 18 storage places.
Storage rotation uses the trainer's preferred species/type and experience.

Training costs 12 companion credits and adds fatigue. It awards 8–16
companion experience, with a threshold of 20 plus three times the current
level. Practice between two ready, familiar trainers compares the sum of
compiled base stats times level, competence, and a seeded tie-break.
It awards 8 and 5 experience to the winner and partner respectively.
This is a companion practice rule. Rest restores party readiness. The
level cap of 16 is a companion training limit. Only a single unambiguous,
unconditional level evolution can apply. Its effective species, ability
and move data are reloaded from the same manifest. Medicine, badges,
native PC contents, traded or conditional evolutions, player-level
transactions, and story-led Gym challenges are outside the preview.

## Persistence and validation

The trainer snapshot and day journals share the native tick transaction
with population changes and the recorded planning input. Retries cannot
advance the same native tick twice. Replaying recorded ecology inputs also
checks every trainer journal entry and the resulting projection. The
paired SQLite checkpoint holds the native events, trainer state and
ecology together, with the prior save and rollback rules intact. There
is no offline advancement. The Monitor separates simulated ownership
and discoveries from authored native roster definitions and observations.

Run `python -B tests/living_world_trainers.py` and
`python -B tests/living_world_trainers_benchmark.py trainer.json --manifest world.json`.
The benchmark checks resource balances, unique ownership, wild removals
and exact replay at days 30, 90 and 365 through 250 stress-test profiles.
The extra profiles are benchmark identities. Use `--profiles 0` for the
actual compiled roster and `--model-runtime` for bounded offline trials.
CI also runs the native mGBA suite for Classic, Quantum and authored
settings through at least one trainer day, and verifies packaged Windows
initialization from a native Continue.
