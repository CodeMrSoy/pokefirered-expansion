# Eirik, Surf and the Gold Teeth

The intended chain is: Safari House ticket -> Havora -> find Koga -> beat Koga
for the Soul Badge and beat Eirik for the Wailmer Wailer -> Surf for the Gold
Teeth -> return them to the Warden for Power Gloves -> use Strength in the
existing boulder maze before Eldervik Woods. Koga and Eirik may be beaten in
either order; Surf requires both the tool and Soul Badge. Strength still
requires Erika's Rainbow Badge and Power Gloves.

Route 2's aide now awards the Lantern for ten species seen across the national
Pokédex. Caught/owned count is irrelevant. All request, success, refusal and
insufficient-count text refers to seeing species. Other aides are unchanged.

The original Safari Secret House attendant gives advice about Eirik and Surf,
without granting a Wailer or setting its reward flag. The Stellar Ticket
traveler and his gift remain unchanged.

Eirik gives the Wailer after his victory and Havora Crest award. The ordinary
post-victory conversation also gives an unclaimed reward, including completed
legacy gym saves. A full Bag without a Field Item Case leaves the reward
claimable; a preexisting case needs no extra slot. Ownership is checked before
any gift, preserving existing tools and avoiding duplicates. `FLAG_GOT_HM03`
records success; no save layout or item IDs change. The gym script generator
preserves this reward on regeneration.

Safari Zone West now has a six-tile island at x10-12, y17-18 in its existing
pond. The Gold Teeth item is at (11,17), with its original pickup flag and item
script. Water separates the island from every land entrance, with room to land
and return to shore. The Secret House remains reachable without Surf, so the
player can obtain the ferry ticket first. The Warden's normal teeth exchange
and the existing maze geometry are unchanged. Existing saves that already own
tools or have collected the teeth retain their progress.

Verification:

- Standard FireRed build.
- `eirik_surf_progression_emulator.py`: nine seen rejected; ten seen and zero
  caught accepted, including non-Kanto species; full Bag and repeat gifts;
  Safari attendant has no Surf gift; incomplete Eirik trial gives no reward;
  victory/full-Bag/retry flow; actual Surf crossing, dismount, teeth pickup,
  safe return and Warden exchange; flash save/reload; dialogue width checks.
- `havora_no_surf_route_emulator.py`: all 30 current puzzle actions with normal
  walking and real boat travel, no Surf ownership or use, all stations visited
  and captain readiness reached. Crew victories are fixtures, not combat tests.
- Existing directional solver and gym graph/map audit pass without changing
  gym geometry or puzzle controls. Current NPC reward regressions also pass.
