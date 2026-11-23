"""SQLite transactions, an hourly world clock, and deterministic command replay."""

from contextlib import contextmanager
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import sqlite3

from .actions import (
    Rejected, apply, check_action, integer, reachable, remember, require, tell, validate,
)

HOURS_PER_DAY = 24
MAX_CATCH_UP = 31 * HOURS_PER_DAY
GOAL_FIELDS = {
    "employment": {"firm"}, "money": {"amount"}, "goods": {"item", "amount"},
    "skill": {"skill"}, "home": {"home"}, "location": {"location"}, "request": {"skill"},
    "teach": {"skill"}, "rested": set(), "practice": {"pokemon", "amount"},
}


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)


def digest(value):
    return hashlib.sha256(encoded(value).encode("ascii")).hexdigest()


def known_places(world, actor):
    person = world["people"][actor]
    here = person["location"]
    adjacent = set()
    for route in world["routes"].values():
        if here in (route["a"], route["b"]):
            adjacent.update((route["a"], route["b"]))
    return {here, *adjacent, *world["requirements"], *(
        p for p in world["locations"] if f"place:{p}" in person["known"])}


def observation(world, actor):
    person = world["people"][actor]
    here = person["location"]
    local = {key: {"name": p["name"], "trust": person["relationships"].get(key, 0)}
             for key, p in world["people"].items()
             if key != actor and p["location"] == here and not p["transit"]}
    visible = known_places(world, actor)
    routes = {k: v for k, v in world["routes"].items()
              if here in (v["a"], v["b"])}
    firms = {key: dict(location=firm["location"], kind=firm["kind"],
                       goods={item: count - firm["floor"].get(item, 0)
                              for item, count in firm["goods"].items()},
                       prices=firm["prices"], wage=firm["wage"], skill=firm["skill"],
                       vacancies=firm["jobs"] - sum(p["employer"] == key
                                                      for p in world["people"].values()))
             for key, firm in world["firms"].items() if firm["location"] == here}
    places = {key: {"kind": world["locations"][key]["kind"], "town": world["locations"][key]["town"]}
              for key in sorted(visible)}
    housing = {key: dict(vacancies=world["locations"][key]["capacity"] -
                         sum(p["home"] == key for p in world["people"].values()),
                         rent=world["locations"][key]["rent"] if world["locations"][key]["owner"] else 0)
               for key in visible if world["locations"][key]["kind"] == "home"}
    requests = {k: v for k, v in world["requests"].items()
                if actor in (v["to"], v["from"]) and v["status"] == "open"}
    events = {key: e for key, e in world["events"].items()
              if e["location"] == here or f"event:{key}" in person["known"]}
    return deepcopy(dict(revision=world["revision"], tick=world["tick"], actor=actor,
                         self={k: v for k, v in person.items() if k not in ("relationships", "controller")},
                         people=local, routes=routes, places=places, firms=firms, housing=housing,
                         requests=requests, events=events,
                         pokemon={k: v for k, v in world["pokemon"].items() if v["owner"] == actor}))


def goal_is_met(world, actor, goal):
    person = world["people"][actor]
    kind = goal["kind"]
    if kind == "employment":
        return person["employer"] == goal["firm"]
    if kind == "money":
        return person["money"] >= goal["amount"]
    if kind == "goods":
        return person["goods"].get(goal["item"], 0) >= goal["amount"]
    if kind == "skill":
        return goal["skill"] in person["skills"]
    if kind in ("location", "home"):
        return person[kind] == goal[kind] and not person["transit"]
    if kind in ("request", "teach"):
        return any(r["skill"] == goal["skill"] and
                   r["status"] == ("open" if kind == "request" else "teach") and
                   r["from" if kind == "request" else "to"] == actor
                   for r in world["requests"].values())
    if kind == "rested":
        return person["energy"] == 5
    return world["pokemon"].get(goal["pokemon"], {}).get("practice", 0) >= goal["amount"]


def check_goal(goal, obs):
    from .region import ITEMS, SKILLS

    require(isinstance(goal, dict) and isinstance(goal.get("kind"), str), "invalid_goal")
    fields = GOAL_FIELDS.get(goal["kind"])
    require(fields is not None and goal.keys() == fields | {"kind"}, "invalid_goal")
    allowed = dict(firm=obs["firms"], item=ITEMS, skill=SKILLS,
                   home=obs["housing"], location=obs["places"], pokemon=obs["pokemon"])
    for field in fields:
        if field == "amount":
            require(integer(goal[field], 1, 1000), "invalid_goal_amount")
        else:
            require(isinstance(goal[field], str) and goal[field] in allowed[field], "unknown_goal_target")


def observe_place(world, actor):
    person = world["people"][actor]
    here = person["location"]
    tell(person, f"place:{here}", actor, world["tick"])
    for key, event in world["events"].items():
        if event["location"] == here:
            tell(person, f"event:{key}", actor, world["tick"])


def incident(world, kind, target):
    tick = world["tick"]
    event_id = f"{tick}:{kind}:{target}"
    require(event_id not in world["events"], "duplicate_incident")
    if kind == "shortage":
        firm = world["firms"].get(target)
        require(firm and "POTION" in firm["floor"], "unsupported_event_target")
        before = firm["goods"]["POTION"]
        firm["goods"]["POTION"] = firm["floor"]["POTION"]
        data = dict(kind=kind, location=firm["location"], item="POTION",
                    removed=before - firm["goods"]["POTION"])
    elif kind == "route_closure":
        route = world["routes"].get(target)
        require(route and not route["required"] and route["open"], "required_or_closed_route")
        route["open"] = False
        world["pending"].append(dict(kind="reopen", route=target, due=tick + 12))
        data = dict(kind=kind, location=route["a"], route=target, ends=tick + 12)
    else:
        raise Rejected("unsupported_event")
    world["events"][event_id] = dict(data, tick=tick)
    for actor, p in world["people"].items():
        if p["location"] == data["location"] and not p["transit"]:
            tell(p, f"event:{event_id}", "witness", tick)
            world["wake"][actor] = tick
    return dict(event=event_id, **data)


def record_action(world, actor, action, effect):
    person = world["people"][actor]
    remember(person, {"tick": world["tick"], "action": action["verb"], "effect": effect})
    if action["verb"] != "travel":
        observe_place(world, actor)


def execute(world, actor, action):
    effect = apply(world, actor, action)
    record_action(world, actor, action, effect)
    validate(world)
    return effect


def settle(world):
    """Apply due obligations and arrivals using the same rules in forecasts."""
    tick = world["tick"]
    details = []
    due, waiting = [], []
    for task in world["pending"]:
        (due if task["due"] <= tick else waiting).append(task)
    world["pending"] = waiting
    for task in due:
        if task["kind"] == "wage":
            world["people"][task["actor"]]["money"] += task["amount"]
            details.append({"routine": "wage_paid", **task})
        elif task["kind"] == "reopen":
            world["routes"][task["route"]]["open"] = True
            details.append({"routine": "route_reopened", **task})
    for key, req in sorted(world["requests"].items()):
        if req["status"] == "open" and req["expires"] <= tick:
            req["status"] = "expired"
            world["wake"][req["from"]] = tick
            details.append(dict(routine="request_expired", request=key))
    for actor in sorted(world["people"]):
        p = world["people"][actor]
        transit = p["transit"]
        if transit and transit["due"] <= tick:
            p["location"] = transit["to"]
            p["transit"] = None
            observe_place(world, actor)
            details.append(dict(routine="arrived", actor=actor, location=p["location"]))
    return details


def clock(world):
    """Advance obligations first, then execute at most one pending step per actor."""
    world["tick"] += 1
    tick = world["tick"]
    details = settle(world)
    for actor in sorted(world["people"]):
        p = world["people"][actor]
        if p["transit"] or p["ready"] > tick:
            continue
        if p["plan"]:
            action = p["plan"][0]
            candidate = deepcopy(world)
            candidate["people"][actor]["plan"].pop(0)
            try:
                effect = execute(candidate, actor, action)
            except Rejected as error:
                p["plan"].clear()
                remember(p, dict(tick=tick, action=action["verb"], rejected=str(error)))
                world["wake"][actor] = tick
                details.append(dict(actor=actor, action=action, rejected=str(error)))
                continue
            world.update(candidate)
            p = world["people"][actor]
            details.append(dict(actor=actor, action=action, effect=effect))
        if p["goal"] and p["goal"]["status"] == "active":
            goal = p["goal"]["target"]
            if goal_is_met(world, actor, goal):
                p["goal"]["status"] = "met"
                details.append(dict(routine="goal_met", actor=actor, goal=goal))
            elif not p["plan"] and not p["transit"] and p["ready"] <= tick:
                world["wake"].setdefault(actor, tick + 6)
    if tick % HOURS_PER_DAY == 7:
        # Presence supplies provenance for encounters without generating dialogue.
        for actor, p in world["people"].items():
            if not p["transit"]:
                observe_place(world, actor)
                tell(p, f"place:{p['location']}", "local observation", tick)
    if tick % (HOURS_PER_DAY * 5) == 12:
        options = [("shortage", key) for key, firm in sorted(world["firms"].items()) if firm["floor"]]
        options += [("route_closure", key) for key, route in sorted(world["routes"].items())
                    if route["open"] and not route["required"]
                    and all(world["locations"][route[end]]["kind"] == "town" for end in ("a", "b"))]
        word = int(digest([world["seed"], tick])[:8], 16)
        if options:
            details.append(dict(routine="seeded_event", **incident(world, *options[word % len(options)])))
    return details


def preview(world, actor, steps):
    """Fail impossible steps in order, resolving only the actor's known delays."""
    trial = deepcopy(world)
    for step in steps:
        person = trial["people"][actor]
        arrival = person["transit"]["due"] if person["transit"] else trial["tick"]
        trial["tick"] = max(trial["tick"] + 1, arrival, person["ready"])
        settle(trial)
        execute(trial, actor, step)
    return trial


def forecast(state, actor, steps, target):
    # Never supply hypothetical destination observations. They become visible
    # after actual travel and can wake the actor for a follow-up turn.
    trial = preview(state, actor, steps)
    person = trial["people"][actor]
    trial["tick"] = max(trial["tick"], person["ready"])
    settle(trial)
    context = observation(trial, actor) if not person["transit"] else None
    if person["transit"]:
        trial["tick"] = person["transit"]["due"]
        settle(trial)
    return (goal_is_met(trial, actor, target), context)


def dispatch(world, command):
    kind = command["kind"]
    if kind == "tick":
        return clock(world)
    if kind == "native_roster":
        require(world.get("case") == "native_manifest" and command["source"] == "native_rom",
                "unauthorized")
        actors = {}
        for actor in world["people"].values():
            identity = (actor["location"], actor.get("native_trainer"))
            actors.setdefault(identity, []).append(actor)
        taught = 0
        for row in command["team"]:
            witnesses = actors.get((row["location"], row["trainer"]), [])
            if len(witnesses) == 1 and not witnesses[0]["transit"]:
                remember(witnesses[0], dict(tick=world["tick"], source="own_native_team",
                                            species=row["species"], slot=row["slot"]))
                taught += 1
        return dict(status="observed", participants=taught)
    if kind == "incident":
        require(command["source"] == "director", "unauthorized")
        return incident(world, command["event"], command["target"])
    actor = command["actor"]
    require(actor in world["people"], "unknown_actor")
    person = world["people"][actor]
    if kind == "action":
        require(command["source"] == person["controller"], "unauthorized")
        return execute(world, actor, command["action"])
    if kind == "decision":
        require(person["controller"] == "npc" and command["source"] in ("model", "unavailable"),
                "unauthorized")
        require(world["revision"] == command["observed_revision"], "stale_observation")
        require(not person["plan"] and not person["transit"] and person["ready"] <= world["tick"],
                "actor_unavailable")
        observation_now = observation(world, actor)
        require(observation_now == command["observation"], "observation_mismatch")
        world["wake"].pop(actor, None)
        if command["source"] == "unavailable":
            require(command["proposal"] is None, "unauthorized")
            world["wake"][actor] = world["tick"] + HOURS_PER_DAY
            return dict(status="idle", reason=command.get("evidence", {}).get("error", "model_unavailable"))
        proposal = command["proposal"]
        require(isinstance(proposal, dict) and proposal.keys() == {"ambition", "goal", "steps"},
                "malformed_proposal")
        ambition, goal, steps = (proposal[key] for key in ("ambition", "goal", "steps"))
        require(isinstance(ambition, str) and 1 <= len(ambition) <= 150 and ambition.isprintable(),
                "invalid_ambition")
        require(isinstance(steps, list) and len(steps) <= 12, "invalid_plan_length")
        if not person["goal"] or goal != person["goal"]["target"]:
            check_goal(goal, observation_now)
        for step in steps:
            check_action(step)
        preview(world, actor, steps)
        person["goal"] = dict(ambition=ambition, target=goal, status="active", updated=world["tick"])
        person["plan"] = deepcopy(steps)
        if not steps:
            world["wake"][actor] = world["tick"] + HOURS_PER_DAY
        return dict(status="queued", steps=len(steps), initially_met=goal_is_met(world, actor, goal))
    raise Rejected("unknown_command")


def evolve(state, command):
    state_after = deepcopy(state)
    try:
        effect = dispatch(state_after, command)
        validate(state_after)
    except (Rejected, KeyError, TypeError) as error:
        # Persist the failed decision and a bounded retry; discard its candidate.
        state_after = deepcopy(state)
        actor = command.get("actor")
        if (command.get("kind") == "decision" and isinstance(actor, str) and actor in state_after["people"] and
                command.get("observed_revision") == state["revision"]):
            remember(state_after["people"][actor], dict(tick=state["tick"], rejected=str(error)))
            state_after["wake"][actor] = state["tick"] + HOURS_PER_DAY
        result = dict(accepted=False, reason=str(error) if isinstance(error, Rejected) else "malformed_command")
    else:
        result = dict(accepted=True, effect=effect)
    state_after["revision"] += 1
    return state_after, result


class Simulation:
    def __init__(self, path, initial=None, *, read_only=False, manifest=None):
        path = Path(path).resolve() if path != ":memory:" else path
        self.db = sqlite3.connect(path.as_uri() + "?mode=ro" if read_only else path, uri=read_only)
        try:
            if not read_only and initial is not None:
                validate(initial)
                with self._write():
                    tables = {row[0] for row in self.db.execute(
                        "SELECT name FROM sqlite_master WHERE type='table'")}
                    existing = {"simulation", "journal"}
                    if manifest is not None:
                        existing.add("starting_manifest")
                    native_tables = {"native_streams", "native_events", "observed_pokemon",
                                     "observed_aliases", "observed_party", "native_ticks", "native_clock"}
                    allowed = (set(), existing, existing | native_tables) if manifest is not None else (set(), existing)
                    require(tables in allowed, "database_is_not_a_simulation")
                    self.db.execute("CREATE TABLE IF NOT EXISTS simulation (slot INTEGER PRIMARY KEY CHECK(slot=1), state TEXT NOT NULL)")
                    self.db.execute("CREATE TABLE IF NOT EXISTS journal (revision INTEGER PRIMARY KEY, entry TEXT NOT NULL)")
                    created = self.db.execute("INSERT OR IGNORE INTO simulation VALUES (1,?)",
                                              (encoded(initial),)).rowcount
                    if created:
                        self.db.execute("INSERT INTO journal VALUES (0,?)", (encoded(dict(initial=initial)),))
                    if manifest is not None:
                        self.db.execute("CREATE TABLE IF NOT EXISTS starting_manifest "
                                        "(slot INTEGER PRIMARY KEY CHECK(slot=1), document TEXT NOT NULL)")
                        document = encoded(manifest)
                        if created:
                            self.db.execute("INSERT INTO starting_manifest VALUES (1,?)", (document,))
                        else:
                            prior = self.db.execute("SELECT document FROM starting_manifest WHERE slot=1").fetchone()
                            require(prior == (document,), "starting_manifest_mismatch")
            require(self.state()["version"] == 1, "unsupported_simulation_schema")
            validate(self.state())
        except Exception:
            self.db.close()
            raise

    @contextmanager
    def _write(self):
        with self.db:
            self.db.execute("BEGIN IMMEDIATE")
            yield

    def state(self):
        row = self.db.execute("SELECT state FROM simulation WHERE slot=1").fetchone()
        require(row is not None, "missing_simulation")
        return json.loads(row[0])

    def snapshot(self):
        with self.db:
            self.db.execute("BEGIN")
            return self.state(), self.history()

    def history(self):
        return [json.loads(entry) for entry, in self.db.execute("SELECT entry FROM journal ORDER BY revision")]

    def command(self, command):
        # Round-tripping also snapshots caller-owned data and rejects NaN values.
        require(isinstance(command, dict), "malformed_command")
        command = json.loads(encoded(command))
        with self._write():
            return self._apply_command(command)

    def _apply_command(self, command):
        """Apply one command inside the caller's write transaction."""
        state, result = evolve(self.state(), command)
        entry = dict(revision=state["revision"], tick=state["tick"], command=command,
                     result=result, state_digest=digest(state))
        self.db.execute("UPDATE simulation SET state=? WHERE slot=1", (encoded(state),))
        self.db.execute("INSERT INTO journal VALUES (?,?)", (state["revision"], encoded(entry)))
        return result

    def advance(self, hours, planner=None, *, actors=(), limit=0):
        require(integer(hours, 0, MAX_CATCH_UP), "catch_up_limit")
        require(integer(limit, 0, 1000), "decision_budget")
        turns = 0
        for _ in range(hours):
            result = self.command(dict(kind="tick"))
            require(result["accepted"], "clock_transaction_failed")
            if planner is None or turns >= limit:
                continue
            state = self.state()
            for actor in actors:
                p = state["people"][actor]
                due = state["wake"].get(actor)
                if due is None and p["goal"] is not None:
                    continue
                if p["plan"] or p["transit"] or p["ready"] > state["tick"] or (due is not None and due > state["tick"]):
                    continue
                obs = observation(state, actor)
                try:
                    proposal, evidence = planner(obs, lambda steps, target: forecast(state, actor, steps, target))
                    source = "model"
                except (TimeoutError, ValueError, OSError, RuntimeError) as error:
                    proposal, evidence = None, dict(error=str(error))
                    source = "unavailable"
                self.command(dict(kind="decision", actor=actor, observed_revision=obs["revision"],
                                  observation=obs, proposal=proposal, source=source, evidence=evidence))
                turns += 1
                if turns >= limit:
                    break
                state = self.state()
        return turns

    def close(self):
        self.db.close()

    def verify_replay(self):
        state, entries = self.snapshot()
        rebuilt = replay(entries)
        require(digest(rebuilt) == digest(state), "snapshot_replay_diverged")
        return rebuilt["revision"]


def replay(entries):
    require(bool(entries) and "initial" in entries[0], "missing_replay_baseline")
    state = entries[0]["initial"]
    require(state["version"] == 1, "unsupported_simulation_schema")
    validate(state)
    for record in entries[1:]:
        state, result = evolve(state, record["command"])
        require(state["revision"] == record["revision"] and state["tick"] == record["tick"]
                and result == record["result"] and digest(state) == record["state_digest"],
                f"replay_diverged_at_{record['revision']}")
    return state
