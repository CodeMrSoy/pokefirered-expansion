# Koga's Havora shopping trip

Before earning the Soul Badge, Koga is shopping beside the berry sellers in
Havora Market (2, 48). The Fuchsia Gym guide explains his absence and points
toward Vermilion's ferry. A stationary visitor in Havora Harbor (15, 23) says
Koga headed north toward the market to buy battle items.

Talking to Koga plays his shopping dialogue and a brief ninja departure. He
then stays at his original Fuchsia Gym position, ready for the existing leader
battle, Soul Badge and TM reward. The harbor visitor's dialogue changes to say
he returned home. The conversation gives no badge or items.

The Vermilion ferry now accepts the Rainbow Badge as an alternative to the
existing Stellar Ticket. The low-level ferry destination check uses the same
condition and still requires departure from Vermilion. Both routes retain the
boat animation, Vidra artwork and disembark sequence. Return sailings work as
before. The harbor and market can be reached on foot; Surf still requires the
Soul Badge. No encounter or trainer level scaling is changed by this update.

Persistent state uses two previously unused flags, with no save layout change:

- `FLAG_KOGA_RETURNED_FROM_HAVORA` (0x4E9) completes the encounter and hides the
  market object.
- `FLAG_HIDE_FUCHSIA_GYM_KOGA` (0x4EA) hides his gym object until he returns.

Map entry scripts normalize existing saves that already have the Soul Badge
or Koga's defeated flag: Koga remains in his gym, and the market encounter is
skipped. New saves must speak to him in Havora before challenging him.

Validation: `tests/havora_koga_emulator.py` exercises the actual ferry and
object interactions, normal walking without Surf, all four interaction sides,
the original gym battle starting, permanent return through flash save/reload,
existing post-Koga saves, and native-font dialogue widths. The existing
`tests/vidra_arrival_art_emulator.py` checks ticketed sailings, return trips,
arrival graphics and rejected destinations. Standard FireRed build required.
