"""Two discovered quest categories coexist without writing the native save."""
import pathlib
import sys
from tempfile import TemporaryDirectory

source_path = pathlib.Path(__file__).with_name("pokeglass_bag_quest_qc_emulator.py")
exec(compile(source_path.read_text().split("# Discover the optional quest")[0], str(source_path), "exec"))
sys.path.insert(0, str(m.root / "experiments/living_world"))
from bridge import validate
from director import TRIP
from dynamic_quests import museum_exchange, project_brock, project_museum
from world import WorldMemory
import json

with TemporaryDirectory() as folder:
    path = pathlib.Path(folder) / "museum.sqlite"
    memory = WorldMemory(path, "museum", b"first")
    director, world = memory.director, memory.society
    now = 39600
    world.tick(now, "pewter")
    ticket = world.decision("researcher")
    plan = next(plan for plan in ticket.choices if plan[-1].action == "REQUEST_ASSISTANCE")
    world.submit(ticket, plan)
    world.tick(now+32,"viridian")
    world.tick(now+36,"viridian")
    assert not any(project_museum(world))
    validate(json.dumps({"action": "SAY_DIALOGUE", "text": museum_exchange(world,"assistant")}))
    assert museum_exchange(world,"assistant",accepted=True)
    memory.checkpoint(b"new")
    memory.close()
    memory = WorldMemory(path, "museum", b"new")
    director, world = memory.director, memory.society
    assert project_museum(world)[8] == 1
    director.observe(now, "pewter", False)
    director.submit(director.decision(), TRIP)
    assert director.message("brock_attendant", accepted=True)
    m.write(m.symbols["gLivingWorldQuestView"], project_brock(director))
    address = m.symbols["gLivingWorldMuseumQuestView"]
    m.write(address, project_museum(world))
    m.write(m.symbols["sHubCursor"], b"\x0d")
    m.press(3)
    wait_task("Task_PokeGlassHub")
    m.press(8)
    wait_task("Task_GlassQuestBook")
    m.run(40)
    count = m.read(m.symbols["sQuestCount"], 1)[0]
    rows = m.read(m.symbols["sQuestIds"], count)
    assert bytes((254,253)) == rows[-2:]
    record = m.read(ptr("gSaveBlock2Ptr") + 3803, 144)
    m.press(4, 30)
    m.snap("phase10-museum-quest-active")
    m.press(8, 20)
    assert not task_active("Task_GlassQuestOffer")
    assert museum_exchange(world, "researcher", accepted=True)
    m.write(address, project_museum(world))
    m.run(40)
    assert m.read(m.symbols["sMuseumQuestView"], 1) == b"\x03"
    m.snap("phase10-museum-quest-completed")
    assert m.read(ptr("gSaveBlock2Ptr") + 3803, 144) == record
    memory.close()
    memory = WorldMemory(path, "museum", b"first")
    assert project_museum(memory.society)[8] == 1
    world = memory.society
    event = world.state["museum_objective"]["event"]
    memory.checkpoint(b"npc-resolution")
    actor = world.decision("assistant")
    world.submit(actor, actor.choices[1])
    while active := world.state["agents"]["assistant"]["active"]:
        world.tick(active["due"], "route_2")
    assert project_museum(world)[8] == 3
    del world.state["requests"][event]
    assert project_museum(world)[8] == 3
    memory.close()
    memory = WorldMemory(path, "museum", b"first")
    world = memory.society
    world.tick(world.state["requests"][event]["expires"], "route_2")
    assert project_museum(world)[8] == 4
    memory.close()
print(f"PASS mode {mode}: two dynamic categories, independent save projection, delivery and expiry")
