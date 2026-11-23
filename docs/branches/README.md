# Pokémon Quantum development

Use `Pokemon-Quantum-V3` for the integrated game. Use `Living-World` for the
native observation bridge, simulation, launcher, and Windows companion. Every
branch is a complete game checkout.

| Work | Start from |
| --- | --- |
| PokéGlass, randomizer, balance, sprites, campaign, and shared game fixes | `Pokemon-Quantum-V3` |
| Simulation, native bridge and companion packaging | `Living-World` |
| Unfinished Havora or Corvala work | Reconcile the retained `Havora-Development` or `Corvala-dev` branch against V3 |
| V2 reproduction and save migration | `Pokemon-Quantum-V2` or its milestone tag |

1. Fetch the current heads before starting and check for pending local work.
2. Use a focused temporary feature branch when an edit needs independent review
   or testing. Set the pull request base to the owning workstream.
3. Sync V3 into Living World as shared game changes are needed. Review conflicts
   and run native bridge tests. Integration from Living World into V3 requires
   a reviewed game change.
4. Use normal fast-forwards or merge commits on shared branches. Preserve exact
   milestone commits with annotated tags such as `quantum/v2` or
   `living-world/phase-17`. Continue future phases on Living World.
5. Before deleting a completed branch, verify its tip can be recovered from a
   fetched tag or is an ancestor of the retained workstream. Check PR and CI
   references and confirm the remote tip still matches the audited tip.

## Builds, saves and evidence

Follow [INSTALL.md](../../INSTALL.md#pokémon-quantum-quick-start) for the native
toolchain. Use the native build and tests for both workstreams. Run the targeted
PokéGlass, randomizer, story or map tests when those systems change. Living
World adds Linux/Windows simulation parity, native manifest and live observation
checks, and a Windows package smoke test on the exact candidate ZIP. For manual
package validation, select the Living World branch in GitHub Actions.

Keep build products under `build/` or in a dedicated output directory. Treat
the top-level ROM and ELF as local Makefile outputs. Store local emulator saves
and companion databases outside tracked source or under `local-profiles/`.
Use disposable profiles for regression tests and keep checked-in synthetic
fixtures with their tests. Retain benchmark summaries with the tested revision,
environment and commands. Save larger benchmark evidence and Windows candidates
as CI artifacts or with their milestone.

Keep tracked source art, map binaries, generator inputs, multiboot payloads,
and native test runners with their build consumers. Review references before
moving anything under `data/`, `graphics/` or `tools/`.

[audit-2026-10-28.json](audit-2026-10-28.json) records the earlier V2 branch
consolidation. The original history and its branch ownership remain part of
that audit snapshot.
