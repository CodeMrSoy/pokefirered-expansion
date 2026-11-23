# Phase 18 initialization benchmark

The benchmark drives the actual Quantum New Game menu once per case. It measures disabled randomization and three distinct native seeds with all supported randomizer options enabled, including Items and Vidra Gyms. Each timed trial starts with a fresh companion directory. The player core runs at approximately normal cadence during initialization. A native Flash save and native Continue supply the fixture states.

| Report field | Timed operation |
| --- | --- |
| `replica_startup` | Read the catalog, ROM and frozen state in the child, validate the build and open the isolated mGBA replica |
| `native_resolution` | Issue requests and read native replies for encounters, abilities, moves, trainers and static encounters |
| `manifest_assembly` | Assemble and validate the hashed manifest, excluding native query and progress writes |
| `database_initialization` | Import the manifest and commit the initial simulation database |
| `save_association` | Write native Flash to disk and commit the paired snapshot at the first save |
| `new_game_ready` | Elapsed time from the first launcher poll with finalized New Game context through publication of the ready database |
| `continue_ready` | Verify and restore a newly paired companion world after the ROM publishes Continue context |

The raw report also separates progress writes and launcher overhead. New Game timing covers child process startup and shutdown. Save association happens when the player makes a save. Menu navigation, the Oak introduction, the initial application launch, and the native menu wait before Continue are outside these measurements. Continue uses a fresh world checkpoint. Long-running worlds and concurrent AI inference should be measured in a later Windows pass if they affect the loading-screen decision.

## Reference measurements

The Phase 17 release ROM (`cb5ed66a`) ran on a Linux AMD EPYC 9V74 host with mGBA libretro. Each case ran seven times. Values are median / slowest observed, in milliseconds.

| Randomizer setting and seed | New Game ready | Continue |
| --- | ---: | ---: |
| Off, `00000000` | 737 / 972 | 108 / 155 |
| Fully enabled, `1df46bd4` | 1,122 / 1,307 | 116 / 128 |
| Fully enabled, `8eccae66` | 1,206 / 1,391 | 110 / 150 |
| Fully enabled, `9fcd6b41` | 1,256 / 1,327 | 107 / 130 |

Fully enabled trials spent a median of 561 ms on native resolution, 305 ms on replica startup, 99 ms on manifest assembly, and 79 ms on database initialization. First save association took 118 ms median. The slowest sum of New Game and first save timings from the same trial was 1,513 ms. The intended Windows machine still needs to run the benchmark.

## Reproduce on the target Windows PC

Use Python 3.12 with Pillow and NumPy, the ARM GNU binutils, and the exact source revision's compiled `pokefirered.gba` and `pokefirered.elf` in the repository root. Use the same `mgba_libretro.dll` that ships in the Windows package. The benchmark uses disposable profiles and never opens the active player profile.

```powershell
$env:ARM_NM = 'C:\arm-toolchain\bin\arm-none-eabi-nm'
$env:MGBA_CORE = 'C:\LivingQuantumWorld\mgba_libretro.dll'
python -B experiments/living_world/build-world-catalog.py pokefirered.gba pokefirered.elf world-catalog.json --nm $env:ARM_NM
python -B tests/living_world_init_benchmark.py world-catalog.json Quantum_Phase18_Windows_Benchmark.json --trials 7
```

Compare the median and slowest observed trial per seed. Keep initialization in the background if the slowest Windows case stays under two seconds. Revisit the transition decision if the Windows timings cross that threshold.

## Live world synchronization

The Living World development branch starts at the published Phase 17 release
(`cb5ed66a`) plus the benchmark. The Phase 16 tip is an ancestor. The local
Phase 15 through Infrastructure predecessors include branch-specific commits,
so their historical refs remain available. `Pokemon-Quantum-V3` was inspected
separately and kept outside this integration.

The GBA publishes 64-byte versioned records to a 48-entry ring in EWRAM. The
emulator client only reads the ring. A VBlank heartbeat and monotonically
increasing sequence distinguish frame gaps, ring overwrite, and detectable
external rollback. Start records come after actual opponent construction and
initial form changes. Capture events come after the normal party/PC handoff.
The capture-ball failure path records the native ball ID after the failed roll.
End events report the native outcome. Field observations track map, selected
story flags, and material party changes. Evolution records include the previous
native species and the resulting individual attributes.

The live path copies events off the core at the normal frame boundary. A
bounded queue waits for the Phase 17 database to become ready, then a single
background worker commits events, projections, and acknowledgments. It advances
the existing simulation at one hour per 3,600 native frames. The native frame
remainder is paired with Flash to preserve the phase of the clock on Continue.
Legacy offline dialogue and scheduling retain their existing entry points.
Only a uniquely mapped trainer on the battle map can learn what that trainer
actually fielded. Wild sightings, player party data, and hidden flags are
available to the host journal. There is no broadcast of those facts to NPCs.

The `native_event_journal` SQLite view exposes event ID, world UUID, manifest
digest, originating Flash checkpoint, stream, sequence, native event, current
acknowledgment, and simulation tick. Exact duplicate payloads are ignored;
divergent payloads or sequence gaps quarantine the attachment. A real save
marker must match the checksummed native Flash counter. The background worker
archives the SQLite snapshot through that marker. Continue reopens a fresh
copy of the exact archived pair. When the native Quest Log plays a recap,
the handoff waits for the recap to close and the saved field to be playable. Journal writes beyond that checkpoint remain
in the prior working copy. The launcher's backup now includes the immutable
paired checkpoint archive.

Wild and trainer individuals are scoped to battle and slot. Successful captures
link the battle identity to the player's observed OT ID, personality, and IVs.
A later party record updates the same individual. Species IDs include native
forms. The observed ownership record describes the last confirmed state, and
party membership is tracked separately. A party disappearance can mean
reordering, PC deposit, trade or release. Phase 18 does not infer which
happened or claim to enumerate the PC. Link, recorded and tutorial battles
are excluded. Special battle paths that bypass normal end finalization may have
start observations with no outcome. Story telemetry is intentionally limited
to badges, acquiring a starter, game clear, Koga's return, and the Safari
Stellar Ticket.

After a detectable external save-state discontinuity, native gameplay continues
and the companion stops accepting events or checkpoints until a fresh launch.
A save from a different build can still load in the ROM. Companion pairing
requires the exact catalog and matching Flash, so older Phase 17 companion
archives need a separate migration tool. Phase 18 supplies no writes to native
encounter probabilities, battle rosters, or progression flags and has no
loading screen.

### Native regression and performance

Run `tests/living_world_live_emulator.py` with the matching ROM, catalog,
mGBA libretro core, and ARM GNU binutils. The suite runs a real wild battle,
throws a low-probability ball and a Master Ball through the native bag, battles
the protected Pewter practice trainer and Havora Dock Crew, warps between
maps, saves Flash, and re-enters Continue. The extended test adds 11,000 native
frames and reports host polling, receive-to-commit latency, SQLite time,
simulation time, checkpoint time, and resident memory. Timings cover the
actual host path and use a headless display. Repeat under SDL on target Windows
hardware to evaluate visible frame pacing.

The attached-host and no-host control use the same instrumented ROM and the
same input trace. The recorder is always built into the ROM. A separate,
unsupported debug experiment can zero the native recorder magic. That removes
native work and may alter the VBlank-dependent RNG stream. It is not a
supported player option and exact parity against a recorder-free ROM has not
been established. The recorder makes no calls to the gameplay RNG.

This milestone's packaged Windows smoke exercises the observation ABI and
reports replica timings. The multi-seed benchmark and actual frame pacing
still require a run on suitable Windows hardware.
