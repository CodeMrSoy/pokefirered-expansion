# V2 Havora Gym validation

Target: `Pokemon-Quantum-V2`, commit `db333930` (two distinct switches per platform).

Result: all seven selected source/map and host-controller suites passed. No gameplay logic or map defect was found in these checks. No production files were changed or pushed.

## Verified

- A complete 30-action solution from all LOW with the current two-switch assignments.
- Exhaustive exploration of 287 reachable abstract puzzle states: all can reach one of six captain-ready states without a reset. This treats trainer victories as successful battle actions; it does not simulate combat.
- Omitting any station's battle/switch actions prevents completion.
- Collision and elevation access across 180 platform/water profiles, including legal incoming/outgoing pads, trainers and switches.
- All 27 independent water combinations, 27 native RLE map profiles, 14 active lever bindings, seven removed lever bindings and nine native route entries.
- BL3 -> Island LEFT requires B MID; Island RIGHT -> AR3 requires A/B MID; BL1 -> BR2 requires B HIGH.
- Both dams reject incompatible levels; hull routes clear only submerged crossings. Transport script uses continuous boat handling rather than a map warp.
- C's foot crossing and captain access require C LOW; bunker roof remains at MID, and HIGH submerges it. Island remains exposed at MID and is submerged at HIGH.
- Existing metatiles/art assets are preserved, with the approved latest switch/layout changes.
- All eight battle scripts and source/generated party definitions use doubles. Crew parties remain progressive; the captain has six Pokemon.

## Production C checks on the host

`tests/havora_controller_host.py` extracts and compiles the actual production controller functions using GCC. Engine-boundary stubs supply variables, map entries, party records, immediate tide completion and boat-route availability. It verifies controller decisions, not frame execution.

- 360 live lever/water combinations: four color effects, both wrap directions, blocked island flooding and required trainer victory.
- Removed and remotely invoked levers rejected.
- 243 route/water combinations and outbound station-use requirements.
- Every missing crew victory and switch clearance rejected by the captain.
- All six party slots checked for empty, egg or fainted members; six healthy Pokemon accepted.
- Healing, reset preservation, crest award and unfinished/completed legacy-state migration.

## Commands that passed

```text
python3 tests/havora_directional_trial.py
python3 tests/havora_v2_gym_audit.py
python3 tests/havora_controller_host.py
python3 tests/havora_boat_routes.py
python3 tests/havora_section_water.py
python3 tests/havora_artwork_assets.py
python3 tools/havora/tidal_color_rules.py
git diff --check
```

Individual logs and a machine-readable result list are in `build/havora-tests/v2-audit/`.

## Remaining verification

A new GBA build and mGBA replay were unavailable: this session lacks the ARM compiler and mGBA core, and dependency retrieval failed. Consequently this is a logic/map pass, not a full in-game sign-off. Animation, actual battle execution, trainer approach and real save/reload require emulator checks on a ROM built from this commit.

Some historical emulator suites also need updating for the latest two-switch/color design. In particular, `havora_directional_emulator.py` still references a third lever and old color assignments; `havora_tidal_trial_emulator.py` replays the retired pre-color rules. These old suites were not counted as passing.
