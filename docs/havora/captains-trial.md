# Havora Captain’s Trial: first playable interior

A dedicated 40×36 boathouse replaces only the QuantumHavoraGym Pewter placeholder. The three exit warp indices and their exterior destination remain intact; exterior maps, painstaking cliffs, events, tileset files, and connection offsets are unchanged.

## Native artwork

The private primary/secondary pair uses Havora’s existing Pacifidlog-style wood, boat and animated water. Thirty-five 8×8 graphics are imported unchanged from FireRed’s S.S. Anne: wall panels, portholes, charts, chairs, bookcases, plants, life rings and machinery. No generated or redrawn pixels are used. Colored control faces are recombined over wooden floors. Primary graphics are private; secondary graphics share the existing compressed city sheet. Only gym metatiles/palettes change, so no city graphics slots are consumed. Unused city metatiles are omitted from the gym editor catalog.

## Playable route

1. Red winch lowers the entrance gangway. Board the launch from the lower west landing.
2. Ride east; defeat the dock crew in doubles to obtain lock clearance.
3. With the launch in the eastern lock, the blue control raises it to the upper berth. The control reports LOW/HIGH water before confirming.
4. Ride west at high water. Defeat the navigator in doubles, then lower the captain’s gangway with the yellow control.
5. Defeat Captain Eirik in doubles. Harbor Crest progress is saved and the starboard return gangways open.

The launch moves along fixed scripted routes while player input is locked; empty launches can be called from the matching landing. An animated lock transfer moves the vessel between lower and upper berths. Industrial basin water is impassable to personal Surf, so the puzzle cannot be bypassed. Boat pixels render below the passenger. The green reset bell restores the puzzle but retains defeated trainers and Crest progress. Re-entry and battle-return scripts reconstruct the saved configuration.

## State and teams

Two previously-unused variables: 0x40D7 (boat side, water level and gangways) and 0x40D8 (crew, navigator and Crest progress). Three new trainer IDs 743–745 stay below the existing 768 capacity; no save-block expansion. All three use native four-battler doubles. First-pass levels are 49–54, with Machoke/Pelipper, Lanturn/Skarmory, and the captain’s Pelipper/Magnezone/Machamp/Kingdra. Team balance is provisional. The Crest is presently a persistent story achievement; it is not an inventory item or a new Trainer Card badge icon.

## Verification

- Development ROM compiled: 21,621,596 bytes, 64.44% of 32 MiB. Approximately 39 KiB added versus the prior Havora build; static EWRAM usage unchanged at 258,376 bytes.
- Independent graph audit: 48 reachable puzzle states, leader and exit reachable, every state can return to the entrance/reset. All original outdoor layouts, cliff art, events, warps, connections and tilesets preserved.
- mGBA: low/high passenger rides, lock transfer, crew/navigator requirements, re-entry state, reset retaining progress, return shortcut, real Yes/No winch interaction, actual exterior exit, and native four-battler launches for all three trainers.
- Puzzle route test sets the battle-result progress variables to isolate mechanics. Battles were launched in the emulator; complete combat balance and reward presentation still need player testing.

`review/captains-trial.png` is a native tile-and-NPC rendering with reference labels. Emulator captures are in build/havora-tests. No Porymap UI walkthrough is claimed.
