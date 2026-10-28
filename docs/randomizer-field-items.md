# Overworld item randomization

With field-item randomization enabled:
- Item balls and hidden items use deterministic replacements.
- Story key items (including Gold Teeth, Lift Key, Card Key, Secret Key and
  Silph Scope) remain fixed. NPC gifts are unchanged.
- Ground TMs become a different TM from the configured TM01–TM50 pool.
- Other pickups become a different regular item from the existing item whitelist.
- Mail and obsolete ground HMs/field tools become regular items, never rewards.
- Key items, Mail, HMs/field tools, TMs and Z-Crystals are excluded from regular
  item results. Field Item Case remains a progression key item.
- Hidden coins remain coins.

Hidden pickups seed from the current map and their persistent pickup flag,
rather than a stale selected object. Retries and revisits remain deterministic.
The expanded location seed changes uncollected randomized rewards in existing
saves; already-collected pickup flags are unchanged.

The retired Icefall Cave HM07 item-ball script now contains an Ultra Ball.
Basculegion Bait remains deferred for Corvala; this does not add a new source.

Validation: `python3 tests/randomizer_field_items.py` compiles the production
pickup functions with host stubs and the real item constants/whitelist. It checks
200 seeds across every item ID, TM classes, fixed story keys, excluded rewards,
determinism, hidden-item identity and disabled behavior. Host stubs isolate item
selection; this is not a ROM build or emulator progression test.
