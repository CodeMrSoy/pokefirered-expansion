"""Read-only, filterable world and journal reports."""

from .adapter import native_progression_policy


def inspect(simulation, actor=None, *, history_limit=50):
    world, journal = simulation.snapshot()
    if actor is not None and actor not in world["people"]:
        raise ValueError("unknown_actor")
    entries = []
    for entry in journal[1:]:
        command = entry["command"]
        result = entry["result"]
        if command["kind"] == "tick" and result["accepted"]:
            for effect in result["effect"]:
                if actor is None or effect.get("actor") == actor:
                    entries.append(dict(tick=entry["tick"], source="scheduler", **effect))
        elif actor is None or command.get("actor") == actor:
            entries.append(entry)
    return dict(world=world if actor is None else world["people"][actor],
                progression=native_progression_policy(), timeline=entries[-history_limit:] if history_limit else [],
                timeline_count=len(entries), revision=world["revision"], tick=world["tick"])
