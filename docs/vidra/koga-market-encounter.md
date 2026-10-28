# Koga's Safari clue and Havora shopping trip

Before earning the Soul Badge, a stationary Gym guide at Fuchsia City (9, 33)
blocks the approach to the gym door. He says Koga left for the Safari Zone and
recommends checking the house at the far end. The blocker disappears permanently
when the player speaks to Koga in Havora and he returns to his gym.

A traveler at Safari Zone Secret House (2, 5) says Koga headed to Vidra, the next
region over, to buy battle items at Havora's market. He gives the player his
extra Stellar Ticket and explains how to take Vermilion's ferry. This is a
separate NPC; the original attendant still gives the Wailmer Wailer for Surf.
The gift retries if the Key Item pocket is full and never duplicates a ticket.

Vermilion's ferry requires the Stellar Ticket. The prior Rainbow Badge bypass
has been removed from both sailor scripts and the destination guard. Ticketed
sailings retain the boat animation, Vidra artwork and disembark sequence. The
harbor and market can be reached on foot; Surf still requires the Soul Badge.
No encounter or trainer level scaling is changed by this update.

Koga is beside the berry sellers in Havora Market (2, 48). A stationary harbor
visitor at (15, 23) points north toward the market. Talking to Koga plays his
shopping dialogue and a brief ninja departure. He then stays at his original
Fuchsia Gym position, ready for the existing battle, Soul Badge and TM reward.
The harbor visitor's dialogue changes to say he returned home. The conversation
gives no badge or items.

Giovanni's original FireRed gym script and dialogue are restored: Earth Badge,
TM26, retirement from Team Rocket and farewell. His dropped ticket object and
Vidra pursuit dialogue have been removed. Existing saves that defeated him in
the earlier Quantum version receive the previously withheld Earth Badge during
save normalization. A legacy saved ticket object is hidden; previously owned
Stellar Tickets remain valid and the Safari traveler does not duplicate them.

Persistent flags, without a save layout change:

- `FLAG_KOGA_RETURNED_FROM_HAVORA` (0x4E9) completes the encounter and hides the
  market object and outside gym blocker.
- `FLAG_HIDE_FUCHSIA_GYM_KOGA` (0x4EA) hides Koga until he returns.
- `FLAG_RECEIVED_SAFARI_STELLAR_TICKET` (0x4EB) records the successful gift.

Map entry scripts normalize existing saves that already have the Soul Badge
or Koga's defeated flag: Koga remains in his gym, the blocker is absent, and the
market encounter is skipped. Old ticket-drop flag numbers stay reserved.

Validation: `tests/havora_koga_emulator.py` exercises the physical gym blockade,
Safari gift and full-bag recovery, separate Surf reward, ticketed ferry and
arrival, normal walking without Surf, Koga interactions from all four sides,
reopened gym entrance, original leader battle starting, flash save/reload,
existing saves, restored Giovanni rewards and native-font dialogue widths.
`tests/quantum_stellar_emulator.py` is a compatibility entry point to these
current story checks. `tests/vidra_arrival_art_emulator.py` checks arrival art,
return trips and rejected destinations. Standard FireRed build required.
