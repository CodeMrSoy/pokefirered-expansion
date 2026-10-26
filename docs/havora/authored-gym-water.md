# Havora gym: artwork-first revision

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
included. No new pieces are placed in the gym automatically.

`tools/havora/brick-cliff-kit.json` lists every source cliff and destination ID.
Run `python tools/havora/add_brick_cliff_kit.py` to reproduce the kit. It preserves
all existing metatiles and used graphics and does not modify map cells.

Previews:

- `review/restored-all-low.png`: starting map.
- `review/native-brick-cliff-kit.png`: complete catalog with metatile IDs.
- `review/native-brick-cliff-example.png`: separate kit assembly example;
  this demonstration is not part of the gym layout.
- `review/reference-high-low-low.png`, `review/reference-mid-high-mid.png`,
  `review/reference-low-mid-high.png`: the three supplied height arrangements.

## Puzzle status

The previous conserved-water puzzle is **retired pending redesign around the
finished artwork**. Its old 25-step solution is not applicable. All-LOW supplies
no transferable water; the replacement puzzle must define how water enters
and drains as well as where the player travels.

Old transfer, sailing and mooring actions are inactive and report that the lock
system is being refitted. Trainer teams and victories are retained. A reset
restores all three pools to LOW. Old gym saves migrate safely to the entrance.

For emulator/authoring review only, special command 26 selects an independent
chamber (0–2 in VAR_0x8005) and height (0–2 in VAR_0x8006). It animates the artwork;
it is not a replacement player puzzle. All 27 height combinations are supported.

## Preserve subsequent Porymap edits

`map.bin` is the compiled all-LOW default and is authoritative on map entry,
resume and reset. The renderer overlays only changes from this default; it does
not rebuild galleries, gates, boat approaches or cliff placements. Subsequent
Porymap edits to the default map therefore survive normal play.

The explicit overlay builder still reads the preserved `authored.bin` snapshot
and the three reference silhouettes. Do not run that builder over new Porymap
edits until those edits have intentionally been incorporated into the snapshot
and height profiles. Updating the puzzle will require updating the profiles
and collision/elevation transitions for the final artwork.

## Validation

- Successful ROM build.
- Existing metatiles and used graphic pixels match the user's pre-rework art.
- The new kit is unplaced; no generated bridge/gallery tiles remain.
- All 27 independent height combinations are valid.
- Emulator checks old-save migration to LOW/LOW/LOW, exact runtime/default map
  agreement, reference height transitions, resets, re-entry and victory retention.
- The old puzzle's movement and transfer actions cannot modify the artwork.

Use `tests/havora_artwork_assets.py` and
`tests/havora_artwork_review_emulator.py` for this revision. The former
837-state/570-route/25-action puzzle checks describe the retired design and
are not validation of a new playable puzzle.
