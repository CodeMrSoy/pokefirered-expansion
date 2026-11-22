"""Exercise the expanded scheduler, observation boundaries and checkpoint migration."""

import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
from time import perf_counter

APP = Path(__file__).resolve().parents[1] / "experiments" / "living_world"
sys.path.insert(0, str(APP))

from bridge import Conversation, validate
from hybrid import FieldHint
from kanto import KantoCatalog, dialogue, residents as kanto_residents
from platform_io import publish_monitor
from population import DAY, TRANSITIONS, residents
from world import WorldMemory


def test(directory):
    catalog_path = directory / "catalog.sqlite3"
    subprocess.run([sys.executable, "-B", APP / "build-knowledge.py", catalog_path], check=True)
    catalog = KantoCatalog(catalog_path)
    legacy = residents()
    roster = (*legacy, *kanto_residents(catalog))
    path = directory / "test.sqlite3"
    first = WorldMemory(path, "main.sav", b"base")
    first.population.tick(DAY + 36000)
    first.close()
    world = WorldMemory(path, "main.sav", b"base", roster=roster)
    pop = world.population
    assert len(pop.state["actors"]) == len(roster) == 36
    assert len(catalog.nearby("mt_moon")) > 8
    assert "gym:leader" in {fact["key"] for fact in catalog.local_facts("misty")}
    assert catalog.local_facts("viridianforest/boy") == ()
    assert not any(fact["key"].startswith("gym:") for fact in catalog.local_facts("blue"))
    encounter = Conversation("route3/youngster", 25)
    first_line = dialogue(catalog, world, pop, encounter)
    assert validate(json.dumps({"action": "SAY_DIALOGUE", "text": first_line}))
    world.checkpoint(b"new")
    world.remember_kanto(encounter)
    world.remember_kanto(encounter)
    assert "You two are back." in dialogue(catalog, world, pop, encounter)
    assert world.knowledge(encounter.npc, 25)[0]["source"] == "visible_follower"
    assert not world.knowledge("ceruleancity/baldingman", 25)

    highwater = 0
    clock_start = perf_counter()
    step_count = 0
    offsets = sorted({p.shift + i for p in roster for i in (0, 24)})
    for day in range(1, 27):
        for offset in offsets:
            while True:
                count = pop.tick(DAY * day + offset)
                step_count += count
                assert count <= TRANSITIONS
                highwater = max(highwater, len(pop.queue))
                if count < TRANSITIONS:
                    break
    sim_ms = (perf_counter() - clock_start) * 1000
    assert highwater == len(roster)
    active = [person for person in roster if person.partner]
    assert sum(bool(pop.state["actors"][person.id]["facts"]) for person in active) >= 8
    for person in active:
        actor = pop.state["actors"][person.id]
        assert actor["location"] == person.home
        assert all(fact["source"] == person.partner and fact["kind"] == "reported"
                   for fact in actor["facts"].values())
        assert len(actor["memory"]) <= 8
    assert len(pop.state["events"]) <= 48 and len(pop.state["requests"]) <= 24
    ref = pop.state["actors"][encounter.npc]
    prior = dialogue(catalog, world, pop, encounter)
    assert ref["facts"] and "helped with my notes." in prior
    publish_monitor(directory, world, FieldHint(1, 25, "route_3", 0, None, False), pop,
                    False, (), "main.sav", kanto=catalog)
    monitor = json.loads((directory / "monitor.json").read_bytes())
    assert "kanto_district" in monitor and len(monitor["host_only_residents"]) == 24
    row = next(row for row in monitor["kanto_district"]["identities"] if row["id"] == encounter.npc)
    assert row["tier"] == 2 and row["player_memory"] == [25]
    assert row["activity_state"]["facts"] == ref["facts"]
    world.close()
    world = WorldMemory(path, "main.sav", b"new", roster=roster)
    assert prior == dialogue(catalog, world, world.population, encounter)
    world.checkpoint(b"base")
    assert not world.knowledge(encounter.npc, 25)
    world.close()
    print(f"PASS 36 residents, 26 days, {step_count} transitions in {sim_ms:.1f} ms, "
          f"queue high-water {highwater}, {path.stat().st_size} bytes")


if __name__ == "__main__":
    with TemporaryDirectory() as directory:
        test(Path(directory))
