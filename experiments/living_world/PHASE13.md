# Phase 13 autonomous inquiry pilot

## Baseline audit

Phase 13 starts at Phase 12 commit `9f3d12f`. The exact Windows package passed
[all four jobs](https://github.com/CodeMrSoy/pokefirered-expansion/actions/runs/44968409900).
The census, named relationships, and first-person observations were persisted,
while the twelve Kanto residents' schedules and cooperation outcomes followed
deterministic rules. The older Pewter planner, Brock director, and some special
conversations used Qwen with constrained options. The social scheduler could
run without player input. The baseline had no general event proposal loop.

The bundled Qwen3 0.6B has limited reasoning depth. Phase 12 Windows CI
measured roughly 3.45–11.88 seconds per selected existing task. The resident
worker is serial and a running request cannot be preempted. The catalog's
adjacency is descriptive. The existing mobility code only projects a narrow
Pewter-area graph. Story scripts and badge progression live in the ROM.

## Play the pilot

Open **Living World Demo** from the launcher to start in Pewter with Brock's
badge, or unlock the badge normally in **Play Pokemon Quantum**. The pilot
looks for its first lead shortly after unlock. Allow about half a minute of
overworld time for the initial proposal and the first resident response. An
inquiry may concern Route 3 or Mt. Moon. Talk to the Museum assistant behind
the exhibit desk, the tired youngster on Route 3, or the visitor on the first
floor of Mt. Moon. Only people who know a lead can discuss it.

If a field contact asks you to report what you heard, return to the assistant
and choose **Yes** when asked to file the account. You can also leave the
residents to work on the lead and return later. An inquiry closes after six
minutes of valid game-clock time. Talk again to hear what happened. The menu
**Living World Monitor** displays the proposal and response options, evidence
source, player decision, relationship changes, and model timing in
`autonomous_pilot`. Saving preserves the inquiry and its history. Phase 13 uses
a separate profile at `%LOCALAPPDATA%\LivingQuantumWorldPhase13`. It does not
write to an installed Phase 12 profile.

## How the pilot works

- The ROM reports the actual Boulder Badge flag and game clock through a
  compatible field hint. The pilot only creates inquiries in the two reviewed
  destinations. It cannot write story flags, alter battles or grant rewards.
- The director composes a subject, reachable site, and originator. The seed
  shapes the available environmental leads. The model sees those leads and
  recent outcomes. Every choice is independently validated at commit time
  against the current save, event, actor, and allowed options.
- Local residents and the assistant independently choose how to react based on
  the accounts they have received, their roles, routines, goals, past outcomes,
  and bilateral trust. The first witness and each report source are recorded.
  Comparing a second account or receiving a player report can change the
  resulting evidence. No player appearance is required to settle an outcome.
- The database uses the same battery checkpoints as the existing Living World
  state. The bounded record contains one live event, eight finished events,
  twenty-four audit entries, and four memories per participant. Latest event
  resolution does not replay missed intervals after a long save gap.
- One worker serves foreground and background requests. Director and resident
  requests enter only while that worker is idle. Each model generation has a
  seven-second budget, separate from worker startup. A missed or invalid
  request can use seeded deterministic choices. A save switch discards stale
  work. The game resumes stock dialogue if optional bridge text is unavailable.

## Validation and limits

Run `python -B tests/living_world_autonomy.py` for the 32-seed replay,
knowledge isolation, player influence, relationship changes, and checkpoint
tests. Run `tests/living_world_autonomy_emulator.py` under mGBA in both modes.
The fixture uses compiled scripts, advances original dialogue, confirms the
optional Museum prompt and validates the ROM's resulting mailbox request.
The Windows package workflow also runs model-backed director and resident
benchmarks using its actual offline worker.

This is a dialogue-visible pilot with two sites and three active residents.
The generated scenarios combine a small set of supported leads rather than
creating free-form mechanics. Investigations update host state. They do not
add a moving field sprite or an objective row to the Quest Book. The existing
Pewter travel and Quest Book paths remain in use. Physical controller testing,
real audio, a fully played Windows route circuit, larger planning groups and
more event types remain outside the automated evidence for this preview.
