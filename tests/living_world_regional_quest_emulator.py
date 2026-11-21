"""Classic/Quantum Survey Notes UI and preservation of the native record."""
import json
import pathlib
import sys
from tempfile import TemporaryDirectory

source = pathlib.Path(__file__).with_name("pokeglass_bag_quest_qc_emulator.py")
exec(compile(source.read_text().split("# Discover the optional quest")[0], str(source), "exec"))
sys.path.insert(0, str(m.root / "experiments/living_world"))
from bridge import DialogueBridge, validate
from dynamic_quests import project_regional, regional_exchange
from population import DAY, TRANSITIONS
from world import WorldMemory

maps = json.loads((m.root / "data/maps/map_groups.json").read_text())
mailbox = m.symbols["gLivingWorldMailbox"]
address = m.symbols["gLivingWorldRegionalQuestView"]
bridge = DialogueBridge(m.read, m.write, mailbox, deferred=True)


def museum_position(x, y):
    for group, key in enumerate(maps["group_order"]):
        if "PewterCity_Museum_1F" in maps[key]:
            number = maps[key].index("PewterCity_Museum_1F")
            m.inject(b"\x39" + struct.pack("<BBBhh", group, number, 255, x, y) + b"\x27\x6b\x02")
            return
    raise AssertionError("Unknown public Museum map")


def exchange_in_game(population, actor, x, y):
    museum_position(x, y)
    m.press(4, 20)
    m.keys.add(8)
    for frame in range(480):
        m.run(1)
        m.keys.discard(8)
        if m.read(mailbox, 4) == b"LQW1":
            break
        if frame % 40 == 30:
            m.keys.add(8)
    else:
        raise AssertionError(f"No Museum exchange from {actor}")

    def reply(context):
        assert context.npc == "society_" + actor, context
        message = regional_exchange(population, actor)
        return json.dumps({"action": "SAY_DIALOGUE", "text": message})

    trace = bridge.poll(reply)
    assert trace and trace["validation"] == "accepted", trace
    result = regional_exchange(population, actor, accepted=True)
    m.write(address, project_regional(population))
    for _ in range(12):
        if m.read(m.symbols["sGlobalScriptContextStatus"], 1) == b"\x02":
            break
        m.press(8, 40)
    else:
        raise AssertionError("Museum encounter left its script active")
    bridge.poll(reply)
    return result


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
    assert "added" in exchange_in_game(population, "assistant", 5, 6)
    assert "is open" in exchange_in_game(population, "assistant", 5, 6)
    objective = population.state["objective"]["event"]
    memory.checkpoint(b"survey")
    m.write(address, project_regional(population))
    m.press(3)
    wait_task("Task_PokeGlassHub")
    m.press(6, 30)  # Page one Pokédex -> page two Quest Book.
    assert m.read(m.symbols["sHubCursor"], 1) == b"\x0d"
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
    m.press(0, 30)
    wait_task("Task_PokeGlassHub")
    m.press(0, 90)
    assert "Thanks" in exchange_in_game(population, "researcher", 2, 5)
    assert "complete" in exchange_in_game(population, "assistant", 5, 6)
    m.press(3)
    wait_task("Task_PokeGlassHub")
    assert m.read(m.symbols["sHubCursor"], 1) == b"\x0d"
    m.press(8)
    wait_task("Task_GlassQuestBook")
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
