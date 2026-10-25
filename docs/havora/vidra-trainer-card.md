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
