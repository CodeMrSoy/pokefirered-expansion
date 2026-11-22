# Autonomous Agency Framework · Pewter planning experiment

Phase 14 asks a resident to choose a project option such as counter training.
This experiment replaces that choice for the two residents in the Pewter Mart.
Its unit of validation is a proposed action on a particular world state.
The existing Gym coaching project and regional inquiry system retain their
earlier selection mechanisms. The original clerk still runs the native shop.

Each resident receives their own profile, skills, social requests, trust,
previous goal and outcome. Qwen writes a short ambition in its own words.
It then proposes up to three actions in order. After each suggestion, a copy
of the world applies the action and the worker sees the feasible next actions.
It can finish early or wait. The engine has no list of complete itineraries.
A goal is text used to condition planning. It cannot authorize effects or
certify that an action meaningfully serves the goal.

| Capability | Observable or persistent effect |
| --- | --- |
| practice | Learn a missing shop skill through personal study |
| ask | Send a request to the other resident without compelling a response |
| teach / decline | Answer an outstanding request. Teaching requires the teacher's knowledge and raises the learner's trust |
| work | Take a duty using a known skill. Sales opens the native shop from that resident. Stock enables a shelf-work conversation |
| wait | Commit to no current change |

The host rechecks the entire plan on the emulator thread. A failed later
step discards all earlier simulated effects. The save revision, checkpoint and
Boulder Badge gate must still match. Player endorsement invalidates pending
work and supplies a changed circumstance to the next decision. Requests from
one resident reach only the other. A maximum of six decisions per resident
bounds this small demonstration. Waiting residents wake on relevant changes.
A worker failure grants no duties. Existing checkpoint transactions persist
the result. The read-only monitor includes each proposal, steps checked, and
commit or rejection in the world rules audit.

## Linux measurements

All three workers used the same three starting situations on an AMD EPYC
9V74 host using the CPU worker. The normal shift started with neither
resident on duty. The second fixture introduced an in-game endorsement
between proposal and commit. The third seeded a request for teaching.
Later opportunities differed with the residents' own choices. Timings cover
all inference calls in one plan and exclude initial model loading.

| Weights, Q4_K_M | Plans committed / proposed | Median generation per plan | Peak worker RSS |
| --- | ---: | ---: | ---: |
| Qwen3 0.6B | 5 / 6 | 6.45 s | 725 MiB |
| Gemma 3 1B IT | 6 / 7 | 9.44 s | 983 MiB |
| Qwen3 1.7B | 7 / 8 | 13.34 s | 1,848 MiB |

Each run rejected one stale proposal. All other plans were mechanically
valid. Mechanical validity is an expected benefit of grounding each primitive
in a simulated state. It does not score intelligence. In an earlier trial
that generated the entire plan in one pass, both Qwen sizes attempted to
teach a peer who had never requested help.

In the ordinary 1.7B run the resident proposed `sales specialist|ask stock`.
The neighbor proposed `stocking the shelves|ask sales;teach stock`. The
original resident then chose `Sales specialist|teach sales`. Both residents
learned through a mutually answered request. The motive for studying stock
was weakly connected to the first goal. In the seeded request case Gemma
proposed `Organize shelves meticulously|decline stock`; the other resident
then proposed `Inventory Management|practice stock`. Gemma also proposed
“Organize pickles” in a different interaction. There are no pickles in the
native inventory. This grounded no new item and illustrates the remaining
gap in generated motives. Qwen 0.6B's ordinary resident practiced stock
and took stock duty. After player endorsement invalidated that proposal,
the same actor revised it to waiting.

The [raw Linux records](benchmarks/agency/) contain every proposal, actor
context, validator disposition, model checksum, inference timing and memory
sample. Each benchmark uses greedy decoding. This small sample suits
mechanism testing. It cannot establish broad goal quality, seed diversity,
or a justification for a separate Director model.

## Playing and reproducing

Use **Living World Demo**, continue the post-Brock Pewter save, and stay in
the overworld. Decisions first become eligible after 45 game-clock seconds.
Speak to both residents in the Mart, especially after leaving and returning.
A sales shift allows a purchase. A shelf shift or a colleague's request
appears in conversation. Use the Living World Monitor to see the actual
proposal. The original clerk is always available. The Phase 15 launcher
uses its own save profile.

Run `python -B tests/living_world_agency.py` for the deterministic tests.
For actual inference run `python -B tests/living_world_agency_benchmark.py
RUNTIME MODEL.gguf qwen3` (or use `gemma`). The Windows workflow checks
the extracted application and benchmarks all three model files. Candidate
weights are fetched and checksum-verified during development only. The
player ZIP includes only Qwen3 0.6B. The mGBA tests exercise both adventure
modes and expose live model results in the build log.

This version supports two co-located agents, a shared shop workspace and two
work skills. It executes each short plan atomically. Durable multi-day plans,
open-ended business formation, negotiation over resources, and new occupations
need additional reusable capabilities and stronger semantic evaluation.
