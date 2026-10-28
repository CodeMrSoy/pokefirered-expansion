# Pokémon Quantum repository instructions

## Branch ownership

- `Pokemon-Quantum-V2`: combined game, merges, cross-region campaign integration
  and release builds.
- `QOL`: mechanics, shared systems, PokéGlass/UI, field-tool behavior, performance
  and general bug fixes.
- `Havora-Development`: Havora city/maps, gym, encounters, local assets and scripts.
- `Sprites`: character/trainer/overworld sprite sheets, frames and palettes.
- `Corvala-dev`: Corvala maps and local assets; preserve its unfinished work.
- `Pokemon-Quantum-V1` and `master`: historical references, not feature targets.
- `Randomizer`: Pokémon, ability and move randomization mechanics; keep active.

Explicit user branch choices take precedence. For an unspecified target, choose
by the change's responsibility. Use a focused branch from that target, such as
`feature/qol-*`, `feature/havora-*`, `feature/sprites-*` or
`feature/randomizer-*`. Cross-region story
work can use `feature/story-*` based on V2. Do not put an unrelated feature
straight on V2 merely because the last task used it.

Every branch is a complete game snapshot. Existing shared history and baseline
assets do not violate branch ownership; keep new work focused. Read
`docs/branches/README.md` for the integration workflow.

## Preserve shared work

Fetch and inspect current heads before editing or publishing. Preserve local
uncommitted work and changes from other chats. Keep branch-specific contents
when merging. Do not force-push, rewrite old mixed-scope history, reset shared
branches or delete unique work to clean up the branch list.

Use normal merge commits for divergent development-branch integrations and
fast-forward when possible. Sync V2 back into a development branch when a new
feature needs the current baseline. Merge into the combined game when the user
requests integration/release or the task's existing authorization includes it.
Use expected-head protection when updating refs through the GitHub connector.

## Verify the actual requested behavior

Use targeted build/emulator/visual checks appropriate to the change. Separate
an executed check from an outdated test, a skipped suite or an untested claim.
Update source generators when changing their generated content. Do not edit
unrelated map art, gym geometry or character sprites to make an old test pass.

Known map/release limitations are documented under `docs/vidra/` and
`docs/havora/`; inspect the relevant notes rather than assuming all old test
scripts match the latest map organization.

Publish through the connected GitHub tools if terminal push authentication is
unavailable. Verify the remote head/tree before claiming work is pushed. Branch
updates do not change GitHub's default-branch setting.
