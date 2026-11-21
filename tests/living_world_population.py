"""Regression tests for regional schedules, goals and save branches."""
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "experiments/living_world"))
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


if __name__ == "__main__":
    with TemporaryDirectory() as directory:
        checkpoint_test(Path(directory) / "world.sqlite")
        event_test(Path(directory) / "events.sqlite")
        demo_test(Path(directory) / "demo.sqlite")
    print("PASS 24 residents, multi-day goal, checkpoint fork and backward-clock guard, autonomous regional events and provenance")
