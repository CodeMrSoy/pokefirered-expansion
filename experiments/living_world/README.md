# Living Quantum World

This branch starts from Pokémon Quantum V3 at `c3a7e53bed3055d9d78a3a28e55db907661efa97`. Its first slice uses the existing PC-storage conversation in Pallet Town. The guest exports an NPC identifier and the species of an onscreen follower, if present, after the player has received the Pokédex. An mGBA host can return two short lines. If it stays silent, returns unusable text, or replies with the wrong sequence, the ROM falls back to the original PC-storage tip within 30 script ticks. The desktop player runs an offline Qwen2.5-0.5B-Instruct model through llama.cpp. The test can use either the actual worker or a deterministic responder.

## Run the bridge in mGBA

Build the standard FireRed target with the repository's [build prerequisites](../../INSTALL.md). Use the mGBA libretro core and the Python dependencies for the existing emulator harness (Pillow and NumPy). Run these commands from the repository root with the toolchain on PATH.

```sh
make -j
export MGBA_CORE=/path/to/mgba_libretro.so
export ARM_NM=arm-none-eabi-nm
ADVENTURE_TEST_MODE=0 python3 tests/living_world_bridge_emulator.py
ADVENTURE_TEST_MODE=1 python3 tests/living_world_bridge_emulator.py
```

Mode 0 is Classic and mode 1 is Quantum. The harness runs the compiled map event through the field script interpreter and verifies the resulting text buffer. Its JSON lines show request context, proposals, host validation, response writes, elapsed time and, for successful cases, the rendered text. Set `LIVING_WORLD_INFERENCE_RUNTIME` to run with the actual worker. The emulator trace measures the host handoff and frames to the text buffer. The desktop log also records model load, inference and IPC overhead. The [playtest guide](PLAYTEST.md) covers the packaged desktop launcher. See [Phase 2](PHASE2.md) for model comparisons, persistent memory, the Pond Survey and its structured inspection log.

### Build the offline worker and Windows package

Build [llama.cpp b6500](https://github.com/ggml-org/llama.cpp/tree/b6500) without CURL, GPU backends or OpenMP. Link `offline-worker.cpp` against llama, ggml, ggml-cpu and ggml-base. On Linux also link `sandbox-linux.c` and keep the supplied worker single-threaded. The worker installs a seccomp allowlist after loading the trusted GGUF and before tokenizing the prompt. Compile `security_probe.c` with the same Linux isolation code and run it against a disposable file outside the worker directory.

For Windows x64, build the same CPU-only libraries statically, link the worker with Unicode entry point support, compile `sandbox-win.c` with Userenv and Advapi32, and compile the probe with Winsock. Place the resulting `offline-worker.exe`, `sandbox.exe`, and `sandbox-probe.exe` in the staging directory. The wrapper launches inference with AppContainer security capabilities, a child-process restriction, and a job that kills its only allowed process on close. It grants the AppContainer read and execute access to the packaged inference directory. It passes only input/output handles. The desktop player pauses ROM execution during inference while continuing to process window events. The worker timeout is eight seconds, and failure releases the ROM back to the stock tip.

Place the pinned Qwen GGUF and the mGBA, SDL2, and embedded Python archives in the staging directory under the names listed in `package-windows.py`. Also supply the license texts under `licenses` and run the emulator integration test with `LIVING_WORLD_TEST_SAVE=/path/to/staging/PalletTest.sav` to create the demo save. After building the ROM in the normal way, run `python3 experiments/living_world/package-windows.py /path/to/staging Living-Quantum-World-Windows-x64.zip`. The packager checks the upstream inputs and binds the ROM hash to the mailbox symbol from the same ELF.

### Mailbox

Use the symbol `gLivingWorldMailbox` from the ELF paired with the loaded ROM. The reference host validates the region and uses little-endian fields. Call its synchronous poll between frames with a fast test responder. It reads the 12-byte request header and writes within the response slot only.

| Offset | Size | Field |
| --- | ---: | --- |
| 0 | 4 | Request marker `LQW1`, cleared on completion or timeout |
| 4 | 4 | Request sequence |
| 8 | 2 | Stable NPC ID, currently 1 for the PC-storage resident |
| 10 | 2 | Visible follower species ID, or zero |
| 12 | 4 | Response sequence, written last |
| 16 | 1 | Response text length |
| 17 | 57 | Plain ASCII dialogue with at most one line break |
| 74 | 2 | Alignment padding |

The host accepts the exact JSON shape `{"action":"SAY_DIALOGUE","text":"..."}`. The ROM independently encodes an allowlist of plain characters and checks field-font pixel width before displaying text. The only outcome of a valid message is dialogue. The protocol has no operation for state mutation. The test and desktop frontend publish on the emulator thread. The desktop frontend pauses emulation while its worker processes the current request. Reset, ROM switching and save-state rewind would require invalidating outstanding replies before resuming a different game state.

## Pallet Town NPC audit

Sources are the map objects and associated scripts under [data/maps](../../data/maps). Oak's outdoor event and lab object represent the same character. Starter balls, Pokédex props and the Town Map are map objects without NPC profiles. The player's upstairs room has no NPC object.

| NPC | Existing script or map role | Proposed personality, goal and preference | Knowledge and protected behavior |
| --- | --- | --- | --- |
| Professor Oak | Town Oak trigger and lab `ProfOak` | Curious, encouraging, occasionally absent-minded. Advance research and encourage new Trainers. Nidorino. | Direct research conversations and Pokémon he has seen. Preserve the opening interception, starter scene, parcel, Pokédex, PokéGlass, items and Dex ratings. |
| Blue | Lab `Rival` and rival battle scripts | Proud, observant and competitive. Become the strongest and surpass the player. Pidgeot. | His own fights and Pokémon he has seen. Preserve starter selection, mandatory battles, teams, scheduled appearances and progression. |
| Daisy | Rival's house `Daisy` | Sociable and supportive. Stay close to family and help local Trainers. Clefairy. | Direct conversations and Pokémon shown for grooming or observation. Preserve the Town Map, grooming, friendship ratings and existing rewards. |
| Mom | Player's house 1F `Mom` | Warm and practical. Keep the player safe and encourage independence. Chansey. | Family interactions and Pokémon the player shows her. Preserve the opening directions and healing. |
| Sign guide | Town `SignLady` and tutorial triggers | Eager and civic-minded. Help newcomers read town signs and learn to navigate. Pidgey. | Local signs and conversations she witnessed. Preserve the tutorial, movements and triggers. |
| PC-storage resident | Town `FatMan` | Enthusiastic and practical. Teach useful PC habits and collect examples for newcomers. Porygon. | Pallet's public landmarks, direct interactions, and visible followers. The first bridge uses this event and falls back to the original tip. |
| Lab aide 1 | Lab `Aide1`, scientist at local object 1 | Methodical. Improve research records and explain Oak's public work. Magnemite. | Lab work and public announcements. Preserve the postgame radio dialogue and Oak Fame Checker event. |
| Lab aide 2 | Lab `Aide2`, scientist at local object 3 | Considerate. Improve Pokémon care at the lab and share grooming advice. Vulpix. | Local care work and reported observations. Preserve the postgame Daisy dialogue and Fame Checker event. |
| Lab aide 3 | Lab `Aide3`, worker at local object 2 | Inquisitive and outgoing. Explain Oak's research and encourage visitors. Oddish. | Public research and lab activity. Preserve the Oak Fame Checker event. |

The audit describes **nine distinct NPCs** across the town and interiors. The profile concepts are proposed content. At Level 1, give each NPC only expression actions and put the hook in a freestanding conversation or after an existing script has completed its required work. Preserve mandatory text verbatim for the first expansion. New memory and relationship rules start with per-NPC baselines and consume only validated game observations.

## Next verification

Run the Phase 2 save, restart, survey and Windows isolation checks on a native
Windows machine before extending resident behavior to any other Pallet NPC.
