# Vidra — known issues after map organization

## Existing map and test discrepancies

- `tests/havora_layouts.py` still expects a 40×32 harbor; the current authored
  harbor has different dimensions. The older assertion needs updating against
  the approved artwork.
- `tests/havora_market.py` still expects a 40×64 market; its dimensions also
  differ from the current authored map.
- `tests/havora_civic_layouts.py` finds the Lookout fisher at x=9, y=-7, outside
  the map. Confirm the intended position and place the NPC on reachable land.

The organization change preserves the authored map binaries and event
coordinates. These checks remain failing; they have not been described as
passing or silently disabled. The ROM build, map-reference/geometry-preservation
checks and all 50 legacy map migrations pass.

## Unbuilt locations and compatibility

- Corvala Corals has its canonical name and identity recorded, but no dedicated
  reef or tidal-cave map exists yet.
- Lake Myrvatn labels the existing lake region-map area; there is no separate
  standalone lake map yet.
- Existing saves receive a one-time migration for regrouped maps. Old Vidra
  recap scenes and map-specific RAM scripts are cleared as part of migration.
  Keep an original save backup: saves written with the regrouped map IDs should
  not be loaded in an older ROM.

See [map-organization.md](map-organization.md) for naming, group structure,
validation and the previous-to-current map directory list.
