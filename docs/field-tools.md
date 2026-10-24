# QOL field tools

The seven supported HM field actions now use reusable Key Items. They require
ownership and the same badges as before, with no move/party/species requirement.
The battle moves remain available and can be forgotten normally.

| Action | Key Item | Badge | Acquisition |
| --- | --- | --- | --- |
| Cut | Pruning Shears | Cascade | S.S. Anne captain |
| Fly | Sky Whistle | Thunder | Route 16 house |
| Surf | Wailmer Wailer | Soul | Safari Zone Secret House |
| Strength | Power Gloves | Rainbow | Return the Warden's Gold Teeth |
| Flash | Lantern | Boulder | Route 2 aide, ten caught/owned species |
| Rock Smash | Rock Hammer | Marsh | Celadon Department Store, 4F |
| Waterfall | Basculegion Bait | Volcano | Celadon Department Store, 4F |

Press A at trees, boulders, cracked rocks, water edges and waterfalls for the
corresponding Yes/No prompt. Lantern and Sky Whistle work from Key Items or the
registered-item wheel. The tablet's native map also offers whistle travel when
available. All tools can be registered; invalid locations show a message.

Cut also trims grass when used directly. Gloves remain active for the map using
the original Strength state. The Wailmer Wailer calls a sea Pokémon using a round, blue
Wailmer-shaped flute icon. Boarding, water movement, dismounting and encounters retain native
Surf behavior, including the original riding sprite.
The whistle uses native Fly destinations, visited-location restrictions and the
existing bird transport. Bait is reusable and uses native waterfall movement.
The field-move cut-in shows the appropriate item icon at twice its Bag size,
centered in the banner, instead of a Pokémon and
plays an item sound instead of a cry. Pokémon field-move summon poses are skipped
for Cut, Strength, Rock Smash and Lantern.

Item art uses native 24×24 indexed sprites with a transparent outer margin and
an individual 16-entry palette per tool (15 opaque colors plus transparency).
`tools/render_field_tools.py` imports the seven designs approved on October 24,
2026 and reproduces the PNGs and JASC palettes. The unmodified RGB uploads are
preserved in `tools/field_tool_sources`. The importer removes their baked-in
checkerboards, fits their silhouettes inside a 22×22 area and quantizes each
to 15 foreground colors at GBA RGB555 precision without dithering. Fine emblem,
cord and finger-hole details are reduced at the native item-icon resolution.
The set uses green-handled shears, gold reinforced gloves, a dark flame lantern,
a Corviknight-themed Sky Whistle, a blue Wailmer ocarina, a gold-ended hammer
and a red-and-cream Basculegion bait pouch.

Original HM item IDs, gift flags and save structures are unchanged. Existing HM
inventory moves from the TM Case to Key Items on Continue or opening the Bag.
If the pocket is full, the old entry is retained and continues to authorize field
interactions. Opening the Bag retries migration after space becomes available.
Deferred entries are hidden from the TM Case until recovery.
Repeated grants/migration do not duplicate tools. Existing learned moves remain
on Pokémon; HM entries no longer appear in the TM Case or as Party field actions.
Unused Dive has no overworld functionality in this campaign.

The party/box last-usable-Pokémon, Egg, Mail and held-item release protections
remain. The obsolete requirement to retain a sole HM user is removed.

Validation: `tests/field_tools_emulator.py` runs against the built ROM with a party
knowing only Tackle. It covers gates, Key Item identity, repeat grants, migration,
full pockets, TM Case filtering, all seven actions, item banners, Bag/Select use,
actual flash saving and automatic migration on Continue. Waterfall uses a temporary
RAM fixture because the retained Kanto maps have no waterfalls. Seven existing
regressions also pass: title, tablet transitions, Party text, storage visuals,
release safety, storage actions and story rewards/League access.
The regular QOL runner includes the tool check.

Acquisition audit: `tests/field_tool_rewards_emulator.py` runs the complete five
retained NPC reward conversations, checking full-pocket refusal, retry, reward
flags, one-copy ownership and the Warden's Gold Teeth consumption. The captain
and Warden now check Key Item space before marking their gifts complete. The
aide still requires ten caught/owned species; ten merely seen or nine caught
do not qualify. HM06's Ember Spa gift and HM07's Icefall Cave pickup were retired
with those Sevii maps during the ROM cleanup. Their replacement items are tested
through actual purchases at Celadon Department Store 4F, at zero cost.
