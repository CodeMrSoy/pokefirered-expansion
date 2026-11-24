# Phase 19 · Wild Pokémon ecology

Phase 19 starts from Living World `f4304d0f`. The ROM and the native
observation ABI are unchanged. The Phase 18 journal, clock and paired Flash
checkpoints remain authoritative for native evidence and companion progress.
Phase 18's released Windows package smoke passed. The original recorder-free
RNG timing diagnostic remains outside the verified same-ROM host comparison.

## Habitats and populations

The registry is derived from the immutable World Manifest. Map IDs, map
types, access notes, adjacency, encounter methods, resolved weights and
variant indexes retain their native provenance. Land and rock encounters
inform a land pool. Surf and fishing inform a water pool. Hidden encounters
and interiors do not seed populations. The native lists remain conditional
where only gameplay can establish availability. The counts, resource levels,
seasons and habitat capacities are companion settings.

A linked-ROM catalog extraction protects legendary, mythical, Ultra Beast,
Paradox and temporary battle forms. Known compiled static encounters also
protect their maps and both authored and resolved species. The extractor
checks the expected ABI against representative compiled species and refuses
unsupported layouts. Ecology on a catalog without a verified protection list
is disabled. No story individual is created in the native game.

One ecological update runs every 24 existing simulation hours. Growth and
decline use integer arithmetic, a stable seed, seasonal resource variation,
and the effective native time windows. A depleted native cohort can recover
through the same resource rules. Ordinary Pokémon are aggregate counts.
A bounded number of rare residents are promoted from an existing group and
keep a simulated ID, species/form, location and sighting history. The
simulated ID is unrelated to an individual instantiated by a native battle.
The world advances only during a live session.

## Migration and native evidence

The first release reviews Route 9–10, Route 13–14, Route 14–15, Route 19–20
and Route 24–25. Each edge needs reciprocal cardinal links and matching
compiled offsets. Terrain, the same habitat layer, valid runtime encounter
tables, regional restrictions and protected maps apply at both ends.
Unreviewed, indoor, warp-only and cross-region links are denied. A reviewed
corridor can carry a native cohort or a vetted companion-only arrival with a
shared non-Normal habitat affinity. Water introductions require Water typing.
A new group can establish after arrival. It never changes a native table.
Population pressure initiates travel, resources bound arrivals, and reserved
capacity covers the one-to-three-day transit.

Native wild encounters and outcomes are evidence. An ordinary successful
capture adjusts an eligible, unambiguous native cohort once. Scripted, special
and protected encounters do not subtract from the population. A wild win
does not establish death. Native individual details remain in the Phase 18
observation tables, with separately labelled Monitor entries.

## Save, replay and knowledge

Ecology writes share the native event and daily tick transactions. Stream
acknowledgments, ecological input IDs and daily keys make retries idempotent.
The immutable starting manifest and ecology inputs rebuild the projection,
including migration and NPC reports. Recent events are bounded in the
snapshot, and the input journal can reconstruct past events. Companion
ecology, native observations and the clock ride together in the paired
checkpoint. A previous catalog can restore only if its exact prior digest
can be reconstructed and the ROM digest matches. Phase 18's rollback
quarantine remains in effect.

Eligible existing NPC profiles collect sightings on local simulated patrols.
A trusted contact may receive an attributed, lower-confidence report. Each
report retains source, location, day, confidence and an investigation option.
Reports expire after 21 simulation days. Dialogue receives only the active
speaker's report when the native field hint confirms that speaker and area.
It uses the existing retrieval, line validation and dialogue routing.

The Living World Monitor shows simulated groups, capacity and changes,
migrations, rare individuals, NPC reports, recent ecological events, native
observations and background-worker health. The worker supplies the snapshot,
so the emulator frame loop does not query SQLite for the Monitor.

## Verification

Run the existing native suite with the exact built ROM and catalog. For an
ecology benchmark from real resolved tables, export the manifest with
`WORLD_ECOLOGY_MANIFEST` during that suite.

```bash
python -B tests/living_world_ecology.py
python -B tests/living_world_live_emulator.py
python -B tests/living_world_ecology_benchmark.py ecology.json --manifest world.json
```

Run the native suite with `WORLD_TEST_NO_RANDOMIZER=1` and
`WORLD_ECOLOGY_ORDINARY=1` to exercise a Sweet Scent encounter on a normal
Route 1 grass tile and verify an ordinary capture adjustment. The default
native test exercises the protected scripted path. Linux headless frame
timings measure core and host processing, including operating-system
scheduling spikes. They do not measure displayed frames on a Windows PC.
Windows CI exercises synthetic projection parity and the packaged native
Continue smoke separately.
