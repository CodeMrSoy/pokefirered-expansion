# Living World platform and merge readiness

Infrastructure base `51c4ecb05e7b3e0365aef0d1868ab75ea404be79`. Phase 11 survey
lifecycle, PokéGlass layout and Route 2 retirement fixes are inherited without
changing the game ROM or save format. Keep this branch separate until native
evidence for this release is available.

## Architecture audit

| Boundary | Shared behavior and platform risk |
| --- | --- |
| ROM / mGBA | The ROM owns gameplay and battery RAM. The host uses libretro and checks bounded EWRAM addresses from the matching ELF. Windows loads the pinned x64 DLL and SDL2. Linux uses the matching .so and system SDL2. |
| Model | The same Python planner, schema and validation consume the resident worker stream. Windows launches through AppContainer; Linux uses the seccomp worker. Token choices can vary. Pipe timeouts, Windows policy, NTFS AppContainer access and process startup need native checks. |
| Saves | The host owns one SQLite profile and keys checkpoints by battery hash. The profile lock coordinates infrastructure builds and backups. Older builds do not take this lock, so close them before starting this build. The launcher makes an export without overwriting the originals. |
| Monitor | The host publishes a bounded atomic snapshot. The UI reads it without a writable database connection. Projected ROM actors show intended locations, and the ROM nearby hint identifies a confirmed nearby NPC when available. Host-only residents do not have sprites. |
| Desktop | The menu uses Windows PowerShell 5.1 and WinForms, while game, controls and diagnostics use embedded Python. Desktop policies may disable PowerShell. Direct CMD entry points remain available. |

## Retest

1. Extract the entire versioned ZIP into a new directory on a local Windows
   drive. Run **Open Pokemon Quantum.cmd**.
2. Choose **Living World Demo**, select **Continue**, then open **Living World
   Monitor** in the launcher. Inspect the Pewter location, schedules, events,
   relationships and decision timings. Open the Museum assistant conversation
   and deliver an open Survey Notes objective to the volunteer. Save and reload.
3. **Diagnostics** runs the AppContainer and Qwen checks. **Settings and controls**
   opens the normal SDL remapper. **Save management** exports batteries and the
   SQLite world database into a non-destructive backup ZIP, or opens the profile.
   Manual restoration should be done with the host closed.
4. Test a physical controller's hotplug and menu navigation, window rendering
   and physical audio. The dummy SDL CI drivers cannot verify those behaviors.

## Automated evidence

The push workflow compares a deterministic fixture on Linux and Windows, then
runs a Windows integration job on the exact extracted package. It checks the
ZIP hash and the manifest commit before calling embedded Python. The embedded
smoke checks SDL, a virtual controller, keyboard persistence, libretro,
actual ROM field hints, mailbox write boundaries, battery reload, SQLite
quest lifecycle, sandbox denials, Qwen decisions and worker failure fallback.
It does not drive the full Museum script through Windows SDL.

On branch pushes the Linux build job stages one candidate ZIP, which the
native job downloads, verifies by hash, extracts, and starts. A published
exact-commit ZIP can also be selected with the package URL and SHA-256
repository variables. The native job verifies that the WinForms launcher
showed a window before testing the packaged Python and mGBA host.
On a Windows machine you can run the same smoke from the extracted directory
with `python\python.exe -B package_smoke.py native-smoke.json`. The report
contains the commit and actual check output. Make a report for this exact ZIP,
and retain it alongside the ZIP. An earlier Phase 11 Windows run validated
the same sandbox and Qwen components, but the new launcher and package require
their own evidence.

Release status is in `TEST-RESULTS.json` and `release.json`. Do not merge or
promote the release until the exact Windows candidate and manual launcher and
controller checks pass.

## NPC-originated release scenario

Run `python -B tests/living_world_release_scenario.py`. Ada originates
survey `ada:1:1` during her scheduled work. It is visible as an event in
the monitor before the player has a quest. The assistant discloses it
and a second visit confirms the same open request. Wren cooperates
during the existing simulation schedule. The monitor attributes the
outcome to Wren and both the Quest Book projection and the saved
checkpoint report the survey as completed after reload. The scenario
uses the same scheduler, dialogue decisions and persistence as gameplay,
with model inference disabled to make the cooperation replayable.
