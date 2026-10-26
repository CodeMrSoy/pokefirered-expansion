# Havora overhead lock yard

Implemented against `e9c7434ec`, October 26, 2026. This supersedes the old
cross-section geometry described in `three-lock-prototype.md`.

## Spatial behavior

- The dedicated interior is 80×40. Its high decks and two galleries have fixed
  footprints; short south-facing retaining walls and ladders lead to low shelves.
- LOW/MID/HIGH covers those shelves in place. High decks stay anchored. The dry
  entrance corridor is independent of the tide, and submerged ladders are closed.
- Both boats have fixed plan coordinates at each berth. Water changes never
  move a berth eight map rows. Different water heights enable the appropriate
  gangway/landing instead.
- Boat travel searches the real map for clearance of the entire 3×3 hull.
  It avoids solid banks, islands, closed lock gates and the other moored boat.
  North/south/east/west travel rotates the boat; its passenger remains standing.
- The service cargo deck spans three water tiles plus a short gangway. At the
  final quay, the vessel bridges the three water cells to the captain island;
  the staging quays have a separate one-cell hinged connection. A small boat
  is no longer drawn as an unexplained eleven-cell vessel.
- The old abstract rules and 25-decision solution survive the spatial rebuild.
  The gallery gates are visible even when closed. All 837 reachable walking
  states and 570 legal boat trips were checked against the new footprints.

`tools/havora/overhead_lock_geometry.py` is the geometry authority. Imports are
read-only; the compatibility builder writes only the dedicated gym. Its compact
RLE overlays are shared with the native renderer, avoiding a second handwritten
copy of the geometry. Transfer stages update changed tiles, without translating
high decks or boats. Draws may span video frames in map RAM; only the completed
overlay is committed to the displayed map.

## Battles and progression

| Order | Crew | Party | Levels | Main lesson |
|---|---|---|---|---|
| 1 | Deckhand | Hariyama / Machamp | 47–48 | Fake Out and physical pressure |
| 2 | Navigator | Magnezone / Lanturn / Seismitoad | 48–49 | Partner-safe Discharge |
| 3 | Engineer | Skarmory / Rotom-Wash / Scizor | 49–50 | Tailwind, burns and priority |
| 4 | Diver | Bronzong / Araquanid / Crawdaunt / Cradily | 50–51 | Trick Room |
| 5 | First Mate | Pelipper / Kingdra / Scizor / Lanturn | 51–52 | Rain and Swift Swim |
| 6 | Captain Eirik | Pelipper / Archaludon / Kingdra / Hariyama / Jellicent / Dhelmise | 52–54 | Full 6v6 doubles |

The first two party entries are the opening pair. Exact moves, abilities, held
items, natures, IVs, EVs and AI flags are in `src/data/trainers.party`. Dhelmise
is exclusive to Eirik and has Jolly maximum Speed with Tailwind support.
No omniscient, forced setup, sequence switching or forced-last-ace AI is enabled.
These remain the approved low-50s baseline levels, pending campaign pacing review.

NPC scripts enforce the clearance order. A free healer is available at the
entrance. Eirik requires six usable non-Egg Pokémon for his first challenge.
Existing completed-captain dialogue remains available without that readiness gate.
The final mooring requires First Mate clearance, preventing a battle bypass.

The original progression bits (crew=1, navigator=2, captain=4) are preserved;
engineer=8, diver=16, first mate=32 are added. Bit updates are additive. Machinery
reset preserves victories and crests. The new machinery version relocates legacy
interior saves to the safe entrance; completed old gyms retain their completion.
New trainer IDs 746–748 remain inside the existing reserved trainer flag capacity.

Curated Havora species and abilities stay fixed when randomization is enabled.
The missing getter for `MON_DATA_CANT_RANDOMIZE_ABILITY` is repaired. Ordinary
trainer construction explicitly retains its previous randomizable behavior,
rather than accidentally treating its ability-slot index as a Boolean exemption.

## Verification

- Development ROM build passed. ROM content: 21,648,552 bytes / 32 MiB. Static
  EWRAM and IWRAM use unchanged; boat searches allocate temporary heap storage and
  release their queue/parent data immediately and their path on trip completion.
- `tools/havora/check_captains_trial.py`: original outdoor layouts, cliffs,
  tilesets, events, connections and warps preserved; all 837 mapped states pass.
- `tests/havora_overhead_routes.py`: all 570 legal trips fit the whole hull;
  berths are independent of water height.
- `tests/havora_lever_visual_emulator.py`: full 25-action native walking/boat
  route, all lever poses/collision/neutral restoration, real boat and valve
  menus, invalid operations, crest, reset, exit and legacy migration pass.
- `tests/havora_three_lock_battles.py`: all six native double battles launch.
- `tests/havora_team_data_emulator.py`: real NPC party construction matches all
  22 approved sets exactly, including with trainer/ability randomization active.
- `tests/havora_gym_progression_emulator.py`: clearance bits, six-usable-mon
  readiness, free healing, reset preservation and completed-save migration pass.
- `tests/havora_lever_ui_emulator.py`: real mooring completion and reset UI pass.
- `tests/havora_fixed_berth_visual_emulator.py`: stationary-camera
  LOW/MID/HIGH/MID/LOW native tide cycle keeps the boat at its berth.
- `tests/record_three_lock_gym.py`: fresh 2:19 native walkthrough; standing
  passenger/boat alignment verified on 1,340 captured frames. Automated controls,
  2× playback, and all six battles preset as won are labelled in the video.

Tests use an mGBA libretro core and ARM binutils as in the existing Havora harness.
The party-data probe is compiled and injected only by the test; no debug battle
probe is added to production code. Neither complete competitive battle balance
nor perfect AI coordination is established by launch/data checks. Those still
require player matchups and difficulty playtesting.
