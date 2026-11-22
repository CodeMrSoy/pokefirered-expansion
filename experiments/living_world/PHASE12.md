# Phase 12 early Kanto preview

Baseline and branch point: `c9d2835fd41af0d7e34ab083455a93806a711221` on
`Living-World-Infrastructure`. [Run 44915388462](https://github.com/CodeMrSoy/pokefirered-expansion/actions/runs/44915388462)
passed both parity lanes, the archive build, and the native Windows test of that
same Phase 11.1 archive. Keep that artifact available separately.

## Priority 0 investigation

| Earlier run and commit | Failed job | Exact failure and remedy present in the baseline |
| --- | --- | --- |
| 44912426530, `ccd082a` | windows-package | `Native validation requires the release ZIP URL and SHA-256.` Build and pass a candidate artifact on pushes. |
| 44913818136, `ff6248b` | build-candidate | `Windows requires epoxy module!` Configure mGBA for the libretro target only. |
| 44913976029, `5ea4354` | build-candidate | `curl: (22) The requested URL returned error: 404` when fetching the Qwen license. Fetch from the official model repository. |
| 44914306453, `a123f5b` | build-candidate | `KeyError: 'ARM_NM'` while generating the demo batteries. Export the ARM toolchain name. |
| 44914697937, `22973c5` | windows-package | `AssertionError: Watts did not send a real ROM mailbox request`. The fixture tapped before Continue released field controls. Retry within a fixed frame budget. |

## Census and identity

The generated SQLite catalog contains early-Kanto map objects, script reachable
references, trainer definitions, story-machine flags, placements, and profiles.
Map and object records are regenerated from the source revision that ships with
the ROM. Stable aliases for recurring characters and special markers are
reviewed in `kanto/identities.json`. A clone of an existing NPC references the
original profile. Journal markers, props, Pokemon, and remote player avatars
remain classified separately. Authored trainer names are retained. New names
are display metadata; original event text and trainer names stay in the ROM.

Query `kanto_identity`, `kanto_appearance`, `kanto_map`, `kanto_trigger`, and
`kanto_connection` in the read-only `world-knowledge.sqlite3` shipped beside the
ROM. Static geography facts show topology. Individual battle, badge, service,
and travel gates remain governed by the ROM. Host travel is separate and
continues to use its independently verified, narrow Pewter-area graph.

## Playtest

Extract into a new directory. Start the launcher with **Open Pokemon Quantum.cmd**
and select **Play Pokemon Quantum**. After obtaining the Pokédex, talk to the
supply-conscious boy in Viridian Forest, the tired youngster on Route 3, the
visitor in Mt. Moon, the youngster on Route 4, the reader in Cerulean, or the
resident on Route 25. The authored line comes first. Return with the same
visible Pokémon or several in-game days later to see a remembered reaction or
attributed report where applicable. Open the read-only Monitor for the local
district's identities, studied activity, and existing projected and host-only
residents. The Pewter demo still uses its separate save and existing quest path.

Phase 12 keeps a separate Windows profile at
`%LOCALAPPDATA%\LivingQuantumWorldPhase12`. To test a copy of an existing
Phase 11 game, close both versions, back up the Phase 11 profile, and copy
the battery save alongside its matching `living-world.sqlite3` into the new
profile. Keep the original files in Phase 11. Existing checkpoint keys in
the copied database are retained.

## Scope

The census assigns stable identity metadata across the district. The runtime
adds six optional dialogue hooks and twelve linked regional residents. The
shared scheduler handles the new residents deterministically. Existing Qwen
requests and the Pewter dynamic quest path retain their earlier bounds. There
are no new offscreen travel destinations, mobile sprites, major-character plans,
or regional Quest Book categories in this preview. The tier designation records
the profile's role in the design and does not by itself enable model planning.

The static census captures object templates and map trigger script references.
It does not expand engine-created link visitors, temporary visual effects,
out-of-region versions of recurring characters, encounter table Pokemon,
or every possible ROM script branch into separate residents.

## Reproduce

- `python -B tests/living_world_kanto_census.py`
- `python -B tests/living_world_kanto.py`
- Compile the ROM. Run `tests/living_world_kanto_emulator.py` and the existing
  Living World regressions with `ADVENTURE_TEST_MODE=0` and again with `1`.
  Set `ARM_NM` to the cross-toolchain's nm and `MGBA_CORE` to the libretro core.
- GitHub Actions builds and validates the exact Windows candidate ZIP on each
  Phase 12 push. Desktop controller, real audio playback, and long Windows
  play sessions still require hands-on verification.
