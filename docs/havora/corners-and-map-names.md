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

## Native FireRed houses

The roof recolors and narrowed Lilycove cottages have been removed. Use
`native-houses.png` and the hexadecimal grids in
`tools/havora/native-houses.json` for the original Pallet two-story house and
Cerulean single-story home designs. Both use HavoraCityPrimary / HavoraCity.
Source map footprints and metatile IDs are recorded in the manifest.

House pixels retain the original FireRed designs, fitted to the existing shared
palette; roof-edge backgrounds use Havora grass. No palette files or placed map
blocks change. These are authoring kits: place them in Porymap, set building
collision, and configure door warps/interiors where needed. They do not create
new enterable houses automatically.

All 224 placed metatile definitions and 509 protected catalog definitions retain
their referenced graphics and packed attributes. Animation graphic destinations
are pinned. Reclaimed unplaced catalog art is archived in
`native-houses-archive.json`.

Native-house replacement: 38 definitions added; 70 static graphic slots reclaimed from 31 unplaced catalog definitions. ROM compilation and the corner/topology checks passed again after the replacement. No emulator or Porymap UI test was performed.

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
