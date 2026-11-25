"""Deterministic companion ecology projected from the immutable world manifest."""
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from hashlib import sha256
import json

from kanto import DISTRICTS
from profiles import KNOWLEDGE_PROFILES

SCHEMA = (
    "CREATE TABLE IF NOT EXISTS ecology_state(slot INTEGER PRIMARY KEY CHECK(slot=1), document TEXT NOT NULL)",
    "CREATE TABLE IF NOT EXISTS ecology_inputs(id TEXT PRIMARY KEY, entry TEXT NOT NULL)",
)
# Reviewed outdoor corridors. A policy entry alone never establishes an edge.
CORRIDORS = {frozenset(pair) for pair in (
    ("Route9", "Route10"), ("Route13", "Route14"), ("Route14", "Route15"),
    ("Route19", "Route20"), ("Route24", "Route25"),
)}
REVERSE = {1: 2, 2: 1, 3: 4, 4: 3}
METHODS = {"land": "land", "rock_smash": "land", "surf": "water", "fishing": "water"}
# Safari, roamer, scripted, legendary, ghost, and tutorial encounters are evidence only.
SPECIAL_BATTLE = sum(1 << bit for bit in (4, 7, 9, 10, 13, 14, 17, 18, 28, 29))
MAX_RECENT = 120
KNOWLEDGE_DAYS = 21
SEASONS = ("spring", "summer", "autumn", "winter")
SEASON_RESOURCE = {"land": (100, 95, 88, 77), "water": (93, 100, 95, 84),
                   "cave": (100, 99, 98, 97)}


@dataclass(frozen=True)
class Limits:
    land_capacity: int = 72
    water_capacity: int = 56
    cave_capacity: int = 38
    notable_limit: int = 64
    transit_limit: int = 128


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def draw(seed, *key):
    return int.from_bytes(sha256(encoded((seed, key)).encode("ascii")).digest()[:8], "little")


def map_key(native_id):
    return ":".join(map(str, native_id))


def registry(manifest, protection, limits):
    maps = {map_key(row["id"]): row for row in manifest["maps"]}
    static_maps = {map_key(row["map"]) for row in manifest["static_encounters"]}
    protected = set(protection or ()) | {
        mon["species"] for scene in manifest["static_encounters"] for mon in scene["party"]
        if mon.get("species") is not None
    } | {
        mon["authored"]["species"] for scene in manifest["static_encounters"] for mon in scene["party"]
        if mon.get("authored", {}).get("species") is not None
    }
    types = {str(row["id"]): set(row.get("authored", {}).get("types", ())) - {0}
             for row in manifest["species"]}
    enabled = {row["id"] for row in manifest["species"] if row.get("authored", {}).get("enabled")}
    habitats, weights = {}, defaultdict(Counter)
    for entry in manifest["encounters"]:
        table = entry["table"]
        key = map_key(table["map"])
        row = maps[key]
        environment = {1: "settlement", 2: "settlement", 3: "outdoor", 4: "cave",
                       5: "underwater", 6: "coast", 8: "interior"}.get(row.get("map_type"), "unknown")
        habitat = habitats.setdefault(key, dict(name=row["name"], environment=environment,
              native=dict(map=row["id"], map_type=row.get("map_type"), section=row.get("section"),
                          access=row.get("access"), connections=row.get("connections", []),
                          protected_encounter=key in static_maps, distributions=[]), simulated=dict(layers={}, edges={})))
        layer = METHODS.get(table.get("kind"))
        variant = str(table["variant"])
        distribution = Counter()
        for slot in entry["slots"]:
            if slot["status"] == "resolved" and slot["authored"]["weight"] is not None:
                distribution[str(slot["species"])] += slot["authored"]["weight"]
        habitat["native"]["distributions"].append(dict(method=table.get("kind"), variant=table["variant"],
                season_index=table["variant"] // manifest["rules"].get("time_variants", 1),
                time_index=table["variant"] % manifest["rules"].get("time_variants", 1),
                weights=dict(distribution), status=table.get("status", "conditional")))
        if (protection is None or not layer or environment in {"interior", "unknown"} or key in static_maps):
            continue
        for species, weight in distribution.items():
            if int(species) in enabled and int(species) not in protected:
                weights[key, layer, variant][species] += weight

    for (key, layer, variant), candidates in sorted(weights.items()):
        if not candidates:
            continue
        habitat = habitats[key]
        capacity = limits.cave_capacity if habitat["environment"] == "cave" else getattr(limits, f"{layer}_capacity")
        pool = habitat["simulated"]["layers"].setdefault(layer, dict(capacity=capacity, variants={}))
        pool["variants"][variant] = dict(candidates)

    for key, habitat in sorted(habitats.items()):
        row = maps[key]
        if row.get("map_type") not in (3, 6) or key in static_maps:
            continue
        if not row.get("access") or row["access"].get("vidra_section") is not False:
            continue
        for edge in row["connections"]:
            dest = map_key(edge["target"])
            neighbor = habitats.get(dest)
            if not neighbor or dest in static_maps or maps[dest].get("map_type") not in (3, 6):
                continue
            if not maps[dest].get("access") or maps[dest]["access"].get("vidra_section") is not False:
                continue
            if frozenset((habitat["name"], neighbor["name"])) not in CORRIDORS:
                continue
            if not any(other["target"] == row["id"] and other["direction"] == REVERSE.get(edge["direction"])
                       and other["offset"] == -edge["offset"] for other in maps[dest]["connections"]):
                continue
            for layer in sorted(habitat["simulated"]["layers"].keys() & neighbor["simulated"]["layers"].keys()):
                habitat["simulated"]["edges"].setdefault(layer, {})[dest] = 1 + min(2, abs(edge["offset"]) // 24)

    # Compatibility uses the effective local fauna as a conservative proxy
    # for habitat affinities. A species can establish only after an arrival.
    for key, habitat in sorted(habitats.items()):
        for layer, edges in habitat["simulated"]["edges"].items():
            pool = habitat["simulated"]["layers"][layer]
            sources = set().union(*(set(group) for group in pool["variants"].values()))
            for dest in edges:
                target = habitats[dest]["simulated"]["layers"][layer]
                supports = {}
                for variant, candidates in target["variants"].items():
                    shared = set().union(*(types[species] for species in candidates))
                    compatible = sorted(species for species in sources if species not in candidates
                                        and types[species] & shared
                                        and (layer != "water" or 12 in types[species]))
                    if compatible:
                        supports[variant] = compatible
                if supports:
                    pool.setdefault("migration_affinity", {})[dest] = supports
                    known = target.setdefault("compatible_arrivals", [])
                    target["compatible_arrivals"] = sorted(set(known).union(*supports.values()))
    return habitats


def initial_state(manifest, protection, tick, limits=Limits()):
    habitats = registry(manifest, protection, limits)
    seed = manifest["context"]["seed"]
    groups = {}
    for key, habitat in sorted(habitats.items()):
        groups[key] = {}
        for layer, pool in habitat["simulated"]["layers"].items():
            weights = Counter()
            for candidates in pool["variants"].values():
                weights.update(candidates)
            cap = pool["capacity"]
            budget = cap * (55 + draw(seed, key, layer) % 26) // 100
            total = sum(weights.values())
            groups[key][layer] = {species: budget * weight // total for species, weight in sorted(weights.items())}
    return dict(version=1, seed=seed, world=manifest["world_uuid"], start_tick=tick, day=tick // 24,
                limits=asdict(limits), wild_times=manifest["rules"].get("time_variants", 1),
                wild_variants=manifest["rules"].get("season_time_variants", 1),
                habitats=habitats, groups=groups, transit=[], individuals={}, history=[], sightings={},
                native_counts={}, event_counts={}, trends={}, protected_policy=protection is not None)


def note(state, kind, location, **details):
    row = dict(kind=kind, location=location, day=state["day"], **details)
    if details.get("source") != "native_observation":
        state["event_counts"][kind] = state["event_counts"].get(kind, 0) + 1
    state["history"].append(row)
    del state["history"][:-MAX_RECENT]
    return row


def totals(state):
    named = Counter(mon["location"] for mon in state["individuals"].values())
    return {key: named[key] + sum(sum(pool.values()) for pool in by_layer.values())
            for key, by_layer in state["groups"].items()}


def occupied(state):
    return Counter((mon["location"], mon["layer"]) for mon in state["individuals"].values())


def active_variants(state):
    season = state["day"] // 90 % 4 if state["wild_variants"] > state["wild_times"] else 0
    return tuple(str(season * state["wild_times"] + hour) for hour in range(state["wild_times"]))


def active_weights(state, pool):
    variants = active_variants(state)
    daily = Counter()
    for variant, candidates in pool["variants"].items():
        if variant in variants:
            daily.update(candidates)
    return daily


def evolve_day(state, day):
    """Apply one daily update using integer rules and seeded tie breaks."""
    if day != state["day"] + 1:
        raise ValueError("Ecology day must advance exactly once")
    state["day"] = day
    seed = state["seed"]
    before = totals(state)
    survivors = []
    for journey in state["transit"]:
        if journey["arrival"] <= day:
            target = state["groups"][journey["destination"]][journey["layer"]]
            species = journey["species"]
            target[species] = target.get(species, 0) + journey["count"]
            note(state, "migration_arrived", journey["destination"], **journey)
        else:
            survivors.append(journey)
    state["transit"] = survivors
    reserved = Counter()
    for trip in survivors:
        reserved[trip["destination"], trip["layer"]] += trip["count"]
    notables = occupied(state)
    resources, daily = {}, {}
    for key, habitat in sorted(state["habitats"].items()):
        for layer, pool in habitat["simulated"]["layers"].items():
            capacity = pool["capacity"]
            seasonal = SEASON_RESOURCE["cave" if habitat["environment"] == "cave" else layer][day // 90 % 4]
            resource = capacity * seasonal * (58 + draw(seed, "resource", key, layer, day // 7) % 39) // 10000
            resources[key, layer] = resource
            weights = active_weights(state, pool)
            daily[key, layer] = weights.copy()
            groups = state["groups"][key][layer]
            arrival_weight = max(1, sum(weights.values()) // max(1, capacity))
            if weights:
                for species in pool.get("compatible_arrivals", ()):
                    if groups.get(species):
                        weights.setdefault(species, arrival_weight)
            count = sum(groups.values()) + notables[key, layer]
            can_add = max(0, capacity - count - reserved[key, layer])
            total_weight = sum(weights.values())
            for species in sorted(groups):
                current = groups[species]
                weight = weights.get(species, 0)
                target = max(1, resource * weight // total_weight) if weight else 0
                chance = draw(seed, "growth", day, key, layer, species) % 100
                if current > target and chance < (45 if count > resource else 22):
                    groups[species] -= 1
                    can_add += 1
                elif current < target and can_add and chance < (42 if current else 10):
                    groups[species] += 1
                    can_add -= 1
            # Promote at most one already-counted resident per habitat per day.
            if (len(state["individuals"]) < state["limits"]["notable_limit"]
                    and not notables[key, layer] and draw(seed, "notable", day, key, layer) % 83 == 0):
                eligible = [species for species in sorted(groups) if 2 <= groups[species] <= 5]
                if eligible:
                    species = eligible[0]
                    uid = f"sim:{key}:{layer}:{species}:{day}"
                    groups[species] -= 1
                    state["individuals"][uid] = dict(id=uid, species=int(species), location=key, layer=layer,
                                                      origin="simulated", form_species=int(species),
                                                      first_seen=day, last_seen=day)
                    notables[key, layer] += 1
                    note(state, "unusual_sighting", key, individual=uid, species=int(species), confidence=70)

    for key, habitat in sorted(state["habitats"].items()):
        for layer, edges in habitat["simulated"]["edges"].items():
            source = state["groups"][key][layer]
            if 100 * sum(source.values()) < 85 * resources[key, layer] or len(state["transit"]) >= state["limits"]["transit_limit"]:
                continue
            for dest, duration in sorted(edges.items()):
                target = state["groups"][dest][layer]
                room = resources[dest, layer] - sum(target.values()) - reserved[dest, layer] - notables[dest, layer]
                affinity = habitat["simulated"]["layers"][layer].get("migration_affinity", {}).get(dest, {})
                suitable = set(daily[dest, layer])
                for variant in active_variants(state):
                    suitable.update(affinity.get(variant, ()))
                candidates = [species for species in sorted(source)
                              if source[species] >= 4 and species in daily[key, layer] and species in suitable]
                if room < 2 or not candidates:
                    continue
                species = candidates[draw(seed, "migration", day, key, dest, layer) % len(candidates)]
                count = min(room, 3, source[species] // 3)
                source[species] -= count
                reserved[dest, layer] += count
                trip = dict(source=key, destination=dest, layer=layer, species=species,
                            count=count, departure=day, arrival=day+duration)
                state["transit"].append(trip)
                note(state, "migration_departed", key, **trip)

    for uid, mon in sorted(state["individuals"].items()):
        if draw(seed, "resighting", day, uid) % 17 == 0:
            mon["last_seen"] = day
            note(state, "unusual_sighting", mon["location"], individual=uid, species=mon["species"], confidence=70)

    for key, count in totals(state).items():
        delta = count - before[key]
        state["trends"][key] = dict(change=delta, resources={layer: value for (place, layer), value in resources.items()
                                                           if place == key})
        if abs(delta) >= 4:
            note(state, "unusual_population_change", key, change=delta, confidence=55)
    fieldwork(state)


def fieldwork(state):
    """Existing local profiles collect and share uncertain reports during bounded patrols."""
    day = state["day"]
    names = Counter(row["name"] for row in state["habitats"].values())
    by_name = {row["name"]: key for key, row in state["habitats"].items() if names[row["name"]] == 1}
    visible = defaultdict(list)
    for event in state["history"]:
        if event["day"] == day and event["kind"] in ("unusual_sighting", "unusual_population_change", "migration_arrived"):
            visible[event["location"]].append(event)
    for npc, (area, _, expertise, _, _) in sorted(KNOWLEDGE_PROFILES.items()):
        local = by_name.get(DISTRICTS.get(area))
        if (not local or not set(expertise) & {"biology", "directions", "research"}
                or draw(state["seed"], "patrol", day, npc) % 3):
            continue
        if visible[local]:
            event = visible[local][-1]
            state["sightings"][npc] = {**event, "observed_day": day, "source": npc, "activity": "local_patrol",
                                        "confidence": event.get("confidence", 65), "followup": "survey_locally",
                                        "followup_day": day + 2}
    prior = dict(state["sightings"])
    for npc, (_, _, _, contacts, _) in sorted(KNOWLEDGE_PROFILES.items()):
        if npc in prior and prior[npc]["observed_day"] >= day-2:
            continue
        for source in contacts:
            report = prior.get(source)
            if report and report["observed_day"] == day-1 and report["activity"] == "local_patrol":
                state["sightings"][npc] = dict(report, source=source, activity="received_from_contact",
                                               confidence=max(10, report["confidence"] - 25),
                                               followup="ask_source", followup_day=day + 1)
                break
    for npc, row in list(state["sightings"].items()):
        if day - row["observed_day"] > KNOWLEDGE_DAYS:
            del state["sightings"][npc]


def observe(state, event, event_id):
    key = map_key(event["map"])
    if key not in state["habitats"]:
        return
    kind = event["kind"]
    counts = state["native_counts"].setdefault(key, {})
    counts[kind] = counts.get(kind, 0) + 1
    mon = event.get("mon")
    if kind == "map":
        return
    evidence = dict(source="native_observation", event=event_id, species=mon["species"] if mon else None,
                    battle=event.get("battle"), outcome=event.get("outcome"))
    if event.get("persistent"):
        evidence["persistent_individual"] = event["persistent"]
    if (kind == "capture" and event["value"] in (0, 1) and mon and not event.get("persistent")
            and not event.get("flags", 0) & SPECIAL_BATTLE):
        species = str(mon["species"])
        habitat = state["habitats"][key]["simulated"]["layers"]
        options = [group for layer, group in state["groups"][key].items() if species in group and
                   any(species in weights for weights in habitat[layer]["variants"].values())]
        if event.get("projection_land"):
            options = [state["groups"][key]["land"]]
        if len(options) == 1 and options[0].get(species, 0) > 0:
            options[0][species] -= 1
            evidence["population_adjustment"] = -1
    # Battle identity and known attributes remain in the Phase 18 observation
    # tables. Ordinary sightings never link to a simulated individual.
    note(state, kind, key, **evidence)


def native_wild(state, change):
    """Replay a single lease status change inside the native journal transaction."""
    status, stream = change["status"], change["stream"]
    if status == "map":
        for uid, mon in state["individuals"].items():
            lease = mon.get("reservation")
            if lease and (lease["stream"] != stream or mon["location"] != change["location"]):
                if lease.get("battle") and lease["stream"] == stream:
                    raise ValueError("Reserved native wild battle left its map")
                del mon["reservation"]
                note(state, "native_reservation_released", mon["location"], individual=uid, cause="map_or_session")
        return
    uid = change["individual"]
    mon = state["individuals"].get(uid)
    if not mon:
        raise ValueError("Named native encounter has no wild individual")
    lease = mon.get("reservation")
    if status == "reserved":
        if lease or mon["location"] != change["location"] or mon["layer"] != "land":
            raise ValueError("Wild reservation could not acquire the individual")
        mon["native_level"] = change["level"]
        mon["reservation"] = dict(id=change["lease"], stream=stream)
        if mon["location"] == "3:44":
            sightings = [row for row in state["history"] if row["kind"] == "unusual_sighting"
                         and row.get("individual") == uid and state["day"] - row["day"] <= KNOWLEDGE_DAYS]
            if sightings:
                observed = sightings[-1]
                state["sightings"]["route25/man"] = dict(observed, kind="named_local_report",
                     source="route_25_ecological_survey", observed_day=observed["day"],
                     activity="received_from_contact", confidence=45)
    elif not lease or (lease["stream"], lease["id"]) != (stream, change["lease"]):
        raise ValueError("Native encounter did not own the reserved individual")
    elif status == "engaged" and not lease.get("battle"):
        lease["battle"] = change["battle"]
    elif lease.get("battle") == change["battle"] and status in {"captured", "released"}:
        del mon["reservation"]
        if status == "captured":
            del state["individuals"][uid]
            state["sightings"] = {npc: report for npc, report in state["sightings"].items()
                                  if report.get("individual") != uid}
        else:
            mon["release_day"] = state["day"]
    else:
        raise ValueError("Invalid native reservation transition")
    note(state, "native_reservation_" + status, mon["location"], individual=uid, battle=change.get("battle"))


def relevant(event):
    return (event["kind"] == "map" or
            event.get("battle_kind") == "wild" and event["kind"] in {"battle_mon", "capture", "battle_end"})


def write_state(db, state):
    db.execute("INSERT OR REPLACE INTO ecology_state VALUES (1,?)", (encoded(state),))


def read_state(db):
    row = db.execute("SELECT document FROM ecology_state WHERE slot=1").fetchone()
    return json.loads(row[0]) if row else None


def initialize(db, protection, limits=Limits()):
    for statement in SCHEMA:
        db.execute(statement)
    if db.execute("SELECT 1 FROM ecology_state").fetchone():
        return
    manifest, = db.execute("SELECT document FROM starting_manifest WHERE slot=1").fetchone()
    tick, = db.execute("SELECT json_extract(state,'$.tick') FROM simulation WHERE slot=1").fetchone()
    manifest = json.loads(manifest)
    protected = manifest.get("ecology_protected", protection)
    state = initial_state(manifest, protected, tick, limits)
    db.execute("INSERT INTO ecology_inputs VALUES ('origin',?)",
               (encoded(dict(tick=tick, protected=protected, limits=asdict(limits))),))
    write_state(db, state)


def trainer_day(eco, previous, entry, index):
    import trainers

    state = previous if previous is not None else trainers.start(index, eco, eco["day"] - 1)
    events = trainers.advance(state, eco, index, entry.get("proposal"))
    return state, events


def trainer_index(db):
    import trainers

    manifest, = db.execute("SELECT document FROM starting_manifest WHERE slot=1").fetchone()
    origin, = db.execute("SELECT entry FROM ecology_inputs WHERE id='origin'").fetchone()
    return trainers.build_index(json.loads(manifest), json.loads(origin)["protected"])


def apply(db, entries):
    import trainers

    state = None
    for key, entry in entries:
        payload = encoded(entry)
        if not db.execute("INSERT OR IGNORE INTO ecology_inputs VALUES (?,?)", (key, payload)).rowcount:
            if db.execute("SELECT entry FROM ecology_inputs WHERE id=?", (key,)).fetchone() != (payload,):
                raise ValueError("Divergent ecological input")
            continue
        if state is None:
            state = read_state(db)
        if "day" in entry:
            evolve_day(state, entry["day"])
            if entry.get("trainer_phase") == 1:
                projection, events = trainer_day(state, trainers.load(db), entry, trainer_index(db))
                trainers.write(db, projection, events)
        elif "wild_native" in entry:
            native_wild(state, entry["wild_native"])
        elif "trainer_native" in entry:
            projection = trainers.load(db)
            if not projection:
                raise ValueError("Projection has no companion trainer state")
            trainers.observe_native(projection, entry["trainer_native"])
            db.execute("UPDATE trainer_state SET document=? WHERE slot=1", (encoded(projection),))
        else:
            observe(state, entry["event"], key)
    if state is not None:
        write_state(db, state)


def replay(db):
    import trainers

    origin = json.loads(db.execute("SELECT entry FROM ecology_inputs WHERE id='origin'").fetchone()[0])
    manifest = json.loads(db.execute("SELECT document FROM starting_manifest WHERE slot=1").fetchone()[0])
    state = initial_state(manifest, origin["protected"], origin["tick"], Limits(**origin["limits"]))
    projection, index = None, None
    has_trainers = trainers.load(db)
    for key, raw in db.execute("SELECT id, entry FROM ecology_inputs WHERE id!='origin' ORDER BY rowid"):
        entry = json.loads(raw)
        if "day" in entry:
            evolve_day(state, entry["day"])
            if entry.get("trainer_phase") == 1:
                if index is None:
                    index = trainers.build_index(manifest, origin["protected"])
                projection, events = trainer_day(state, projection, entry, index)
                if not has_trainers or db.execute("SELECT events FROM trainer_journal WHERE day=?",
                                                (entry["day"],)).fetchone() != (encoded(events),):
                    raise ValueError("Trainer action replay differs from the persisted journal")
        elif "wild_native" in entry:
            native_wild(state, entry["wild_native"])
        elif "trainer_native" in entry:
            if not projection:
                raise ValueError("Replay has no companion trainer state")
            trainers.observe_native(projection, entry["trainer_native"])
        else:
            observe(state, entry["event"], key)
    if state != read_state(db) or projection != has_trainers:
        raise ValueError("Ecology or trainer replay differs from the persisted projection")
    return state


def monitor(state):
    rows = []
    count = totals(state)
    for key, habitat in state["habitats"].items():
        if not state["groups"][key]:
            continue
        rows.append(dict(id=key, habitat=habitat["name"], terrain=habitat["environment"], population=count[key],
                         capacity=sum(pool["capacity"] for pool in habitat["simulated"]["layers"].values()),
                         trend=state["trends"].get(key), groups=state["groups"][key]))
    return dict(status="ready" if state["protected_policy"] else "protected_policy_unavailable",
                day=state["day"], simulated_season=SEASONS[state["day"] // 90 % 4],
                habitats=rows, migrations_in_transit=state["transit"],
                notable_simulated=list(state["individuals"].values()), npc_sightings=state["sightings"],
                ecological_events=[row for row in state["history"] if row.get("source") != "native_observation"][-15:],
                native_observations=[row for row in state["history"] if row.get("source") == "native_observation"][-15:],
                native_observation_counts=state["native_counts"], ecological_event_counts=state["event_counts"])


def native_individuals(db):
    if not db.execute("SELECT 1 FROM sqlite_master WHERE name='observed_pokemon'").fetchone():
        return []
    return [dict(id=uid, owner=owner, map=json.loads(location), attributes=json.loads(attributes),
                 event=event, origin="native_observed")
            for uid, owner, location, attributes, event in db.execute(
                "SELECT id,owner,location,attributes,last_event FROM observed_pokemon p "
                "WHERE owner IS NULL OR EXISTS(SELECT 1 FROM observed_aliases a WHERE a.individual=p.id) "
                "ORDER BY rowid DESC LIMIT 12")]
