# Phase 6 · Predictive Pallet dialogue and hybrid routing

## Windows playtest

Extract the standalone Windows x64 build to a new folder, or apply the
small update over the extracted Phase 5 build. Keep the ROM, Python files,
catalog, and `rom.json` together. Open **Play Pallet Social Demo.cmd** and
select **Continue** with Z. The package uses the same pinned Qwen3-0.6B
Q4_K_M CPU worker and save slots as Phase 5.

1. Walk up to Watts with Pikachu out. Give the predictor a moment before
   starting his dialogue. The first reply uses a reviewed voice line and
   permitted facts. After the sighting, come back with Pikachu to let the
   model choose whether Watts offers the Pond Survey.
2. Put Squirtle in the lead with PokéGlass and walk until it follows you.
   Return to Watts. His remark now uses the Squirtle context. Try Daisy
   in the rival's house and Oak in the lab for character-specific wording.
   Their stock story scripts determine when an aside is available.
3. Give Watts a few seconds to share the sighting, and speak to the sign
   guide near Trainer Tips. Her report identifies Watts as the source.
   Choose **Yes** at **Ask for more details?** A valid first request lets
   the model choose whether to ask Watts. The town sign can show their
   exchange. After restarting, the guide can recall that Watts was unsure
   of the timing.
4. Observe `%LOCALAPPDATA%\LivingQuantumWorld\dialogue.jsonl`. The first
   line for an approach may record `prefetched`. Replies log `hit`,
   `pending`, or `miss`, a route, and timings. Try
   `Play.cmd --pallet-social --no-predict` to see an uncached approach.
   Repeated contexts can still benefit from the cache.

The demo retains Phase 5's menu-based follow-up and separate save. Previously
completed surveys or report requests affect which options are available.
`Play.cmd --model-test` tests both retrieved and model routes using the
bundled weights. `Play.cmd --sandbox-test` runs the native restrictions probe.

## Architecture

- **Reused:** read-only SQLite catalog, per-save memory and knowledge
  provenance, social scheduling, WorldMemory action validation,
  Qwen3/Qwen2.5 worker, GBA pagination, stock fallback, and PokéGlass timing
  fix. The shipped model, Windows sandbox, and runtime dependencies are
  the Phase 5 versions.
- **Compact state:** The host projects world location, story tier, role,
  primary and secondary goals, current concern, topic, remembered companion,
  trust, survey state, permitted evidence, report status and current
  intention choices. It reconstructs this small projection from character
  profiles and existing save rows, avoiding a second persistent source of
  truth or saved reasoning transcripts.
- **Field prediction:** The ROM emits a separate 12-byte read-only hint
  for Pallet Town, the rival house and Oak's lab. It tracks the nearest
  eligible on-screen NPC within seven tiles and the actual visible
  follower. It suppresses prediction during scripts and stops refreshing
  in menus. The host samples at 10 Hz and waits about 200 ms for a stable
  candidate. Only a real script request may display dialogue or apply an
  action. Mandatory story conditions remain under the ROM's control.
- **Cache:** The in-process LRU holds up to 32 replies. Keys include save
  checkpoint, catalog file identity and version, NPC, location, story,
  companion, topic, relevant memories, relationship and event state.
  Delivery rechecks current context and the action allowlist, then validates
  the reply and writes only to the existing mailbox. A follower switch
  changes the key. An unrelated rumor does not evict other characters.
- **Routing:** Ordinary asides and attributed reports select reviewed
  examples and permitted fact lines. Routine sightings and off-screen social
  outcomes remain deterministic. A survey choice uses a one-letter model
  grammar. The guide uses the model only while asking Watts is available,
  and later turns retrieve the persisted result. Foreground routine
  replies bypass speculative inference. There is at most one live
  speculative submission. The host cancels queued work and discards an
  obsolete running result. The existing worker pipe cannot interrupt an
  inference already running, so a foreground model request can still wait
  behind one obsolete inference.
- **Content workflow:** The catalog builder adds eight source-linked
  dialogue examples. It verifies their original script anchors and the
  field-prediction object mappings. The reviewed lines supply voice and
  reactions. Factual statements still come from the existing permissions
  query. The ROM separately checks line width. Future drafts can be generated
  during development and reviewed against the same source before entry.

## Performance and correctness

Reference host exposed nine logical CPUs on AMD EPYC 9V74. The Linux
inference worker uses one thread. These figures are from a controlled
harness and Linux/mGBA, with the ordinary comparison using the Phase 5
model path on the same catalog and companion contexts.

| Operation | Median | p95 or sample range |
| --- | ---: | ---: |
| Phase 5 fresh routine reply, warm worker | 2,240 ms | 1,992–3,956 ms |
| Phase 6 uncached routine reply | 0.54 ms | 0.75 ms p95 |
| Phase 6 cached routine reply | 0.041 ms | 0.136 ms p95 |
| Phase 6 state and version retrieval on hit | 0.024 ms | 0.093 ms p95 |
| Phase 6 cache lookup on hit | 0.007 ms | 0.012 ms p95 |
| Phase 6 facts and examples on miss | 0.45 ms | 0.68 ms p95 |
| Phase 6 fresh survey model decision | 1.06 s | 1.03–1.08 s |
| Phase 6 prepared survey host lookup | 0.16 ms | 0.11–0.20 ms |
| Phase 6 fresh guide model follow-up | 1.95 s | 1.87–2.08 s |

Routine hit and miss results use 200 samples each. The fresh survey had
two samples, the prepared survey two, and the guide four. The model made
the expected choice in all eight scripted survey and guide cases. These
tests cover specific validated choices and do not measure general reasoning
accuracy. Purposefully alternating prediction on and off yielded two
prepared hits and two misses. Actual mGBA approach tests produced four
of four intended hits across Pikachu and Squirtle in Classic and Quantum.
They measured 0.18–0.23 ms of host response, then two emulated frames
(about 34 ms at nominal speed) until the ROM dialogue buffer was ready.
Full text rendering still follows the player's text speed. This sample
does not establish an overall playthrough cache-hit rate.

The tests also verify that a new report or clarification invalidates the
guide's affected reply, while Oak and Daisy stay cached, and that save,
story and catalog changes revoke stale entries. The live model relay and
its persistent consequence passed. Protected event and malformed-action
tests applied zero unsupported changes. The existing deferred-response
checks show frames advance during inference. The in-game conversation
still holds field controls until reply or fallback. Party navigation,
palette restoration, and social/save regressions passed.

For repeatable benchmarks run
`LIVING_WORLD_PHASE5_RUNTIME=/path/to/qwen3-worker python3 tests/living_world_hybrid.py`.
The emulator tests use the catalog produced by `build-knowledge.py` as
described in the Phase 5 report. App logs include retrieval, state, cache,
prompt, proposal validation, mailbox validation, and handoff timings.

## Security and remaining limits

The worker receives only a compact dialogue or allowed choice prompt. It
has no access to the emulator memory addresses or cache database. The host
reads the fixed hint and request and writes the same bounded response
slot as Phase 5. The Linux restrictions probe denied networking, unrelated
file access and process execution. The build packages all required assets
locally. Qwen2.5 remains a separately packable CPU compatibility option.
The Windows x64 archive and its checksums were verified on Linux. Native
Windows offline play, AppContainer behavior, GPU performance and a longer
playthrough remain unverified.
