# Vidra regional map

The new island is a native GBA region-map page, available through PokéGlass Map
and the Fly map's region switch icon. The tablet preview switches between Kanto and Vidra with L/R; A
opens the native guide. The native picker retains its historical Sevii preview,
but retired destinations cannot be used for travel. Viewing a map does not
unlock travel.

The accepted concept becomes a 176×120-pixel map on the 22×15 cursor grid:

| Location | Grid position |
| --- | --- |
| Havora City | 15, 12 |
| Coastal City | 4, 10 |
| Forest Town | 6, 7 |
| Lake Town | 14, 7 |
| Snow Town | 10, 2 |
| Hot Springs | 13, 2 |

Eight named routes connect these locations: Coastal Road, Forest Path, Mountain
Pass, Snow Trail, Lake Road, Harbor Road, River Road, and Woodland Link. Names
are descriptive placeholders. Port City has a larger built-up market district,
piers and a small daycare garden in the regional artwork.

The island reuses the retired Sevii 4–5 region page, so the region-map structure
does not grow. Its atlas preserves all 320 original map tiles and adds 191 native
4bpp tiles including controls, remaining within BG0's 512-tile character bank.
The new palette uses BG palette bank 5. Existing section IDs, including
`MAPSEC_NONE`, retain their original values; new section IDs follow that sentinel.
The shared name lookup and current-location projection support the new IDs.

The Stellar Ticket quest adds a playable harbor, five starter town layouts,
four connecting route layouts, and individual Pokémon Centers. QOL seals the obsolete multiplayer
stairs; upstairs maps remain for compatibility with older V2 saves. The field layouts are travel foundations using existing native
Kanto tiles; the finished port market, daycare, snowy terrain, hot springs and
island story are future work. The regional artwork remains the accepted concept.

The Stellar Ticket is given by a traveler in the Safari Zone Secret House.
A guide blocks Fuchsia Gym while Koga is away and directs players to that house.
The traveler explains that Koga went to Vidra's Havora Market and offers an
extra ticket. Talking to Koga there sends him home and reopens his gym. The
Secret House attendant directs players to Eirik, whose Havora Gym victory now
awards the Wailmer Wailer. Koga's Soul Badge still authorizes Surf. The reusable
Key Item is required by the Vermilion ferry, and Havora's sailor returns the
player to Vermilion. See `docs/vidra/koga-market-encounter.md` for current details.

Giovanni's normal Earth Badge, TM26 and retirement sequence has been restored.
Saves from the former Vidra pursuit arc receive the withheld badge if Giovanni
was already defeated; previously obtained Stellar Tickets remain valid.

A legitimate ticketed voyage sets the arrival flag. Each town's Center entrance
then sets its own saved Fly flag and healing point; arrival or viewing the map
alone unlocks no town. Fly can subsequently cross between Kanto and visited
island towns. The Earth Badge guard opens after the ordinary Giovanni gym
victory; no additional Vidra confrontation is required.
New map and healing IDs are appended, preserving every existing V1 map ID and
retired-map save migration.

Run `python3 tools/quantum_region/generate.py` to regenerate the artwork,
binary atlas/tilemaps, controls, hit map, palette and matching location metadata.
`make` compresses the binary assets and converts the palette normally.

The combined build uses 23,823,688 bytes of ROM. Global EWRAM/IWRAM usage
is unchanged. `tests/quantum_stellar_emulator.py` exercises the gym quest,
full Key Item pocket recovery, restricted outbound voyage, return boat,
independent Center unlocks, exits and stairs, route crossings, cross-region Fly,
and reset/Continue persistence. The region-map and campaign tests cover map
navigation, retired-map migration and the existing ending.
