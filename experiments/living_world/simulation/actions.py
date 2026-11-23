"""Primitive actions and whole-world rules shared by every simulation writer."""

from collections import Counter
from dataclasses import dataclass


class Rejected(ValueError):
    """Stable rejection code suitable for the journal and planning feedback."""


def require(condition, reason):
    if not condition:
        raise Rejected(reason)


def integer(value, lower=0, upper=1_000_000_000):
    return type(value) is int and lower <= value <= upper


def reachable(world, start, *, protected=False):
    found = {start}
    queue = [start]
    routes = world["routes"].values()
    for here in queue:
        for route in routes:
            if not route["open"] or (protected and not route["required"]):
                continue
            there = route["b"] if route["a"] == here else route["a"] if route["b"] == here else None
            if there and there not in found and world["locations"][there]["accessible"]:
                found.add(there)
                queue.append(there)
    return found


def validate(world):
    from .region import ITEMS, SKILLS

    locations, people, firms = (world[key] for key in ("locations", "people", "firms"))
    for r in world["routes"].values():
        require(r["a"] in locations and r["b"] in locations and r["a"] != r["b"]
                and integer(r["hours"], 1, 24), "invalid_route")
        require(not r["required"] or r["open"], "required_connection")
    homes = Counter(p["home"] for p in people.values() if p["home"] is not None)
    jobs = Counter(p["employer"] for p in people.values() if p["employer"] is not None)
    for key, location in locations.items():
        require(location["owner"] is None or location["owner"] in people, "invalid_property_owner")
        require(integer(location["capacity"]) and homes[key] <= location["capacity"],
                "property_full")
    for person in people.values():
        require(person["location"] in locations and locations[person["location"]]["accessible"],
                "invalid_location")
        require(person["home"] is None or (person["home"] in locations and
                locations[person["home"]]["kind"] == "home"), "invalid_home")
        require(person["employer"] is None or person["employer"] in firms, "invalid_employer")
        require(integer(person["energy"], 0, 5), "invalid_energy")
        require(all(skill in SKILLS and integer(level, 1, 5) for skill, level in person["skills"].items()),
                "invalid_skill")
        require(all(peer in people and integer(trust, -5, 5)
                    for peer, trust in person["relationships"].items()), "invalid_relationship")
        if travel := person["transit"]:
            require(travel["to"] in locations and locations[travel["to"]]["accessible"]
                    and integer(travel["due"], world["tick"] + 1), "invalid_transit")
    for key, firm in firms.items():
        require(firm["owner"] in people and firm["location"] in locations, "invalid_firm")
        require(integer(firm["jobs"]) and jobs[key] <= firm["jobs"], "jobs_full")
        require(set(firm["members"]) <= people.keys(), "invalid_membership")
        require(all(firm["goods"].get(item, 0) >= amount
                    for item, amount in firm["floor"].items()), "essential_stock")
    for holder in (*people.values(), *firms.values()):
        require(integer(holder["money"]), "invalid_balance")
        require(all(item in ITEMS and integer(amount) for item, amount in holder["goods"].items()),
                "invalid_inventory")
    require(sum(p["money"] for p in people.values()) + sum(f["money"] for f in firms.values())
            + sum(p["amount"] for p in world["pending"] if p["kind"] == "wage")
            == world["issued_money"], "currency_conservation")
    for entry in world["pokemon"].values():
        require(entry["owner"] in people and entry["species"] == "PIDGEY"
                and integer(entry["practice"], 0, 100), "invalid_pokemon")
    for town, services in world["requirements"].items():
        available = reachable(world, town, protected=True)
        require(world["requirements"].keys() <= available, "required_town_unreachable")
        require(set(services.values()) <= available, "essential_service_unreachable")
        require(services["shopping"] in firms, "essential_shop_missing")
        for kind, place in services.items():
            require(locations[place]["town"] == town and locations[place]["kind"] == kind,
                    "required_facility_mismatch")
    for request in world["requests"].values():
        require(request["from"] in people and request["to"] in people, "invalid_request")


def cash(source, target, amount):
    require(source["money"] >= amount, "insufficient_money")
    source["money"] -= amount
    target["money"] += amount


def move_goods(source, target, item, count):
    stock = source["goods"].get(item, 0)
    require(stock - source.get("floor", {}).get(item, 0) >= count, "insufficient_tradeable_stock")
    source["goods"][item] = stock - count
    target["goods"][item] = target["goods"].get(item, 0) + count


def tell(person, key, source, tick):
    person["known"][key] = {"source": source, "tick": tick}


def remember(person, entry):
    person["memories"] = [*person["memories"][-11:], entry]


@dataclass(frozen=True)
class Primitive:
    parameters: dict
    description: str
    apply: object


def travel(world, actor, person, to):
    require(to in world["locations"] and world["locations"][to]["accessible"], "unknown_destination")
    here = person["location"]
    paths = [route for route in world["routes"].values()
             if route["open"] and {route["a"], route["b"]} == {here, to}]
    require(paths, "no_open_connection")
    hours = min(route["hours"] for route in paths)
    person["transit"] = dict(to=to, due=world["tick"] + hours)
    return dict(departed=here, destination=to, arrival=world["tick"] + hours)


def local_peer(world, actor, person, peer):
    require(peer != actor and peer in world["people"], "unknown_peer")
    other = world["people"][peer]
    require(not other["transit"] and other["location"] == person["location"], "peer_not_present")
    return other


def communicate(world, actor, person, peer, fact):
    other = local_peer(world, actor, person, peer)
    require(fact in person["known"], "unknown_fact")
    tell(other, fact, actor, world["tick"])
    world["wake"][peer] = world["tick"]
    return dict(heard=fact, speaker=actor, listener=peer)


def request(world, actor, person, peer, skill):
    local_peer(world, actor, person, peer)
    from .region import SKILLS
    require(skill in SKILLS, "unknown_skill")
    key = f"{actor}|{peer}|{skill}"
    require(world["requests"].get(key, {}).get("status") != "open", "already_requested")
    world["requests"][key] = {"from": actor, "to": peer, "skill": skill,
                              "status": "open", "expires": world["tick"] + 24}
    world["wake"][peer] = world["tick"]
    return dict(request=key, status="open")


def respond(world, actor, person, peer, skill, decision):
    other = local_peer(world, actor, person, peer)
    key = f"{peer}|{actor}|{skill}"
    record = world["requests"].get(key)
    require(record and record["status"] == "open", "no_open_request")
    require(decision in ("teach", "decline"), "unknown_response")
    if decision == "teach":
        level = other["skills"].get(skill, 0)
        require(person["skills"].get(skill, 0) > level and person["energy"] > 0,
                "cannot_teach_skill")
        other["skills"][skill] = level + 1
        person["energy"] -= 1
        other["relationships"][actor] = min(5, other["relationships"].get(actor, 0) + 1)
    record["status"] = decision
    world["wake"][peer] = world["tick"]
    remember(other, dict(tick=world["tick"], peer=actor, result=decision, skill=skill))
    return dict(request=key, status=decision)


def give(world, actor, person, peer, item, count):
    other = local_peer(world, actor, person, peer)
    move_goods(person, other, item, count)
    world["wake"][peer] = world["tick"]
    return dict(recipient=peer, item=item, count=count)


def local_firm(world, person, firm):
    business = world["firms"].get(firm)
    require(business and business["location"] == person["location"], "firm_not_here")
    return business


def trade(world, actor, person, firm, item, count, side):
    business = local_firm(world, person, firm)
    require(item in business["prices"], "item_not_traded")
    require(side in ("buy", "sell"), "invalid_trade_side")
    buyer, seller = (person, business) if side == "buy" else (business, person)
    price = business["prices"][item] if side == "buy" else max(1, business["prices"][item] - 2)
    cash(buyer, seller, price * count)
    move_goods(seller, buyer, item, count)
    return dict(side=side, item=item, count=count, paid=price * count, firm=firm)


def employment(world, actor, person, firm):
    business = local_firm(world, person, firm)
    require(person["employer"] != firm, "already_employed_here")
    require(business["skill"] in person["skills"], "skill_required")
    require(sum(p["employer"] == firm for p in world["people"].values()) < business["jobs"],
            "no_vacancy")
    old = person["employer"]
    person["employer"] = firm
    return dict(previous=old, employer=firm)


def work(world, actor, person):
    firm = person["employer"]
    require(firm is not None, "unemployed")
    business = local_firm(world, person, firm)
    require(person["energy"] > 0, "needs_rest")
    require(business["money"] >= business["wage"], "employer_cannot_pay")
    business["money"] -= business["wage"]
    person["energy"] -= 1
    person["ready"] = world["tick"] + 4
    world["pending"].append(dict(kind="wage", actor=actor, firm=firm, due=person["ready"],
                                  amount=business["wage"]))
    return dict(shift_until=person["ready"], firm=firm)


def release(world, actor, person, firm, peer):
    business = local_firm(world, person, firm)
    require(business["owner"] == actor, "owner_required")
    require(peer in world["people"] and world["people"][peer]["employer"] == firm, "not_employee")
    other = world["people"][peer]
    require(other["ready"] <= world["tick"], "work_in_progress")
    other["employer"] = None
    world["wake"][peer] = world["tick"]
    return dict(released=peer, firm=firm)


def rent(world, actor, person, home):
    place = world["locations"].get(home)
    require(place and place["kind"] == "home" and person["location"] == home, "home_not_here")
    require(person["home"] != home, "already_live_here")
    require(sum(p["home"] == home for p in world["people"].values()) < place["capacity"],
            "property_full")
    # Unowned dwellings have no landlord and charge no rent.
    if place["owner"] is not None and place["owner"] != actor:
        cash(person, world["people"][place["owner"]], place["rent"])
    old = person["home"]
    person["home"] = home
    return dict(previous_home=old, home=home)


def establish(world, actor, person, name, kind, capital):
    from .region import ITEMS
    require(kind in ("association", "business"), "invalid_organization_type")
    site = world["locations"][person["location"]]
    require(site["kind"] == "town", "public_registration_site_required")
    require(kind != "business" or ("retail" in person["skills"] and capital >= 10),
            "business_needs_skill_and_capital")
    key = f"firm:{actor}:{name}"
    require(key not in world["firms"], "duplicate_organization")
    business = dict(name=name, location=person["location"], owner=actor, kind=kind,
                    money=0, goods={}, prices=dict.fromkeys(ITEMS, 5) if kind == "business" else {},
                    wage=5, jobs=1 if kind == "business" else 0,
                    floor={}, members=[actor], skill="retail")
    cash(person, business, capital)
    world["firms"][key] = business
    return dict(established=key, capital=capital)


def join(world, actor, person, firm):
    business = local_firm(world, person, firm)
    require(business["kind"] == "association", "membership_unavailable")
    require(actor not in business["members"], "already_member")
    business["members"].append(actor)
    return dict(joined=firm)


def train(world, actor, person, pokemon):
    entry = world["pokemon"].get(pokemon)
    require(entry and entry["owner"] == actor, "pokemon_not_owned")
    require(person["energy"] > 0 and entry["practice"] < 100, "cannot_train")
    person["energy"] -= 1
    entry["practice"] += 1
    return dict(pokemon=pokemon, practice=entry["practice"])


def rest(world, actor, person):
    require(person["energy"] < 5, "already_rested")
    person["energy"] = 5
    person["ready"] = world["tick"] + 6
    return dict(rest_until=person["ready"])


def modification(world, actor, person, route):
    connection = world["routes"].get(route)
    require(connection and person["location"] in (connection["a"], connection["b"]), "route_not_here")
    require(not connection["required"], "required_connection")
    require(not connection["open"], "route_already_open")
    # A report enables later policy or player review. No unvetted map edit.
    key = f"repair:{route}"
    require(key not in world["events"], "already_reported")
    world["events"][key] = dict(kind="repair_proposed", location=person["location"],
                                route=route, tick=world["tick"], actor=actor)
    return dict(proposed=key)


ACTIONS = {
    "travel": Primitive(dict(to=str), "Start a direct trip. A traveler cannot act until arrival.", travel),
    "communicate": Primitive(dict(peer=str, fact=str), "Share a known fact with a present peer.", communicate),
    "request": Primitive(dict(peer=str, skill=str), "Ask a present peer to teach a skill.", request),
    "respond": Primitive(dict(peer=str, skill=str, decision=str), "Teach or decline an open request.", respond),
    "give": Primitive(dict(peer=str, item=str, count=int), "Donate your own goods to a present peer.", give),
    "trade": Primitive(dict(firm=str, item=str, count=int, side=str), "Buy or sell onsite at the listed price.", trade),
    "employment": Primitive(dict(firm=str), "Take an open onsite job if qualified. Releases prior job.", employment),
    "work": Primitive({}, "Work four hours onsite, spending one energy and earning a wage on completion.", work),
    "release": Primitive(dict(firm=str, peer=str), "As owner, release an employee outside their shift.", release),
    "rent": Primitive(dict(home=str), "Lease a vacant bed while onsite. Releases prior room.", rent),
    "establish": Primitive(dict(name=str, kind=str, capital=int), "Register an association or business from a town square.", establish),
    "join": Primitive(dict(firm=str), "Join a local association.", join),
    "train": Primitive(dict(pokemon=str), "Spend energy to practice with your Pokémon. No ROM experience.", train),
    "rest": Primitive({}, "Restore energy over six hours.", rest),
    "modification": Primitive(dict(route=str), "Report a closed optional route for repair.", modification),
}


def check_action(action):
    require(isinstance(action, dict) and isinstance(action.get("verb"), str), "malformed_action")
    spec = ACTIONS.get(action["verb"])
    require(spec is not None, "unknown_action")
    arguments = {key: value for key, value in action.items() if key != "verb"}
    require(arguments.keys() == spec.parameters.keys(), "wrong_action_arguments")
    for key, kind in spec.parameters.items():
        value = arguments[key]
        require((kind is str and isinstance(value, str) and 0 < len(value) <= 160
                 and value.isprintable() and (key != "name" or value.replace("_", "").isalnum()))
                or (kind is int and integer(value, 0 if key == "capital" else 1, 100)),
                "invalid_action_argument")
    return spec, arguments


def apply(world, actor, action):
    spec, arguments = check_action(action)
    require(actor in world["people"], "unknown_actor")
    person = world["people"][actor]
    require(not person["transit"], "in_transit")
    require(person["ready"] <= world["tick"], "occupied")
    if action["verb"] in ("give", "trade"):
        from .region import ITEMS
        require(arguments["item"] in ITEMS, "unknown_item")
    return spec.apply(world, actor, person, **arguments)
