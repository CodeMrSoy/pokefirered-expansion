# Vidra native map drafts

These are real FireRed map headers, metatile/collision binaries and registered
layouts. Open the project root in Porymap, then the **VidraDrafts** map group.
The separate group keeps existing maps, IDs and unfinished city work intact.

Enter the forest by walking north beyond the final gate in Havora's existing
counterweight grove (NorthQuadrant, 10,10). The exit inside the forest returns
to the gate approach at 10,12. The original maze and its puzzle logic are intact.

| Editable map | Size | Purpose |
|---|---:|---|
| VidraDraft_WesternForest | 88 × 80 | Large looping forest, two destination branches and optional dead ends |
| VidraDraft_CorvalaPassage | 56 × 48 | Two-ended cave: forest ↔ Corvala only |
| VidraDraft_RainfallRoute | 56 × 72 | Rain, three waterfall curtains, stairs and three walking bridges |
| VidraDraft_Veyden | 56 × 48 | Forest settlement with south, east and north exits |
| VidraDraft_LakewoodRoute | 64 × 40 | Woodland-to-lakeside route to Lyrvik |
| VidraDraft_Lyrvik | 56 × 48 | Lakeside settlement with piers |
| VidraDraft_HighlandAscent | 56 × 72 | Forest switchbacks and gradual patches of native winter terrain |
| VidraDraft_Norvyn | 56 × 48 | Snowy terraced settlement |
| VidraDraft_Corvala | 64 × 64 | Static copy of Corvala-dev's existing authored LOW map |

Outdoor connections are reciprocal, with aligned walking seams. The forest and
cave use real warp events. Corvala has no direct connection to the waterfall
route or Veyden. Veyden connects independently to Lyrvik and Norvyn.

The new towns use native building footprints as placeholders. Inspecting their
doors explains that interiors are pending. No new gyms, trainers, encounters,
quests or progression gates have been invented. Rain and snow use the engine's
weather; waterfall curtains are static draft artwork borrowed from Havora's
existing native tiles. Highland snow uses GeneralWinter art alongside green
General terrain in a dedicated secondary tileset.

Corvala is copied from `Corvala-dev` commit
`f9cee13458cc5e80ab2e0e6611ad7010a05596c3`. Its original map and branch are
unchanged; this copy does not import its tide engine or scripts. The existing
cave mouth is temporarily the passage endpoint for layout review.

`tools/vidra_drafts/build.py` is the authoring recipe, not a build step. It
rewrites **only these draft layouts**, their headers, the draft assets, and the
one Havora entrance trigger when explicitly run. Backport Porymap changes to
the recipe before regenerating. A normal `make` preserves manual Porymap edits.
The manifest records review coordinates and rendered native-map previews.

Run `python tests/vidra_draft_maps.py` for dimensions, map IDs, collision and
elevation paths, cave behaviors, reciprocal connections and aligned seams.
Run `python tests/vidra_draft_emulator.py` against a built ROM and an mGBA
libretro core for actual walking transitions and map screenshots.
