# Three-lock Captain's Trial — playable prototype, uncommitted

The dedicated indoor layout is now 80x54. Outdoor Havora layouts, cliffs,
events, ferry scripts, tilesets, connections and return destinations are unchanged.
The three existing exit warp indices are retained at the new west entrance.

## Implemented mechanics

- Three chambers, LOW/MID/HIGH water and four conserved transferable units.
  Each labeled valve transfers exactly one level. Empty/full endpoints reject
  the operation; mismatched chamber gates reject boat travel.
- Dry control decks, ladder shafts, separate landing heights, and lower docks
  that disappear under higher water. The stair shafts sit outside the flooding
  footprint. This also leaves the entrance accessible at every water level.
- Two sail-less boats with separate physical berths and native destination menus.
  The narrow launch is transport; the broad cargo boat can become a secured bridge.
  Players walk aboard, stand during smooth sprite travel, and walk off at a landing.
- The cargo bridge reaches an isolated service platform. Its maintenance winch
  is one level lower and is actually flooded/inaccessible at HIGH. Drain to expose
  it, release the final mooring chain, then refill to align the bridge for return.
- C's shore is walkable only at LOW. The final cargo bridge requires B and C
  HIGH plus the maintenance release. It connects B, the outer staging quay and
  the captain island. The island has no ordinary landing to bypass that bridge.
- B/C controls require dock-crew clearance; the C manifold requires navigator
  clearance. All three existing trainer battles remain native doubles. The
  captain awards the Havora Crest on the separate Trainer Card page.
- Status gauges report all three heights. Green bells reset machinery and return
  to the entrance while preserving trainer victories and crest progress.

## Saved state and resources

The existing 0x40D7 variable is versioned and packs the three water levels, two
berths, cargo mooring and maintenance release. The previous 0x40D8 trainer
progress and 0x40D9 crest mask are preserved. Old interior saves initialize the
new machinery and relocate to the safe entrance; this was tested in the emulator.
No save structure changes or static EWRAM additions. Each occupied boat ride
temporarily allocates its sprite tiles/palette and releases them on completion.

The drawing and route model share generated geometry. Five extra abstract states
come from the final bridge's real connection through the outer staging quay.
The shortest solution remains 25 decisions and ten transfers. All 837 reachable
states still have a natural recovery route. Removing cargo travel, launch reuse,
A/B transfers, the LOW shore or maintenance release makes the model unsolvable.

## Actual verification

- Development ROM compiles: 21,648,308 bytes used (64.52%); static EWRAM remains
  258,376 bytes. ROM padding is still the normal 32 MiB.
- Tile collision/elevation flood-fill checks compare actual walk components and
  usable boat landing access against all 837 abstract states, including the exit.
- mGBA completes the entire 25-action solution with actual D-pad walking and
  ladder transitions, native boat movement, and a packed-state assertion after
  every decision. Machinery actions in that route test are called directly.
- Separate actual A-button tests cover the native boarding destination menu,
  selecting a boat route, and the valve Yes/No prompt. Invalid operations reject
  without corrupting the state. Re-entry, legacy save relocation, crest recording,
  reset preserving victories and the exterior exit all pass.
- All three native four-battler double battle scripts launch. Complete combat
  balance/playthrough is not claimed. The recorded puzzle route presets victories.
- The video also verifies idle passenger pose and pixel-perfect boat tracking on
  1,916 captured frames. It includes automated controls, shortened idle pauses and 2x playback,
  all labeled onscreen. It is an actual emulator capture, not a concept animation.

## Remaining work

This is the functional layout pass. Upper galleries, room framing, pipe labels,
boat-route feedback and furnishings need an art pass after puzzle review.
Human difficulty testing remains important; solver counts are not a substitute.
No Porymap UI testing or commit/push is claimed for this unreviewed prototype.

Build assets with `python tools/havora/build_captains_trial.py`; the final stage
is `build_fixed_transfer_gym.py`. Run `check_captains_trial.py` for preservation
and physical state checks. Emulator drivers are `havora_three_lock_emulator.py`,
`havora_three_lock_battles.py`, and `record_three_lock_gym.py` in `tests/`.

### Supplied lever artwork revision

Replaced custom control wheels/levers/bell at metatiles 0x300–0x303 with the user-supplied lever sheet (`graphics/havora_gym/source/lever-reference.png`). Reduced doubled 32px cells to native 16px, mapped housing and colored handles to the existing private palette, and filled transparency with platform planks. No interaction positions, collision, scripts, or puzzle rules changed. Static mapped-state validation passes all 837 states; outdoor preservation checks pass. This initial replacement was static; the following polish pass adds animation.

### Lever and script polish

- All four control colors have native 16px left/upright/right poses derived from the supplied sheet; upright is the resting pose. A successful water transfer, mooring action, maintenance release, or reset animates its own physical lever and plays FireRed's switch sound. Transfer controls spring back as the water settles.
- Control coordinates and command/direction associations are generated from the same source as background events. This prevents adjacent forward/reverse levers from animating the wrong control.
- Mooring actions now run a short locked animation before their completion message; reset waits for its animation before returning to the entrance. Existing conservation, save state, clearance, and boat rules remain unchanged.
- Added explicit mooring/chain error and completion text; removed unused dialogue from the earlier single-lock puzzle, and replaced obsolete bell references with green-lever instructions.
- Added continuous timber rafters and perimeter posts only in already-blocked backdrop cells. The 837-state walking/landing proof and outdoor preservation check pass.
- Development build succeeds at 21,648,476 bytes of ROM content (64.52% of 32 MiB), with unchanged static EWRAM/IWRAM use. Native emulator checks cover the complete solution and all lever poses, collision, and spring return. No Porymap UI testing is claimed.

The native A-button mooring completion and animated reset scripts also pass. Shortened overlong dialogue after reviewing the actual message box.

Changes remain local for review.

### Structural waterline revision

The flooded bank cutoff now interpolates over all eight transfer stages with the waterline. The maintenance ledge and boarding pads follow that intermediate cutoff too; they no longer wait until the end to change. The fixed-transfer rules and final collision states are unchanged.

The private tile kit now includes a quiet outside border, stone coping, continuous boardwalk rails and pool-facing deck lips. A compact masonry perimeter and solid support blocks replace the repeated timber backdrop; disconnected partial furniture was removed. The stair shafts remain dry and retain their existing elevation transitions.

Verification: development compilation, all 837 mapped states and outdoor preservation, full native emulator solution and lever checks. `waterline-structure.gif` is a native emulator inspection showing a direct scripted drain/fill cycle from the lower dock viewpoint; it is not a player-operated console walkthrough. Changes are uncommitted.

### Reviewed terrace treatment applied across the gym

Implemented private metatiles 0x3C0–0x3C4 for rounded terrace fronts with a highlighted coping and two shaded brick courses. All six banks use the new fronts; the captain and service platforms receive matching corner/front pieces. Ladder shafts now have wooden landings with one short metal flight at each elevation break rather than continuous repeated rungs. Elevation-zero traversal and all established docking coordinates are retained.

All three pools now expose only a shallow rear retaining face (0–2 tile rows), while progressive deck flooding remains tied to the fixed transfer. Boats still move between the existing height-specific berths; this is an adaptation of the reviewed art to the existing puzzle geometry, not a replacement of its layout with the smaller study.

Build and full-state/native route checks are recorded under `build/terrace-*.log`. Outdoor maps and branches are untouched; this work is not committed or pushed.
