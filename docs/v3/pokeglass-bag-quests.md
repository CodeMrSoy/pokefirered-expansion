# V3 Bag grid and Quest Book

Implemented on `Pokemon-Quantum-V3` from `30a6e919`. V2 and Living World are
unchanged. Crown references informed composition; graphics use Quantum's own
Bag, item sprites, tablet shell and a new tile-drawn book icon.

## Source audit and design

The two existing six-slot launcher pages are full. Quest Book occupies the
bottom-right slot on a third page. Existing app IDs, slots and dispatch remain;
horizontal movement skips reserved/unavailable slots. No application is replaced.

The Bag's native ListMenu, inventory pockets and action tasks remain authoritative.
The grid adapts their absolute selection index, replacing only their printed rows
inside a normal PokéGlass Bag session. Battle, tutorial, item-PC and other native
entry points retain their original layouts and restrictions. TM Case, Berry Pouch
and Field Item Case remain separate native applications, accessible as before.

The existing Bag has three inventory pockets: Items, Key Items and Poké Balls.
A 64x64 Bag sprite, including pocket animation, stays visible on the left. Its
selected item name and word-wrapped description occupy the lower left. Nine real
item sprites, quantities and a selected-cell outline occupy the right. Icons are
rebuilt only when page, pocket or item identities change. Quantities and text are
redrawn on input/action return, rather than every frame. No placeholder item art
or copied Crown assets are used.

### Controls

| Screen | Controls |
| --- | --- |
| Bag | D-pad: grid; L/R: pockets; A: item actions; B: return |
| Bag descriptions | Hold L+R together to cycle full wrapped description pages |
| Bag sorting | START: native sort menu; SELECT: native manual reorder |
| Quest Book | Up/Down: quests; Left/Right: objective/story/location/reward pages |
| Quest Book filters | SELECT: All, Main, Side, Done; undiscovered entries stay hidden |
| Quest Book actions | A: track/untrack active quest, accept offered quest, or collect/archive completion |
| Optional offer | D-pad: Accept/Decline; A: confirm; B: decline or leave an accepted quest |

A cyan or white status marker indicates progress; the tracked entry has a red
marker. The right pane has bounded, word-wrapped pages and a visible Info control.
Story rewards stay with their original NPCs; archiving adds no duplicate reward.

## Quest registry and gameplay hooks

`include/constants/quest_book.h` assigns stable IDs. `src/quest_book.c` owns the
validated definitions, centralized discovery/completion conditions and reward
operations. `src/poke_glass_quests.inc` renders views and calls that API; temporary
UI state is never the authoritative quest record. `src/poke_glass_text.c` shares
actual-font word wrapping between Bag and Book.

| ID | Quest | Verified source of progress |
| --- | --- | --- |
| 0 | Oak's Parcel | Starter/Pokédex flags and actual parcel ownership |
| 1 | Kanto Badges | Eight existing Kanto badge flags |
| 2 | Safari Expedition | Fuchsia discovery, HM03/HM04 flags and Gold Teeth ownership |
| 3 | The Vidra Passage | Quantum only: Stellar Ticket, Vidra map visit, Koga's return flag |
| 4 | The Harbor Trial | Quantum only: Havora Gym progress bit 4 or Eirik crest bit 1 |
| 5 | Field Notes | Optional aide offer, post-acceptance Route 1 visit, report to that aide |
| 6 | Indigo Challenge | Earth Badge discovery and existing game-clear flag |

The registry can hold 32 stable IDs. This release defines seven quests; it does
not invent objectives for unfinished Vidra locations. Main-story tracking observes
existing requirements and never adds a new campaign gate. Classic cannot obtain
Vidra definitions, even by passing their IDs directly to the public API.

Field Notes is offered by the first Oak aide after obtaining the Pokédex, after
his original dialogue. It remains available after the Hall of Fame. The player
may decline and later reconsider. Visit Route 1 after acceptance, return to the
same aide, and receive three Poké Balls. The report cannot complete before the
visit. Full inventory leaves the reward pending. Collection is allowed once.

Reusable script sequence:

```asm
setvar VAR_0x8004, QUEST_FIELD_NOTES
callnative QuestBook_OfferFromScript, requests_effects=1
compare VAR_RESULT, FALSE
goto_if_eq EventScript_ReleaseEnd
waitstate
release
end
```

The native offer validates the ID and optional/discovery rules before opening,
reports hardware/save effects, hides the previous dialogue and suspends the
script through `waitstate`. Its UI task resumes that script on exit. Invalid IDs
or unavailable storage return FALSE and must not enter `waitstate`.

Available, Active, Completed, Claimed and Declined states work. Failed is reserved;
none of these quests has a failure condition. Gameplay polling runs once per 30
field frames and skips the original FireRed Quest Log playback. Updates also run
when opening Book or reporting to the aide. Future optional content must add a
compiled, validated definition and condition hook. The API accepts registered
IDs; it provides no arbitrary save writes, dynamic rewards or runtime AI access.

## Save compatibility

ARM compile-time assertions preserve SaveBlock1 at 15,780 bytes and SaveBlock2
at 3,968 bytes. Existing seed/settings, Nuzlocke and adventure offsets are
unchanged. Quest Book uses 144 bytes of old reserved padding at offset 3803;
21 bytes remain reserved. The unaligned record uses byte operations, not casts.

A tagged/versioned header precedes 32 four-byte records (state, current objective,
16 objective bits). Tracking is a validated header ID. The normal Flash sector
checksum covers this data. An older save with all-zero padding initializes its
quest record and derives story progress from current flags. Unknown nonzero
padding is preserved, and Book reports unavailable rather than overwriting it.
This does not replace existing adventure, Pokémon or gameplay-settings migration.

Real prior-ROM Classic V3, Quantum V3 and pre-V3 Flash fixtures loaded successfully.
Identity, adventure choice, seed/settings/history and remaining padding were
checked. The pre-V3 fixture correctly followed the existing game-mode migration
(default caps and version tag). The optional quest also survived two actual
Flash saves, resets and Continue loads, including after reward collection.
Private save fixtures are not committed or included in the release package.

## Executed QA

Native ARM build passed. mGBA libretro executed these focused suites:

| Suite | Result |
| --- | --- |
| `pokeglass_bag_grid_emulator.py` | All three pockets, real icon IDs, quantity 999, 3x3 movement, multiple pages/Back, empty pocket, sorting, reorder, description pages, field return |
| `pokeglass_bag_actions_emulator.py` | Potion healing/consumption, toss, give last item/removal, directional registration, TM/Berry/Field Item Cases, controls restored |
| `quest_book_emulator.py` | Hidden quests, invalid IDs, Classic filtering, unknown-padding protection, zero-padding migration, actual aide script, decline/accept, visit/report, full-Bag retry, exact reward quantity, duplicate rejection, tracking and Flash/reset persistence |
| Quest Book pixel checks | Both panel borders intact across 48 detail navigations and Side filter |
| `quest_book_legacy_emulator.py` | Three private older Flash fixtures; identity, adventure, settings migration and reserved-byte checks |
| `adventure_mode_menu_emulator.py` | Fresh Classic and Quantum; intro/avatar, cancellation and Flash/reset/Continue |
| `pokeglass_text_layout_emulator.py` | 49 captured states: Dex, Stats, Storage, Party, Summary, Field Kit, Trainer Card, Save and Options; text/border checks |
| `pokeglass_time_return_emulator.py` | Repeated Party/hub/field returns in day/evening/night, outdoors/indoors and rain |

Build footprint: EWRAM 238,896 / 262,144 bytes; IWRAM 27,573 / 32,768 bytes;
linked ROM 21,923,924 / 33,554,432 bytes, padded to 32 MiB. Relative to the source
baseline, persistent EWRAM grew 64 bytes; save-block sizes did not grow. Up to
nine grid sprites/palettes supplement the existing Bag sprite. Windows use
separate tile ranges; normal native action windows keep their existing allocator.

## Limits and further validation

This is a test build, not a certification of a full campaign playthrough. No
complete Classic/Quantum run, every randomizer combination, every battle item,
physical-GBA test, link session, or exhaustive full-capacity inventory was run.
The focused checks exercise actual UI, scripts, gameplay events and Flash saves;
compilation alone is not counted as gameplay verification. Existing campaign,
AI, Nuzlocke and randomizer code remains shared and otherwise unchanged.

More side quests, additional implemented Vidra Gym definitions and a gameplay
performance profile can build on this registry. Historical five-row Bag visual
tests need grid-specific expectations; the new grid suite supplies those checks.
