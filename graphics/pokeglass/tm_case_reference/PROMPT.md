# TM Case artwork provenance

Tool: built-in `image_gen.imagegen`; transparent background requested.
The user's screenshot was supplied as a design reference. This is a new asset,
not a pixel-exact extraction. The full-size output is saved in the workspace at
`qol-pokeglass-preview/reference-case-art/source.png`.

The game's source is `case-native.png` (44 by 43, indexed palette with transparent
index zero and fifteen opaque colors). Native export uses nearest-neighbor
scaling and no dithering. `tools/compile_pokeglass_tm_cards.py` encodes the PNG
and animation tiles into the generated C header. The original screenshot and
legacy TM Case artwork are unchanged.

## Exact prompt

Use case: background-extraction / game sprite asset. The input image is a design REFERENCE. Create ONLY the open gold-and-blue SD card storage case seen on the left of this reference, as a standalone transparent-background pixel-art sprite for a Pokemon GBA game. Preserve the reference case design closely: open upright hinged gold lid with a broad blue center stripe and small red-white Pokeball emblem; gold bottom shell with a blue stripe and silver latch on the front; dark charcoal foam insert with small colorful SD cards in neat rows; three-quarter view showing top, front and right side, bright upper-left highlights and darker sides. IMPORTANT remove the one tall raised red card in the central slot: leave that central slot empty, so the game can animate a separate selected card rising out. Keep all the other small stored cards. Crisp hand-placed retro pixel-art shapes, dark one-pixel outlines, limited saturated 15-color-like palette, visible substantial 3D depth like the reference. No soft paint, no photorealism, no text, no UI, no tablet, no background, no ground shadow outside the sprite. Entire case visible centered and tightly framed with a small transparent margin. This will be reduced to approximately 56 by 56 game pixels; simplify tiny details to remain readable. Produce one case only, not a sprite sheet.
