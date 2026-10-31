# PokéGlass UI overhaul

Requested after QoL commit 82967008. Keep the red-and-white 240×160 tablet,
220×140 translucent display, six-box save compatibility, and existing gameplay.

Acceptance checklist (implementation and emulator verification required):

- [x] Two-page launcher: consistent app cards, readable titles/navigation; no wardrobe.
- [x] Pokédex: clearer list/detail hierarchy and usable filtering/area navigation.
- [x] Party: readable six-member layout, icons, HP/status, and retained actions.
- [x] Town Map framed within the tablet when legible, with navigation retained.
- [x] Storage: actual Pokémon icon sprites, full 30-slot box grid plus party;
      preserve move/swap/cancel, item actions, release and last-mon safeguards.
- [x] Ordinary Bag remains fully functional inside the tablet border.
- [x] Dedicated Stats app with complete values/EVs/IVs/nature/ability information;
      remove duplicate Summary stats view while retaining identity/move pages.
- [x] Field Kit app for collected field tools and real use; keep the Bag's case.
- [x] Build, targeted behavior and memory regressions; populated emulator previews.
- [x] Publish to QOL only, verify remote tree and refresh preview ROM.

Existing test/build infrastructure is in the workspace's v2-integration-test
folder. The isolated build tree is recorded in build-directory.txt there.
Use the native incremental build helper to avoid the Windows make dependency
scan issue; expand its changed-source list as additional translation units change.
Execution details and limits are recorded in pokeglass-overhaul-qa.md.
Publishing uses expected-head protection on QOL and compares the remote tree
with the local staged tree; V2 remains a separate integration.
