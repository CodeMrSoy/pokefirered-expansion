# Pokémon Quantum repository instructions

## Branch ownership

- `Pokemon-Quantum-V3` integrates the game, including randomizer, PokéGlass,
  shared mechanics, story, maps, and sprites.
- `Living-World` owns the native observation bridge, simulation, companion
  launcher, and Windows packaging. Integrate Living World changes into V3 on
  request.
- `Havora-Development` and `Corvala-dev` retain unfinished map work.
  `Living-Quantum-World` retains outstanding prototype runtime fixes.
- `Pokemon-Quantum-V2` is the stable V2 save-migration baseline.
  `Pokemon-Quantum-V1` and `master` are historical snapshots.

Use a temporary feature branch from the relevant workstream when isolation
helps. Use annotated tags for completed milestones. Read
[the branch guide](docs/branches/README.md) for review and release procedures.

## Preserve shared work

Fetch and inspect current heads before editing or publishing. Preserve local
uncommitted work and changes from other chats. Keep branch-specific contents
when merging. Do not force-push, rewrite old mixed-scope history, reset shared
branches or delete unique work to clean up the branch list.

Use normal merge commits for divergent development-branch integrations and
fast-forward when possible. Sync V3 into Living World when a change needs the current
integration baseline. Merge into the combined game when the user
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
