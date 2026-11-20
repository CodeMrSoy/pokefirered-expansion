# Phase 5 · Pallet conversations and local reasoning

## Windows playtest

Extract the **Phase 5 Windows x64** ZIP into a new folder. Run **Play Pallet
Social Demo.cmd** and choose **Continue** with Z. The standalone archive
includes one model, the emulator, the game, and the Windows sandbox. It does
not need network access or a separate language model program. The model is
about 378 MiB. Windows 10/11 x64 and a CPU compatible with the existing worker
are the target. Allow at least 1 GiB of disk space for the ZIP and extracted
program and about 2 GiB of free RAM for testing. Those are planning estimates,
not native Windows measurements. A GPU is optional.

1. Walk so Pikachu becomes visible. Talk to Watts by the pond. He recognizes
   the follower and remembers it on a return visit. Oak in the lab has his own
   research-focused dialogue when he sees Pikachu.
2. Wait about four seconds. Optionally read the **Pallet Town sign** for the
   existing Watts/guide exchange. Put Squirtle in the lead slot before
   talking to the sign guide by the southwest Trainer Tips sign.
3. Advance her stock line and her attributed sighting, then pick **Yes** at
   **Ask for more details?** The second turn refers to precisely the report
   she just named. Advance again if the reaction occupies its own page.
4. If she decides to ask Watts, her request is saved. After about four
   seconds, check the town sign after any unread exchange. The guide and
   Watts discuss the timing. Restart, ask the guide again, and check that
   she remembers Watts could not tell her when. An NPC without the report
   lacks the information.
5. From Command Prompt in the folder, run `Play.cmd --model-test` and
   `Play.cmd --sandbox-test` with Windows networking disabled. The first
   exercises the bundled weight and a synthetic two-turn prompt. The
   sandbox check should report four denials. Real gameplay entries and
   intention outcomes are logged in
   `%LOCALAPPDATA%\LivingQuantumWorld\dialogue.jsonl`.

The social demo has its own battery save and structured world memory.
Existing Phase 4 demo progress can affect whether there is an unread town
sign exchange. The ROM and `rom.json` must come from the same build. Use
`Play.cmd --pallet-social --lightweight` to skip optional generated prose
and guide intentions on a slower CPU. Developers can package the known
Qwen2.5 weights with `package-windows.py --legacy-weights`. A failed model
call cannot approve a new intention and leaves the deterministic dialogue
or the original stock script available.

## Controlled conversation and effects

The GBA menu offers one fixed follow-up per talk. There is no arbitrary
text-entry interface. The desktop host binds the second turn to the next
mailbox sequence and to the actual report described in the first reply.
The summary expires after 90 seconds, or when another NPC request intervenes.
It carries a report ID and source, with no saved transcript.

The model composes reactions by selecting short clauses under a grammar.
It proposes either asking Watts or waiting when the guide has an attributed,
unverified report. The game supplies facts, source attribution and action
outcome text. It checks source ownership, save, recipient, witnessed status
and freshness before recording the request. The guide can't use a report
as evidence that she personally saw Pikachu. Unsupported requests, duplicate
requests and stale turns do not change the save. A scheduled, deterministic
answer records that Watts cannot give a reliable in-world observation time.
It affects future dialogue and persists with the Phase 4 checkpoint system.
The first Watts-to-guide relay, ordinary game scripts and Pond Survey remain
active. Background simulation itself uses no extra model.

The ROM supports two pages with up to two lines per page and checks each
line's actual pixel width. Model prose stays in a nonfactual vocabulary,
with separate checks for words, length, formatting and action allowlists.
During a model wait, emulator frames continue and conversation holds normal
field controls. Scope is limited to Pallet Town and this one question. Open
conversation, generated quests and broadly autonomous NPC planning remain
experimental.

## Comparative benchmark

The same ten Pallet situations cover first sight, remembered visit,
attribution, a follow-up with missing time, Oak's fact recall and ignorance,
private information, relevant sharing, rumor verification, and choosing to
wait. Greedy decoding and the same output grammar were used, with each
family's chat template. All four GGUFs loaded with the isolated
**llama.cpp b6500** CPU worker. The Qwen3 runs disabled reasoning output
for the interactive budget.

| Exact model and quantization | Correct structured choices | Lexical fact checks | Median warm inference | Worker RSS |
| --- | ---: | ---: | ---: | ---: |
| Qwen2.5-0.5B-Instruct Q4_0 | 3/10 | 4/10 | 1.62 s | 705 MiB |
| Qwen3-0.6B Q4_K_M | 8/10 | 8/10 | 2.06 s | 734 MiB |
| Qwen3-1.7B Q4_K_M | 8/10 | 9/10 | 4.42 s | 1,855 MiB |
| Gemma-3-1B-IT Q4_K_M | 2/10 | 4/10 | 3.70 s | 988 MiB |

These measurements came from concurrent Linux test jobs. An isolated
Qwen3-0.6B rerun took 1.27–1.86 s (1.46 s median) and used about one Linux
CPU core while generating. Lexical tests only check selected evidence or
contradictions. They can accept unnatural lines such as “Admit unknown
time.” Qwen3-0.6B got the source and unknown-time decisions right but chose
the wrong action code for the private-note and unverified-rumor cases.
Gemma called out “Sunrise” despite the missing time. Qwen3-1.7B got the
rumor decision right but chose the incorrect attribution code and took
roughly twice as long. These are small scenario tests with one greedy
response per case, rather than a general intelligence or personality score.

The balanced package picks Qwen3-0.6B for its two-turn attribution,
decision accuracy, size and latency. Model-authored reactions appear only
where the host can validate them. The Windows test build keeps a single
resident model and the existing CPU worker. The existing serverless pipe
and process boundaries remain in place. GPU device access was unavailable
in the build environment. Upstream llama.cpp provides Windows Vulkan and
CUDA builds, but native driver behavior and AppContainer access would
need verification before either backend can ship. Phi-4-mini-instruct
(MIT) and SmolLM3-3B (Apache-2.0) were screened by model card for their
larger weight class. Neither was benchmarked or bundled.

### Model sources and exact hashes

| Artifact | Source and license | SHA-256 |
| --- | --- | --- |
| Qwen2.5-0.5B-Instruct Q4_0 | [Qwen official GGUF](https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct-GGUF), Apache-2.0 | `7671c0c304e6ce5a7fc577bcb12aba01e2c155cc2efd29b2213c95b18edaf6ed` |
| Qwen3-0.6B Q4_K_M | [Unsloth conversion, 626eb58](https://huggingface.co/unsloth/Qwen3-0.6B-GGUF/blob/626eb58354de1127ccd7a9dc213485a3b716534c/Qwen3-0.6B-Q4_K_M.gguf), Apache-2.0 | `e773ccf7adfa50fcabfa5ea0e30312e11f0e83bf4ae00e6a38503e49358d1952` |
| Qwen3-1.7B Q4_K_M | [Unsloth conversion](https://huggingface.co/unsloth/Qwen3-1.7B-GGUF), Apache-2.0 | `b139949c5bd74937ad8ed8c8cf3d9ffb1e99c866c823204dc42c0d91fa181897` |
| Gemma-3-1B-IT Q4_K_M | [GGML conversion](https://huggingface.co/ggml-org/gemma-3-1b-it-GGUF), [Gemma terms](https://ai.google.dev/gemma/terms) | `8ccc5cd1f1b3602548715ae25a66ed73fd5dc68a210412eea643eb20eb75a135` |

To rerun each model, call
`python3 tests/living_world_reasoning_benchmark.py /path/to/worker-directory qwen3 /path/to/model.gguf`.
Use the template option `chatml` for Qwen2.5 and `gemma` for Gemma.
The JSONL output has per-case sentences, scores, failures and timings.
For the mGBA regression, use the Phase 4 catalog variables and set
`LIVING_WORLD_PHASE5_RUNTIME` to the worker directory containing the
balanced model as `model.gguf`.

## Verification boundaries

Linux/mGBA runs in both modes verified two-page mailbox text and the actual
Qwen3 guide proposal, save reopen, the model conserving once a request
exists, deterministic resolution, and the worker-error/timeout fallbacks.
The normal dialogue, social, knowledge and V3 PokéGlass regression suites
also ran. The existing Linux restriction probe exercises network,
filesystem and process-access denial. The Windows archive was assembled
and checked on Linux; native Windows performance, network-disabled
gameplay and AppContainer behavior remain unverified.
