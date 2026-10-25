# Region map and Sky Whistle review

Vidra is the island; Havora City is its southeast port city. The other four
settlements retain their existing descriptive names because the later naming
conversation was not recovered.

QOL's shared native map now contains no selectable Sevii page data or graphics.
Legacy map flags cannot restore them. The campaign-enabled picker has exactly
Kanto and Vidra; its two UI rows translate to the existing region page IDs 0/2.
QOL remains Kanto-only until combined with V2's island campaign section IDs.

Vidra uses the original FireRed map palette, ocean pattern, city tile and
controls. Its five city positions, route sections, healing destinations and
visit flags retain their IDs. The atlas stays within the existing 16-KiB BG0
allocation, and no additional palette or persistent RAM allocation is needed.

Sky Whistle displays all city/Center destinations. Available destinations use
the native animated Fly marker, and unavailable destinations use a steady grey
marker. Each Vidra Center still unlocks only its own city after legitimate
arrival; showing or switching maps cannot unlock travel. Canceling the region
picker now restores the selected region's markers even when the player is in
the other region. Empty marker slots are checked before visibility changes,
and marker tile/palette tags are retained for resource cleanup.

## Verification

Both QOL and a detached V2 integration build compiled successfully. No remote
branch was changed by this review.

- `tests/region_map_destinations_emulator.py`: QOL case-to-whistle entry, all 13
  Kanto town/Center markers, legacy Sevii flags and cancel cleanup. V2 additionally
  checks five locked markers, independent real Center unlocks, one/all available
  markers, all five completed flights, return to Kanto, two-region picker,
  canceled switching from another region, plain Town Map and resource cleanup.
- `tests/pokeglass_native_apps_emulator.py`: native Town Map and PC regression.
- `tests/field_tools_emulator.py`: all seven tools, old-HM migration, actual
  interactions, completed Sky Whistle flight, Bag/registration and save/Continue.
- `tests/rom_cleanup_maps_emulator.py`: retired stairs, Route 20 and replacement
  encounter map screens.
- Repeated map generation gives identical assets. The first 10,240 atlas bytes
  exactly match FireRed's original map tiles; the full atlas is 16,320 bytes.
- `git diff --check` passes.

Actual native ROM captures are saved as Quantum_Kanto_Vidra_Map_Review.png.

## Border and header follow-up

Fly now uses the same native map opening/closing path and persistent decorative
frame as Town Map. Vidra's generator preserves the transparent outer margins
and original top two rows, allowing the shared frame and continuous blue header
to show through. The entire map viewport is replaced with Vidra/ocean pixels;
no Kanto terrain fringe is retained. The art atlas and its VRAM budget are unchanged.

The destination emulator regression compares rendered blue-header and left/right
border pixels directly with the real Town Map. It repeats those comparisons
while switching regions, canceling, opening in either region and using Town Map,
and checks frame-resource cleanup after completed flights.
