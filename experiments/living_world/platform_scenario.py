"""Canonical cross-platform trace of validated Living World transitions."""

import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory

from bridge import validate
from dynamic_quests import project_regional, regional_exchange
from platform_io import atomic_write, backup_profile, profile_lock, publish_monitor
from population import DAY
from world import WorldMemory


def scenario(directory):
    slot = "Phase11RegionalSociety.sav"
    database = directory / "living-world.sqlite3"
    start = 5 * DAY + 12 * 3600
    world = WorldMemory(database, slot, b"initial")
    population = world.population
    population.initialize(start)
    population.state["clock"] = start
    trace = []

    def contact(actor, accepted):
        text = regional_exchange(population, actor, accepted=accepted)
        trace.append(text)
        validate(json.dumps({"action": "SAY_DIALOGUE", "text": text}))

    def offer(id_, owner):
        population.event(id_, "survey_support", owner, start, audience="museum_desk")
        contact("assistant", False)
        contact("assistant", True)
        trace.append(project_regional(population).hex())

    offer("survey:one", "ada")
    contact("assistant", True)
    world.checkpoint(b"open")
    world.checkpoint(b"delivered")
    contact("researcher", True)
    contact("assistant", True)
    trace.append(project_regional(population).hex())
    offer("survey:two", "gail")
    population.close_event("survey:two", "completed", start, "quin")
    contact("assistant", True)
    trace.append(project_regional(population).hex())
    offer("survey:three", "mina")
    population.state["requests"]["survey:three"] = {"owner": "mina", "deadline": start + 1}
    population.tick(start + 1)
    trace.append(project_regional(population).hex())
    publish_monitor(directory, world, None, population, False, (), slot)
    snapshot = json.loads((directory / "monitor.json").read_text(encoding="ascii"))
    assert len(snapshot["host_only_residents"]) == 24
    assert snapshot["dynamic_quests"]["Survey Notes"]["status"] == "expired"
    world.close()

    for battery, status in ((b"open", 1), (b"delivered", 4)):
        world = WorldMemory(database, slot, battery)
        view = project_regional(world.population)
        assert view[8] == status
        trace.append(view.hex())
        world.close()

    atomic_write(directory / slot, b"delivered")
    with profile_lock(directory):
        try:
            backup_profile(directory)
        except RuntimeError:
            pass
        else:
            raise AssertionError("Backup bypassed the running game's lock")
    from zipfile import ZipFile
    with ZipFile(backup_profile(directory)) as archive:
        assert archive.read(slot) == b"delivered"
        assert archive.testzip() is None
        assert database.name in archive.namelist()

    return {"schema": 1, "transitions": trace}


if __name__ == "__main__":
    with TemporaryDirectory() as folder:
        output = json.dumps(scenario(Path(folder)), indent=2) + "\n"
    Path(sys.argv[1]).write_bytes(output.encode("ascii"))
