# Corvala overworld — first map pass

Branch: feature/corvala-overworld, based on Pokemon-Quantum-V2 db333930c.

Replaces the 24×24 placeholder with a 56×60 low-tide layout. Includes raised wooden residential platforms, a Pokémon Center, a market stall, a lighthouse platform, a southern landing, coral shelves, and a reserved northeast cave approach. Existing north/east connections retain their original seam coordinates. Center warp remains index 0 and has moved to (26,20).

Uses an independent General/Corvala tileset pair. Native harbor source art is reused from the checked-in Havora asset pack; reef, shore, stone, rail, and support tiles are authored at 16×16. Native buildings remain at their original scale. Build with `python tools/corvala/build_map.py`; this deliberately overwrites the Corvala layout, so preserve Porymap edits before running it.

Validation: native palette/metatile rendering inspected; native graphic and metatile capacities checked; palette length and map bounds checked; collision flood-fill connects the north/east routes, Center doorway, lighthouse platform, and southern landing. `git diff --check` passes.

ROM build attempted but blocked by missing arm-none-eabi-gcc and libpng development headers in this environment. No in-game validation claimed.

Pending: finer cliff contours and coral variety, finished shoreline corners, stilt-house variations, house/market interiors and warps, cave maps, NPCs, encounters, and tide-state logic. Low/mid/high state artwork and changing collision are not implemented in this first map pass. The reef and cave areas must be revisited with the tide design; no real-time clock behavior has been added.
