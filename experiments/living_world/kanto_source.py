"""Generate early-Kanto census records from ROM sources and reviewed identity aliases."""

from collections import defaultdict
from hashlib import sha256
import json
import re

from profiles import PROFILES

MAP_SCOPE = re.compile(
    r"^(?:PalletTown|Route(?:1|2|3|4|24|25)|ViridianCity|ViridianForest|PewterCity|"
    r"MtMoon|CeruleanCity|CeruleanCave|DiglettsCave_NorthEntrance|TradeCenter|UnionRoom)(?:_|$)"
)
PROPS = frozenset(("ITEM_BALL", "FOSSIL", "CUT_TREE", "POKEDEX", "TOWN_MAP", "OLD_AMBER", "CLIPBOARD"))
POKEMON = frozenset(("SPEAROW", "SLOWBRO", "NIDORAN_M", "JIGGLYPUFF"))
ROLE_GRAPHICS = {
    "NURSE": "nurse", "CLERK": "merchant", "SCIENTIST": "researcher",
    "GYM_GUY": "guide", "CABLE_CLUB_RECEPTIONIST": "attendant",
    "UNION_ROOM_RECEPTIONIST": "attendant", "MG_DELIVERYMAN": "attendant",
    "POLICEMAN": "guard", "ROCKET_M": "criminal", "ROCKET_F": "criminal",
}
# Fictional character design, separate from authored roles and sourced facts.
ARCHETYPES = {
    "resident": ("neighborly", "local traditions", "visit neighbors", "keep neighborhood ties"),
    "researcher": ("inquisitive", "taking careful notes", "verify an observation", "keep useful records"),
    "trainer": ("determined", "practice battles", "review the last practice", "become a better Trainer"),
    "gym_leader": ("disciplined", "team training", "prepare the Gym team", "serve challengers"),
    "guide": ("observant", "local paths", "review local directions", "help travelers find their way"),
    "merchant": ("practical", "equipment", "check the counter", "serve local Trainers"),
    "nurse": ("patient", "Pokemon care", "prepare the service desk", "care for visiting teams"),
    "caregiver": ("attentive", "Pokemon care", "check on visiting Pokemon", "keep Pokemon comfortable"),
    "technician": ("methodical", "PC technology", "check the equipment", "maintain the town's computers"),
    "student": ("curious", "local Pokemon", "review today's notes", "learn about nearby habitats"),
    "attendant": ("punctual", "keeping appointments", "prepare the service desk", "keep service available"),
    "guard": ("alert", "local conditions", "check the assigned post", "keep the area safe"),
    "criminal": ("guarded", "their own plans", "stay at the assigned post", "fulfill their orders"),
}
GIVEN = ("Ari", "Cora", "Dara", "Emi", "Fern", "Galen", "Hana", "Iona", "Jori", "Kiri",
         "Lio", "Mara", "Neri", "Oren", "Pia", "Quill", "Reed", "Sera", "Tavi", "Vela")
FAMILY = ("Alder", "Bay", "Briar", "Cove", "Elm", "Fern", "Gale", "Hart", "Linden",
          "Marsh", "Moss", "Reed", "Rowan", "Rush", "Vale", "Wren")
FAMILY_TIES = {"oak": ("blue", "daisy"), "blue": ("oak", "daisy"), "daisy": ("oak", "blue")}
LABEL = re.compile(r"^(\w+)::?\s*(?:@.*)?$", re.M)
FLAG = re.compile(r"\b(?:FLAG_[A-Z0-9_]+|VAR_MAP_SCENE_[A-Z0-9_]+)\b")
BATTLE = re.compile(r"^\s*(?:trainerbattle\w*|settrainerflag|checktrainerflag)\s+"
                    r"[^\n@]*?\b(TRAINER_[A-Z0-9_]+)\b", re.M)
COMMAND = re.compile(r"^\s*((?:goto|call)(?:_\w+)?)\s+([^\n@]+)", re.M)
CONTINUATION = re.compile(r"^\s*trainerbattle\w*\s+([^\n@]+)", re.M)


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def scripts(root, maps):
    index = {}
    for path in [root / "data/event_scripts.s", *sorted((root / "data/scripts").glob("*.inc")),
                 *(root / "data/maps" / name / "scripts.inc" for name in maps)]:
        if not path.is_file():
            continue
        source = path.read_text(encoding="utf-8")
        labels = list(LABEL.finditer(source))
        for i, match in enumerate(labels):
            end = labels[i + 1].start() if i + 1 < len(labels) else len(source)
            index[match[1]] = (source[match.end():end], path.relative_to(root).as_posix())
    return index


def inspect_script(labels, entry):
    visited = set()
    stack = [entry]
    while stack:
        key = stack.pop()
        if key in visited or key not in labels:
            continue
        visited.add(key)
        body, _ = labels[key]
        for _, args in COMMAND.findall(body):
            branch = args.rsplit(",", 1)[-1].strip()
            if branch in labels:
                stack.append(branch)
        for args in CONTINUATION.findall(body):
            stack.extend(label for field in args.split(",") if "_EventScript_" in (label := field.strip())
                         and label in labels)
    words = "\n".join(labels[key][0] for key in sorted(visited))
    return {
        "scripts": sorted(f"{labels[key][1]}#{key}" for key in visited),
        "story_conditions": sorted(set(FLAG.findall(words)) - {"FLAG_TEMP_1", "FLAG_TEMP_2"}),
        "trainers": sorted(set(BATTLE.findall(words))),
        "effects": sorted(set(re.findall(
            r"^\s*(giveitem\w*|givemon\w*|pokemart\w*|setflag|clearflag|warp\w*|"
            r"trainerbattle\w*|special|specialvar|famechecker|setobject\w*|removeobject)\b", words, re.M))),
    }


def trainer_metadata(root):
    source = (root / "src/data/trainers.h").read_text(encoding="utf-8")
    headers = list(re.finditer(r"\[DIFFICULTY_NORMAL\]\[(TRAINER_[A-Z0-9_]+)\]\s*=", source))
    result = {}
    for i, match in enumerate(headers):
        end = headers[i + 1].start() if i + 1 < len(headers) else len(source)
        section = source[match.end():end]
        name = re.search(r'\.trainerName\s*=\s*_\("([^"]*)"\)', section)
        role = re.search(r"\.trainerClass\s*=\s*(TRAINER_CLASS_[A-Z0-9_]+)", section)
        if name and role:
            result[match[1]] = {"name": name[1], "class": role[1], "source": "src/data/trainers.h"}
    return result


def designation(name, row, override, details, trainers):
    graphics = row["graphics_id"].removeprefix("OBJ_EVENT_GFX_")
    if row.get("type") == "clone":
        return "clone", None, None
    if name == "UnionRoom" and row.get("local_id", "").startswith("LOCALID_UNION_ROOM_PLAYER_"):
        return "remote_avatar", None, None
    kind = override.get("classification", "prop" if graphics in PROPS else
                        "pokemon" if graphics in POKEMON else "person")
    trainer = next((trainers[t] for t in details["trainers"] if t in trainers), None)
    role = override.get("role", "trainer" if trainer else ROLE_GRAPHICS.get(graphics, "resident"))
    return kind, role if kind == "person" else None, trainer


def character(id_, home, role, override, existing_name, graphics):
    digest = sha256(id_.encode()).digest()
    prior = PROFILES.get(id_, {})
    trait, preference, short, long = ARCHETYPES[role]
    shift = 7 + digest[2] % 5
    return {
        "name": override.get("name") or existing_name or
                f"{GIVEN[digest[0] % len(GIVEN)]} {FAMILY[digest[1] % len(FAMILY)]}",
        "name_source": "authored_or_established" if override.get("name") or existing_name else "generated",
        "age_category": "child" if graphics in ("OBJ_EVENT_GFX_LITTLE_GIRL", "OBJ_EVENT_GFX_LITTLE_BOY") else
                        "older_adult" if re.search(r"(?:OLD_MAN|OLD_WOMAN)", graphics) else None,
        "home": home,
        "role": role,
        "tier": override.get("tier", 1),
        "traits": prior.get("traits", [trait, ("steady", "direct", "thoughtful")[digest[3] % 3]]),
        "interests": prior.get("favorite_type") or preference,
        "short_goal": prior.get("secondary_motivation", short),
        "long_goal": prior.get("primary_goal", long),
        "relationships": list(FAMILY_TIES.get(id_, ())),
        "initial_knowledge": [home],
        "schedule": {"start_hour": shift, "end_hour": shift + 8, "activity": role,
                     "source": "profile", "may_change_rom_position": False},
        "memory_capacity": 8,
        "memory_policy": "save_checkpoint",
        "protected": True,
        "protected_behaviors": prior.get("protected_interactions", ()),
    }


def census(root):
    paths = sorted(p for p in (root / "data/maps").glob("*/map.json") if MAP_SCOPE.match(p.parent.name))
    maps = {p.parent.name: read_json(p) for p in paths}
    overrides = read_json(root / "experiments/living_world/kanto/identities.json")
    labels = scripts(root, maps)
    trainers = trainer_metadata(root)
    people, objects, event_links = {}, [], []
    appearances = defaultdict(list)
    for name, map_ in maps.items():
        for slot, row in enumerate(map_["object_events"], 1):
            label = row.get("script")
            suffix = label.removeprefix(name + "_EventScript_") if label not in (None, "0", "0x0") else None
            key = name + "/" + (suffix or row.get("local_id") or str(slot))
            local_key = f"{name}/{row.get('local_id')}"
            # Some authored objects deliberately share a script.
            if local_key in overrides:
                key = local_key
            elif sum(o.get("script") == label for o in map_["object_events"]) > 1:
                if name + "/" + str(slot) in overrides or not row.get("local_id"):
                    key = name + "/" + str(slot)
            override = overrides.pop(key, {})
            entry = override.get("entry", label)
            details = inspect_script(labels, entry)
            base_flags = (row["flag"],) if row.get("flag") not in (None, "0", "0x0") else ()
            kind, role, trainer = designation(name, row, override, details, trainers)
            id_ = override.get("id", key.lower()) if kind == "person" else None
            record = {
                "map": name, "slot": slot, "local_id": row.get("local_id"), "identity": id_,
                "kind": kind, "graphics": row["graphics_id"], "position": [row["x"], row["y"]],
                "rom_movement": row.get("movement_type"),
                "simulation_movement": override.get("movement", "rom_only"),
                "battle_type": row.get("trainer_type"),
                "visibility_flags": base_flags, "script": entry,
                "clone": {"map": row.get("target_map"), "local_id": row.get("target_local_id")}
                         if kind == "clone" else None,
                "trainer_data": {t: trainers[t] for t in details["trainers"] if t in trainers},
                **details,
            }
            objects.append(record)
            if id_ is not None:
                if id_ not in people:
                    people[id_] = character(id_, override.get("home", name), role, override,
                                            trainer and trainer["name"].title(), row["graphics_id"])
                appearances[id_].append([name, slot])
        for event in map_["coord_events"]:
            label = event.get("script")
            if label:
                event_links.append({"map": name, "script": label, "position": [event["x"], event["y"]],
                                    "condition": [event.get("var"), event.get("var_value")],
                                    **inspect_script(labels, label)})
    if overrides:
        raise ValueError(f"Stale identity references: {sorted(overrides)}")
    tokens = {row["id"]: name for name, row in maps.items()}
    authored = {(row["map"], row["local_id"]): row for row in objects if row["local_id"]}
    for record in objects:
        if (clone := record["clone"]) is not None:
            target = authored.get((tokens.get(clone["map"]), clone["local_id"]))
            if target and (id_ := target["identity"]) is not None:
                record["identity"] = id_
                appearances[id_].append([record["map"], record["slot"]])
    for id_, profile in people.items():
        profile["appearances"] = appearances[id_]
        assert profile["home"] in maps
    return maps, people, objects, event_links


def write_catalog(db, root):
    maps, people, objects, events = census(root)
    db.executescript("""
        CREATE TABLE kanto_map (
            id TEXT PRIMARY KEY, token TEXT UNIQUE NOT NULL, data TEXT NOT NULL
        );
        CREATE TABLE kanto_identity (
            id TEXT PRIMARY KEY, home TEXT NOT NULL REFERENCES kanto_map(id),
            tier INTEGER NOT NULL CHECK (tier BETWEEN 1 AND 3), data TEXT NOT NULL
        );
        CREATE INDEX kanto_home ON kanto_identity(home, id);
        CREATE TABLE kanto_appearance (
            map TEXT NOT NULL REFERENCES kanto_map(id), slot INTEGER NOT NULL,
            identity TEXT REFERENCES kanto_identity(id), kind TEXT NOT NULL, data TEXT NOT NULL,
            PRIMARY KEY (map, slot)
        );
        CREATE INDEX kanto_appearance_identity ON kanto_appearance(identity);
        CREATE TABLE kanto_trigger (map TEXT NOT NULL REFERENCES kanto_map(id), data TEXT NOT NULL);
        CREATE TABLE kanto_connection (
            origin TEXT NOT NULL REFERENCES kanto_map(id), destination TEXT NOT NULL,
            kind TEXT NOT NULL, data TEXT NOT NULL
        );
        CREATE INDEX kanto_connections ON kanto_connection(origin, destination);
    """)
    db.executemany("INSERT INTO kanto_map VALUES (?,?,?)", (
        (name, row["id"], json.dumps({"source": f"data/maps/{name}/map.json",
                                     "layout": row["layout"], "region_section": row["region_map_section"],
                                     "type": row["map_type"]}))
        for name, row in maps.items()
    ))
    db.executemany("INSERT INTO kanto_identity VALUES (?,?,?,?)", (
        (id_, profile["home"], profile["tier"], json.dumps(profile)) for id_, profile in people.items()
    ))
    db.executemany("INSERT INTO kanto_appearance VALUES (?,?,?,?,?)", (
        (row["map"], row["slot"], row["identity"], row["kind"], json.dumps(row)) for row in objects
    ))
    db.executemany("INSERT INTO kanto_trigger VALUES (?,?)",
                   ((row["map"], json.dumps(row)) for row in events))
    for name, map_ in maps.items():
        for kind, records, key in (("border", map_["connections"], "map"), ("warp", map_["warp_events"], "dest_map")):
            db.executemany("INSERT INTO kanto_connection VALUES (?,?,?,?)", (
                (name, item[key], kind, json.dumps({**item, "npc_travel": False,
                                                  "source": f"data/maps/{name}/map.json"}))
                for item in records or ()
            ))
    db.execute("""CREATE TABLE kanto_fact (
        map TEXT NOT NULL REFERENCES kanto_map(id), key TEXT NOT NULL, text TEXT NOT NULL,
        role TEXT, source TEXT NOT NULL, PRIMARY KEY(map, key)
    )""")
    # Border connections are topological knowledge, independent of present
    # access. NPC travel still uses only the runtime allowlist of tested edges.
    by_token = {row["id"]: name for name, row in maps.items()}
    for map_, row in maps.items():
        for edge in row["connections"] or ():
            if (destination := by_token.get(edge["map"])) is not None:
                db.execute("INSERT INTO kanto_fact VALUES (?,?,?,?,?)", (
                    map_, "border:" + destination,
                    f"{destination} borders this area to the {edge['direction']}.",
                    None, f"data/maps/{map_}/map.json#connections"
                ))
    for map_, key, role, label, text in (
        ("PewterCity_Museum_1F", "museum:fossils", "researcher",
         "PewterCity_Museum_1F_EventScript_Scientist2", "The Museum displays two fossils."),
        ("CeruleanCity_Gym", "gym:leader", "gym_leader",
         "CeruleanCity_Gym_EventScript_Misty", "Misty leads Cerulean Gym."),
        ("ViridianCity_Mart", "mart:service", "merchant",
         "ViridianCity_Mart_EventScript_Clerk", "The clerk serves customers after the parcel errand."),
        ("MtMoon_1F", "journal:brock", None,
         "MtMoon_1F_EventScript_BaldingMan", "A local visitor has heard of Brock."),
    ):
        path = "data/scripts/fame_checker.inc" if key == "journal:brock" else f"data/maps/{map_}/scripts.inc"
        if f"{label}::" not in (root / path).read_text(encoding="utf-8"):
            raise ValueError(f"Missing source for {key}: {path}#{label}")
        db.execute("INSERT INTO kanto_fact VALUES (?,?,?,?,?)", (map_, key, text, role, f"{path}#{label}"))
