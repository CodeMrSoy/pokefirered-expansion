# Quantum character looks and Wardrobe

Four looks are available during character creation and in the PokéGlass Wardrobe:
Red, Leaf, Emerald Brendan, and Emerald May. Left/right previews a look. A wears it; B cancels. Appearance does not
change the player's name, gender, Pokémon OT data, or story flags.

`VAR_PLAYER_AVATAR` uses the previously unused permanent variable `0x40FD`.
Zero and invalid values retain the original gender-based appearance for older
saves. Values 1–4 encode the selected look. Legacy values 5 and 6 migrate to Emerald
Brendan and May respectively. Character creation chooses a default
after gender selection; `NewGameInitData` preserves the look across clearing
SaveBlock1. The save structures and sector layout are unchanged.

Emerald looks use object graphics IDs 157–170 and their palette/reflection tags.
Legacy Ruby/Sapphire graphics IDs 171–184 now alias the matching Emerald sprites. They include walking, running, bike, surf, fishing, field-move,
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

The ARM ROM build passes. `tests/avatar_wardrobe_emulator.py` checks all four
creation and Wardrobe previews, cancellation, applying a look, preservation of
name/gender, movement graphics, actual battle back portraits, map artwork,
Fly landing, and a real flash save followed by reset and Continue. Existing
QOL, Stats, and shared-shell emulator regressions pass. Native screenshots of
creation, Wardrobe, movement, battle portraits, and reload were inspected.

The new creation step adds one A press to the standard emulator bootstrap.
This is a cosmetic feature; no full-game playthrough was performed.

## Custom playable avatars

Cody, Ben and Brandon are available in character creation and Wardrobe.
Saved look values 7, 8 and 9 identify them; legacy values 5/6 continue to
migrate to the Emerald looks. Name, gender and OT identity are independent.

Ben and Brandon use the corrected approved artwork in
`graphics/avatars/{ben,brandon}/source/approved.png`. Both have neutral black
hair. Ben's trainer stance is narrower, and rear-facing Poké Balls hide the
front button. Additional activity and rear throw poses are generated FireRed
template adaptations in `source/poses.png`. Run
`python3 tools/import_quantum_avatar_art.py` to regenerate native indexed
sprites, palettes, trainer portraits and map icons. Native overworld frame
order is down/up/left idle, down steps, up steps, left steps. Right-facing
frames use the existing engine mirroring. Index zero is transparent; assets
use at most 15 visible colors. The artwork still benefits from a longer
in-game visual playtest, especially fishing and throwing motion.

After importing the source art, run `python3 tools/polish_quantum_avatars.py`
for the revised FireRed-scale walking art, aligned action silhouettes, trainer
and trainer ground shadows. Cody retains his original trainer artwork and palette. This command
reruns the importer before applying the corrections so exports are repeatable.
The revised walking silhouettes use Red's 19-pixel visible height and baseline.
