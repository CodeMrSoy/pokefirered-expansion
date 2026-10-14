# PokéGlass Pokédex

The PokéGlass Pokédex now runs as a field overlay using the same opaque shell,
glass window, and palette restoration as the hub, Stats, and Wardrobe. Party
uses the corresponding shared shell tiles. Catch-registration screens remain
on the existing battle/Pokédex registration path.

The app lists encountered Pokémon in National Dex order, including all
supported generations. Caught Pokémon are marked in the list. START switches
between seen and caught entries; SELECT switches between number and name
order. Up/down selects an entry; left/right or L/R moves by a page. A opens an
entry, and B returns to the list or closes the app to the hub.

Entry pages show a portrait and national number. Caught entries also show
category, types, metric height/weight, and wrapped description text. Seen-only
entries keep these details locked. A cycles description pages, SELECT plays the
cry, and R shows habitat locations. Habitat locations come from actual wild
encounter tables, across configured seasons/times, and deduplicate map sections.
No wild listing is represented as no recorded wild habitat, rather than as an
unobtainable Pokémon. L/R pages through habitat locations; B returns to the entry.

New games and Oak's Pokédex handoff enable FireRed's actual National Dex flag,
magic value, and variable. Opening this app upgrades old saves. This never
sets seen/caught records or story completion flags. The obsolete Emerald
National Dex initializer was replaced with the FireRed initializer.

The app allocates its list and text state only while open and reuses its
portrait buffer while browsing. Closing releases its allocation and portrait
palette, then restores the field window and blending registers.

`tests/pokeglass_pokedex_emulator.py` checks empty filters, numeric/name order,
seen-only detail locks, habitats, cries, page navigation, species beyond Kanto
through Gen 9, exact shell pixels, repeated cleanup, and flash save/Continue.
The shared shell regression also checks Party and Stats return behavior.
