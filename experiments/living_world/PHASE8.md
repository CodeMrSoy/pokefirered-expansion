# Phase 8 · Brock and the Pewter World Director

## Play the demo

Extract the Windows x64 directory and run **Play Pewter World Demo.cmd**.
The demo uses its own Pewter battery slot and starts outside the Gym. Its
first visit has an arranged research opportunity so it can be tested at any
time of day. Give the local worker a few seconds while outside. Enter the Gym,
ask the attendant about Brock, and read both pages. The Museum forecourt is
outside the main Museum entrance, east of the door. Speak to Brock there or
wait at the Gym. The standard Gym battle remains the way to earn the badge.
If Brock elects to stay on duty or the model is unavailable, the normal Gym
encounter is available. Use **Play.cmd** for your regular save.

In ordinary play, the agent considers research from 10:00 to 16:00,
team practice from 16:00 to 20:00, and Gym duties at other times. A
recent interaction at the Gym makes a departure temporarily ineligible.
The clock and area come from the ROM. Model-backed choices are visible in
`dialogue.jsonl` in the player's local LivingQuantumWorld profile.

## Map audit and progression contract

Pewter's Gym entrance at (15,16) links to Gym warp 1. Gym warp 1 returns
to Pewter warp 2. The Museum entrance at (17,6) leads to the ticketed
Museum interior. Brock's alternate slot (19,9) is an unblocked outdoor
tile outside that admission boundary. The outdoor tile requires no item,
badge, HM or optional fee. The Museum exhibits and Brock's journal provide
the subject for the research activity. The researcher request and cast
comparison are new optional world events, with no item reward.

The map audit also found the eastbound Gym guide triggers on the Route 3
approach. The allowed graph therefore excludes Route 3, the Museum
interior, and Mt. Moon. Brock can leave only from a fresh, safe Pewter
observation. A validated museum plan includes its return and a hard
90-clock-second deadline. The normal execution path has 12 seconds of
travel in each direction. Clock rollback, clock loss, protected
progression or an overdue plan restore his Gym duty. A stale or malformed
host projection defaults to the original Gym object in the ROM. Active
scripts, locked field controls and palette fades defer reconciliation.
The stock battle, Boulder Badge, TM, flags and map continuation remain in
the original Gym script. There is no badge award path in the Director.

## State and execution

`director_state` stores a bounded JSON snapshot on the existing SQLite
battery checkpoint key. It carries one current location and commitment,
queued step index, due time and hard deadline, research source and status,
recent decisions, researcher familiarity, recent challenger commitment,
and the optional objective and appointment. The existing checkpoint
transaction copies this state when there is a new battery save. Reopening
an older checkpoint reads that branch. It does not advance a newer branch.
Recent decision history is capped at 32 entries.

A scheduled decision produces a character-specific ticket containing
Brock's role, permitted research request, prior comparisons, current time,
Gym commitments and the valid candidate sequences. One grammar-constrained
call on the shared Qwen3 0.6B worker selects a candidate. The Director
rechecks the ticket after inference and checks each step's location,
target, timing and source. It logs rejected proposals. A missing or
failed worker chooses ordinary Gym duty. Existing Phase 7 routines,
knowledge propagation and dialogue caches still run through their original
paths.

| Action | Preconditions | Effect |
| --- | --- | --- |
| WORK, TRAIN_POKEMON, REST | Brock at the Gym | Finish the scheduled field activity without changing party or battle data |
| TRAVEL_TO | Gym, valid research ticket and return reservation | Mark Brock in transit, then at the Museum forecourt |
| VISIT_NPC | Forecourt and sourced request | Perform the scheduled researcher meeting |
| INVESTIGATE | Forecourt and valid request | Compare the exhibit after a bounded delay |
| SHARE_INFORMATION | Forecourt and valid request | Record firsthand comparison and increase familiarity once |
| RETURN_TO_DUTY | Forecourt and planned return route | Travel back and resume challenges at the Gym |

Assistant requests, other agent itineraries, arbitrary destinations and
model-invented action parameters are outside this slice. The model selects
among proposed sequences. The Director retains authority over every timed
transition. No research step reads player files or writes game memory.
The desktop publishes an eight-byte, three-state presence projection at a
ROM-specified address. The ROM owns safe object spawning and checks for a
player, follower or other object on the arrival tile. Plans execute during
ordinary field play. A running model call remains non-preemptible,
although the launcher uses one worker, limits reattempts, and discards
results when world eligibility or the checkpoint changes.

## Locate Brock

The attendant can relay what Brock told him when leaving. That statement
is an intended destination, and the objective records the notice as its
source. The objective only appears when the player asks while he is away.
A firsthand meeting at the forecourt resolves the objective and records a
Gym appointment with the existing return deadline. If Brock has already
started back, the attendant points the player to his return. An open
objective follows that return and closes when Brock confirms his presence
at the Gym. These are optional field interactions backed by saved state.
The separate V3 Quest Book is outside this feature.

## Verification

The bundled quantized Qwen3 0.6B produced 12 valid choices in 12 attempts
and matched the expected duty, practice, research, and competing-duty
cases. Median 1.55 s and maximum 2.18 s in the Linux standalone model suite.
The first model choice in the paired mGBA runs took about 2.6 s including
worker startup. These samples test action selection and timing, not
unconstrained dialogue or quantitative intelligence.

| 120 seeded Pewter replays | Count |
| --- | ---: |
| Prepared Gym challenges | 46 |
| Practiced at the Gym | 33 |
| Contacted Brock at the forecourt | 8 |
| Returned without an outdoor contact | 2 |
| Recovered after an invalid backwards clock | 8 |
| Recovered at the return deadline | 7 |
| Recovered when progression became protected | 5 |
| Fell back to duty after a simulated inference failure | 11 |

These replays used the measured choices for matching situation types.
The replays themselves made zero model calls. They rejected unsupported
actions, inaccessible destinations, incomplete plans and competing
commitments. All 120 ended with a reachable Gym challenge. Tests also
branched and reopened a battery checkpoint during travel.

Seven accelerated days with the Phase 7 scheduler and seven additional
Brock duty plans per population gave the following results on Linux.
These are synthetic actors, with one planning agent.

| Simulated residents | Report chains | Scheduler p95 | CPU time | DB size |
| ---: | ---: | ---: | ---: | ---: |
| 10 | 6 | 0.066 ms | 0.076 s | 88 KiB |
| 50 | 32 | 0.088 ms | 0.096 s | 156 KiB |
| 100 | 66 | 0.136 ms | 0.105 s | 244 KiB |
| 250 | 166 | 0.210 ms | 0.150 s | 492 KiB |

The 250-resident run peaked at about 90 KiB of traced Python allocation.
All four runs produced zero duplicate events and no autonomous model
calls in the synthetic loop.

Linux mGBA tests run both adventure modes against the compiled ROM,
including original Gym presence, absence, attributed dialogue, a travel
checkpoint, occupancy-safe late arrival, forecourt contact, departure and
return. The tests verify that the original trainer battle starts and
exercise the original victory script in a separate field fixture. They do
not play a full fight from start to finish. Phase 7 and PokéGlass checks
cover Pallet's bridge, existing walkers, time-of-day and repeated Party
screen returns. Native Windows launch and the Windows sandbox still
require a Windows run.

For reproduction, run `python -B tests/living_world_director.py` with
`LIVING_WORLD_PHASE5_RUNTIME` set to the bundled worker and weights on
Linux. Run `python -B tests/living_world_routines.py` for the scale table.
Build the ROM and run `tests/living_world_brock_emulator.py` with
`MGBA_CORE`, `ARM_NM` and `ADVENTURE_TEST_MODE` set for each mode. Set
`LIVING_WORLD_PEWTER_FIXTURE=1` to generate the standalone Pewter demo
battery fixture. Place it beside the existing pinned packaging inputs
and run `experiments/living_world/package-windows.py`.
