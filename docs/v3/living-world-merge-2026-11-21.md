# V3 into Living World — 2026-11-21

Destination baseline: `ab999fdb3be5cb629f85cd90d38551debb324d11` on
`Living-Quantum-World`. Incoming V3: `0dedb6d798f6fb5968111817a80b865028112acb`.
The integration uses a normal merge with both histories retained. V3 and V2
are not advanced by this operation.

## Resolution

Only `PalletTown_ProfessorOaksLab/scripts.inc` required a manual content merge.
The first aide retains his original dialogue and Living World aside, then
continues into the Field Notes offer. His Fame Checker/postgame dialogue also
retains access to that offer. Other Living World NPC scripts, Brock's bounded
Pewter travel, host routines, memory, mailbox and model/runtime code are retained.

The initial combined tests caught a carried-over A press after the optional
aside: advancing dialogue could immediately accept the next quest offer.
Offer input now waits for A/B release, requiring a fresh player choice. This
also applies when reopening an offer from Quest Book. The quest regression
checks that the offer remains Available before the deliberate decline.

Quest Book uses V3's reserved SaveBlock2 bytes, without enlarging either save
block. Living World's bridge and presence structures remain in runtime EWRAM;
its host-managed records are outside these guest save bytes. Existing dialogue
permissions are unchanged. The scripted Quest Book registry and existing
host-managed objectives keep their current separate progression paths.

## Executed verification

The combined ROM compiles with the standard native ARM build. Its linked
footprint is EWRAM 239,172 / 262,144 bytes; IWRAM 27,573 / 32,768 bytes; ROM
21,928,264 / 33,554,432 bytes, padded to 32 MiB.

- Living World bridge emulator checks passed in Classic and Quantum, covering
  Pallet asides, validated replies, timeouts and protected original branches.
- Brock's emulator checks passed in both modes: home/absence, clues, travel
  checkpoint, safe contact, original challenge and award continuation.
- The V3 Bag/Quest Book QC passed in both fresh modes: 52 repeated app visits,
  stable heap/sprite cleanup, field controls and day/evening/night/rain palettes.
- Actual aide offer/decline/accept, Route 1 objective, reporting, exactly-once
  rewards and Flash save/reset/Continue checks passed with the combined script.
- All 656 Bag-grid descriptions fit one page with clear pixel gutters, and
  selected item graphics matched actual OBJ VRAM after pocket switches.
- Full 42/30/27-stack Bag checks passed, including every page, sort, reorder in
  both directions, cross-page cancellation, insertion at the end and tossing.
- Host-only knowledge, social memory, hybrid invalidation, routines and the
  seeded World Director checks passed. The director replay covers 120 seeds.

These are targeted merge checks, not full campaign completion or a native
Windows playtest. Deterministic host responders were used for emulator checks;
actual model inference was not re-benchmarked. Existing Windows download ZIPs
are not changed by a Git merge. Any rebuilt Windows package must pair this ROM
with metadata derived from its matching ELF, as `package-windows.py` does.
