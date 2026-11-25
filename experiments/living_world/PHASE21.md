# Phase 21 · Native gameplay projection

Phase 21 starts at the verified Phase 20 commit `f7b440a`. It retains the
native manifest resolver, observation ring, simulation clock, background
planner and paired Flash journal. The companion generates offers and the
ROM decides whether an offer is eligible at a gameplay boundary.

## Versioned mailbox and fallback

The linked ROM exposes one 192-byte EWRAM projection symbol. The catalog
records the linker address and validates its size. The first 188 bytes are
the fixed version-one offer and six bounded candidate rows. The ROM writes
the final address-dependent seal itself. The host checks the seal and writes
only the offer region between core frames. No dialogue or planner output
has access to this writer.

The trusted host verifies ROM and immutable manifest identity, durably
registers each revision against the world UUID, native stream and paired
Flash checkpoint, then publishes the prepared bytes. Native code checks
the current map, save counter, context generation, trainer ID, adventure
mode, randomizer seed, feature bits, difficulty, freshness and checksum.
The ROM does not store the companion UUID, so the full checkpoint and
world identities are checked at attachment and acceptance in the host.
The bounded checksum detects corruption. The protocol does not assume a
malicious replacement of the entire application or emulator.

Offers age out after 120 native frames without a heartbeat. The host
refreshes a cached offer at most once per 35 frames and stops refreshing
if its journal worker has not confirmed current state within a simulation
hour. A new save mutes publication until its paired checkpoint settles.
Map changes and detected external state resets invalidate the attachment
or the offer. The emulator never waits for the worker. A rejected candidate
leaves the authored path available. When a roster or rare spawn is accepted,
native copies of the instantiated Pokémon survive subsequent offer updates.

## Sammy pilot and reconciliation

Only trainer 104 on the compiled Viridian Forest map may receive a team.
Only ordinary single trainer battles are eligible. The companion provides
up to two ready party members and clamps levels to 9 and the current native
cap. There are no projected held items. The ROM validates the exact resolved
ability slot and checks moves against its own current effective level-up
learnset before creating any opponent. When a clamped or evolved Pokémon no
longer has legal moves at this pilot level, that candidate is omitted.
Personality and fixed IV handling are deterministic projection presentation
choices and do not claim previously observed genetic attributes.

Sammy's class AI, dialogue scripts, rewards and defeat flag are native.
The observation stream associates confirmed native slots with companion IDs
and records the accepted revision, final HP and confirmed participation.
Wounded members need one day of recovery and fainted members need two.
Confirmed participation contributes to companion trainer experience. The
opponent's native battle result awards no extra companion Pokémon levels
or native rewards. Defeated Pokémon remain alive. Duplicate journal events
are idempotent. Sammy is absent from the native Vs. Seeker rematch table,
so his authored defeat flag continues to govern repeat interactions.

Sammy's native post-battle aside can retrieve verified local activity
through the existing dialogue validator. The aside requires the real
forest map, Pokédex and native defeat flag.

## Land and named wild pilot

Only ordinary grass step encounters on Routes 24 and 25 can consult an
offer. The compiled reciprocal ecology corridor and native variant mask
must be present. Surfing, fishing, scripted encounters, static encounters,
DexNav, Sweet Scent, roamers, Safari, doubles and type-attraction selections
retain their native paths. The native encounter rate, level roll, repel and
first-encounter checks still run. There is always an authored fallback.

At most 20 percent of eligible native spawns consult the overlay. A
local copy of the native RNG state supplies the extra selection value
without advancing the global RNG cursor. Eligible species weights use
three times the integer square root of local abundance, capped at 20.
The offer includes up to two compatible migrant species and four locally
supported species. Local candidates are present across applicable native
variants. A migrant must have passed the simulation's corridor checks.
Protected, disabled, unstable forms and Unown are excluded. Low simulated
populations cannot eliminate the native encounter table or change levels.

One named individual can be leased on the current pilot map. It adds
weight four and is eligible only when the native level roll matches its
recorded level. The ROM instantiates it with stable personality and IV
values, using the native player's OT from the start so the standard
capture handoff preserves the encrypted Pokémon record. The native engine still computes stats and handles combat, bag
restrictions and capture. A lease keeps companion trainers from taking the
same individual. A verified capture aliases the player's observed native
identity to the one existing companion ID and removes the wild resident
once. Escape, defeat or an unsuccessful handoff release the lease with a
same-day cooldown. A map leave or a new paired session releases stale
leases. On Route 25, a recent local survey can give the resident an
attributed report about the same reserved individual. Battle input validation, history and aliases use the same paired
database. Missing or incompatible companion checkpoints leave native saves
playable. The preview requires a matching ROM build and does not silently
upgrade Phase 20 companion databases to the new linked binary.

## Playtest the Windows preview

Extract the complete ZIP. Open **Open Pokemon Quantum.cmd**. The launcher
has **Sammy native battle demo** and **Route 24 ecology demo** buttons. Each
uses its own persistent disposable profile. These saves deliberately
accelerate companion days and supply a prepared native party. Captures,
training and corridor populations in their databases were produced by the
real simulator.

- Sammy demo. Select Continue in Viridian Forest. From the prepared tile,
  face north and interact with Bug Catcher Sammy.
  Battle as usual. The Monitor shows the offered roster, accepted native
  revision, companion identities and condition after the battle. Talk to
  Sammy again for his post-battle response.
- Route 24 demo. Select Continue and walk in the grass by Nugget Bridge.
  Ordinary native spawns still occur. The Monitor distinguishes an offer,
  a named reservation and native acceptance. The named Pokémon is
  deliberately rare. Catch it with a supplied ball or run away, then check
  the native outcome and reservation. Save normally and use Continue to
  inspect the restored outcome.
- Choose **Living World Monitor** after starting either demo. Use **Play
  Pokemon Quantum** for the regular profile. Normal saves are separate
  from both prepared profiles.

The native test harness uses the ordinary land entry point and actual
battle controls. The disposable wild capture scenario turns off Nuzlocke
at New Game so prior exploratory escapes do not consume the capture
opportunity. Normal saves keep their own settings. Windows CI uses the
extracted package, checks its hashes and bundled offline worker, and
attaches the native paired demos. Native Linux regression covers the actual
capture path and protected battles. Windows displayed frame pacing on
physical hardware is a separate manual check.
