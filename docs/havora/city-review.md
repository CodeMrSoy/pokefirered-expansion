# First Havora city planning review — superseded

Current draft: see city-review-natural.md. The revised draft intentionally edits
the Market coast/border and repairs the Center/Mart assets; preservation claims
below describe the earlier preview only.

This draft starts from ac291bc1 on Havora-Development. No commit or push has
been made. The generation script reads that baseline and is safe to rerun while
reviewing this exact draft; it must not be used to overwrite subsequent Porymap
work without a new baseline.

Changes:

- Three animated fountain placements: market square, gym forecourt and northern
  civic garden. All use the existing shared fountain animation.
- Eleven additional houses: seven on the western terraces and four in the north.
  Existing unused house interiors and their warp indices serve the new homes.
- Remaining orange residential/workshop fronts in Market replaced by the selected
  Viridian designs. Blue harbor housing stays unchanged.
- Eight market stalls around broad browsing aisles and a statue meeting point;
  vendors use the existing working market-shop interaction.
- Celadon Department Store facade on the lower market terrace, with two doors
  linked to the existing Havora provisions shop. A dedicated multi-floor store
  interior is outside this visual draft.
- Complete Center/Mart roofs, corrected civic doors, planted garden paths,
  flowers, shrubs and tree groves. No new route exits added.
- NPC coordinates corrected after earlier resizes, and actors moved out of solid
  scenery. No map has more than sixteen outdoor NPCs.

Preserved: harbor layout/scripts/ferry, tilesets, map dimensions, borders,
connection offsets, cliff/water/stair cells and existing interior destinations.
The original exterior warp indices are retained; the store's second door returns
through its main doorway.

Validation: ROM compilation passed. Read-only data checks cover 26 exterior door
warps, reciprocal interior references, NPC bounds, 3,718 unchanged terrain/water
cells and collision-level routes from the market to every door approach. Seven
traversable districts are connected; Coastal Cliffs is the existing decorative
coast extension. No emulator walking test or Porymap UI test was performed.

Review images are native renders of these actual edited maps, with their real
connection offsets: city-review-connected.png and city-review-market.png.
