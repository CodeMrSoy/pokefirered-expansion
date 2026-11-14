# Quantum trainer AI — first implementation

Target: QOL. Trainer skill is independent of team levels, EVs, IVs, items and
the existing selectable party difficulty. Those team definitions are unchanged.

## Profiles

Use one profile in `src/data/trainers.party`; regenerate `trainers.h` with make.

| Party syntax | Behavior added to earlier tiers |
| --- | --- |
| `AI: Quantum Regular` | Bad-move checks, KO and viability scoring; reliable KO bonus; don't waste a clear winning turn on status in singles. |
| `AI: Quantum Gym Trainer` | HP awareness, smart replacement selection in singles; penalize setup into a revealed lethal attack. |
| `AI: Quantum Gym Leader` | Smart switching, smart Tera where available, setup/recovery tempo, suicidal recoil penalty. |
| `AI: Quantum Rival` | Additional setup penalty against revealed Haze/Clear Smog. |
| `AI: Quantum Elite Four` | Conservative damage rolls, reliable two-hit attacking races, reject near-fatal voluntary entries. |
| `AI: Quantum Champion` | Stronger attacking-race bonus and a larger HP reserve on voluntary entries. |

All six use the same legal-information boundary. No profile enables omniscience,
the upstream hidden-party switch predictor, or PP-stall prevention (which reads
unrevealed party slots). Selecting a Quantum profile in the debug battle menu
loads its full preset. The menu now labels every current flag correctly and
supports 64-bit flags, including Elite Four/Champion markers above bit 31.

`tools/ai/assign_quantum_profiles.py` assigns profiles from trainer IDs/classes
and gym script membership. Eirik (`TRAINER_HAVORA_CAPTAIN`) is explicitly a
leader despite using the Sailor class. It covers rival starter variants and
Elite Four/Champion rematches. Run it again when adding gyms. New custom leaders
should use a leader class/ID or an explicit exception in `tier_for`.

## Shared decision changes

- Disabled, empty-PP and Choice-locked move slots retain zero scores instead of
  being reset to 100 by the following initialization branch.
- Reliable KOs use minimum damage and at least 100% calculated accuracy;
  priority/speed and known retaliation are considered. Self-destruct moves do
  not receive the ordinary reliable-KO bonus.
- Setup and immediate recovery use damage from revealed opposing moves.
  Doubles use a conservative estimate of both foes attacking the user, while
  existing partner-aware scoring still handles support and friendly fire.
- Voluntary switches are vetoed if the selected replacement dies to hazards
  or a revealed incoming attack. A safe singles KO usually takes precedence.
  Consecutive voluntary switches are discouraged, with a Perish Song exception.
  Forced replacements are not vetoed by this policy.
- Hazard checks now correctly respect Boots/Magic Guard and include Steelsurge.
  The survival estimate handles lethal hazard damage without unsigned wrap and
  is capped at eight simulated hits to avoid long hypothetical healing loops.
- Incoming conservative/risky damage reads the defending AI's flags.

## Information and state

The expansion already records revealed moves, abilities and item effects in
`gAiPartyData`; reuse that memory across switches. During a Quantum decision,
human battlers are temporarily presented through a known-information snapshot.
This also covers older evaluator code that reads `gBattleMons` directly. Live
battlers are restored afterwards. Unknown held-item IDs/parameters are masked;
revealed item effects update item memory, and consumed items clear it. Having
an AI partner no longer exposes the human's complete moveset to Quantum AI.

This is a targeted boundary improvement, not a proof that all upstream helpers
are free of inference leaks. The engine still uses exact current combat stats
and PP/limitation state in parts of its estimates. Unknown abilities can be
guessed from species possibilities. There is no reading of the player's chosen
action in the new tactical evaluator. Do not enable upstream prediction flags
on these profiles without another information-boundary audit.

## Verification

Run `bash tools/ai/check_quantum_ai.sh -j8` with the ordinary build dependencies.
This checks source assignments and runs the new scenarios in mGBA. The focused
suite includes accurate KOs across six tiers, priority, immunities, setup,
recovery, move locks, hidden moves/items, live-state restoration and hazard
entries with/without Boots.

The legacy full test target includes outdated `trainer_control.c` calls to the
party creation API. `TEST_SOURCES` allows a focused suite without editing that
unrelated test. The test linker now accepts function/data sections used by the
modern compiler. The battle harness passes full-width AI flags directly in
test builds; the 32-bit recorded-battle save format is unchanged.

`AI_LOG` in a battle test records the scoring adjustments. Final per-target
move scores remain available in `gAiBattleData->finalScore`.

Validation on 2026-11-14: normal FireRed ROM build passed; all 11 Quantum
scenario groups passed in mGBA (including the six-tier parameterizations);
21 existing tests from `ai_trytofaint.c`, `ai_calc_best_move_score.c`,
`check_bad_move.c` and `ai_choice.c` passed in the same focused run. All three
host assignment checks passed. The full legacy suite was not run successfully
because of the unrelated trainer-control API mismatch noted above. No win-rate
or device timing benchmark was performed.

## Next stage

This implements the agreed first version. It is still a heuristic evaluator,
not a recursive search. Full role inference, preserving specific counters to
revealed bench threats, pattern-based switch prediction and multi-turn state
simulation remain future work. Weather/screens/hazards/pivot combinations use
the expansion's existing effect and partner logic. Tier ordering describes
decision capabilities; no tournament win-rate benchmark has been established.
