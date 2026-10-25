# Vidra crest page

The local FireRed Trainer Card has three views: Kanto front, Vidra crests,
then the original statistics. A or Right opens Vidra from the front; A or Right
from Vidra opens statistics. B or Left from Vidra restores the Kanto front.
The original statistics B returns to the Kanto front; front B closes the card.
Link/remote cards retain their original two-side behavior.

There are five reward slots, separate from Kanto badge flags. Harbor uses a
small blue anchor seal; unearned slots are gray. Four future crests use neutral
numbered placeholders until their gyms and artwork are defined. These are not
implemented gym rewards. Native menu colors avoid new palette allocations.

VAR_VIDRA_CRESTS reuses previously unused save variable 0x40D9, bits 0-4.
HavoraGym_Control's reward refresh ORs bit 0 after captain victory. Existing
saves with VAR_HAVORA_GYM_PROGRESS bit 2 also display Harbor automatically.
No save structure, link TrainerCard struct, Kanto badge or Trainer Card star
calculation changes. The front text window expands by one tile column to keep
the crest page's right edge clean; its allocation remains below window 0.

Verification: successful development ROM build; mGBA tests empty/earned Harbor,
legacy victory, five-bit masking, front/crests/statistics navigation, portrait
restoration, closing and reopening. Gym tests check Harbor reward recording,
boat/lock/gangway/reset, exit and native double battle launches. Link behavior
is guarded in code; no two-console link session was tested.

## Artwork revision awaiting review

The revised page uses a blue-and-gold title panel, a pale striped inset,
recessed crest holders and a 24-pixel Harbor enamel shield with an ivory anchor.
The four unassigned crests retain muted empty mounts, rather than fabricated
badge designs. A framed Harbor description replaces the earlier plain list.

A private 16-color window palette follows the native FireRed card colors.
All 16 original palette entries are saved in the allocated UI state and restored
before either the Kanto front or statistics is shown. This adds 32 bytes to the
card's temporary allocation, no static EWRAM or save data. Development build
passes (21,623,160 ROM bytes used); mGBA checks palette restoration, card
navigation, earned/unearned Harbor, portrait restoration, closing and reopening.
The review previews are `review/vidra-crests-art-review.png` and its locked
counterpart. This revision is uncommitted for visual review.

The spacing revision renames the displayed reward to Havora (including the
captain's award text), centers all five labels using measured font widths,
raises the anchor two pixels within the drop's bowl, and enlarges the description
panel with padding on both text lines. The latest build and native card tests
pass; `review/vidra-crests-spacing-review.png` is the earned-state screenshot.
This revision remains uncommitted for review.
