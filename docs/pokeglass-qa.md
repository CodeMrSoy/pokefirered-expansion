# PokéGlass performance and UI QA

## Transition follow-up (2026-11-01)

The tablet icon now rises over 12 frames, lights over eight, and pauses lit for
ten. The emulator observes 32 frames of icon animation (about 0.54 seconds).
The complete Start-to-launcher transition is 77 frames / 1.289 seconds, compared
with 55 frames / 0.921 seconds before this follow-up.

Native Map, Bag, Trainer Card, Options and TM Case handoffs keep partial graphics
uploads and field reconstruction hidden behind black until their destination
has finished drawing and DMA has drained. They retain their native fades.
Bag/TM frame palettes load before the fade begins, avoiding a partially lit
frame or temporary black labels. Embedded Pokédex, Party, Storage, Stats and
Field Kit retain their uninterrupted tablet bezel and have no blank frames.

The map's native name/dungeon boxes reuse WIN1, which also clips the tablet
viewport. Normal Town Map rendering now reapplies the tablet window and removes
native name-box darkening after these updates. Region pickers and dungeon
previews retain their own window effects while active. First-open map rendering,
cursor movement, Kanto/Vidra round trips and repeated reopenings now use the same
viewport. The returned Kanto tilemap and atlas graphics match the initial ones.

`pokeglass_benchmark_emulator.py` captures every standard app's entry/return and
checks embedded bezel stability, blank frames and native overworld flashes.
`pokeglass_map_transition_emulator.py` checks the actual icon duration, affine
matrix cleanup, map windows, real region switches and three reopenings. Both
passed against the release ROM. Final frame captures and timings are in the
workspace's `qol-pokeglass-preview/transitions-final/`; the baseline is retained
in `transitions-before/`. Native fades still include black frames by design.
EWRAM remains 238,828 bytes and IWRAM remains 27,573 bytes. Physical hardware and
live multiplayer were not tested. Earlier timings below describe the previous
optimization pass.

The same ROM also passed launcher/save, native Town Map/PC operations, glass Bag
pockets/actions, TM app teaching/consumption/Continue, Field Kit discovery,
eight repeated resource-cleanup sessions, and twelve frame-by-frame Party
returns across bedroom, Viridian and Cerulean fixtures. These nine suites are
recorded under the workspace result groups `emulator-transition-final`,
`emulator-map-transitions` and `emulator-transition-resources`.

Measured in mGBA/libretro at 59.7275 emulated frames per second. Timings run from button input until the destination accepts input, including its animation/fade and a three-frame readiness guard. They are game-frame measurements, not a benchmark of the host computer or physical hardware. The baseline is V2 `de8c441c` before this change. QOL and V2 standard builds produced matching final transition timings in the test bedroom.

## Transition times

| Screen | Open | Return to launcher |
| --- | ---: | ---: |
| Pokédex | 0.335s | 0.301s |
| Party | 0.820s | 0.720s |
| Storage / PC menu | 0.201s | 0.201s |
| Stats | 0.301s | 0.301s |
| Town Map | 0.921s | 1.205s |
| Bag | 0.670s | 1.189s |
| Trainer Card | 1.239s | 1.105s |
| Options | 0.954s | 1.189s |
| Save confirmation | 0.804s | 0.184s |

Tablet opening improved from 2.093s to 0.954s; closing takes 0.100s. Party return improved from 1.875s to 0.720s. Town Map return improved from 3.097s to 1.205s. Bag return improved from 2.193s to 1.189s. A full 1,025-record Pokédex opens in about 0.32s; alphabetical sort and caught-filter rebuild each take 0.335s, down from 3.365s.

Trainer Card remains the slowest app opening (1.239s). Town Map, Bag, Trainer Card and Options keep their native full-screen fades. Those deliberate fades are included above. The embedded Party, Pokédex and Stats handoffs contain no entirely black frames and no changed bezel pixels in the frame-by-frame regression.

## Fixes

- Reuse the frozen field backdrop for the entire launcher visit; release it on exit and recapture after a map or player-position change.
- Expand packed backdrop rows in bulk, reuse the original shell as a pre-rendered asset, and compile a compact native-menu frame. The shell's palette-index pixels match the original rectangle drawing.
- Shorten tablet startup and omit the Town Map paper unfolding/folding animation when launched through PokéGlass.
- Build the national-dex species lookup once per visit and replace insertion sorting with `qsort`.
- Keep Party loading/return covered until its graphics are ready. Reserve separate VRAM map blocks, commit cover uploads in VBlank, and defer conflicting register/palette writes. This fixes the black flash and one-frame color tear.
- Fit Party nicknames into the space before the gender icon. Exceptionally wide names receive a display-only ellipsis; saved names are preserved.

## Verification

Standard QOL and V2 ROM builds passed. A V2 development build also passed the complete transition benchmark, including Debug (0.285s open / 0.184s close). Emulator checks covered every available standard app opening/closing, horizontal launcher paging, actual PC deposit/withdrawal and item management, Save cancel and flash write, field unlock/reopening, and the fixed outfit.

Party checks covered one/six members, four field locations, twelve actual Party returns, action menus, Summary, Stats, level 100, one/two/three-digit HP, healing/fainting, genuine Rare Candy level-up/stat popups, and twelve-wide-letter nicknames without overwriting the gender column. Pokédex checks covered empty/legacy records, generations 1–9, seen/caught filters, sorting, entry/habitat/cry, and save/reload. Full-Dex and Stats raster checks found zero text foreground pixels outside the glass. All 311 compiled ability names/descriptions fit their Stats columns. Existing nature colors, egg values, member cycling and portrait palette cleanup passed.

Eight repeated real launcher sessions retained no backdrop and returned to exactly the same allocated heap (11,520 bytes in five field allocations). Native Town Map/PC resource cleanup passed. V2 region-map regression also passed all five actual Vidra Center unlocks and Fly destinations, return to Kanto, and Town Map switching. Existing map/gym issues remain documented separately in `docs/vidra/known-issues.md` on V2.

## Reproduce

Build with `make -j8`, then run the relevant `tests/pokeglass_*_emulator.py` scripts with `MGBA_CORE` pointing at an mGBA libretro shared library and `ARM_NM` pointing at the matching ARM toolchain's `nm`. Run `tests/pokeglass_stats_text_layout.py` against the built ROM/ELF. The benchmark writes timings, screenshots, contact sheets and actual transition GIFs under `build/quantum-qol-tests/pokeglass-benchmark/`. These generated captures are excluded from source control.

`graphics/poke_glass_shell.png` is the indexed source art. Regenerate `src/data/poke_glass_frame.h` with `python3 tools/compile_pokeglass_frame.py` if the shell changes. The normal build generates the shell's `.4bpp` file.
