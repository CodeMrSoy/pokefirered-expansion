# Revised Havora preview — uncommitted

This revision supersedes the first city-review preview. No commit or push has
been made. Current images: city-review-natural.png, market-natural-detail.png,
and civic-repair.png.

The Center was cropped from a five-column source into four columns. Its complete
FireRed footprint is 5x4, sourced from Vermilion (13,3). The Mart's 4x4 footprint
was complete, but both roof textures had collapsed during palette fitting.
The revised import retains distinct shade indices for their roof grids and
restores the Center's right wall. Both service buildings now sit at row 5 in
North Quadrant with doors at row 8, clear of the original ridge. Former roof
openings in the ridge are closed using adjacent native cliff tiles.

An unused shared palette 0 slot 7 supplies the missing dark-red shade. Static
references and animated flower/water references were checked before repurposing
it. Two unplaced obsolete Lilycove modules (807 and 809) supplied the final
repair slots and are archived. All other non-service definitions, their pixels,
all animation destinations and the harbor graphics remain unchanged.

The market stalls now form uneven clusters with planted gaps, rather than two
matching rows. The fountain is slightly off the visual axis. The eastern market
edge borrows a native western-coast cliff stencil and rounds into a small tidal
inlet beside the lower shopping terrace. Sixty-two cells define the permitted
coast edit area; all other existing terrain is preserved. The Market border is
now ocean, matching the unconnected seaward edge. Map dimensions, cardinal
connection offsets, the river and harbor remain unchanged.

Validation: ROM compilation passed. All 26 door approaches remain reachable by
collision-level route checks, all NPC/warp positions are in bounds, vendors
stand on walkable tiles, and fountain scheduling checks pass. Asset checks
verify the full service-building grids, unused palette slot, unchanged harbor
pixels and unchanged flower/water/fountain animation graphics. No emulator or
Porymap UI test has been performed.

Replay order while reviewing this exact draft: repair_civic_tiles.py (one-time,
manifest guarded), design_city_review.py, naturalize_market.py. The design script
reads ac291bc1 baseline map data; never rerun it over later Porymap edits without
updating the baseline and the reviewed placement plan.
