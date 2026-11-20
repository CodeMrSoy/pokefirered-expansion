"""Exercise save-bound memory, authorized decisions and resident worker reuse."""
from pathlib import Path
import os
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "experiments/living_world"))

from bridge import Conversation, validate
from inference import LocalModel
from world import WorldMemory

pikachu = Conversation("pc_resident", 25)
squirtle = Conversation("pc_resident", 7)
runtime = os.environ.get("LIVING_WORLD_INFERENCE_RUNTIME")
model = LocalModel(Path(runtime), {"25": "Pikachu", "7": "Squirtle"}) if runtime else None


def apply(memory, observation, expected=None):
    encounter = memory.context(observation)
    if model:
        plan = model.plan(encounter)
        validate(plan.dialogue)
        print(plan, flush=True)
        action = plan.action
        if expected:
            assert action == expected, (action, expected)
    else:
        action = expected or encounter.allowed()[0]
    return memory.apply(encounter, action), encounter


try:
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "living-world.sqlite3"
        memory = WorldMemory(path, "demo", b"initial")
        try:
            memory.apply(memory.context(pikachu), "PROPOSE_OPTIONAL_QUEST")
        except ValueError:
            pass
        else:
            raise AssertionError("Authorized a quest without a prior encounter")
        changes, old = apply(memory, pikachu)
        assert "REMEMBER_EVENT" in changes
        try:
            memory.apply(old, old.allowed()[0])
        except ValueError:
            pass
        else:
            raise AssertionError("Accepted a stale proposal")
        worker_pid = model.worker.process.pid if model else None
        memory.close()

        memory = WorldMemory(path, "demo", b"initial")
        assert memory.context(pikachu).remembered
        changes, _ = apply(memory, pikachu, "PROPOSE_OPTIONAL_QUEST")
        assert "pond_survey:offered" in changes
        changes, _ = apply(memory, pikachu)
        assert "pond_survey:completed" not in changes
        memory.checkpoint(b"saved")
        changes, _ = apply(memory, squirtle, "SAY_DIALOGUE")
        assert "pond_survey:completed" in changes
        assert memory.context(pikachu).trust >= 2
        assert apply(memory, squirtle)[0] == []
        if model:
            assert model.worker.process.pid == worker_pid
        memory.close()

        restored = WorldMemory(path, "demo", b"initial")
        assert restored.context(pikachu).quest == "offered"
        assert not restored.context(squirtle).remembered
        restored.checkpoint(b"saved")
        assert restored.context(pikachu).quest == "completed"
        restored.close()
        assert WorldMemory(path, "main", b"saved").context(pikachu).quest == "none"
finally:
    if model:
        model.close()
print("Persistent memories, stale-action rejection, quest completion, checkpoint branching and slot isolation passed.")
