"""Early-Kanto identities and grounded dialogue on the read-only catalog."""

from contextlib import closing
from functools import lru_cache
import json
import sqlite3

# These mailbox IDs authorize dialogue at individual authored script hooks.
HOOKS = {
    20: "viridianforest/boy",
    21: "route3/youngster",
    22: "mtmoon_1f/baldingman",
    23: "route4/boy",
    24: "ceruleancity/baldingman",
    25: "route25/man",
}
AREAS = {
    9: "viridian_forest", 10: "route_3", 11: "mt_moon", 12: "route_4",
    13: "cerulean", 14: "route_24", 15: "route_25", 16: "cerulean_gym", 17: "sea_cottage",
    18: "pallet_home", 19: "viridian_inside", 20: "route_2_inside", 21: "pewter_inside",
    22: "route_4_center", 23: "cerulean_inside", 24: "cerulean_cave", 25: "link_service",
}
DISTRICTS = {
    "pallet": "PalletTown", "rival_house": "PalletTown_RivalsHouse",
    "oak_lab": "PalletTown_ProfessorOaksLab", "route_1": "Route1",
    "viridian": "ViridianCity", "pewter": "PewterCity", "pewter_gym": "PewterCity_Gym",
    "route_2": "Route2", "viridian_forest": "ViridianForest", "route_3": "Route3",
    "mt_moon": "MtMoon", "route_4": "Route4", "cerulean": "CeruleanCity",
    "route_24": "Route24", "route_25": "Route25", "cerulean_gym": "CeruleanCity_Gym",
    "sea_cottage": "Route25_SeaCottage",
    "pallet_home": "PalletTown_PlayersHouse", "viridian_inside": "ViridianCity",
    "route_2_inside": "Route2", "pewter_inside": "PewterCity", "route_4_center": "Route4_PokemonCenter",
    "cerulean_inside": "CeruleanCity", "cerulean_cave": "CeruleanCave",
    "union_room": "UnionRoom", "trade_center": "TradeCenter",
}

# Dialogue voice and local topics. The world state supplies any recall or
# secondhand information. These lines never introduce state or grant access.
VOICE = {
    "viridianforest/boy": ("I count my supplies now.", "I'm making a packing list."),
    "route3/youngster": ("I like a good rest stop.", "I'm pacing myself today."),
    "mtmoon_1f/baldingman": ("I look down as I walk.", "Slow steps work for me."),
    "route4/boy": ("I keep an eye on the paths.", "I'm comparing route notes."),
    "ceruleancity/baldingman": ("Books never tire me out.", "Time to check my notes."),
    "route25/man": ("I enjoy a quiet walk.", "I like to check the paths."),
}
# Observation of the companion can safely be used without species name input.
COMPANION = {
    "viridianforest/boy": "You two look well prepared.",
    "route3/youngster": "Keep pace with your partner.",
    "mtmoon_1f/baldingman": "Stay close to your partner.",
    "route4/boy": "Exploring with a friend?",
    "ceruleancity/baldingman": "Your partner looks curious.",
    "route25/man": "Glad you have company.",
}


class KantoCatalog:
    def __init__(self, path):
        self.uri = path.resolve().as_uri() + "?mode=ro"
        with closing(sqlite3.connect(self.uri, uri=True)) as db:
            self.available = db.execute(
                "SELECT 1 FROM sqlite_master WHERE type='table' AND name='kanto_identity'"
            ).fetchone() is not None

    @lru_cache(maxsize=64)
    def nearby(self, area):
        district = DISTRICTS.get(area)
        if area == "link_service" and self.available:
            return (*self.nearby("union_room"), *self.nearby("trade_center"))
        if not district or not self.available:
            return ()
        with closing(sqlite3.connect(self.uri, uri=True)) as db:
            rows = db.execute("""
                SELECT i.id, i.data FROM kanto_identity i
                WHERE i.home = ? OR instr(i.home, ? || '_') = 1 OR EXISTS
                  (SELECT 1 FROM kanto_appearance a
                   WHERE a.identity = i.id AND (a.map = ? OR instr(a.map, ? || '_') = 1))
                ORDER BY i.tier DESC, i.id
            """, (district,) * 4)
            return tuple((id_, json.loads(data)) for id_, data in rows)

    def profile(self, id_):
        if not self.available:
            return None
        with closing(sqlite3.connect(self.uri, uri=True)) as db:
            row = db.execute("SELECT data FROM kanto_identity WHERE id=?", (id_,)).fetchone()
        return json.loads(row[0]) if row else None

    def local_facts(self, id_):
        if not self.available:
            return ()
        with closing(sqlite3.connect(self.uri, uri=True)) as db:
            rows = db.execute("""
                SELECT f.key, f.text, f.source
                FROM kanto_fact f JOIN kanto_identity i ON i.home = f.map
                WHERE i.id = ? AND (f.role IS NULL OR f.role = json_extract(i.data, '$.role'))
                ORDER BY f.key LIMIT 4
            """, (id_,)).fetchall()
        return tuple(dict(zip(("key", "text", "source"), row)) for row in rows)


def dialogue(catalog, memory, population, context):
    if not catalog.profile(context.npc):
        return None
    praise, occupation = VOICE[context.npc]
    state = memory.snapshot(context.npc)
    actor = population.state["actors"].get(context.npc) if population else None
    if actor and actor.get("facts"):
        facts = actor["facts"]
        latest = max(facts.values(), key=lambda fact: fact["received"])
        peer = population.people[latest["source"]].name.split()[0]
        return f"{peer} helped with my notes.\nI'll check them again."
    if context.visible_species and context.visible_species == state.get("last_kanto_companion"):
        return f"You two are back.\n{occupation}"
    if context.visible_species:
        return f"{COMPANION[context.npc]}\n{praise}"
    return praise


# Each contact works with a specific colleague in the same district.
# The ROM still controls their authored positions. Using roles with existing
# Population mechanics keeps schedules, events, and checkpointing shared.
PARTNERS = (
    (20, "viridianforest/youngster", "guide", "volunteer"),
    (21, "route3/robin", "guide", "volunteer"),
    (22, "mtmoon_1f/jovan", "volunteer", "researcher"),
    (23, "route4/woman", "guide", "volunteer"),
    (24, "ceruleancity/youngster", "researcher", "volunteer"),
    (25, "route25/beauty", "guide", "volunteer"),
)


def residents(catalog):
    from population import Resident

    for number, partner, role, peer_role in PARTNERS:
        contact = HOOKS[number]
        for id_, peer, activity in ((contact, partner, role), (partner, contact, peer_role)):
            profile = catalog.profile(id_)
            if profile is None:
                raise ValueError(f"Missing Kanto profile {id_}")
            shift = profile["schedule"]["start_hour"] * 3600
            yield Resident(id_, profile["name"], activity, profile["home"], shift,
                           (6,), profile["long_goal"], profile["traits"][0], number % 3, peer)
