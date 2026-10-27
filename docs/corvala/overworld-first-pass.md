# Corvala overworld — reference refinement

Development branch: Corvala-dev.

The supplied concept's low-tide panel guides the map's geography: a northwest bluff residence, a recessed northeast sea cave, a central red-roofed Pokémon Center, blue/green/gold timber houses on individual platforms, two southern homes, a lighthouse rock, and the long southern arrival pier. Replaces the first draft's uniform retaining walls and small repeated houses with a native-resolution art kit and irregular bay contours.

The General/Corvala tileset pair remains independent from Havora. New reusable art is authored in `tools/corvala/art.py`: timber houses with visible roof planes, coastal trees, cave mouth, cliff textures, coral gardens, reef rims, shore edges, railings, stairs, pier supports, lanterns, and lighthouse. Six explicit GBA palettes and reflected tile deduplication keep the complete kit within the secondary tileset's 384-graphic budget.

Build with `python tools/corvala/build_map.py`; this overwrites the installed Corvala map and tileset, so preserve Porymap edits first. The game uses LOW tide. MID and HIGH renders are artwork previews, not functioning game states. The map builder checks all three states for walkable connections from the north exit to the east exit, Pokémon Center, lighthouse approach, and arrival pier.

Center warp 0 is at (28,18), elevation 3. Existing return warps and north/east seam coordinates are preserved.

Validate with `python tools/corvala/validate_map.py`. This checks actual GBA palette precision, metatile and tile budgets, descriptor references, the native Center door, and pixel equality between the independent packed-tile renderer and the map preview. Generator output is checked for determinism.

Remaining work: further cliff/reef contour polish, distinctive building variants, interiors and their door warps, NPCs, encounters, cave maps and runtime tides. Some stylization remains compared with the concept's much higher detail density. This is a map art pass, not a completed town.

ROM build/in-game validation remains unavailable in this workspace: arm-none-eabi-gcc and libpng development headers are missing. No ROM compilation or emulator verification is claimed.

## FireRed perspective cleanup

The camera remains the Gen III elevated overhead view. Houses now allocate most of their visible height to the roof, with a short south-facing front wall, staggered roof shingles, overhang shadow, recessed 16-pixel doorway, and contact shadow under the porch. The lighthouse cupola has a visible elliptical top. Pier fronts and reef shelves have short shaded faces below their top planes. The long southern pier is a boardwalk with a short stair flight at the landing.

`tools/corvala/native_reference.py` reuses the repository's native FireRed General art at 1× resolution. Broadleaf tree metatiles are 0x14/0x15, 0x1C/0x1D, 0x24/0x25; rock materials use 0x71 and 0x79. Pixel silhouettes and texture clusters are retained while colors are matched to Corvala's palettes. Source: the existing FireRed General tileset, originally Game Freak. No community asset pixels were imported in this pass.

Community style research (references, not imported assets):
- Ekat's Public Gen 3 Tilesets: https://eeveeexpo.com/resources/621/
- Foxowl's Public Gen 3 Tiles: https://eeveeexpo.com/resources/565/
- Alistair's Gen III Johto Tile Set: https://mail.eeveeexpo.com/resources/1858/

These establish the native-scale roof surfaces, terrain tops/faces, short walls, clustered vegetation, and consistent depth cues used as the art direction. Any later asset import must retain its author's stated per-set credits.
