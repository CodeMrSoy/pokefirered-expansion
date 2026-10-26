# Havora gym: authored layout, water profiles, and solution

Based on Havora-Development commit e7737e147 (the manually edited 80×29 map).
The gym runtime now uses that footprint, the moved controls, and the captain's
platform below section C's walkway. No outdoor map or trainer team was edited.

## Visual changes

The three supplied pictures define the individual pools' LOW, MID, and HIGH
silhouettes. They are local height references, rather than a three-picture cycle:
the existing puzzle conserves four transferable water units, so High/Low/Low
is not a reachable simultaneous arrangement. Berths remain fixed while side
walls and lower shelves flood in place. A hull-width route passes below the
captain's quay. The upper galleries and gates preserve the puzzle connections.

Fourteen private brick metatiles occupy 0x3C5–0x3D2. The kit includes paired
side faces, rounded upper and lower corners, inward returns, coping and front
faces. The runtime places contours along exposed brick/water boundaries,
preserving collision and elevation. Graphics and palettes outside the private
gym pair are unchanged. Existing glyphs and boat graphics are retained.

## Puzzle solution

A, B and C mean sections 1, 2 and 3. Initial levels: HIGH / HIGH / LOW.
Clear the five crew encounters in order as you meet them; captain Eirik requires
all five victories and six usable Pokémon. The entrance attendant heals free.

1. Ride the launch from A's west quay to B's west quay.
2. Transfer **B → C**. Ride the launch to C's control quay.
3. Take the cargo boat to B's west quay.
4. Transfer **C → B**. Ride cargo to B's upper service berth.
5. Secure cargo as the service bridge. Cross to the service platform.
6. Transfer **B → C**, release the mooring chain on the lower shelf, then
   transfer **C → B**.
7. Return over the service bridge, release cargo, and ride it to B's west quay.
8. Transfer **B → C**. Ride cargo to C's outer mooring.
9. Transfer **C → B**. Cross C's exposed lower walkway to the control quay.
10. Transfer **B → C**, **A → B**, **B → C**, **A → B**, in that order.
    Final levels: LOW / HIGH / HIGH.
11. Tension cargo as the final bridge from C's control quay.
12. Ride the launch to B's upper service berth. Cross the final walkway and
    descend to Eirik's platform below C's walkway.

A machinery reset returns the player to (3,27) and retains trainer victories.
Old gym-state saves migrate to that safe entrance.

## Authoring sources

- `data/layouts/HavoraCaptainsTrial/authored.bin` is a preserved copy of the
  user's pushed Porymap plan, never overwritten by the builder.
- `reference_states/` stores the decoded three reference silhouettes. Only
  structural water/masonry cells are used; screenshot props are not imported.
- `tools/havora/overhead_lock_geometry.py` builds runtime RLE overlays and the
  initial `map.bin`; its geometry is also used by the state/route checks.
- `tools/havora/add_brick_cliff_kit.py` rebuilds only the private brick kit.

Porymap edits to `map.bin` must be intentionally incorporated into `authored.bin`
before rebuilding overlays; otherwise the generated initial view will replace
those map edits. Update geometry and control coordinates when moving quays.
The previous 80×40 layout builder must not be restored.

## Validation

- ROM builds successfully.
- 837 reachable map states match the abstract walking/elevation graph.
- All 570 legal boat trips have a collision-free route for the full 3×3 hull.
- Emulator completes the full 25-action route to the relocated captain.
- Actual boarding menu, valve prompt, machinery reset, exit, saved-state
  re-entry, and legacy-state migration pass.
- A stationary-camera cycle verifies LOW/MID/HIGH/MID/LOW with a fixed berth.
- Tile kit and map-overlay generation are byte-for-byte reproducible.

Battle balance is unchanged by this map/artwork update.
