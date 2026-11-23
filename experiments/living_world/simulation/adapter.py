"""Read-only projection seam for a future native bridge consumer."""

from copy import deepcopy

from world_rules import CLASSIC_CAPS, QUANTUM_CAPS


def project(world, native_map):
    """Return host presentation records plus an explicit native authority marker."""
    return deepcopy(dict(
        simulation_revision=world["revision"], native_map=native_map, authority="host_preview",
        residents=[dict(identity=key, name=p["name"], native_object=p["native"],
                        employer=p["employer"], ambition=p["goal"]["ambition"] if p["goal"] else None)
                   for key, p in world["people"].items() if p["location"] == native_map
                   and not p["transit"] and p["controller"] == "npc"],
        businesses={key: dict(name=f["name"], owner=f["owner"], kind=f["kind"])
                    for key, f in world["firms"].items() if f["location"] == native_map},
        events={key: e for key, e in world["events"].items() if e["location"] == native_map},
    ))


def native_progression_policy():
    """Reference for the inspector. Native code is responsible for battle entry."""
    return dict(authority="rom", classic=dict(CLASSIC_CAPS), quantum=dict(QUANTUM_CAPS))
