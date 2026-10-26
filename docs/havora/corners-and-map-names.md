# Havora corner loading, names and house options

Work targets Havora-Development only. The current housing update starts from
5ece37d9; the original corner/name migration started from a85c6562.

## Map names in Porymap

| Previous name | Current name |
| --- | --- |
| QuantumHarbor | Havora_Harbor |
| QuantumHavoraNorthQuay | Havora_Market |
| QuantumHavoraNorthDistrict | Havora_NorthQuadrant |
| QuantumPortCity | Havora_WestQuadrant |
| QuantumHavoraCoastalDaycare | Havora_DaycareExterior |
| QuantumHavoraWestQuay | Havora_River |
| QuantumHavoraNorthWalk | Havora_Lookout |
| QuantumHavoraCliffs | Havora_CoastalCliffs |

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

## Selected FireRed housing and department store

The active residential designs outside the harbor are the long Cerulean house
and the plain / garden-front Viridian houses shown in the reference. The blue
Lilycove houses remain on Havora_Harbor. The unused Pallet option is superseded.

Eight existing buildings were replaced within reviewed plots: four in Market,
two in North Quadrant, one in West Quadrant and the Daycare frontage. The long
home uses an eight-column arrangement of the original Cerulean modules. Changed
doors retain their interior destinations and exterior warp indices; the existing
interior return warps point to those indices. Door/landing collisions, matching
elevations, door behaviors and reciprocal return references pass data checks.

The native Celadon Department Store fits as a complete 9x10 metatile authoring
kit. It has not been placed and has no new Havora interior. Assemble it using
`tools/havora/green-houses.json`, then configure a plot and interior when placing
it. `green-houses.png` previews the available buildings; the connected city view
is `connected-green-houses.png`. These are native data renders, not UI captures.

71 new metatile definitions use 98 reclaimed static graphic slots. Only
unplaced, obsolete catalog pieces were retired; their original definitions and
graphics are in `green-houses-archive.json`. The authoring catalog has been
filtered so it no longer advertises retired pieces. Original FireRed geometry
is adapted to the shared Havora palette, with contrasting green roof stripes.

The existing 224 placed metatile definitions and their referenced graphic pixels
remain unchanged. All 2,397 cliff/stair map cells, every border, all connection
offsets, harbor data, palette colors and fixed animation destinations are
preserved. Only the reviewed house plots and their door approaches change.

## Verification and limits

- ROM compilation passed with ARM GCC 13.2.1.
- `python tools/havora/test_corner_buffer.py`: compiled C regression test of the
  actual loader functions, across all four viewpoints; 49-56 corner cells filled
  per view; existing main/cardinal cells and non-Havora maps preserved.
- `python tools/havora/check_topology.py`: names, dimensions, border lengths,
  numeric map IDs, original art outside reviewed house plots, and reciprocal placement checked.
- No Porymap UI or in-game walking/ferry test was performed.

The latest source resize already left several NPC/door events outside their
layouts. They are listed in topology-review.json and require a separate event
placement pass. Unrelated existing event placement issues remain; only the eight replacement
buildings have their exterior door coordinates updated. It does not claim those pre-existing event positions are valid.
