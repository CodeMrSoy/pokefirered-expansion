# Phase 17 · Native world initialization

The Phase 16 baseline was 6772ebea. The audited Pokémon Quantum V3 source was
0dedb6d7. Phase 17 derives data from the **linked Phase 17 ROM**, which includes
the Phase 16 bridge and practice trainers. The catalog compares ROM bytes
with its ELF load segments and includes both hashes and the build revision.

## Build and run

```sh
make world-catalog
python -B tests/living_world_manifest.py
python -B tests/living_world_simulation.py
```

The package builder always regenerates the catalog against the ROM it ships.
After bringing a V3 content change onto this branch, rebuild and regenerate
together. The generator extracts compiled maps, connections, warps, event
objects, encounter variants and slots, species, evolution prerequisites,
normal trainer parties and exact linked layout metadata. It records static
and trainer bindings only where the bounded script-prefix reader can prove
them. Script gates, special encounters and dynamic routes retain conditional
or deferred metadata. Reviewed essential-service and cap registries remain
separate from the compiled rows. A Vidra region section is only metadata,
since shared department-store access is decided by the ROM.

The package's established launcher supplies the ROM, SDL2, mGBA, embedded
Python, existing offline model and worker, the new catalog and schema, and
the Phase 16 engine. A regular New Game publishes a versioned context after
native save and adventure initialization. The host freezes a snapshot at its
frame boundary and launches the same ROM and core in a separate process.
The player receives no native export requests. It can keep playing if the
host is absent. The native query port uses context generation, incremental
request IDs, bounded pages and a per-page resolved/deferred status. The
initialization report is in the profile's native-worlds/progress.json and
counts acknowledged native queries and commits. The ROM has no wait loop
and there is no loading-screen UI in this phase.

The replica calls the existing wild, fixed, trainer, ability and move
functions. Initial trainer moves reuse the same level-up selection routine
as Pokémon creation. Authored learnsets longer than the randomizer's 20-move
cap are paged in full when the setting is off. Disabled species IDs remain
in the catalog since some compiled native form tables can still return
such an ID. Their unverified effective traits are deferred. Randomized rival
evolutions and pooled parties are deferred. Deterministic trainer templates
describe the normal single-trainer assembly even for trainers with a doubles
format. Two-opponent and facility variants are outside that guarantee.

## Manifest and recovery

world-manifest-v1.schema.json defines the envelope. The runtime additionally
checks hashes, cross-references, unique keys, levels and the rod-specific
weight sums. Field status is inherited from its containing record. A row may
carry both an authored record and an effective resolution with its own status.
The immutable starting manifest is stored in a dedicated SQLite table in the
same transaction as the initial world state and journal record. There are
habitat index entries for encounter tables, native trainer actors for decoded
bindings, and service/Gym metadata. Unobserved abundance, owned Pokémon and
dynamic routes are intentionally empty. Reimport of the same manifest preserves
the journal and simulation state. The original Phase 16 scenarios keep using
their own fixtures and rules.

The app pairs verified Flash images with a consistent companion DB snapshot
using a single SQLite transaction. Continue admits only the exact Flash digest
and compatible ROM catalog, mode, seed, flags and trainer identity. Restore
opens a new copy of that revision and preserves the historical snapshot. The
ordinary native .sav remains available for ROM-only recovery. Missing pairs
and changed ROM/catalog identity produce a safe unpaired Continue. The
prototype archives a full world DB per distinct Flash checkpoint, so retention
and compact incremental storage can be added before wider release. External
savestates are unmanaged. Their native/companion rollback contract is the exact
paired Flash revision. Arbitrary RAM-only rollback needs a future checkpoint
protocol and must stay separated from this pairing.

Future simulation changes can use the stable keys (map, header, variant,
method, slot), (map, object), (trainer, battle context) and a host-owned
individual UUID. Later observations, sightings, ownership, migration and slot
weight changes belong in the replay journal. The manifest remains the starting
distribution. Protect Havora's native double-battle format, AI flags and
authored fallback before accepting writable roster projections. This release
keeps all ecology and trainer projection capability read-only.

## Native verification

CI builds the ROM and runs tests/living_world_native_manifest.py for Classic,
Quantum, randomizer disabled, and protected Havora. The fixture enters the
real menu, checks the finalized seed, runs the isolated exporter, compares the
serialized player state, constructs matching scripted wild and trainer
parties, then saves native Flash and Continues with the same world and tick.
It tests interruption before the checkpoint transaction commits. CI also runs
the existing Phase 16 tests. Packaged Windows smoke uses the pinned local
runtime to initialize a real bundled native save from a frozen replica, verify
the database, and confirm that the player core did not change. The earlier
Qwen and native gameplay regressions are still part of the Windows smoke.

The catalog and initialized-world example are generated CI artifacts. The
example is an excerpt with a resolved Route 1 table, exact context, hashes
and Havora captain. The full starting manifest can be read from
starting_manifest.document in a world database.
