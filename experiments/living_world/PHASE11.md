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

## 11E

An outstanding, published survey request can produce one Survey Notes
objective after an accepted Museum desk dialogue. Player delivery completes
the objective and NPC resolution can independently complete, expire, or
withdraw it. The dedicated projection has a fixed size and source code.
Classic and Quantum mGBA validated all four display states, rollback,
and preservation of the 144-byte native quest record.

## 11F

The model queue handles only survey-assistance decisions where the volunteer
can spare the time. Other shift and relationship choices use deterministic
rules. It allows three eligible requests per regional day and one per actor
per day, with a cap of four pending and 32 processed transitions per tick.
Old decisions become invalid on deadline, save change or response. If the
worker times out, the scheduler retains the already permissible default.
Current foreground actions take priority over queued plans. A resident's
in-flight request can still occupy the one offline worker. Logs record
ready-to-dispatch wait separately from Qwen and executor timings.

Forty-day synthetic measurements under Python allocation tracing on Linux:

| Residents | Transitions | p95 tick | Traced peak | SQLite |
| --- | ---: | ---: | ---: | ---: |
| 20 | 1370 | 4.534 ms | 140 KiB | 128 KiB |
| 50 | 3436 | 6.062 ms | 270 KiB | 160 KiB |
| 100 | 6878 | 11.574 ms | 492 KiB | 208 KiB |
| 250 | 17155 | 27.299 ms | 1089 KiB | 336 KiB |

These workloads made zero model calls. The 250-resident burst exceeded a
60 FPS frame budget with tracing active, and the package uses 24 people.
The size is for one battery history. Separate checkpoint snapshots retain
their own state, so the file can grow as the player makes additional saves.
The roster keeps eight memories and twelve relationships per resident,
24 open requests and 48 events. A simultaneous burst admitted three
distinct volunteers to the real Qwen worker. All three chose to continue
their work in that fixture. Cooperation and refusal were both exercised
by the deterministic simulations. No larger model was adopted.
