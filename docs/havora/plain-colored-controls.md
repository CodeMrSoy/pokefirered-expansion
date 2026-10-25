# Plain colored puzzle controls

Buttons A/B/C/D now have solid red/blue/yellow/green faces without the previous added circle, diamond or triangle markers. Gate A has red painted log tips, gate B blue tips, and the shared forest gate blue/yellow/green bands matching its B/C/D requirements. There are still three gates: the existing puzzle logic, six stones, pits, Cut trees, coordinates, heights and 37-action solution are unchanged.

All pressure button metatiles and the resting gate-cap metatile use the covered/ground layer type. Boulders draw over the buttons. Retracted gates show only their end-grain caps flush in the grass, beneath actors; their temporary animation sprites are destroyed when the animation finishes. Moving gates remain blocked in both directions.

Four pairs of button metatile IDs: 0x233/234, 0x235/236, 0x237/238, 0x23C/23D. Closed gates keep 0x239–23B and the shared open cap remains 0x232. This uses seven formerly blank graphics 1017–1023, the existing palette 12, and no extra graphics beyond the tileset limit. Water animation tiles 896–1015 are untouched. Only D’s existing map cell changes ID; all terrain and map connections stay intact.

Validation: development ROM compiled; preservation validator passes, including all cliff art, terrain/collision, original palette files, dimensions and nursery warps. The independent solver and mGBA full puzzle route pass. Emulator checks actual BG buffers to verify ground controls leave the actor-covering layer empty, plus opening/closing frames, palette exhaustion fallback, occupied-gate guard, task/sprite cleanup, reset and reload.

`review/plain-colored-controls.png` is a native metatile rendering. `gate-animation.gif` and the emulator captures are actual ROM output, not Porymap screenshots.
