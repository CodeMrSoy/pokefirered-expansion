# Recessed lock and passenger prototype (uncommitted)

The existing Captain's Trial route is retained while the visual mechanics are
reworked. This is the first-chamber prototype, not the proposed harder multi-lock
gym. No outdoor maps, cliffs, ferry interactions or connections are changed.

Low water exposes masonry retaining courses and wall marks. Fill/drain steps
move the waterline along those courses, submerging/exposing them with the launch.
Both west landing shutters close during transfer; only the matching upper/lower
shutter opens afterward. Animated water remains the existing native callback.
This is a tile-based height illusion, not a new engine elevation system.

The sailboat is replaced by a small flat wooden work launch. Its private 64x64
sprite contains the same art as the moored 3x3 metatile kit. The player walks on,
stands on deck during the crossing, then walks off. The boat tracks the player
sprite every pixel while the standing animation is held. Temporary sprite tiles
and palette are allocated only for a passenger ride and freed afterward; failure
to allocate returns the existing machinery error without locking controls.

The passenger task, saved boat side/level, control/sign positions and puzzle
rules remain compatible with the existing gym saves. The new visual kit stays
within the private gym pair. No static EWRAM was added.

Verification: development build passes (21,626,296 bytes ROM used, 64.45%).
The independent route/preservation check passes all 48 reachable states. mGBA
checks raising and draining, exposed/submerged masonry, matching shutters,
boarding/disembarking, progress gates, reset/re-entry, exit and three native
double battle launches. A per-frame assertion verifies standing animation and
pixel-aligned launch tracking over 542 occupied frames in both directions.

The 71-second emulator video demonstrates filling, draining, both passenger
crossings, gangways and the crest page. It explicitly labels skipped battles
and cuts between stations. No full combat playthrough or Porymap test is claimed.
