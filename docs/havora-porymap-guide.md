# Havora Harbor — Porymap editing guide

Open `QuantumHarbor` on `Havora-Development`. The map is 40×32. Its tileset pair is `gTileset_HavoraPrimary` + `gTileset_HavoraHarbor`. The two city approaches use this same pair.

## Reusable blocks

IDs below are the combined map metatile IDs shown in Porymap (hex). Building parts are stored row by row. `tools/havora/assets.json` contains every exact grid.

| Piece | Metatile IDs | Size in blocks |
| --- | --- | --- |
| bollard | `0x283` | 1×1 |
| crane | `0x280`, `0x284`, `0x285`, `0x286`, `0x287`, `0x288`, `0x289`, `0x28A`, `0x28B`, `0x28C`, `0x28D`, `0x28E` | 3×4 |
| dock_east | `0x28F` | 1×1 |
| dock_foot | `0x290` | 1×1 |
| dock_foot_east | `0x291` | 1×1 |
| dock_foot_west | `0x292` | 1×1 |
| dock_se | `0x293` | 1×1 |
| dock_sw | `0x294` | 1×1 |
| dock_west | `0x295` | 1×1 |
| house | `0x296`, `0x297`, `0x298`, `0x299`, `0x29A`, `0x29B`, `0x29C`, `0x29D`, `0x29E`, `0x29F`, `0x2A0`, `0x2A1`, `0x2A2`, `0x2A3` | 4×4 |
| lighthouse | `0x2A4`, `0x2A5`, `0x2A6`, `0x2A7`, `0x2A8`, `0x2A9`, `0x2AA`, `0x2AB` | 2×4 |
| planter | `0x2AC` | 1×1 |
| quay_east | `0x2AD` | 1×1 |
| quay_north | `0x2AE` | 1×1 |
| quay_se | `0x2AF` | 1×1 |
| quay_south | `0x2B0` | 1×1 |
| quay_sw | `0x2B1` | 1×1 |
| quay_west | `0x2B2` | 1×1 |
| rock | `0x2B3` | 1×1 |
| sailboat | `0x2B4`, `0x2B5`, `0x2B6`, `0x2B7`, `0x2B8`, `0x2B9`, `0x2BA`, `0x2BB`, `0x2BC` | 3×3 |
| warehouse | `0x2BD`, `0x2BE`, `0x2BF`, `0x2C0`, `0x2C1`, `0x2C2`, `0x2C3`, `0x2C4`, `0x2C5`, `0x2C6`, `0x2C7`, `0x2C8`, `0x2C9`, `0x2CA`, `0x2CB`, `0x2CC`, `0x2CD`, `0x2CE`, `0x2CF` | 5×5 |
| stone | `0x280` | 1×1 |
| wood | `0x281` | 1×1 |
| water | `0x282` | 1×1 |

## Keep travel working

- Keep the ferry at (25,17), sailor at (20,17), and arrival at (20,16). The sailor must remain reachable from (20,18).
- The north and west borders connect outdoors through `QuantumHavoraNorthQuay` and `QuantumHavoraWestQuay`. Keep reciprocal connections and matching elevation 3.
- Harbor buildings are exterior scenery. Doors do not currently have interior warps.
- Walking ground uses elevation 3 / collision 0. Buildings, planters and pier lips use collision 1. Water and decorative boats remain blocked.
- A tall prop can be walked behind where its upper tiles retain the ground collision. Its feet should block movement.
- The lighthouse plaque remains at (36,25), read from (36,26).

## Save and build

Porymap edits belong in `data/layouts/Quantum_Havora_Harbor_Layout/map.bin` and the usual map JSON / tileset files. Commit all files Porymap saves.

**After manual layout edits, do not run `tools/havora/build_map.py` or `emerald_harbor.py`: they regenerate the approved layout and overwrite those edits.** `build_assets.py` regenerates the tileset and asset catalog. Ordinary ROM builds do not run these scripts.

Run `python tests/havora_layouts.py` after layout changes. It checks every unoccupied walking tile is connected, the ferry route, map dimensions and connections. Existing tests protect the current promenade edges and docking lips; update them deliberately when redesigning those areas.

The import currently uses 86 of 384 secondary metatiles and 193 custom 8×8 graphics. Original art cutouts, the dark wood recolor and source attribution are in `tools/havora/source_art/emerald_harbor/`. Unplaced quay corner and bollard blocks are also available for polishing.
