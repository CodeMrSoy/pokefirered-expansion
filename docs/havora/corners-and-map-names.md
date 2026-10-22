# Havora corner loading, names and house options

All work is on Havora-Development, based on a85c6562.

## Map names in Porymap

| Previous name | Current name |
| --- | --- |
| QuantumHarbor | HavoraHarbor |
| QuantumHavoraNorthQuay | HavoraMarket |
| QuantumHavoraNorthDistrict | HavoraNorthQuadrant |
| QuantumPortCity | HavoraWestQuadrant |
| QuantumHavoraCoastalDaycare | HavoraDaycare |
| QuantumHavoraWestQuay | HavoraRiver |
| QuantumHavoraNorthWalk | HavoraLookout |
| QuantumHavoraCliffs | HavoraCoastalCliffs |

Map directories, layout directories/IDs, scripts, connections, incoming return
warps, ferry references and the map group table use the new names. The map group
order is identical, preserving the numeric map IDs used in saves. The region
section and the existing interiors retain their established IDs.

## Four-map corner

The North quadrant's east edge gains one repeated edge column, making its width
90. Every pre-existing authored block stays byte-identical at its original map
coordinate. Daycare begins one row above the North quadrant so its complete
29-row artwork ends flush with Market and Coastal Cliffs. Its east/west link
uses offsets -1 / +1. The River / Harbor link now uses +62 / -62, matching the
Market's 62-row height. All eleven connection pairs and placement loops agree.

FireRed normally copies only cardinal neighbor strips. Its diagonal camera
corner can therefore show a forest border, grass or water from the active map
instead of the fourth district. A loader scoped to HavoraCityPrimary fills only
undefined corner cells from a two-hop neighbor with the exact same tileset pair.
It preserves the current map and all existing cardinal strips. Other regions
are excluded by the primary-tileset guard.

The four-corner PNG is a native map-data simulation of the old border fallback
and corrected diagonal loading, not an emulator screenshot. Its bottom row
shows the same junction from all four active districts.

## House variety

Use HavoraCityPrimary / HavoraCity. `house-variety.png` shows four complete kits:
brick-red house, brick-red cottage, coastal-teal house, and coastal-teal cottage.
The narrower cottages use three columns while the houses use four. Assemble
using the hexadecimal grid in `tools/havora/house-variants.json`; apply solid
building collision and door-warp/elevation settings as appropriate to the map.

Twelve new roof metatiles reuse the existing wall and door pieces. Seventeen
static graphic slots were reclaimed from eight unplaced, unprotected catalog
entries. Their original definitions and graphics are retained in
`house-variants-archive.json`. All 224 placed metatile definitions and 509
protected catalog entries retain their graphics, attributes and referenced
pixels. Animation destinations and palette files are unchanged.

## Verification and limits

- ROM compilation passed with ARM GCC 13.2.1.
- `python tools/havora/test_corner_buffer.py`: compiled C regression test of the
  actual loader functions, across all four viewpoints; 49-56 corner cells filled
  per view; existing main/cardinal cells and non-Havora maps preserved.
- `python tools/havora/check_topology.py`: names, dimensions, border lengths,
  numeric map IDs, all original authored cells and reciprocal placement checked.
- No Porymap UI or in-game walking/ferry test was performed.

The latest source resize already left several NPC/door events outside their
layouts. They are listed in topology-review.json and require a separate event
placement pass. This change preserves those authored events while updating their
map references. It does not claim those pre-existing event positions are valid.
