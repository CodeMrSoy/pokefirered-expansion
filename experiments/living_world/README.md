# Living Quantum World

This branch starts from Pokémon Quantum V3 at `c3a7e53bed3055d9d78a3a28e55db907661efa97`. Its first slice uses the existing PC-storage conversation in Pallet Town. The guest exports an NPC identifier and the species of an onscreen follower, if present, after the player has received the Pokédex. An mGBA host can return two short lines. If it stays silent, returns unusable text, or replies with the wrong sequence, the ROM falls back to the original PC-storage tip within 30 script ticks. The test uses a deterministic stand-in for inference.

## Run the bridge in mGBA

Build the standard FireRed target with the repository's [build prerequisites](../../INSTALL.md). Use the mGBA libretro core and the Python dependencies for the existing emulator harness (Pillow and NumPy). Run these commands from the repository root with the toolchain on PATH.

```sh
make -j
export MGBA_CORE=/path/to/mgba_libretro.so
export ARM_NM=arm-none-eabi-nm
ADVENTURE_TEST_MODE=0 python3 tests/living_world_bridge_emulator.py
ADVENTURE_TEST_MODE=1 python3 tests/living_world_bridge_emulator.py
```

Mode 0 is Classic and mode 1 is Quantum. The harness runs the compiled map event through the field script interpreter and verifies the resulting text buffer. Its JSON lines show request context, proposals, host validation, response writes, elapsed time and, for successful cases, the rendered text. The measured time is for the fixture and validation. A Windows launcher, a live model, SQLite, quest actions and the graphical inspection panel are future milestones.

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

The host accepts the exact JSON shape `{"action":"SAY_DIALOGUE","text":"..."}`. The ROM independently encodes an allowlist of plain characters and checks field-font pixel width before displaying text. The only outcome of a valid message is dialogue. The protocol has no operation for state mutation. The current synchronous fixture keeps emulation and transport on one thread. Before adding asynchronous inference, assign each outstanding request a host-side session generation and cancel it on reset, ROM change, or save-state load. Reject a response if its generation, ROM identity, or request no longer matches. Keep inference off the emulator thread and give the player a bounded wait with immediate fallback on worker failure.

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

## Next vertical slice

- **Local inference.** Benchmark a CPU-only llama.cpp worker with a pinned, bundled Qwen2.5-1.5B-Instruct Q4_K_M GGUF (1.12 GB of weights). Compare with a smaller model if latency or memory is impractical. Measure cold load, resident memory, warm p50 and p95, timeout rate and proposal rejection rate on Windows. A grammar constrains the response shape, and the application validator still enforces action permissions. See [Qwen's model files](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF/tree/main) and [llama.cpp grammars](https://github.com/ggml-org/llama.cpp/tree/master/grammars).
- **Windows host.** mGBA Lua is viable for manual development probes using frame callbacks and the memory API. Use a native mGBA core or libretro frontend for the portable application so the host owns frame timing, input and memory transport. Run the inference worker in a Windows AppContainer with no network capabilities, access only to packaged runtime assets and an inherited IPC channel. The worker receives no emulator, save or database handle. Add job limits and fail closed to stock dialogue if isolation fails. Verify launch, network denial and unrelated file denial on Windows before enabling real inference. See [mGBA's scripting API](https://mgba.io/docs/scripting.html), [native mGBA core API](https://github.com/mgba-emu/mgba/blob/master/include/mgba/core/core.h) and [Microsoft's AppContainer documentation](https://learn.microsoft.com/en-us/windows/win32/secauthz/appcontainer-isolation).
- **Memory and a first quest.** Enable Level 2 only for the PC-storage resident. Give the model two reachable fact-finding objectives drawn from existing town signs, such as checking the Trainer Tips sign or confirming the lab's location. Let the model choose or decline an objective based on what the player has already checked and supply the resident's reason. After player acceptance, only an actual sign interaction followed by a return visit can complete it. Limit the reward to a capped trust increase and a distinct follow-up conversation in the first test. Use engine-owned objective IDs and completion checks. Add an item reward only after the save and reward transaction can survive retries safely.
- **Persistence and tooling.** Put compact observations, bounded relationship values and quest records in SQLite. Tie records to the active battery-save slot and a host-managed checkpoint. Commit durable state with a recoverable save/checkpoint transaction and disable save-state rewind for this slice until database rollback can be paired with the ROM checkpoint. Record the prompt-visible facts, model revision, timing, proposal, validation result and applied effect in the developer panel. Compare outcomes across independent saves.
- **Packaging.** Produce a portable Windows directory with pinned runtime binaries, bundled weights, user-writeable dedicated save storage and atomic backups. Review notices and redistribution rights for mGBA, the inference stack, weights and game assets before release. If ROM redistribution rights are unavailable, distribute a patch and build a local ROM from a user-supplied compatible base during offline setup.
