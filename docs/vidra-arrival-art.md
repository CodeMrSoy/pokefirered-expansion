# Vidra arrival and PokéGlass artwork

Uses the supplied Vidra Region illustration at 240×160 with a 256-color GBA background palette. The entire 3:2 composition is retained, including its title. A valid, ticketed Vermilion-to-Vidra voyage plays the existing sailing scene, fades to the illustration, then loads Havora Harbor and automatically walks the player three tiles down the ferry pier (20,17 to 20,20). Controls remain locked until disembarking finishes. Return voyages and rejected/ordinary ferry destinations skip the illustration.

The illustration holds for three seconds after fading in, then continues automatically. A new A/B press after its first second continues sooner. A held boarding button cannot immediately dismiss it. No new save flags or persistent save data are required.

QOL alone does not contain the Havora harbor maps or its Stellar Ticket sailing route. After merging QOL into V2, `MAP_HAVORA_HARBOR` enables the arrival hook and the sequence is active on the actual harbor map. The `ShowVidraArrivalArt` script special also provides a standalone preview and returns to the same field. V2's release checks cover the real Vermilion sailor, full sailing/artwork/disembarking sequence, walking off the pier and return voyage. Havora-Development's latest commit is included in V2; the merge preserves its gym files.

The supplied PokéGlass device artwork replaces both the Bag's 24×24 item icon and the 64×64 startup sprite. Both use 16-color palettes with transparent index zero. Startup lights the blue glass using matching generated palettes; the launcher shell and apps retain their current design.

To reimport the supplied originals:

```sh
python3 tools/import_quantum_art.py /path/to/vidra.png /path/to/tablet.png
make -j8
```

The converted PNGs and palettes are source assets; the normal build generates the native tile/palette files. Test with `tests/vidra_arrival_art_emulator.py` using the same mGBA/ARM toolchain environment as the other emulator tests. It checks native artwork pixels, automatic/early-input/skip behavior, field restoration, new startup and Bag artwork, and (when Vidra maps exist) the real sailor route, walking coordinates/control lock and return voyage. The existing complete PokéGlass transition benchmark also passes after the artwork change.
