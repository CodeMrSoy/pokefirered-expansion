# Randomized Gym rewards and trainer moves

The eight Kanto Gym TM gifts now follow the field-item randomizer setting.
Each leader gives a deterministic, different TM from the configured TM pool.
The chosen TM is resolved before checking Bag space, survives retries, and uses
existing one-time reward flags. Randomized receipt and explanation text refer
to the actual reward; non-randomized games retain the original gifts/dialogue.
Previously claimed rewards are not granted again or retroactively exchanged.
Eirik's Wailmer Wailer remains a fixed progression reward.

CreateMon already initializes moves from the generated species' level-up
learnset, including seeded move randomization when enabled. The custom trainer
party path previously overwrote those moves with the original authored set.
That overwrite is now skipped when trainer species or learnsets are randomized.
Species-only randomization uses the new species' normal level-appropriate moves;
learnset randomization uses that species' randomized level-appropriate moves.
This covers leaders, rivals and other custom trainer parties. With both options
off, authored moves remain intact. Havora's six fixed puzzle crews retain their
specific strategies in every mode. Levels, items, IVs, EVs and team sizes are
not changed by this fix.

Validation commands:

- make -j6 DEVKITARM=<ARM toolchain>
- python3 tests/randomizer_field_items.py
- python3 tests/randomizer_early_catch.py
- python3 tests/randomizer_regressions.py
- python3 tests/randomizer_gym_emulator.py

The emulator regression runs all eight real Gym gift scripts and repeat
conversations, checks seeded TM substitution and disabled behavior, verifies
full-Bag retry, and checks the generated parties of all eight Kanto leaders plus
Eirik against their current initial learnsets in three option combinations.
It also checks the fixed-crew and non-randomized trainer policy.
