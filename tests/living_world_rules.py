"""Validate native registries, fail-closed transformations and transactional save scope."""

import json
from pathlib import Path
import re
import sqlite3
import sys
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "experiments/living_world"))
from world import WorldMemory
from world_rules import (BASE, CENTERS, CLASSIC_CAPS, KANTO_GYMS, MARTS, PROJECTS,
                         QUANTUM_CAPS, RESERVED_CRESTS, Change, apply_decision, team_ceiling)


def registries():
    maps = ROOT / "data/maps"
    retired = json.loads((ROOT / "data/quantum/retired_content.json").read_bytes())["retired_maps"]
    for area in CENTERS:
        name = f"{area}_PokemonCenter_1F"
        source = (maps / name / "scripts.inc").read_text()
        assert name not in retired and "EventScript_PkmnCenterNurse" in source, name
    for name in MARTS.values():
        assert name not in retired and "pokemart " in (maps / name / "scripts.inc").read_text(), name
    for i, town in enumerate(KANTO_GYMS.values(), 1):
        script = (maps / f"{town}_Gym/scripts.inc").read_text()
        assert f"FLAG_BADGE{i:02d}_GET" in script, town
        assert "trainerbattle" in script
    source = (ROOT / "src/caps.c").read_text().split("u32 i;")[0]
    assert tuple(map(int, re.findall(r", (\d+)\},", source))) == tuple(QUANTUM_CAPS.values())
    source = (ROOT / "src/caps.c").read_text().split("sClassicCaps[] = {", 1)[1].split("}", 1)[0]
    assert tuple(map(int, source.split(","))) == tuple(CLASSIC_CAPS.values())[:-1]
    assert "TRAINER_HAVORA_CAPTAIN" in (maps / "Havora_Gym/scripts.inc").read_text()
    assert set(RESERVED_CRESTS) <= QUANTUM_CAPS.keys()
    assert team_ceiling("quantum", "cody", 79, [78, 79])
    assert team_ceiling("classic", "koga", 43, [43])
    assert not team_ceiling("quantum", "koga", 43, [43])
    assert not team_ceiling("quantum", "misty", 14, [21])
    assert not team_ceiling("classic", "brock", 14, [True, 14])
    assert not team_ceiling("classic", "brock", 14, [14] * 7)


def transaction(root):
    db = root / "memory.sqlite"
    world = WorldMemory(db, "save", b"original")
    rules = world.rules
    rules.observe(100, False)
    assert rules.decision() is None and not rules.endorse()
    rules.observe(100, True)
    rules.observe(147, True)
    first = rules.decision()
    for action in ("delete_gym", "remove_healing", "close_mart", "set_badge", "level:100",
                   "teleport_resident", "replace_warps", "disable_cut", "overwrite_save"):
        assert not rules.submit(Change(world.save, first.number, first.actor, action), "qwen")
        assert rules.state["projects"] == BASE
    assert not rules.submit(Change("other-save", first.number, first.actor, first.options[0]), "qwen")
    world.db.execute("""
        CREATE TEMP TRIGGER test_abort BEFORE UPDATE ON world_changes
        BEGIN
           SELECT RAISE(ABORT, 'test write failure');
        END
    """)
    try:
        apply_decision(rules, first, first.options[0], "qwen")
    except sqlite3.IntegrityError:
        pass
    else:
        raise AssertionError("Transaction did not roll back")
    assert rules.state["projects"] == BASE and rules.state["revision"] == 0
    world.db.execute("DROP TRIGGER test_abort")
    assert rules.endorse()
    assert not apply_decision(rules, first, first.options[0], "qwen")
    world.checkpoint(b"endorsed")
    assert rules.decision() is None
    world.checkpoint(b"working")
    for second in (150, 270):
        rules.observe(second, True)
        ticket = rules.decision()
        assert ticket
        assert apply_decision(rules, ticket, ticket.fallback, "fallback")
    assert rules.state["projects"]["mart"] == "counter_apprentice"
    assert rules.state["projects"]["gym"] in PROJECTS["gym"]
    world.checkpoint(b"grown")
    world.close()
    world = WorldMemory(db, "save", b"grown")
    assert world.rules.state["projects"]["mart"] == "counter_apprentice"
    world.checkpoint(b"endorsed")
    assert world.rules.state["projects"] == BASE
    world.checkpoint(b"grown")
    with world.db:
        world.db.execute("UPDATE world_changes SET data=? WHERE save=?", ('{"broken":[]}', world.save))
    world.rules.load()
    assert world.rules.quarantined and world.rules.monitor()["state"]["projects"] == BASE
    world.close()
    isolated = WorldMemory(db, "different", b"grown")
    assert isolated.rules.state["projects"] == BASE
    isolated.close()


def simulate(seed):
    world = WorldMemory(":memory:", "replay", bytes([seed]))
    rules = world.rules
    rules.observe(100, True)
    result = []
    for second in (150, 250, 350):
        rules.observe(second, True)
        if ticket := rules.decision():
            assert apply_decision(rules, ticket, ticket.fallback, "fallback")
            result.append((ticket.actor, ticket.fallback))
    world.close()
    return tuple(result)


if __name__ == "__main__":
    registries()
    with TemporaryDirectory() as tmp:
        transaction(Path(tmp))
    histories = [simulate(seed) for seed in range(32)]
    assert histories == [simulate(seed) for seed in range(32)]
    assert len(set(histories)) >= 6
    print(f"PASS native registries, adversarial actions, rollback, migration, player endorsement; {len(set(histories))} histories across 32 seeds")
