# Phase 11 · Regional NPC society

Phase 10 baseline: `cbacf9e60bd38eaecaf3560714041a44a1e93e28`.
This includes the controller and keyboard-remapping update. Development and
delivery are isolated on `Living-World-Phase11`.

## 11A

The configurable roster contains 24 host-side residents with distinct names,
six occupations, assigned workplaces, weekly days off, and shift times.
A deadline heap drives their schedules. The new table uses the existing
battery checkpoint transaction. No new native NPC slots are allocated.

## 11B

Goals survive daily shifts and battery branches. Profiles establish a work
motive and priority. Work units advance an explicit target over multiple
working days. Expired work ends against a game-clock deadline. Missed shifts
cannot create retroactive work, and a later goal gets its own identity.
