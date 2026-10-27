# Corvala overworld — reference refinement

Development branch: Corvala-dev.

The supplied concept's low-tide panel guides the map's geography: a northwest bluff residence, a recessed northeast sea cave, a central red-roofed Pokémon Center, blue/green/gold timber houses on individual platforms, two southern homes, a lighthouse rock, and the long southern arrival pier. Replaces the first draft's uniform retaining walls and small repeated houses with a native-resolution art kit and irregular bay contours.

The General/Corvala tileset pair remains independent from Havora. New reusable art is authored in `tools/corvala/art.py`: two-storey timber houses, coastal trees, cave mouth, cliff textures, coral gardens, reef rims, shore edges, railings, stairs, pier supports, lanterns, and lighthouse. Six explicit GBA palettes and reflected tile deduplication keep the complete kit within the secondary tileset's 384-graphic budget.

Build with `python tools/corvala/build_map.py`; this overwrites the installed Corvala map and tileset, so preserve Porymap edits first. The game uses LOW tide. MID and HIGH renders are artwork previews, not functioning game states. The map builder checks all three states for walkable connections from the north exit to the east exit, Pokémon Center, lighthouse approach, and arrival pier.

Center warp 0 is at (28,18), elevation 3. Existing return warps and north/east seam coordinates are preserved.

Validate with `python tools/corvala/validate_map.py`. This checks actual GBA palette precision, metatile and tile budgets, descriptor references, the native Center door, and pixel equality between the independent packed-tile renderer and the map preview. Generator output is checked for determinism.

Remaining work: further cliff/reef contour polish, distinctive building variants, interiors and their door warps, NPCs, encounters, cave maps and runtime tides. Some stylization remains compared with the concept's much higher detail density. This is a map art pass, not a completed town.

ROM build/in-game validation remains unavailable in this workspace: arm-none-eabi-gcc and libpng development headers are missing. No ROM compilation or emulator verification is claimed.
