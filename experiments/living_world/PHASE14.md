# Phase 14 evolving Pewter preview

Phase 14 starts from `77e4983`. The exact Phase 13 package passed
[all four CI jobs](https://github.com/CodeMrSoy/pokefirered-expansion/actions/runs/44976666971).
Earlier builds failed through a late demo-save fixture that reopened in the
Gym and a seven-second Windows Qwen timeout. Phase 13 fixed the fixture
and measured the shorter prompt on the native runner. The Phase 13 release
and its save profile remain available.

Phase 13 accepts Qwen choices for constrained event topics, originators,
locations, and responses. The scheduler, reachability gates, deadlines,
approval, dialogue templates, consequences, and missing-model policy are
deterministic. Its Win32-compatible CPU worker runs one request at a time.

## Start the preview

Open **Living World Demo** and continue into Pewter after the Boulder Badge.
Stay in the overworld long enough for projects to be considered. Look for
the resident inside the Mart and the attendant in the Gym. The first project
becomes eligible after 45 game-clock seconds. Subsequent projects are spaced
by at least 90 game-clock seconds. Existing inquiries share the same worker.

While the Mart decision is still open, the resident can ask whether you
support counter training. Saying yes invalidates any outstanding proposal
and prioritizes counter training. Without player input, the resident can
take a stock or counter job. A counter apprentice can open the standard
native buy/sell menu through the original stock list. The original clerk
continues to serve customers. The Gym can start either type coaching or
field preparation after winning the badge. Advice appears alongside the
attendant's stock post-victory dialogue. The project also offers one optional
practice battle after Brock. The fixed Rock drill uses a level 10 Geodude,
and the trail drill uses a level 11 Sandshrew.

The Monitor's `world_rules` section shows protected native services and Gym
maps, Classic and Quantum caps, choices, provenance, player endorsement,
approval and rejection history, and quarantined saves. The separate profile is
`%LOCALAPPDATA%\LivingQuantumWorldPhase14`.

## Policy boundaries

- The exported service registry names implemented shop and healing scripts.
  Missing facilities are not inferred from town names. Havora's listed
  shop is its Market, which has native stock, rather than the empty Mart script.
- The cap tests compare the complete 14-entry Quantum table and separate
  Classic table to `src/caps.c`. Havora's implemented challenge uses the
  Captain battle/crest. Corvala, Brandon, Ben and Cody have reserved crests
  and caps in this checkout. Their presence in the table does not create
  playable leader battles.
- A proposal carries a checkpoint, revision, supported project and exact
  option. The validator simulates a copy, validates the complete proposed
  state, and uses a conditional SQLite write inside a transaction. A failed
  write leaves the published state unchanged. A malformed saved state is
  quarantined and native stock scripts remain usable. Accepted project state
  travels through the existing save checkpoints.
- The ROM checks the actual Boulder Badge before exposing Phase 14 hooks.
  The host sends optional dialogue. The two new operations are entering the authored Pewter shop menu from an
  existing NPC and starting a vetted optional post-badge practice battle.
  Native stock, prices, protected flags, party data, tile geometry, puzzles,
  warps, rewards and required battles are outside the allowlist.
- The team ceiling checks both mode and progression ceilings, including
  boolean/oversized input rejection. The practice parties are fixed, keep their authored move lists in randomizer
  mode, and are checked for species, moves, held item, actual progression cap
  and a hard ceiling of 14 immediately before the battle script. Stock
  mandatory battles remain authoritative. Arbitrary team assembly, generated
  puzzles, relocation and broader physical changes are outside this preview.

Run `python -B tests/living_world_rules.py` for the registry checks, adversarial
proposals, SQLite rollback, replay, migration, and save scope. The
`living_world_rules_emulator.py` suite exercises the compiled native choices
and counter in both adventure modes. Native CI validates the exact packaged
copy and executes the actual bundled Qwen worker.
