# V2 arrival integration — 2026-10-27

Merged QOL `906b6ec003929807af461f1bbfa20f2d2b227726` into V2, starting from `1867c902d29091a0bc4435598c83d07681c611d9`. Verified that the current Havora-Development head `8364d56bed45e619510929a2e41ebf1b51b3fca7` is already an ancestor of V2. All three remote heads were checked again before publication. The gym code, compiled geometry, map/event data and gym artwork remain byte-for-byte identical to Havora-Development.

The standard ROM compiled with `make -j8` using arm-none-eabi-gcc 13.2.1. Its size is 33,554,432 bytes and SHA-256 is:

`84d4c3cadf7f133252a1d160f7f1da59f8f96e2cb74095a29a7c63e43e074e18`

Passed:

- The actual Vermilion sailor and Stellar Ticket route: sailing, full-screen Vidra image, warp to Havora Harbor, three automatic steps from (20,17) to (20,20), controls locked until finished.
- Collision checks on all four landing tiles and ordinary player movement down to (20,22), off the pier.
- Return voyage to Vermilion, missing-ticket rejection and wrong-departure rejection; none show the arrival artwork.
- Artwork preview pixels, first-second input guard, deliberate skip, automatic continuation and same-field return.
- New PokéGlass startup/Bag artwork and every standard PokéGlass app opening/closing.
- All five independent Vidra Center unlocks and native Sky Whistle flights, Kanto return and Town Map switching.
- All 50 renamed map layouts, map groups, connections and warps retain valid references and original geometry/events.
- Native Trainer Card Kanto/Vidra/statistics pages, crest rewards and resource cleanup.
- All 27 Python-generated gym water combinations and unchanged puzzle control logic.

The old 25-action gym progression test is explicitly retired/skipped by its own harness. The strict gym emulator reference comparison fails on both this ROM and the pre-merge V2 ROM at the same tile (row 3, x=1; runtime `0x4703`, reference `0x4700`, levels `(0,0,1)`). This is an existing editor/runtime reference discrepancy, not a new merge failure. See `known-issues.md`; the gym assets were preserved rather than changing approved map artwork to satisfy an older reference.
