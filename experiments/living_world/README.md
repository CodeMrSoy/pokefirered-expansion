# Living Quantum World

This branch starts from Pokémon Quantum V3 at `c3a7e53bed3055d9d78a3a28e55db907661efa97`. Its first slice uses the existing PC-storage conversation in Pallet Town. The guest exports an NPC identifier and the species of an onscreen follower, if present, after the player has received the Pokédex. An mGBA host can return up to two short pages. If it stays silent, returns unusable text, or replies with the wrong sequence, the ROM falls back to the original PC-storage tip within 30 script ticks. The desktop player runs an offline Qwen3-0.6B model through llama.cpp. The test can use either the actual worker or a deterministic responder.

## V3 Bag and Quest Book integration

The V3 changes through `0dedb6d` are merged into Living World. The grid Bag,
Quest Book app and inventory reordering fixes coexist with the current NPC
routines, dialogue bridge and Brock travel code. Oak's first aide completes
his Living World aside before offering the engine-owned Field Notes quest.
A button-release guard prevents a dialogue-advance press from accepting it.
Host permissions and existing host-managed objectives retain their own flow.
See [integration checks](../../docs/v3/living-world-merge-2026-11-21.md).

## Run the bridge in mGBA

Build the standard FireRed target with the repository's [build prerequisites](../../INSTALL.md). Use the mGBA libretro core and the Python dependencies for the existing emulator harness (Pillow and NumPy). Run these commands from the repository root with the toolchain on PATH.

```sh
make -j
export MGBA_CORE=/path/to/mgba_libretro.so
export ARM_NM=arm-none-eabi-nm
ADVENTURE_TEST_MODE=0 python3 tests/living_world_bridge_emulator.py
ADVENTURE_TEST_MODE=1 python3 tests/living_world_bridge_emulator.py
```

Mode 0 is Classic and mode 1 is Quantum. The harness runs the compiled map event through the field script interpreter and verifies the resulting text buffer. Its JSON lines show request context, proposals, host validation, response writes, elapsed time and, for successful cases, the rendered text. Set `LIVING_WORLD_INFERENCE_RUNTIME` to run with the actual worker. The emulator trace measures the host handoff and frames to the text buffer. The desktop log also records model load, inference and IPC overhead. The [playtest guide](PLAYTEST.md) covers the packaged desktop launcher. See [Phase 7](PHASE7.md) for regional routines, automation results and the Windows playtest. See [Phase 2](PHASE2.md) for model comparisons and the Pond Survey, and [Phase 3](PHASE3.md) for the offline catalog, knowledge boundaries, and benchmark results.

[Phase 8](PHASE8.md) covers the Pewter World Director, Brock’s optional objective and the Pewter demo.
[Phase 9](PHASE9.md) covers Pewter Society. [Phase 10](PHASE10.md) covers composed plans,
regional travel, two dynamic PokéGlass entries and the offline demo.

### Build the offline worker and Windows package

Build [llama.cpp b6500](https://github.com/ggml-org/llama.cpp/tree/b6500) without CURL, GPU backends or OpenMP. Link `offline-worker.cpp` against llama, ggml, ggml-cpu and ggml-base. On Linux also link `sandbox-linux.c` and keep the supplied worker single-threaded. The worker installs a seccomp allowlist after loading the trusted GGUF and before tokenizing the prompt. Compile `security_probe.c` with the same Linux isolation code and run it against a disposable file outside the worker directory.

For Windows x64, build the same CPU-only libraries statically, link the worker with Unicode entry point support, compile `sandbox-win.c` with Userenv and Advapi32, and compile the probe with Winsock. Place the resulting `offline-worker.exe`, `sandbox.exe`, and `sandbox-probe.exe` in the staging directory. The wrapper launches inference with AppContainer security capabilities, a child-process restriction, and a job that kills its only allowed process on close. It grants the AppContainer read and execute access to the packaged inference directory. It passes only input/output handles. The desktop player continues emulating while inference runs. The worker timeout is eight seconds, and failure releases the ROM back to the stock tip.

Place the pinned Qwen GGUF and the mGBA, SDL2, and embedded Python archives in the staging directory under the names listed in `package-windows.py`. Also supply the license texts under `licenses` and run the emulator integration test with `LIVING_WORLD_TEST_SAVE=/path/to/staging/PalletTest.sav` to create the demo save. After building the ROM in the normal way, run `python3 experiments/living_world/package-windows.py /path/to/staging Living-Quantum-World-Windows-x64.zip`. The packager checks the upstream inputs and binds the ROM hash to the mailbox symbol from the same ELF.

### Mailbox

Use the symbol `gLivingWorldMailbox` from the ELF paired with the loaded ROM. The reference host validates the region and uses little-endian fields. Call its synchronous poll between frames with a fast test responder. It reads the 12-byte request header and writes within the response slot only.

| Offset | Size | Field |
| --- | ---: | --- |
| 0 | 4 | Request marker `LQW1`, cleared on completion or timeout |
| 4 | 4 | Request sequence |
| 8 | 2 | Stable NPC ID from `include/constants/living_world.h` |
| 10 | 2 | Visible follower species ID, or zero |
| 12 | 4 | Response sequence, written last |
| 16 | 1 | Response text length |
| 17 | 115 | Plain ASCII dialogue, up to two lines per page and one form-feed page break |


The host accepts the exact JSON shape `{"action":"SAY_DIALOGUE","text":"..."}`. The ROM independently encodes an allowlist of plain characters and checks field-font pixel width before displaying text. The only outcome of a valid message is dialogue. The protocol has no operation for state mutation. The test and desktop frontend publish on the emulator thread. The desktop frontend polls worker results between emulator frames. Reset, ROM switching and save-state rewind would require invalidating outstanding replies before resuming a different game state.

## Pallet Town NPC audit

Sources are the map objects and associated scripts under [data/maps](../../data/maps). Oak's outdoor event and lab object represent the same character. Starter balls, Pokédex props and the Town Map are map objects without NPC profiles. The player's upstairs room has no NPC object.

| NPC | Existing script or map role | Proposed personality, goal and preference | Knowledge and protected behavior |
| --- | --- | --- | --- |
| Professor Oak | Town Oak trigger and lab `ProfOak` | Curious, encouraging, occasionally absent-minded. Advance research and encourage new Trainers. Nidorino. | Direct research conversations and Pokémon he has seen. Preserve the opening interception, starter scene, parcel, Pokédex, PokéGlass, items and Dex ratings. |
| Blue | Lab `Rival` and rival battle scripts | Proud, observant and competitive. Become the strongest and surpass the player. Pidgeot. | His own fights and Pokémon he has seen. Preserve starter selection, mandatory battles, teams, scheduled appearances and progression. |
| Daisy | Rival's house `Daisy` | Sociable and supportive. Stay close to family and help local Trainers. Clefairy. | Direct conversations and Pokémon shown for grooming or observation. Preserve the Town Map, grooming, friendship ratings and existing rewards. |
| Mom | Player's house 1F `Mom` | Warm and practical. Keep the player safe and encourage independence. Chansey. | Family interactions and Pokémon the player shows her. Preserve the opening directions and healing. |
| Sign guide | Town `SignLady` and tutorial triggers | Eager and civic-minded. Help newcomers read town signs and learn to navigate. Pidgey. | Local signs and conversations she witnessed. Preserve the tutorial, movements and triggers. |
| PC-storage resident | Town `FatMan` | Watts is practical and friendly. Keep Pallet's computers working and compare notes on local Pokemon. Pikachu. | Pallet's public landmarks, direct interactions, and visible followers. The first bridge uses this event and falls back to the original tip. |
| Lab aide 1 | Lab `Aide1`, scientist at local object 1 | Methodical. Improve research records and explain Oak's public work. Magnemite. | Lab work and public announcements. Preserve the postgame radio dialogue and Oak Fame Checker event. |
| Lab aide 2 | Lab `Aide2`, scientist at local object 3 | Considerate. Improve Pokémon care at the lab and share grooming advice. Vulpix. | Local care work and reported observations. Preserve the postgame Daisy dialogue and Fame Checker event. |
| Lab aide 3 | Lab `Aide3`, worker at local object 2 | Inquisitive and outgoing. Explain Oak's research and encourage visitors. Oddish. | Public research and lab activity. Preserve the Oak Fame Checker event. |

All nine audited NPCs have profiles. Watts retains the optional survey. The
other eight can offer short asides and remember a visible follower they saw.
They cannot offer quests, change trust, or affect items, maps, battles or
story state through the host bridge.

## Optional Pallet conversations

The additional NPCs finish their original dialogue or service before the host
can supply an aside. All asides require the Pokédex and skip quest-log playback.
With a missing or rejected reply, the script ends after the original dialogue.

- Daisy can add a remark to her casual conversations. Her Town Map and grooming keep their original paths.
- Oak can add a remark after his ordinary Dex rating or when revisiting the lab after his completion thanks. The initial starter, parcel, and Pokédex sequences have no hook.
- Blue uses his existing lab object for an optional visit after the League clear and the Pokédex introduction. His starter and battle scripts have no hook.
- Mom can add a remark after healing. The sign guide can add one after finishing her tutorial.
- The lab aides can add remarks to their ordinary conversations. Their Fame Checker calls and special postgame paths remain in their scripts.

Classic and Quantum mGBA tests exercised all nine NPC IDs, Blue's postgame
return, early protected branches, and the Town Map gift. Native Windows
playtesting of the updated ROM and host is pending.
