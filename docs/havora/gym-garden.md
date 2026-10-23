# Havora western gym garden

Uncommitted review patch based on `a8b19167` (the user's latest collision, city and boundary cleanup).

The empty gym plateau now contains an evergreen lookout garden, two timber seating areas, a fenced 10x8 practice court with four dialogue trainers, flowers, native rocks and bushes, and linked stone paths. The front-door apron connects around the gym's right side, to both original stairways and the northern entrance. The surrounding coastal cliffs, river, gym building footprint, map dimensions, borders and connection offsets are preserved.

The court uses dialogue actors, not new trainer battles. The gym's leader, battle teams, doubles enforcement, Crest and interior puzzle remain separate design work. The gym sign identifies the partner practice court. The existing Gym Guide and gardener are moved onto walkable terrace cells. The original gym-door warp keeps its index, coordinates and destination, with elevation corrected from 5 to the door block's actual elevation 6.

Three previously blank primary metatiles (492, 494, 495) provide sand and two wooden bench halves, built entirely from existing graphics. No existing metatile definitions, palette entries, tile graphics, or animation slots change. Four practice actors bring the map to 14 object events, within the engine limit of 16.

Validation: `python tools/havora/check_gym_garden.py` passes. It checks the change boundary, original cliff/sea preservation, all other Havora map binaries and borders, original metatiles/graphics/palettes, warp coordinates, and walking routes with NPC occupancy and gym walls treated as obstacles. All seven local destinations are accessible. `git diff --check` passes. The complete ROM compiles successfully with ARM GCC; log: `build/gym-garden/build-final.log`. No Porymap UI or emulator walkthrough was performed.

The broad legacy city audit stops at an existing issue outside this patch: `QuantumHavoraNorthLodge` exits to North Quadrant warp 7, while that map currently has five warp entries. It is left unchanged so the gym-garden patch does not alter other districts.

Preview images are native tile-and-sprite renders, not generated concept illustrations or Porymap screenshots. `gym-garden-preview.png` shows the plateau; `gym-garden-connected.png` shows the full city using actual connection offsets.

## Later editor-kit expansion

The court now has white chalk lines and a Poké Ball motif. Complete market stalls and the requested Bond Bridge forest mouth have been added to the shared tile palette for manual placement. This expansion reclaims archived, unplaced catalogue art; the earlier statement that all unplaced definitions and graphics remain untouched applies to the initial garden patch only. See editor-kits.md and editor-kits.json for current details. The combined build passes (build/editor-kits/build.log).
