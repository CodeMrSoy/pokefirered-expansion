# Havora gym water profiles

Based on **67626075 — Finishing touches on Havora Gym**, using the user's latest
**80×27** Porymap map and the supplied ALL LOW, ALL MID, ALL HIGH and collision references.

The all-LOW map is byte-for-byte identical to the latest pushed map.

The two new MID-height landings beside the section 1/2 divider are included:

- Section 1: columns 23–26, rows 13–17; boarding pad at (24,16).
- Section 2: columns 28–31, rows 13–17; boarding pad at (30,16).
- LOW keeps the complete authored deck, stairs and exposed masonry.
- MID keeps the walkable deck/pads at elevation 4 and the existing stairs,
  while the lower masonry is submerged.
- HIGH submerges the full landing footprints, including the lower stairs.

Each landing follows its own section. The new [boat-and-dam trial](directional-tidal-trial.md)
uses the two lower pads for a MID-only boat crossing over the submerged A/B dam;
it does not add bridge artwork. Section C's authored crossing remains LOW-only and is
required to walk between its two sides. All authored cells and water silhouettes
remain intact. Gameplay bindings and trainer clearances are documented separately.

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

- `authored.bin`: latest Porymap LOW baseline plus the approved per-station
  switch color artwork.
- `reference_states/all-low.bin`, `all-mid.bin`, `all-high.bin`: complete height
  snapshots, including water, masonry, furnishings and submerged collisions.
- `overhead_lock_geometry.py`: combines those independent section profiles and
  generates the RLE header; does not add paths or change puzzle rules.
- `map.bin`: authoritative compiled LOW baseline. Future Porymap edits survive
  entry/reset; incorporate later edits into the snapshots before explicitly
  regenerating these overlays.

## Validation

`tests/havora_section_water.py` checks the exact latest baseline, all 27
combinations, MID island access, MID roof collision, HIGH submersion, and the MID lower landing footprints.

`tests/havora_tidal_trial_emulator.py` checks native map tiles for all 27
combinations, actual LOW/MID/HIGH/MID/LOW transitions, live captain removal and
return, and correct hiding after map re-entry. ROM build succeeds.

Previews: `review/water-island-cycle.gif`, `review/water-bunker-cycle.gif`, and
`review/water-all-low.png`, `water-all-mid.png`, `water-all-high.png`.

## Annotated Section A corrections

At MID and HIGH the entrance threshold (2–4,26) is covered by water. The
complete authored boat hull shifts left with the shoreline without leaving
outline fragments. The upper terrace fascia (22–25,13) remains exposed at MID
and is submerged at HIGH. LOW and the MID stair-to-pad route are preserved.
`fix_section_a_profiles.py` reproduces these changes; `render_section_a.py`
renders the current comparison from native metatiles.

The second annotated correction makes the A gate four tiles tall (rows 22–25).
The wall cell above it is completed at LOW/MID. Its face is hidden whenever A
is HIGH, even if B is LOW; unequal water still blocks boat passage. The MID
left quay's side face at (5,7–9) is continuous beside the hull.
