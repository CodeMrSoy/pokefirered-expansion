# PokéGlass Oak progression fix — 2026-10-28

The previously delivered ROM allowed Start to open PokéGlass on a fresh game without the device. Its Party and Pokédex scripts then returned to the launcher because the player had no Pokémon and had not received the Pokédex. This was reproduced against the delivered ROM. Earlier app tests supplied Pokémon, the device and/or the Pokédex flag up front, so they did not cover this story boundary.

PokéGlass now requires both Oak's Pokédex milestone and possession of the device. Start, Bag/registered-item use and scripted entry enforce the gate. Denied Start input leaves no menu, intro, or field-control lock. The existing Oak parcel handoff grants the device and milestone normally; no new save flags or save layout are required. Party/Stats tiles require an actual party, and the Pokédex tile requires its obtained flag, instead of offering apps whose scripts immediately reject entry.

`tests/pokeglass_oak_progression_emulator.py` covers a fresh game, an early device without Oak's milestone, the milestone without the device, registered/scripted entry and a starter before the parcel. It then talks to the actual Oak object and completes the full parcel/Pokédex/PokéGlass/five-Ultra-Ball dialogue with ordinary button input. With that real earned state, it opens the Pokédex list and Bulbasaur entry, the one-starter Party and its action menu, returns to the field, writes a flash save and reboots before exercising both apps again. App-only fixtures explicitly mark their post-Oak prerequisite.

The standard ROM build and the existing PokéGlass app benchmark, Pokédex filtering/entries/habitats/save checks, Party text/candy flow, Stats checks, native PC/Town Map, twelve Party returns and eight memory-cleanup sessions pass. The Vidra boat/artwork/disembark sequence remains covered by its existing regression with a post-Oak one-starter fixture.

The current V2 household commit also removed `Havora_TraderHouse_Owner`, while five connected house maps still reference it. A compatibility label now aliases the existing merchant dialogue so the latest branch links successfully. No household layouts or gym assets were changed.
