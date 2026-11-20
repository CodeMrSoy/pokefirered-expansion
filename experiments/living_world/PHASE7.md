# Phase 7 · Kanto routines and persistent notes

## Playable slice

The Phase 7 Windows x64 build bundles the existing Qwen3 0.6B worker.
Extract the full ZIP to a new folder, or install the small update over
the extracted Phase 6 build. Launch **Play Pallet Social Demo.cmd**.
The update uses the same battery save slot and storage as Phase 6.

1. Meet Watts with Pikachu following. The existing Pallet conversation
   can give the sign guide the first attributed report.
2. Visit the ledge scout on eastern Route 1. A verified transfer takes
   about 12 in-game clock seconds after the guide hears the sighting.
   The scout can tell you whose report it is.
3. Visit the youngster who talks about Caterpie and Weedle in southeast
   Viridian City. The second transfer takes another 18 clock seconds.
   During study hours he reviews it, then returns to his usual research.
   An overnight delivery waits for his next study shift. The review
   lasts one clock minute. His dialogue reflects the report and activity.
4. Save and re-open the desktop game to revisit the report. The usual
   game save keeps its own field location. The sidecar carries the
   bounded events, attributed reports and relationships associated with
   that battery checkpoint.

Talk to the scout during the day and again at night to see his normal
wander give way to stationary note-taking. His nightly stance retains
the tile where a safe normal walk finished. The Viridian youngster has a
different walking window. The launcher follows the ROM clock.

| Resident | Clock schedule | Persistent goal | Event behavior |
| --- | --- | --- | --- |
| Pallet guide | Helps travelers 06:00–20:00, sorts notes otherwise | Share useful local tips | Plans a handoff after hearing Watts |
| Route 1 ledge scout | Walks the ledges 07:00–19:00, writes notes otherwise | Keep useful route notes | Records and forwards the report |
| Viridian insect student | Studies and walks 09:00–18:00, rests otherwise | Compare Pokémon habitats | Reviews secondhand evidence during a study shift |

## Implementation

The production host consumes the ROM's clock and location through the
existing read-only field hint, extended from 12 to 16 bytes. Background
events run even with dialogue prediction disabled. The ROM updates the
hint on the field and the scheduler reconciles overdue events once play
returns to the field. The desktop simulator has an indexed persistent
queue, a four-transition budget per call, stable report IDs, and a
two-day expiry for unfinished chains. Clock progress is monotonic for
events within a save checkpoint. Local daily activity follows the most
recent ROM clock reading. Existing checkpoints restore their own world
clock and observations.

The first Pallet relay still requires Watts's verified follower
observation and the guide's matching hearsay record. The new chain
validates each sender's knowledge before allowing a recipient to learn
the report. The event preserves the original source and recipient
knowledge preserves immediate provenance. Each successful new handoff
adjusts familiarity, trust, affinity and shared experiences once. The
scout's curiosity permits the handoff. The student's caution triggers
review of an unverified public note. A repeat or expired task cannot
create additional firsthand evidence. The known campaign can generate
two report chains, one for each supported species. The synthetic harness
uses the same queue implementation with a larger configured roster.

The two map residents stay on their own maps. Cross-map travel is an
off-screen delivery estimate for the reports. The visible guests use
their original wandering bounds, object-event slots and collision checks.
The game gates new walk steps by the clock, and existing engine scripts
control cutscenes, tutorials, freezes and in-progress movement. No new
movement command crosses the bridge. The two map scripts retain their
original dialogue, then offer a validated aside.

Phase 6's state, predictive cache and hybrid routing remain in use.
Routine activity and received evidence change the affected dialogue key.
The production scheduler invokes no model. The existing single worker
serves visible decisions such as the Pond Survey and the guide's
clarification choice. Routine foreground replies bypass obsolete
speculation. A new foreground model request can still queue behind one
running speculative job. Interrupting the existing worker would require
restarting its process and reloading weights, so this build keeps the
Phase 6 priority behavior.

## Verification

The harness ran seven accelerated days with seeded randomized starting
hours. Work counts include report deliveries, shift-gated review
starts, and review completions. Each run includes duplicate submission
attempts, provenance and relationship checks, and reopening the save.
The memory column reports peak Python allocation during the run and
excludes the interpreter and SQLite native allocations. The DB column
includes the existing save schema. Reference machine was Linux, AMD
EPYC 9V74 with nine logical CPUs exposed.

| Synthetic NPCs | Completed events | Transitions | CPU time | Tick p95 | Python peak | DB size |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 10 | 6 | 23 | 0.115 s | 0.104 ms | 83 KiB | 80 KiB |
| 50 | 32 | 113 | 0.092 s | 0.079 ms | 83 KiB | 148 KiB |
| 100 | 66 | 240 | 0.112 s | 0.161 ms | 86 KiB | 236 KiB |
| 250 | 166 | 603 | 0.173 s | 0.249 ms | 85 KiB | 484 KiB |

The runs recorded zero duplicate events and zero inference calls. The
harness also verifies clock rollback, cooldown and expiry, night
interruption, checkpoint branching, attribution and cache selectivity.
In a separate 200-hit and 200-miss dialogue run, the median routine hit
was 0.053 ms and the median miss was 0.62 ms. The existing foreground
Qwen routes took 0.87–1.10 s on two fresh survey decisions and
1.84–2.12 s on four guide replies. All eight scripted choices,
including two prepared survey decisions, matched the expected action.

The mGBA fixture uses real field objects, stock clock offsets, scripted
location setup and the production scheduler. It records daylight walking,
an occupied-tile collision check, stationary night behavior, attribution
in Route 1 and Viridian, and re-opens the sidecar from the mGBA battery
key. An initial assertion incorrectly expected a one-tile wander radius
in Viridian. The map defines a two-tile radius, so the assertion now
uses the actual allowed range.
The save-reopen fixture also found that companion facts could displace
the attributed note after a new firsthand sighting. These two residents
now rank received local news first, while preserving the access checks.
Two older story fixtures still named the retired gift command. They
now invoke the maintained gift command with the same fixture arguments.
The preserved Phase 6 coverage includes
PokéGlass, the V3 palette repair, follower-sensitive caching and guarded
model and script paths. The Linux worker probe denies network, process,
and unrelated file access. The Windows archives retain the same sandbox
and inference worker. Native Windows offline play, AppContainer
behavior, and long native playthroughs remain unverified.

Run `python3 tests/living_world_routines.py` for the scheduler suite.
Run the existing `tests/living_world_bridge_emulator.py` integration
with `LIVING_WORLD_ROUTINES_TEST=1` and a freshly built knowledge catalog.
Use both `ADVENTURE_TEST_MODE=0` and `ADVENTURE_TEST_MODE=1` for the Classic
and Quantum cases. The mGBA screenshot output contains the raw
`phase7-*.png` frames.

Phase 7 remains scoped to three Kanto maps and two visible walkers.
Expanded social roles, dynamic routing of physical sprites between
maps, and behavior outside this connected test area are future work.
