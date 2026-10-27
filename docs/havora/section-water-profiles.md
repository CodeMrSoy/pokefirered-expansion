# Havora gym water profiles

Based on **6ab7bd9e2 — Havora gym update**, using the user's latest **80×27**
Porymap map and the supplied ALL LOW, ALL MID, ALL HIGH and collision references.

The all-LOW map is byte-for-byte identical to the latest pushed map. This update
changes only the water-height profiles, submerged collision, and captain
visibility. Existing puzzle controls, transfers, trainer progression and teams
are unchanged. The existing artwork-review mode remains in place.

| Feature | LOW | MID | HIGH |
| --- | --- | --- | --- |
| B switch island | Original island and switches | Floor and boarding pads accessible; switches visible | Entire footprint covered by water |
| C leader bunker | Original floor, furnishing, approach and Eirik | Solid roof visible; approach flooded; Eirik hidden | Roof and approach completely submerged; Eirik hidden |
| Remaining walls and shelves | Original authored contours | Exposed contour from MID reference | Exposed contour from HIGH reference |

Each section uses its own water level. Filling one section does not alter the
other two. All 27 combinations of LOW/MID/HIGH have complete runtime overlays.
When water drains, the same artwork, collision and captain visibility return.

The latest map's event positions are preserved. Its reset entrance was aligned
to (3,25), immediately above the user's exit warps on row 26. Old saved positions
outside the shortened map are moved safely to that entrance.

The captain uses the map-local temporary hide flag FLAG_TEMP_1F while C is above
LOW. This prevents him appearing when his object streams into view or the player
re-enters the map; lowering C clears that flag and restores his object. Trainer
victories and crest flags are unaffected.

## Source data

- `authored.bin`: preserved latest Porymap LOW baseline.
- `reference_states/all-low.bin`, `all-mid.bin`, `all-high.bin`: complete height
  snapshots, including water, masonry, furnishings and submerged collisions.
- `overhead_lock_geometry.py`: combines those independent section profiles and
  generates the RLE header; does not add paths or change puzzle rules.
- `map.bin`: authoritative compiled LOW baseline. Future Porymap edits survive
  entry/reset; incorporate later edits into the snapshots before explicitly
  regenerating these overlays.

## Validation

`tests/havora_section_water.py` checks the exact latest baseline, all 27
combinations, MID island access, MID roof collision, HIGH submersion, and unchanged
puzzle-control code.

`tests/havora_section_water_emulator.py` checks native map tiles for all 27
combinations, actual LOW/MID/HIGH/MID/LOW transitions, live captain removal and
return, and correct hiding after map re-entry. ROM build succeeds.

Previews: `review/water-island-cycle.gif`, `review/water-bunker-cycle.gif`, and
`review/water-all-low.png`, `water-all-mid.png`, `water-all-high.png`.
