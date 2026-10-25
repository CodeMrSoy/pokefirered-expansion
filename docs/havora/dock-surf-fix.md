# Havora dock Surf correction

Two map-data problems prevented Surf at exposed dock edges:

- Fifteen bottom/end pieces remained at elevation 1, matching the water, while the rest of the docks had been changed to elevation 3. Twelve Harbor cells and three West Quadrant cells now use elevation 3.
- Secondary metatile 0x2BC is an exact graphical duplicate of animated water 0x282, but its attributes were zero (normal land). This blank cell is also used around sailboats and extensively beside the western dock. It now shares 0x282’s water behavior, terrain, encounter and layer properties. Actual boat graphics are unchanged.

No tile graphics, cliff shapes, collision bits, map connections, headers, ferry scripts, events, or warps change. No engine-wide elevation checks are relaxed. Boats, railings, rocks and occupied ferry cells are not new launch points.

The development ROM compiled successfully. The mGBA regression audits 99 dock cells and completes 48 native Surf launch/dismount round trips across the Harbor and West Quadrant. The fixture checks the normal Surf eligibility function, invokes the original Surf field effect with a test party, then lands through real directional input; badge/party progression is intentionally outside this map regression. Dock cells without exposed water are reported separately. `check_dock_surf.py` verifies every retained map/border, tileset and event against source commit 6776592f, allowing only the 15 elevation values and the single water attribute entry. Puzzle/cliff preservation also passes.
