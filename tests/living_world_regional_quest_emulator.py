"""Classic/Quantum Survey Notes UI and preservation of the native record."""
import json
import pathlib
import sys
from tempfile import TemporaryDirectory

source = pathlib.Path(__file__).with_name("pokeglass_bag_quest_qc_emulator.py")
exec(compile(source.read_text().split("# Discover the optional quest")[0], str(source), "exec"))
sys.path.insert(0, str(m.root / "experiments/living_world"))
from bridge import validate
from dynamic_quests import project_regional, regional_exchange
from population import DAY, TRANSITIONS
from world import WorldMemory

with TemporaryDirectory() as folder:
    path = pathlib.Path(folder) / "regional.sqlite"
    memory = WorldMemory(path, "phase11", b"start")
    population = memory.population
    notice = None
    for day in range(1, 8):
        for hour in range(9, 14):
            for offset in (0, 24):
                while population.tick(day * DAY + hour * 3600 + offset) == TRANSITIONS:
                    pass
                notice = regional_exchange(population, "assistant")
                if notice:
                    break
            if notice:
                break
        if notice:
            break
    assert notice and project_regional(population) == bytes(12)
    assert regional_exchange(population, "trainer") is None
    validate(json.dumps({"action": "SAY_DIALOGUE", "text": notice}))
    regional_exchange(population, "assistant", accepted=True)
    objective = population.state["objective"]["event"]
    memory.checkpoint(b"survey")
    address = m.symbols["gLivingWorldRegionalQuestView"]
    m.write(address, project_regional(population))
    m.write(m.symbols["sHubCursor"], b"\x0d")
    m.press(3)
    wait_task("Task_PokeGlassHub")
    m.press(8)
    wait_task("Task_GlassQuestBook")
    m.run(40)
    ids = m.read(m.symbols["sQuestIds"], m.read(m.symbols["sQuestCount"], 1)[0])
    assert ids[-1] == 252
    m.press(4, 20)
    m.snap("phase11-survey-notes-active")
    record = m.read(ptr("gSaveBlock2Ptr") + 3803, 144)
    m.press(8, 20)
    assert not task_active("Task_GlassQuestOffer")
    regional_exchange(population, "researcher", accepted=True)
    m.write(address, project_regional(population))
    m.run(40)
    assert m.read(m.symbols["sRegionalQuestView"], 1) == b"\x03"
    m.snap("phase11-survey-notes-completed")
    assert m.read(ptr("gSaveBlock2Ptr") + 3803, 144) == record
    memory.close()

    for status, code in (("expired", 4), ("withdrawn", 5), ("completed", 3)):
        memory = WorldMemory(path, "phase11", b"start")
        population = memory.population
        assert population.state["objective"]["status"] == "active"
        memory.checkpoint(status.encode())
        population.close_event(objective, status, population.state["clock"], "fixture")
        assert project_regional(population)[8] == code
        m.write(address, project_regional(population))
        m.run(12)
        assert m.read(m.symbols["sRegionalQuestView"], 1) == bytes([code])
        assert m.read(ptr("gSaveBlock2Ptr") + 3803, 144) == record
        memory.close()
print(f"PASS mode {mode}: scoped discovery, complete/expired/withdrawn projections and unchanged native quest bytes")
