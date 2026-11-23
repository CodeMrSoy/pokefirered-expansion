"""An isolated test region seeded from native identities and facility names."""

from copy import deepcopy
import json
from pathlib import Path

from world_rules import CENTERS, KANTO_GYMS, MARTS

TOWNS = ("ViridianCity", "PewterCity", "CeruleanCity")
ITEMS = ("POTION", "ANTIDOTE", "POKE_BALL")
SKILLS = ("retail", "research", "training")
CASES = ("ordinary", "shortage", "employment", "cooperation", "relocation", "event")
# Each identity maps to an authored object in the Phase 15 census. Services
# remain anchored to native locations. The trial economy is host-only.
IDENTITIES = Path(__file__).resolve().parents[1] / "kanto" / "identities.json"


def region(seed=16, case="ordinary"):
    if type(seed) is not int or case not in CASES:
        raise ValueError("invalid_region")
    world = dict(version=1, seed=seed, case=case, tick=0, revision=0, people={},
                 locations={}, routes={}, firms={}, pokemon={}, requests={},
                 events={}, pending=[], wake={}, requirements={}, issued_money=0)
    census = json.loads(IDENTITIES.read_text(encoding="utf-8"))
    used = set()

    def place(key, town, kind, **fields):
        world["locations"][key] = dict(town=town, kind=kind, accessible=True,
                                        owner=None, capacity=0, **fields)

    def connect(a, b, hours, required=True):
        world["routes"][f"{a}|{b}"] = dict(a=a, b=b, hours=hours, open=True, required=required)

    for town in TOWNS:
        place(town, town, "town")
        guest = f"{town}:guest-house"
        place(guest, town, "home")
        world["locations"][guest].update(capacity=1, rent=5)
        connect(town, guest, 1, required=False)
        center = town + "_PokemonCenter_1F"
        assert town in CENTERS
        mart = MARTS[town]
        gym = town + "_Gym"
        assert town in KANTO_GYMS.values()
        for key, kind in ((center, "healing"), (mart, "shopping"), (gym, "gym")):
            place(key, town, kind)
            connect(town, key, 1)
        world["requirements"][town] = dict(healing=center, shopping=mart, gym=gym)
        residents = []
        for source, obj in sorted(census.items()):
            map_id = source.split("/")[0]
            if "id" not in obj:
                continue
            if (map_id == town or map_id.startswith(town + "_")) and obj["id"] not in used:
                if obj.get("role") in {"gym_leader", "story", "rival"} or obj["id"] in KANTO_GYMS:
                    continue
                residents.append((source, obj))
                used.add(obj["id"])
            if len(residents) == 8:
                break
        for i in range(len(residents), 8):
            residents.append((None, {"id": f"{town}-resident-{i}", "role": "resident"}))
        for i, (source, obj) in enumerate(residents):
            actor = obj["id"]
            home = f"{town}:home:{i // 2}"
            if home not in world["locations"]:
                place(home, town, "home")
                world["locations"][home].update(capacity=2, rent=3)
                connect(town, home, 1, required=False)
            person = dict(name=obj.get("name", actor.replace("_", " ")), native=source,
                          traits=[("practical", "curious", "patient", "independent")[i % 4]],
                          location=mart if i < 4 else town, home=home, money=30 + i,
                          goods={"POTION": 1} if i % 2 else {}, skills={"retail": 1} if i < 3 else {},
                          employer=None, energy=5, transit=None, goal=None, plan=[],
                          known={}, relationships={}, memories=[], controller="npc", ready=0)
            world["people"][actor] = person
            if i % 2:
                peer = residents[i - 1][1]["id"]
                person["relationships"][peer] = 1
                world["people"][peer]["relationships"][actor] = 1
            if i < 2:
                person["employer"] = mart
            if i == 0:
                owner = actor
        world["firms"][mart] = dict(name=mart, location=mart, owner=owner, kind="business",
                                    money=100, goods={item: 8 for item in ITEMS},
                                    prices=dict(zip(ITEMS, (5, 4, 6))), wage=5, jobs=3,
                                    skill="retail", members=[], floor={item: 1 for item in ITEMS})
        world["locations"][mart]["owner"] = owner
        world["locations"][guest]["owner"] = owner
        world["locations"][guest]["sale_price"] = 20
        world["pokemon"][f"{town}:partner"] = dict(species="PIDGEY", owner=owner, practice=0)
    museum = "PewterCity_Museum_1F"
    place(museum, "PewterCity", "workplace")
    connect("PewterCity", museum, 1)
    world["firms"][museum] = dict(name="Pewter Museum", location=museum, owner="society_researcher",
                                  kind="business", money=70, goods={}, prices={},
                                  wage=7, jobs=2, skill="research", members=[], floor={})
    world["people"]["society_researcher"]["skills"]["research"] = 2
    world["people"]["society_researcher"]["employer"] = museum
    connect(*TOWNS[:2], 3)
    connect(*TOWNS[1:], 4)
    connect(TOWNS[0], TOWNS[2], 9, required=False)
    # Case interventions adjust starting conditions and never select a reaction.
    pewter = MARTS["PewterCity"]
    people = [key for key, p in world["people"].items() if p["location"] == pewter]
    lead, peer = people[2:4]
    world["focus"] = [lead, peer]
    world["people"][lead]["location"] = pewter
    if case == "shortage":
        world["firms"][pewter]["goods"]["POTION"] = 1
        world["people"][lead]["goods"].pop("POTION", None)
    elif case == "employment":
        world["people"][lead]["money"] = 0
    elif case == "cooperation":
        world["people"][lead]["skills"].clear()
        world["people"][peer]["skills"]["retail"] = 2
        world["people"][lead]["money"] = 0
    elif case == "relocation":
        # A vacant bed elsewhere and a co-tenant who takes the lead's former lease.
        home = world["people"][lead]["home"]
        world["people"][lead]["home"] = None
        assert world["locations"][home]["capacity"] > 1
        world["locations"][home].update(rent=25, owner=peer)
        world["people"][lead]["location"] = "PewterCity"
        world["people"][lead]["money"] = 15
    elif case == "event":
        world["people"][lead]["location"] = TOWNS[0]
        world["people"][peer]["location"] = TOWNS[0]
    player = deepcopy(world["people"][lead])
    player.update(name="Visiting trainer", native=None, controller="player", home=None,
                  skills={}, goods={}, relationships={}, money=20)
    world["people"]["player"] = player
    world["issued_money"] = sum(p["money"] for p in world["people"].values()) + sum(
        f["money"] for f in world["firms"].values())
    return world
