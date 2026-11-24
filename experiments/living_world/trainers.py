"""Companion trainer actions and deterministic arbitration on the live ecology clock."""
from collections import Counter
from dataclasses import dataclass
import json
from types import SimpleNamespace

from profiles import PROFILES

# Companion policy. Each native object label must also occur in the compiled catalog.
POLICY = {
    "route_scout": ("Route1", "Route1_EventScript_Boy", 14, "survey_habitats", 35),
    "viridian_student": ("ViridianCity", "ViridianCity_EventScript_Youngster", 7, "study_bug_partners", 20),
    "sammy": ("ViridianForest", "ViridianForest_EventScript_Sammy", 7, "develop_a_partner", 50),
}
CORRIDORS = {frozenset(("PalletTown", "Route1")), frozenset(("Route1", "ViridianCity"))}
REVERSE = {1: 2, 2: 1, 3: 4, 4: 3}
BALL_PRICE, JOB_PAY, TRAIN_COST = 40, 32, 12
MAX_LEVEL, STORAGE_SLOTS, SIGHT_DAYS = 16, 18, 14
SCHEMA = (
    "CREATE TABLE IF NOT EXISTS trainer_state(slot INTEGER PRIMARY KEY CHECK(slot=1), document TEXT NOT NULL)",
    "CREATE TABLE IF NOT EXISTS trainer_journal(day INTEGER PRIMARY KEY, events TEXT NOT NULL)",
)


@dataclass(frozen=True)
class Step:
    action: str
    target: str


def build_index(manifest, protected):
    from ecology import map_key

    maps = {map_key(row["id"]): row for row in manifest["maps"]}
    roster = {row["id"]: row for row in manifest.get("trainers", ())}
    actors, edges, levels = {}, {}, {}
    forbidden = set(protected or ())
    for scene in manifest["static_encounters"]:
        for mon in scene["party"]:
            forbidden.update((mon.get("species"), mon.get("authored", {}).get("species")))
    species = {row["id"]: row for row in manifest["species"]
               if row["id"] not in forbidden and row.get("status") == "resolved"
               and 1 <= row["authored"].get("catch_rate", 0) <= 255 and any(row.get("abilities", ()))}
    if protected is None:
        return dict(actors={}, edges={}, species={}, levels={}, markets=set())

    def name(row):
        # Several compiled symbols can alias this header. Verify its outdoor
        # map placement by two distinct, authored Pallet objects.
        labels = {label for obj in row["objects"] for label in obj.get("labels", ())}
        if {"PalletTown_EventScript_SignLady", "PalletTown_EventScript_FatMan"} <= labels:
            return "PalletTown"
        return row["name"]

    for key, row in maps.items():
        if row.get("access", {}).get("vidra_section") is not False:
            continue
        for actor, (home, script, affinity, ambition, skill) in POLICY.items():
            if row["name"] != home:
                continue
            objects = [obj for obj in row["objects"] if script in obj.get("labels", ())]
            if len(objects) != 1 or actor in actors:
                continue
            binding = objects[0].get("binding") or {}
            native_id = binding.get("trainer")
            if actor == "sammy" and binding.get("opcode") == 0x5C and "trainer_local" not in binding:
                # Upgrade this one reviewed historical binding. Keep the
                # immutable Phase 19 manifest exactly as it was.
                native_id = 104 if native_id == 104 << 8 and binding.get("battle_script_mode") == 4 else None
            native = roster.get(native_id)
            if actor == "sammy" and (not native or native.get("protected") or native_id != 104
                                     or binding.get("battle_script_mode") != 4):
                continue
            if actor != "sammy" and "trainer" in binding:
                continue
            profile = PROFILES.get(actor, {})
            actors[actor] = dict(name=profile.get("name", "Bug Catcher Sammy"), home=key,
                                 preferences=dict(type=affinity, species=profile.get("favorite_species")),
                                 personality=list(profile.get("traits", ("patient", "competitive"))),
                                 ambition=ambition, competence=skill, native_script=script, native_roster=native)
        for edge in row["connections"]:
            dest = map_key(edge["target"])
            other = maps.get(dest)
            if (not other or other.get("access", {}).get("vidra_section") is not False
                    or frozenset((name(row), name(other))) not in CORRIDORS
                    or row.get("map_type") not in (1, 2, 3) or other.get("map_type") not in (1, 2, 3)):
                continue
            if any(link["target"] == row["id"] and link["offset"] == -edge["offset"]
                   and link["direction"] == REVERSE.get(edge["direction"]) for link in other["connections"]):
                edges.setdefault(key, {})[dest] = 1 + min(2, abs(edge["offset"]) // 24)
    for encounter in manifest["encounters"]:
        table = encounter["table"]
        if table["kind"] != "land":
            continue
        for slot in encounter["slots"]:
            if slot["status"] == "resolved":
                levels.setdefault((map_key(table["map"]), slot["species"]), []).extend(slot["level"])
    markets = {key for key, row in maps.items() if row["name"] == "ViridianCity"}
    return dict(actors=actors, edges=edges, species=species, levels=levels, markets=markets)


def start(index, eco, day, profiles=None):
    profiles = index["actors"] if profiles is None else profiles
    return dict(world=eco["world"], day=day, version=1, mons={}, recent=[],
                counters={}, request=None, actors={
                    key: dict(profile=profile, location=profile["home"], cash=64, balls=3,
                              resources=dict(grant_cash=64, grant_balls=3, earned=0, spent=0,
                                             balls_bought=0, balls_used=0),
                              experience=0, journeys=0, party=[], storage=[], goal=profile["ambition"],
                              activity="opening_companion_grant", sighting=None, journey=None,
                              fatigue=0, decisions=[], notices=[], plans=[], practice_day=None,
                              contacts={"viridian_student": 40} if key == "route_scout" else
                              {"route_scout": 40} if key == "viridian_student" else {})
                    for key, profile in sorted(profiles.items())})


def record(state, events, actor, kind, **data):
    row = dict(actor=actor, kind=kind, day=state["day"], location=state["actors"][actor]["location"],
               source="companion_simulation", **data)
    events.append(row)
    state["recent"].append(row)
    del state["recent"][:-60]
    state["counters"][kind] = state["counters"].get(kind, 0) + 1
    if kind in {"capture", "capture_failed", "evolution", "scout"}:
        a = state["actors"][actor]
        a["notices"].append(row)
        del a["notices"][:-5]


def available(state, eco, index, actor):
    a = state["actors"][actor]
    loc, day = a["location"], state["day"]
    if a["journey"] or a["practice_day"] == day:
        return ()
    choices = [Step("REST", "")]
    land = eco["groups"].get(loc, {}).get("land", {})
    if loc in index["markets"] and a["cash"] >= BALL_PRICE and a["balls"] < 8:
        choices.append(Step("BUY_BALL", "poke_ball"))
    if a["fatigue"] >= 3:
        return tuple(choices)
    if a["cash"] < 256:
        choices.append(Step("TRAINER_WORK", "local_odd_job"))
    for dest in sorted(index["edges"].get(loc, {})):
        choices.append(Step("EXPLORE_TRAVEL", dest))
    if land:
        choices.append(Step("SCOUT_HABITAT", loc))
    sight = a["sighting"]
    if (sight and sight["location"] == loc and day - sight["day"] <= SIGHT_DAYS and a["balls"]
            and len(a["party"]) + len(a["storage"]) < 6 + STORAGE_SLOTS):
        choices.append(Step("ATTEMPT_CAPTURE", str(sight["species"])))
    partner = (min(a["party"], key=lambda uid: (state["mons"][uid]["level"], uid))
               if a["party"] else None)
    if partner and (a["cash"] >= TRAIN_COST and state["mons"][partner]["level"] < MAX_LEVEL
                    and state["mons"][partner]["fatigue"] < 2):
        choices.append(Step("DEVELOP_PARTNER", partner))
    if a["storage"]:
        change = rotation(state, index, a)
        if change:
            choices.append(Step("ROTATE_PARTY", change[0]))
    for contact in sorted(a["contacts"]):
        other = state["actors"].get(contact)
        if (other and other["location"] == loc and not other["journey"] and sight
                and sight["source"] == actor and day - sight["day"] <= SIGHT_DAYS
                and (not other["sighting"] or other["sighting"]["day"] < sight["day"])):
            choices.append(Step("REPORT_SIGHTING", contact))
        if (other and other["location"] == loc and other["party"] and partner and not other["journey"]
                and other["fatigue"] < 2 and other["practice_day"] != day and a["contacts"][contact] >= 40
                and (not other["decisions"] or other["decisions"][-1]["day"] < day)
                and state["mons"][partner]["fatigue"] == 0
                and state["mons"][other["party"][0]]["fatigue"] == 0):
            choices.append(Step("SPAR_PRACTICE", contact))
    return tuple(choices)


def rotation(state, index, a):
    pref = a["profile"]["preferences"]
    party, storage = a["party"], a["storage"]
    roster = state["mons"]
    types = {uid: index["species"][roster[uid]["species"]]["authored"]["types"]
             for uid in party + storage}

    def score(team):
        diversity = set().union(*(set(types[uid]) for uid in team))
        favor = sum(32 * (roster[uid]["species"] == pref["species"]) + 16 * (pref["type"] in types[uid])
                    + roster[uid]["level"] for uid in team)
        return favor + 8 * len(diversity)

    best, change = score(party), None
    demotions = party if len(party) == 6 else (None,)
    for incoming in sorted(storage):
        for outgoing in demotions:
            value = score([uid for uid in party if uid != outgoing] + [incoming])
            if value > best:
                best, change = value, (incoming, outgoing)
    return change


def recent_moves(row, level, prior=(), after=0):
    moves = list(prior)
    for move, at in sorted(row.get("learnset", ()), key=lambda entry: entry[1]):
        if move > 0 and after < at <= level and move not in moves:
            moves.append(move)
    return moves[-4:]


def capture(state, eco, index, actor, target, events):
    from ecology import draw, note

    a = state["actors"][actor]
    loc, day = a["location"], state["day"]
    sight, species = a["sighting"], int(target)
    row = index["species"].get(species)
    land = eco["groups"].get(loc, {}).get("land", {})
    notable = eco["individuals"].get(sight.get("individual"))
    if notable and (notable["location"], notable["layer"], int(notable["species"])) != (loc, "land", species):
        notable = None
    eligible = row and (notable if sight.get("individual") else land.get(target, 0) > 0)
    if not eligible:
        a["sighting"] = None
        record(state, events, actor, "sighting_unconfirmed", species=species)
        return
    a["balls"] -= 1
    a["resources"]["balls_used"] += 1
    a["fatigue"] += 1
    attempt = a["resources"]["balls_used"]
    condition = 30 + draw(eco["seed"], actor, day, "condition") % 71
    odds = min(925, row["authored"]["catch_rate"] * 2 + a["profile"]["competence"] * 3
               + min(90, a["experience"]) + (100 - condition) * 2 + sight["confidence"])
    if draw(eco["seed"], actor, day, "capture", attempt) % 1000 >= odds:
        record(state, events, actor, "capture_failed", species=species, condition=condition, odds_per1000=odds)
        a["experience"] += 1
        return
    uid = sight["individual"] if notable else f"trainer-wild:{state['world']}:{actor}:{attempt}"
    if uid in state["mons"]:
        raise ValueError("Companion individual is already owned")
    if notable:
        del eco["individuals"][uid]
        # Old patrol reports cannot transfer that individual again.
        eco["sightings"] = {npc: report for npc, report in eco["sightings"].items()
                            if report.get("individual") != uid}
    else:
        land[target] -= 1
    bounds = index["levels"].get((loc, species))
    if not bounds:
        bounds = [1, 1]  # Companion starting level for a non-native migrant.
    low = min(MAX_LEVEL, max(1, min(bounds)))
    high = min(MAX_LEVEL, max(low, max(bounds)))
    level = low + draw(eco["seed"], actor, day, "level", attempt) % (high - low + 1)
    slots = [(i, ability) for i, ability in enumerate(row["abilities"]) if ability]
    ability_slot, ability = slots[draw(eco["seed"], actor, day, "ability", attempt) % len(slots)]
    state["mons"][uid] = dict(id=uid, owner=actor, species=species, form_key=species,
                              origin="ecology_notable" if notable else "ecology_aggregate",
                              captured=day, captured_at=loc, level=level, ability=ability, ability_slot=ability_slot,
                              moves=recent_moves(row, level), xp=0, fatigue=0,
                              starter_level_source="native_land_range" if (loc, species) in index["levels"]
                              else "companion_migrant_policy")
    (a["party"] if len(a["party"]) < 6 else a["storage"]).append(uid)
    a["experience"] += 3
    a["sighting"] = None
    note(eco, "trainer_capture", loc, actor=actor, species=species, individual=uid)
    record(state, events, actor, "capture", species=species, individual=uid, condition=condition,
           odds_per1000=odds)


def develop(state, index, actor, uid, events):
    a = state["actors"][actor]
    mon = state["mons"][uid]
    a["cash"] -= TRAIN_COST
    a["resources"]["spent"] += TRAIN_COST
    a["fatigue"] += 1
    mon["fatigue"] += 1
    xp = 8 + min(8, a["experience"] // 4)
    a["experience"] += 1
    progress(state, index, actor, uid, xp, events)
    record(state, events, actor, "training", individual=uid, xp=xp, level=mon["level"], moves=mon["moves"])


def progress(state, index, actor, uid, xp, events):
    mon = state["mons"][uid]
    previous = mon["level"]
    if previous >= MAX_LEVEL:
        return
    mon["xp"] += xp
    if mon["xp"] < 20 + previous * 3:
        return
    mon["xp"] -= 20 + previous * 3
    mon["level"] += 1
    species = index["species"][mon["species"]]
    mon["moves"] = recent_moves(species, mon["level"], mon["moves"], previous)
    options = [row for row in species["authored"]["evolutions"]
               if row["method"] == 1 and not row["conditions"] and mon["level"] >= row["parameter"]
               and row["target"] in index["species"]]
    if len(options) != 1:
        return
    prior, target = mon["species"], options[0]["target"]
    replacement = index["species"][target]
    slots = [(i, ability) for i, ability in enumerate(replacement["abilities"]) if ability]
    slot, ability = next((pair for pair in slots if pair[0] == mon["ability_slot"]), slots[0])
    mon.update(species=target, form_key=target, ability=ability, ability_slot=slot,
               moves=recent_moves(replacement, mon["level"], mon["moves"], previous))
    record(state, events, actor, "evolution", individual=uid, previous=prior, species=target,
           level=mon["level"], moves=mon["moves"])


def practice(state, eco, index, actor, contact, events):
    from ecology import draw

    pair = []
    for key in (actor, contact):
        member = state["actors"][key]
        uid = min(member["party"], key=lambda id_: (state["mons"][id_]["level"], id_)) if key == actor else member["party"][0]
        mon = state["mons"][uid]
        stats = index["species"][mon["species"]]["authored"]["stats"]
        score = sum(stats) * mon["level"] + 5 * member["profile"]["competence"]
        score += draw(eco["seed"], state["day"], "practice", key) % 120
        pair.append((score, key, uid))
    _, winner, _ = max(pair)
    for _, key, uid in pair:
        a = state["actors"][key]
        mon = state["mons"][uid]
        a.update(activity="spar_practice", practice_day=state["day"], fatigue=a["fatigue"] + 1)
        mon["fatigue"] += 1
        xp = 8 if winner == key else 5
        progress(state, index, key, uid, xp, events)
        record(state, events, key, "spar_practice", individual=uid, xp=xp, winner=winner, level=mon["level"])



def execute(state, eco, index, actor, step, events):
    from ecology import draw

    a = state["actors"][actor]
    loc, day = a["location"], state["day"]
    action, target = step.action, step.target
    a["activity"] = action.lower()
    if action == "REST":
        a["fatigue"] = 0
        for uid in a["party"]:
            state["mons"][uid]["fatigue"] = 0
    elif action == "TRAINER_WORK":
        a["cash"] += JOB_PAY
        a["resources"]["earned"] += JOB_PAY
        a["fatigue"] += 1
        record(state, events, actor, "paid_odd_job", amount=JOB_PAY, employer="companion_local_services")
    elif action == "BUY_BALL":
        a["cash"] -= BALL_PRICE
        a["balls"] += 1
        a["resources"]["spent"] += BALL_PRICE
        a["resources"]["balls_bought"] += 1
        record(state, events, actor, "purchased_ball", amount=BALL_PRICE, shop="companion_viridian_supplier")
    elif action == "EXPLORE_TRAVEL":
        a["journey"] = dict(destination=target, arrival=day + index["edges"][loc][target])
        a["journeys"] += 1
        a["sighting"] = None
        record(state, events, actor, "travel", **a["journey"])
    elif action == "SCOUT_HABITAT":
        from ecology import active_weights

        pool = eco["habitats"][loc]["simulated"]["layers"]["land"]
        current = active_weights(eco, pool)
        candidates = [(int(species), None, count) for species, count in sorted(eco["groups"][loc]["land"].items())
                      if count > 0 and int(species) in index["species"]
                      and (species in current or species in pool.get("compatible_arrivals", ())) ]
        candidates.extend((int(mon["species"]), uid, 1) for uid, mon in sorted(eco["individuals"].items())
                          if mon["location"] == loc and mon["layer"] == "land"
                          and int(mon["species"]) in index["species"])
        if candidates:
            def rank(item):
                species, uid, count = item
                pref = a["profile"]["preferences"]
                types = index["species"][species]["authored"].get("types", ())
                return (draw(eco["seed"], actor, day, "spot", species, uid) % 600
                        + min(25, count) * 7 + (100 if pref["type"] in types else 0)
                        + (200 if pref["species"] == species else 0))
            species, uid, _ = max(candidates, key=rank)
            a["sighting"] = dict(species=species, individual=uid, location=loc, source=actor,
                                 day=day, confidence=80 if uid is None else 64)
            record(state, events, actor, "scout", **{k: v for k, v in a["sighting"].items()
                                                   if k not in {"location", "source", "day"}})
        else:
            a["sighting"] = None
            record(state, events, actor, "scout_no_sighting")
        a["fatigue"] += 1
    elif action == "ATTEMPT_CAPTURE":
        capture(state, eco, index, actor, target, events)
    elif action == "DEVELOP_PARTNER":
        develop(state, index, actor, target, events)
    elif action == "SPAR_PRACTICE":
        practice(state, eco, index, actor, target, events)
    elif action == "ROTATE_PARTY":
        candidate, demoted = rotation(state, index, a)
        if target != candidate:
            raise ValueError("Trainer chose an unavailable party rotation")
        a["storage"].remove(target)
        if demoted is not None:
            a["party"].remove(demoted)
            a["storage"].append(demoted)
        a["party"].append(target)
        record(state, events, actor, "party_rotation", promoted=target, demoted=demoted)
    elif action == "REPORT_SIGHTING":
        other = state["actors"][target]
        other["sighting"] = dict(a["sighting"], confidence=max(10, a["sighting"]["confidence"] - 25))
        other["contacts"][actor] = min(70, other["contacts"].get(actor, 35) + 1)
        record(state, events, actor, "shared_sighting", recipient=target, species=a["sighting"]["species"])


def priorities(state, eco, index, key, steps):
    from ecology import draw

    a = state["actors"][key]
    profile = a["profile"]
    loc = a["location"]
    party = a["party"]
    survey = profile["ambition"] == "survey_habitats"
    student = profile["ambition"] == "study_bug_partners"
    at_home = loc == profile["home"]
    sight = a["sighting"]
    owned = Counter(state["mons"][uid]["species"] for uid in party + a["storage"])
    prefer = profile["preferences"]
    scores = {"REST": 20 + 15 * a["fatigue"], "TRAINER_WORK": 70 if a["cash"] < 50 else 15,
              "BUY_BALL": 105 if not a["balls"] else 36, "EXPLORE_TRAVEL": 63 if survey else 35,
              "SCOUT_HABITAT": 68 if survey else 64, "ATTEMPT_CAPTURE": 81 if not survey else 61,
              "DEVELOP_PARTNER": 90 if not survey and not student else 67,
              "ROTATE_PARTY": 76, "REPORT_SIGHTING": 74 if survey else 60,
              "SPAR_PRACTICE": 76 if not survey else 55}
    if not party:
        scores["ATTEMPT_CAPTURE"] += 25
        scores["TRAINER_WORK"] -= 12
    if sight and sight["species"] in index["species"]:
        species = sight["species"]
        types = index["species"][species]["authored"]["types"]
        scores["ATTEMPT_CAPTURE"] += (22 if prefer["type"] in types or prefer["species"] == species else 0)
        scores["ATTEMPT_CAPTURE"] -= 30 * min(3, owned[species]) + 2 * len(party)
        scores["SCOUT_HABITAT"] -= 20 if a["balls"] else 10
    if not a["balls"]:
        scores["SCOUT_HABITAT"] -= 18
    if a["fatigue"] >= 3:
        scores["REST"] = 150
    if a["cash"] < TRAIN_COST and party:
        scores["TRAINER_WORK"] += 35
    if any(state["mons"][uid]["fatigue"] >= 2 for uid in party):
        scores["REST"] += 36

    def score(step):
        adjustment = 0
        if step.action == "EXPLORE_TRAVEL":
            if not a["balls"] and step.target in index["markets"]:
                adjustment = 62 if a["cash"] >= BALL_PRICE else 9
            elif a["balls"] and loc not in eco["groups"] and step.target in eco["groups"]:
                adjustment = 45
            elif a["balls"] and at_home and not eco["groups"].get(loc, {}).get("land"):
                adjustment = 30
        return scores[step.action] + adjustment + draw(eco["seed"], key, state["day"], step.action, step.target) % 23

    return sorted(steps, key=score, reverse=True)


def feasible_paths(steps):
    from planning import goals_for

    paths = {}
    rest = Step("REST", "")
    for step in steps:
        for goal in goals_for(step):
            paths.setdefault(goal, []).append((step,))
            if rest in steps and step.action in {"SCOUT_HABITAT", "DEVELOP_PARTNER", "SPAR_PRACTICE"}:
                paths[goal].append((rest, step))
    return paths


def request_plan(model, request):
    from planning import choose_plan

    steps = tuple(Step(*pair) for pair in request["steps"])
    ticket = SimpleNamespace(context=request["context"], cause="")
    persona = SimpleNamespace(role=request["name"], motive=request["motive"])
    planner = SimpleNamespace(plan_paths=lambda _, available: feasible_paths(available))
    proposal, _ = choose_plan(model, ticket, steps, persona, planner=planner, timeout=60, concise=True)
    return dict(day=request["day"], actor=request["actor"], goal=proposal.goal,
                steps=[[step.action, step.target] for step in proposal.steps])


def confirmed_plan(request, payload):
    if not request or not isinstance(payload, dict):
        return ()
    if (payload.get("day"), payload.get("actor")) != (request["day"], request["actor"]):
        return ()
    steps = payload.get("steps")
    if not isinstance(steps, list) or not 1 <= len(steps) <= 3:
        return ()
    if any(pair not in request["steps"] for pair in steps):
        return ()
    parsed = tuple(Step(*pair) for pair in steps)
    goal = payload.get("goal")
    if not isinstance(goal, str):
        return ()
    paths = feasible_paths(tuple(Step(*pair) for pair in request["steps"]))
    return parsed if parsed in paths.get(goal, ()) else ()


def advance(state, eco, index, proposal=None):
    from planning import goals_for

    day = eco["day"]
    if state["world"] != eco["world"] or state["day"] + 1 != day:
        raise ValueError("Trainer journal world or day mismatch")
    state["day"] = day
    events = []
    key = state["request"]["actor"] if state["request"] else None
    steps = confirmed_plan(state["request"], proposal)
    if steps:
        state["actors"][key]["plans"] = [[step.action, step.target] for step in steps]
        state["actors"][key]["goal"] = proposal["goal"]
        record(state, events, key, "model_plan_admitted", goal=proposal["goal"], steps=proposal["steps"])
    elif proposal is not None and key:
        record(state, events, key, "model_plan_rejected")
    state["request"] = None
    for key, a in state["actors"].items():
        if a["sighting"] and day - a["sighting"]["day"] > SIGHT_DAYS:
            a["sighting"] = None
        if a["practice_day"] == day:
            continue
        if a["journey"]:
            if day < a["journey"]["arrival"]:
                a["activity"] = "in_transit"
                continue
            a["location"] = a["journey"]["destination"]
            a["journey"] = None
            record(state, events, key, "arrived")
        report = eco["sightings"].get(key)
        if (report and report["location"] == a["location"] and report.get("species") in index["species"]
                and (not a["sighting"] or report["observed_day"] > a["sighting"]["day"])):
            a["sighting"] = dict(species=report["species"], individual=report.get("individual"),
                                 location=report["location"], source=report["source"],
                                 day=report["observed_day"], confidence=report["confidence"])
        choices = available(state, eco, index, key)
        step = Step(*a["plans"].pop(0)) if a["plans"] else None
        reason = "offline_qwen"
        if step not in choices:
            if step:
                record(state, events, key, "plan_became_unavailable", action=step.action, target=step.target)
                a["plans"] = []
            source = priorities(state, eco, index, key, choices)
            step, reason = source[0], "deterministic_policy"
            goals = goals_for(step)
            if goals and step.action != "REST":
                a["goal"] = goals[0]
        decision = dict(day=day, action=step.action, target=step.target, source=reason, goal=a["goal"])
        a["decisions"].append(decision)
        del a["decisions"][:-8]
        events.append(dict(decision, kind="trainer_decision", actor=key, location=a["location"]))
        execute(state, eco, index, key, step, events)

    actors = tuple(state["actors"])
    if actors and day % 5 == 1:
        key = actors[(day // 5) % len(actors)]
        a = state["actors"][key]
        choices = available(state, eco, index, key)
        if len(choices) >= 3 and not a["plans"]:
            fact = (f"Local sighting: species {a['sighting']['species']}."
                    if a["sighting"] else "No fresh sighting.")
            state["counters"]["decision_opportunities"] = state["counters"].get("decision_opportunities", 0) + 1
            preferred = a["profile"]["preferences"]
            motive = a["profile"]["ambition"].replace("_", " ")
            traits = ", ".join(a["profile"]["personality"])
            last = a["notices"][-1]["kind"].replace("_", " ") if a["notices"] else "none"
            choices = priorities(state, eco, index, key, choices)
            state["request"] = dict(day=day, actor=key, name=a["profile"]["name"],
                                    motive=f"{traits}. You want to {motive}.",
                                    context=f"Map {a['location']}, cash {a['cash']}, balls {a['balls']}, "
                                            f"party {len(a['party'])}, fatigue {a['fatigue']}. {fact} "
                                            f"Preference: species {preferred['species']}, type {preferred['type']}. "
                                            f"Last: {last}.",
                                    steps=[[step.action, step.target] for step in choices])
    return events


def load(db):
    if not db.execute("SELECT 1 FROM sqlite_master WHERE name='trainer_state'").fetchone():
        return None
    return read_state(db)


def read_state(db):
    row = db.execute("SELECT document FROM trainer_state WHERE slot=1").fetchone()
    return json.loads(row[0]) if row else None


def write(db, state, events):
    from ecology import encoded

    for statement in SCHEMA:
        db.execute(statement)
    db.execute("INSERT OR REPLACE INTO trainer_state VALUES (1,?)", (encoded(state),))
    db.execute("INSERT INTO trainer_journal VALUES (?,?)", (state["day"], encoded(events)))


def fact(state, npc):
    from knowledge import Fact

    a = state["actors"].get(npc)
    if not a:
        return None
    lines = {"capture": "I caught a wild Pokemon.", "capture_failed": "One got away from me.",
             "evolution": "My partner evolved!", "scout": "I spotted a wild Pokemon."}
    for report in reversed(a["notices"]):
        if report["location"] == a["profile"]["home"] and state["day"] - report["day"] <= SIGHT_DAYS:
            line = lines[report["kind"]]
            key = f"trainer:{npc}:{report['location']}:{report['day']}:{report['kind']}"
            return Fact(key, "rumor", line, line, key)
    return None
