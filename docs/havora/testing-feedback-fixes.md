# Havora testing feedback

The nursery now uses the original Four Island two-parent interior and services,
restored from the repository's pre-Sevii-retirement history. The existing outdoor
caretaker handles compatibility and eggs. The exterior entrance is unchanged;
both directions reference the valid warp 0. The Route 5 daycare and its saved
single-parent slot remain separate; existing saved daycare data is not erased.

Counterweight Grove keeps its positions, terrain, elevations, collision and rules.
Red circles identify plate A / gate A. Blue diamonds identify plate B / gate B.
Gold triangles identify plates C and D. The forest gate carries blue and gold:
B, C and D must stay weighted, and all three pits must be filled. Six formerly
blank static graphics and nine blank metatile entries provide the markers; no
existing cliff, house, palette or water animation graphics are replaced. All
marked gates retain the sinking animation and resting log caps.

The Vermilion walking ticket triggers now complete the sailor/player facing
movements before checking for a Stellar Ticket. QOL itself has no Stellar Ticket
campaign; this fix belongs to Havora/V2's campaign script.

Verified with a development ROM build, `check_counterweight.py`, the full native
Counterweight emulator route (including animation/resource fallback and resets),
`havora_daycare_emulator.py` (normal door transitions, two parents, step-generated
egg, outdoor collection and withdrawals), and `havora_sailor_emulator.py` (both
walking triggers). No Porymap UI testing is claimed.
