> Current rules: [directional color-switch trial](directional-tidal-trial.md). The recipe-based rules below are historical.

# Havora seven-station tidal trial

The recipe below is retired. The current puzzle starts at **LOW / LOW / LOW**
and keeps two distinct-color switches on each of the seven authored platforms.
Use the directional trial document for the current routes, switch colors, and
solution.
Operate at least one successful switch on each platform and defeat its crew.
All seven switch clearances and seven crew victories are required for Eirik.
Failed or no-op operations do not count. Earlier victories survive a reset.

The authored LOW map, tilesets and three water silhouettes are preserved.
The lower platforms beside A/B are **MID-height** (their stairs remain usable
at LOW/MID; the platforms disappear at HIGH). Section C's foot crossing is
**LOW-height**: it joins both sides only at LOW and floods at MID/HIGH.
The bunker is reachable at LOW, a solid roof at MID, and submerged at HIGH.

## Controls

On each quay the top lever raises the local section one step, the middle lever
lowers it one step, and the bottom lever cycles the labeled remote section
LOW → MID → HIGH → LOW. Raising at HIGH or lowering at LOW fails without credit.

| Station | Top | Middle | Bottom | Crew's required A / B / C |
| --- | --- | --- | --- | --- |
| A WEST | Raise A | Lower A | Cycle B | MID / LOW / LOW |
| A INNER | Raise A | Lower A | Cycle B | HIGH / MID / LOW |
| B WEST | Raise B | Lower B | Cycle C | MID / MID / MID |
| Switch island | Raise A | Lower C | Transfer one level A → C | MID / MID / HIGH |
| B EAST | Raise B | Lower B | Cycle A | HIGH / HIGH / HIGH |
| C WEST | Raise C | Lower C | Cycle A | HIGH / HIGH / MID |
| C EAST | Raise C | Lower C | Cycle B | MID / MID / LOW |

Trainer prerequisites follow the table order. Eirik retains his six-Pokémon
doubles encounter and requires six conscious, non-egg party members. The five
existing crew teams remain unchanged. Two added stations use copies of the
Dock Crew and Engineer teams with separate trainer flags.

## Movement and recovery

Marked pads provide fixed ferry/lift trips with dialogue and a same-map fade.
The water animation and artwork do not generate bridges or change the map.

- A WEST ↔ A INNER: ferry at the upper pads.
- A INNER ↔ B WEST: lower landing lift at (24,16) and (30,16); **both MID**.
- B WEST ↔ switch island ↔ B EAST: ferry pads, **B MID**.
- B EAST ↔ C WEST: upper lock lift, **B HIGH and C HIGH**.
- C WEST ↔ C EAST: walk the authored crossing, **C LOW**. No transport bypass.

Onward transport requires earlier crew clearance. Reverse trips remain usable
at their required levels. A gauge panel on every quay, or a crew's hint/after
conversation, can drain all pools and return the player to the entrance while
preserving defeated trainers and successful switch clearances. The entrance
steward heals for free. The steward, island trainer and captain disappear when
their respective floors flood and return when exposed.

## One complete solution (spoilers)

1. A WEST: raise A to MID; defeat Harborhand. Raise A to HIGH and ferry across.
2. A INNER: cycle B to MID; defeat Dock Crew. Lower A to MID; use lower lift.
3. B WEST: cycle C to MID; defeat Diver. Ferry to switch island.
4. Island: raise A to HIGH; transfer A → C. Defeat Lockkeeper at MID/MID/HIGH.
   Raise A to HIGH again; ferry to B EAST before changing B.
5. B EAST: raise B to HIGH; defeat Engineer. Take the B/C HIGH lift.
6. C WEST: lower C to MID; defeat First Mate. Lower C to LOW to open its crossing.
   Cycle A HIGH → LOW → MID. Walk across to C EAST.
7. C EAST: cycle B HIGH → LOW → MID; defeat Navigator.
8. Follow the exposed LOW crossing into Eirik's bunker. All seven crews and
   switch stations are cleared; challenge him with six conscious Pokémon.

The shortest modeled solution takes 28 actions (switch operations, crew battles,
transport trips and the C crossing), followed by walking to Eirik. Individual
walking steps and Eirik's battle are not counted in those 28 actions.

## Reproduction and verification

`tools/havora/tidal_trial.json` is the rule source. Run
`python tools/havora/build_tidal_trial.py` to regenerate event bindings, scripts
and the C rule header. `overhead_lock_geometry.py` independently generates the
27 water overlays from the existing reference silhouettes.

- `tests/havora_tidal_trial.py`: searches the puzzle, proves every station's
  switches are mandatory, and follows the solution on actual collision and
  elevation tiles with solid NPCs. Confirms unchanged authored LOW map.
- `tests/havora_tidal_trial_emulator.py`: replays the solution against compiled C,
  exercises real C-crossing/MID-stair walking, scripted transport, rejected
  bypasses, NPC occlusion, recovery, save migration and all eight doubles scripts.
- `tests/havora_section_water.py`, `tests/havora_artwork_assets.py`: preserve the
  27 water states, MID lower platforms, island/bunker behavior and original art.

Save vars: `VAR_HAVORA_GYM_STATE` is now version 0x8000 plus ternary water (0–26).
`VAR_HAVORA_GYM_PROGRESS` retains old crew/captain bits and adds Harborhand (64)
and Lockkeeper (128). `VAR_HAVORA_GYM_SWITCHES` (0x40DA) stores seven station bits.
Legacy unfinished states reset water/position, preserving earned victories.
An existing captain victory marks the trial complete and retains the crest.
Artwork-review command 26 remains available to emulator tools only; no player
map event invokes it. All old transfer/mooring commands are removed.
