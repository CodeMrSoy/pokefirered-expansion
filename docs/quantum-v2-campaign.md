# Quantum V2 campaign scope

The campaign retains Kanto, the first Elite Four and Champion battles, the Hall
of Fame, credits, Continue, and ordinary exploration of the retained world.
The Bill/Lostelle trip to Islands 1–3, Berry Forest, and Mt. Ember/Moltres remain.
Quantum's existing National PokéGlass support remains available from new game;
Oak's separate post-League National Dex ceremony is removed.

Removed playable content:

- Islands 4–7, including Icefall Cave, Rocket Warehouse, Dotted Hole, Lost Cave,
  Pattern Bush, Altering Cave, Trainer Tower, and the Tanoby chambers.
- Celio's Ruby/Sapphire quest, Rainbow Pass travel, and the Ruby Path under
  Mt. Ember. The Ruby cave entrance stays sealed.
- Cerulean Cave/Mewtwo and the Navel Rock/Birth Island event destinations.
- The dug-out Dunsparce tunnel expansion and roaming-beast unlock.
- Upgraded Elite Four/Champion teams and their rematch introductions.
- The automatic post-League Oak scene and postgame gossipers.

`quantum-retired-maps.json` lists 127 retired map slots and 119 exclusive layout
slots. Their scripts, text, objects, items, encounters, connections, and original
layout binaries are deleted. Inert map headers and tiny layout entries retain
the original numeric IDs; shared layouts are preserved. Engine ABI labels and
event-ID constants remain inert where shared C code still references them.
Shared graphics, Pokémon data, battle systems, and other reusable engine code
remain. V1 on GitHub preserves the original content.

Incoming warp indices in retained maps remain stable. Late ferry and Fly
destinations are unavailable, and the warp loader redirects retired destinations
to Pallet Town. Retired healing slots also resolve to Pallet Town. Continue
relocates a V1 save from a retired map through a fresh map load, repairs stored
return/escape/healing warps, clears late unlocks and map visibility, and disables
roamers. It preserves name, gender, party, bag, and the selected character look.
Oak's starter scene values 0/1 are preserved.

## Verification

The ARM build uses 23,807,428 bytes of the 32 MiB ROM, down 194,128 bytes
(about 190 KiB) from the V1 Wardrobe build. Approximately 9.3 MiB remains.
The physical `.gba` is padded to 32 MiB; the linker reports actual used space.

`tests/quantum_campaign_emulator.py` checks retired and retained map boundaries,
early starter state, save migration through reset/Continue, movement, identity,
party and character-look preservation, end-of-League flags, Hall of Fame, and
credits. The retained encounter records, map-group IDs, early-island maps,
and ending maps were compared with V1. Existing QOL, PokéGlass shell, and
Stats regression checks are also used. No full campaign playthrough was run.
