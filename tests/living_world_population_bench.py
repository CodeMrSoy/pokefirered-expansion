"""Scale deterministic residents separately from real shared-worker decisions."""
from dataclasses import replace
import json
import os
from pathlib import Path
import statistics
import sys
from tempfile import TemporaryDirectory
from time import perf_counter, process_time
import tracemalloc

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "experiments/living_world"))
from inference import LocalModel
from population import DAY, TRANSITIONS, Population, choose_commitment, residents
from world import WorldMemory


def simulation(path, count):
    memory = WorldMemory(path, "scale", b"start")
    base = residents()
    roster = tuple(replace(base[i % len(base)], id=f"resident-{i}") for i in range(count))
    run = Population(memory, roster)
    tracemalloc.start()
    cpu = process_time()
    samples = []
    completed = 0
    for day in range(1, 41):
        for hour in range(9, 14):
            for offset in (0, 24, 360):
                state = day * DAY + hour * 3600 + offset
                transitions = TRANSITIONS
                while transitions == TRANSITIONS:
                    start = perf_counter()
                    transitions = run.tick(state)
                    samples.append((perf_counter() - start) * 1000)
                    completed += transitions
    cpu = process_time() - cpu
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    assert len(run.state["actors"]) == count
    assert len(run.state["events"]) <= 48 and len(run.state["requests"]) <= 24
    assert all(len(actor["memory"]) <= 8 and len(actor["bonds"]) <= 12
               for actor in run.state["actors"].values())
    assert len(run.queue) == count
    print(json.dumps(dict(residents=count, days=40, transitions=completed, calls=0, cpu_s=round(cpu, 3),
                          p95_ms=round(statistics.quantiles(samples, n=20)[18], 3),
                          peak_kib=round(peak/1024), database_kib=path.stat().st_size//1024)))
    memory.close()


def contention(model=None):
    memory = WorldMemory(":memory:", "contention", b"start")
    run = memory.population
    run.model_decisions = True
    now = DAY + 9 * 3600
    run.tick(now)
    # A burst of simultaneous legal requests reaches the attention budget.
    people = list(person for person in run.people.values() if person.role == "researcher")
    for person in people:
        owner = run.state["actors"][person.id]
        owner["goal"] = run.start_goal(person, owner, now)
        run.supplement(person, owner, now)
    for request in tuple(run.state["requests"].values()):
        recipient = request["recipient"]
        run.respond(run.people[recipient], run.state["actors"][recipient], now)
    pending = [req for req, r in run.state["requests"].items() if "decision" in r]
    assert len(pending) == 3
    first = run.decision()
    assert first
    queue = []
    batch_ready = perf_counter()
    while ticket := run.decision():
        queue.append(ticket.actor)
        if model:
            submitted = perf_counter()
            choice, metrics = choose_commitment(model, ticket)
            print(json.dumps(dict(resident=ticket.actor, choice=choice, wall_ms=round((perf_counter()-submitted)*1000, 1),
                                  service_wait_ms=round((submitted-batch_ready)*1000, 1),
                                  **metrics)))
        else:
            choice = "CONTINUE" if len(queue) % 2 == 0 else "HELP"
        run.submit(ticket, choice)
    assert len(set(queue)) == 3
    try:
        run.submit(first, "HELP")
    except ValueError:
        pass
    else:
        raise AssertionError("decision replayed")
    print(json.dumps(dict(requests=len(people), queued=len(pending), distinct=len(set(queue)),
                          real_calls=len(queue) if model else 0)))
    memory.close()


if __name__ == "__main__":
    folder = os.environ.get("LIVING_WORLD_PHASE5_RUNTIME")
    if folder:
        model = LocalModel(Path(folder), {}, style="qwen3", natural=True)
        try:
            contention(model)
        finally:
            model.close()
    else:
        contention()
        with TemporaryDirectory() as temp:
            for size in (20, 50, 100, 250):
                simulation(Path(temp) / f"{size}.sqlite", size)
