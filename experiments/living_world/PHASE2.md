# Living World Phase 2

## A. Dialogue and performance

The desktop host keeps one worker and one model context alive. It clears the
inference context between requests. Framed requests and replies use the worker's
existing pipes. The demo prepares likely replies at startup and again after a
memory change. Replies are keyed by the observed follower and NPC state.

The same five scenarios ran through llama.cpp b6500 on one isolated Linux x86-64
CPU thread on an AMD EPYC 9V74. These are observed single-run ranges across three
different dialogue cases and two different decision cases, not percentiles. The
models were already downloaded and cached locally. Peak RSS is the worker's
VmHWM after all five scenarios.

| Model | GGUF bytes | Load | Peak RSS | Warm dialogue | Warm decision | Observed behavior |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| Qwen2.5 0.5B Instruct Q4_0 | 428,730,208 | 1.304 s | 698 MiB | 1.211–2.199 s | 0.829–1.000 s | Mentioned the pond. Repeated its memory line. Both broad action prompts returned SAY_DIALOGUE. |
| SmolLM2 360M Instruct Q4_K_M | 270,590,880 | 0.253 s | 351 MiB | 1.763–2.561 s | 1.189–1.298 s | Repeated phrases and clipped both first-visit lines. Both action prompts returned SAY_DIALOGUE. |
| Qwen2.5 1.5B Instruct Q4_K_M | 1,117,320,736 | 1.227 s | 1,775 MiB | 4.138–4.387 s | 2.434–3.155 s | Used more relevant details but clipped sentences under the same constraints. Both action prompts returned SAY_DIALOGUE. |

Keep the existing 0.5B model for this test. The 1.5B model's generation was
roughly twice as slow and still clipped its lines. The 360M model cut memory and
load time, with weaker results and slower warm replies on these scenarios.
The measurement used a permissive two-line grammar so instruction following
and mistakes remained visible. Phase 2 uses a narrower grammar with authored
phrases for coherent two-line text. The model chooses wording and the permitted
action in the same pass. This is still a constrained roleplay prototype.

A Phase 2 live-model run loaded once in 0.925 s. Five exchanges took
1.56–2.58 s of inference apiece. Measured pipe overhead was about 0.3–1.8 ms.
The emulator consumed prepared replies after two frames (about 34 ms at GBA
frame rate) into its text buffer. The in-game character print animation is
separate and remains governed by the player's text-speed setting. Native Windows
performance and GPU performance are unmeasured; this build has a CPU backend.

Reproduce the model comparison with local files:

```sh
python3 tests/living_world_benchmark.py /path/to/runtime baseline.gguf smol.gguf qwen15.gguf
```

The [Qwen 1.5B GGUF](https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF)
and [SmolLM2 GGUF](https://huggingface.co/bartowski/SmolLM2-360M-Instruct-GGUF)
are benchmark inputs only. Gameplay performs zero downloads.

## B. Personality and memory

Watts is the existing Pallet PC-storage resident. His profile defines his
voice, goals, favorite species and type, knowledge, and permitted actions.
The first encounter with each visible species records a deduplicated fact.
Later dialogue can acknowledge that encounter. Trust starts at zero and can
increase once for a first Pikachu encounter and once for completing the survey.

SQLite stores facts, trust, and quest state by battery-save slot and exact
checkpoint digest. A new in-game save carries forward the prior state.
Returning to a known older checkpoint uses its existing record. A new unsaved
regular adventure starts with a unique session key. The demo uses its own
slot. The desktop frontend has no emulator save-state import or rewind UI.

## C. Pond Survey

When the player returns with a previously seen Pikachu, the model can offer
the survey or comment instead. The host validates that choice against the
current encounter. If offered, the player completes it by showing Watts
a different visible follower. Showing Pikachu again leaves it open.
Completion adds two trust points and unlocks Watts's repair-tip dialogue
on future visits. That consequence is a persistent NPC interaction, with
no item reward or changes to story progression. The two-line quest instruction
uses fixed wording so the objective is clear.

The structured `dialogue.jsonl` includes profile, observations, proposed action,
validator result, memory snapshot, model metrics and fallback status. The
ROM bridge still accepts only validated dialogue on the existing mailbox.

```sh
LIVING_WORLD_INFERENCE_RUNTIME=/path/to/runtime python3 tests/living_world_phase2.py
```

The live test exercised a first greeting, a SQLite reopen, the model choosing
to offer a survey, refusal to complete with the same follower, completion with
Squirtle, repair-tip dialogue, restored checkpoint state and slot isolation.
It confirmed all requests used the same worker PID. The mGBA tests rendered
the two contextual greetings in both Classic and Quantum. A separate Linux
probe tested blocked networking, subprocess execution and unrelated file reads
and writes. The updated Windows executable is cross-compiled. The existing
AppContainer launch policy is reused, with native Windows Phase 2 still to verify.

## D. Pallet Town expansion

The optional dialogue path now covers all nine Pallet profiles. The eight new
profiles can remember observed species, with their own save-scoped memory.
Watts remains the sole quest and relationship NPC. The [script audit](README.md)
lists the eligible branches and protected interactions for each character.
Blue's optional return to the lab requires a completed League and Pokédex
introduction. The Windows worker and isolation policy are reused. Native
Windows verification of the expanded playtest is still pending.
