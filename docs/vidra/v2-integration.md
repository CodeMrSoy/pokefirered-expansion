# V2 integration: QoL and Havora development

Integrated source heads:

- V2: `62484501c0a11691a12bea43e079d47b4691c569`
- QoL: `457af3e551d3e9bc31eb594b8ffadf850bd44dab`
- Havora-Development: `8364d56bed45e619510929a2e41ebf1b51b3fca7`

The combined version retains the paged PokéGlass Start replacement, fixed
starting outfits, Oak's Ultra Balls, and move-description fixes. Havora's
settlement groups, map names, migration and latest authored gym/map data are
preserved. V2's field tools and the native Kanto/Vidra map presentation remain
available, with all five canonical settlement names and no Sevii picker entry.

Conflicts were resolved by retaining both sets of script specials, updating
integration-only map references, and preserving the newer region-map palette,
atlas and two-region selector. Historical gym asset tests reference their
original paths at their historical commits, while the latest editor preview
is compared against Havora's incoming authored version.

Validation passed:

- Standard ROM build; whitespace checks.
- All 50 renamed maps, warps, connections, event positions and map geometry.
- All 50 legacy map migrations across five saved warp fields; new-game version,
  idempotence, vanilla locations, and rendering of the five settlements.
- PokéGlass paging, app returns, Save cancellation and actual flash write,
  fixed starting outfit, field exit and reopening.
- All 935 move descriptions against Summary, Relearner and both battle layouts.
- Native Kanto/Vidra map frames, independent Center unlocks and five completed
  flights, picker and cancellation cleanup.
- Field tools: actual prompts, travel, Bag Use, registration, flash save and
  Continue, old-HM migration, and all seven retained tools.
- All 27 gym water combinations, existing tile graphics, unchanged puzzle
  controller and incoming editor-preview preservation.

Existing map discrepancies and the editor/runtime gym preview difference are
recorded in [known-issues.md](known-issues.md). They were preserved during the
merge, not silently repaired or treated as passing gameplay checks.
