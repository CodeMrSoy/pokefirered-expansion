# Quantum character looks and Wardrobe

Six looks are available during character creation and in the PokéGlass Wardrobe:
Red, Leaf, Emerald Brendan, Emerald May, Ruby/Sapphire Brendan, and Ruby/Sapphire
May. Left/right previews a look. A wears it; B cancels. Appearance does not
change the player's name, gender, Pokémon OT data, or story flags.

`VAR_PLAYER_AVATAR` uses the previously unused permanent variable `0x40FD`.
Zero and invalid values retain the original gender-based appearance for older
saves. Values 1–6 encode the selected look. Character creation chooses a default
after gender selection; `NewGameInitData` preserves the look across clearing
SaveBlock1. The save structures and sector layout are unchanged.

Hoenn looks use separate object graphics IDs 157–184 and palette/reflection tags
0x11E0–0x11E7. They include walking, running, bike, surf, fishing, field-move,
and Vs. Seeker states. FRLG animation tables address adapted frame lists;
Vs. Seeker uses the character's field-move poses and bicycle idle poses.
Other player lookups remain separate from link guests and NPC graphics.
The selected appearance supplies naming icons, creation portraits, battle front
and back portraits, Trainer Cards, Pokédex size comparisons, Hall of Fame,
VS transitions, and map icons. Hoenn Fly passengers use the real avatar sprite
above the unoccupied bird graphic, avoiding baked-in Red/Leaf passengers.

## Asset sources and credits

The character art is native Pokémon Ruby/Sapphire/Emerald art preserved by the
pret decompilation projects and RHH contributors. Retain their existing credits.
Source PNGs were copied without visual modification; the Ruby overworld and
map palettes were extracted from their indexed PNG palettes.

- Emerald walking/running/activity sheets, portraits, and map icons:
  [mudskipper13/pokeemerald, feature/outfits-system-rhh](https://github.com/mudskipper13/pokeemerald/tree/feature/outfits-system-rhh),
  commit `fb560657d555070c0291ab433f46e0cd82c16c60`.
- Complete Ruby/Sapphire activity sheets:
  [pret/pokeruby](https://github.com/pret/pokeruby),
  commit `5784633ce4ef7ade1a7f2d2d0c288e3d5e6cdd7f`.
- Existing Red/Leaf and Ruby/Sapphire trainer portraits are from this FireRed base.
- Mudskipper13's Outfit System and Slawter666's original Costume System informed
  the saved-look/menu approach; Quantum uses its own small FireRed implementation.

## Verification

The ARM ROM build passes. `tests/avatar_wardrobe_emulator.py` checks all six
creation and Wardrobe previews, cancellation, applying a look, preservation of
name/gender, movement graphics, actual battle back portraits, map artwork,
Fly landing, and a real flash save followed by reset and Continue. Existing
QOL, Stats, and shared-shell emulator regressions pass. Native screenshots of
creation, Wardrobe, movement, battle portraits, and reload were inspected.

The new creation step adds one A press to the standard emulator bootstrap.
This is a cosmetic feature; no full-game playthrough was performed.
