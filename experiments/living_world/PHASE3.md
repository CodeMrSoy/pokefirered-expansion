# Phase 3 · Shared world knowledge

The Windows packager builds and bundles a read-only SQLite catalog from
Pokémon Quantum's source. The initial catalog covers 18 Pokémon, 14 Kanto and
Vidra maps, base species types and abilities, selected evolutions, Viridian
Forest base encounters, a type matchup, Pallet relationships and local
history, some story events, and existing quest prerequisites. Source paths
and anchors are stored with each entry. Rumors, beliefs, discoveries, and
canonical facts have separate kinds. Species definitions and base wild
encounters describe the standard game. They cannot reveal a randomized
ability, a live encounter roll, or hidden attributes of the follower.

All nine Pallet asides use the same catalog. The host knows which location
called an aside from its stable NPC ID. It uses the visible follower for a
species topic and the hook location for local context. SQLite checks familiar
regions, access type, expertise, known characters, evidence, trust, and story
prerequisites before it ranks matched facts. The default response context
contains at most two fact entries and 220 UTF-8 bytes of fact text. The model
worker receives only the selected excerpt. Dialogue still uses approved GBA
lines and validated choices. An unreadable or incompatible catalog triggers
the ROM's stock dialogue.

The save database maintains acquisition records separately from interaction
memory. Records preserve origin, source, timestamp and verification, and are
keyed to the same save slot, battery checkpoint and NPC. A validated aside
with a visible follower records a sighting. Completing the existing Pond
Survey records distinct evidence and keeps its persistent repair tips.
Restoring an existing checkpoint keeps the knowledge and memories that
belong to that checkpoint. This release supports rules for rumors and
reported knowledge; no player report, battle witness, or NPC news wire is
exposed by this mailbox. Unknown story prerequisites fail closed.

## Windows playtest

- For the small update ZIP, exit the application and extract its contents into
  the folder that already contains the **Pallet Expansion** update and
  `Play.cmd`. Allow those files to be replaced. The matching ROM starts with
  SHA-256 `b7d295bbda85de565`. The complete Phase 3 Windows build can also be
  produced by the packager in [README.md](README.md).
- Launch **Play Pallet Demo.cmd**. Walk until Pikachu is visible and talk to
  Watts near the southern pond. After restarting the app, bring Pikachu back.
  Watts may offer the Pond Survey. Return with Squirtle to complete an
  offered survey, then talk to Watts again for repair tips.
- For Oak, ask for an ordinary Pokédex rating in his lab and advance past the
  stock rating. For Daisy, visit the rival's house during her casual
  pre-League dialogue. Blue's in-game aside is available in Oak's lab after
  the League. Open Command Prompt in the application folder and run
  `Play.cmd --model-test` to compare all four with Pikachu immediately,
  including Blue, without changing a save.
- Run `Play.cmd --sandbox-test` to exercise the AppContainer. Retest
  `Play.cmd --model-test` with Windows networking disabled. Inspect
  `%LOCALAPPDATA%\LivingQuantumWorld\dialogue.jsonl` for retrieved fact IDs,
  sighting provenance, proposed/approved actions, timings, and fallbacks.

## Reproduce the checks

From the repository root, run `python3 tests/living_world_knowledge.py`.
Set `LIVING_WORLD_INFERENCE_RUNTIME` to the directory holding the Linux
worker and model to include real inference and process reuse. For the mGBA
test, set `LIVING_WORLD_CATALOG` to a catalog from
`python3 experiments/living_world/build-knowledge.py /absolute/path/world-knowledge.sqlite3`.
Follow [README.md](README.md) for the emulator and ARM toolchain variables and
run `tests/living_world_bridge_emulator.py` in both adventure modes.

In the Linux test, the 44 KiB catalog across nine NPCs returned p50 0.320 ms
and p95 0.424 ms over 1,200 requests. With 25,000 additional synthetic facts
and 309 NPC profiles, the 4.33 MiB catalog measured p50 0.368 ms and p95
0.456 ms. Peak traced Python allocation
for the retrieval sample was about 3 KiB, excluding SQLite's native
allocations. The first local model response took 3.37 s including 0.44 s to
load weights. Five subsequent responses took 1.74–2.84 s on the same worker.
Prompt assembly took 0.025–0.046 ms per response. With a prefetched reply the
ROM placed the dialogue in the text buffer in two emulated frames. An
unprefetched conversation also waits for the model and any queued request.

The mGBA runs rendered four different responses to Pikachu and passed
protected-script and missing-catalog fallback checks in Classic and Quantum.
The Linux isolation probe denied network sockets, execution, and reads and
writes to an unrelated test file. Native Windows with networking disabled
remains to be tested. The catalog is deliberately scoped to representative
Pallet knowledge. Speculative lore, unrestricted text generation, and new
quest generation are outside this implementation.
