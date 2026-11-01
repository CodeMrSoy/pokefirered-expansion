# PokéGlass reading screens (2026-11-01)

Pokédex, Stats, Storage, Field Kit/native Field Item Case and PokéGlass Town Map
omit navigation instruction text. Ownership, badge locks, inventory errors,
release confirmation and page/count indicators remain.

## Pokédex

Up/down scrolls the list. Left selects Seen; right selects Caught. A opens info
page 1, then toggles between info and habitat page 2. B returns from either to
the list. The optional SELECT sort, shoulder list paging and page-1 cry remain.
Habitat lists scroll with up/down when they exceed eight locations.

The list names the selected species' seed-assigned ability. Info includes its
description and the original Summary type badge bitmap/palette. Seen entries
can show these fields; caught entries also show category and measurements.
Badges occupy temporary windows after the tablet's 600 tiles and are removed
on page changes. They do not recolor the glass palette.
Transparent padding/corners are filled with the glass background, using native
type palette entry 10 (unused by every badge). This prevents unfiltered field
lighting from showing around the edges without changing badge artwork colors.

Each habitat slot is resolved through the actual RandomizeWildEncounter API,
including map number/group, encounter method and slot. All authored seasons
and times are considered. The job is bounded to 32 slots and 96 scanlines per
callback, with a VBlank boundary guard. It skips duplicate encounter tables and
map sections already found, pauses on the list, and resumes for the same
species. Looking up habitats cannot block an entire info-page opening.

## Stats and maps

Stats is one page: values, individual EVs/IVs, both totals, nature-effect colors,
and the actual Pokémon's ability name/description. The old profile/training
pages and nature text are removed. Member cycling, Egg privacy and saved
Pokémon data are preserved.

Kanto's original 320 atlas tiles are unchanged. Vidra uses the same palette,
striped ocean, city markers, stepped contours and broad gold routes. The atlas
uses 502 of 512 tiles. Section IDs, city/route coordinates and campaign metadata
remain unchanged. The generator preserves UTF-8 names and needs Pillow/NumPy.

Vidra's region picker is unavailable before FLAG_QUANTUM_ARRIVED, except when a
legacy save is already physically in Vidra. Town Map and Fly both use the gate;
old Sevii flags cannot bypass it. This changes visibility, not travel unlocks.

## Verification

The release ARM incremental build passes with EWRAM unchanged at 238,828 bytes
and IWRAM unchanged at 27,573 bytes. The native-call test helper now preserves
r3 when calling four-argument functions, matching the ARM ABI.

Targeted mGBA suites cover seeded habitat/ability comparisons, native badges,
new navigation, one-page Stats, text/border clearance, arrival locks, real map
switches, PC operations, launcher/save, all app handoffs and repeated cleanup.
The seeded fixture uses two seeds and all four encounter methods with authored
tables in this ROM (land, water, rocks and fishing); there are no authored
hidden-encounter tables to exercise. Production scanning includes that method.
Final executed results and previews are recorded in the workspace artifact
folder `qol-pokeglass-preview/reader-cleanup/`. Physical hardware and live link
play are not tested.
