# Pokémon Quantum — Vidra map organization

The game is Pokémon Quantum; the island is Vidra.

| Settlement | Landmark | Identity |
| --- | --- | --- |
| Havora City | Havora Harbor | Maritime industry and navigation |
| Corvala Town | Corvala Corals | Coral reefs and tidal caves |
| Eldervale Village | Eldervik Woods | Ancient Nordic forest |
| Myrdal City | Lake Myrvatn | Freshwater city and misty wetlands |
| Iskora Village | Frostfell Mountains | Alpine wilderness and frozen peaks |

Each settlement has its own Porymap group containing its exterior maps and
interiors. Roads use VidraRoutes; Eldervik Woods and Frostfell Mountains use
VidraLandmarks. Names follow Place_Description, with _1F/_2F for floors and
_1/_2 for numbered buildings. Havora_DaycareExterior and
Havora_DaycareInterior distinguish the two previously confusing daycare maps.

Existing layout order, tiles, metatiles, collision data, event coordinates,
warp destinations and map connections are preserved. Names and references
change together. Region-map section order stays stable; names update in
Fly, location popups, ferry text, ticket text and the region selector.

Corvala Corals is the designated coastal landmark; a dedicated coral/tidal-cave
map does not exist yet. Lake Myrvatn labels the existing lake region-map area;
a standalone lake map has not been invented as part of this rename.

Old saves migrate their location, heal/escape/return warps and saved object
map pairs once using VAR_VIDRA_MAP_VERSION (0x40FC). Old Vidra recap scenes
and map-specific RAM scripts are retired because they can contain encoded
legacy map IDs. New saves start with the current version. Do not load a save
written with the new group IDs in an older ROM.

## Map directory changes

| Previous name | New name |
| --- | --- |
| HavoraWestQuadrant | Havora_WestQuadrant |
| QuantumPortCityPokemonCenter1F | Havora_PokemonCenter_1F |
| QuantumPortCityPokemonCenter2F | Havora_PokemonCenter_2F |
| QuantumCoastalCity | Corvala_Town |
| QuantumCoastalCityPokemonCenter1F | Corvala_Town_PokemonCenter_1F |
| QuantumCoastalCityPokemonCenter2F | Corvala_Town_PokemonCenter_2F |
| QuantumForestTown | Eldervale_Village |
| QuantumForestTownPokemonCenter1F | Eldervale_Village_PokemonCenter_1F |
| QuantumForestTownPokemonCenter2F | Eldervale_Village_PokemonCenter_2F |
| QuantumLakeTown | Myrdal_City |
| QuantumLakeTownPokemonCenter1F | Myrdal_City_PokemonCenter_1F |
| QuantumLakeTownPokemonCenter2F | Myrdal_City_PokemonCenter_2F |
| QuantumSnowTown | Iskora_Village |
| QuantumSnowTownPokemonCenter1F | Iskora_Village_PokemonCenter_1F |
| QuantumSnowTownPokemonCenter2F | Iskora_Village_PokemonCenter_2F |
| QuantumHarborRoad | Vidra_HarborRoad |
| QuantumCoastalRoad | Vidra_CoastalRoad |
| QuantumWoodlandLink | Eldervik_Woods |
| QuantumMountainPass | Frostfell_Mountains |
| HavoraHarbor | Havora_Harbor |
| HavoraRiver | Havora_River |
| HavoraMarket | Havora_Market |
| QuantumHavoraShipwrightHouse | Havora_ShipwrightHouse |
| QuantumHavoraWeaverHouse | Havora_WeaverHouse |
| QuantumHavoraFisherHouse | Havora_FisherHouse |
| QuantumHavoraTraderHouse | Havora_TraderHouse |
| QuantumHavoraTradeHall | Havora_TradeHall |
| QuantumHavoraOutfitters | Havora_Outfitters |
| QuantumHavoraProvisions | Havora_Provisions |
| HavoraNorthQuadrant | Havora_NorthQuadrant |
| HavoraDaycare | Havora_DaycareExterior |
| HavoraLookout | Havora_Lookout |
| QuantumHavoraGym | Havora_Gym |
| QuantumHavoraMart | Havora_Mart |
| QuantumHavoraDaycare | Havora_DaycareInterior |
| QuantumHavoraWestHouse1 | Havora_WestHouse_1 |
| QuantumHavoraWestHouse2 | Havora_WestHouse_2 |
| QuantumHavoraNorthHouse1 | Havora_NorthHouse_1 |
| QuantumHavoraNorthHouse2 | Havora_NorthHouse_2 |
| QuantumHavoraNorthHouse3 | Havora_NorthHouse_3 |
| QuantumHavoraCliffHouse1 | Havora_CliffHouse_1 |
| QuantumHavoraCliffHouse2 | Havora_CliffHouse_2 |
| QuantumHavoraCliffHouse3 | Havora_CliffHouse_3 |
| QuantumHavoraCliffHouse4 | Havora_CliffHouse_4 |
| QuantumHavoraCliffHouse5 | Havora_CliffHouse_5 |
| QuantumHavoraHarborInn | Havora_HarborInn |
| QuantumHavoraNorthHouse4 | Havora_NorthHouse_4 |
| QuantumHavoraNorthHouse5 | Havora_NorthHouse_5 |
| QuantumHavoraNorthLodge | Havora_NorthLodge |
| HavoraCoastalCliffs | Havora_CoastalCliffs |

## Validation

- ROM build passes.
- `tests/vidra_map_organization.py` validates all 50 renamed maps, every
  registered warp/connection/layout, unchanged map binaries and event positions.
- `tests/vidra_map_migration_emulator.py` exercises all 50 legacy map IDs,
  five saved warp fields, unchanged coordinates, repeat-call safety and
  unmodified Kanto destinations; all five settlements render in mGBA.
- Older Havora layout/market/civic checks still assume earlier map dimensions
  and in-bounds NPC placement. They report existing geometry discrepancies,
  including the Lookout fisher at y=-7. This organization pass preserves those
  authored coordinates rather than moving NPCs or redrawing maps.
