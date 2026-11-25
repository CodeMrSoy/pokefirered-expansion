"""Translate reviewed companion state into one bounded native gameplay offer."""
import ctypes as c
from hashlib import sha256
from collections import Counter
import json
from math import isqrt
from struct import Struct

from native_world import ewram_pointer

MAGIC = 0x3132574C
HEADER = Struct("<17I")
MON = Struct("<I6H4B")
SIZE = HEADER.size + 6 * MON.size
TRAINER, LAND = 1, 2
FOREST = (1, 0)
LAND_PILOT = {(3, 43): "Route24", (3, 44): "Route25"}
SAMMY = 104
LEVEL_LIMIT = 9
CONTEXT_FIELDS = ("seed", "mode", "modes", "trainer_id", "features", "species_mode", "difficulty")
PUBLICATION_INTERVAL = 35
SEAL = 0x215EA1AB
REJECTION_SCHEMA = ("CREATE TABLE IF NOT EXISTS projection_rejections(stream TEXT NOT NULL, seq INTEGER NOT NULL, "
                    "event TEXT NOT NULL, PRIMARY KEY(stream,seq))")
SCHEMA = (
    "CREATE TABLE IF NOT EXISTS native_projections(stream TEXT NOT NULL, revision INTEGER NOT NULL, "
    "document TEXT NOT NULL, PRIMARY KEY(stream, revision))",
    "CREATE TABLE IF NOT EXISTS projected_battles(stream TEXT NOT NULL, battle INTEGER NOT NULL, "
    "revision INTEGER NOT NULL, kind INTEGER NOT NULL, selection INTEGER NOT NULL, "
    "outcome TEXT, PRIMARY KEY(stream,battle))",
    "CREATE TABLE IF NOT EXISTS projected_individuals(stream TEXT NOT NULL, battle INTEGER NOT NULL, "
    "slot INTEGER NOT NULL, individual TEXT NOT NULL, observation TEXT NOT NULL, PRIMARY KEY(stream,battle,slot))",
    "CREATE TABLE IF NOT EXISTS projected_conditions(stream TEXT NOT NULL, battle INTEGER NOT NULL, "
    "slot INTEGER NOT NULL, hp INTEGER NOT NULL, maximum INTEGER NOT NULL, participated INTEGER NOT NULL, "
    "PRIMARY KEY(stream,battle,slot))",
    "CREATE TABLE IF NOT EXISTS projected_captures(stream TEXT NOT NULL, battle INTEGER NOT NULL, "
    "identity TEXT, PRIMARY KEY(stream,battle))",
    "CREATE TABLE IF NOT EXISTS projected_player_aliases(native TEXT PRIMARY KEY, individual TEXT NOT NULL UNIQUE)",
)

def identifier(value):
    return int.from_bytes(sha256(value.encode("ascii")).digest()[:4], "little") or 1


def checksum(raw):
    result = 2166136261
    for byte in raw:
        result = ((result ^ byte) * 16777619) & 0xFFFFFFFF
    return result


def packet(document, frame):
    rows = []
    for mon in document["party"]:
        moves = (*mon.get("moves", ()), 0, 0, 0, 0)[:4]
        rows.append(MON.pack(mon["tag"], mon["species"], mon.get("ability", 0), *moves,
                             mon.get("level", 0), mon.get("ability_slot", 0),
                             mon.get("weight", 0), (identifier(mon["lease"]) & 255 or 1) if "lease" in mon else 0))
    body = b"".join(rows).ljust(6 * MON.size, b"\0")
    header = HEADER.pack(MAGIC, 1, document["generation"], document["counter"], frame,
                         document["seed"], document["mode"] | document.get("species_mode", 0) << 8
                         | document.get("difficulty", 0) << 16,
                         document["modes"] | document.get("features", 0) << 8, document["trainer_id"],
                         document["key_a"], document["key_b"], document["revision"], document["kind"],
                         (document["map"][0] << 8) | document["map"][1],
                         document["variant"], len(rows), 0)
    return header[:-4] + checksum(header[4:-4] + body).to_bytes(4, "little") + body


def trainer_offer(manifest, state, day):
    if not state or "sammy" not in state["actors"]:
        return []
    a = state["actors"]["sammy"]
    if (a["location"] != "1:0" or a["journey"] or a.get("native_battle")
            or not a["profile"]["native_roster"] or a["profile"]["native_roster"]["id"] != SAMMY):
        return []
    roster = []
    protected = frozenset(manifest.get("ecology_protected", ()))
    species = {row["id"]: row for row in manifest["species"]}
    for uid in a["party"]:
        mon = state["mons"][uid]
        if mon["owner"] != "sammy" or mon["fatigue"] >= 2 or mon.get("recover_until", 0) > day:
            continue
        species_id = mon["species"]
        data = species.get(species_id)
        if not data or data["status"] != "resolved" or species_id in protected or species_id == 201:
            continue
        level = min(mon["level"], LEVEL_LIMIT)
        slot = mon["ability_slot"]
        if not 0 <= slot < len(data["abilities"]) or mon["ability"] != data["abilities"][slot] or not mon["ability"]:
            continue
        legal = {move for move, at in data["learnset"] if 0 < at <= level and move > 0}
        moves = [move for move in mon["moves"] if move in legal]
        if len(moves) == 0:
            continue
        roster.append(dict(id=uid, tag=identifier(uid), species=species_id, level=level,
                           ability=mon["ability"], ability_slot=slot, moves=moves))
        if len(roster) == 2:
            break
    if len({row["tag"] for row in roster}) != len(roster):
        return []
    return roster


def land_support(eco, location):
    key = ":".join(map(str, location))
    habitat = eco["habitats"].get(key)
    if (not habitat or habitat["name"] != LAND_PILOT.get(tuple(location))
            or habitat["native"]["protected_encounter"] or not habitat["simulated"]["edges"].get("land")):
        return 0, set(), set()
    distributions = [row for row in habitat["native"]["distributions"]
                     if row["method"] == "land" and 0 <= row["variant"] < 32 and row["weights"]]
    if not distributions:
        return 0, set(), set()
    layer = habitat["simulated"]["layers"]["land"]
    authored = set().union(*(row["weights"].keys() for row in distributions))
    eligible = set(layer.get("compatible_arrivals", ()))
    eligible.update(set.intersection(*(set(row["weights"]) for row in distributions)))
    mask = sum(1 << variant for variant in {row["variant"] for row in distributions})
    return mask, eligible, authored


def wild_offer(manifest, eco, location):
    """An overlay is valid only across the reviewed native time variants."""
    mask, eligible, authored = land_support(eco, location)
    if not mask:
        return 0, []
    key = ":".join(map(str, location))
    protected = set(manifest.get("ecology_protected", ()))
    groups = eco["groups"][key]["land"]
    migrants, familiar = [], []
    for species, size in sorted(groups.items(), key=lambda pair: (-pair[1], int(pair[0]))):
        if size > 0 and species in eligible and int(species) not in protected and int(species) != 201:
            row = dict(tag=0, species=int(species), weight=min(20, isqrt(size) * 3),
                       migrant=species not in authored)
            (migrants if row["migrant"] else familiar).append(row)
    return mask, migrants[:2] + familiar[:4]


def lease_wild(db, stream, manifest, eco, location, variants):
    """Reserve at most one named land resident while the stream is on its map."""
    from ecology import apply

    key = ":".join(map(str, location))
    residents = [(uid, mon) for uid, mon in sorted(eco["individuals"].items())
                 if mon["location"] == key and mon["layer"] == "land"]
    lease = next(((uid, mon) for uid, mon in residents if mon.get("reservation")), None)
    if lease:
        uid, mon = lease
        if mon["reservation"]["stream"] == stream and not mon["reservation"].get("battle"):
            return dict(id=uid, lease=mon["reservation"]["id"], tag=identifier(f"{eco['world']}:{uid}"),
                        species=mon["species"], level=mon["native_level"], weight=4, migrant=False)
        return None

    _, eligible, _ = land_support(eco, location)
    protected = set(manifest.get("ecology_protected", ())) | {201}
    levels = Counter()
    for encounter in manifest["encounters"]:
        table = encounter["table"]
        if table["map"] == location and table["kind"] == "land" and variants & (1 << table["variant"]):
            for slot in encounter["slots"]:
                if slot["status"] == "resolved":
                    for level in range(slot["level"][0], min(slot["level"][1], 15) + 1):
                        levels[level] += slot["authored"]["weight"] or 0
    for uid, mon in residents:
        if (str(mon["species"]) not in eligible or mon["species"] in protected
                or mon.get("release_day", -1) >= eco["day"]):
            continue
        level = mon.get("native_level") or (levels.most_common(1)[0][0] if levels else None)
        if not level or level not in levels:
            continue
        source, = db.execute("SELECT COALESCE(MAX(rowid),0)+1 FROM ecology_inputs").fetchone()
        lease_id = f"{stream}:{source}"
        apply(db, [(f"projection-lease:{lease_id}", dict(wild_native=dict(
            status="reserved", stream=stream, individual=uid, lease=lease_id, location=key, level=level)))])
        return dict(id=uid, lease=lease_id, tag=identifier(f"{eco['world']}:{uid}"),
                    species=mon["species"], level=level, weight=4, migrant=False)
    return None


def prepare(db, stream, request, summary, eco):
    """Register an immutable offer before publication. Runs on the journal worker."""
    location = tuple(request["map"])
    if location != FOREST and location not in LAND_PILOT:
        return None, "outside_pilot"
    manifest, = db.execute("SELECT document FROM starting_manifest WHERE slot=1").fetchone()
    manifest = json.loads(manifest)
    context = manifest["context"]
    if any(request[k] != context[k] for k in CONTEXT_FIELDS):
        raise ValueError("Projection context did not match the paired manifest")
    if location == FOREST:
        kind, variant = TRAINER, SAMMY
        party = trainer_offer(manifest, summary["trainers"], summary["day"])
        fallback = "no_eligible_sammy_party"
    else:
        kind = LAND
        variant, party = wild_offer(manifest, eco, list(location))
        rare = lease_wild(db, stream, manifest, eco, list(location), variant) if party else None
        if rare:
            party = [dict(rare, ot=request["trainer_id"]), *party[:5]]
        fallback = "no_eligible_land_groups"
    if not party:
        return None, fallback
    document = dict(request, kind=kind, variant=variant, world=manifest["world_uuid"],
                    manifest=manifest["manifest_sha256"], party=party)
    key = f"{document['world']}:{document['manifest']}:{request['checkpoint']}:{stream}"
    document.update(key_a=identifier(key + ":a"), key_b=identifier(key + ":b"))
    document["revision"] = identifier(json.dumps(document, sort_keys=True, separators=(",", ":")))
    payload = json.dumps(document, sort_keys=True, separators=(",", ":"))
    for statement in SCHEMA:
        db.execute(statement)
    db.execute("INSERT OR IGNORE INTO native_projections VALUES (?,?,?)",
               (stream, document["revision"], payload))
    if db.execute("SELECT document FROM native_projections WHERE stream=? AND revision=?",
                  (stream, document["revision"])).fetchone() != (payload,):
        raise ValueError("Projection revision collision")
    return document, None


def publish(game, address, document, frame):
    ptr = ewram_pointer(lambda key: (game.memory(key), game.memory_size(key)), address, SIZE + 4)
    if c.c_uint32.from_address(ptr + SIZE).value != SEAL ^ address:
        return False
    if document is None:
        c.memset(ptr, 0, 4)
    else:
        c.memmove(ptr, packet(document, frame), SIZE)
    return True


def receive(db, stream, event):
    """Validate the accepted native offer against its prior durable registration."""
    battle = event["battle"]
    if event["kind"] == "projection_rejected":
        db.execute(REJECTION_SCHEMA)
        db.execute("INSERT INTO projection_rejections VALUES (?,?,?)",
                   (stream, event["seq"], json.dumps(event, sort_keys=True)))
        return None
    if event["kind"] == "projection":
        if not db.execute("SELECT 1 FROM sqlite_master WHERE name='native_projections'").fetchone():
            raise ValueError("Native battle accepted an unregistered projection")
        row = db.execute("SELECT document FROM native_projections WHERE stream=? AND revision=?",
                         (stream, event["value"])).fetchone()
        if not row:
            raise ValueError("Wrong native projection stream or revision")
        document = json.loads(row[0])
        identity = db.execute("SELECT world,manifest FROM native_streams WHERE stream=?", (stream,)).fetchone()
        if identity != (document["world"], document["manifest"]):
            raise ValueError("Projection belongs to another world or manifest")
        start = db.execute("SELECT event FROM native_events WHERE stream=? AND seq=?", (stream, battle)).fetchone()
        if (not start or document["map"] != event["map"] or document["kind"] != event["actor"]
                or (document["kind"] == TRAINER and len(document["party"]) != event["flags"])
                or (document["kind"] == LAND and not 0 <= event["flags"] < len(document["party"]))):
            raise ValueError("Unexpected native projection acceptance")
        start = json.loads(start[0])
        expected_flags = 8 if document["kind"] == TRAINER else 0
        expected_actor = SAMMY if document["kind"] == TRAINER else None
        if (start["kind"] != "battle_start" or start["actor"] != expected_actor
                or start["flags"] & ~4 != expected_flags or start["map"] != document["map"]):
            raise ValueError("Projected battle did not start in the allowed context")
        db.execute("INSERT INTO projected_battles VALUES (?,?,?,?,?,NULL)",
                   (stream, battle, event["value"], event["actor"], event["flags"]))
        if document["kind"] == TRAINER:
            return dict(trainer_native=dict(status="started", battle=f"{stream}:{battle}"))
        chosen = document["party"][event["flags"]]
        return wild_change(chosen, stream, battle, "engaged") if "id" in chosen else None
    if (not battle or event["kind"] not in {"battle_mon", "battle_end", "project_condition", "capture"}
            or not db.execute("SELECT 1 FROM sqlite_master WHERE name='projected_battles'").fetchone()):
        return None
    row = db.execute("SELECT p.document,b.selection FROM projected_battles b JOIN native_projections p "
                     "ON p.stream=b.stream AND p.revision=b.revision WHERE b.stream=? AND b.battle=?",
                     (stream, battle)).fetchone()
    if not row:
        return None
    document = json.loads(row[0])
    if document["kind"] == LAND:
        return receive_wild(db, stream, event, document["party"][row[1]])
    if event["kind"] == "battle_end":
        db.execute("UPDATE projected_battles SET outcome=? WHERE stream=? AND battle=?",
                   (event["outcome"], stream, battle))
        if event["outcome"] not in {"won", "lost", "draw", "forfeited"}:
            raise ValueError("Invalid projected trainer battle outcome")
        members = list(db.execute(
            "SELECT i.individual,c.hp,c.maximum,c.participated FROM projected_individuals i "
            "JOIN projected_conditions c USING(stream,battle,slot) "
            "WHERE i.stream=? AND i.battle=? ORDER BY i.slot", (stream, battle)))
        if len(members) != len(document["party"]):
            raise ValueError("Missing projected trainer conditions")
        return dict(trainer_native=dict(status="finished", battle=f"{stream}:{battle}",
                                        outcome=event["outcome"], members=[list(row) for row in members]))
    if event["kind"] == "project_condition":
        slot = (event["actor"] or 0) - 1
        hp, maximum = event["value"] & 65535, event["value"] >> 16
        if not 0 <= slot < len(document["party"]) or not 0 <= hp <= maximum or maximum == 0:
            raise ValueError("Malformed projected trainer condition")
        db.execute("INSERT INTO projected_conditions VALUES (?,?,?,?,?,?)",
                   (stream, battle, slot, hp, maximum, bool(event["flags"])))
        return None
    mon = event["mon"]
    if not mon or mon["egg"] or not 0 <= mon["slot"] < len(document["party"]):
        raise ValueError("Invalid projected native opponent")
    expected = document["party"][mon["slot"]]
    if (any(mon[key] != expected[key] for key in ("species", "ability", "ability_slot", "level"))
            or tuple(move for move in mon["moves"] if move) != tuple(expected["moves"])
            or mon["personality"] != expected["tag"] or mon["ot"] != expected["tag"] ^ 0x5A000000
            or mon["item"]):
        raise ValueError("Native opponent differed from frozen projection")
    db.execute("INSERT INTO projected_individuals VALUES (?,?,?,?,?)",
               (stream, battle, mon["slot"], expected["id"], json.dumps(mon, sort_keys=True)))
    return dict(individual=expected["id"])


def wild_change(row, stream, battle, status):
    return dict(wild_native=dict(status=status, stream=stream, battle=f"{stream}:{battle}",
                                 individual=row["id"], lease=row["lease"]))


def receive_wild(db, stream, event, expected):
    battle = event["battle"]
    kind = event["kind"]
    rare = "id" in expected
    if kind == "battle_end":
        db.execute("UPDATE projected_battles SET outcome=? WHERE stream=? AND battle=?",
                   (event["outcome"], stream, battle))
        if rare:
            captured = db.execute("SELECT 1 FROM projected_captures WHERE stream=? AND battle=?",
                                  (stream, battle)).fetchone()
            if not captured:
                return wild_change(expected, stream, battle, "released")
        return None
    mon = event["mon"]
    if kind not in {"battle_mon", "capture"} or not mon or mon["slot"] != 0 or mon["species"] != expected["species"]:
        raise ValueError("Native land opponent differed from the selected overlay")
    if kind == "battle_mon" and rare:
        if (mon["personality"] != expected["tag"] or mon["ot"] != expected["ot"]
                or mon["level"] != expected["level"] or mon["egg"]):
            raise ValueError("Named individual did not match native instantiation")
        db.execute("INSERT INTO projected_individuals VALUES (?,?,?,?,?)",
                   (stream, battle, 0, expected["id"], json.dumps(mon, sort_keys=True)))
        return dict(individual=expected["id"])
    if kind == "capture" and event["value"] in (0, 1):
        db.execute("INSERT INTO projected_captures VALUES (?,?,?)", (stream, battle, expected.get("id")))
        if rare:
            row = db.execute("SELECT observation FROM projected_individuals WHERE stream=? AND battle=? AND slot=0",
                             (stream, battle)).fetchone()
            if not row:
                raise ValueError("Named capture is missing its native encounter")
            encountered = json.loads(row[0])
            if any(mon[key] != encountered[key] for key in ("personality", "ot", "ivs", "species")):
                raise ValueError("Native capture did not match the named encounter")
            native = "player:{ot:08x}:{personality:08x}:{ivs:08x}".format_map(mon)
            db.execute("INSERT INTO projected_player_aliases VALUES (?,?)", (native, expected["id"]))
            return dict(wild_change(expected, stream, battle, "captured"), persistent=expected["id"])
        return dict(projection_land=True)
    return None


def recent(db, stream):
    if not db.execute("SELECT 1 FROM sqlite_master WHERE name='projected_battles'").fetchone():
        return []
    return [dict(battle=battle, revision=revision, kind=kind, outcome=outcome, current_session=owner == stream,
                 individuals=[uid for uid, in db.execute(
                     "SELECT individual FROM projected_individuals WHERE stream=? AND battle=? ORDER BY slot",
                     (owner, battle))])
            for owner, battle, revision, kind, outcome in db.execute(
                "SELECT stream,battle,revision,kind,outcome FROM projected_battles ORDER BY rowid DESC LIMIT 12")]

def rejections(db, stream):
    if not db.execute("SELECT 1 FROM sqlite_master WHERE name='projection_rejections'").fetchone():
        return []
    return [json.loads(raw) for raw, in db.execute(
        "SELECT event FROM projection_rejections WHERE stream=? ORDER BY seq DESC LIMIT 8", (stream,))]
