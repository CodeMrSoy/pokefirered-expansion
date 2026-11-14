# Main-menu game modes

The Continue/New Game menu opens **Randomized Options** in place of the old
randomizer/seed card. The seed is internal and is never displayed on this card
or settings screen. A toggles; Left selects Off; Right selects On; B returns.

| Selection | Behavior |
| --- | --- |
| All Pokémon | Randomize wild, trainer, fixed, starter/gift and egg species. |
| Moves | Randomize level-up learnsets; ordinary trainers use the current learnset instead of overwriting it with authored moves. |
| Abilities | Enable the existing stable per-species ability randomizer. |
| Level caps | Enable the existing campaign milestones and experience/Rare Candy cap. Off restores the normal maximum level and experience behavior. |
| Nuzlocke | Restrict captures to the first eligible wild battle in each named map area. |
| Items | Independently enable the existing field-item randomizer. |
| Vidra gyms | Opt themed Vidra gym teams into the selected Pokémon, Moves and Abilities categories. Defaults to Off; does not enable any category by itself. |

With **Vidra gyms Off**, all eight current Havora Gym encounters retain their
authored species, moves and abilities, including Harborhand and Lockkeeper.
With it On, each enabled category applies to these teams. The selected row warns:
“WARNING: Designed for specific Pokémon, abilities and moves.” Kanto gyms continue
to follow the main categories. Future Vidra gym definitions must be added to
`GameModes_PreserveGymTeam` when their trainer IDs are implemented.
The seven-option list scrolls to keep its selection and warning visible.

Settings belong to the current save, take effect on Continue and persist with
the next ordinary game save. Starting a new game carries the selected modes
forward, creates a fresh seed when any randomization is active, and clears
Nuzlocke encounter history. Switching categories does not reroll an existing
seed. Legacy saves migrate to their previous all-on/all-off randomization
behavior, with caps on and Nuzlocke off.

Nuzlocke records an area when its first eligible wild battle starts, not when
a Pokémon is caught. Grass, surfing, fishing and other wild encounters share
the area's map-section ID; floors sharing a named area share one allowance.
Fleeing, knocking out the opponent or failing to catch it uses that allowance.
Repeated ball attempts are allowed during the first encounter until a catch.
Later encounters reject balls in the bag, last-used-ball shortcut and direct
battle/Safari command. An explanatory message replaces a failed capture attempt.
Gifts and trainer battles do not use an encounter. Catching tutorials, ghosts,
link/recorded and facility battles are excluded. Invalid area IDs cannot be used
to bypass the restriction. Turning Nuzlocke off and back on preserves history;
enabling it on an existing game tracks encounters from that point forward.
This mode adds the requested catch restriction; it does not enforce permanent
fainting, a duplicate-species clause or a shiny exception.

SaveBlock2 uses 34 bytes of its existing 207 reserved bytes for a version,
settings mask and 256-area bitset. Its size and all earlier offsets are unchanged.

## Verification

- `make check TEST_SOURCES="test/game_modes.c test/battle/ai/quantum_ai.c" TESTLDFLAGS=--gc-sections TESTS="" -j8`
- `MGBA_CORE=/path/to/mgba_libretro.so ARM_NM=/path/to/arm-none-eabi-nm python3 tests/game_modes_menu_emulator.py`
- `python3 tests/randomizer_regressions.py`
- `python3 tests/randomizer_field_items.py`
- `python3 tests/quantum_ai_profiles.py`

The menu emulator checks independent controls, stable seeds, repeated open/close,
return from general Options, New Game, Flash reload, Continue, and saved encounter
history. Screenshots are written under `build/quantum-qol-tests/` for visual review.

Validation on 2026-11-14: release ROM build passed; all 21 focused emulator test
groups passed, including parameterized category and ball-command checks; the
menu/Flash emulator and all three listed host-check scripts passed. The menu and
Continue screenshots were visually reviewed. No full legacy test-suite claim is
made by this focused run.
