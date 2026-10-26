# Captain's Trial approved art pass

Direction chosen with the user: covered shipyard, rustic Nordic port, and a working captain's deck rather than a painted battle court.

The revised private gym kit uses broader S.S. Anne wooden planks, complete desks and storage cases, paired chart pieces, existing dock waterlines, stone quay facings, and two complete Slateport hoists. Timber columns and rafters are assembled from the native post art. Colored controls sit on native riveted machinery plates. Private walnut/stone palette adjustments keep the water colors and every outdoor palette unchanged. No image generation or replacement city artwork is used.

The captain's desk is a full native two-row kit. Incomplete furniture fragments have been replaced by complete arrangements. The original NPCs, sign coordinates, entrance/exit warps, boarding points, save variables, trainer teams and puzzle rules remain intact. Some furnishings change local walking space; the independently checked puzzle state graph still has 48 reachable states, and all have a return/reset route.

The native tile/NPC preview is docs/havora/review/captains-trial.png. Emulator verification covers low/high boat rides, lock transfer, progress gates, state reload, reset, the real winch interaction, exterior exit and all three native double battle launches. Outdoor preservation checks pass. The development ROM compiles with unchanged static EWRAM allocation. No Porymap UI testing is claimed.

The user approved this art pass for Havora-Development, together with the new Vidra crest page. V2 integration is a separate step.

## Readability pass

The next pass adds small custom 16x16 pixel assets within the existing private
GBA tileset: framed timber, clean beams, a red wheel winch, blue/yellow levers,
a green reset bell, boarding arrows, rope coils and a LOW/HIGH lock gauge.
The gauge updates from the existing HIGH state and is restored on map load.
All four boarding pads remain passable at elevation 3. Boat pixels are drawn
after the pads. No trainer, switch, boarding event or warp was moved.

Custom assets use eight previously unused indices of private palette 2, plus
its existing wood shades. Native graphics using other indices are preserved.
No animated-water or fountain graphic slot is overwritten. No city asset is
modified. The clean preview uses exact 2x nearest-neighbor scaling.

Design references reviewed:

- Pastoria Gym (Platinum): water levels and floating access. Here this informs
  the visible level gauge and separate upper/lower boarding markers.
  https://bulbapedia.bulbagarden.net/wiki/Pastoria_Gym
- Sootopolis Gym (Emerald): distinct puzzle stages leading upward. Here the
  captain deck, upper berth and lower dock have distinct physical boundaries.
  https://bulbapedia.bulbagarden.net/wiki/Sootopolis_Gym
- Vermilion Gym (FireRed): visible barriers controlled by switches. Controls
  here are explicit machinery rather than hidden switches.
  https://bulbapedia.bulbagarden.net/wiki/Vermilion_Gym

These are design interpretations, not copied layouts or Platinum graphics.
Puzzle difficulty is unchanged in this art pass.

Verification for this pass: development ROM compiled (21,621,252 bytes used;
static EWRAM 258,376 bytes, unchanged). The 48-state preservation/route audit
passes. mGBA checks pass for the LOW/HIGH gauge, boat rides, lock, progress
requirements, re-entry, reset, exterior exit and all three double-battle launches.
The east-lock emulator screenshot was visually inspected. No Porymap UI test or
complete combat playthrough is claimed.
