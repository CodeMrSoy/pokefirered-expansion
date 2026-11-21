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

## 11C

Occupations supply different work dependencies. A resident can ask an
eligible peer, prefer previous collaborators, and attempt independent work
after two failed requests. The recipient answers from their shift capacity
and existing relationship. A successful exchange records its actual
source, updates both relationships, and unlocks dependent work. Pending
requests expire and are capped at 24.

## 11D

Validated requests now create regional cooperation or survey events. Work
that reaches its goal yields a research, training, or ordinary work result.
Requests can complete, expire, or be withdrawn without a player action.
The capped ledger preserves the active entries and their true origin.
Only researchers' outstanding survey requests are published at the Museum
desk. Other resident memories and internal events remain private.
