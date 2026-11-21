# Phase 9 · Pewter Society

## Play the demo

Extract the Windows package and launch **Play Pewter Society Demo.cmd**.
Choose **Continue**. This demo uses a separate battery slot, starts outside
Pewter Gym with PokéGlass, and arranges a Museum working shift at any clock
hour. Routine changes take game-clock time. Leave the field running for
about a minute, or explore the northern Route 2 path and return. NPCs do
not require an interaction to make decisions. The Bug Catcher may take a
field practice trip. Museum staff may accept or decline a second check.
Brock can consider a report only when a legitimate request reaches him.

When Brock travels, ask the Gym attendant and read both pages to discover
**Locate Brock**. Open the PokéGlass Quest Book and select the optional
objective. Its entry updates as the situation changes. You may speak to
Brock in the Museum forecourt, east of the front door, or check the Gym
after his return. If a report never reaches him or duty takes precedence,
the normal Gym challenge is available. The data log records those
different outcomes. Use **Play.cmd** to launch your ordinary save.
The older **Play Pewter World Demo.cmd** still isolates Phase 8.

## Milestones

| Milestone | Main files and behavior | Verification |
| --- | --- | --- |
| 9A · `2a04d92` | `society.py`, `world.py`, `play.py` and packager add save-local planning, independent of dialogue | Real Qwen chose a Museum visit for Brock and an independent investigation for the researcher. An offscreen decision, invalid plan and stale checkpoint were exercised. |
| 9B · `ac13c97` | `society.py`, `director.py`, and host routing add five roles, requests, action composition, commitments and attributed reports | Deterministic cooperation returned a report. Qwen chose to investigate and request assistance, and made separate roster decisions. |
| 9C · `cf96bed` | Map, projection and spawn hooks add the Pewter–Route 2 boundary and two roaming actors | Both adventure modes exercised trainer absence, safe arrival on a cleared tile, exclusive presence, and return. |
| 9D · `3b4c352` | `dynamic_quests.py`, the bridge and `poke_glass_quests.inc` add a runtime-only Book row | Both modes showed the active and completed objective, rejected malformed provenance, and preserved all 144 static record bytes. |
| 9E | Release scheduling, attributed society dialogue, replay and soak harnesses, packaged demo | Real decision samples, deterministic replays, native emulator regressions, and package checks below. |

## Architecture and authority

Brock retains the Phase 8 Director and protected challenge. The researcher,
assistant, Bug Catcher and attendant have distinct roles, duties, opening
hours, motives, independent decision tickets, commitments, personal facts,
and relationship counters. A verified shared result changes a relationship
once. Trust from earlier successful work can influence willingness to take
a request near the end of a shift. Replies from the assistant and trainer
use their own evidence. A report identifies its source and remains a
report even if the receiver has other firsthand knowledge.

The engine assembles small candidate sequences from the action vocabulary.
The shared, quantized Qwen3 0.6B worker chooses a label for a candidate.
Step targets and availability are engine-owned. Acceptance checks the
save key and decision context. The simulation revalidates permission,
source, meeting, location, travel, and deadlines as steps run. No agent
creates game items or triggers battles, flags, or executable commands.
Malformed, timed-out, and stale decisions recover to normal duty or a
conservative response to an outstanding request.

Pewter's Museum and Gym exchange messages between named contacts. A
cooperative plan may accept, book a meeting, visit, investigate, and
return its findings. The Director interprets these as local logical
meetings, with no relocation of the staff sprites. Physical relocation
is implemented for Brock and the Bug Catcher. The latter can leave Pewter
for (7,6) at the north end of Route 2 through its direct border connection.
There is no Cut, ticket, eastern Pewter, or Mt. Moon bypass. The ROM
reconciles four approved slots after safe field frames using exclusive
timed position codes and occupied-tile checks. With stale or absent host
presence, these characters default to their original maps.

The SQLite sidecar carries `society_state` and the Phase 8 Director
snapshot using the battery checkpoint key. Two-way work uses stable day,
sender, topic and recipient identifiers. The log keeps 48 recent events,
each agent retains eight recent entries, and the directed request table
is capped at 12. Branch loads restore their saved version. During play
the host advances timed events offscreen after the first Pewter visit.
Long forward skips expire overdue commitments and clock rollback returns
agents to duty. Routine activities and presentation do not invoke Qwen.

The Quest Book only displays a validated, player-discovered objective,
with an event ID and source from the Director. The row is read-only and
uses display text compiled into the ROM. The seven authored definitions,
save bytes, tracking and claim paths still use the original subsystem.
There is no model-defined quest, reward or new native save structure.

## Measured results

On AMD EPYC Linux, live Qwen accepted a request when the desk had time
and declined the equivalent request near closing. These two samples
included one cold call. They took 2.49 and 1.49 seconds respectively.
The deterministic engine completed the accepted meeting and independently
recorded the assistant's finding. Early testing exposed a tendency for
Qwen to decline either request when given internal action IDs. Short,
human-readable choice labels improved the paired case. This is a small
sample of model behavior.

A deterministic policy replayed 120 seeded circumstances with distinct
shift timing, prior relationships and existing Gym commitments. The
scenarios produced 73 Brock outings, 12 choices to honor an existing Gym
commitment, 164 resolved and 41 declined requests, and 17 discovered
objectives completed. All 120 recovered to an available Gym. Checkpoints
were copied and reopened mid-run. Tick p95 was 1.18 ms under tracing, CPU
time was 1.97 seconds and the combined database was about 2 MiB. The
100-day single-save soak reached 100 research checks, retained its bounds
and reopened correctly with a 108 KiB database.

The existing seven-day scaling harness reran synthetic populations of
10, 50, 100 and 250. At 250 it measured 0.248 ms p95, 500 KiB SQLite,
about 91 KiB peak traced Python allocation and zero duplicate events.
This harness scales the Phase 7 scheduler and includes a Brock workload.
It does not simulate 250 simultaneous model-driven agents. The live host
records queue wait separately from decision latency. Only one background
decision can be pending. New foreground dialogue retains priority over
queued work, and can still wait behind an in-flight inference.

## Regression and reproduction

The release builds and runs Classic and Quantum mGBA tests for Bag,
Quest Book, Brock, the Route 2 projection, live objectives, the Pallet
bridge, protected progression, and the previous story paths. The
standalone Quest Book suite covers a real aide offer, Route 1 event,
full-bag retry, exactly-once rewards and Flash persistence. The native
Brock test starts the actual battle and tests the original victory
continuation in a separate fixture. It does not play a complete battle.

From the repo root, build with `make -j8`, set `ARM_NM` and `MGBA_CORE`
for the GBA toolchain and mGBA libretro core, then run:

- `python -B tests/living_world_society.py` and `python -B tests/living_world_society_replay.py`
- Set `LIVING_WORLD_PHASE5_RUNTIME` to the local bundled-model runtime for real inference.
- `python -B tests/living_world_routines.py`
- Run `living_world_travel_emulator.py` and `living_world_brock_emulator.py` with `ADVENTURE_TEST_MODE=0` and `1`.
- Run `living_world_quest_book_emulator.py` and `pokeglass_bag_quest_qc_emulator.py` with `QUEST_QC_ADVENTURE=0` and `1`.
- Set `LIVING_WORLD_PEWTER_FIXTURE=1` for the Brock test to generate both Pewter demo saves.
- Place the fixtures beside the pinned packaging inputs and run `experiments/living_world/package-windows.py`.

There are five agent identities, two physically relocating sprites, and
one integrated dynamic quest type. Cross-region roaming, continuous
tile walking between maps, and a complete native Windows run are
outside the tested release. The distribution retains the existing local
worker isolation. Native AppContainer behavior remains unverified.
