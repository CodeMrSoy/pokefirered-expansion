"""Regression tests for regional schedules, goals and save branches."""
import json
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "experiments/living_world"))
from bridge import validate
from dynamic_quests import project_regional, regional_exchange
from population import DAY, TRANSITIONS
from world import WorldMemory


def through(population, second):
    while population.tick(second) == TRANSITIONS:
        pass


def checkpoint_test(db):
    game = WorldMemory(db, "regional", b"initial")
    day = DAY + 12 * 3600
    through(game.population, day)
    through(game.population, day + 24)
    actors = game.population.state["actors"]
    assert len(actors) == 24
    original = actors["ada"]["goal"].copy()
    assert original["progress"] == 1
    game.checkpoint(b"later")
    through(game.population, day + DAY)
    through(game.population, day + DAY + 24)
    goal = game.population.state["actors"]["ada"]["goal"]
    assert goal["id"] == original["id"] and goal["progress"] == 2
    game.close()
    early = WorldMemory(db, "regional", b"initial")
    assert early.population.state["actors"]["ada"]["goal"] == original
    assert early.population.tick(0) == 0
    early.close()
    later = WorldMemory(db, "regional", b"later")
    assert later.population.state["actors"]["ada"]["goal"]["progress"] == 2
    later.close()


def event_test(db):
    w = WorldMemory(db, "events", b"start")
    seen = set()
    for day in range(1, 10):
        for hour in range(9,15):
            for offset in (0,24):
                through(w.population, day*DAY+hour*3600+offset)
                seen.update((e["kind"],e["status"]) for e in w.population.state["events"].values())
    assert ("survey_support", "active") in seen
    assert ("survey_support", "completed") in seen
    assert ("training_milestone", "completed") in seen
    assert len(w.population.state["events"]) <= 48
    assert any(f["kind"] == "reported" for a in w.population.state["actors"].values() for f in a["facts"].values())
    w.close()


def demo_test(db):
    memory = WorldMemory(db, "demo", b"early")
    run = memory.population
    run.demo_tick(39600)
    assert run.state["demo_anchor"] == 39600
    assert len(run.state["actors"]) == 24
    assert run.state["actors"]["ada"]["goal"]["progress"] == 2
    for second in range(39601, 39790):
        run.demo_tick(second)
    assert any(event["kind"] == "survey_support" for event in run.state["events"].values())
    memory.checkpoint(b"later")
    clock = run.state["clock"]
    memory.close()
    memory = WorldMemory(db, "demo", b"later")
    assert memory.population.state["clock"] == clock
    memory.population.demo_tick(39800)
    assert memory.population.state["clock"] > clock
    memory.close()


def survey_lifecycle_test(db):
    def open_save(battery):
        game = WorldMemory(db, "survey", battery)
        return game, game.population

    def speak(actor, accepted=False):
        message = regional_exchange(population, actor, accepted=accepted)
        if message:
            validate(json.dumps({"action": "SAY_DIALOGUE", "text": message}))
        return message

    game, population = open_save(b"start")
    start = DAY + 9 * 3600
    through(population, start)
    population.event("first", "survey_support", "ada", start, audience="museum_desk")
    assert "added" in speak("assistant")
    assert project_regional(population) == bytes(12)
    assert "added" in speak("assistant", True)
    first = project_regional(population)
    assert first[8] == 1 and "is open" in speak("assistant", True)
    game.checkpoint(b"delivered")
    assert "Thanks" in speak("researcher", True)
    assert population.state["events"]["first"]["status"] == "active"
    assert population.state["events"]["first"]["notice_delivered"] == start
    assert project_regional(population)[8] == 3
    game.close()

    game, population = open_save(b"delivered")
    assert "note reached" in speak("assistant", True)
    assert "complete" in speak("assistant", True)
    assert "complete" in speak("researcher", True)
    population.event("second", "survey_support", "mina", start, audience="museum_desk")
    assert "Mina" in speak("assistant", True)
    second = project_regional(population)
    assert second[4:8] != first[4:8]
    owner = population.state["actors"]["mina"]
    owner["goal"] = {"id": "survey-goal", "status": "active"}
    population.state["requests"]["second"] = {"owner": "mina", "recipient": "quin", "goal": "survey-goal"}
    population.settle_request("second", True, start)
    assert owner["facts"]["volunteer"]["source"] == "quin"
    assert owner["goal"]["verified"]
    assert "found help" in speak("researcher", True)
    assert "found help" in speak("assistant", True)
    assert not population.state["objective"].get("delivered")
    assert "complete" in speak("assistant", True)
    assert project_regional(population)[4:9] == second[4:8] + b"\x03"
    population.event("third", "survey_support", "gail", start, audience="museum_desk")
    population.state["requests"]["third"] = {"owner": "gail", "deadline": start + 1}
    assert "Gail" in speak("assistant", True)
    through(population, start + 1)
    assert "expired" in speak("researcher", True)
    assert project_regional(population)[8] == 4
    game.close()

    game, population = open_save(b"delivered")
    assert "expired" in speak("assistant", True)
    assert "expired" in speak("assistant", True)
    game.close()
    game, population = open_save(b"start")
    assert project_regional(population) == first
    assert "is open" in speak("assistant")
    game.close()


if __name__ == "__main__":
    with TemporaryDirectory() as directory:
        checkpoint_test(Path(directory) / "world.sqlite")
        event_test(Path(directory) / "events.sqlite")
        demo_test(Path(directory) / "demo.sqlite")
        survey_lifecycle_test(Path(directory) / "survey.sqlite")
    print("PASS 24 residents, multi-day goal, checkpoint fork and backward-clock guard, autonomous regional events and provenance")
