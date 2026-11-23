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
