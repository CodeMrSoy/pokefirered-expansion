# Phase 4 · Pallet Town social simulation

## Play the Windows demo

Extract the standalone x64 ZIP and open **Play Pallet Social Demo.cmd**. For an
existing Pallet Expansion or Phase 3 installation, use the smaller update ZIP
and extract it over that directory. Allow replacement of the ROM and manifest
as a pair. The social demo keeps its own save under
`%LOCALAPPDATA%\LivingQuantumWorld`; the main adventure and earlier Pallet
demo keep their own slots. Windows 10 or 11 x64 is the target.

1. At the title screen, press Enter and select **Continue** with Z. Walk a few
   steps to bring Pikachu out. Speak to Watts, the PC enthusiast by the
   southern pond, and let him finish.
2. Walk toward the **Pallet Town sign** in the middle of town, above and left
   of the pond. A sighting is shared after a four-second delay even if you
   skip the sign. Read the sign and advance past the normal sign text with Z
   to see the short Watts/guide exchange. The sign plays each new exchange
   once.
3. In PokéGlass, put Squirtle in the lead slot and walk until it is out. Talk
   to the woman near the southwest Trainer Tips sign. Advance past her stock
   line. She can say **Watts saw your Pikachu** even with Squirtle in view.
   You can close and relaunch before seeing either scene. The report remains
   in the social demo's save history.
4. Open Command Prompt in the game folder. With Windows networking disabled,
   run `Play.cmd --sandbox-test` and `Play.cmd --model-test`. The sandbox check
   should report four denials. Repeat the social demo with networking disabled
   and inspect `dialogue.jsonl` for an entry with a `social` object and
   subsequent dialogue containing the corresponding fact ID.

## Simulation and boundaries

Phase 4 cherry-picks V3's PokéGlass time-of-day repair (`cd274cc4`). Existing
Pallet voices, player relationship memory, and the Pond Survey stay in use.

A validated Watts encounter can queue a local sighting of Pikachu or
Squirtle. The scheduler wakes only for a due event and processes at most one
event per frame. It queues each supported species once per battery-save
history, with a 12-second spacing between reports. Its transaction checks
the original witness, participants, mutual contact, locality, trust, and
allowlisted species. It records the event, gives the guide a sourced report
without marking it first-hand, and updates directional trust, familiarity,
affinity, shared experiences, and follow-up goals. The guide's conversation
consumes this evidence through the existing knowledge catalog. Other NPCs
receive no report. Hearsay cannot be used as a witness or automatically
relayed again. Pending events, reports, relationships and the presentation
marker follow the existing battery checkpoint and save slot isolation.

The visible scene uses the town sign's optional text box. Its species comes
from the completed event. No NPC pathfinding or forced story cutscene is
involved. The demo represents one cooperative relationship. It does not
simulate general-purpose gossip, conflicts, rivalry, or daily schedules.
Local AI remains available for the player-facing dialogue, and it cannot
approve the transfer or write outside the validated mailbox response slot.
When inference is pending, game frames, rendering, and window input
continue. The conversation still holds ordinary field controls until its
reply or fallback.

## Verification and measurements

The ROM compiled, and the V3 Party return checks passed 12 repeated
transitions. Day, evening and night palette comparisons passed outdoors and
indoors, including a rainy map. Real-model mGBA runs in Classic and Quantum
showed the same recorded event at the sign, then an attributed guide reply
without the follower present after a database reopen. Both modes checked
deferred frame advancement, worker failure, the ROM timeout, protected
scripts and normal input release. Tests also cover persistence, rollback,
cooldown, unauthorized recipients and duplicate prevention.

| Linux measurements | Baseline | With 5,000 simulated NPC bonds and queued events |
| --- | ---: | ---: |
| CPU per idle scheduler check | 0.072 µs | 0.046 µs |
| Witness and scheduling, p95 | 0.226 ms | 0.207 ms |
| Transfer and memory, p95 | 0.241 ms | 0.207 ms |

These timings are from 100 durable SQLite transfers per case and 250,000
idle checks. Ordinary Pallet gameplay through SDL/mGBA used about 2.1–2.2 ms
of host CPU per frame in the dummy display test, with idle simulation
enabled and disabled measured separately. One cold player-facing exchange
including the renderer handoff took 3.43 s. The scripted GBA tests separately
verified that the emulator kept running while awaiting a real reply.

| CPU model, isolated worker | Warm inference per social benchmark case | Worker RSS |
| --- | ---: | ---: |
| Qwen2.5 0.5B Q4_0 | 0.75–1.29 s | 687 MiB |
| SmolLM2 360M benchmark GGUF | 1.07–1.55 s | 348 MiB |
| Qwen2.5 1.5B benchmark GGUF | 2.42–3.18 s | 1,765 MiB |

All three sometimes produced incomplete or poorly attributed free text and
all chose to send hearsay in the action benchmark. The playable build
therefore retains the 0.5B model, approved dialogue choices and
deterministic transfer rules. GPU inference was unavailable in the test
environment. The Linux worker probe denied sockets, execution and unrelated
file reads and writes. The Windows archives were built and checked from
Linux. Native AppContainer execution, Windows performance and an offline
Windows playthrough remain unverified.

For repeatable social tests, run `python3 tests/living_world_social.py`.
See [Phase 3](PHASE3.md) for emulator setup. Use the same worker and catalog
environment variables for the Phase 4 social assertions. To generate the
dedicated battery fixture for packaging, run the mGBA test with
`LIVING_WORLD_TEST_SAVE=/path/to/staging/PalletSocialTest.sav` and
`LIVING_WORLD_SOCIAL_FIXTURE=1`.
