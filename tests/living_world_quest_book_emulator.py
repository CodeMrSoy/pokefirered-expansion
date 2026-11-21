"""Open the real V3 Quest Book and verify the separate live projection."""
import pathlib
import sys
import struct

source_path = pathlib.Path(__file__).with_name("pokeglass_bag_quest_qc_emulator.py")
exec(compile(source_path.read_text().split("# Discover the optional quest")[0], str(source_path), "exec"))
sys.path.insert(0, str(m.root / "experiments/living_world"))
from director import TRIP
from dynamic_quests import QUEST_VIEW, project_brock
from world import WorldMemory

memory = WorldMemory(":memory:", "book", b"fresh")
director = memory.director
second = 11 * 3600
director.observe(second, "pewter", False)
director.submit(director.decision(), TRIP)
address = m.symbols["gLivingWorldQuestView"]
assert not any(project_brock(director)), "Undiscovered activity became a quest"
assert director.message("brock_attendant", accepted=True)
m.write(address, project_brock(director))
m.write(m.symbols["sHubCursor"], b"\x0d")
m.press(3)
wait_task("Task_PokeGlassHub")
m.press(8)
wait_task("Task_GlassQuestBook")
m.run(40)
def rows():
    count = m.read(m.symbols["sQuestCount"], 1)[0]
    return m.read(m.symbols["sQuestIds"], count) if count else b""
assert 254 in rows()
record = m.read(ptr("gSaveBlock2Ptr") + 3803, 144)
m.press(4, 30)
m.snap("phase9-book-seeking")
m.press(8, 20)
assert not task_active("Task_GlassQuestOffer"), "Runtime-only objective uses the static mutation path"
director.observe(second + 12, "pewter", False)
director.message("brock_contact", accepted=True)
m.write(address, project_brock(director))
m.run(40)
assert m.read(m.symbols["sLivingQuestView"], 1) == b"\x03"
m.snap("phase9-book-complete")
m.press(8, 20)
assert m.read(ptr("gSaveBlock2Ptr") + 3803, 144) == record
m.write(address, QUEST_VIEW.pack(b"LWQ9", 99, 1, 3, 0))
m.run(30)
assert 254 not in rows(), "Malformed source should hide the projection"
m.press(0)
wait_task("Task_PokeGlassHub")
m.press(0)
assert field()
assert native("QuestBook_GetDefinition", 254) == 0
memory.close()
print(f"PASS mode {mode}: dynamic row activates, updates, rejects malformed evidence and leaves all static record bytes intact")
