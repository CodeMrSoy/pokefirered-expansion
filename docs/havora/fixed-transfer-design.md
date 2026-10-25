# Havora fixed-transfer puzzle — validated abstract draft

Status: the mapped prototype is now implemented in the dedicated gym interior.
The approved larger footprint became 80x54 to fit dry stair shafts, two separate
berths per quay and isolated service/captain islands. See
`three-lock-prototype.md` for the actual build/emulator evidence. This document
retains the design rationale and abstract decision sequence.

## Physical rules

- Water has LOW (0), MID (1), HIGH (2) positions. LOW retains enough baseline
  water to float a boat; zero means no additional transferable water above LOW.
- Four transferable units are conserved across all three chambers. Each valve
  moves exactly one unit from a donor above LOW to a receiver below HIGH.
- Boat gates A/B and B/C open only at equal neighboring heights. Both gates can
  never align simultaneously: that would require all three levels equal, whose
  sum cannot be four.
- All valve controls occupy dry upper decks above HIGH. Lower boarding docks
  flood, requiring a distinct upper landing and ladder/stair access. Being
  allowed to stand on a dry deck does not imply a boat can dock at every level.
- The narrower launch is transport. The broad cargo workboat can be secured
  as a bridge. Both are sail-less; both use the standing-passenger ride.
- Each modeled deck group needs two separate physical berths where both boats
  may be present. They must never overlap on one map coordinate.

## Interconnected layout

A is the receiving lock, B the service lock, C the captain lock. Start with
A HIGH, B HIGH, C LOW; player/launch at A west quay and cargo at C control quay.
The captain deck is above the outer staging berth, behind a seawall, with no
ordinary boat landing. Reaching the staging berth alone cannot reach the leader.

The service platform in B is reached by securing cargo at its HIGH berth.
It has a dry B/C pump and a maintenance winch on a lower ledge. Drain B below
HIGH to expose that winch, release the final mooring chain, then refill B HIGH
so the boat bridge lines up for the return. This is an intentional reversal.

Next move cargo to C's outer staging berth. Drain C to LOW to expose the shore
and walk back to the control quay while leaving cargo in place. Redistribute
water through C's labeled A/B and B/C manifold until A LOW, B HIGH, C HIGH.
Secure cargo from the control quay. The final bridge aligns B's upper service
berth with the captain deck. The launch left at C is the way back to B.

Control pairs: A west/inner A-B, B west B-C, C control A-B and B-C, C outer
B-C, and isolated service platform B-C. These need visibly labeled valves and
traceable pipe colors. Recovery ledges: A LOW connects A west/inner; B's raised
stairs connect its quays; C LOW connects C control/outer; matching A/B MID and
B/C MID each align a maintenance boardwalk. The JSON lists boarding heights.

Double battles punctuate access to new sections but are excluded from the
solver so they cannot disguise a shallow machinery puzzle. Their exact positions
are not fixed in this draft. A machinery reset restores water, both boats,
moorings and the maintenance chain to the start. Trainer victories and the
Havora Crest remain saved independently. No reset is required to recover in
this abstract model.

## What was actually checked

The solver exhaustively explores 837 reachable states. All 837 have a natural
path to the captain. Its shortest route is 25 decision actions, including ten
water transfers, excluding walking distance and battles. Removing cargo travel,
A/B transfers, the LOW shore at C, launch reuse from C, or the maintenance
release makes the puzzle unsolvable. These are real dependencies in this model.

Counts alone do not prove expert difficulty. Pixel layout, event reach, collision,
boating shortcuts, feedback and human playtesting still need verification.
The mapped prototype has since passed compilation and emulator tests; see the separate implementation report.

Run: `python tools/havora/solve_fixed_transfer_design.py`.
The PNG is a functional/height study, not finished FireRed artwork.

## Shortest solution (spoilers)

| Action | Decision | A / B / C after action |
|---|---|---|
| 1 | Ride launch to B west quay | HIGH / HIGH / LOW |
| 2 | Transfer B > C at B west quay | HIGH / MID / MID |
| 3 | Ride launch to C control quay | HIGH / MID / MID |
| 4 | Ride cargo to B west quay | HIGH / MID / MID |
| 5 | Transfer C > B at B west quay | HIGH / HIGH / LOW |
| 6 | Ride cargo to B upper service berth | HIGH / HIGH / LOW |
| 7 | Secure cargo boat as service bridge | HIGH / HIGH / LOW |
| 8 | Walk to Service platform | HIGH / HIGH / LOW |
| 9 | Transfer B > C at Service platform | HIGH / MID / MID |
| 10 | Release captain-islet mooring chain | HIGH / MID / MID |
| 11 | Transfer C > B at Service platform | HIGH / HIGH / LOW |
| 12 | Walk to B upper service berth | HIGH / HIGH / LOW |
| 13 | Release cargo boat from service bridge | HIGH / HIGH / LOW |
| 14 | Ride cargo to B west quay | HIGH / HIGH / LOW |
| 15 | Transfer B > C at B west quay | HIGH / MID / MID |
| 16 | Ride cargo to C outer mooring | HIGH / MID / MID |
| 17 | Transfer C > B at C outer mooring | HIGH / HIGH / LOW |
| 18 | Walk to C control quay | HIGH / HIGH / LOW |
| 19 | Transfer B > C at C control quay | HIGH / MID / MID |
| 20 | Transfer A > B at C control quay | MID / HIGH / MID |
| 21 | Transfer B > C at C control quay | MID / MID / HIGH |
| 22 | Transfer A > B at C control quay | LOW / HIGH / HIGH |
| 23 | Tension cargo boat as final bridge from control quay | LOW / HIGH / HIGH |
| 24 | Ride launch to B upper service berth | LOW / HIGH / HIGH |
| 25 | Walk to Captain deck | LOW / HIGH / HIGH |
