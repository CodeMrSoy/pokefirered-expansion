"""Earn the first Survey Notes request from the scheduler and follow it to reload."""

import json
from pathlib import Path
import sys
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "experiments/living_world"))
from bridge import validate
from dynamic_quests import project_regional, regional_exchange
from platform_io import publish_monitor
from population import DAY, TRANSITIONS
from world import WorldMemory


def run(directory):
    database = directory / "world.sqlite"
    save_slot = "Phase11RegionalSociety.sav"
    world = WorldMemory(database, save_slot, b"before-survey")
    population = world.population
    timeline = []
    event_id = None

    def observe(stage):
        publish_monitor(directory, world, None, population, False, (), save_slot)
        snapshot = json.loads((directory / "monitor.json").read_bytes())
        objective = snapshot["dynamic_quests"]["Survey Notes"]
        event = snapshot["survey_event"] if objective else dict(snapshot["recent_events"])[event_id]
        residents = {actor["name"]: actor for actor in snapshot["host_only_residents"]}
        assert len(residents) == 24
        result = {"stage": stage, "id": event_id, "origin": event["origin"],
                  "source": event["source"], "event": event["status"],
                  "quest": objective["status"] if objective else None,
                  "projected_status": project_regional(population)[8]}
        if event["status"] == "active":
            assert snapshot["pending_resident_requests"][event_id]["owner"] == event["origin"]
        elif event["status"] == "completed":
            assert event_id not in snapshot["pending_resident_requests"]
            owner = population.people[event["origin"]].name
            assert residents[owner]["facts"]["volunteer"]["source"] == event["source"]
        timeline.append(result)

    def tick(second):
        while population.tick(second) == TRANSITIONS:
            pass

    for day in range(1, 8):
        for hour in range(9, 15):
            for offset in (0, 24):
                tick(day * DAY + hour * 3600 + offset)
                if event_id is None:
                    event_id = next((id_ for id_, event in population.state["events"].items()
                                     if event["kind"] == "survey_support" and event["status"] == "active"), None)
                    if event_id is not None:
                        observe("npc-request")
                        notice = regional_exchange(population, "assistant")
                        assert notice and "Survey Notes added" in notice
                        validate(json.dumps({"action": "SAY_DIALOGUE", "text": notice}))
                        assert regional_exchange(population, "assistant", accepted=True) == notice
                        assert "is open" in regional_exchange(population, "assistant", accepted=True)
                        assert population.state["objective"]["event"] == event_id
                        observe("player-discovery")
                        world.checkpoint(b"with-survey")
                elif population.state["objective"]["status"] != "active":
                    break
            else:
                continue
            break
        else:
            continue
        break
    assert event_id and population.state["objective"]["status"] == "completed"
    observe("npc-cooperation")
    assert "found help" in regional_exchange(population, "assistant", accepted=True)
    world.checkpoint(b"completed-survey")
    world.close()

    world = WorldMemory(database, save_slot, b"completed-survey")
    population = world.population
    observe("after-reload")
    world.close()
    assert [row["projected_status"] for row in timeline] == [0, 1, 3, 3]
    assert timeline[2] == {**timeline[3], "stage": "npc-cooperation"}
    return timeline


if __name__ == "__main__":
    with TemporaryDirectory() as directory:
        print(json.dumps(run(Path(directory)), indent=2))
