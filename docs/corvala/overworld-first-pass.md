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

## Native animated sand shoreline

The beach now uses native General sand 0x115. Cardinal edges, convex corners and diagonal concave caps are assembled from the existing General surf tiles (0x250–0x264) by retaining each quadrant's original descriptors. These point to the original primary animation graphics 464–481, preserving flips and palettes. General's existing callback updates all eight surf frames every eight engine ticks; there is no new runtime callback and no duplicated animation data.

Autotiling runs after platforms, cliffs and props are placed, and only actual visible water qualifies as a water neighbor. This removes spurious surf along piers and walls. The neighboring ocean is native General 0x12B so its water matches the shore; low-tide shallow-water cells retain their wading behavior via native descriptors with separate attributes. Pilings overlay the animated water rather than carrying a static painted water background. Reef props match the native ocean's background color.

`python tools/corvala/render_animation.py` renders the actual checked-in animation PNGs through the packed map descriptors. It verifies eight distinct surf frames over the map's shore cells and exports a sixteen-frame GIF spanning the ocean/surf animation cycle. This is an asset-derived preview, not an emulator capture. `validate_map.py` verifies the General primary callback and the live primary animation references. In-game verification remains pending the build toolchain.

## Native house cleanup

House rendering now comes from `tools/corvala/houses.py`, replacing the earlier procedural house drawing. Three designs are extracted directly from the repository's native FireRed maps: Pallet Town (5,3,5,5), Cerulean City (13,14,7,4), and One Island (18,6,5,4). Their source metatile grids and original door columns are recorded in `tools/corvala/map.json`. Native roof planes, corrugations, eave profiles, window recesses and door details remain at 1× pixel resolution. No interpolation or outside asset imports are used.

Blue homes use the wide Cerulean silhouette; green homes use the Sevii roof/front; gold homes and the northwest residence use the Pallet silhouette. Five-column source houses gain native center columns to fit a seven-column frontage. Background grass/cliff fragments outside the native building silhouettes are removed. The timber wall palette is separated from colored roof banks, preserving blue window glass independently of roof color. Shared wall/roof materials fit within the secondary tileset's graphics budget.

Door approaches follow actual source warp columns instead of assuming centered doors. All seven house approaches are checked in each tide illustration. The southern gold house moves one tile north on its existing platform to leave a usable front porch. House interiors and their warp events remain pending. Original house art attribution: Game Freak; source bytes are already in this repository.

## Concept-specific stilt houses

The active house kit is now `tools/corvala/stilt_houses.py`. The supplied concept requires taller timber-front homes with pitched or hipped roofs, upper/lower windows, deep eaves, framed gables, porch rails and short exposed supports. These custom silhouettes replace the generic Kanto/Sevii outlines while retaining FireRed-scale window and door pixels. The north/south roof ridge has visible depth, and upper-left lighting is consistent across framing and roof planes.

Native material details come from the preserved `houses.py` kit: Pallet window crop (16,62,32,74) and Sevii door crop (16,80,32,96). These are transferred without scaling. Colored roofs use banks 9–11; timber faces and blue glass use bank 7. House dimensions remain seven by six metatiles, with centered doors at column 3 and unchanged front approach positions. Provenance marks the native source rectangles as references rather than the final custom geometry.

Validation: packed preview equality, palette and metatile bounds, source material anchors, all seven entrances in each tide illustration, and all eight native shoreline animation frames. The scene remains a work in progress relative to the concept; no in-game capture is claimed.
