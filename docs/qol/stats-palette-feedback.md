# Stats and PokeGlass palette fixes

The PokeGlass Stats app lists the ability name and its in-game description below the stat table. The control hint is removed; Left/Right and B keep their existing behavior. Stat category labels are red for the effective nature’s raised stat and blue for its lowered stat. Neutral natures and eggs have no nature coloring. Stat/EV/IV values and save data are unchanged.

The live field overlay now uses menu BG palette 13, preserving map palettes 0–12. The native Party screen keeps its original palette 11 because it replaces the field and reserves palette 13 for native menu borders. Both normal and faded overlay palettes are restored on exit.

The main 64px Power Gloves picture moves the left hand two pixels left to align it with its cuff. Its original indexed palette, transparency and smaller Bag icon remain intact.

Validation: development ROM compiled; mGBA Stats test checks controlled Brave/Timid/neutral/egg fixtures, red/blue label pixels, unchanged field palettes, party navigation, portrait resource cleanup and unchanged party data. Six-app grid and native Map/PC deposit/withdrawal tests pass. Empty Field Item Case test also passes. Screenshots are actual ROM output except the separately enlarged glove sprite.
