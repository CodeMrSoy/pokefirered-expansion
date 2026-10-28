# Story level progression

`story-levels.json` records the requested caps, area ownership, and the exact
before/after levels for this rebalance. The baseline commit is recorded so the
audit remains usable after committing the changes.

| Milestone | Old ace | New cap | Area shift |
| --- | ---: | ---: | ---: |
| Brock | 14 | 14 | 0 |
| Misty | 21 | 21 | 0 |
| Lt. Surge | 24 | 24 | 0 |
| Erika | 29 | 29 | 0 |
| Koga | 43 | 35 | -8 |
| Eirik | 54 | 46 | -8 |
| Sabrina | 43 | 50 | +7 |
| Corvala leader | Unbuilt | 57 | Pending content |
| Blaine | 47 | 63 | +16 |
| Brandon (Eldervale) | Unbuilt | 68 | Pending content |
| Ben (Myrdal) | Unbuilt | 73 | Pending content |
| Cody (Iskora) | Unbuilt | 79 | Pending content |
| Giovanni | 50 | 82 | +32 |
| Elite Four / Champion | 63 | 90 | +27 |

All members of a team receive the same shift; only levels change. Held items,
abilities, EVs, IVs, moves and species stay intact. Existing wild encounter
weights, species, time/version tables and slot counts stay intact. Level ranges
shift at both ends; levels cannot fall below 1 (notably Old Rod encounters).

Area scope:

- Koga: Fuchsia, Safari Zone, and Routes 12-18.
- Eirik: all Havora maps, including the Gym and the new grass/water pools.
- Sabrina: Saffron, Fighting Dojo, Silph Co., and Power Plant.
- Blaine: Cinnabar, Pokemon Mansion, Seafoam, Routes 19-21, and the original
  three Sevii islands/Mt. Ember visited after Blaine.
- Giovanni: his own team, Route 23 and all Victory Road floors.
- League: the four Elite Four teams and all three first-Champion variants.

Viridian City/Forest, Route 22 (including both rival encounters), and Viridian
Gym support trainers stay unchanged. Giovanni himself is explicitly changed to
82. Earlier story areas retain their existing levels because their caps did not
change. Later Sevii/postgame maps are outside this first-story rebalance.
Active Vs. Seeker teams follow their area's shift; retired definitions under
`#if 0`, including League rematches, remain unchanged.

Scripted wild battles also follow their area: both Snorlax, Electrode, Zapdos,
Articuno, Moltres and the Berry Forest Hypno. Gifts, eggs, fossil revivals and
trades are unchanged.

The cap function uses Kanto badge flags and `VAR_VIDRA_CRESTS` in story order.
Eirik also recognizes his trainer defeat flag and the older Havora progress bit.
Completed games remain uncapped at 100, including older saves without Vidra
crests. Existing hard EXP and Cap Candy behavior uses these caps automatically.

**Unbuilt Gym integration:** Corvala, Eldervale, Myrdal and Iskora currently
have no Gym battles or wild encounter tables. Their future victory scripts must
award crest bits 1, 2, 3 and 4 respectively (preserving other bits). Until those
Gyms are implemented, their unfinished milestones intentionally stop cap
progression at 57, 68, 73 and 79. This change does not fabricate their teams or
award unearned victories.

Run from the repository root:

```sh
python3 tests/story_level_progression.py
python3 tests/havora_wild_encounters.py
python3 tests/havora_captain_rules.py
python3 test/host/cap_candy.py
```

The progression audit compiles the actual cap/EXP functions with host save
mocks and checks all 16,384 milestone combinations. It also checks every changed
trainer and wild level, route/rematch coverage, and the generated trainer header.
The Havora audit runs native encounter generation and compiled selection code.
These are source/host checks; they do not replace an emulator playthrough.
