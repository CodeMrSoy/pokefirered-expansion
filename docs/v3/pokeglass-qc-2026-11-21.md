# PokéGlass Bag and Quest Book QC — 2026-11-21

Source: `Pokemon-Quantum-V3` at `3688bbc5`. Changes remain on V3.

Quest Book is a real PokéGlass app on page three, in the bottom-right slot.
Moving right from Options reaches it. The existing apps remain available.

## Bugs found and fixed

1. Native item movement copied intermediate stacks only under an incorrect
   equality condition. A move across several slots could duplicate the source
   and overwrite a destination stack. The loop now shifts every intervening
   item and quantity before inserting the source.
2. The grid stores its absolute selection in `scrollPosition` and keeps its
   selected row at zero. Native move/cancel logic decremented that unsigned
   row when moving downward, allowing it to wrap to 65535. Grid moves now
   adjust the absolute index; cancellation keeps a valid selection.

The full-Bag test failed on the original source, exposing changed item IDs.
After the fixes it passes while checking both IDs and encrypted quantity values
through downward/upward moves, cross-page cancellation and insertion at Back.
The native non-grid selection behavior is retained.

## Executed checks

Native ARM build passed. Focused mGBA libretro tests ran on the actual ROM.

| Check | Result |
| --- | --- |
| Fresh Classic Adventure | Launcher navigation to Quest Book, Book offers/decline/accept/tracking/filters, saving, reset and Continue passed |
| Fresh Quantum Adventure | Same checks passed; mode-specific quest definitions preserved |
| Repeated Bag/Book visits | 24 Classic + 28 Quantum visits; no heap growth, retained backdrop/grid sprite resources or field lock |
| Field lighting | Day, evening and night, indoors/outdoors; Quantum rain; map palettes unchanged after app and launcher returns |
| NPC quest offers | Actual aide scripts at night, normal and postgame branches, in both modes; lighting and controls restored |
| Full Bag | Items 42 stacks, Key Items 30, Poké Balls 27; every cell/page/Back/boundary traversed; sort/reorder/toss and live window tile ranges passed |
| Inventory safety | Item IDs and quantities retained after moves in either direction, across pages, at the end and after cancellation |
| Native item actions | Potion healing/consumption, toss, giving the last item, directional registration, TM/Berry/Field Item Cases and return passed |
| All Bag descriptions | All 656 grid-table records fit one page, with four clear pixel gutters; case-only entries excluded |
| Item graphics | Actual OBJ VRAM matched selected item graphics after pocket switches |
| Quest progression/rewards | Actual aide decline/accept, Route 1 visit/report, full-Bag reward retry, exact reward amount and duplicate rejection passed |
| Quest persistence | Progress, tracking and claimed state survived Flash saves, resets and Continue |
| Older saves | Three private older Classic/Quantum/pre-V3 Flash fixtures loaded with expected identity/mode/settings migration and reserved bytes preserved |
| Other PokéGlass UI | 49 captured states across Dex, Stats, Storage, Party, Summary, Field Kit, Trainer Card, Save and Options; text/border checks passed |
| Party lighting regression | Two returns in each of seven day/evening/night/indoor/outdoor/rain conditions preserved map colors |

Key repeatable suites:

- `tests/pokeglass_bag_quest_qc_emulator.py`, separately with
  `QUEST_QC_ADVENTURE=0` and `QUEST_QC_ADVENTURE=1`.
- `tests/pokeglass_full_bag_qc_emulator.py`.
- `tests/pokeglass_bag_descriptions_emulator.py`.
- `tests/pokeglass_bag_actions_emulator.py` and `pokeglass_bag_grid_emulator.py`.
- `tests/quest_book_emulator.py` and `quest_book_legacy_emulator.py`.
- `tests/pokeglass_text_layout_emulator.py` and `pokeglass_time_return_emulator.py`.

The legacy-save suite requires private local fixtures through
`QUEST_LEGACY_SAVES`. Those save files are not published.

## Scope and remaining validation

No further failures appeared in these focused checks. This is evidence for the
Bag, Quest Book and tested app interactions; it is not an exhaustive claim that
the entire ROM has no bugs. Full campaign playthroughs, all randomizer/Nuzlocke
combinations, every battle item, full-capacity TM/Berry Case stress, link sessions
and physical GBA hardware remain outside this pass.

Save layouts and gameplay settings are unchanged. Final build footprint:
EWRAM 238,896 / 262,144 bytes; IWRAM 27,573 / 32,768 bytes; linked ROM
21,924,844 / 33,554,432 bytes (padded ROM 32 MiB).
