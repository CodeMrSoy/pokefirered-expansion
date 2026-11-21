"""Verified waypoints in the initial regional travel graph.

Museum is the public exhibit wing. Route 2 is the open north road. The
bridge projects endpoint slots only, while intermediate legs stay offscreen.
"""
from collections import deque

EDGES = {
    "museum": {"pewter": 12},
    "pewter": {"museum": 12, "route_2": 16},
    "route_2": {"pewter": 16},
}
TRAVEL_PERMISSIONS = {
    "researcher": frozenset(EDGES),
    "trainer": frozenset(("pewter", "route_2")),
}
RESEARCHER_PRESENCE = {"museum": 0, "in_transit": 1, "pewter": 2, "route_2": 3}
TRAINER_PRESENCE = {"pewter": 0, "in_transit": 1, "route_2": 2}


def route(actor, origin, destination):
    known = TRAVEL_PERMISSIONS.get(actor, frozenset())
    if {origin, destination} - known or origin == destination:
        return None
    queue = deque([(origin, (), 0)])
    seen = {origin}
    while queue:
        current, legs, duration = queue.popleft()
        for neighbor, seconds in EDGES[current].items():
            if neighbor in seen or neighbor not in known:
                continue
            path = (*legs, neighbor)
            if neighbor == destination:
                return path, duration + seconds
            seen.add(neighbor)
            queue.append((neighbor, path, duration + seconds))
    return None
