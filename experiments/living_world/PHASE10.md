# Phase 10 · Regional Living World

## Baseline audit

Phase 9 release `2482854` confirmed five decision producers on one offline
Qwen3 0.6B worker. Its classifier selected a letter for an engine-assembled
itinerary. Duty schedules and timings, step effects, physical movement and
dialogue presentation were deterministic. The major guarded exception is
Brock's Gym contract, enforced independently by the ROM.

Personas and the actor's own observations, directed requests and collaboration
counts shape the prompt. Existing work with a sender affects willingness to
help close to closing. A report carries both original observer and immediate
sender. Only the recipient may act on an incoming request. The SQLite sidecar
aliases this state to the same battery checkpoint as existing Living World
events and the Phase 9 Locate Brock objective.

Before this phase, only Brock and the Bug Catcher had alternate physical
slots. Travel simulated transit and reconciled those slots on safe field
frames. The Quest Book showed one immutable template with a host-backed
state and never changed the seven native records. Phase 9 measured 1.49–2.49
seconds for the paired decision sample, 1.18 ms p95 across 120 policy replays,
and 0.248 ms p95 in its 250-resident routine harness. Foreground dialogue
could still wait behind one in-flight inference. Native Windows and
AppContainer verification remained open.

## 10A · Composed plans

The shared Qwen worker now receives available atomic targets and goal effects
for the four ordinary Pewter agents. It emits a constrained goal and up to
six ordered action IDs. A copy of world state executes the exact same rules
used by live steps to validate dependencies, time, result and end location.
Invalid plans leave the live state unchanged and the host applies a safe
routine where the ticket is still current. Brock keeps the separate
protected Gym contract and its bounded choice interface.

## 10B · Regional routes

The public Museum wing, Pewter and north Route 2 form the new graph. Graph
search respects actor-specific locations and persists its chosen legs,
arrival time and destination. The volunteer uses the existing Museum
visitor slot and two authored alternate slots. Geometry is checked from
the ROM layouts, including the public door and the open Route 2 border.
Classic and Quantum mGBA exercised departure, offscreen investigation,
arrival and return. Intermediate legs are simulated offscreen.

## 10C · Social choices

Agents may form a proactive offer for a known collaborator or pass a recent
field report to a known contact. A relay records immediate sender, original
observer and observation time. Contact rules prevent repeats, echo back
to the original observer and broadcasting to strangers. Accepted, declined
and completed requests become bounded memories. Report records never turn
into firsthand facts merely because they crossed another contact.

## 10D · Quest discovery and resolution

Museum Follow-up is derived from a current request that the volunteer
actually sent to the assistant. The public-wing assistant can disclose
that request. Talking to the volunteer can deliver an update, or the
assistant can resolve the request independently. An expired or withdrawn
request ends the objective. A checkpoint preserves its event ID, source
and terminal outcome, even when the bounded request history later rotates.

The Museum projection has a separate, fixed-size, validated slot. Both
dynamic entries coexist with the original seven native definitions and
cannot invoke tracking, reward or offer mutations. Classic and Quantum
mGBA tested both rows, dialogue-derived discovery, active and completed
presentation, independent resolution, expiry and checkpoint rollback.

## 10E · Scheduling and measured results

The planning thread explores at most 256 world-state prefixes and builds a
compact grammar from feasible transitions. This narrows semantic errors
before inference while preserving distinct compositions, targets and goals.
The first unrestricted sample led the researcher to investigate before
traveling and led the trainer to submit actions unrelated to practice.
Both were rejected. A longer prompt also exceeded the worker's input
capacity in the researcher case. The release uses compact prompt text,
transitions from the simulated graph and final authoritative revalidation.

One shared Qwen3 0.6B worker still serves all NPCs. Only one background
decision is pending, and foreground dialogue takes priority over queued
background work. An in-flight inference remains non-preemptible. Routine
plans have a bounded 16-entry in-session, checkpoint-scoped cache. Timed
actions use field clock updates; repeated frames within the same second
avoid scanning unchanged events. A composed plan interrupted by a missed
deadline or clock problem may retry once with a fresh ticket.

On AMD EPYC Linux the final real-model sample accepted four composed
ordinary-agent plans and Brock's protected decision. The volunteer selected
the Route 2 survey, investigating tracks, returning and resting. Decision
latency was 1.45–2.85 s, including a cold Brock call. The largest graph
took 71.5 ms off the emulator thread. These are five measured decisions,
not a population-wide acceptance-rate estimate.

120 seeded policy runs produced 72 regional surveys, 36 local checks and
12 interruptions followed by a new planning ticket. Under allocation
tracing, validation and transition calls measured 0.69 ms p95 and peak
Python allocations were about 203 KiB. The Phase 9 100-day soak retained
100 checks and reopened a 108 KiB database. The 250-resident Phase 7
synthetic workload reran at 0.288 ms p95, 500 KiB SQLite and zero duplicate
events. That workload scales the routine scheduler, not 250 inference
clients. No model calls were made inside the seeded or synthetic loops.

## Play the release

Extract the full package or apply the update over a full Phase 9 package.
Run **Play Pewter Regional Demo.cmd** and choose **Continue**. The fixture
starts in Pewter with PokéGlass and uses its own battery slot. Leave the
field running for about half a minute, then visit the northern Route 2 road
via Pewter's south exit. The volunteer can choose a survey, travel across
Pewter and return to the public Museum wing. The shared worker can also
choose local work or cooperation based on the available plans. Outcomes
are logged to the existing local LivingQuantumWorld profile. Use the older
**Play Pewter Society Demo.cmd** to begin from the Museum-oriented context.

If an assistant discloses an outstanding Museum request, the optional
Museum Follow-up appears in the Quest Book. Check in with the volunteer or
let the staff resolve it. Locate Brock remains discoverable from the Gym
attendant when Brock is away. The standard Gym battle is required for the
Boulder Badge. The public Museum uses its existing admission script.

## 10F · Validation and reproduction

The release GBA build passed 19 mGBA suites and mode variants on Linux,
including two-slot dynamic Quest Book, regional travel, the previous
Pallet bridge and schedule behavior, adventure story paths, Brock,
Bag and static quest persistence. Brock's native battle launch and
victory continuation were tested in separate fixtures. The suite does
not automate a full fight. The Linux isolation probe denied a network
socket, process execution, and unrelated file reads and writes. Native
Windows was unavailable. Windows launcher execution, the AppContainer
boundary and long Windows gameplay are still unverified.

**Validate Offline Runtime.cmd** is included for a Windows machine. It
runs the bundled sandbox probe, then boots the worker and verifies both
existing NPC inference and a validated regional composition. It is a
diagnostic, not a substitute for a Windows gameplay run.

Build from the repository root with `make -j8`. Set `ARM_NM` and
`MGBA_CORE` for the ARM toolchain and mGBA core. Use the following
reproduction checks:

- `python -B tests/living_world_planning.py` for 120 policy replays. Set
  `LIVING_WORLD_PHASE5_RUNTIME` to measure real bundled Qwen.
- `python -B tests/living_world_field_exchange.py` for provenance and access.
- Run `living_world_regional_emulator.py`, `living_world_brock_emulator.py`
  and `adventure_story_emulator.py` with `ADVENTURE_TEST_MODE=0` and `1`.
- Run `living_world_museum_quest_emulator.py` and
  `pokeglass_bag_quest_qc_emulator.py` with `QUEST_QC_ADVENTURE=0` and `1`.
- Set `LIVING_WORLD_PEWTER_FIXTURE=1` on the Brock test to generate the two
  Pewter fixtures. Put both beside the pinned Windows packaging inputs and
  run `experiments/living_world/package-windows.py`.

The supported region is the public Pewter Museum, Pewter City and north
Route 2, with Brock's existing Gym and Museum forecourt contract. The
volunteer and Bug Catcher use approved slots and simulated travel legs.
Visible movement between maps, broader Kanto/Vidra deployment, and free
form world targets remain outside this build.
