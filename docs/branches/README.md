# Quantum branch guide

`Pokemon-Quantum-V2` is the combined playable game. The other active branches
organize development by responsibility. A Git branch contains the whole game;
it does not contain only the files mentioned in its name.

## Where work belongs

| Branch | New work | Integration target |
| --- | --- | --- |
| `QOL` | PokéGlass, menus, battle/system mechanics, field-tool behavior, performance, shared bug fixes | `Pokemon-Quantum-V2` |
| `Randomizer` | Pokémon, ability and move randomization rules, settings and randomizer-specific fixes | `Pokemon-Quantum-V2` |
| `Havora-Development` | Havora layouts, tilesets, gym, encounters, city dialogue and local events | `Pokemon-Quantum-V2` |
| `Sprites` | Playable characters, trainer/overworld sheets, character palettes, walking/running/riding frames | `Pokemon-Quantum-V2` |
| `Corvala-dev` | Corvala geography, buildings, local tiles and city events | `Pokemon-Quantum-V2`, when ready |
| `Pokemon-Quantum-V2` | Integrating the above, cross-region campaign/story changes and releases | Playable build |

Examples: changing Party rendering belongs on QOL; moving a Havora gym switch
belongs on Havora-Development; revising Ben's walking animation belongs on
Sprites; changing Pokémon, ability or move randomization belongs on Randomizer. A cross-region story involving Koga, Safari Zone and Vidra can use a
focused `feature/story-*` branch based on V2.

## Normal workflow

1. Fetch before starting. Check for existing uncommitted work and current branch
   heads so another session's work is preserved.
2. Branch from the relevant active branch. Short-lived names such as
   `feature/qol-party-layout`, `feature/havora-market-npcs`, and
   `feature/sprites-ben-walk` make the purpose clear.
3. Keep commits focused on the requested change. Include its assets, scripts,
   generator updates and appropriate verification together.
4. Merge the focused work into its matching development branch. When it is
   tested and ready for the combined game, merge that branch into V2. In a pull
   request, choose the intended **base** branch explicitly.
5. Use a regular merge commit for development-branch integration when histories
   diverge; fast-forward when possible. This keeps Git's merged status accurate.
   Avoid repeatedly squash-merging the same long-lived branches.
6. Bring V2 back into a development branch before new work when it needs the
   latest shared baseline. This is a normal sync, not a transfer of ownership
   of unrelated features to that branch.
7. Delete short-lived feature branches only after their commits are retained by
   the target branch and the work is verified. Do not delete a branch with
   unique work just to make the list shorter.

QOL, Havora-Development, Sprites and Randomizer were aligned to a common V2 baseline during
the 2026-10-28 cleanup. Their old commits remain in history. Old mixed-scope
commits are not rebased, erased or retroactively split.

## Historical and unfinished branches

- `Pokemon-Quantum-V1` is a frozen V1 reference.
- `master` is a historical base, not the current game. Prefer V2 as GitHub's
  default branch when repository settings permit it.
- `Randomizer` remains an active development branch even though its existing
  commits are already included in V2. Keep future randomization work there.
- `Corvala-dev` has seven unique commits at the audit snapshot. It remains
  separate and is not automatically approved or merged by this cleanup.

Do not force-push these shared branches or reset a development branch that has
new commits. Fetch, inspect and merge any divergent work instead.

## Audit and recovery

[audit-2026-10-28.json](audit-2026-10-28.json) records all eight original branch
heads, trees, ancestry counts and Corvala's unique commits. At that snapshot,
all branches except Corvala-dev were ancestors of V2. No open pull requests
needed retargeting.

The GitHub default-branch setting is a separate administrative action. No
remote branch is deleted by this cleanup. Updating Git references does not
change the default branch. Keep settings changes factual in cleanup reports; a desired setting is
not proof that it was applied.

## Builds and verification

Build the combined game from V2. Map/sprite edits need visual or emulator checks;
mechanics changes need the relevant targeted regressions. A documentation-only
cleanup does not establish a new gameplay or emulator QA result.

The legacy `.github/workflows/build.yml` targets old upstream branches and has
historical battle-suite limitations. This cleanup does not treat that workflow
as a complete Quantum release check or require it for merging.
