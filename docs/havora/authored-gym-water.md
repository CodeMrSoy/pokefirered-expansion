> Current rules: [directional color-switch trial](directional-tidal-trial.md). The recipe-based rules below are historical.

# Havora gym: artwork-first revision

Latest water artwork: see [section-water-profiles.md](section-water-profiles.md), based on the user's 80×27 commit 67626075.

The user's layout and original metatiles are restored. The starting/default
water levels are **LOW / LOW / LOW**. Platforms and walkways follow the supplied
pictures; the captain's furnished platform remains below section C's walkway.
The generated upper galleries, gangplanks, gates, automatic cliff placements,
and extra channel geometry from the previous revision have been removed.

## Brick cliff kit for manual placement

The new kit follows **28 native FireRed cliff silhouettes**, with brick texture
in the existing gym colors. Each shape has an animated-water background and an
original-wood background: **56 metatiles, 0x3C5 through 0x3FC**. Convex corners,
concave corners, side faces, thicker fronts, feet and connecting returns are
included. The water renderer does not place new pieces automatically; it preserves the user's subsequent Porymap placements.

`tools/havora/brick-cliff-kit.json` lists every source cliff and destination ID.
Run `python tools/havora/add_brick_cliff_kit.py` to reproduce the kit. It preserves
all existing metatiles and used graphics and does not modify map cells.

Previews:

- `review/water-all-low.png`: latest starting map.
- `review/native-brick-cliff-kit.png`: complete catalog with metatile IDs.
- `review/native-brick-cliff-example.png`: separate kit assembly example;
  this demonstration is not part of the gym layout.
- `review/reference-high-low-low.png`, `review/reference-mid-high-mid.png`,
  `review/reference-low-mid-high.png`: the three supplied height arrangements.

## Puzzle status

The conserved-water/cargo puzzle has been replaced by the playable
[seven-station tidal trial](tidal-trial.md). All 21 authored switches now have
bindings. Each platform requires successful switch operation and its crew's
water-level challenge. All seven crews guard Eirik's LOW bunker.

The new rules keep these artwork profiles. A/B's lower platforms are MID-height;
C's crossing is LOW-height. Gauge panels offer reset/return without losing
victories. Switch colors now vary by station; the approved color assignments are
listed in `directional-tidal-trial.md` and recorded in the authored layout and
each height snapshot. Command 26 remains an emulator-only independent water preview.

## Preserve subsequent Porymap edits

`map.bin` is the compiled all-LOW default and is authoritative on map entry,
resume and reset. The renderer overlays only changes from this default; it does
not rebuild galleries, gates, boat approaches or cliff placements. Subsequent
Porymap edits to the default map therefore survive normal play. The switch tile
colors are the one intentional artwork update; their corresponding tile IDs are
kept aligned across all authored height snapshots.

The explicit overlay builder still reads the preserved `authored.bin` snapshot
and the three reference silhouettes. Do not run that builder over new Porymap
edits until those edits have intentionally been incorporated into the snapshot
and height profiles. Puzzle rules are generated separately from `tools/havora/tidal_trial.json`.

## Validation

See `tidal-trial.md` for the playable puzzle solver, native emulator checks and
build validation. `havora_section_water.py` and `havora_artwork_assets.py` retain
the original graphics, all-LOW map and all 27 height profiles. Historical
cargo-boat/artwork-review-only tests describe retired revisions.
