# PokéGlass Pokédex

The PokéGlass Pokédex now runs as a field overlay using the same opaque shell,
glass window, and palette restoration as the hub and Stats. Party
uses the corresponding shared shell tiles. Catch-registration screens remain
on the existing battle/Pokédex registration path.

The app lists encountered Pokémon in National Dex order, including all
supported generations. Caught Pokémon are marked in the list. Left selects
Seen and right selects Caught; up/down scrolls one entry at a time. SELECT
switches between number and name order, and shoulder L/R retains list paging.
A opens an entry; repeated A presses toggle info page 1 and habitat page 2.
B returns from either page to the list, then closes the app to the hub.
Navigation instructions are omitted from the screen.

Info page 1 shows a portrait, national number, the Summary screen's native
type badges and the species' assigned ability with its description. The list
also names the selected species' ability. Ability assignments use the same
seed-aware getter as Pokémon creation; caught records additionally reveal
category and metric measurements. SELECT still plays the cry on page 1.

Habitat page 2 lists eight locations at a time; up/down scrolls additional
habitat pages. Locations come from actual wild encounter tables across
configured seasons/times, with each slot resolved through RandomizeWildEncounter
using its map, encounter method and slot. This lists the current seed's actual
wild locations, rather than the species' original locations or merely possible
randomizer candidates. Map sections are deduplicated. No listing means no
recorded wild habitat; gifts/evolutions/trades are not labeled unobtainable.
The scan runs in bounded background steps, skips duplicate time tables and
already-known map sections, and caches results for the selected species.
Info opens immediately; a habitat search status disappears when scanning is
complete. Short A/B presses remain available during the search.

New games and Oak's Pokédex handoff enable FireRed's actual National Dex flag,
magic value, and variable. Opening this app upgrades old saves. This never
sets seen/caught records or story completion flags. The obsolete Emerald
National Dex initializer was replaced with the FireRed initializer.

The app allocates its list and text state only while open and reuses its
portrait buffer while browsing. Native type badges use two small temporary
windows and the original Summary palette, preserving the glass palette.
Changing pages removes these windows. Closing releases its allocation and
portrait palette, then restores the field window and blending registers.
Badge padding and transparent corner pixels use a glass-colored backing rather
than BG transparency, so they cannot expose raw overworld lighting. An unused
palette entry supplies this backing; all badge artwork colors are preserved.

`tests/pokeglass_pokedex_emulator.py` checks empty filters, numeric/name order,
seen-only measurements, A-toggled info/habitat pages, cries, navigation, species beyond Kanto
through Gen 9, exact shell pixels, repeated cleanup, and flash save/Continue.
The shared shell regression also checks Party and Stats return behavior.
`tests/pokeglass_randomized_habitat_emulator.py` compares real seeded encounter
results with the habitat list, assigned-ability foreground glyphs against an
independent native-font reference, native type palettes and map arrival locks.

Flavor descriptions have been removed from the species tables and shared text
data. Their pointers all reference one valid empty string so existing capture
registration and species-description readers remain safe. Names, statistics,
category, types, measurements, graphics, and encounter data are unchanged.
